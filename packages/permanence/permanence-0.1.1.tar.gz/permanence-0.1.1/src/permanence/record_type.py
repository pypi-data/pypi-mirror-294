import attrs
import frozendict

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
    """

    @classmethod
    def get(cls) -> Self:
        # This method gets patched in later
        raise NotImplementedError()

    def asdict(self):
        return attrs.asdict(self)


T = TypeVar("T", bound=type[RunScope])


def make_scope(cls: T) -> T:
    """Class decorator for registering class names and ensuring inheritance from Metric."""
    assert issubclass(cls, RunScope)

    # disallow subclassing of other records
    scope_cls = [
        parent_cls
        for parent_cls in cls.mro()
        if issubclass(parent_cls, RunScope)
        and parent_cls.__module__.split(".")[0] != "permanence"
    ]
    assert len(scope_cls) == 1, "Subclassing a Record type is disallowed"

    cls = attrs.frozen(field_transformer=freeze_metric_fields)(cls)
    return cls


def new_scope_namespace(name: str):
    """
    Defines a unique namespace that will be considered completely independent of other namespaces (w.r.t scopes, objects and all other functions).

    Also helps with type-safety.
    """

    class NamedScope(RunScope):
        _scope_namespace = name

    return NamedScope
