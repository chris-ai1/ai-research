#!/usr/bin/env python3
"""Random-feature experiment: how many RANDOM bottom gates of a given class are needed before an LP
top gate represents A_{k,m} exactly (margin 1 after scaling)?  Classes:
  mixed    : address weights iid N(0,1) per bit
  blocksym : one N(0,1) weight per block (all bits of the block equal)
  coherent : |N(0,1)| per bit, one random sign per (gate, block)
  pm1      : address weights iid uniform {-1,+1}
Table weights are N(0,1) in all classes; the threshold is the gate's value at a random input point
(so every hyperplane passes through the data).  For each S we draw `reps` circuits and record the
fraction for which the top-gate LP is feasible.  This is a heuristic comparison of the classes as
feature families, not a bound.
Usage: python3 -I random_features.py K M [reps]
"""
import sys, os
sys.path.insert(0, '/tmp/pydeps'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import linprog
from mscore import andreev_points, andreev_blocks


def feasible(G, X, y):
    # find v,u,tau: s_p*(G v + X u - tau) >= 1
    n = len(y); sgn = 2 * y - 1
    A = np.hstack([G, X, -np.ones((n, 1))]) * sgn[:, None]
    nv = A.shape[1]
    res = linprog(np.zeros(nv), A_ub=-A, b_ub=-np.ones(n), bounds=[(None, None)] * nv, method='highs')
    return res.status == 0


def draw(cls, S, X, N, blocks, rng):
    n, D = X.shape
    W = np.zeros((S, D))
    W[:, :N] = rng.normal(0, 1, (S, N))
    for B in blocks:
        if cls == 'mixed':
            W[:, B] = rng.normal(0, 1, (S, len(B)))
        elif cls == 'blocksym':
            W[:, B] = rng.normal(0, 1, (S, 1))
        elif cls == 'coherent':
            W[:, B] = np.abs(rng.normal(0, 1, (S, len(B)))) * rng.choice([-1, 1], (S, 1))
        elif cls == 'pm1':
            W[:, B] = rng.choice([-1.0, 1.0], (S, len(B)))
    piv = X[rng.integers(0, n, S)]
    th = (piv * W).sum(1) - 1e-9
    return (X @ W.T >= th).astype(float)


def main():
    k, m = int(sys.argv[1]), int(sys.argv[2])
    reps = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    pts = andreev_points(k, m); N = 1 << k
    X = np.array([p for p, _ in pts], float); y = np.array([t for _, t in pts])
    blocks = andreev_blocks(k, m)
    rng = np.random.default_rng(0)
    for cls in ['blocksym', 'coherent', 'mixed', 'pm1']:
        lo, hi = 1, 8
        # find an S with success, doubling
        def rate(S):
            return np.mean([feasible(draw(cls, S, X, N, blocks, rng), X, y) for _ in range(reps)])
        while rate(hi) < 0.5 and hi < 4096:
            lo, hi = hi, hi * 2
        while hi - lo > max(1, lo // 16):
            mid = (lo + hi) // 2
            if rate(mid) >= 0.5: hi = mid
            else: lo = mid
        print(f'k={k} m={m} points={len(y)} class={cls:9s}: ~{hi} random gates give exact representation '
              f'(>=50% of {reps} draws)', flush=True)


if __name__ == '__main__':
    main()
