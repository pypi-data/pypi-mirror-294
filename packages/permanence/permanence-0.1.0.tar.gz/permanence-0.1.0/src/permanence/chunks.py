from __future__ import annotations

import asyncio
from functools import reduce
from permanence.namespace import ScopeNamespace
from permanence.tag_type import Tagged
from .artifact import Artifact, Arty, JSONArtifact, TableArtifact
from .scope_type import RunScope

import iroh
from iroh import Iroh
import pyarrow as pa
import pyarrow.feather as ft
from uuid6 import uuid7

from io import BytesIO
import itertools
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Iterator, Iterable, Any, Literal, Optional, Protocol, Sequence

from loguru import logger


"""
# Chunk data model

Remote

"""


class TaggedArtifact(Protocol):
    artifact: Artifact
    tag: Tagged
    # TODO: datetime maybe? or convert via method
    logged_at: float

    def load(self) -> Any: ...


@dataclass
class TaggedLocalArtifact(TaggedArtifact):
    artifact_content: Any
    artifact: Artifact
    tag: Tagged
    logged_at: float

    def load(self):
        return self.artifact_content


@dataclass
class TaggedRemoteArtifact(TaggedArtifact):
    artifact: Artifact
    # generate "mock" scopes via attrs instead of registry?
    tag: Tagged
    logged_at: float

    def load(self):
        raise NotImplementedError()


class Chronos:
    """
    Wrapper for a chronologically ordered iterator (usually derived from a collection of TaggedArtifact via log timestamp).
    """

    def __init__(self, iterator):
        self.iterator = iterator
        self.consumed = None

    def collected(self):
        if self.consumed is not None:
            return self.consumed
        else:
            self.consumed = list(self.iterator)
            return self.consumed

    def __iter__(self):
        yield from self.collected()

    def __len__(self):
        return len(self.collected())

    @property
    def empty(self):
        return len(self) == 0

    def earliest(self):
        return self.collected()[0]

    def latest(self):
        return self.collected()[-1]

    def only(self):
        assert len(self) == 1, self.collected()
        return self.latest()


