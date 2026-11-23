#!/usr/bin/env python3
"""Minimum number S of bottom gates of a depth-2 threshold circuit (real weights) computing
Andreev's function A(x,a) = x_b, b_i = (|a_i| mod 2), where the top gate reads the S bottom gates
AND the inputs directly.  Exact SMT (z3, QF_LRA) with optional symmetry breaking, CEGAR on the
point set, valid cuts and incremental search over S.  Every SAT circuit is re-checked with exact
rational arithmetic on ALL inputs; every UNSAT is a proof (all added constraints are valid,
see report.md).

Typical use
  # prove the exact minimum (or the best lower bound reachable in the time limit)
  python3 -I min_circuit.py blocksym 2,2 --tl 600
  # a single S: UNSAT proves min >= S+1 (feasibility is monotone in S: pad with v_j=0 gates, and
  # all symmetry breaking used here admits padded circuits), SAT proves min <= S.
  python3 -I min_circuit.py full 2,3 --only 3 --tl 3600 --portfolio 4
  # sequential scan S=start..upto (needed only for --nonred, which assumes S-1 infeasible)
  python3 -I min_circuit.py full 2,2 --upto 3 --tl 3600 --nonred 1

Output lines:  'S=<s>: UNSAT (proved) | SAT (verified exactly) | UNKNOWN', then a summary
  RESULT <mode> k= m=: minimum = S   or   lower bound >= L (proved), undecided at S

IMPORTANT semantics: blocksym is a RESTRICTION (each gate has equal weights inside a block).
blocksym SAT => full upper bound; blocksym UNSAT is NOT a lower bound for general circuits.
"""
import sys, os, time, argparse, itertools, random
sys.path.insert(0, '/tmp/pydeps')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import z3
from fractions import Fraction as F
from common import andreev_points, eval_circuit


# --------------------------------------------------------------------------- geometry helpers
def axis_squares(pts_index, D, maxstep):
    """(i1,i2,i3,i4) with p2=p1+e_a, p3=p1+e_b, p4=p1+e_a+e_b, all points present."""
    out = []
    for p, i1 in pts_index.items():
        for a in range(D):
            pa = list(p); pa[a] += 1; pa = tuple(pa)
            if pa not in pts_index: continue
            for b in range(a + 1, D):
                pb = list(p); pb[b] += 1; pb = tuple(pb)
                pab = list(pa); pab[b] += 1; pab = tuple(pab)
                if pb in pts_index and pab in pts_index:
                    out.append((i1, pts_index[pa], pts_index[pb], pts_index[pab]))
    return out


def axis_triples(pts_index, D):
    out = []
    for p, i1 in pts_index.items():
        for a in range(D):
            q = list(p); q[a] += 1; q = tuple(q)
            r = list(q); r[a] += 1; r = tuple(r)
            if q in pts_index and r in pts_index:
                out.append((i1, pts_index[q], pts_index[r]))
    return out


