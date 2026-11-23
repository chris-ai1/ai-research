# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
# Preserved core encoder from ../mixed_sign/mscore.py.
"""Core encoder for depth-2 threshold circuits (top gate reads the S bottom gates AND the inputs).

Exact SMT over the reals (z3 QF_LRA) unless integer bottom weights are requested.
Every SAT model is re-verified with exact rational arithmetic on ALL points (eval_circuit).

Point sets (all exact):
  parity_points(M)            : all 2^M inputs, target = parity
  andreev_points(k, m)        : full model, table bits x_0..x_{N-1} then k blocks of m address bits
  andreev_points(k,m,tables)  : same, restricted to the given list of tables (a sub-instance:
                                UNSAT on a sub-instance is a valid lower bound for the full instance)

Gate classes (constraints on bottom weights; all are restrictions, so SAT => valid circuit of that class):
  free      : no constraint
  coherent  : for each gate j and address block B a Boolean e_{j,B}; e => all weights in B >= 0,
              not e => all weights in B <= 0  (solver chooses the sign pattern)
  pattern   : fixed sign per (gate, coordinate): +1 => >=0, -1 => <=0, 0 => ==0, None => free
"""
import sys, itertools, time
sys.path.insert(0, '/tmp/pydeps')
import z3
from fractions import Fraction as F


# ----------------------------------------------------------------------------- point sets
def parity_points(M):
    return [(p, sum(p) % 2) for p in itertools.product((0, 1), repeat=M)]


def andreev_points(k, m, tables=None):
    N = 1 << k
    pts = []
    tabs = list(itertools.product((0, 1), repeat=N)) if tables is None else [tuple(t) for t in tables]
    for x in tabs:
        for a in itertools.product((0, 1), repeat=k * m):
            b = 0
            for i in range(k):
                if sum(a[i * m:(i + 1) * m]) % 2:
                    b |= 1 << i
            pts.append((tuple(x) + tuple(a), x[b]))
    return pts


def andreev_blocks(k, m):
    N = 1 << k
    return [list(range(N + i * m, N + (i + 1) * m)) for i in range(k)]


# ----------------------------------------------------------------------------- exact check
def eval_circuit(circ, pts):
    bad = []
    for p, out in pts:
        g = [1 if sum(F(a) * c for a, c in zip(al, p)) >= F(th) else 0 for al, th in circ['bottom']]
        top = sum(F(vj) * gj for vj, gj in zip(circ['v'], g)) + sum(F(uj) * c for uj, c in zip(circ['u'], p))
        if (1 if top >= F(circ['tau']) else 0) != out:
            bad.append((p, out))
    return bad


def fmt_circ(c, names=None):
    D = len(c['u'])
    nm = names or [f'z{d}' for d in range(D)]
    s = lambda x: str(x)
    lines = [f'    g{j}: [{" + ".join(f"{s(a)}*{nm[d]}" for d, a in enumerate(al) if a)} >= {s(th)}]'
             for j, (al, th) in enumerate(c['bottom'])]
    top = ' + '.join([f'{s(v)}*g{j}' for j, v in enumerate(c['v']) if v] +
                     [f'{s(u)}*{nm[d]}' for d, u in enumerate(c['u']) if u])
    lines.append(f'    top: [{top} >= {s(c["tau"])}]')
    return '\n'.join(lines)


