"""Stronger adversaries for the single-cut XOR/OR example (review of v3 section 5).

bias(P,B) = |sum_{(q,q') in P, b in B} sig| / (|P||B|), sig = (-1)^S  (same normalisation as the note's script).
Adversaries:
  alt      : alternating top-K rows / top-K columns from random starts (the note's greedy), more restarts + perturbation (ILS)
  biclique : P = Q x Q' with |Q||Q'| = K, alternating over (Q, Q', B) using the product structure; then polished by alt
The same generic adversary (alt + ILS, same budget) is run on an i.i.d. sign matrix.
"""
import sys, numpy as np

def alt(sig, r, K, sign, iters=40):
    for _ in range(iters):
        col = sign * sig[r].sum(0, dtype=np.int32)
        c = np.argpartition(-col, K)[:K]
        row = sign * sig[:, c].sum(1, dtype=np.int32)
        r2 = np.argpartition(-row, K)[:K]
        if set(r2.tolist()) == set(r.tolist()): break
        r = r2
    col = sign * sig[r].sum(0, dtype=np.int32)
    c = np.argpartition(-col, K)[:K]
    return r, c, float(col[c].sum()) / (K * K)

def ils(sig, K, rng, starts, rounds=6, frac=0.25):
    best = 0.0
    R = sig.shape[0]
    for s in starts:
        for sign in (1, -1):
            r, c, v = alt(sig, np.array(s), K, sign)
            for _ in range(rounds):
                r2 = r.copy()
                idx = rng.choice(K, int(frac * K), replace=False)
                r2[idx] = rng.choice(R, len(idx), replace=False)
                r2 = np.unique(r2)
                if len(r2) < K:
                    extra = np.setdiff1d(rng.choice(R, 3 * K, replace=False), r2)[:K - len(r2)]
                    r2 = np.concatenate([r2, extra])
                r3, c3, v3 = alt(sig, r2, K, sign)
                if v3 > v: r, c, v = r3, c3, v3
            best = max(best, v)
    return best

def biclique(Y, Yp, K, a, rng, tries=40, iters=40):
    """max over Q (|Q|=a), Q' (|Q'|=K//a), B (|B|=K) of sum_{b in B} s_Q(b) s_Q'(b) / (a*(K//a)*K)."""
    M, m = Y.shape; ap = K // a; best = (0.0, None)
    for _ in range(tries):
        for sign in (1, -1):
            Q = rng.choice(M, a, replace=False); Qp = rng.choice(M, ap, replace=False)
            last = None
            for _ in range(iters):
                sQ = Y[Q].sum(0, dtype=np.int32); sQp = Yp[Qp].sum(0, dtype=np.int32)
                B = np.argpartition(-(sign * sQ * sQp), K)[:K]
                Q = np.argpartition(-(sign * (Y[:, B] @ sQp[B])), a - 1)[:a] if a < M else np.arange(M)
                sQ = Y[Q].sum(0, dtype=np.int32)
                Qp = np.argpartition(-(sign * (Yp[:, B] @ sQ[B])), ap - 1)[:ap] if ap < M else np.arange(M)
                key = (tuple(sorted(Q)), tuple(sorted(Qp)))
                if key == last: break
                last = key
            sQ = Y[Q].sum(0, dtype=np.int32); sQp = Yp[Qp].sum(0, dtype=np.int32)
            prod = sign * sQ * sQp
            B = np.argpartition(-prod, K)[:K]
            v = float(prod[B].sum()) / (a * ap * K)
            if v > best[0]: best = (v, (Q.copy(), Qp.copy()))
    return best

def main(M, m, K, seed=0, n_starts=40):
    rng = np.random.default_rng(seed)
    g = rng.integers(0, 2, (M, m)); gp = rng.integers(0, 2, (M, m))
    Y = (1 - 2 * g).astype(np.int32); Yp = (1 - 2 * gp).astype(np.int32)
    q, qp = np.divmod(np.arange(M * M), M)
    sig = (Y[q] * Yp[qp]).astype(np.int8)
    rnd = rng.choice(np.array([-1, 1], dtype=np.int8), size=sig.shape)
    starts = [rng.choice(M * M, K, replace=False) for _ in range(n_starts)]
    print(f'M={M} rows={M*M} cols={m} K={K}  (ln m)^2={np.log(m)**2:.0f}  M>=K: {M>=K}  M>=2K: {M>=2*K}', flush=True)
    vS = ils(sig, K, rng, starts); vR = ils(rnd, K, rng, starts)
    print(f'  generic alt+ILS      S: {vS:.4f}   iid: {vR:.4f}', flush=True)
    bestb = 0.0; pol = 0.0
    for a in sorted({x for x in (1, 2, 4, 8, int(K ** 0.5), K // 8, K // 4, K // 2, K, max(1, K // M), min(M, K)) if 1 <= x <= M and K // x <= M and K // x >= 1}):
        v, (Q, Qp) = biclique(Y, Yp, K, a, rng)
        rows = np.array([i * M + j for i in Q for j in Qp])
        if len(rows) < K:
            rows = np.concatenate([rows, np.setdiff1d(rng.choice(M * M, 2 * K, replace=False), rows)[:K - len(rows)]])
        p = max(alt(sig, rows[:K], K, s)[2] for s in (1, -1))
        print(f'  biclique |Q|={a:4d} |Qp|={K//a:4d}: {v:.4f}   polished by alt: {p:.4f}', flush=True)
        bestb = max(bestb, v); pol = max(pol, p)
    print(f'  best structured S: {max(bestb, pol):.4f}   ratio to iid: {max(bestb, pol, vS)/vR:.3f}', flush=True)
    # other cuts, fixed b0: monochromatic rectangle sizes
    b0 = 0
    print(f'  cut ({{q,b}}|{{q\'}}) and its mirror, the PREFIX cut ({{q}}|{{q\',b}}): S constant on a '
          f'{int((g[:, b0]==0).sum())} x {int((gp[:, b0]==0).sum())} rectangle (large iff >= K={K})')

if __name__ == '__main__':
    cfgs = [(40, 4096, 400), (64, 8192, 1024), (128, 4096, 64), (160, 2048, 80)]
    if len(sys.argv) > 1: cfgs = [tuple(int(x) for x in a.split(',')) for a in sys.argv[1:]]
    for M, m, K in cfgs:
        main(M, m, K); print()
