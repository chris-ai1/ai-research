#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""On the actual 5/16 circuit: per-gate split counts and splitting gates per cube.

A gate (tw, bc, th) with bc >= 0 sees block i through bc[i]*s_i. On cube c with table x
its form ranges over [tw.x + bc.c, tw.x + bc.c + sum(bc)], so it splits c iff
tw.x + bc.c < th <= tw.x + bc.c + sum(bc).
"""
import sys, random, bisect
sys.path.insert(0, '/tmp/andreev_gap/explainer_review')
from itertools import product
from math import log2
from build_circuit import build

def run(k, m, tables):
    c = build(k, m)
    forms = []
    for (tw, bc), ths in c['forms'].items():
        assert min(bc) >= 0
        forms.append((tw, bc, sorted(t for t, _ in ths)))
    cubes = list(product(range(m), repeat=k))
    S = len(c['gates']); bound = m ** k - (m - 1) ** k
    per_gate_max = 0
    sum_d = 0; min_avg = None
    per_cube_tot = [0] * len(cubes)
    for x in tables:
        gate_split = {}
        for fi, (tw, bc, ths) in enumerate(forms):
            tx = sum(a * b for a, b in zip(tw, x)); width = sum(bc)
            for ci, cu in enumerate(cubes):
                lo = tx + sum(a * b for a, b in zip(bc, cu))
                # thresholds th with lo < th <= lo + width
                i0 = bisect.bisect_right(ths, lo); i1 = bisect.bisect_right(ths, lo + width)
                per_cube_tot[ci] += i1 - i0
                for th in ths[i0:i1]:
                    gate_split[(fi, th)] = gate_split.get((fi, th), 0) + 1
        per_gate_max = max([per_gate_max] + list(gate_split.values()))
    T = len(tables)
    avgs = [t / T for t in per_cube_tot]
    N = c['N']
    D0 = max(0.0, N - k - 1 - log2(S + 1)) / (k + log2(S + 1))
    print(f'k={k} m={m} N={N} S={S}: max cubes split by one gate = {per_gate_max} (bound {bound}); '
          f'avg #splitting gates per cube: min {min(avgs):.2f}, mean {sum(avgs)/len(avgs):.2f}, max {max(avgs):.2f}; '
          f'kN/4 = {k*N/4:.1f}; D0 = {D0:.3f}; method ceiling m^k*mean/bound = {len(cubes)*sum(avgs)/len(avgs)/bound:.1f}',
          flush=True)
    return per_gate_max <= bound and min(avgs) >= D0

rng = random.Random(3)
res = []
res.append(run(3, 4, list(product((0, 1), repeat=8))))
res.append(run(4, 4, [tuple(rng.randrange(2) for _ in range(16)) for _ in range(100)]))
res.append(run(5, 6, [tuple(rng.randrange(2) for _ in range(32)) for _ in range(6)]))
print('PASS' if all(res) else 'FAIL', ' 5/16 circuit: every gate splits <= m^k-(m-1)^k cubes; E d_c >= D0')
