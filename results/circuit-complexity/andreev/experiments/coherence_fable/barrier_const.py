# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Exact computation of the per-cube 'informative' probability of a one-table-bit +-1 gate
   g = [ sum_{i,l} eps_{i,l} a_{i,l} + x_d >= 1/2 ],  eps uniform in {+-1}^{km}.
Under a count restriction with cube c (K = sum_i c_i fixed ones), the restricted gate depends on x_d
iff F in [-P, Q], where F = sum of K independent random signs, P = number of live weights equal to +1,
Q = k - P.  (Proof in report, Thm 3.1.)
We compute  p(k,K) = E_P Pr[F in [-P,Q]]  exactly, its minimum over K <= k(m-1), and compare with
1/(2 sqrt(2 k m)) (the Prop. F constant) and with sqrt(k/m).
Also the cube-average  E_c p(k, sum c_i)  for c uniform in {0..m-1}^k, to get the constant in c*sqrt(k/m).
"""
import sys
sys.path.insert(0, '/tmp/andreev_gap/coherence_fable/pydeps_local'); sys.path.insert(1, '/tmp/pydeps')
from fractions import Fraction
from math import comb, sqrt
import numpy as np

def pF(K):
    # distribution of F = sum of K random signs: values -K..K step 2
    return {K - 2*t: Fraction(comb(K, t), 2**K) for t in range(K + 1)}

def p_inf(k, K):
    d = pF(K)
    tot = Fraction(0)
    for P in range(k + 1):
        Q = k - P
        pr = sum(v for f, v in d.items() if -P <= f <= Q)
        tot += Fraction(comb(k, P), 2**k) * pr
    return tot

def cube_average(k, m):
    # distribution of K = sum of k uniform {0..m-1}
    dist = {0: Fraction(1)}
    for _ in range(k):
        nd = {}
        for K, v in dist.items():
            for c in range(m):
                nd[K + c] = nd.get(K + c, 0) + v / m
        dist = nd
    return sum(v * p_inf(k, K) for K, v in dist.items())

print("k  m   min_K p(k,K)   1/(2sqrt(2km))  ratio   cube-avg p   cube-avg/sqrt(k/m)")
for k in [1, 2, 3, 4, 6, 8]:
    for m in [2, 4, 8, 16, 32, 64]:
        Kmax = k * (m - 1)
        pmin = min(p_inf(k, K) for K in range(Kmax + 1))
        bound = 1 / (2 * sqrt(2 * k * m))
        avg = cube_average(k, m)
        print(f"{k:2d} {m:3d}   {float(pmin):.5f}       {bound:.5f}      {float(pmin)/bound:6.3f}   {float(avg):.5f}     {float(avg)/sqrt(k/m):.4f}")
