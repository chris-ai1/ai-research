"""Referee check of Proposition F (§5), exact arithmetic.
For a restriction rho with K fixed ones (K <= k(m-1)) and one live bit per block, eps uniform in {+-1}^{km}:
  F = sum of K independent signs, P = #(+1 live weights) ~ Bin(k,1/2), Q=k-P,
  g_eps|rho non-constant  <=>  1-P <= F <= Q.
Exact probability p(K,k) = sum_P Bin(k,P)/2^k * Pr[1-P <= F <= k-P].   Claim: p(K,k) >= 1/(2 sqrt(2km)) for all K<=k(m-1).
Since the claim holds for EVERY rho, it holds for every distribution D.  Also checks the inequality
  C(K,floor(K/2)) 2^-K >= (2K+2)^(-1/2) used in the proof."""
import math
from fractions import Fraction
from math import comb, lgamma, log, exp, sqrt

def central(K):  # C(K, floor(K/2)) / 2^K, via logs for large K
    if K < 2000: return comb(K, K // 2) / 2 ** K
    return exp(lgamma(K + 1) - lgamma(K // 2 + 1) - lgamma(K - K // 2 + 1) - K * log(2))

bad = 0; worst = 9
for K in range(0, 2_000_001):
    r = central(K) * sqrt(2 * K + 2)
    if r < worst: worst, wK = r, K
    if r < 1 - 1e-12: bad += 1
print(f'binomial inequality C(K,K/2)2^-K >= (2K+2)^-1/2 for K<=2e6: violations={bad}, min ratio={worst:.6f} at K={wK}  (limit sqrt(4/pi)={sqrt(4/math.pi):.4f})')

def pF_interval(K, lo, hi):
    # Pr[lo <= F <= hi], F = 2*Bin(K,1/2) - K  (exact rational)
    tot = 0
    for j in range(K + 1):
        f = 2 * j - K
        if lo <= f <= hi: tot += comb(K, j)
    return Fraction(tot, 2 ** K)

def p_exact(K, k):
    return sum(Fraction(comb(k, P), 2 ** k) * pF_interval(K, 1 - P, k - P) for P in range(k + 1))

for k in [1, 2, 3, 4, 6, 8]:
    for m in [2, 3, 5, 10, 30, 64]:
        Kmax = k * (m - 1)
        vals = [p_exact(K, k) for K in range(Kmax + 1)]
        mn = min(vals); Kat = vals.index(mn); bound = 1 / (2 * sqrt(2 * k * m))
        ok = float(mn) >= bound
        if not ok: bad += 1
        print(f'k={k} m={m}: min_K Pr[non-constant] = {float(mn):.4f} (at K={Kat})   claimed bound 1/(2sqrt(2km)) = {bound:.4f}   ok={ok}   '
              f'ratio to sqrt(k/m)={float(mn)/sqrt(k/m):.3f}', flush=True)
print('total failures:', bad)
