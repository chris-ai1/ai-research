r"""Sanity check of the multiplicity-peeling inequality (Theorem 3 of nondet-average-case.md).

Random layered read-once NBP on n binary variables (variable t read at step t), random S.
rho  = max over rectangles R at the prefix cuts t (both sides >= K) of |R & S| / |R \ S|.
Peeling: while some state (t,q) has a peer class (w.r.t. chosen = lexicographically least
accepting path) with >= K distinct prefixes and >= K distinct suffixes, delete the state.
We check, for every run:
  (a) at each peel, |E & S| <= rho * |R \ S|  where E = inputs removed, R = full rectangle of q,
  (b) |A & S| <= rho * sum_{y in A\S} paths(y) + |A_final & S|,
  (c) |A_final| <= (K-1)^2 * (#edges of the final program)   (rectangle bound),
  (d) peel count of each y in A\S <= paths(y).
"""
import itertools, random, sys
from fractions import Fraction

def run(n, W, K, pedge, pS, seed):
    rnd = random.Random(seed)
    # states: layer 0 = {0}, layers 1..n-1 = range(W), layer n = {0} (accept)
    def layer_states(t): return [0] if t in (0, n) else list(range(W))
    edges = set()
    for t in range(n):
        for q in layer_states(t):
            for a in (0, 1):
                for r in layer_states(t + 1):
                    if rnd.random() < pedge: edges.add((t, q, a, r))
    S = {x for x in itertools.product((0, 1), repeat=n) if rnd.random() < pS}
    alive = {(t, q) for t in range(n + 1) for q in layer_states(t)}

    def paths(x, alive):
        # all accepting paths as tuples of states
        out = [(0,)]
        for t in range(n):
            new = []
            for p in out:
                for r in layer_states(t + 1):
                    if (t, p[-1], x[t], r) in edges and (t + 1, r) in alive and (t, p[-1]) in alive:
                        new.append(p + (r,))
            out = new
        return out

    X = list(itertools.product((0, 1), repeat=n))
    P0 = {x: paths(x, alive) for x in X}
    A0 = {x for x in X if P0[x]}
    # rho over prefix cuts, sides >= K (exact: enumerate smaller side, greedy on the other)
    rho = Fraction(0)
    for t in range(1, n):
        L = list(itertools.product((0, 1), repeat=t)); Rr = list(itertools.product((0, 1), repeat=n - t))
        small, big, swap = (L, Rr, False) if len(L) <= len(Rr) else (Rr, L, True)
        if len(small) < K or len(big) < K: continue
        for k in range(K, len(small) + 1):
            for sub in itertools.combinations(small, k):
                items = []
                for b in big:
                    s = sum(1 for a in sub if ((b + a) if swap else (a + b)) in S)
                    items.append((s, k - s))
                items.sort(key=lambda sz: (Fraction(sz[0], sz[1]) if sz[1] else Fraction(10**9)), reverse=True)
                cs = cz = 0
                for j, (s, z) in enumerate(items, 1):
                    cs += s; cz += z
                    if j >= K:
                        val = Fraction(cs, cz) if cz else Fraction(10**9)
                        rho = max(rho, val)
    if rho >= 10**9: return None  # monochromatic large rectangle: hypothesis vacuous
    peelcount = {x: 0 for x in X}
    A = set(A0)
    while True:
        P = {x: paths(x, alive) for x in A}
        chosen = {x: min(P[x]) for x in A}
        found = None
        for t in range(1, n):
            for q in layer_states(t):
                if (t, q) not in alive: continue
                peers = [x for x in A if chosen[x][t] == q]
                if len({x[:t] for x in peers}) >= K and len({x[t:] for x in peers}) >= K:
                    found = (t, q); break
            if found: break
        if not found: break
        t, q = found
        R = {x for x in A if any(p[t] == q for p in P[x])}   # full rectangle of q (inside A)
        alive.discard(found)
        Anew = {x for x in A if paths(x, alive)}
        E = A - Anew
        assert len(E & S) <= rho * len(R - S), "(a) failed"
        for y in R - S: peelcount[y] += 1
        A = Anew
    nedges = sum(1 for (t, q, a, r) in edges if (t, q) in alive and (t + 1, r) in alive)
    lhs = len(A0 & S)
    rhs = rho * sum(len(P0[y]) for y in A0 - S) + len(A & S)
    assert lhs <= rhs, "(b) failed"
    assert len(A) <= (K - 1) ** 2 * max(nedges, 1), "(c) failed"
    assert all(peelcount[y] <= len(P0[y]) for y in A0 - S), "(d) failed"
    return dict(A=len(A0), AS=lhs, AnotS=len(A0 - S), paths_false=sum(len(P0[y]) for y in A0 - S),
                rho=float(rho), final=len(A), finalS=len(A & S))

if __name__ == "__main__":
    n, W, K = 6, 4, 4
    done = 0
    for seed in range(int(sys.argv[1]) if len(sys.argv) > 1 else 40):
        r = run(n, W, K, pedge=0.45, pS=0.5, seed=seed)
        if r is None: continue
        done += 1
        print(seed, r)
    print("checked", done, "instances; all assertions (a)-(d) held")
