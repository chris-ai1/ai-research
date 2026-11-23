"""Periodic ('bulk') LP for the asymptotic slope of A_{k,m} in m at fixed k.

Atom = (beta, alpha, p, r): a staircase on the linear form L = beta.c + alpha.x whose thresholds are all
theta == r (mod p) in the range of L, with one common top weight -w*p.  Up to a linear form (free in the
top gate) and a constant it contributes exactly
        w * ((L - r) mod p)
on the WHOLE box, for every m (no boundary effects).  It costs  ||beta||_1 * h / p + O(1)  gates, where h
is the size of every count coordinate (h=m for block-symmetric coordinates, m/2 for two halves).
Any function D(x) of the table alone costs O(1) at fixed k (free for the slope).

So:  slope <= min over atom sets  sum_a ||beta_a||_1 * (h/m) / p_a   subject to
     sign( sum_a w_a ((L_a - r_a) mod p_a) + D(x) ) = 2 x_b - 1   for all x and all residues c mod P,
P = lcm(2, p_a).  Correctness on residues mod P implies correctness for every m (all residues occur once
m >= P-1; for smaller m only a subset occurs).
"""
import sys
sys.path.insert(0, '/tmp/pydeps')
import itertools, time, math
import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds
from scipy import sparse


class PDomain:
    def __init__(self, k, ncoord_per_block, P, tables=None):
        self.k = k
        self.N = N = 1 << k
        self.P = P
        self.cb = []
        for i in range(k):
            self.cb += [i] * ncoord_per_block
        self.nc = len(self.cb)
        if tables is None:
            tables = ((np.arange(1 << N)[:, None] >> np.arange(N)[None, :]) & 1).astype(np.int64)
        self.tables = np.asarray(tables, dtype=np.int64)
        res = np.array(list(itertools.product(range(P), repeat=self.nc)), dtype=np.int64)
        self.res = res
        nt, nr = len(self.tables), len(res)
        self.tix = np.repeat(np.arange(nt), nr)
        self.X = self.tables[self.tix]
        self.C = np.tile(res, (nt, 1))
        self.npts = len(self.X)
        s = np.zeros((nr, k), dtype=np.int64)
        for j, i in enumerate(self.cb):
            s[:, i] += res[:, j]
        addr = ((s % 2) * (1 << np.arange(k))[None, :]).sum(1)
        addr = np.tile(addr, nt)
        self.y = self.X[np.arange(self.npts), addr]
        self.sig = 2 * self.y - 1


class Atoms:
    def __init__(self, dom, h_over_m):
        self.dom = dom
        self.hm = h_over_m
        self.spec = []      # (beta tuple, alpha tuple, p, r)
        self.cols = []
        self.cost = []
        self._seen = {}

    def add(self, beta, alpha, p, r):
        dom = self.dom
        beta = np.asarray(beta, dtype=np.int64)
        alpha = np.asarray(alpha, dtype=np.int64)
        L = dom.C @ beta + dom.X @ alpha
        col = np.mod(L - r, p).astype(np.float64)
        if np.all(col == col[0]):
            return False
        key = col.tobytes()
        c = float(np.abs(beta).sum()) * self.hm / p
        if key in self._seen:
            j = self._seen[key]
            if c < self.cost[j]:
                self.cost[j] = c
                self.spec[j] = (tuple(beta), tuple(alpha), p, r)
            return False
        self._seen[key] = len(self.spec)
        self.spec.append((tuple(beta), tuple(alpha), p, r))
        self.cols.append(col)
        self.cost.append(c)
        return True

    def matrix(self, idx=None):
        M = np.array(self.cols).T
        return M if idx is None else M[:, idx]


