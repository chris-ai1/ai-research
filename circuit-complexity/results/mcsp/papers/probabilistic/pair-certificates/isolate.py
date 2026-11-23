"""Find 4-variable XOR faces (L, L') at threshold t whose AND-paddings are isolated easy tables.
Checks, for X in {L, L'} and every 4-bit point g:
 (I0) C(X + 1_g) >= t+1                                   [4-variable table]
 (I1) C( r ? X : 1_g ) >= t+2                               [5 variables, bitmap]
 (I2) C( r1 r2 X  or  ~r1 ~r2 1_g ) >= t+3                  [6 variables: one restriction to a 5-variable function with C >= t+2]
 (I3) C( r1 r2 r3 X  or  ~r1 ~r2 ~r3 1_g ) >= t+4           [7 variables: two restrictions], only needed when t = 4 and X(g) = 1
(I1),(I2) are only needed for g close to the support of X, but we simply require them where the general bound does not apply."""
import pickle, mmap, sys, itertools
comp = pickle.load(open('comp4.pkl','rb'))
bms = {}
for G in (4,5,6):
    f = open('bm5_%d.bin' % G, 'rb'); bms[G] = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
def easy5(tt, G): return (bms[G][tt >> 3] >> (tt & 7)) & 1
def ttable(nv, fn):
    t = 0
    for r in range(1 << nv):
        if fn(r): t |= 1 << r
    return t
def restrict(tt, nv, i, v):
    """fix variable i to v; result on nv-1 variables (remaining variables keep their order)"""
    out = 0; k = 0
    for r in range(1 << nv):
        if ((r >> i) & 1) != v: continue
        if (tt >> r) & 1: out |= 1 << k
        k += 1
    return out
def essential(tt, nv, i): return restrict(tt, nv, i, 0) != restrict(tt, nv, i, 1)
def dist_to_support(X, g):
    return min(bin(g ^ p).count('1') for p in range(16) if (X >> p) & 1)
def cert(tt, nv, need, depth):
    """True if we can certify C(tt) >= need by `depth` restrictions of essential variables ending at a 5-variable function not computable with need-depth-1 gates"""
    if nv == 5:
        return not easy5(tt, need - 1)
    for i in range(nv):
        if not essential(tt, nv, i): continue
        for v in (0, 1):
            if cert(restrict(tt, nv, i, v), nv - 1, need - 1, depth - 1): return True
    return False
def isolated(X, t):
    e = t - 4
    for g in range(16):
        if comp[X ^ (1 << g)] < t + 1: return False
    for g in range(16):
        m = dist_to_support(X, g)
        for J in (1, 2, 3):
            if m + J >= e + 4: continue            # general bound applies
            nv = 4 + J
            if J == 1:   fn = lambda r: ((X >> (r & 15)) & 1) if (r >> 4) & 1 else int((r & 15) == g)
            elif J == 2: fn = lambda r: ((X >> (r & 15)) & 1) if (r >> 4) == 3 else (int((r & 15) == g) if (r >> 4) == 0 else 0)
            else:        fn = lambda r: ((X >> (r & 15)) & 1) if (r >> 4) == 7 else (int((r & 15) == g) if (r >> 4) == 0 else 0)
            if not cert(ttable(nv, fn), nv, t + J + 1, J - 1): return False
    return True
for t in (3, 4):
    cache = {}
    for d, b in ((1,1),(2,3),(3,7),(4,15)):
        ma, mb = 1, 1 << b
        tot = good = 0; ex = None
        for f in range(1 << 16):
            if f & (ma | mb): continue
            for L in (f, f | ma):                      # the two possible easy diagonals
                L2 = L ^ ma ^ mb
                if comp[L] > t or comp[L2] > t: continue
                if comp[L ^ ma] <= t or comp[L ^ mb] <= t: continue
                tot += 1
                ok = True
                for X in (L, L2):
                    if X not in cache: cache[X] = isolated(X, t)
                    if not cache[X]: ok = False; break
                if ok:
                    good += 1
                    if ex is None: ex = (hex(L), hex(L2))
        print('t=%d distance %d: XOR faces %d, with both easy corners padding-isolated: %d, example %s' % (t, d, tot, good, ex), flush=True)
