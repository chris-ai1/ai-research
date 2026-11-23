# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Can a circuit-adapted arrangement defeat random +-1 gate sets?

For S random gates with +-1 address weights (threshold 1/2, one table bit), we measure
   T(sigma) = sum_j sum_c 1[ gate j is informative on cube c under sigma ]
             = sum_j #{c : F_j(c) in [-P_j(c), Q_j(c)]},
where F_j(c) = sum_i P_{j,i}(c_i) is the walk and (P,Q) are the numbers of +1 / -1 live weights.
We compare: identity arrangement, random arrangements (mean, min of R draws), and a local-search
minimiser over arrangements (swap two positions inside a block; accept if T decreases; also a
'sort by gate-1 signs' start).  The ratio  min_found / mean_random  shows how much an adversarial
arrangement can lower the total demand met.  Theorem 3.1 predicts ratio -> 1 once S >> km log m.
Also reported: the per-cube minimum  min_c sum_j 1[j informative on c]  under the found arrangement,
against the Theorem A demand D0 = (2^k - k - 1 - log2(S+1)) / (k + log2(S+1)).
"""
import sys, time
sys.path.insert(0, '/tmp/andreev_gap/coherence_fable/pydeps_local'); sys.path.insert(1, '/tmp/pydeps')
import numpy as np
from math import log2

def walks(W, perms):
    # W: (S,k,m) weights; perms: list of k permutations (arrays of length m); returns P: (S,k,m+1)
    S, k, m = W.shape
    P = np.zeros((S, k, m + 1), dtype=np.int32)
    for i in range(k):
        P[:, i, 1:] = np.cumsum(W[:, i, perms[i]], axis=1)
    return P

def demand_matrix(W, perms):
    """returns I: (S, m, ..., m) boolean: gate j informative on cube c"""
    S, k, m = W.shape
    P = walks(W, perms)
    # F(c) = sum_i P[:, i, c_i]; live weight lam_i = W[:, i, perms[i][c_i]]
    shape = (S,) + (m,) * k
    F = np.zeros(shape, dtype=np.int32)
    Pos = np.zeros(shape, dtype=np.int32)   # number of +1 live weights
    for i in range(k):
        idx = [None] * (k + 1); idx[0] = slice(None); idx[i + 1] = slice(None)
        bshape = [1] * (k + 1); bshape[0] = S; bshape[i + 1] = m
        F = F + P[:, i, :m].reshape(bshape)
        live = W[:, i, perms[i][:m]]          # (S, m) live weight for c_i = 0..m-1
        Pos = Pos + (live > 0).astype(np.int32).reshape(bshape)
    Q = k - Pos
    return (F >= -Pos) & (F <= Q)

def total(W, perms):
    return int(demand_matrix(W, perms).sum())

def local_search(W, perms, iters, rng, log=None):
    S, k, m = W.shape
    cur = total(W, perms); best = cur
    perms = [p.copy() for p in perms]
    for it in range(iters):
        i = rng.integers(k)
        a, b = rng.choice(m, 2, replace=False)
        perms[i][a], perms[i][b] = perms[i][b], perms[i][a]
        t = total(W, perms)
        if t <= cur:
            cur = t
        else:
            perms[i][a], perms[i][b] = perms[i][b], perms[i][a]
        if log and it % max(1, iters // 5) == 0:
            print(f"      iter {it}: T={cur}", file=log, flush=True)
    return cur, perms

def run(k, m, S, R=20, iters=600, seed=0):
    rng = np.random.default_rng(seed)
    W = rng.choice([-1, 1], size=(S, k, m)).astype(np.int32)
    ident = [np.arange(m) for _ in range(k)]
    T_id = total(W, ident)
    Ts = [total(W, [rng.permutation(m) for _ in range(k)]) for _ in range(R)]
    mean_r, min_r = np.mean(Ts), min(Ts)
    # start local search from the arrangement that sorts gate 0's signs (+ first) in every block
    start = [np.argsort(-W[0, i, :], kind='stable') for i in range(k)]
    T_sorted0 = total(W, start)
    t0 = time.time()
    T_ls, perms_ls = local_search(W, start, iters, rng)
    # local search from a random start too
    T_ls2, perms_ls2 = local_search(W, [rng.permutation(m) for _ in range(k)], iters, rng)
    if T_ls2 < T_ls: T_ls, perms_ls = T_ls2, perms_ls2
    I = demand_matrix(W, perms_ls)
    percube = I.sum(axis=0)
    D0 = (2**k - k - 1 - log2(S + 1)) / (k + log2(S + 1))
    mk = m**k
    print(f"k={k} m={m} S={S:5d} | per-gate frac: mean_rand={mean_r/(S*mk):.4f} "
          f"sqrt(k/m)={np.sqrt(k/m):.4f} | T_id/mean={T_id/mean_r:.3f} T_min_rand/mean={min_r/mean_r:.3f} "
          f"T_sorted0/mean={T_sorted0/mean_r:.3f} T_localsearch/mean={T_ls/mean_r:.3f} | "
          f"min_c demand met={percube.min()} (mean {percube.mean():.1f}) vs D0={D0:.2f} | {time.time()-t0:.0f}s",
          flush=True)

if __name__ == '__main__':
    k = int(sys.argv[1]); ms = [int(v) for v in sys.argv[2].split(',')]
    mode = sys.argv[3] if len(sys.argv) > 3 else 'all'
    for m in ms:
        km = k * m
        Ss = {'small': [max(2, km // 4)], 'lin': [km], 'pow': [int(km ** 1.5)], 'all': [max(2, km // 4), km, int(km ** 1.5)]}[mode]
        for S in Ss:
            iters = 600 if m <= 32 else 300
            run(k, m, S, iters=iters)