# --------------------------------------------------------------------------- encoder
class Enc:
    def __init__(self, pts, S, o):
        self.pts, self.S, self.o = pts, S, o
        self.D = D = len(pts[0][0])
        if o.tactic == 'qflra':
            self.so = z3.SolverFor('QF_LRA')
        elif o.tactic == 'default':
            self.so = z3.Solver()
        else:  # 'qflra-arith2' etc.
            self.so = z3.SolverFor('QF_LRA'); self.so.set('arith.solver', int(o.tactic[-1]))
        if o.seed is not None: self.so.set('random_seed', o.seed)
        self.al = [[z3.Real(f'a{j}_{d}') for d in range(D)] for j in range(S)]
        self.th = [z3.Real(f't{j}') for j in range(S)]
        self.v = [z3.Real(f'v{j}') for j in range(S)]
        self.u = [z3.Real(f'u{d}') for d in range(D)]
        self.tau = z3.Real('tau')
        self.g = {}            # (j, pidx) -> Bool
        self.added = []        # point indices in insertion order (= lex order)
        self.eq = [z3.BoolVal(True)] * max(S - 1, 0)   # running lex 'prefix equal' literal
        self.index = {p: i for i, (p, _) in enumerate(pts)}
        add = self.so.add
        if o.sym in ('comp', 'comp+lex', 'comp+vsort'):
            # complementing gate j (alpha,th,v)->(-alpha,1-th,-v), tau->tau-v keeps margins:
            # WLOG g_j(origin)=0  <=>  theta_j >= 1
            for j in range(S): add(self.th[j] >= 1)
        if o.sym in ('vpos', 'vpos+sort'):
            for j in range(S): add(self.v[j] >= 0)
        if o.sym in ('vpos+sort', 'comp+vsort'):
            for j in range(S - 1): add(self.v[j] <= self.v[j + 1])
        self._squares = self._triples = None
        if o.cuts:
            self._squares = axis_squares(self.index, D, 1)
            self._triples = axis_triples(self.index, D)

    def gv(self, j, i):
        return self.g[(j, i)]

    def add_point(self, i):
        p, out = self.pts[i]
        S, D, add = self.S, self.D, self.so.add
        terms = []
        for j in range(S):
            g = z3.Bool(f'g{j}_{i}'); self.g[(j, i)] = g
            lin = z3.Sum([self.al[j][d] * p[d] for d in range(D) if p[d]] + [z3.RealVal(0)])
            add(z3.Implies(g, lin >= self.th[j]), z3.Implies(z3.Not(g), lin <= self.th[j] - 1))
            terms.append(z3.If(g, self.v[j], z3.RealVal(0)))
        top = z3.Sum(terms + [self.u[d] * p[d] for d in range(D) if p[d]] + [z3.RealVal(0)])
        add(top >= self.tau if out else top <= self.tau - 1)
        self.added.append(i)
        if self.o.sym == 'comp+lex':
            # non-strict lex order of gate truth tables, points taken in insertion order
            for j in range(S - 1):
                a, b, e = self.g[(j, i)], self.g[(j + 1, i)], self.eq[j]
                add(z3.Implies(z3.And(e, a), b))
                ne = z3.Bool(f'eq{j}_{i}')
                add(z3.Implies(z3.And(e, a, b), ne), z3.Implies(z3.And(e, z3.Not(a), z3.Not(b)), ne))
                self.eq[j] = ne

    def add_cuts(self, newset):
        """valid cuts among currently added points that involve a newly added point"""
        if not self.o.cuts: return
        have = set(self.added); add = self.so.add; S = self.S
        f = lambda i: self.pts[i][1]
        for (i1, i2, i3, i4) in self._squares:
            if not ({i1, i2, i3, i4} <= have) or not ({i1, i2, i3, i4} & newset): continue
            G = lambda j, i: self.g[(j, i)]
            for j in range(S):    # a threshold gate never has the XOR pattern on a parallelogram
                add(z3.Or(z3.Not(G(j, i1)), z3.Not(G(j, i4)), G(j, i2), G(j, i3)))
                add(z3.Or(G(j, i1), G(j, i4), z3.Not(G(j, i2)), z3.Not(G(j, i3))))
            if f(i1) == f(i4) != f(i2) == f(i3):
                # top input part is affine => some bottom gate must be non-additive on the square
                nads = []
                for j in range(S):
                    nd = z3.Bool(f'nad{j}_{i1}_{i4}')
                    a, b, c, d = G(j, i1), G(j, i2), G(j, i3), G(j, i4)
                    for pat in itertools.product((0, 1), repeat=4):
                        if pat[0] + pat[3] == pat[1] + pat[2]:
                            lits = [x if not bit else z3.Not(x) for x, bit in zip((a, b, c, d), pat)]
                            add(z3.Or([z3.Not(nd)] + lits))
                    nads.append(nd)
                add(z3.Or(nads) if nads else z3.BoolVal(False))
        for (i1, i2, i3) in self._triples:
            if not ({i1, i2, i3} <= have) or not ({i1, i2, i3} & newset): continue
            for j in range(S):    # threshold gates are monotone along a line
                a, b, c = self.g[(j, i1)], self.g[(j, i2)], self.g[(j, i3)]
                add(z3.Or(z3.Not(a), b, z3.Not(c)), z3.Or(a, z3.Not(b), c))

    def add_nonred(self):
        """Only valid with ALL points added and when S-1 is already proved infeasible:
        a minimum circuit has no constant gate, no gate equal to an input bit or its negation
        (absorbed by the top gate's direct weights), no two gates equal or complementary
        (merged), and no gate with v_j = 0."""
        S, D, add = self.S, self.D, self.so.add
        allp = range(len(self.pts))
        G = lambda j: [self.g[(j, i)] for i in allp]
        for j in range(S):
            add(z3.Or(G(j)), z3.Or([z3.Not(x) for x in G(j)]))                     # non-constant
            for d in range(D):
                if all(p[d] in (0, 1) for p, _ in self.pts):
                    add(z3.Or([self.g[(j, i)] != bool(self.pts[i][0][d]) for i in allp]))
                    add(z3.Or([self.g[(j, i)] == bool(self.pts[i][0][d]) for i in allp]))
            add(self.v[j] != 0)
        for j in range(S):
            for jj in range(j + 1, S):
                add(z3.Or([self.g[(j, i)] != self.g[(jj, i)] for i in allp]))
                add(z3.Or([self.g[(j, i)] == self.g[(jj, i)] for i in allp]))

    def circuit(self, mdl):
        q = lambda x: mdl.eval(x, model_completion=True).as_fraction()
        return dict(bottom=[([q(a) for a in self.al[j]], q(self.th[j])) for j in range(self.S)],
                    v=[q(x) for x in self.v], u=[q(x) for x in self.u], tau=q(self.tau))


