from typing_extensions import dataclass_transform
import attrs
import frozendict
from uuid import uuid4
import json

from typing import Self, TypeVar


def convert_metric_field(value):
    match value:
        case dict():
            return frozendict.deepfreeze(value)
        case list():
            return tuple(value)
        case _:
            return value


def freeze_metric_fields(cls, fields):
    """
    Instances of Metric are intended to be serialised to JSON, and must be immutable.
    We'd like to have a __hash__ implementation, but dicts and lists are both mutable and unhashable.
    This recursively converts values to frozendicts (https://github.com/Marco-Sulla/python-frozendict) and tuples, respectively.
    """
    return [f.evolve(converter=convert_metric_field) for f in fields]


class RunScope:
    """
    Base marker type for dataclass-like structs containing JSON-isomorphic parameter data for a context level.

    This is an attrs frozen class, so subclasses should not rely on an __init__ method to be called.

    Defining __attrs_post_init__ should work though.
    """

    def asdict(self):
        return attrs.asdict(self)

    @classmethod
    def from_canonical_json(cls, json_str: str) -> Self:
        return cls(**json.loads(json_str))

    def as_canonical_json(self):
        # TODO: actually implement the "canonical" part
        return json.dumps(self.asdict())

    def namespace(self) -> str:
        raise NotImplementedError()

    def scope_name(self) -> str:
        return type(self).__name__


T = TypeVar("T", bound=type[RunScope])


def make_scope(cls: T) -> T:
    """Class decorator for registering class names and ensuring inheritance from Metric."""
    assert issubclass(cls, RunScope)

    cls = attrs.frozen(field_transformer=freeze_metric_fields)(cls)
    return cls
