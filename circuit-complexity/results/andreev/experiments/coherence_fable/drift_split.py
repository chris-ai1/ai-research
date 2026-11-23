# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Numerical check of the Drift Lemma (report Lemma 4.1).
Gate family drift(delta): in every block, (1+delta)m/2 weights are +1 and (1-delta)m/2 are -1
(positions random), so the relative drift is |sum|/(m*max) = delta.  Threshold at the median of F.
Split fraction under random arrangement + uniform cube (exact over cubes, MC over gates/arrangements).
Compare with k/(delta*m) (drift lemma scale) and sqrt(k/m) (balanced scale).
"""
import sys
sys.path.insert(0, '/tmp/andreev_gap/coherence_fable/pydeps_local'); sys.path.insert(1, '/tmp/pydeps'); sys.path.insert(2, '/tmp/andreev_gap/coherence_fable')
import numpy as np
from math import sqrt
from defect_split import split_fraction

def drift_gate(k, m, delta, rng):
    W = np.ones((k, m))
    r = int(round((1 - delta) * m / 2))
    for i in range(k):
        W[i, rng.choice(m, r, replace=False)] = -1
    return W

if __name__ == '__main__':
    k = int(sys.argv[1]); trials = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    rng = np.random.default_rng(7)
    deltas = [1.0, 0.5, 0.25, 0.125, 0.0625]
    print(f"k={k}: split fraction of drift(delta) gates; columns delta -> frac (frac*m/k) ; last column balanced delta~0: frac/sqrt(k/m)")
    for m in [16, 32, 64, 128, 256, 512]:
        if m**k > 3e7: break
        row = []
        for d in deltas:
            vals = [split_fraction(drift_gate(k, m, d, rng), [rng.permutation(m) for _ in range(k)]) for _ in range(trials)]
            f = np.mean(vals); row.append(f"d={d:<6g}: {f:.4f} (x m/k={f*m/k:5.2f})")
        vals = [split_fraction(drift_gate(k, m, 0.0, rng), [rng.permutation(m) for _ in range(k)]) for _ in range(trials)]
        f0 = np.mean(vals)
        print(f"m={m:4d} | " + " | ".join(row) + f" | d=0: {f0:.4f} (/sqrt(k/m)={f0/sqrt(k/m):.3f})", flush=True)
