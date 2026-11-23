#!/usr/bin/env python3
"""Cross-check of parity_min.py with weaker symmetry breaking: mode 'v' (only v sorted >= 0), 'none'."""
import sys, os
sys.path.insert(0, '/tmp/pydeps'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mscore import parity_points, solve
M, S, mode = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
tl = float(sys.argv[4]) if len(sys.argv) > 4 else 3600
pts = parity_points(M)
opts = dict(vsym=(mode == 'v'), usym=None)
r, c, dt = solve(pts, S, opts, timeout=tl)
print(f'PARITY-crosscheck M={M} S={S} sym={mode}: {r} ({dt:.1f}s)', flush=True)
