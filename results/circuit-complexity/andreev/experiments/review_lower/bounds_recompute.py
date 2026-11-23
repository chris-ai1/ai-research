"""Referee recomputation of Corollary C numbers (§2.6 table, crossovers, closed forms), independent code.
Self-consistent bound: smallest integer S with S*f >= D0(S) = (2^k-k-1-log2(S+1))/(k+log2(S+1)).
(S*f - D0(S) is increasing in S, so the set of valid S is an up-ray and its minimum is a valid lower bound.)"""
import math
from fractions import Fraction

def D0(k, S):
    L = math.log2(S + 1); return (2 ** k - k - 1 - L) / (k + L)

def selfcons(k, f):
    lo, hi = 0, 1
    while hi * f < D0(k, hi): hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid * f >= D0(k, mid): hi = mid
        else: lo = mid
    return hi

def fcoh(k, m):
    if k <= 40: return float(Fraction(m ** k - (m - 1) ** k, m ** k))
    return -math.expm1(k * math.log1p(-1 / m))

def fbs(k, m): return min(k, 2 * math.sqrt(2 * k)) / m

def construction_d(k, m):
    N = 1 << k
    tot = sum(N // 2 + 2 * ((bin(S).count('1') * m + 1) // 2) + (bin(S).count('1') * m) // 2 for S in range(1, N))
    return tot + 3 * (N - 1) + 4 * k * m

print(f"{'k':>3} {'n':>10} {'coh LB':>10} {'bs LB':>10} {'closed coh':>11} {'closed bs':>10} {'n^1.5':>10} {'n^1.5/lg^2':>11} {'5n^2/16':>10} {'G_d (report formula)':>14}")
rows = {}
for k in [10, 16, 20, 24, 30, 36, 40, 50]:
    N = 1 << k; m = N // k; n = N + k * m
    a = selfcons(k, fcoh(k, m)); b = selfcons(k, fbs(k, m))
    cc = m * (N - 3 * k - 1) / (3 * k * k); cb = m * (N - 3 * k - 1) / (3 * k * min(k, 2 * math.sqrt(2 * k)))
    Gd = construction_d(k, m) if k <= 20 else float('nan')
    rows[k] = (a, b)
    print(f"{k:>3} {n:>10.2e} {a:>10.2e} {b:>10.2e} {cc:>11.2e} {cb:>10.2e} {n**1.5:>10.2e} {n**1.5/math.log2(n)**2:>11.2e} {5*n*n/16:>10.2e} {Gd:>14.3e}")
    assert cc <= a + 1 and cb <= b + 1, 'closed form exceeds self-consistent bound?'
    assert a <= 5 * n * n / 16 and b <= 5 * n * n / 16
# crossovers
for name, f in [('coherent', fcoh), ('blocksym', fbs)]:
    c1 = c2 = None
    for k in range(6, 70):
        N = 1 << k; m = N // k; n = N + k * m; L = selfcons(k, f(k, m))
        if c1 is None and L > n ** 1.5 / math.log2(n) ** 2: c1 = k
        if c2 is None and L > n ** 1.5: c2 = k
    print(f'{name}: exceeds n^1.5/log2(n)^2 from k={c1}; exceeds n^1.5 from k={c2}')
# exact balanced closed forms (k power of two, km=N exactly)
for k in [8, 16, 32]:
    N = 1 << k; m = N // k; assert k * m == N; n = 2 * N
    coh = N * (N - 3 * k - 1) / (3 * k ** 3); bs = N * (N - 3 * k - 1) / (6 * math.sqrt(2) * k ** 2.5)
    print(f'balanced k={k}: N(N-3k-1)/(3k^3)={coh:.3e}  N(N-3k-1)/(6sqrt2 k^2.5)={bs:.3e}  n^2/(12 log2^3 n)={n*n/(12*math.log2(n)**3):.3e}'
          f'   self-consistent: coh {selfcons(k, fcoh(k, m)):.3e} bs {selfcons(k, fbs(k, m)):.3e}  (5/16)n^2={5*n*n/16:.3e}')
# k=2 sanity vs exact minima (Theorem E bound m-1) and k=1
known = {1: 3, 2: 3, 3: 5, 4: 5, 5: 5, 6: 6, 8: 6, 10: 6}
for m, v in known.items():
    print(f'k=2 m={m}: Theorem E bound m-1={m-1}  vs solver value {v} ({"exact min" if m<=2 else "lower bound only"})  ok={(m-1)<=v or m>=8}')
