"""Exact B2 circuit complexity (free negations/constants) by SAT.  size(tt, n) -> min #gates."""
import sys, itertools
from pysat.solvers import Cadical153

def depends(tt, n):
    N = 1 << n
    dep = []
    for i in range(n):
        if any(((tt >> t) & 1) != ((tt >> (t ^ (1 << i))) & 1) for t in range(N)):
            dep.append(i)
    return dep

def has_circuit(tt, n, k, want_model=False):
    N = 1 << n
    if tt & 1:
        tt ^= (1 << N) - 1
    cnt = [0]
    def new():
        cnt[0] += 1
        return cnt[0]
    val = {}
    for i in range(n, n + k):
        for t in range(1, N):
            val[i, t] = new()
    op = {(i, a, b): new() for i in range(n, n + k) for (a, b) in ((0, 1), (1, 0), (1, 1))}
    sel = {}
    cls = []
    for i in range(n, n + k):
        pairs = [(j, l) for j in range(i) for l in range(j + 1, i)]
        for p in pairs:
            sel[i, p[0], p[1]] = new()
        cls.append([sel[i, j, l] for (j, l) in pairs])
    def lit(node, t, a):
        # literal asserting val[node][t] != a ; returns None if trivially false, 'T' if trivially true
        if node < n:
            v = (t >> node) & 1
            return 'T' if v != a else None
        x = val[node, t]
        return -x if a == 1 else x
    for i in range(n, n + k):
        for j in range(i):
            for l in range(j + 1, i):
                s = sel[i, j, l]
                for t in range(1, N):
                    for a in (0, 1):
                        la = lit(j, t, a)
                        if la == 'T':
                            continue
                        for b in (0, 1):
                            lb = lit(l, t, b)
                            if lb == 'T':
                                continue
                            for c in (0, 1):
                                cl = [-s]
                                if la is not None: cl.append(la)
                                if lb is not None: cl.append(lb)
                                cl.append(-val[i, t] if c == 1 else val[i, t])
                                if (a, b) == (0, 0):
                                    if c == 0:
                                        continue
                                else:
                                    o = op[i, a, b]
                                    cl.append(o if c == 1 else -o)
                                cls.append(cl)
    last = n + k - 1
    for t in range(1, N):
        cls.append([val[last, t] if (tt >> t) & 1 else -val[last, t]])
    # every non-last gate is used
    for i in range(n, n + k - 1):
        cls.append([sel[g, j, l] for (g, j, l) in sel if g > i and (j == i or l == i)])
    s = Cadical153(bootstrap_with=cls)
    r = s.solve()
    s.delete()
    return r

def size(tt, n, kmax=12):
    N = 1 << n
    d = depends(tt, n)
    if len(d) <= 1:
        return 0
    k = max(1, len(d) - 1)
    while k <= kmax:
        if has_circuit(tt, n, k):
            return k
        k += 1
    return None