def lp_weighted_l1(dom, atoms, weights, sel=None, linearD=False):
    """min sum weights_a |w_a| s.t. sig*(M w + D) >= 1.  D per table (free) or linear in x."""
    M = atoms.matrix(sel)
    A = M.shape[1]
    nt = len(dom.tables)
    sg = dom.sig.astype(np.float64)[:, None]
    if linearD:
        Dm = np.hstack([dom.X.astype(np.float64), np.ones((dom.npts, 1))])
    else:
        Dm = sparse.csr_matrix((np.ones(dom.npts), (np.arange(dom.npts), dom.tix)), shape=(dom.npts, nt)).toarray()
    nd = Dm.shape[1]
    Aub = np.hstack([-sg * M, sg * M, -sg * Dm])
    b = -np.ones(dom.npts)
    c = np.concatenate([weights, weights, np.zeros(nd)])
    bounds = [(0, None)] * (2 * A) + [(None, None)] * nd
    res = linprog(c, A_ub=sparse.csr_matrix(Aub), b_ub=b, bounds=bounds, method='highs')
    if res.status != 0:
        return None
    w = res.x[:A] - res.x[A:2 * A]
    return w, res.x[2 * A:], res.fun


def feasible(dom, atoms, sel, linearD=False):
    r = lp_weighted_l1(dom, atoms, np.zeros(len(sel)), sel=sel, linearD=linearD)
    return r is not None


def min_cost_milp(dom, atoms, sel=None, time_limit=300, Mbig=100.0, linearD=False, verbose=False):
    """exact min sum cost_a [w_a != 0] over the given atoms (big-M, |w|<=Mbig)."""
    if sel is None:
        sel = list(range(len(atoms.spec)))
    M = atoms.matrix(sel)
    A = M.shape[1]
    nt = len(dom.tables)
    sg = dom.sig.astype(np.float64)[:, None]
    if linearD:
        Dm = np.hstack([dom.X.astype(np.float64), np.ones((dom.npts, 1))])
    else:
        Dm = sparse.csr_matrix((np.ones(dom.npts), (np.arange(dom.npts), dom.tix)), shape=(dom.npts, nt)).toarray()
    nd = Dm.shape[1]
    # vars: w (A), D (nd), y (A)
    A1 = np.hstack([sg * M, sg * Dm, np.zeros((dom.npts, A))])
    I = sparse.identity(A, format='csr')
    Z = sparse.csr_matrix((A, nd))
    cons = [LinearConstraint(sparse.csr_matrix(A1), lb=1.0, ub=np.inf),
            LinearConstraint(sparse.hstack([I, Z, -Mbig * I]).tocsr(), lb=-np.inf, ub=0),
            LinearConstraint(sparse.hstack([-I, Z, -Mbig * I]).tocsr(), lb=-np.inf, ub=0)]
    cost = np.array([atoms.cost[j] for j in sel])
    c = np.concatenate([np.zeros(A + nd), cost])
    integrality = np.concatenate([np.zeros(A + nd), np.ones(A)])
    lb = np.concatenate([-Mbig * np.ones(A), -1e5 * np.ones(nd), np.zeros(A)])
    ub = np.concatenate([Mbig * np.ones(A), 1e5 * np.ones(nd), np.ones(A)])
    res = milp(c, constraints=cons, integrality=integrality, bounds=Bounds(lb, ub),
               options={'time_limit': time_limit, 'disp': verbose})
    if res.x is None:
        return None
    y = res.x[-A:]
    chosen = [sel[j] for j in range(A) if y[j] > 0.5]
    return chosen, res.fun, getattr(res, 'mip_dual_bound', None), res.status


def greedy_prune(dom, atoms, sel, linearD=False):
    sel = sorted(sel, key=lambda j: -atoms.cost[j])
    i = 0
    while i < len(sel):
        trial = sel[:i] + sel[i + 1:]
        if feasible(dom, atoms, trial, linearD):
            sel = trial
        else:
            i += 1
    return sel


def reweighted(dom, atoms, iters=10, eps=1e-3, linearD=False, verbose=False):
    A = len(atoms.spec)
    cost = np.array(atoms.cost)
    wts = cost.copy()
    best = None
    for it in range(iters):
        r = lp_weighted_l1(dom, atoms, wts, linearD=linearD)
        if r is None:
            return None
        w = r[0]
        supp = [j for j in range(A) if abs(w[j]) > 1e-7 * max(1, np.abs(w).max())]
        tot = sum(atoms.cost[j] for j in supp)
        if verbose:
            print(f'   rw it {it}: support {len(supp)} cost {tot:.3f}', flush=True)
        if best is None or tot < best[1]:
            best = (supp, tot)
        wts = cost / (np.abs(w) + eps * max(1, np.abs(w).max()))
    return best
