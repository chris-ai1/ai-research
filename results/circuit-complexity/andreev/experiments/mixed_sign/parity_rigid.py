#!/usr/bin/env python3
"""Rigidity test: is there a depth-2 parity circuit with S = floor(M/2) gates (normalised: v >= 0 sorted,
u >= 0 sorted [M even] / u_2..u_M >= 0 [M odd]) in which SOME gate has mixed signs, i.e. a weight >= 1 and
a weight <= -1?  (With margin-1 gate normalisation a variable that ever flips the gate along an edge has
|weight| >= 1, so 'mixed' here = has relevant variables of both signs.)
UNSAT => every minimum circuit is globally orientable (flip inputs => all gates monotone or antimonotone).
Usage: python3 -I parity_rigid.py M [S] [timeout]"""
import sys, os
sys.path.insert(0, '/tmp/pydeps'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import z3
from mscore import parity_points, solve, fmt_circ
M = int(sys.argv[1]); S = int(sys.argv[2]) if len(sys.argv) > 2 else M // 2
tl = float(sys.argv[3]) if len(sys.argv) > 3 else 3600
def mixed(e):
    e.so.add(z3.Or([z3.And(z3.Or([e.al[j][d] >= 1 for d in range(M)]), z3.Or([e.al[j][d] <= -1 for d in range(M)]))
                    for j in range(S)]))
opts = dict(vsym=True, usym='parity_even' if M % 2 == 0 else 'parity_odd', extra=[mixed])
r, c, dt = solve(parity_points(M), S, opts, timeout=tl)
print(f'PARITY-RIGID M={M} S={S} (some gate mixed): {r} ({dt:.1f}s)', flush=True)
if c: print(fmt_circ(c))
