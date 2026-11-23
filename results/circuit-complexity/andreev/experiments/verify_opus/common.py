"""Shared helpers (independent re-implementation): point sets, target, exact circuit check."""
import itertools
from fractions import Fraction as F


def andreev_points(k, m, mode):
    """Return list of (p, out). p = table bits x_0..x_{N-1} followed by
    full:     k*m address bits (block i = coords N+i*m .. N+i*m+m-1)
    thermo:   like full, but only thermometer blocks 1^s 0^(m-s)  (a subset of full's points)
    blocksym: k block weights s_0..s_{k-1} in 0..m.
    Address b = sum_i (s_i mod 2) 2^i ; out = x_b."""
    N = 1 << k
    pts = []
    if mode == 'blocksym':
        addr_space = list(itertools.product(range(m + 1), repeat=k))
        wt = lambda a: a
    elif mode == 'thermo':
        # sub-instance of 'full': every block is a thermometer string 1^s 0^(m-s).  UNSAT here
        # implies UNSAT for full (subset of the constraints) -> valid general lower bounds.
        therm = [tuple([1] * s + [0] * (m - s)) for s in range(m + 1)]
        addr_space = [sum(c, ()) for c in itertools.product(therm, repeat=k)]
        wt = lambda a: tuple(sum(a[i * m:(i + 1) * m]) for i in range(k))
    elif mode == 'full':
        addr_space = list(itertools.product((0, 1), repeat=k * m))
        wt = lambda a: tuple(sum(a[i * m:(i + 1) * m]) for i in range(k))
    else:
        raise ValueError(mode)
    for x in itertools.product((0, 1), repeat=N):
        for a in addr_space:
            s = wt(a)
            b = 0
            for i in range(k):
                if s[i] % 2:
                    b |= 1 << i
            pts.append((tuple(x) + tuple(a), x[b]))
    return pts


def eval_circuit(circ, pts):
    """circ = dict(bottom=[(alpha(list), theta)], v=[...], u=[...], tau=...), all Fractions/ints.
    Gate semantics exactly as defined: [sum >= threshold].  Returns list of failing points."""
    bad = []
    for p, out in pts:
        g = [1 if sum(F(a) * c for a, c in zip(al, p)) >= F(th) else 0 for al, th in circ['bottom']]
        top = sum(F(vj) * gj for vj, gj in zip(circ['v'], g)) + sum(F(uj) * c for uj, c in zip(circ['u'], p))
        if (1 if top >= F(circ['tau']) else 0) != out:
            bad.append((p, out))
    return bad
