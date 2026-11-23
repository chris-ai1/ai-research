"""Core LP/MILP machinery for gate-pool experiments on Andreev's function A_{k,m}.

Count-vector model.  Block i (m bits) is partitioned into parts P_{i,1..r_i} of sizes h_{i,p}.
A gate is *part-symmetric* if its weight is constant on every part:  g = [alpha.x + beta.c >= theta],
where c_{i,p} = number of ones of block i inside part p.  If every bottom gate is part-symmetric, the
top gate may be symmetrised (average over permutations inside parts: the target and all gates are
invariant, the margin condition is convex), so the top sum is  sum_j v_j g_j + mu.x + nu.c - t0.
Hence the circuit is correct on all 2^n inputs iff it is correct on all count vectors (x,c), and the
bit-level circuit is obtained by giving every bit of part p of block i the weight beta_{i,p} (bottom)
or nu_{i,p} (top).  Block-symmetric = one part per block.

Domain points: all tables x in {0,1}^N (or a subset) times all count vectors.
Target: x_b with b_i = (sum_p c_{i,p}) mod 2, table index c = sum_i b_i 2^i.
"""
import sys
sys.path.insert(0, '/tmp/pydeps')
import itertools, time
import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds
from scipy import sparse


class Domain:
    def __init__(self, k, parts, tables=None):
        self.k = k
        self.N = N = 1 << k
        self.parts = [list(p) for p in parts]          # parts[i] = list of part sizes of block i
        self.coord_block = []
        self.coord_size = []
        for i, ps in enumerate(self.parts):
            for h in ps:
                self.coord_block.append(i)
                self.coord_size.append(h)
        self.nc = len(self.coord_size)
        if tables is None:
            # row t: x_c = bit c of t  (column c)
            tables = ((np.arange(1 << N)[:, None] >> np.arange(N)[None, :]) & 1).astype(np.int8)
        self.tables = np.asarray(tables, dtype=np.int8)
        cvs = np.array(list(itertools.product(*[range(h + 1) for h in self.coord_size])), dtype=np.int16)
        self.cvs = cvs
        nt, ncv = len(self.tables), len(cvs)
        self.X = np.repeat(self.tables, ncv, axis=0)
        self.C = np.tile(cvs, (nt, 1))
        self.P = len(self.X)
        # address
        svec = np.zeros((ncv, k), dtype=np.int64)
        for j, i in enumerate(self.coord_block):
            svec[:, i] += cvs[:, j]
        addr_cv = ((svec % 2) * (1 << np.arange(k))[None, :]).sum(1)
        addr = np.tile(addr_cv, nt)
        self.y = self.X[np.arange(self.P), addr].astype(np.int8)
        self.sig = (2 * self.y.astype(np.int64) - 1)
        # bit-level multiplicity of each count vector (for reporting only)
        from math import comb
        mult = np.ones(ncv, dtype=object)
        for j, h in enumerate(self.coord_size):
            mult = mult * np.array([comb(h, int(v)) for v in cvs[:, j]], dtype=object)
        self.mult_cv = mult

    def n_bits(self):
        return self.N + sum(self.coord_size)


class Pool:
    """A pool of gates given by directions (alpha, beta) and threshold lists."""
    def __init__(self, dom):
        self.dom = dom
        self.alpha = []
        self.beta = []
        self.theta = []
        self.tag = []
        self._seen = set()

    def add_direction(self, alpha, beta, tag='', thetas=None, dedupe=True):
        dom = self.dom
        alpha = np.asarray(alpha, dtype=np.int64)
        beta = np.asarray(beta, dtype=np.int64)
        L = dom.X.astype(np.int64) @ alpha + dom.C.astype(np.int64) @ beta
        vals = np.unique(L)
        if thetas is None:
            thetas = vals[1:]
        added = 0
        for th in thetas:
            th = int(th)
            if th <= vals[0] or th > vals[-1]:
                continue
            if dedupe:
                col = (L >= th)
                key = hash(np.packbits(col).tobytes())
                keyc = hash(np.packbits(~col).tobytes())
                if key in self._seen or keyc in self._seen:
                    continue
                self._seen.add(key)
            self.alpha.append(alpha)
            self.beta.append(beta)
            self.theta.append(th)
            self.tag.append(tag)
            added += 1
        return added

    def __len__(self):
        return len(self.theta)

    def columns(self, idx_pts, gates=None):
        """dense matrix of gate values on the given points (int8)."""
        dom = self.dom
        if gates is None:
            gates = range(len(self))
        gates = list(gates)
        Xp = dom.X[idx_pts].astype(np.int64)
        Cp = dom.C[idx_pts].astype(np.int64)
        out = np.empty((len(idx_pts), len(gates)), dtype=np.int8)
        # group by direction for speed
        cache = {}
        for col, j in enumerate(gates):
            key = (self.alpha[j].tobytes(), self.beta[j].tobytes())
            if key not in cache:
                cache[key] = Xp @ self.alpha[j] + Cp @ self.beta[j]
            out[:, col] = cache[key] >= self.theta[j]
        return out