# ----------------------------------------------------------------------------- encoder
class Enc:
    """opts keys:
       cls: 'free' | 'coherent' | 'pattern'
       blocks: list of coordinate lists (address blocks) for 'coherent'
       pattern: list over gates of dict coord -> sign (+1/-1/0) for 'pattern'
       intw: None or W (integer bottom weights/thresholds in [-W,W] on ALL coordinates)
       intw_coords: if given, only these coordinates are integer-bounded (others real)
       vsym: True => v_j >= 0 and sorted (valid WLOG for any class closed under gate complement
             and gate permutation; all classes here are)
       usym: None | 'parity_even' | 'parity_odd' | list of (d1,d2) pairs meaning u_d1 <= u_d2
             | ('nonneg', coords)
       seed, timeout
    """

    def __init__(self, pts, S, opts):
        self.pts, self.S, self.o = pts, S, opts
        D = self.D = len(pts[0][0])
        o = opts
        if o.get('intw') is not None:
            self.so = z3.SolverFor('QF_LIRA') if o.get('logic') is None else z3.SolverFor(o['logic'])
        else:
            self.so = z3.SolverFor('QF_LRA')
            if o.get('arith2', True):
                self.so.set('arith.solver', 2)
        if o.get('seed') is not None:
            self.so.set('random_seed', o['seed'])
        add = self.so.add
        W = o.get('intw')
        ic = set(o.get('intw_coords', range(D))) if W is not None else set()
        self.al = [[(z3.Int(f'a{j}_{d}') if d in ic else z3.Real(f'a{j}_{d}')) for d in range(D)]
                   for j in range(S)]
        self.th = [(z3.Int(f't{j}') if W is not None and len(ic) == D else z3.Real(f't{j}')) for j in range(S)]
        self.v = [z3.Real(f'v{j}') for j in range(S)]
        self.u = [z3.Real(f'u{d}') for d in range(D)]
        self.tau = z3.Real('tau')
        if W is not None:
            for j in range(S):
                for d in ic:
                    add(self.al[j][d] >= -W, self.al[j][d] <= W)
        cls = o.get('cls', 'free')
        if cls == 'coherent':
            self.esign = {}
            for j in range(S):
                for bi, B in enumerate(o['blocks']):
                    e = z3.Bool(f'e{j}_{bi}')
                    self.esign[(j, bi)] = e
                    for d in B:
                        add(z3.Implies(e, self.al[j][d] >= 0), z3.Implies(z3.Not(e), self.al[j][d] <= 0))
            # symmetry: none on e here (complementing a gate negates all its weights, which flips
            # every block sign of that gate; vsym already uses the complement freedom)
        elif cls == 'pattern':
            for j in range(S):
                for d, sg in o['pattern'][j].items():
                    if sg == 1: add(self.al[j][d] >= 0)
                    elif sg == -1: add(self.al[j][d] <= 0)
                    elif sg == 0: add(self.al[j][d] == 0)
        elif cls == 'blocksym':
            for j in range(S):
                for B in o['blocks']:
                    for d in B[1:]:
                        add(self.al[j][d] == self.al[j][B[0]])
        if o.get('vsym', True):
            for j in range(S):
                add(self.v[j] >= 0)
            for j in range(S - 1):
                add(self.v[j] <= self.v[j + 1])
        us = o.get('usym')
        if us == 'parity_even':
            for d in range(D): add(self.u[d] >= 0)
            for d in range(D - 1): add(self.u[d] <= self.u[d + 1])
        elif us == 'parity_odd':
            for d in range(1, D): add(self.u[d] >= 0)
            for d in range(D - 1): add(self.u[d] <= self.u[d + 1])
        elif isinstance(us, list):
            for item in us:
                if item[0] == 'le':
                    add(self.u[item[1]] <= self.u[item[2]])
                elif item[0] == 'ge0':
                    add(self.u[item[1]] >= 0)
        for extra in o.get('extra', []):
            extra(self)
        self.g = {}

    def add_point(self, i):
        p, out = self.pts[i]
        S, D, add = self.S, self.D, self.so.add
        terms = []
        for j in range(S):
            g = z3.Bool(f'g{j}_{i}')
            self.g[(j, i)] = g
            lin = z3.Sum([self.al[j][d] * p[d] if p[d] != 1 else self.al[j][d] for d in range(D) if p[d]]
                         + [z3.RealVal(0)])
            add(z3.Implies(g, lin >= self.th[j]), z3.Implies(z3.Not(g), lin <= self.th[j] - 1))
            terms.append(z3.If(g, self.v[j], z3.RealVal(0)))
        top = z3.Sum(terms + [self.u[d] * p[d] if p[d] != 1 else self.u[d] for d in range(D) if p[d]]
                     + [z3.RealVal(0)])
        add(top >= self.tau if out else top <= self.tau - 1)

    def circuit(self, mdl):
        def q(x):
            val = mdl.eval(x, model_completion=True)
            if z3.is_int_value(val):
                return F(val.as_long())
            return val.as_fraction()
        return dict(bottom=[([q(a) for a in self.al[j]], q(self.th[j])) for j in range(self.S)],
                    v=[q(x) for x in self.v], u=[q(x) for x in self.u], tau=q(self.tau))


def solve(pts, S, opts, timeout=600, order=None, verify=True):
    """returns (status, circuit_or_None, seconds)"""
    t0 = time.time()
    e = Enc(pts, S, opts)
    idx = order if order is not None else sorted(range(len(pts)), key=lambda i: (sum(pts[i][0]), pts[i][0]))
    for i in idx:
        e.add_point(i)
    e.so.set('timeout', int(timeout * 1000))
    r = e.so.check()
    dt = time.time() - t0
    if r == z3.sat:
        c = e.circuit(e.so.model())
        if verify:
            bad = eval_circuit(c, pts)
            if bad:
                raise RuntimeError(f'model fails exact check on {len(bad)} points')
        return 'SAT', c, dt
    return ('UNSAT' if r == z3.unsat else 'UNKNOWN'), None, dt


def solve_cegar(pts, S, opts, timeout=600, init=64, batch=8, seed=0, verify=True):
    """CEGAR for the SAT side: solve on a subset, add violated points. UNSAT on a subset is a proof."""
    import random
    rng = random.Random(seed)
    t0 = time.time()
    e = Enc(pts, S, opts)
    order = list(range(len(pts)))
    rng.shuffle(order)
    used = set()
    for i in order[:init]:
        e.add_point(i); used.add(i)
    it = 0
    while True:
        it += 1
        rem = timeout - (time.time() - t0)
        if rem <= 0:
            return 'UNKNOWN', None, time.time() - t0, dict(iters=it, pts=len(used))
        e.so.set('timeout', int(rem * 1000))
        r = e.so.check()
        if r != z3.sat:
            return ('UNSAT' if r == z3.unsat else 'UNKNOWN'), None, time.time() - t0, dict(iters=it, pts=len(used))
        c = e.circuit(e.so.model())
        bad_idx = [i for i in order if i not in used and eval_circuit(c, [pts[i]])]
        if not bad_idx:
            if verify:
                assert not eval_circuit(c, pts)
            return 'SAT', c, time.time() - t0, dict(iters=it, pts=len(used))
        rng.shuffle(bad_idx)
        for i in bad_idx[:batch]:
            e.add_point(i); used.add(i)
