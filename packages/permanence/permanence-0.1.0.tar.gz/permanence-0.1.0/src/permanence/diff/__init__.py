from .bounds import btest_rel

from permanence import RunScope
from permanence.chunks import ChunkQuerySet

import pandas as pd
import numpy as np

from dataclasses import dataclass
from typing import Any, Literal

from loguru import logger


@dataclass
class PairedSignificance:
    n: int
    "Number of paired samples"

    p_b_gt_t: float
    "Is target < baseline?"

    p_t_gt_b: float
    "Is target > baseline?"

    mu_B: float

    mu_T: float

    std: float

    @staticmethod
    def perform(baseline_values, target_values):
        B = np.array(baseline_values).flatten()
        T = np.array(target_values).flatten()
        assert (n := len(B)) == len(T)
        b_gt_t, t_gt_b = btest_rel(B, T)
        return PairedSignificance(
            n, b_gt_t, t_gt_b, B.mean(), T.mean(), (T - B).std(ddof=1)
        )

    def ratio(self):
        return max(self.p_b_gt_t / self.p_t_gt_b, self.p_t_gt_b / self.p_b_gt_t)


@dataclass
class GroupSignificance:
    n1: int
    n2: int
    # TODO: support


@dataclass
class Comparison:
    feature: Any
    baseline: RunScope
    target: RunScope
    sig: PairedSignificance


class ComparisonSet:
    def __init__(self, direction: Literal["min", "max"] = "min"):
        self.comparisons: list[Comparison] = []
        self.direction = direction

    def add(self, cmps: list[Comparison]):
        self.comparisons.extend(cmps)

    def table(self):
        from rich.table import Table
        from rich.text import Text
        from rich.pretty import Pretty

        table = Table(show_lines=True)
        table.add_column("Feature")
        table.add_column("Better")
        table.add_column(f"Comparison ({self.direction})")
        table.add_column("Worse")
        table.add_column("Significance", justify="right")
        table.add_column("n", justify="right")
        table.add_column("Δ", justify="right")
        table.add_column("μ", justify="right")
        table.add_column("σ", justify="right")

        self.comparisons.sort(key=lambda s: s.sig.ratio())
        for cmp in self.comparisons:
            sgn = 0  # index of "better" in [baseline, target]
            if cmp.sig.p_b_gt_t < cmp.sig.p_t_gt_b:  # assume min
                sgn = sgn ^ 1
            if self.direction == "max":
                sgn = sgn ^ 1

            scopes = [cmp.baseline, cmp.target]
            means = [cmp.sig.mu_B, cmp.sig.mu_T]
            better = sgn
            worse = sgn ^ 1

            table.add_row(
                cmp.feature,
                Pretty(scopes[better]),
                self.ratio_significance_description(cmp.sig.ratio()),
                Pretty(scopes[worse]),
                f"{cmp.sig.ratio():.03g}x",
                f"{cmp.sig.n}",
                f"{means[better] - means[worse]:.3g}",
                f"{means[better]:.3g}",
                f"{cmp.sig.std:.3g}",
            )

        return table

    def show_table(self):
        import rich

        rich.print(self.table())

    @staticmethod
    def ratio_significance_description(ratio: float):
        if ratio < 1:
            logger.error(f"Expected comparison ratio to be >= 1 (got {ratio})")

        if ratio < 2:
            return "[grey37]is similar to"
        elif ratio < 10:
            return "is better than"
        elif ratio < 100:
            return "[yellow]is much better than"
        else:
            return "[green]is overwhelmingly better than"


def grid_compare_frame(df: pd.DataFrame, baseline_sorter=lambda s: repr(s)):
    """
    Index set as scope columns.

    Count # samples in each grid.

    Row type design?
    """
    # baseline_sorter hack: repr => lexicographic order!

    metric_cols = [c for c in df.columns if c.startswith("metric:")]

    comparisons = []

    for metric in metric_cols:
        metric_df = df[[metric]].reset_index()
        scope_cols = list(metric_df.columns)
        scope_cols.remove(metric)

        def Not(*cols):
            return [c for c in metric_df.columns if c not in cols]

        for scope in scope_cols:
            scope_values = sorted(
                metric_df[scope].dropna().unique(), key=baseline_sorter
            )
            if len(scope_values) < 2:
                continue

            baseline_scope = scope_values[0]

            set_baseline = metric_df[metric_df[scope] == baseline_scope]

            for target_scope in scope_values[1:]:
                set_target = metric_df[metric_df[scope] == target_scope]

                set_combined = set_baseline.set_index(Not(metric, scope)).join(
                    set_target.set_index(Not(metric, scope)),
                    lsuffix="_baseline",
                    rsuffix="_target",
                    how="inner",
                )

                if (nsamples := len(set_combined)) < 3:
                    logger.warning(
                        f"Not enough samples ({nsamples}) to perform comparison of {baseline_scope} <-> {target_scope} for {metric}"
                    )
                    continue

                comparisons.append(
                    Comparison(
                        metric,
                        baseline_scope,
                        target_scope,
                        PairedSignificance.perform(
                            set_combined[f"{metric}_baseline"],
                            set_combined[f"{metric}_target"],
                        ),
                    )
                )
    return comparisons


def grid_compare(cqs: ChunkQuerySet, direction="min"):
    comparisons = []
    for af_type, df in cqs.metrics_view("scope").items():
        logger.info(f"Comparing {af_type}")
        comparisons.extend(grid_compare_frame(df))

    cset = ComparisonSet(direction=direction)
    cset.add(comparisons)
    return cset