@dataclass
class LocalChunk:
    """
    Blobs are stored fully deserialised in their respective Python types:
    - Table => pyarrow.Table
    - JSON => dict
    """

    # TODO: remove default initialisers (in `new` instead)

    chunk_id: str
    "UUIDv7 identifying the chunk"

    reverse_artifacts: dict[RunScope, set[str]] = field(
        default_factory=lambda: defaultdict(lambda: set())
    )
    "Maps scopes to the set of artifact hashes logged within them"

    art_hashes: dict[str, list[Artifact]] = field(
        default_factory=lambda: defaultdict(lambda: [])
    )
    """
    Maps content hashes to matching artifacts.
    
    Although hashes uniquely (mod collisions) uniquely identify content, they're mapped to a list because `Artifact` equality also requires types to match.
    """

    art_logs: dict[Artifact, list[TaggedLocalArtifact]] = field(
        default_factory=lambda: defaultdict(lambda: [])
    )
    """
    Maps artifacts to the contexts they've been logged in.

    Values are lists because despite containing identical content (as references into art_storage) 
    the same blob can be logged multiple times under different tags.
    """

    blob_storage: dict[str, bytes] = field(default_factory=lambda: {})
    "Hash to binary blob lookup. To eventually be replaced with a global blob store/cache of calls to Iroh storage"

    @classmethod
    def new(cls):
        return cls(chunk_id=str(uuid7()))

    def copy(self):
        # Always returns LocalChunk (strips mutability)
        return LocalChunk(
            chunk_id=self.chunk_id,
            reverse_artifacts=self.reverse_artifacts.copy(),
            art_hashes=self.art_hashes.copy(),
            art_logs=self.art_logs.copy(),
            blob_storage=self.blob_storage.copy(),
        )

    def filter_scope_intersection(self, scopes: Iterable[RunScope]) -> set[Artifact]:
        """
        Finds artifacts that have been logged at least once in each of the given scopes.

        Warning! This might not do what you think it does. Because this operates on artifacts rather than instances, if scopes is `[A(), B()]` this will return artifacts logged once under A() and once separately under B(), in addition to those logged under `[A(), B()]` jointly.
        """
        scopes = list(scopes)
        if not scopes:
            return set().union(*self.art_hashes.values())

        artifact_hashes = reduce(
            set.intersection, map(self.reverse_artifacts.__getitem__, scopes)
        )
        return reduce(
            set.union, map(self.art_hashes.__getitem__, artifact_hashes), set()
        )

    def match_scope_intersection(self, match_scopes) -> list[TaggedLocalArtifact]:
        match_scopes = set(match_scopes)
        candidate_artifacts = self.filter_scope_intersection(match_scopes)
        logs_stream = itertools.chain.from_iterable(
            map(self.art_logs.__getitem__, candidate_artifacts)
        )
        matched = filter(lambda taf: taf.tag.matches_query(match_scopes), logs_stream)
        return list(matched)

    def serialise(self) -> dict[str, bytes]:
        """
        Converts into Iroh document {keys => binary blob} format.

        This does not include artifact contents which need to be sent to a content-addressed-storage backend like Iroh that can map BLAKE3 hashes to arbitrary binary content.
        """
        # TODO: Use package __version__
        metadata = {"format_version": "0.0.1"}

        # Serialise scopes
        scopes = {}

        def scope_with_hash(scope: RunScope, scope_id: str, saw_obj_hash: str):
            nonlocal scopes

            if scope_id not in scopes:
                scopes[scope_id] = {
                    "name": type(scope).__name__,
                    "content": scope.as_canonical_json(),
                    "namespace": scope.namespace(),
                    "objects": [],
                }
            scopes[scope_id]["objects"].append(saw_obj_hash)
            return scope_id

        # Serialise logs
        rows = []

        iter_artifacts = itertools.chain.from_iterable(self.art_logs.values())
        for tagged_artifact in iter_artifacts:
            artifact = tagged_artifact.artifact
            tagged = tagged_artifact.tag
            row_ser = {
                "content_binary_local": None,
                "content_binary_blake3": artifact.data_hash,
                "log_metadata": {"logged_at": tagged_artifact.logged_at},
                "artifact_name": artifact.scope_name(),
                "artifact_type": artifact.type_string(),
                "context_ids": [
                    scope_with_hash(s, h, artifact.data_hash)
                    for s, h in tagged.scope_state.items()
                ],
                "contexts_hash": tagged.hashed(),
            }

            # For small-ish values, storing inline is way faster
            if isinstance(artifact, JSONArtifact):
                row_ser["content_binary_local"] = artifact.new(
                    tagged_artifact.artifact_content
                )[0]
            rows.append(row_ser)

        # also specify reciprocal hashes to ensure batches can be matched together?
        scope_table = pa.Table.from_pylist(
            [{"context_id": k, **v} for k, v in scopes.items()], metadata=metadata
        )
        log_table = pa.Table.from_pylist(rows, metadata=metadata)

        # TODO: declare Arrow schema - to handle case of empty tables
        write_logs = BytesIO()
        with pa.ipc.new_file(write_logs, log_table.schema) as writer:
            writer.write_table(log_table)

        write_scopes = BytesIO()
        with pa.ipc.new_file(write_scopes, scope_table.schema) as writer:
            writer.write_table(scope_table)

        return {
            # TODO: more chunk/scope/session metadata?
            "contexts": write_scopes.getvalue(),
            "logs": write_logs.getvalue(),
        }

    @staticmethod
    def deserialise(
        scope_namespace: ScopeNamespace,
        doc_keys: dict[str, bytes],
        doc_blobs: dict[str, bytes],
        chunk_id: str,
    ):
        def reconstruct_scope_type(row: dict):
            if row["namespace"].startswith("."):
                # Artifact scopes get special path
                match row["namespace"].split("."):
                    case ["", "Artifact", artifact_cls]:
                        artifact_type = getattr(
                            getattr(Arty, artifact_cls), row["name"]
                        )
                        return artifact_type
                    case _:
                        raise ValueError(f"{row}: expected artifact namespace")
            else:
                return scope_namespace.registered_scopes[row["name"]]

        # TODO: return Result
        log_key = f"{chunk_id}/logs"
        scope_key = f"{chunk_id}/contexts"
        assert log_key in doc_keys
        assert scope_key in doc_keys

        log_table = ft.read_table(BytesIO(doc_keys[log_key]))
        scope_table = ft.read_table(BytesIO(doc_keys[scope_key]))

        contexts = scope_table.to_pylist()
        # TODO: reconstruct all contexts in one pass here?
        contexts = {c["context_id"]: c for c in contexts}

        builder = MutableLocalChunk.new()

        for log in log_table.to_pylist():
            match log["artifact_type"]:
                case "Table":
                    artifact_type = getattr(Arty.Table, log["artifact_name"])
                    artifact = artifact_type(
                        log["content_binary_blake3"],
                    )
                    content_blob = doc_blobs[log["content_binary_blake3"]]
                    artifact_content = artifact_type.reconstruct(content_blob)
                case "JSON":
                    artifact_type = getattr(Arty.JSON, log["artifact_name"])
                    artifact = artifact_type(
                        log["content_binary_blake3"],
                    )
                    content_blob = log["content_binary_local"]
                    artifact_content = artifact_type.reconstruct(content_blob)
                case unknown_artifact:
                    raise TypeError(f"{unknown_artifact}: unknown artifact type")

            tag = Tagged(
                {
                    reconstruct_scope_type(contexts[ctx_id]).from_canonical_json(
                        contexts[ctx_id]["content"]
                    ): ctx_id
                    for ctx_id in log["context_ids"]
                }
            )
            # TODO: load log timestamp
            tla = TaggedLocalArtifact(
                artifact_content,
                artifact,
                tag,
                log["log_metadata"].get("logged_at", 0.0),
            )
            builder.append(content_blob, tla)

        return builder.copy()


