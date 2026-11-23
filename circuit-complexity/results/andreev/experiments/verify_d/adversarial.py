import sys; sys.path.insert(0,'/tmp/andreev_gap/verify_d')
from impl import *
import time
rng = np.random.default_rng(12345)

def tables(N, b, rng):
    T = []
    z = np.zeros(N, np.int8); o = np.ones(N, np.int8)
    T += [z, o]
    t = o.copy(); t[0] = 0; T.append(t)                 # x0=0, rest 1  (P = N+2N(N-1) max)
    t = z.copy(); t[0] = 1; T.append(t)                 # only x0
    for c in {0, b, N - 1, 1, N // 2}:
        if c < N:
            t = z.copy(); t[c] = 1; T.append(t)         # single-1
            t = o.copy(); t[c] = 0; T.append(t)         # single-0
    for _ in range(6):
        for p in (0.1, 0.5, 0.9):
            T.append((rng.random(N) < p).astype(np.int8))
    # tables with controlled |x'| near extremes and x0 in {0,1}
    for x0 in (0, 1):
        for w in (0, 1, N // 2, N - 2, N - 1):
            t = z.copy(); t[0] = x0
            idx = rng.permutation(np.arange(1, N))[:w]; t[idx] = 1; T.append(t)
    return np.array(T)

def blocks(k, m, b, mode, rng):
    out = np.zeros((k, m), np.int8)
    for i in range(k):
        p = (b >> i) & 1
        ws = [w for w in range(m + 1) if w % 2 == p]
        if mode == 0: w = ws[0]
        elif mode == 1: w = ws[-1]
        elif mode == 2: w = ws[rng.integers(len(ws))]
        else: w = ws[0] if rng.random() < .5 else ws[-1]
        out[i, rng.permutation(m)[:w]] = 1
    return out.reshape(-1)

def run(builder, k, m, merge, budget_b=64):
    c = builder(k, m)
    if merge: c = dedupe(c)
    N = c.N; n = c.n
    bs = list(range(N)) if N <= budget_b else sorted(set([0] + [1 << i for i in range(k)] + [N - 1] + list(rng.integers(0, N, budget_b))))
    wrong = cfbad = 0; mn = 10**18; tot = 0; b0 = 0
    for b in bs:
        for mode in range(4):
            T = tables(N, b, rng)
            blk = blocks(k, m, b, mode, rng)
            Z = np.concatenate([T, np.tile(blk, (len(T), 1))], axis=1).astype(np.int8)
            w, cb, ma = check(c, Z); wrong += w; cfbad += cb; mn = min(mn, ma); tot += len(Z); b0 += (b == 0) * len(Z)
    # fully random inputs
    R = 20000 if c.size < 3000 else 6000
    Z = rng.integers(0, 2, (R, n)).astype(np.int8)
    w, cb, ma = check(c, Z); wrong += w; cfbad += cb; mn = min(mn, ma); tot += R
    return c, wrong, cfbad, mn, tot, b0

if __name__ == "__main__":
    which = sys.argv[1]
    cases = [(3,5),(3,6),(4,2),(4,3),(4,4),(4,6),(4,8),(5,3),(5,4),(5,5),(5,6),(6,3),(6,4),(6,6),(7,2),(7,3),(8,1)]
    if len(sys.argv) > 2: cases = eval(sys.argv[2])
    for (k, m) in cases:
        for builder in ((build_d,) if which == 'd' else (build_c,)):
            for merge in (False, True):
                t0 = time.time()
                c, wrong, cfbad, mn, tot, b0 = run(builder, k, m, merge)
                print(f"{c.name:8s} (k={k},m={m}) n={c.n} N={c.N} gates={c.size} inputs={tot} (b=0: {b0}) wrong={wrong} closedform_mismatch={cfbad} min|P|={mn} [{time.time()-t0:.0f}s]", flush=True)
