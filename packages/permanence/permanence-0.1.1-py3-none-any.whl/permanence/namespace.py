from .scope_type import RunScope, make_scope

from typing_extensions import dataclass_transform


class ScopeNamespace:
    def __init__(self, named_identifier: str):
        self.name = named_identifier

        self.registered_artifacts = {}
        self.registered_scopes: dict[str, type[RunScope]] = {}

        # TODO: Sanitise scope name?
        self.scope_cls = type(
            self.name, (RunScope,), {"namespace": lambda _: self.name}
        )

    @property
    def Scope(self) -> type[RunScope]:
        return self.scope_cls

    @dataclass_transform()
    def new_scope(self, cls) -> type[RunScope]:
        new_cls = type(cls.__name__, (self.scope_cls,), {**cls.__dict__})
        new_cls = make_scope(new_cls)

        # TODO: do some sort of "class equality" check
        # assert new_cls.__name__ not in self.registered_scopes
        if new_cls.__name__ in self.registered_scopes:
            return self.registered_scopes[new_cls.__name__]
            # Error: only supported for mutable types or...
            # self.registered_scopes[new_cls.__name__].__class__ = new_cls

        self.registered_scopes[new_cls.__name__] = new_cls
        return new_cls

    def new_artifact(self, cls):
        return cls
