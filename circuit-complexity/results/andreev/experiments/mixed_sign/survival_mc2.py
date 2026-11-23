#!/usr/bin/env python3
"""Monte Carlo of p(g) = Pr_{sigma,c,x}[g splits the cube] under the randomised count restriction,
maximised over the gate threshold, for adversarial weight profiles.  Lemma B3' predicts
p(g) <= k/m + C k^{3/2}/sqrt(m) for EVERY gate; the old Lemma B3 gave O(k m^{-1/3}).
Reports p*sqrt(m)/k^{1.5} (should stay bounded as m grows).
Sampling uses the equivalent form: live bit uniform; q ~ U[0,1]; other bits Bernoulli(q).
"""
import sys
sys.path.insert(0, '/tmp/pydeps')
import numpy as np


def profile(name, m, rng):
    if name == 'pm1_balanced':
        w = np.array([1.0] * (m // 2) + [-1.0] * (m - m // 2))
    elif name == 'geometric':
        w = 2.0 ** np.arange(m) * rng.choice([-1, 1], m)
    elif name == 'geometric_pos':
        w = 2.0 ** np.arange(m)
    elif name == 'gauss':
        w = rng.normal(0, 1, m)
    elif name == 'one_huge':
        w = rng.choice([-1, 1], m) * 1.0; w[0] = 50.0 * m
    elif name == 'cauchy':
        w = rng.standard_cauchy(m)
    elif name == 'sqrt_heavy':   # sqrt(m) heavy weights, rest +-1
        w = rng.choice([-1.0, 1.0], m); h = max(1, int(np.sqrt(m))); w[:h] *= 30 * np.sqrt(m)
    return w


def p_split(W, k, m, rng, samples=40000, nth=41):
    # W: k x m weights.  sample restriction
    live = rng.integers(0, m, size=(samples, k))
    q = rng.random((samples, k))
    bits = (rng.random((samples, k, m)) < q[:, :, None]).astype(float)
    idx = np.arange(samples)[:, None]
    lam = W[np.arange(k)[None, :], live]                        # samples x k
    phi = (bits * W[None, :, :]).sum(2) - bits[idx, np.arange(k)[None, :], live] * lam
    Phi = phi.sum(1)
    lo = Phi + np.minimum(lam, 0).sum(1)
    hi = Phi + np.maximum(lam, 0).sum(1)
    # table part: random +-1 table weights on N bits shift threshold; fold into a random shift
    shift = rng.normal(0, 0.0, samples)
    best = 0.0
    qs = np.quantile(np.concatenate([lo, hi]), np.linspace(0.02, 0.98, nth))
    for th in qs:
        best = max(best, np.mean((lo < th + shift) & (th + shift <= hi)))
    return best


def main():
    rng = np.random.default_rng(1)
    names = ['pm1_balanced', 'geometric', 'geometric_pos', 'gauss', 'one_huge', 'cauchy', 'sqrt_heavy']
    print('k   m   ' + '  '.join(f'{n:>14s}' for n in names) + '   [entries: p, and p*sqrt(m)/k^1.5 in brackets]')
    for k in (2, 3, 4):
        for m in (16, 64, 256):
            row = []
            for nm in names:
                W = np.array([profile(nm, m, rng) for _ in range(k)])
                p = p_split(W, k, m, rng, samples=20000 if m == 256 else 40000)
                row.append(f'{p:.3f}[{p * np.sqrt(m) / k ** 1.5:.2f}]')
            print(f'{k}  {m:3d}  ' + '  '.join(f'{r:>14s}' for r in row), flush=True)


if __name__ == '__main__':
    main()
