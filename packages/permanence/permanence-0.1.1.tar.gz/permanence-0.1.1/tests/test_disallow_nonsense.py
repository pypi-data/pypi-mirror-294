from permanence import ObjectPermanence
from attrs import asdict

import pytest


def test_disallow_record_subclassing():
    pr = ObjectPermanence.new_namespace("just-for-testing_nonsense")

    @pr.new_scope
    class Level(pr.Scope):
        name: str

    # subclassing is not allowed
    with pytest.raises(Exception):

        @pr.new_scope
        class LevelTwo(Level):
            name: str

    # forbid inconsistent scopes
    with pytest.raises(RuntimeError):
        with pr.context(Level("one")):
            with pr.context(Level("two")):
                pass


def test_different_namespaces():
    pr_A = ObjectPermanence.new_namespace("just-for-testing_nonsense_A")
    pr_b = ObjectPermanence.new_namespace("just-for-testing_nonsense_B")

    # At the module level you'd just define `Scope = A` and `new_scope = per_a.new_scope` and import those

    @pr_A.new_scope
    class Ope(pr_A.Scope):
        x: int

    ope_a = Ope

    @pr_b.new_scope
    class Ope(pr_b.Scope):
        x: int

    ope_b = Ope

    # equality checks must take namespace into account
    assert asdict(ope_a(1)) == asdict(ope_b(1))
    assert ope_a(1) != ope_b(1)
    assert ope_a(1).namespace() != ope_b(1).namespace()