class MutableLocalChunk(LocalChunk):
    def append(self, af_bin: bytes, tla: TaggedLocalArtifact):
        af = tla.artifact

        for scope in tla.tag:
            self.reverse_artifacts[scope].add(af.data_hash)

        self.art_hashes[af.data_hash].append(af)

        self.art_logs[af].append(tla)

        self.blob_storage[af.data_hash] = af_bin


class RemoteChunk:
    """
    Keeps a handle to the Iroh worker/sync task and will fetch on-demand.
    """

    pass


class ChunkQueryMixin:
    """
    The result of a query associates each chunk with a subset of matching artifacts.
    """

    def iter_chunks(self) -> Iterator[LocalChunk | RemoteChunk]:
        raise NotImplementedError()

    def query(
        self,
        scopes: Sequence[RunScope] = (),
        values: Sequence[type[Artifact]] | type[Artifact] | None = None,
    ):
        # TODO: support remote chunks
        return ChunkQuerySet.from_query(self.iter_chunks(), scopes, values)

    def instances(self, af: Artifact) -> Iterator[TaggedLocalArtifact]:
        raise NotImplementedError()


class ChunkCollection(ChunkQueryMixin):
    """
    Queries defined and executed on a set of chunks

    We can "load" a document, converting all remote chunks into local ones
    """

    def __init__(self, chunks: list[LocalChunk]):
        # TODO: common API for remote chunks
        # TODO: this should really be a map chunk_id => chunk
        self._chunks = list(chunks)

    def iter_chunks(self):
        yield from self._chunks

    def fetch_instances_by_hash(self, b3sum: str) -> Iterator[TaggedLocalArtifact]:
        # TODO: handle remote chunks
        for chunk in self.iter_chunks():
            for artifact in chunk.art_hashes[b3sum]:
                yield from self.fetch_instances(artifact)

    def fetch_instances(self, af: Artifact) -> Iterator[TaggedLocalArtifact]:
        # TODO: handle remote chunks
        for chunk in self.iter_chunks():
            yield from chunk.art_logs[af]

    @classmethod
    async def persistent_store(cls):
        # TODO: expose path configuration
        return await Iroh.persistent(".iroh-perm-store")

    @classmethod
    async def document_to_local_chunks(
        cls, scope_namespace: ScopeNamespace, document_id: str
    ):
        node: iroh.Iroh = await cls.persistent_store()
        doc = await node.docs().open(document_id)
        assert doc is not None

        entries = await doc.get_many(iroh.Query.all(None))

        # TODO: Batch API? Parallel async?
        blob_keys = await node.blobs().list()
        blobs = {k.to_hex(): await node.blobs().read_to_bytes(k) for k in blob_keys}

        doc_dict = {}
        for entry in entries:
            key = entry.key().decode()
            doc_dict[key] = await entry.content_bytes(doc)

        found_chunk_ids = set(k.split("/")[0] for k in doc_dict.keys())
        chunks = []
        for chunk_id in found_chunk_ids:
            chunks.append(
                LocalChunk.deserialise(scope_namespace, doc_dict, blobs, chunk_id)
            )
        return ChunkCollection(chunks)

    @staticmethod
    async def from_shared_document(space, node: Iroh, ticket):
        doc = await node.docs().join(ticket)
        raise NotImplementedError()

    async def into_document(self, doc_id: Optional[str] = None) -> str:
        node: iroh.Iroh = await self.persistent_store()
        if doc_id is None:
            doc: iroh.Doc = await node.docs().create()
        else:
            doc = await node.docs().open(doc_id)  # type: ignore
            assert doc is not None, "Document does not exist"

        logger.info(f"Created document {doc.id()}")
        whoami = (
            await node.authors().create()
        )  # perhaps try load from environment variable?

        for chunk in self.iter_chunks():
            if isinstance(chunk, RemoteChunk):
                # Presumably we'd just need to set the *hashes* without having to upload blobs, assuming it's the same node?
                raise NotImplementedError()

            for key, data in chunk.serialise().items():
                await doc.set_bytes(whoami, f"{chunk.chunk_id}/{key}".encode(), data)

            for _blob_hash, blob_bin in chunk.blob_storage.items():
                await node.blobs().add_bytes(blob_bin)

        await asyncio.sleep(1)
        await node.node().shutdown(False)
        await asyncio.sleep(1)  # Cleanup?

        return doc.id()

    def __add__(self, other: ChunkCollection):
        return ChunkCollection([*self.iter_chunks(), *other.iter_chunks()])