def symmetry_group(k, m, mode, pts, limit, rng):
    """Affine input maps sigma with A o sigma in {A, not A}, as index permutations perm[i]=idx(sigma(p_i)).
    Generators: table complement; block permutations (with table index permutation);
    full: bit permutations inside a block, flipping one bit of block i (+ table XOR e_i);
    blocksym: s_i -> m - s_i (+ table XOR e_i if m odd).  Closure is computed and every element is
    checked against the target."""
    N = 1 << k
    index = {p: i for i, (p, _) in enumerate(pts)}
    def table_xor(x, t): return tuple(x[c ^ t] for c in range(N))
    gens = []
    gens.append(lambda p: tuple(1 - c for c in p[:N]) + p[N:])
    for i in range(k - 1):           # swap blocks i,i+1 and the corresponding address bits
        def sw(p, i=i):
            x, a = p[:N], p[N:]
            def pc(c): # swap bits i,i+1 of c
                bi, bj = (c >> i) & 1, (c >> (i + 1)) & 1
                return c & ~((1 << i) | (1 << (i + 1))) | (bj << i) | (bi << (i + 1))
            x2 = [0] * N
            for c in range(N): x2[pc(c)] = x[c]
            w = m if mode == 'full' else 1
            bl = [a[j * w:(j + 1) * w] for j in range(k)]
            bl[i], bl[i + 1] = bl[i + 1], bl[i]
            return tuple(x2) + tuple(v for b in bl for v in b)
        gens.append(sw)
    for i in range(k):
        if mode == 'full':
            def fl(p, i=i):
                x, a = p[:N], list(p[N:]); a[i * m] = 1 - a[i * m]
                return table_xor(x, 1 << i) + tuple(a)
            gens.append(fl)
            if m >= 2:
                for r in (1,):
                    def tr(p, i=i):
                        x, a = p[:N], list(p[N:]); a[i * m], a[i * m + 1] = a[i * m + 1], a[i * m]
                        return x + tuple(a)
                    gens.append(tr)
                    def cyc(p, i=i):
                        x, a = p[:N], list(p[N:]); blk = a[i * m:(i + 1) * m]; a[i * m:(i + 1) * m] = blk[1:] + blk[:1]
                        return x + tuple(a)
                    gens.append(cyc)
        else:
            def rf(p, i=i):
                x, a = p[:N], list(p[N:]); a[i] = m - a[i]
                return (table_xor(x, 1 << i) if m % 2 else x) + tuple(a)
            gens.append(rf)
    gperms = [tuple(index[f(p)] for p, _ in pts) for f in gens]
    ident = tuple(range(len(pts)))
    group = {ident}; frontier = [ident]
    while frontier and len(group) < 10 ** 5:
        nf = []
        for h in frontier:
            for gp in gperms:
                c = tuple(gp[h[i]] for i in range(len(pts)))
                if c not in group: group.add(c); nf.append(c)
        frontier = nf
    for perm in group:   # sanity: A o sigma = A or = not A
        same = all(pts[perm[i]][1] == pts[i][1] for i in range(len(pts)))
        neg = all(pts[perm[i]][1] != pts[i][1] for i in range(len(pts)))
        assert same or neg
    group.discard(ident)
    group = sorted(group)
    if limit and len(group) > limit:
        group = rng.sample(group, limit)
    return group


