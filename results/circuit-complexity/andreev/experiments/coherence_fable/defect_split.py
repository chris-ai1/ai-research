# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Split fraction under the randomised count restriction (random arrangement, random cube) for
three gate families as m grows, k fixed:
  coherent      : all address weights +1
  defect(r)     : coherent with r random positions per block flipped to -1  (r = ceil(sqrt(m)))
  balanced +-1  : uniform random signs
Threshold at the median of F over the grid (worst case for coherent is a boundary threshold, but
the median is the natural 'useful' choice and is what the barrier gates use).
A gate splits cube c iff  min_z F(c+z) < theta <= max_z F(c+z).  Exact over all cubes, averaged over
random arrangements and random gates.  Expect: coherent ~ k/m (times a constant <1 at the median),
defect(sqrt m) ~ C/sqrt(m), balanced ~ c*sqrt(k/m).
"""
import sys
sys.path.insert(0, '/tmp/andreev_gap/coherence_fable/pydeps_local'); sys.path.insert(1, '/tmp/pydeps')
import numpy as np
from math import ceil, sqrt

def split_fraction(W, perms, theta=None):
    k, m = W.shape
    P = np.zeros((k, m + 1));
    for i in range(k): P[i, 1:] = np.cumsum(W[i, perms[i]])
    shape = (m,) * k
    F = np.zeros(shape); lo = np.zeros(shape); hi = np.zeros(shape)
    for i in range(k):
        b = [1] * k; b[i] = m
        F = F + P[i, :m].reshape(b)
        live = W[i, perms[i][:m]].reshape(b)
        lo = lo + np.minimum(live, 0); hi = hi + np.maximum(live, 0)
    if theta is None:
        theta = np.median(F) + 0.5   # half-integer threshold near the median
    return np.mean((F + lo < theta) & (theta <= F + hi))

def gate(kind, k, m, rng):
    if kind == 'coherent': return np.ones((k, m))
    if kind == 'balanced': return rng.choice([-1., 1.], size=(k, m))
    if kind.startswith('defect'):
        r = ceil(sqrt(m)); W = np.ones((k, m))
        for i in range(k):
            W[i, rng.choice(m, r, replace=False)] = -1
        return W
    raise ValueError

if __name__ == '__main__':
    k = int(sys.argv[1]); trials = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    rng = np.random.default_rng(1)
    print(f"k={k}; columns: m, coherent, k/m, defect(sqrt m), 1/sqrt(m), balanced, sqrt(k/m)  [split fractions, mean over {trials} (gate, arrangement) draws]")
    for m in [4, 8, 16, 32, 64, 128, 256]:
        if m**k > 3e7: break
        res = {}
        for kind in ['coherent', 'defect', 'balanced']:
            vals = [split_fraction(gate(kind, k, m, rng), [rng.permutation(m) for _ in range(k)]) for _ in range(trials)]
            res[kind] = (np.mean(vals), np.std(vals) / sqrt(trials))
        print(f"m={m:4d}  coh={res['coherent'][0]:.4f}±{res['coherent'][1]:.4f} (k/m={k/m:.4f})  "
              f"def={res['defect'][0]:.4f}±{res['defect'][1]:.4f} (1/sqrt m={1/sqrt(m):.4f})  "
              f"bal={res['balanced'][0]:.4f}±{res['balanced'][1]:.4f} (sqrt(k/m)={sqrt(k/m):.4f})", flush=True)
