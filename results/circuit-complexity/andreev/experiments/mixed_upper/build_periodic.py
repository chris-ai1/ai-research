"""Turn a periodic atom set into explicit finite circuits and verify them exactly.

Atom (beta, alpha, p, r, w): beta = weights per count coordinate (part-symmetric), alpha = table weights.
For a box with part sizes h_j it contributes the gates  [L >= theta],  L = beta.c + alpha.x,
theta in (Lmin, Lmax], theta == r (mod p), each with top weight -w*p, plus the linear term w*L and a
constant; together they equal  w*((L-r) mod p)  exactly on the box.
D(x) is either linear (d, d0) or a dict  table-index -> value realised by minterm gates on x.
Output = [top > 0].  All arithmetic is exact (Fractions)."""
import sys
sys.path.insert(0, '/tmp/pydeps')
from fractions import Fraction as Fr
import itertools
import numpy as np


def build(k, parts, atoms, D, linearD=None):
    """parts: list (per block) of part sizes.  Returns (gates, lin_c, lin_x, const) where gates are
    (beta(list per coord), alpha(list per table bit), theta, topweight)."""
    N = 1 << k
    h = [hh for ps in parts for hh in ps]
    gates = []
    lin_c = [Fr(0)] * len(h)
    lin_x = [Fr(0)] * N
    const = Fr(0)
    for (beta, alpha, p, r, w) in atoms:
        w = Fr(w)
        Lmin = sum(min(0, b) * hh for b, hh in zip(beta, h)) + sum(min(0, a) for a in alpha)
        Lmax = sum(max(0, b) * hh for b, hh in zip(beta, h)) + sum(max(0, a) for a in alpha)
        for th in range(Lmin + 1, Lmax + 1):
            if (th - r) % p == 0:
                gates.append((tuple(beta), tuple(alpha), th, -w * p))
        for j, b in enumerate(beta):
            lin_c[j] += w * b
        for c, a in enumerate(alpha):
            lin_x[c] += w * a
        const += -w * r - w * p * ((Lmin - r) // p)
    if linearD is not None:
        d, d0 = linearD
        for c in range(N):
            lin_x[c] += Fr(d[c])
        const += Fr(d0)
    else:
        for t, val in D.items():
            if val == 0:
                continue
            tb = [(t >> c) & 1 for c in range(N)]
            alpha = tuple(2 * v - 1 for v in tb)
            gates.append((tuple([0] * len(h)), alpha, sum(tb), Fr(val)))
    return gates, lin_c, lin_x, const


def eval_counts(k, parts, circ, x, cvec):
    gates, lin_c, lin_x, const = circ
    tot = const
    for (beta, alpha, th, v) in gates:
        L = sum(b * c for b, c in zip(beta, cvec)) + sum(a * xx for a, xx in zip(alpha, x))
        if L >= th:
            tot += v
    tot += sum(l * c for l, c in zip(lin_c, cvec)) + sum(l * xx for l, xx in zip(lin_x, x))
    return tot


def verify_counts(k, parts, circ):
    """all tables x all count vectors (exact).  Returns (ok, min |top|, #points)."""
    N = 1 << k
    h = [hh for ps in parts for hh in ps]
    cb = [i for i, ps in enumerate(parts) for _ in ps]
    gates, lin_c, lin_x, const = circ
    # vectorised exact check with integers: scale by common denominator
    den = 1
    for g in gates:
        den = np.lcm(den, g[3].denominator)
    for l in lin_c + lin_x + [const]:
        den = np.lcm(den, Fr(l).denominator)
    den = int(den)
    tabs = np.array([[(t >> c) & 1 for c in range(N)] for t in range(1 << N)], dtype=np.int64)
    cvs = np.array(list(itertools.product(*[range(hh + 1) for hh in h])), dtype=np.int64)
    s = np.zeros((len(cvs), k), dtype=np.int64)
    for j, i in enumerate(cb):
        s[:, i] += cvs[:, j]
    addr = ((s % 2) * (1 << np.arange(k))[None, :]).sum(1)
    ok = True
    minabs = None
    for ti in range(len(tabs)):
        x = tabs[ti]
        tot = np.full(len(cvs), int(const * den), dtype=object)
        tot = np.zeros(len(cvs), dtype=np.int64) + int(const * den)
        for (beta, alpha, th, v) in gates:
            L = cvs @ np.array(beta, dtype=np.int64) + int(np.dot(alpha, x))
            tot += (L >= th).astype(np.int64) * int(v * den)
        tot += cvs @ np.array([int(l * den) for l in lin_c], dtype=np.int64) + int(sum(int(l * den) * int(xx) for l, xx in zip(lin_x, x)))
        y = x[addr]
        good = np.where(y == 1, tot > 0, tot <= 0)
        if not good.all():
            ok = False
        m_ = np.abs(tot).min()
        minabs = m_ if minabs is None else min(minabs, m_)
    return ok, Fr(int(minabs), den), len(tabs) * len(cvs)


def verify_bits(k, parts, circ):
    """exhaustive over all 2^n bit inputs (n<=22).  Part-symmetric gates: each bit of part p of block i
    carries beta_{i,p}.  Independent of the count reduction."""
    N = 1 << k
    h = [hh for ps in parts for hh in ps]
    cb = [i for i, ps in enumerate(parts) for _ in ps]
    nb = sum(h)
    n = N + nb
    gates, lin_c, lin_x, const = circ
    den = 1
    for g in gates:
        den = np.lcm(den, g[3].denominator)
    for l in lin_c + lin_x + [const]:
        den = np.lcm(den, Fr(l).denominator)
    den = int(den)
    # bit-level weight vectors
    coord_of_bit = []
    for j, hh in enumerate(h):
        coord_of_bit += [j] * hh
    block_of_bit = [cb[j] for j in coord_of_bit]
    Z = ((np.arange(1 << n)[:, None] >> np.arange(n)[None, :]) & 1).astype(np.int64)
    X = Z[:, :N]
    A = Z[:, N:]
    tot = np.zeros(len(Z), dtype=np.int64) + int(const * den)
    for (beta, alpha, th, v) in gates:
        wv = np.array([beta[j] for j in coord_of_bit], dtype=np.int64)
        L = A @ wv + X @ np.array(alpha, dtype=np.int64)
        tot += (L >= th).astype(np.int64) * int(v * den)
    tot += A @ np.array([int(lin_c[j] * den) for j in coord_of_bit], dtype=np.int64)
    tot += X @ np.array([int(l * den) for l in lin_x], dtype=np.int64)
    s = np.zeros((len(Z), k), dtype=np.int64)
    for b in range(nb):
        s[:, block_of_bit[b]] += A[:, b]
    addr = ((s % 2) * (1 << np.arange(k))[None, :]).sum(1)
    y = X[np.arange(len(Z)), addr]
    good = np.where(y == 1, tot > 0, tot <= 0)
    return bool(good.all()), len(Z)