def top_values(dom, pool, gates, v, mu, nu, t0, idx=None):
    if idx is None:
        idx = np.arange(dom.P)
    G = pool.columns(idx, gates).astype(np.float64)
    return G @ v + dom.X[idx].astype(np.float64) @ mu + dom.C[idx].astype(np.float64) @ nu - t0


def solve_lp(dom, pool, gates, weights=None, active=None, max_rounds=60, add_per_round=4000,
             seed=0, verbose=False, margin=1.0, free_cols=True, time_limit=None):
    """minimise sum_j w_j |v_j| subject to margin constraints on ALL points of dom,
    using constraint generation.  Returns (status, v, mu, nu, t0, active)."""
    rng = np.random.default_rng(seed)
    gates = list(gates)
    S = len(gates)
    if weights is None:
        weights = np.ones(S)
    if active is None:
        n0 = min(dom.P, 3000)
        active = np.sort(rng.choice(dom.P, n0, replace=False))
    active = np.unique(active)
    N, nc = dom.N, dom.nc
    t_start = time.time()
    for rnd in range(max_rounds):
        G = pool.columns(active, gates).astype(np.float64)
        Xa = dom.X[active].astype(np.float64)
        Ca = dom.C[active].astype(np.float64)
        sg = dom.sig[active].astype(np.float64)[:, None]
        # variables: vp (S), vm (S), mu (N), nu (nc), t0 (1)
        A = np.hstack([-sg * G, sg * G, -sg * Xa, -sg * Ca, sg])
        b = -margin * np.ones(len(active))
        c = np.concatenate([weights, weights, np.zeros(N + nc + 1)])
        bounds = [(0, None)] * (2 * S) + [(None, None)] * (N + nc + 1)
        opts = {'presolve': True}
        if time_limit:
            opts['time_limit'] = time_limit
        res = linprog(c, A_ub=sparse.csr_matrix(A), b_ub=b, bounds=bounds, method='highs', options=opts)
        if res.status != 0:
            return ('infeasible' if res.status == 2 else 'fail:%d' % res.status), None, None, None, None, active
        z = res.x
        v = z[:S] - z[S:2 * S]
        mu = z[2 * S:2 * S + N]
        nu = z[2 * S + N:2 * S + N + nc]
        t0 = z[-1]
        # check all points (chunked)
        viol_idx = []
        viol_amt = []
        for st in range(0, dom.P, 200000):
            idx = np.arange(st, min(dom.P, st + 200000))
            tv = top_values(dom, pool, gates, v, mu, nu, t0, idx)
            slack = dom.sig[idx] * tv
            bad = slack < margin - 1e-7
            viol_idx.append(idx[bad])
            viol_amt.append(slack[bad])
        viol_idx = np.concatenate(viol_idx)
        viol_amt = np.concatenate(viol_amt)
        if verbose:
            print(f'  round {rnd}: active={len(active)} obj={res.fun:.4f} violated={len(viol_idx)}', flush=True)
        if len(viol_idx) == 0:
            return 'ok', v, mu, nu, t0, active
        order = np.argsort(viol_amt)[:add_per_round]
        active = np.union1d(active, viol_idx[order])
        if time_limit and time.time() - t_start > time_limit:
            return 'timeout', None, None, None, None, active
    return 'maxrounds', None, None, None, None, active


def feasible(dom, pool, gates, active=None, seed=0):
    st, v, mu, nu, t0, act = solve_lp(dom, pool, gates, weights=np.zeros(len(list(gates))), active=active, seed=seed)
    return st == 'ok', (v, mu, nu, t0), act


def reweighted_l1(dom, pool, gates=None, iters=8, eps=1e-3, seed=0, verbose=False, active=None):
    if gates is None:
        gates = list(range(len(pool)))
    gates = list(gates)
    w = np.ones(len(gates))
    best = None
    for it in range(iters):
        st, v, mu, nu, t0, active = solve_lp(dom, pool, gates, weights=w, active=active, seed=seed)
        if st != 'ok':
            if verbose:
                print('  rw-L1 status', st)
            return best, active
        supp = np.abs(v) > 1e-6 * max(1.0, np.abs(v).max())
        nsup = int(supp.sum())
        if verbose:
            print(f'  rwL1 iter {it}: support={nsup}', flush=True)
        if best is None or nsup < len(best):
            best = [gates[j] for j in np.nonzero(supp)[0]]
        w = 1.0 / (np.abs(v) + eps * max(1.0, np.abs(v).max()))
    return best, active


