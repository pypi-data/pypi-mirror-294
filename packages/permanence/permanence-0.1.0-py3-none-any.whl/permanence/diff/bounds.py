import numpy as np
from scipy.stats import beta, gmean


def score_ranks(bounds):
    bounds = np.array(bounds)
    n = len(bounds)
    K = 1 + np.arange(n)
    X = np.sort(bounds)

    distribution = beta(K, n + 1 - K)
    cutoff = distribution.median()

    L = np.where(X > cutoff, 1, distribution.cdf(X) / distribution.cdf(cutoff))
    return gmean(L)


def bound_right(mean, median, stdev, x):
    a = x - mean
    k = a / stdev
    with np.errstate(divide="ignore"):
        # TODO: adjust stdev fudge using sample size
        return np.clip(
            np.minimum(
                np.where(x > median + stdev / 10, 0.5, 1.0),
                np.where(
                    a <= 0,
                    1.0,
                    np.where(
                        k >= np.sqrt(8 / 3), 4 / (9 * k**2), 4 / (3 * k**2) - 1 / 3
                    ),
                ),
                np.where(a <= 0, 1.0, stdev**2 / (stdev**2 + a**2)),
            ),
            0,
            1,
        )


def bound_left(mean, median, stdev, x):
    return bound_right(2 * x - mean, 2 * x - median, stdev, x)


def btest_rel(A, B):
    A = np.array(A)
    B = np.array(B)
    assert A.shape == B.shape and len(A.shape) == 1

    stdev = max(1e-8, np.std(A - B, ddof=1))

    p_a_gt_b = score_ranks(bound_right(0.0, 0.0, stdev, A - B))
    p_b_gt_a = score_ranks(bound_left(0.0, 0.0, stdev, A - B))
    return p_a_gt_b, p_b_gt_a
