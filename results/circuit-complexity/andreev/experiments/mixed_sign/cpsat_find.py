#!/usr/bin/env python3
"""SAT-side search with OR-tools CP-SAT and BOUNDED integer weights (a restriction: SAT gives a valid
circuit, UNSAT/UNKNOWN proves nothing about real weights).  Every model found is re-verified exactly.
Usage: python3 -I cpsat_find.py K M S TABLES W V TL WORKERS
  TABLES: 'all' or comma list closed automatically under c -> c xor e_i (as in andreev_min.py)
  W: bound on bottom weights (all coordinates), V: bound on top weights, TL: seconds
"""
import sys, os, itertools, time
sys.path.insert(0, '/tmp/pydeps'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortools.sat.python import cp_model
from fractions import Fraction as F
from mscore import andreev_points, andreev_blocks, eval_circuit, fmt_circ

k, m, S = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
tabsarg = sys.argv[4]; W = int(sys.argv[5]); V = int(sys.argv[6]); TL = float(sys.argv[7])
workers = int(sys.argv[8]) if len(sys.argv) > 8 else 4
N = 1 << k
tabs = None
if tabsarg != 'all':
    tabs = set(tuple(int(ch) for ch in t) for t in tabsarg.split(','))
    grow = True
    while grow:
        grow = False
        for t in list(tabs):
            for i in range(k):
                t2 = tuple(t[c ^ (1 << i)] for c in range(N))
                if t2 not in tabs: tabs.add(t2); grow = True
    tabs = sorted(tabs)
pts = andreev_points(k, m, tabs)
D = len(pts[0][0])
blocks = andreev_blocks(k, m)
md = cp_model.CpModel()
w = [[md.NewIntVar(-W, W, f'w{j}_{d}') for d in range(D)] for j in range(S)]
t = [md.NewIntVar(-D * W - 1, D * W + 1, f't{j}') for j in range(S)]
v = [md.NewIntVar(0, V, f'v{j}') for j in range(S)]         # WLOG v >= 0 (complement gates)
u = [md.NewIntVar(-V, V, f'u{d}') for d in range(D)]
tau = md.NewIntVar(-V * (S + D) - 1, V * (S + D) + 1, 'tau')
for j in range(S - 1): md.Add(v[j] <= v[j + 1])
for B in blocks:                                            # WLOG (single-bit flips, bit permutations)
    for d in B: md.Add(u[d] >= 0)
    for a, b in zip(B, B[1:]): md.Add(u[a] <= u[b])
for pi, (p, y) in enumerate(pts):
    zs = []
    for j in range(S):
        g = md.NewBoolVar(f'g{j}_{pi}')
        lin = sum(w[j][d] for d in range(D) if p[d])
        md.Add(lin >= t[j]).OnlyEnforceIf(g)
        md.Add(lin <= t[j] - 1).OnlyEnforceIf(g.Not())
        z = md.NewIntVar(0, V, f'z{j}_{pi}')
        md.Add(z == v[j]).OnlyEnforceIf(g)
        md.Add(z == 0).OnlyEnforceIf(g.Not())
        zs.append(z)
    top = sum(zs) + sum(u[d] for d in range(D) if p[d])
    if y: md.Add(top >= tau)
    else: md.Add(top <= tau - 1)
sol = cp_model.CpSolver()
sol.parameters.max_time_in_seconds = TL
sol.parameters.num_workers = workers
t0 = time.time(); st = sol.Solve(md); dt = time.time() - t0
name = sol.StatusName(st)
print(f'CPSAT k={k} m={m} S={S} tables={tabsarg} W={W} V={V}: {name} ({dt:.1f}s)', flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    circ = dict(bottom=[([F(sol.Value(w[j][d])) for d in range(D)], F(sol.Value(t[j]))) for j in range(S)],
                v=[F(sol.Value(x)) for x in v], u=[F(sol.Value(x)) for x in u], tau=F(sol.Value(tau)))
    bad = eval_circuit(circ, pts)
    print(f'  exact re-check on all {len(pts)} points: {"OK" if not bad else "FAILED %d" % len(bad)}', flush=True)
    names = [f'x{c}' for c in range(N)] + [f'a{i + 1}{l + 1}' for i in range(k) for l in range(m)]
    print(fmt_circ(circ, names), flush=True)
