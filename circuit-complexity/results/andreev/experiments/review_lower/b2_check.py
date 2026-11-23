"""Referee check of Lemma B2 (block-symmetric gates; Ball + Brunn slab bound), exact integer counting.
Gate [beta.s >= th] (table part only shifts th).  Cube c split iff th-pos <= beta.c < th-neg.
max_th #split = max over windows of (pos-neg)=||beta||_1 consecutive values of beta.c  (beta integer).
Claimed: #split <= min(m^k-(m-1)^k, 2 sqrt2 (||beta||_1/||beta||_2) m^(k-1)).
We report the worst ratio actual/bound per (k,m) for many directions incl. extremal ones."""
import itertools, math, sys
import numpy as np

def value_counts(beta, m):
    cur = {0: 1}
    for b in beta:
        nxt = {}
        for v, c in cur.items():
            for t in range(m):
                nxt[v + b * t] = nxt.get(v + b * t, 0) + c
        cur = nxt
    return cur

def max_split(beta, m):
    cnt = value_counts(beta, m); L = sum(abs(b) for b in beta)
    if L == 0: return 0
    vals = sorted(cnt)
    lo, hi = vals[0], vals[-1]
    arr = np.zeros(hi - lo + 1, dtype=np.int64)
    for v, c in cnt.items(): arr[v - lo] = c
    cs = np.concatenate([[0], np.cumsum(arr)])
    # window of L consecutive integer values [v, v+L-1]
    best = 0
    for v in range(lo - L, hi + 1):
        a = max(v - lo, 0); b = min(v + L - lo, len(arr))
        if b > a: best = max(best, int(cs[b] - cs[a]))
    return best

rng = np.random.default_rng(3)
worst_overall = 0
for k, m in [(2, 6), (2, 9), (3, 4), (3, 7), (4, 4), (4, 6), (5, 3), (5, 5), (6, 3), (6, 4), (7, 3), (8, 2), (8, 3)]:
    dirs = [tuple([1] * k), tuple([1, 1] + [0] * (k - 2)), tuple([1, -1] + [0] * (k - 2)), tuple([1] * (k // 2) + [0] * (k - k // 2))]
    dirs += [tuple(rng.integers(-3, 4, k)) for _ in range(150)] + [tuple(rng.integers(-50, 51, k)) for _ in range(60)]
    dirs += [tuple(int(v) for v in (rng.random(k) < 0.5) * rng.integers(1, 4, k)) for _ in range(60)]
    worst = 0; wd = None; worst_coh = 0
    for d in dirs:
        if not any(d): continue
        c = max_split(list(d), m)
        l1 = sum(abs(x) for x in d); l2 = math.sqrt(sum(x * x for x in d))
        bound = min(m ** k - (m - 1) ** k, 2 * math.sqrt(2) * l1 / l2 * m ** (k - 1))
        r = c / bound
        if r > worst: worst, wd = r, (d, c, bound)
        worst_coh = max(worst_coh, c / (m ** k - (m - 1) ** k))
        if c > bound + 1e-9: print('VIOLATION', k, m, d, c, bound)
    worst_overall = max(worst_overall, worst)
    print(f'k={k} m={m}: worst actual/bound = {worst:.3f} (dir {wd[0]}: {wd[1]} vs {wd[2]:.1f});  worst actual/(m^k-(m-1)^k) = {worst_coh:.3f}', flush=True)
print('max ratio over all cases:', round(worst_overall, 4))
# asymptotic comparison for the all-ones direction: exact max fraction vs Ball bound 2 sqrt(2k)/m and CLT sqrt(6k/pi)/m
for k, m in [(8, 20), (12, 12), (16, 8)]:
    c = max_split([1] * k, m)
    print(f'all-ones k={k} m={m}: max split fraction = {c/m**k:.4f};  Ball 2sqrt(2k)/m = {2*math.sqrt(2*k)/m:.4f};  CLT sqrt(6k/pi)/m = {math.sqrt(6*k/math.pi)/m:.4f};  coherent 1-(1-1/m)^k = {1-(1-1/m)**k:.4f}')