def add_group_lex(e, order, group):
    """Gate 0 is the lex-smallest canonical gate; since the whole circuit may be replaced by
    C o sigma, WLOG g_0 <=_lex canon(g_0 o sigma) for every sigma (canon = complement so value at
    origin is 0).  Valid together with comp+lex (gate 0 = lex-min)."""
    g = lambda i: e.g[(0, i)]
    o0 = order[0]
    for gi, perm in enumerate(group):
        c = g(perm[o0])
        eq = z3.BoolVal(True)
        for t, i in enumerate(order):
            a = g(i); h = z3.Xor(g(perm[i]), c)
            e.so.add(z3.Implies(z3.And(eq, a), h))
            ne = z3.Bool(f'gl{gi}_{t}')
            e.so.add(z3.Implies(z3.And(eq, a == h), ne))
            eq = ne


def order_points(pts, how, rng):
    idx = list(range(len(pts)))
    origin = min(idx, key=lambda i: sum(pts[i][0]))
    if how == 'weight':
        idx.sort(key=lambda i: (sum(pts[i][0]), pts[i][0]))
    elif how == 'random':
        rng.shuffle(idx)
    idx.remove(origin)
    return [origin] + idx


def build_full(pts, S, o, rng):
    e = Enc(pts, S, o)
    order = order_points(pts, o.order, rng)
    for i in order: e.add_point(i)
    e.add_cuts(set(order))
    if o.nonred: e.add_nonred()
    if o.glex and S >= 1:
        add_group_lex(e, order, symmetry_group(o.k, o.m, o.mode, pts, o.glex, rng))
    return e, order


def _cube_worker(args):
    pts, S, o, deadline, cube = args
    e, order = build_full(pts, S, o, random.Random(o.seed or 0))
    for (j, i, val) in cube:
        e.so.add(e.g[(j, i)] if val else z3.Not(e.g[(j, i)]))
    t0 = time.time()
    r, circ = check(e, pts, deadline)
    return r, circ, cube, time.time() - t0


