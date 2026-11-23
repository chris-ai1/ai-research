#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Checks of the cost table, the exact count formula, and its balanced asymptotics."""
import sys, math
sys.path.insert(0, '/tmp/andreev_gap/explainer_review')
from fractions import Fraction as F
from build_circuit import build, formula, stats

def popcount(v):
    return bin(v).count('1')

ok = {}
# main-ridge + last-correction identity (paper display before bestcount)
def lhs(k, m):
    N = 1 << k; a = (m - 1) // 2
    return sum(-(-(N + 2 * a * popcount(S) + popcount(S) * m) // 2) + (popcount(S) * m) // 2 for S in range(1, N))
ok['main+corr = N(N-1)/2 + alpha kN/2 + kmN/2 (k<=10, m<=40)'] = all(
    F(lhs(k, m)) == F((1 << k) * ((1 << k) - 1), 2) + F(((m - 1) // 2) * k * (1 << k), 2) + F(k * m * (1 << k), 2)
    for k in range(1, 11) for m in range(1, 41))
ok['sum_S |S| = kN/2'] = all(sum(popcount(S) for S in range(1 << k)) == k * (1 << k) // 2 for k in range(1, 15))
# formula = main+corr + R + 2km + (km - floor(km/2))
ok['formula = main+corr + R + km (squares) + km (products) + ceil(km/2) (x0 sigma gates net)'] = all(
    formula(k, m) == lhs(k, m) + (2 * ((1 << k) - 1) + 2 * ((m - 1) // 2) * k + k * m) + k * m + k * m + (k * m - (k * m) // 2)
    for k in range(1, 11) for m in range(1, 41))

# cost-table rows at exact balance in units of N^2 (leading terms)
rows = []
for k in (1, 2, 4, 8, 16, 32):
    N = 1 << k; m = N // k; a = (m - 1) // 2
    main2Y = F(N * (N - 1), 2)
    tpart = sum(F(popcount(S) * m, 2) for S in range(1, N)) if k <= 16 else F(k * m * N, 4)
    amp = F(a * k * N, 2)
    corr = F(k * m * N, 4)
    rows.append((k, float(main2Y / N**2), float(tpart / N**2), float(amp / N**2), float(corr / N**2),
                 float((main2Y + tpart + amp + corr) / N**2)))
print('balanced rows (k, 2Y-part, t-part, amplification, b=0 corr, total) in units of N^2:')
for r in rows:
    print('  ', r)

# exact balance asymptotics: total = formula + 1 vs 5/16 n^2 - n/4 log2(n/2) + O(n)
print('exact balance: k, n, total, residual, residual - (3n - 2k - 1)')
res_ok = True
for k in (1, 2, 4, 8, 16, 32, 64):
    N = 1 << k; m = N // k; n = N + k * m
    assert k * m == N
    total = formula(k, m) + 1
    main = F(5, 16) * n * n - F(n, 4) * math.log2(n // 2)
    resid = F(total) - main
    res_ok &= (resid == 3 * n - 2 * k - 1)
    print('  ', k, n, total, float(resid), float(resid - (3 * n - 2 * k - 1)), 'resid/n =', float(resid / n))
ok['exact balance: total = 5/16 n^2 - n/4 log2(n/2) + 3n - 2k - 1'] = res_ok

# floor balance m = floor(N/k): ratio -> 5/16
print('floor balance: k, m, n, total/n^2')
for k in (3, 5, 6, 7, 10, 12, 20, 30, 40, 60):
    N = 1 << k; m = N // k; n = N + k * m
    print('  ', k, m, n, (formula(k, m) + 1) / n ** 2)

# weights at larger sizes (build only, no evaluation)
print('weights: k, m, n, gates, formula, max bottom weight, max threshold, max top, max top / n^2')
for k, m in [(4, 4), (5, 6), (6, 10), (8, 32)]:
    c = build(k, m); st = stats(c)
    print('  ', k, m, st['n'], st['gates'], st['formula'], st['max_bottom_weight'], st['max_threshold'], st['max_top'],
          round(st['max_top'] / st['n'] ** 2, 3), 'coherent', st['coherent_nonneg'])

# 58264 cases
ok['58264 = sum_{k<=3,m<=4} 2^N (m+1)^k'] = sum(2 ** (1 << k) * (m + 1) ** k for k in range(1, 4) for m in range(1, 5)) == 58264

# Where does the gap below the formula come from at k=4?  main coefficients -8 theta + kappa_S vanish
for k, m in [(4, 4), (8, 32)]:
    N = 1 << k; a = (m - 1) // 2
    vanish = 0
    for S in range(1, N):
        kap = -4 * (2 * a + 1) * (k - 2 * popcount(S))
        top = N + 2 * a * popcount(S) + popcount(S) * m
        vanish += sum(1 for th in range(1, top + 1, 2) if -8 * th + kap == 0)
    print(f'k={k}, m={m}: main-staircase coefficients that vanish: {vanish}; formula - realized =',
          formula(k, m) - stats(build(k, m))['gates'])

for kk, v in ok.items():
    print(f"{'PASS' if v else 'FAIL'}  {kk}")
