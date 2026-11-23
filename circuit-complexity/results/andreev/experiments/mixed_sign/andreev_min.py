#!/usr/bin/env python3
"""Decide whether Andreev's function A_{k,m} (full model: every address bit is an input) has a depth-2
threshold circuit with S bottom gates of a given class.  Real weights, exact SMT (z3).

  python3 -I andreev_min.py K M S [--cls free|coherent|blocksym] [--tables all|xorpar]
                                  [--tl SEC] [--seed N] [--cegar INIT] [--intaddr W] [--show]

Symmetry breaking (all WLOG, see report.md):
  * 0 <= v_1 <= ... <= v_S (gate complement + permutation; every class here is closed under both)
  * free:      flipping one address bit a_{i,l} and permuting the table by c -> c xor e_i maps a
               circuit for A to a circuit for A and negates only u_{i,l}  =>  u_{i,l} >= 0;
               permuting bits inside a block  =>  u_{i,1} <= ... <= u_{i,m}.
  * coherent:  single-bit flips are NOT symmetries of the class; flipping a whole block is
               (s_i -> m - s_i, table permuted if m odd) => sum_l u_{i,l} >= 0; plus sorting inside blocks.
  * --tables xorpar restricts to the tables x_c = y xor parity(c), y in {0,1}: a sub-instance, so its
    UNSAT is a valid lower bound for A_{k,m}; it is equivalent to PARITY of km+1 bits.
UNSAT => no circuit with S gates of that class (hence none with fewer: pad with v_j = 0 gates).
"""
import sys, os, argparse, itertools
sys.path.insert(0, '/tmp/pydeps'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mscore import andreev_points, andreev_blocks, solve, solve_cegar, fmt_circ

ap = argparse.ArgumentParser()
ap.add_argument('k', type=int); ap.add_argument('m', type=int); ap.add_argument('S', type=int)
ap.add_argument('--cls', default='free')
ap.add_argument('--tables', default='all', help="all | xorpar | list of tables as bit strings x_0x_1.., comma separated (closed under c -> c xor e_i automatically)")
ap.add_argument('--tl', type=float, default=600)
ap.add_argument('--seed', type=int, default=None)
ap.add_argument('--cegar', type=int, default=0)
ap.add_argument('--intaddr', type=int, default=None, help='integer address weights in [-W,W] (restriction)')
ap.add_argument('--nosym', action='store_true')
ap.add_argument('--show', action='store_true')
ap.add_argument('--edgeclauses', action='store_true', help='redundant valid clauses (free class, u_addr>=0, v>=0): '
                'along an address edge where the output drops 1->0 some gate must turn off')
o = ap.parse_args()
k, m, S = o.k, o.m, o.S
N = 1 << k
tabs = None
if o.tables == 'xorpar':
    tabs = [tuple((y + bin(c).count('1')) % 2 for c in range(N)) for y in (0, 1)]
elif o.tables != 'all':
    tabs = set(tuple(int(ch) for ch in t) for t in o.tables.split(','))
    # close under the table permutations x -> (x_{c xor e_i})_c used by the single-bit-flip symmetry
    grow = True
    while grow:
        grow = False
        for t in list(tabs):
            for i in range(k):
                t2 = tuple(t[c ^ (1 << i)] for c in range(N))
                if t2 not in tabs: tabs.add(t2); grow = True
    tabs = sorted(tabs)
    print('sub-instance tables:', [''.join(map(str, t)) for t in tabs], flush=True)
pts = andreev_points(k, m, tabs)
blocks = andreev_blocks(k, m)
if o.cls == 'bsreduced':
    # block-symmetric model on reduced points (x, s_1..s_k), s_i in 0..m  (restriction: SAT => circuit)
    import itertools as _it
    tl_ = tabs if tabs is not None else list(_it.product((0, 1), repeat=N))
    pts = []
    for x in tl_:
        for s in _it.product(range(m + 1), repeat=k):
            b = sum(((s[i] % 2) << i) for i in range(k))
            pts.append((tuple(x) + tuple(s), x[b]))
    blocks = [[N + i] for i in range(k)]
opts = dict(vsym=not o.nosym, seed=o.seed)
usym = []
if not o.nosym:
    for B in blocks:
        for a, b in zip(B, B[1:]):
            usym.append(('le', a, b))
        if o.cls == 'free':
            for d in B:
                usym.append(('ge0', d))
if o.cls == 'coherent' and not o.nosym:
    import z3
    def blocksum(e, blocks=blocks):
        for B in blocks:
            e.so.add(z3.Sum([e.u[d] for d in B]) >= 0)
    opts['extra'] = [blocksum]
opts['usym'] = usym
if o.cls == 'bsreduced':
    # reflection s_i -> m - s_i (+ table xor e_i if m odd) negates u on s_i: WLOG u_{s_i} >= 0
    opts['usym'] = [('ge0', N + i) for i in range(k)]
if o.cls in ('coherent', 'blocksym'):
    opts.update(cls=o.cls, blocks=blocks)
if o.intaddr is not None:
    opts.update(intw=o.intaddr, intw_coords=[d for B in blocks for d in B])
if o.edgeclauses:
    assert o.cls == 'free' and not o.nosym
    import z3 as _z3
    def _edge(e, pts=pts, N=N, k=k, m=m):
        idx = {p: i for i, (p, _) in enumerate(pts)}
        cnt = 0
        for i, (p, yv) in enumerate(pts):
            if yv != 1: continue
            for d in range(N, N + k * m):
                if p[d] == 0:
                    q = list(p); q[d] = 1; q = tuple(q)
                    if pts[idx[q]][1] == 0:
                        e._edges.append((i, idx[q])); cnt += 1
        return cnt
    opts.setdefault('extra', []).append(lambda e: setattr(e, '_edges', []))
    _orig_solve = solve
    def solve(pts_, S_, opts_, timeout=600):
        import time as _t
        from mscore import Enc, eval_circuit
        t0 = _t.time(); e = Enc(pts_, S_, opts_)
        order = sorted(range(len(pts_)), key=lambda i: (sum(pts_[i][0]), pts_[i][0]))
        for i in order: e.add_point(i)
        n_e = _edge(e)
        for (i, i2) in e._edges:
            e.so.add(_z3.Or([_z3.And(e.g[(j, i)], _z3.Not(e.g[(j, i2)])) for j in range(S_)]))
        print(f'  (+{n_e} edge clauses)', flush=True)
        e.so.set('timeout', int(timeout * 1000)); r = e.so.check(); dt = _t.time() - t0
        if r == _z3.sat:
            c = e.circuit(e.so.model()); assert not eval_circuit(c, pts_); return 'SAT', c, dt
        return ('UNSAT' if r == _z3.unsat else 'UNKNOWN'), None, dt
if o.cegar:
    r, c, dt, info = solve_cegar(pts, S, opts, timeout=o.tl, init=o.cegar, seed=o.seed or 0)
else:
    r, c, dt = solve(pts, S, opts, timeout=o.tl)
    info = {}
tag = f'ANDREEV k={k} m={m} S={S} cls={o.cls} tables={o.tables} intaddr={o.intaddr} sym={not o.nosym}'
print(f'{tag}: {r} ({dt:.1f}s) {info}' + (f' verified exactly on all {len(pts)} points' if r == 'SAT' else ''), flush=True)
if r == 'UNSAT':
    print(f'  => every {o.cls} circuit for this instance needs >= {S + 1} bottom gates (proved)')
if c and o.show:
    names = [f'x{c_}' for c_ in range(N)] + [f'a{i + 1}{l + 1}' for i in range(k) for l in range(m)]
    print(fmt_circ(c, names))
