#!/usr/bin/env python3
"""Minimum number of hyperplanes that cut every edge of E_1 = {(x, x+e_d): x_d = 0, |x| odd} of the
M-cube ('half-slicing').  Necessary condition for a depth-2 parity circuit with u >= 0 (WLOG for M even):
at an odd->even step no gate switching means F changes by u_d >= 0, which cannot make F negative.
With --oriented, the cutting gate must go 1 -> 0 along the edge (stronger necessary condition when
all top weights v_j >= 0).
Usage: python3 -I halfslice.py M S [--oriented] [--tl SEC]
"""
import sys, os, itertools, time
sys.path.insert(0, '/tmp/pydeps')
import z3
M, S = int(sys.argv[1]), int(sys.argv[2])
oriented = '--oriented' in sys.argv
tl = float(sys.argv[sys.argv.index('--tl') + 1]) if '--tl' in sys.argv else 600
pts = list(itertools.product((0, 1), repeat=M))
idx = {p: i for i, p in enumerate(pts)}
so = z3.SolverFor('QF_LRA'); so.set('arith.solver', 2)
al = [[z3.Real(f'a{j}_{d}') for d in range(M)] for j in range(S)]
th = [z3.Real(f't{j}') for j in range(S)]
g = [[z3.Bool(f'g{j}_{i}') for i in range(len(pts))] for j in range(S)]
for j in range(S):
    for i, p in enumerate(pts):
        lin = z3.Sum([al[j][d] for d in range(M) if p[d]] + [z3.RealVal(0)])
        so.add(z3.Implies(g[j][i], lin >= th[j]), z3.Implies(z3.Not(g[j][i]), lin <= th[j] - 1))
nE = 0
for p in pts:
    if sum(p) % 2 == 1:
        for d in range(M):
            if p[d] == 0:
                q = list(p); q[d] = 1; q = tuple(q)
                i, i2 = idx[p], idx[q]
                nE += 1
                if oriented:
                    so.add(z3.Or([z3.And(g[j][i], z3.Not(g[j][i2])) for j in range(S)]))
                else:
                    so.add(z3.Or([g[j][i] != g[j][i2] for j in range(S)]))
# symmetry: permuting coordinates is a symmetry of E_1; break lightly on gate 0's weights
for d in range(M - 1):
    so.add(al[0][d] <= al[0][d + 1])
so.set('timeout', int(tl * 1000))
t0 = time.time(); r = so.check()
print(f'HALFSLICE M={M} S={S} oriented={oriented} |E1|={nE}: {r} ({time.time() - t0:.1f}s)', flush=True)
if r == z3.sat:
    mdl = so.model()
    for j in range(S):
        print('  ', [mdl.eval(al[j][d]).as_fraction() for d in range(M)], '>=', mdl.eval(th[j]).as_fraction())
