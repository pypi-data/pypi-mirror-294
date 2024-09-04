from permanence import (
    ObjectPermanence,
    Scope,
    Arty,
)
import pytest


def test_init_and_log():
    pr = ObjectPermanence.new_namespace("just-for-testing_basic")

    @pr.new_scope
    class Basically(pr.Scope):
        name: str

    @pr.new_scope
    class Totally(pr.Scope):
        n: int

    with pr.context(Basically("bob")):
        pr.logged(Arty.JSON.XYZ, {"xyz": 256})

    with pr.context(Basically("eve")):
        pr.log({"abc": 1024})

    all_values = pr.query()
    assert len(all_values) == 2

    with pr.context(Basically("alice")):
        assert pr.query().empty

    with pr.context(Basically("bob")):
        assert pr.query().only().load() == {"xyz": 256}

    with pr.context(Totally(0)):
        pr.log({"id": 0})

    with pr.context(Basically("bob")):
        with pr.context(Totally(0)):
            assert pr.query().empty

    with pr.context(Totally(37)):
        assert pr[Totally].n == 37

    with pytest.raises(RuntimeError):
        # Not in context
        print(pr[Totally].n)


def test_scope_usage():
    # Uses default "global" script scope
    from permanence import pr

    @pr.new_scope
    class Ope(Scope):
        x: int

    with pr.context(Ope(22)):
        pr.log({"result": 1})
