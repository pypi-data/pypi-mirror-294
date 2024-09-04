from .namespace import ScopeNamespace
from .scope_type import RunScope
from .tag_type import Tagged
from .artifact import Artifact, Arty
from .chunks import ChunkCollection, MutableLocalChunk, TaggedLocalArtifact

import time
from contextvars import ContextVar
from uuid6 import uuid7
from contextlib import contextmanager, ExitStack
from typing import Iterable, Callable, Any, TypeVar
from typing_extensions import dataclass_transform


class ObjectPermanence:
    """
    Stores objects, defined as one of:
    - Plain JSON object
    - Arrow table
    - Binary data

    You can choose to store pickled objects at your own risk.
    """

    def __init__(self, scope_namespace: ScopeNamespace):
        self.scope_namespace = scope_namespace
        self.namespace = scope_namespace.name

        self.current_tag = ContextVar("permanence_tag", default=Tagged.empty())
        self.current_chunk = MutableLocalChunk.new()
        # TODO: supports overlaying remote chunks
        self.chunks_overlay = ContextVar(
            "permanence_chunks_overlay", default=ChunkCollection([])
        )

    @staticmethod
    def new_namespace(name):
        return ObjectPermanence(ScopeNamespace(name))

    @dataclass_transform(frozen_default=True)
    def new_scope(self, cls):
        assert issubclass(cls, self.Scope)

        # disallow subclassing of other records
        scope_cls = [
            parent_cls for parent_cls in cls.mro() if issubclass(parent_cls, self.Scope)
        ]

        assert (
            len(scope_cls) <= 2
        ), f"{scope_cls}: Subclassing a Record type is disallowed"

        return self.scope_namespace.new_scope(cls)

    @property
    def Scope(self) -> type[RunScope]:
        return self.scope_namespace.Scope

    def active_scopes(self):
        return self.current_tag.get()

    @contextmanager
    def context(self, context: RunScope):
        # TODO: support multiple contexts
        assert isinstance(context, RunScope)

        # TODO: use contextvars reset token?
        entry_id = str(uuid7())
        self.current_tag.set(self.current_tag.get().with_scope(context, entry_id))

        try:
            yield context  # give back scope
        finally:
            self.current_tag.set(
                self.current_tag.get().without_scope(context, entry_id)
            )

    def contexts(self, *contexts: RunScope):
        # Immediately enters contexts, which could be problematic if ExitStack doesn't get entered
        stack = ExitStack()
        for c in contexts:
            stack.enter_context(self.context(c))
        return stack

    @contextmanager
    def using(self, af: Artifact | TaggedLocalArtifact):
        # TODO: support TaggedRemoteArtifact

        match af:
            case Artifact():
                scope = af
                # any instance will have identical content
                content = next(
                    self.chunks().fetch_instances(af)
                ).artifact_content  # Requires fetch
            case TaggedLocalArtifact():  # returned by the chunk
                scope = af.artifact
                content = af.artifact_content

        entry_id = str(uuid7())
        reset = self.current_tag.set(self.current_tag.get().with_scope(scope, entry_id))

        try:
            yield content
        finally:
            self.current_tag.reset(reset)

    @contextmanager
    def overlayed(self, overlay_chunks: ChunkCollection):
        reset_token = self.chunks_overlay.set(
            self.chunks_overlay.get() + overlay_chunks
        )
        try:
            yield
        finally:
            self.chunks_overlay.reset(reset_token)

    def chunks(self) -> ChunkCollection:
        # Shallow copy because we don't want interior mutability in ChunkCollection
        return self.chunks_overlay.get() + ChunkCollection([self.current_chunk.copy()])

    def query(self, *, scopes=(), values=None):
        return self.chunks().query([*self.active_scopes(), *scopes], values)

    def _log(self, artifact_type: type[Artifact], value_of) -> TaggedLocalArtifact:
        content_bin, value_scope = artifact_type.new(value_of)
        # TODO: write log time
        tla = TaggedLocalArtifact(
            value_of, value_scope, self.current_tag.get(), time.time()
        )
        self.current_chunk.append(content_bin, tla)
        return tla

    def log(self, value):
        """
        Untyped interface for logging arbitrary objects as artifacts.
        """
        artifact_type = Arty.any(value)
        return self.logged(artifact_type, value)

    def logged(self, artifact_type: type[Artifact], value_of):
        """
        Structured interface for logging typed and named artifacts.
        """
        tla = self._log(artifact_type, value_of)
        return tla.artifact

    def checkout(self, b3sum: str) -> Artifact:
        """
        To access `TaggedArtifact`s, use the query interface instead.
        """
        return next(self.chunks().fetch_instances_by_hash(b3sum)).artifact

    def try_checkout(self, b3sum: str):
        # TODO: -> Result[Artifact, None]
        raise NotImplementedError()

    T = TypeVar("T", bound=RunScope)

    def __getitem__(self, scope_or_artifact: type[T]) -> T:
        """
        Convenience interface to access the "current" scope

        where:
            S: RunScope excluding Artifact
        returns, given that:
        - type[S]: looks up and returns unique instance of that type from current scope (error if not found or non-unique)
        """
        if issubclass(scope_or_artifact, self.Scope):
            scopes = [
                s for s in self.active_scopes() if isinstance(s, scope_or_artifact)
            ]
            if len(scopes) != 1:
                raise RuntimeError(f"{scope_or_artifact} in {scopes}: Scope not active")
            return scopes[0]
        else:
            # Artifact or artifact type?
            raise NotImplementedError(scope_or_artifact)
