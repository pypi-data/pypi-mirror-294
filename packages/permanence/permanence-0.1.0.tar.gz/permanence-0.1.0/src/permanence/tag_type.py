from __future__ import annotations

from .scope_type import RunScope

from blake3 import blake3
import numpy as np

from typing import Optional


class Tagged:
    """
    A tag is an immutable set of scopes.
    At time of entry, a scope gets associated with an ID.
    IDs don't matter for equality and hash comparisons - they're mostly just for serialisation.
    Every logged object is associated with the current tag.
    """

    def __init__(self, scopes_in_context: dict[RunScope, str]):
        self.scope_state = {
            scope: context_id for scope, context_id in scopes_in_context.items()
        }  # copy

        # Validate: all records should belong to same namespace
        namespaces = set(
            scope.namespace()
            for scope in self.scope_state
            if not scope.namespace().startswith(".")
        )
        assert len(namespaces) <= 1, f"{namespaces}: Inconsistent namespaces"

        self.types = set(type(s) for s in self.scope_state.keys())

        if len(self.types) != len(self.scope_state):
            raise RuntimeError(
                f"Each scope time can only be entered once ({self.scope_state})"
            )

    def __repr__(self):
        scope_reprs = "\n".join("\t" + repr(s) for s in self)
        return f"Tagged {{\n{scope_reprs}\n}}"

    def __getitem__(self, scope_type: type[RunScope]):
        # TODO: validation
        for sc in self:
            if isinstance(sc, scope_type):
                return sc

    @staticmethod
    def empty():
        return Tagged({})

    def with_scope(self, scope, context_id: str) -> Tagged:
        assert scope not in self.scope_state
        return Tagged({**self.scope_state, scope: context_id})

    def without_scope(self, scope, context_id: Optional[str] = None) -> Tagged:
        # Can pass context_id for consistency check (enter/exit properly paired)
        if context_id is not None:
            assert self.scope_state[scope] == context_id

        sans = {**self.scope_state}
        del sans[scope]
        return Tagged(sans)

    def with_scopes(self, *more_scopes) -> Tagged:
        tag = self
        for s in more_scopes:
            tag = tag.with_scope(s)

    def without_scopes(self, *more_scopes) -> Tagged:
        raise RuntimeError("Deprecated!")
        assert set(more_scopes).issubset(self.scopes)
        return Tagged(self.scopes.difference(more_scopes))

    def matches_query(self, q: Tagged | list[RunScope] | set[RunScope]) -> bool:
        match q:
            case Tagged(scope_state=scope_state):
                return set(self.scope_state.keys()).issuperset(scope_state.keys())
            case (list() | set()) as scopes:
                return set(self.scope_state.keys()).issuperset(scopes)
            case _:
                raise TypeError(f"{q}")

    def hashed(self):
        sup_hash = np.frombuffer(
            b"0000000000000000000000000000000000000000000000000000000000000000",
            dtype=np.uint8,
        )
        for scope in self.scope_state.keys():
            # TODO: not proper hex
            hasher = blake3()
            hasher.update(scope.namespace().encode())
            hasher.update(type(scope).__name__.encode())
            hasher.update(scope.as_canonical_json().encode())
            sup_hash = np.maximum(
                sup_hash,
                np.frombuffer(hasher.hexdigest().encode(), dtype=np.uint8),
            )

        return sup_hash.tobytes().decode("utf-8")

    def __iter__(self):
        # Copy for safety to handle mutation during iteration
        yield from list(self.scope_state.keys())