class ChunkQuerySet(Chronos):
    # TODO: Implement ChunkQueryMixin for this as well!
    def __init__(self, matches: dict[type[Artifact], list[TaggedLocalArtifact]]):
        self.matches = matches
        super().__init__(self.collect_ordered())

    def collect_ordered(self) -> list[TaggedLocalArtifact]:
        x = []
        for v in self.matches.values():
            x.extend(v)
        x.sort(key=lambda tla: tla.logged_at)
        return x

    def iter_artifacts(self):
        # Note: ordered by time *first* encountered, so won't necessarily give you the thing you just logged
        seen_artifacts = set()
        for tla in self.collect_ordered():
            if tla.artifact not in seen_artifacts:
                seen_artifacts.add(tla.artifact)
                yield tla.artifact

    def artifacts(self):
        return Chronos(self.iter_artifacts())

    def values(self):
        return Chronos(map(lambda tla: tla.artifact_content, self.collect_ordered()))

    @staticmethod
    def from_query(
        iter_chunks: Iterator[LocalChunk],
        scopes: Sequence[RunScope],
        values: Sequence[type[Artifact]] | type[Artifact] | None,
    ):
        """
        Scope queries behave like intersections (ALL scopes must match).
        Value queries are unions (artifact type matching ANY one in the query set).
        """
        # TODO: Support RemoteChunk
        match values:
            case None:
                value_queries = None
            case type():
                value_queries = {values}
            case _:
                value_queries = set(values)

        def require_artifact_of(af: Artifact):
            if value_queries is not None:
                return type(af) in value_queries
            else:
                return True

        by_type = defaultdict(list)
        for ch in iter_chunks:
            for la in ch.match_scope_intersection(scopes):
                if require_artifact_of(la.artifact):
                    by_type[type(la.artifact)].append(la)
        return ChunkQuerySet(by_type)

    def query(
        self,
        *,
        scopes: Sequence[RunScope] = (),
        values: Sequence[type[Artifact]] | type[Artifact] | None = None,
    ):
        raise NotImplementedError()

    def metrics_view(self, expand: Literal["field", "scope", "unit"] = "field"):
        """
        Converts JSON artifacts into a Pandas DataFrame, with scopes set as index columns.

        Expansion argument controls how scopes are turned into columns:
        - ...
        """

        import pandas as pd

        match expand:
            case "field":

                def expand_row(row):
                    res = {}
                    for scope in row["pr.scopes"]:
                        res.update(
                            {
                                f"{scope.scope_name()}.{k}": v
                                for k, v in scope.asdict().items()
                            }
                        )
                    return res
            case "scope":

                def expand_row(row):
                    res = {}
                    for scope in row["pr.scopes"]:
                        res[scope.scope_name()] = scope
                    return res

            case "unit":
                pass

            case _:
                raise ValueError(
                    f'{expand} must be a Literal["field", "scope", "unit"]'
                )

        def expand_df(df):
            if expand == "unit":
                return df.set_index("pr.scopes")
            else:
                non_index_cols = set(df.columns) - {"pr.scopes"}
                result = df.join(
                    df.apply(
                        expand_row,
                        result_type="expand",
                        axis=1,
                    )
                )
                del result["pr.scopes"]
                return result.set_index(
                    [c for c in result.columns if c not in non_index_cols]
                )

        rows_by_type = defaultdict(lambda: [])
        for tla in self:
            tla: TaggedLocalArtifact
            # Should loading happen at a chunk level?
            # TODO: in principle we could concatenate table artifacts as well
            if isinstance(tla.artifact, JSONArtifact):
                rows_by_type[tla.artifact.scope_name()].append(new_row := tla.load())
                new_row["pr.scopes"] = tla.tag
        return {af: expand_df(pd.DataFrame(rows)) for af, rows in rows_by_type.items()}
