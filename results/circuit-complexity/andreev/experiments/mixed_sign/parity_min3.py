#!/usr/bin/env python3
"""parity_min.py + redundant valid clauses: with v >= 0 and u_d >= 0 (WLOG, see report), along an edge
(x, x+e_d) with |x| odd, F must drop by >= 1 while u_d >= 0, so some gate j must turn OFF:
   OR_j ( g_j(x) AND NOT g_j(x+e_d) ).        (for M odd only directions d with u_d >= 0 forced, d >= 2)
Usage: python3 -I parity_min2.py M S [timeout] [seed]"""
import sys, os, itertools
sys.path.insert(0, '/tmp/pydeps'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import z3, time
from mscore import parity_points, Enc, eval_circuit, fmt_circ
M, S = int(sys.argv[1]), int(sys.argv[2])
tl = float(sys.argv[3]) if len(sys.argv) > 3 else 3600
seed = int(sys.argv[4]) if len(sys.argv) > 4 else None
pts = parity_points(M)
opts = dict(vsym=True, usym='parity_even' if M % 2 == 0 else 'parity_odd', seed=seed)
t0 = time.time()
e = Enc(pts, S, opts)
order = sorted(range(len(pts)), key=lambda i: (sum(pts[i][0]), pts[i][0]))
for i in order: e.add_point(i)
idx = {p: i for i, (p, _) in enumerate(pts)}
dirs = range(M) if M % 2 == 0 else range(1, M)
ncl = 0
for p, _ in pts:
    if sum(p) % 2 == 1:
        for d in dirs:
            if p[d] == 0:
                q = list(p); q[d] = 1; q = tuple(q)
                i, i2 = idx[p], idx[q]
                e.so.add(z3.Or([z3.And(e.g[(j, i)], z3.Not(e.g[(j, i2)])) for j in range(S)])); ncl += 1
# extra WLOG symmetry breaking (see report 1.3): equal v => thresholds sorted; equal u => gate-0 weights sorted
for j in range(S - 1):
    e.so.add(z3.Implies(e.v[j] == e.v[j + 1], e.th[j] <= e.th[j + 1]))
for d in range(M - 1):
    e.so.add(z3.Implies(e.u[d] == e.u[d + 1], e.al[0][d] <= e.al[0][d + 1]))
e.so.set("timeout", int(tl * 1000))
r = e.so.check(); dt = time.time() - t0
res = 'SAT' if r == z3.sat else ('UNSAT' if r == z3.unsat else 'UNKNOWN')
print(f'PARITY3 M={M} S={S} (+{ncl} edge clauses): {res} ({dt:.1f}s)', flush=True)
if r == z3.sat:
    c = e.circuit(e.so.model()); assert not eval_circuit(c, pts); print(fmt_circ(c))
