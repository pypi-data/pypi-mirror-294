from __future__ import annotations
from .scope_type import RunScope

import pyarrow as pa
import pyarrow.feather as ft
import pandas as pd
from blake3 import blake3
import attrs
import json
from io import BytesIO

from typing import Any, Self


class _CreateArtifact:
    def __init__(self, artifact_type):
        self.artifact_type = artifact_type
        self.registered = {}

    def __call__(self, *args, **kwargs):
        # To allow passing config for validation...
        return self

    def __getattr__(self, name):
        if name in self.registered:
            return self.registered[name]

        # TODO: support defining validators?
        new_artifact = attrs.frozen(
            type(
                name,
                (self.artifact_type,),
                {"__annotations__": {"data_hash": str}},
            )
        )
        self.registered[name] = new_artifact

        return new_artifact


class Artifact(RunScope):
    data_hash: str

    @classmethod
    def new(cls, obj) -> tuple[bytes, Self]:
        raise NotImplementedError()

    @staticmethod
    def type_string():
        raise NotImplementedError()


class JSONArtifact(Artifact):
    @classmethod
    def new(cls, obj) -> tuple[bytes, Self]:
        obj_bin = json.dumps(obj).encode()
        obj_hash = blake3().update(obj_bin).hexdigest()
        return obj_bin, cls(obj_hash)

    @classmethod
    def reconstruct(cls, data: bytes):
        return json.loads(data)

    def namespace(self):
        # special dot-prefixed namespace
        return ".Artifact.JSON"

    @staticmethod
    def type_string():
        return "JSON"


class TableArtifact(Artifact):
    @classmethod
    def new(cls, table) -> tuple[bytes, Self]:
        write_to = BytesIO()
        match table:
            case pd.DataFrame():
                table = pa.Table.from_pandas(table)
            case pa.Table():
                table = table
            case _:
                raise TypeError(f"{table}")

        with pa.ipc.new_file(write_to, table.schema) as writer:
            writer.write_table(table)

        obj_bin = write_to.getvalue()
        obj_hash = blake3().update(obj_bin).hexdigest()
        return obj_bin, cls(obj_hash)

    @classmethod
    def reconstruct(cls, data: bytes):
        return ft.read_table(BytesIO(data))

    def namespace(self):
        # special dot-prefixed namespace
        return ".Artifact.Table"

    @staticmethod
    def type_string():
        return "Table"


class Arty:
    JSON = _CreateArtifact(JSONArtifact)
    Table = _CreateArtifact(TableArtifact)

    @classmethod
    def any(cls, obj):
        """
        Unnamed default artifact scope.
        """
        match obj:
            case pd.DataFrame() | pa.Table():
                return cls.Table.AnyTable
            case dict():
                return cls.JSON.AnyJSON
            case _:
                raise TypeError(f"{type(obj)}")


"""
per[SavedMeasurements].load
for m in per[SavedMeasurements].query_all():
    with per.using(m) as df:
        computed_stuff = {"x": 100, "y": df["y"].sum()}
        # relax
        per.log(per.Arty.JSON.Computed, computed_stuff)

        # will autmatically log and upload?
        with per.context(Arty.JSON.Computed({"x": 1})):  # returns context
            Arty.JSON.Computed.load()  # will error if multiple found
            Arty.JSON.Computed.get()  # will

    # How does this handle using multiple of a type?
per.fetch_logs(SavedMeasurements)
"""