def prune(dom, pool, support, active=None, verbose=False, order=None):
    """greedy removal of gates while feasibility (margin 1) holds."""
    support = list(support)
    if order is not None:
        support = [support[i] for i in order]
    i = 0
    while i < len(support):
        trial = support[:i] + support[i + 1:]
        ok, sol, active = feasible(dom, pool, trial, active=active)
        if ok:
            support = trial
            if verbose:
                print(f'  pruned -> {len(support)}', flush=True)
        else:
            i += 1
    return support, active


def solve_milp(dom, pool, gates, active, Mbig=50.0, time_limit=600, verbose=False, max_rounds=30,
               lb_count=0):
    """exact min #gates within 'gates' (big-M), with constraint generation on points."""
    gates = list(gates)
    S = len(gates)
    N, nc = dom.N, dom.nc
    active = np.unique(active)
    for rnd in range(max_rounds):
        G = pool.columns(active, gates).astype(np.float64)
        Xa = dom.X[active].astype(np.float64)
        Ca = dom.C[active].astype(np.float64)
        sg = dom.sig[active].astype(np.float64)[:, None]
        nv = S + N + nc + 1 + S         # v, mu, nu, t0, y
        A1 = np.hstack([sg * G, sg * Xa, sg * Ca, -sg, np.zeros((len(active), S))])
        cons = [LinearConstraint(sparse.csr_matrix(A1), lb=1.0, ub=np.inf)]
        I = sparse.identity(S, format='csr')
        Z = sparse.csr_matrix((S, N + nc + 1))
        # v - M y <= 0 ; -v - M y <= 0
        A2 = sparse.hstack([I, Z, -Mbig * I])
        A3 = sparse.hstack([-I, Z, -Mbig * I])
        cons.append(LinearConstraint(A2.tocsr(), lb=-np.inf, ub=0))
        cons.append(LinearConstraint(A3.tocsr(), lb=-np.inf, ub=0))
        if lb_count:
            row = np.concatenate([np.zeros(S + N + nc + 1), np.ones(S)])
            cons.append(LinearConstraint(row[None, :], lb=lb_count, ub=np.inf))
        c = np.concatenate([np.zeros(S + N + nc + 1), np.ones(S)])
        integrality = np.concatenate([np.zeros(S + N + nc + 1), np.ones(S)])
        lb = np.concatenate([-Mbig * np.ones(S), -1e4 * np.ones(N + nc + 1), np.zeros(S)])
        ub = np.concatenate([Mbig * np.ones(S), 1e4 * np.ones(N + nc + 1), np.ones(S)])
        res = milp(c, constraints=cons, integrality=integrality, bounds=Bounds(lb, ub),
                   options={'time_limit': time_limit, 'disp': verbose})
        if res.x is None:
            return 'nosol:%s' % res.message, None, active, None
        z = res.x
        v = z[:S]
        mu = z[S:S + N]
        nu = z[S + N:S + N + nc]
        t0 = z[S + N + nc]
        yv = z[-S:]
        supp = [gates[j] for j in range(S) if yv[j] > 0.5]
        # verify on all points with LP restricted to the support
        ok, sol, active2 = feasible(dom, pool, supp, active=active)
        if ok:
            return 'ok', supp, active2, getattr(res, 'mip_dual_bound', None)
        # add violated points: evaluate MILP solution
        tv = top_values(dom, pool, gates, v, mu, nu, t0)
        slack = dom.sig * tv
        bad = np.nonzero(slack < 1 - 1e-6)[0]
        if len(bad) == 0:
            bad = np.setdiff1d(active2, active)
        order = np.argsort(slack[bad])[:3000]
        active = np.union1d(active, bad[order])
        if verbose:
            print(f'  milp round {rnd}: support {len(supp)} not globally feasible; active={len(active)}')
    return 'maxrounds', None, active, None


def exact_certificate(dom, pool, gates, active=None, scale=10 ** 6):
    """Re-solve LP (margin 1) on the support, round top weights to integers/scale and verify in exact
    integer arithmetic on every point.  Returns (ok, (v_int, mu_int, nu_int, t0_int, scale), min_slack)."""
    ok, sol, active = feasible(dom, pool, gates, active=active)
    if not ok:
        return False, None, None
    v, mu, nu, t0 = sol
    vi = np.round(v * scale).astype(np.int64)
    mui = np.round(mu * scale).astype(np.int64)
    nui = np.round(nu * scale).astype(np.int64)
    t0i = int(np.round(t0 * scale))
    minslack = None
    for st in range(0, dom.P, 200000):
        idx = np.arange(st, min(dom.P, st + 200000))
        G = pool.columns(idx, gates).astype(np.int64)
        tv = G @ vi + dom.X[idx].astype(np.int64) @ mui + dom.C[idx].astype(np.int64) @ nui - t0i
        sl = (dom.sig[idx] * tv).min()
        minslack = sl if minslack is None else min(minslack, sl)
    return bool(minslack > 0), (vi, mui, nui, t0i, scale), int(minslack)
