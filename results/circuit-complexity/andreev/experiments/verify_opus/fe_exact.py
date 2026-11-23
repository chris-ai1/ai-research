"""Exact, exhaustive re-check of five_eighths.py circuits (integer arithmetic, all 2^n inputs).
Also reports the top-gate margin and checks gate count vs formula."""
import sys, itertools
sys.path.insert(0, '/tmp/pydeps')
import numpy as np
src = open('/tmp/andreev_gap/five_eighths.py').read().split('for k,m in')[0]
ns = {}; exec(src, ns)
build = ns['build']

def exact(k, m, chunk=1 << 16):
    gates, K, N, n = build(k, m)
    W = np.array([g[0] for g in gates]); T = np.array([g[1] for g in gates]); V = np.array([g[2] for g in gates])
    for arr in (W, T, V, np.array([K])):
        assert np.all(arr == np.round(arr)) and np.all(np.abs(arr) < 2 ** 50), 'non-integer weight'
    W = W.astype(np.int64); T = T.astype(np.int64); V = V.astype(np.int64); K = int(round(K))
    ok = True; worst_true = -10 ** 18; worst_false = 10 ** 18; cnt = 0
    total = 1 << n
    for start in range(0, total, chunk):
        idx = np.arange(start, min(total, start + chunk), dtype=np.int64)
        Z = ((idx[:, None] >> np.arange(n)) & 1).astype(np.int64)
        P = ((Z @ W.T) >= T).astype(np.int64) @ V + K
        addr = sum(((Z[:, N + i * m:N + (i + 1) * m].sum(1) % 2) << i) for i in range(k))
        xb = Z[np.arange(len(Z)), addr]
        out = (P < -N).astype(np.int64)            # five_eighths output rule
        ok &= bool(np.array_equal(out, xb)); cnt += len(Z)
        if (xb == 1).any(): worst_true = max(worst_true, int(P[xb == 1].max()))
        if (xb == 0).any(): worst_false = min(worst_false, int(P[xb == 0].min()))
    formula = (N - 1) * (N + 2) + 3 * k * m * N // 2 + 1
    print(f'k={k} m={m} n={n}: gates={len(gates)} formula={formula} EXACT-correct={ok} on all {cnt} inputs; '
          f'max P on x_b=1: {worst_true} (<{-N}), min P on x_b=0: {worst_false} (>={-N})', flush=True)

for km in sys.argv[1:]:
    exact(*map(int, km.split(',')))
