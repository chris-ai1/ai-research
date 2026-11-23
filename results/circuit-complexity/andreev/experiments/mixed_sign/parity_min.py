#!/usr/bin/env python3
"""Exact minimum number of bottom gates of a depth-2 threshold circuit (real weights, top reads inputs)
computing PARITY of M bits.  Valid WLOG symmetry breaking (proof in report.md, section 'parity'):
  * gate complement + gate permutation:  0 <= v_1 <= ... <= v_S
  * input permutation + flips (each flip composed with output negation flips the signs of all
    OTHER direct weights):  M even: 0 <= u_1 <= ... <= u_M ;  M odd: u_1 <= u_2, 0 <= u_2 <= ... <= u_M
Usage: python3 -I parity_min.py M S [timeout] [cls] [seed]
   cls: free | coherent (all M bits one block) | intW (integer bottom weights in [-W,W])
"""
import sys, os
sys.path.insert(0, '/tmp/pydeps'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mscore import parity_points, solve, fmt_circ

M, S = int(sys.argv[1]), int(sys.argv[2])
tl = float(sys.argv[3]) if len(sys.argv) > 3 else 600
cls = sys.argv[4] if len(sys.argv) > 4 else 'free'
seed = int(sys.argv[5]) if len(sys.argv) > 5 else None
pts = parity_points(M)
opts = dict(vsym=True, usym='parity_even' if M % 2 == 0 else 'parity_odd', seed=seed)
if cls == 'coherent':
    opts.update(cls='coherent', blocks=[list(range(M))])
elif cls.startswith('int'):
    opts.update(intw=int(cls[3:]))
r, c, dt = solve(pts, S, opts, timeout=tl)
print(f'PARITY M={M} S={S} cls={cls}: {r} ({dt:.1f}s)' + (' verified exactly on all inputs' if r == 'SAT' else ''), flush=True)
if c: print(fmt_circ(c))
