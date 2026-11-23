"""Referee check of the Ring Lemma (Theorem E), independent code.
Claim: for EVERY up-set U of the vertex grid {0..m}^2 (componentwise order), at most 4 of the 4(m-1)
boundary unit squares Q have |U cap Q| in {1,3}.  (The 1-set of a sign-coherent k=2 gate is such an up-set
after reflections, for every table and arrangement.)
We enumerate ALL up-sets: U = {(a,b): b >= h(a)}, h:{0..m}->{0..m+1} non-increasing (binom(2m+2,m+1) of them).
For each we count corner-cut squares directly from the 4 vertices.  Also record the max total number of cut
squares (claim in ring_lemma.py: <= 2m-1), and check the 1-sets of random separable monotone functions
P1(s1)+P2(s2) >= th (with zero increments / ties) are up-sets and obey the same bound."""
import itertools, sys
import numpy as np

def nonincreasing_seqs(length, top):
    # all sequences h(0)>=h(1)>=...>=h(length-1) with values in {0..top}
    def rec(prefix, maxv):
        if len(prefix) == length:
            yield tuple(prefix); return
        for v in range(maxv, -1, -1):
            prefix.append(v); yield from rec(prefix, v); prefix.pop()
    yield from rec([], top)

def check(m):
    sq = [(a, b) for a in range(m) for b in range(m)]
    bnd = np.array([a in (0, m - 1) or b in (0, m - 1) for a, b in sq])
    A = np.array([a for a, b in sq]); B = np.array([b for a, b in sq])
    worst_b = 0; worst_t = 0; n = 0; ex = None
    H = np.array(list(nonincreasing_seqs(m + 1, m + 1)), dtype=np.int64)      # (#upsets, m+1)
    n = len(H)
    # membership of vertex (a,b): b >= h(a)
    inU = lambda a, b: (b[None, :] >= H[:, a]) if True else None
    v00 = B[None, :] >= H[:, A]; v10 = B[None, :] >= H[:, A + 1]
    v01 = (B + 1)[None, :] >= H[:, A]; v11 = (B + 1)[None, :] >= H[:, A + 1]
    cnt = v00.astype(np.int8) + v10 + v01 + v11
    cut = (cnt == 1) | (cnt == 3)
    nb = (cut & bnd[None, :]).sum(1); nt = cut.sum(1)
    worst_b = int(nb.max()); worst_t = int(nt.max())
    ex = H[int(np.argmax(nb))]
    return n, worst_b, worst_t, ex

def separable_check(m, trials, rng):
    """random monotone P1,P2 (non-decreasing, with zero steps), all thresholds: 1-set must be an up-set
    and have <=4 boundary corner cuts."""
    sq = [(a, b) for a in range(m) for b in range(m)]
    bnd = [a in (0, m - 1) or b in (0, m - 1) for a, b in sq]
    worst = 0
    for _ in range(trials):
        P1 = np.concatenate([[0], np.cumsum(rng.integers(0, 3, m))]); P2 = np.concatenate([[0], np.cumsum(rng.integers(0, 3, m))])
        F = P1[:, None] + P2[None, :]
        for th in np.unique(F):
            U = F >= th
            # up-set check
            assert (U[1:, :] >= U[:-1, :]).all() and (U[:, 1:] >= U[:, :-1]).all()
            c = 0
            for (a, b), isb in zip(sq, bnd):
                if not isb: continue
                s = int(U[a, b]) + int(U[a + 1, b]) + int(U[a, b + 1]) + int(U[a + 1, b + 1])
                c += s in (1, 3)
            worst = max(worst, c)
    return worst

if __name__ == '__main__':
    rng = np.random.default_rng(7)
    for m in range(2, int(sys.argv[1]) + 1 if len(sys.argv) > 1 else 11):
        n, wb, wt, ex = check(m)
        ws = separable_check(m, 200, rng) if m <= 9 else -1
        print(f'm={m}: all {n} up-sets: max boundary corner-cuts = {wb} (lemma <= 4);  max total corner-cuts = {wt} (2m-1 = {2*m-1});'
              f'  separable-monotone random max boundary cuts = {ws};  extremal h = {ex.tolist()}', flush=True)
