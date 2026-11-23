# Copyright (c) 2026 Christian Reitwiessner. All rights reserved.
# Authors: Christian Reitwiessner
"""Small-library stress test: local rectangles versus global top feasibility."""
import sys
sys.path.insert(0, '/tmp/andreev_gap/coherence_fable/pydeps_local')
import numpy as np
from scipy.optimize import linprog
from itertools import product
from fractions import Fraction
import json
from pathlib import Path

k, m, N = 2, 2, 4
xs = np.array(list(product((0, 1), repeat=N)), dtype=int)
as_ = np.array(list(product((0, 1), repeat=k*m)), dtype=int)
bs = np.array([sum((sum(a[i*m:(i+1)*m]) % 2) << i for i in range(k)) for a in as_])
inputs = np.array([list(x)+list(a) for x in xs for a in as_], dtype=int)
y = np.array([2*x[b]-1 for x in xs for b in bs], dtype=int)
rng = np.random.default_rng(561831)
results = []
saved = None
for S in (16, 32, 64, 96, 128):
    weights = rng.choice((-1, 1), size=(S, N+k*m))
    offsets = rng.integers(-3, 4, size=S)
    # Center Boolean inputs so odd thresholds are tie-free for n=8.
    thresholds = 2*offsets+1
    G = ((2*inputs-1) @ weights.T >= thresholds).astype(int)
    lib = G.reshape((len(xs), len(as_), S))
    rectangles = 0
    for p in range(len(xs)):
        for q in range(p):
            delta = xs[p, bs]-xs[q, bs]
            pos = {tuple(z) for z in (lib[p]-lib[q])[delta > 0]}
            neg = {tuple(z) for z in (lib[p]-lib[q])[delta < 0]}
            rectangles += len(pos & neg)
    phi = np.column_stack((np.ones(len(inputs), dtype=int), inputs, G))
    B = y[:, None]*phi
    primal = linprog(np.zeros(phi.shape[1]), A_ub=-B, b_ub=-np.ones(len(inputs)), bounds=[(None, None)]*phi.shape[1], method='highs')
    row = {"S": S, "four_point_rectangles": rectangles, "primal_status": primal.status}
    if primal.status == 2:
        dual = linprog(np.zeros(len(inputs)), A_eq=np.vstack((B.T, np.ones(len(inputs)))), b_eq=np.r_[np.zeros(phi.shape[1]), 1], bounds=(0, None), method='highs')
        assert dual.status == 0
        support = np.flatnonzero(dual.x > 1e-8)
        mu = [Fraction(float(dual.x[i])).limit_denominator(10**7) for i in support]
        exact = sum(mu) == 1 and all(sum(mu[t]*int(B[i,j]) for t,i in enumerate(support)) == 0 for j in range(B.shape[1]))
        row.update({"dual_support": len(support), "rational_certificate_exact": exact})
        if rectangles == 0 and saved is None:
            saved = {"authors": "Christian Reitwiessner", "k": k, "m": m, "weights_signed_inputs": weights.tolist(), "thresholds": thresholds.tolist(), "support_input_indices": support.tolist(), "mu_float": dual.x[support].tolist(), "mu_candidate_rational": [str(v) for v in mu], "certificate_exact": exact}
            # If recovery is not exact, retain only as numerical candidate.
    results.append(row)
output = {"authors": "Christian Reitwiessner", "seed": 561831, "k": k, "m": m, "results": results}
print(json.dumps(output, indent=2))
Path(__file__).with_name('dual_probe.json').write_text(json.dumps(output, indent=2)+'\n')
if saved is not None:
    Path(__file__).with_name('dual_candidate.json').write_text(json.dumps(saved, indent=2)+'\n')
