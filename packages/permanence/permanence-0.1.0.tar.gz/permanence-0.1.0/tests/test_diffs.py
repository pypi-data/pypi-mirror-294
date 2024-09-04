from permanence import ObjectPermanence, Arty
from permanence.diff import grid_compare

import pandas as pd
from random import random
import itertools


def test_grid_diff():
    pr = ObjectPermanence.new_namespace("test-diffs")

    @pr.new_scope
    class A(pr.Scope):
        shift: float

    @pr.new_scope
    class B(pr.Scope):
        dummy: str

    @pr.new_scope
    class C(pr.Scope):
        shift: float

    @pr.new_scope
    class X(pr.Scope):
        seed: int
        sigma: float

    def additive_model():
        point_sample = (random() - 1 / 2) * pr[X].sigma + pr[A].shift - pr[C].shift
        pr.logged(
            Arty.JSON.Additive,
            {"metric:score": point_sample, "metric:potato": random()},
        )  # Basic additive model

    # (A): +2.0
    # (B): +0.0 (no effect)
    # (C): -1.0
    # (X): random epsilon noise sampled some number of times
    param_space = (
        [A(0.0), A(2.0)],
        [B("placebo"), B("nocebo")],
        [C(0.0), C(1.0)],
        [X(s, 0.5) for s in range(5)],
    )
    # may want a Tag Exclusion filter (e.g. unwanted body parts)
    for ctx in itertools.product(*param_space):
        with pr.contexts(*ctx):
            additive_model()

    cmps = grid_compare(pr.query(), "max")
    cmps.show_table()

    # TODO: test sigs


if __name__ == "__main__":
    test_grid_diff()
