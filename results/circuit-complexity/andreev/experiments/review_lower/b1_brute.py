"""Independent brute-force check of Lemma B1 (referee code; does not import anything from push_lower).

Model: gate g = [alpha.x + sum_{i,t} gamma[i,t] a[i,t] >= theta].  Under the count restriction with
arrangement sigma, the address part at grid point s in {0..m}^k is F(s) = sum_i P_i(s_i),
P_i(s) = sum_{t<=s} gamma[i, sigma_i(t)].  For fixed x, alpha.x only shifts theta, so "for every x and theta"
== "for every real threshold th".  A cube c (in {0..m-1}^k) is split iff the 2^k vertex values F(c+z) are
not all on the same side of th.  We compute this DIRECTLY from all 2^k vertices (no extreme-vertex shortcut)
and maximise over ALL thresholds (every dichotomy {F>=th} is realised by th = one of the distinct values of F,
plus th = +inf which splits nothing).  Integer weights, exact arithmetic.

Claim checked: if every block is sign-coherent (all gamma[i,:] >= 0 or all <= 0), then
   #split cubes <= m^k - (m-1)^k     for every sigma and every th.
Also: (i) non-coherent gates CAN exceed the bound (sanity of the checker);
      (ii) exhaustive enumeration of ALL small-integer coherent weight matrices for tiny (k,m)."""
import itertools, sys, random
import numpy as np

def grid_values(gamma, perms):
    k, m = gamma.shape
    P = np.zeros((k, m + 1), dtype=np.int64)
    for i in range(k):
        P[i, 1:] = np.cumsum(gamma[i, perms[i]])
    # F over the grid {0..m}^k as a k-dim array
    F = np.zeros((m + 1,) * k, dtype=np.int64)
    for i in range(k):
        shape = [1] * k; shape[i] = m + 1
        F = F + P[i].reshape(shape)
    return F

def cube_minmax(F, k, m):
    """min and max of F over the 2^k vertices of every unit cube, computed vertex by vertex."""
    sl0 = tuple(slice(0, m) for _ in range(k))
    lo = None; hi = None
    for z in itertools.product((0, 1), repeat=k):
        sl = tuple(slice(zi, zi + m) for zi in z)
        v = F[sl]
        lo = v.copy() if lo is None else np.minimum(lo, v)
        hi = v.copy() if hi is None else np.maximum(hi, v)
    return lo.ravel(), hi.ravel()

def max_split(F, k, m):
    lo, hi = cube_minmax(F, k, m)
    ths = np.unique(F)
    # split iff lo < th <= hi ; count for each candidate th (vectorised by sorting)
    los = np.sort(lo); his = np.sort(hi)
    # #(lo < th) - #(hi < th)  = #{lo<th} - #{hi<th}; cubes with hi<th have lo<th too
    a = np.searchsorted(los, ths, side='left')   # #lo < th
    b = np.searchsorted(his, ths, side='left')   # #hi < th
    cnt = a - b
    j = int(np.argmax(cnt))
    return int(cnt[j]), int(ths[j])

def rand_coherent(k, m, rng, kind):
    sg = rng.choice([-1, 1], size=k)
    if kind == 0:   # small ints with many zeros and ties
        W = rng.integers(0, 3, size=(k, m))
    elif kind == 1: # heavy tailed
        W = (rng.pareto(0.7, size=(k, m)) * 10).astype(np.int64)
    elif kind == 2: # sparse
        W = (rng.random((k, m)) < 0.25) * rng.integers(1, 1000, size=(k, m))
    elif kind == 3: # one huge weight per block + ties
        W = np.ones((k, m), dtype=np.int64); W[np.arange(k), rng.integers(0, m, k)] = 10**6
    elif kind == 4: # some blocks entirely zero
        W = rng.integers(0, 5, size=(k, m)); W[rng.random(k) < 0.4] = 0
    else:           # geometric weights (all subset sums distinct)
        W = np.array([[2 ** rng.integers(0, 20) for _ in range(m)] for _ in range(k)], dtype=np.int64)
    return (W * sg[:, None]).astype(np.int64)

def main():
    rng = np.random.default_rng(2026)
    worst_ratio = 0.0; viol = 0; tight = {}
    for (k, m, trials) in [(1, 5, 300), (2, 2, 400), (2, 3, 400), (2, 5, 400), (2, 8, 300), (3, 2, 400), (3, 3, 400),
                           (3, 5, 300), (4, 2, 300), (4, 3, 300), (4, 4, 200), (5, 2, 200), (5, 3, 150), (6, 2, 100), (6, 3, 40)]:
        bound = m ** k - (m - 1) ** k; best = 0
        for t in range(trials):
            gamma = rand_coherent(k, m, rng, t % 6)
            perms = [rng.permutation(m) for _ in range(k)]
            F = grid_values(gamma, perms)
            c, th = max_split(F, k, m)
            best = max(best, c)
            if c > bound:
                viol += 1; print('VIOLATION', k, m, gamma.tolist(), perms, th, c, bound)
        tight[(k, m)] = (best, bound)
        print(f'coherent random  k={k} m={m}: max split over {trials} gates x all thresholds = {best}   bound m^k-(m-1)^k = {bound}', flush=True)
    # exhaustive: all coherent integer matrices with entries in {0..2} (times a sign per block), all sigma = id
    # (sigma only permutes the columns, which the exhaustive enumeration already covers)
    for (k, m, W) in [(2, 2, 3), (2, 3, 3), (3, 2, 3), (2, 4, 2), (3, 3, 2)]:
        bound = m ** k - (m - 1) ** k; best = 0; n = 0
        for signs in itertools.product((1, -1), repeat=k):
            for flat in itertools.product(range(W), repeat=k * m):
                gamma = np.array(flat, dtype=np.int64).reshape(k, m) * np.array(signs)[:, None]
                F = grid_values(gamma, [np.arange(m)] * k)
                c, _ = max_split(F, k, m); n += 1
                best = max(best, c)
                if c > bound: viol += 1; print('VIOLATION(exh)', k, m, gamma.tolist(), c)
        print(f'coherent EXHAUSTIVE k={k} m={m} entries 0..{W-1} x block signs ({n} gates): max split = {best}  bound = {bound}', flush=True)
    # sanity: non-coherent gates must be able to exceed the bound (else the checker is vacuous)
    for (k, m) in [(2, 4), (3, 4), (2, 8)]:
        bound = m ** k - (m - 1) ** k; best = 0
        for t in range(400):
            gamma = rng.choice([-1, 1], size=(k, m)).astype(np.int64)
            F = grid_values(gamma, [rng.permutation(m) for _ in range(k)])
            best = max(best, max_split(F, k, m)[0])
        print(f'NON-coherent +-1 k={k} m={m}: max split = {best}  (coherent bound {bound}; exceeding it is expected)', flush=True)
    print('total violations of Lemma B1:', viol)

if __name__ == '__main__':
    main()