def solve_cubes(pts, S, o, deadline):
    """cube-and-conquer: split on L gate-output literals, 2^L independent sub-problems in parallel.
    UNSAT iff every cube is UNSAT (the cubes cover the whole space)."""
    import multiprocessing as mp
    rng = random.Random(o.seed or 0)
    order = order_points(pts, o.order, rng)
    n = len(order)
    lits = []
    t = 0
    while len(lits) < o.cube:      # spread points over the middle of the weight order, gates round-robin
        j = t % S
        i = order[(n // 3 + (t * 7919) % (n // 2)) % n]
        if (j, i) not in [(a, b) for a, b in lits]: lits.append((j, i))
        t += 1
    cubes = [[(j, i, v) for (j, i), v in zip(lits, vals)]
             for vals in itertools.product((0, 1), repeat=len(lits))]
    ctx = mp.get_context('fork')
    res = 'UNSAT'; found = None; times = []
    with ctx.Pool(o.jobs) as pool:
        for r, circ, cube, dt in pool.imap_unordered(_cube_worker, [(pts, S, o, deadline, c) for c in cubes]):
            times.append(round(dt, 1))
            if r == 'SAT':
                res, found = 'SAT', circ; pool.terminate(); break
            if r == 'UNKNOWN': res = 'UNKNOWN'
    return res, found, dict(cubes=len(cubes), cube_times_max=max(times) if times else None,
                            cube_times_sum=round(sum(times), 1))


def _portfolio_worker(args):
    pts, S, o, deadline, seed = args
    oo = argparse.Namespace(**vars(o)); oo.seed = seed; oo.portfolio = 0
    r = solve_S(pts, S, oo, deadline)
    return r[0], r[1], seed


def solve_portfolio(pts, S, o, deadline):
    """run o.portfolio copies with different random seeds; first decisive answer wins"""
    import multiprocessing as mp
    base = o.seed or 0
    res = ('UNKNOWN', None, {})
    with mp.get_context('fork').Pool(o.portfolio) as pool:
        for r, circ, seed in pool.imap_unordered(_portfolio_worker,
                                                 [(pts, S, o, deadline, base + 1 + t) for t in range(o.portfolio)]):
            if r in ('SAT', 'UNSAT'):
                res = (r, circ, dict(winning_seed=seed)); pool.terminate(); break
    return res


def solve_S(pts, S, o, deadline):
    if getattr(o, 'portfolio', 0) > 1:
        return solve_portfolio(pts, S, o, deadline)
    rng = random.Random(o.seed or 0)
    if not o.cegar and o.jobs > 1 and S >= 1 and o.cube > 0:
        return solve_cubes(pts, S, o, deadline)
    e = Enc(pts, S, o)
    order = order_points(pts, o.order, rng)
    if not o.cegar:
        for i in order: e.add_point(i)
        e.add_cuts(set(order))
        if o.nonred: e.add_nonred()
        if o.glex and S >= 1:
            add_group_lex(e, order, symmetry_group(o.k, o.m, o.mode, pts, o.glex, rng))
        return check(e, pts, deadline)
    # CEGAR: start with a small subset, add counterexample points (UNSAT on subset => UNSAT)
    start = order[:max(1, o.cegar)]
    for i in start: e.add_point(i)
    e.add_cuts(set(start))
    it = 0
    while True:
        it += 1
        r, circ = check(e, pts, deadline, verify=False)
        if r != 'SAT': return r, circ, dict(iters=it, pts=len(e.added))
        bad = [i for i in order if i not in set(e.added)
               and _wrong(circ, pts[i])]
        if not bad:
            return 'SAT', circ, dict(iters=it, pts=len(e.added))
        rng.shuffle(bad)
        new = bad[:o.batch]
        for i in new: e.add_point(i)
        e.add_cuts(set(new))


def _wrong(circ, pt):
    return bool(eval_circuit(circ, [pt]))


def check(e, pts, deadline, verify=True):
    rem = deadline - time.time()
    if rem <= 0: return 'UNKNOWN', None
    e.so.set('timeout', max(1, int(rem * 1000)))
    r = e.so.check()
    if r == z3.sat:
        circ = e.circuit(e.so.model())
        if verify:
            bad = eval_circuit(circ, pts)
            if bad: raise RuntimeError(f'model fails exact check on {len(bad)} points')
        return 'SAT', circ
    return ('UNSAT' if r == z3.unsat else 'UNKNOWN'), None


def fmt_circ(c):
    s = lambda x: str(x)
    lines = [f'    g{j}: [{" + ".join(f"{s(a)}*z{d}" for d, a in enumerate(al) if a)} >= {s(th)}]'
             for j, (al, th) in enumerate(c['bottom'])]
    top = ' + '.join([f'{s(v)}*g{j}' for j, v in enumerate(c['v']) if v] +
                     [f'{s(u)}*z{d}' for d, u in enumerate(c['u']) if u])
    lines.append(f'    top: [{top} >= {s(c["tau"])}]')
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('mode', choices=['full', 'thermo', 'blocksym'])
    ap.add_argument('inst', nargs='+', help='k,m pairs')
    ap.add_argument('--tl', type=float, default=600, help='time limit per S (seconds)')
    ap.add_argument('--total', type=float, default=None, help='overall time limit per instance')
    ap.add_argument('--start', type=int, default=0, help='first S (lower bound claims need start=0 '
                    'unless S<start were proved elsewhere)')
    ap.add_argument('--upto', type=int, default=None, help='stop after S=UPTO (lower-bound mode)')
    ap.add_argument('--only', type=int, default=None, help='test a single S: UNSAT => min >= S+1 (no nonredundancy cuts)')
    ap.add_argument('--sym', default='vpos+sort', choices=['none', 'comp', 'comp+lex', 'comp+vsort', 'vpos', 'vpos+sort'])
    ap.add_argument('--cuts', type=int, default=0, help='square/line cuts (1/0)')
    ap.add_argument('--nonred', type=int, default=0, help='nonredundancy cuts (needs sequential S)')
    ap.add_argument('--cegar', type=int, default=0, help='CEGAR: initial #points (0 = all points)')
    ap.add_argument('--batch', type=int, default=4, help='CEGAR: counterexamples added per round')
    ap.add_argument('--glex', type=int, default=0, help='lex-leader of gate 0 under the symmetry group of A '
                    '(max #group elements used; 0 = off; needs --sym comp+lex and --cegar 0)')
    ap.add_argument('--portfolio', type=int, default=0, help='run P differently-seeded solvers in parallel, '
                    'first decisive answer wins (recommended parallel mode)')
    ap.add_argument('--jobs', type=int, default=1, help='parallel processes for cube-and-conquer')
    ap.add_argument('--cube', type=int, default=0, help='#split literals (2^cube sub-problems); needs --jobs>1. '
                    'Measured: NOT effective here (each cube ~ as hard as the whole problem)')
    ap.add_argument('--order', default='weight', choices=['weight', 'random', 'natural'])
    ap.add_argument('--tactic', default='qflra-arith2', choices=['qflra', 'default', 'qflra-arith2', 'qflra-arith6'])
    ap.add_argument('--seed', type=int, default=None)
    ap.add_argument('--show', action='store_true', help='print the circuit found')
    o = ap.parse_args()
    if o.glex and o.mode == 'thermo':
        ap.error('--glex not implemented for thermo')
    if o.glex and (o.cegar or o.sym != 'comp+lex'):
        ap.error('--glex needs --sym comp+lex and --cegar 0')
    if o.nonred and o.cegar:
        ap.error('--nonred needs --cegar 0')
    for km in o.inst:
        k, m = map(int, km.split(','))
        o.k, o.m = k, m
        pts = andreev_points(k, m, o.mode)
        N = 1 << k
        Ss = [o.only] if o.only is not None else range(o.start, (o.upto if o.upto is not None else 10 ** 6) + 1)
        t_inst = time.time(); proved_lb = o.start if o.only is None else None; res = None
        for S in Ss:
            t0 = time.time()
            dl = t0 + o.tl
            if o.total: dl = min(dl, t_inst + o.total)
            oo = argparse.Namespace(**vars(o)); oo.nonred = o.nonred and o.only is None and S > 0
            out = solve_S(pts, S, oo, dl)
            r, circ = out[0], out[1]
            extra = f' {out[2]}' if len(out) > 2 else ''
            print(f'{o.mode} k={k} m={m} S={S}: {r}{" (proved)" if r == "UNSAT" else ""}'
                  f'{" (verified exactly on all %d inputs)" % len(pts) if r == "SAT" else ""}'
                  f' [{time.time() - t0:.1f}s]{extra}', flush=True)
            if r == 'SAT' and o.show: print(fmt_circ(circ), flush=True)
            if r == 'UNSAT':
                if proved_lb is not None: proved_lb = S + 1
                continue
            res = (r, S); break
        tag = f'RESULT {o.mode} k={k} m={m} n={N + k * m} points={len(pts)}:'
        if o.only is not None:
            print(f'{tag} S={o.only} -> {r}' + {'UNSAT': f'  => minimum >= {o.only + 1} (proved)',
                  'SAT': f'  => minimum <= {o.only}'}.get(r, ''), flush=True)
        elif res and res[0] == 'SAT':
            print(f'{tag} minimum = {res[1]}' + (' (proved, all smaller S UNSAT)' if o.start == 0 else
                                                f' given min >= {o.start}'), flush=True)
        else:
            print(f'{tag} lower bound >= {proved_lb} (proved)'
                  + (f', undecided at S={res[1]}' if res else ''), flush=True)
        if o.mode == 'blocksym':
            print('   note: blocksym is a restriction; its lower bounds do not transfer to general circuits',
                  flush=True)


if __name__ == '__main__':
    main()
