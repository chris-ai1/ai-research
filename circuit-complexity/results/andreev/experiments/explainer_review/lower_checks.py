#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Checks for Section 3 of explainer.md (sign-coherent lower bound)."""
import sys, math, random
sys.path.insert(0, '/tmp/andreev_gap/explainer_review')
from itertools import product
from fractions import Fraction as F
from math import comb, log2, sqrt

ok = {}
rng = random.Random(11)

# ---------- cube restriction ----------
def a_of(s, m):
    return [tuple(1 if p < si else 0 for p in range(m)) for si in s]

def cube_restriction_ok(k, m):
    for c in product(range(m), repeat=k):
        base = a_of(c, m)
        seen = set()
        for zz in product((0, 1), repeat=k):
            cz = [ci + zi for ci, zi in zip(c, zz)]
            cur = a_of(cz, m)
            for i in range(k):
                diff = [p for p in range(m) if cur[i][p] != base[i][p]]
                if diff != ([c[i]] if zz[i] else []):   # position c_i+1 is index c_i
                    return False
            addr = tuple((ci % 2) ^ zi for ci, zi in zip(c, zz))
            par = tuple(sum(blk) % 2 for blk in cur)
            if addr != par:
                return False
            seen.add(addr)
        if len(seen) != 1 << k:
            return False
    return True
ok['cube restriction: live bit at c_i+1, address (c mod 2) xor z, bijective (k<=3,m<=5)'] = all(
    cube_restriction_ok(k, m) for k in range(1, 4) for m in range(1, 6))

# ---------- lines ----------
def lines_ok(k, m):
    cubes = list(product(range(m), repeat=k))
    cubeset = set(cubes)
    for eps in product((1, -1), repeat=k):
        starts = [c for c in cubes if tuple(ci - ei for ci, ei in zip(c, eps)) not in cubeset]
        nonstart = len(cubes) - len(starts)
        cover = {}
        for st in starts:
            c = st
            while c in cubeset:
                cover[c] = cover.get(c, 0) + 1
                c = tuple(ci + ei for ci, ei in zip(c, eps))
        if not (len(starts) == m ** k - (m - 1) ** k and nonstart == (m - 1) ** k
                and all(cover.get(c, 0) == 1 for c in cubes)):
            return False
    return True
ok['lines: m^k-(m-1)^k lines, (m-1)^k non-starts, partition (k<=4,m<=6)'] = all(
    lines_ok(k, m) for k in range(1, 5) for m in range(1, 7))

# ---------- split counts of gates ----------
def split_count(wblocks, theta, tconst, k, m):
    """wblocks[i][p] = weight of position p in block i; form F(s) = tconst + sum_i prefix_i(s_i)"""
    pref = []
    for i in range(k):
        ps = [0]
        for p in range(m):
            ps.append(ps[-1] + wblocks[i][p])
        pref.append(ps)
    cnt = 0
    for c in product(range(m), repeat=k):
        vals = set()
        for zz in product((0, 1), repeat=k):
            Fv = tconst + sum(pref[i][c[i] + zz[i]] for i in range(k))
            vals.add(Fv >= theta)
        cnt += (len(vals) == 2)
    return cnt

coh_ok = True; worst = {}
for trial in range(4000):
    k = rng.randint(1, 4); m = rng.randint(1, 6)
    wb = []
    for i in range(k):
        sgn = rng.choice((1, -1))
        mode = rng.random()
        if mode < 0.3:
            blk = [sgn * rng.choice((0, 0, 1, 2)) for _ in range(m)]          # zeros and ties
        else:
            blk = [sgn * rng.randint(0, 9) for _ in range(m)]
        wb.append(blk)
    tconst = rng.randint(-20, 20)    # table contribution for a fixed table
    theta = rng.randint(-30, 30) + rng.choice((0, 0.5))
    sc = split_count(wb, theta, tconst, k, m)
    bound = m ** k - (m - 1) ** k
    coh_ok &= sc <= bound
    worst[(k, m)] = max(worst.get((k, m), 0), sc)
ok['random sign-coherent gates split <= m^k-(m-1)^k cubes (4000 trials)'] = coh_ok

# tight example: one large weight on the last position of each block
tight_ok = True
for k in range(1, 5):
    for m in range(1, 7):
        wb = [[0] * (m - 1) + [k + 1] for _ in range(k)]
        tight_ok &= split_count(wb, 1, 0, k, m) == m ** k - (m - 1) ** k
ok['tight example attains m^k-(m-1)^k for all k<=4, m<=6'] = tight_ok

# mixed signs can split every cube
ok['alternating +1,-1 weights (k=1) split all m cubes'] = all(
    split_count([[(-1) ** p for p in range(m)]], 1, 0, 1, m) == m for m in range(1, 10))

# ---------- inequalities ----------
ok['m^k-(m-1)^k <= k m^(k-1) and 1-(1-1/m)^k <= k/m (k<=40, m<=300)'] = all(
    m ** k - (m - 1) ** k <= k * m ** (k - 1) and 1 - (1 - F(1, m)) ** k <= F(k, m)
    for k in range(1, 41) for m in range(1, 301))
ok['log2 C(S,D) <= D log2 S (S<=400)'] = all(
    log2(comb(S, D)) <= D * log2(S) + 1e-12 for S in range(1, 401) for D in range(0, S + 1))
ok['log2(2^k+1) <= k+1 and log2(2^k-1) <= k'] = all(log2(2 ** k + 1) <= k + 1 and log2(2 ** k - 1) <= k for k in range(1, 60))

def D0(N, k, S):
    return max(0.0, N - k - 1 - log2(S + 1)) / (k + log2(S + 1))

# S < N^2 => D0 >= (N-3k-1)/(3k)
g_ok = True
for k in range(1, 25):
    N = 2 ** k
    for S in sorted(set([1, 2, 3, 10, 100, N, N * N - 1] + [rng.randint(1, N * N - 1) for _ in range(50)])):
        if S < N * N:
            g_ok &= D0(N, k, S) >= (N - 3 * k - 1) / (3 * k) - 1e-12
ok['S < N^2 => D0 >= (N-3k-1)/(3k)'] = g_ok

# smallest S allowed by the first inequality, versus the stated balanced bound
print('balanced k: smallest S with S >= m^k/(m^k-(m-1)^k) D0(S);  N(N-3k-1)/(3k^3);  ratio; D0 there; N/(2k); N/(3k)')
bal_ok = True
for k in (4, 8, 16, 32):
    N = 2 ** k; m = N // k
    fac = F(m ** k, m ** k - (m - 1) ** k) if k <= 16 else None
    facf = float(fac) if fac is not None else 1.0 / (1 - (1 - 1 / m) ** k)
    # binary search smallest integer S >= 1 with S >= facf * D0(S)
    lo, hi = 1, 4 * N * N
    while lo < hi:
        mid = (lo + hi) // 2
        if mid >= facf * D0(N, k, mid):
            hi = mid
        else:
            lo = mid + 1
    stated = N * (N - 3 * k - 1) / (3 * k ** 3)
    bal_ok &= lo >= stated - 1
    print('  ', k, lo, round(stated, 2), round(lo / max(stated, 1e-9), 3), round(D0(N, k, lo), 2), N / (2 * k), round(N / (3 * k), 2))
ok['smallest admissible S >= N(N-3k-1)/(3k^3) (k=4..32)'] = bal_ok

# crossover with n^{3/2}, n = 2N, using the stated balanced bound (k treated as real-valued formula)
cross = [k for k in range(2, 80) if (2 ** k) * (2 ** k - 3 * k - 1) / (3 * k ** 3) > (2 * 2 ** k) ** 1.5]
print('stated bound N(N-3k-1)/(3k^3) exceeds n^{3/2} (n=2N) first at k =', cross[0])
# with the sharper first inequality and m = N/k real
def smallest_S(k):
    N = 2 ** k; m = N / k
    facf = 1.0 / (1 - (1 - 1 / m) ** k)
    lo, hi = 1, 4 * N * N
    while lo < hi:
        mid = (lo + hi) // 2
        if mid >= facf * D0(N, k, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
cross2 = [k for k in range(2, 60) if smallest_S(k) > (2 * 2 ** k) ** 1.5]
print('sharper form (smallest admissible S, m=N/k real) exceeds n^{3/2} first at k =', cross2[0])
# with n = N + k*floor(N/k) (floor balance)
cross3 = [k for k in range(2, 80) if (2 ** k) * (2 ** k - 3 * k - 1) / (3 * k ** 3) > (2 ** k + k * (2 ** k // k)) ** 1.5]
print('floor-balance n, stated bound exceeds n^{3/2} first at k =', cross3[0])
# power-of-two k only (exact balance)
cross4 = [k for k in (2, 4, 8, 16, 32, 64) if (2 ** k) * (2 ** k - 3 * k - 1) / (3 * k ** 3) > (2 * 2 ** k) ** 1.5]
print('exact balance (k power of two): first k =', cross4[0])

# ---------- random +-1 gate remark ----------
def rad_pmf(r):
    return {v: comb(r, (r + v) // 2) / 2 ** r for v in range(-r, r + 1, 2)}

def p_nonconst(k, r, theta):
    """gate [R + sum_i l_i z_i >= theta], l_i iid +-1 (q of them +1), R = sum of r iid signs.
    non-constant iff R-(k-q) < theta <= R+q"""
    pmf = rad_pmf(r)
    tot = 0.0
    for q in range(k + 1):
        pq = comb(k, q) / 2 ** k
        tot += pq * sum(p for v, p in pmf.items() if v - (k - q) < theta <= v + q)
    return tot

# brute-force validation of the formula on tiny cases
def brute(k, m, theta):
    worst = 1.0
    for live in product(range(m), repeat=k):
        fixed_pos = [(i, p) for i in range(k) for p in range(m) if p != live[i]]
        for vals in product((0, 1), repeat=len(fixed_pos)):
            cnt = 0
            for w in product((1, -1), repeat=k * m):
                R = sum(w[i * m + p] * v for (i, p), v in zip(fixed_pos, vals))
                outs = set()
                for zz in product((0, 1), repeat=k):
                    outs.add(R + sum(w[i * m + live[i]] * zz[i] for i in range(k)) >= theta)
                cnt += len(outs) == 2
            worst = min(worst, cnt / 2 ** (k * m))
    return worst
bf = {(k, m): brute(k, m, 0) for k, m in [(1, 1), (1, 3), (1, 5), (2, 2), (2, 3), (3, 2)]}
form = {(k, m): min(p_nonconst(k, r, 0) for r in range(0, k * (m - 1) + 1)) for (k, m) in bf}
ok['random-sign formula matches brute force (threshold 0)'] = all(abs(bf[x] - form[x]) < 1e-12 for x in bf)
ok['threshold 0: every restriction gives P(non-constant) >= 1/(2 sqrt(2km)) (k<=12, m<=60)'] = all(
    min(p_nonconst(k, r, 0) for r in range(0, k * (m - 1) + 1)) >= 1 / (2 * sqrt(2 * k * m))
    for k in range(1, 13) for m in range(1, 61))
worst_ratio = min(min(p_nonconst(k, r, 0) for r in range(0, k * (m - 1) + 1)) * 2 * sqrt(2 * k * m)
                  for k in range(1, 13) for m in range(1, 61))
print('threshold 0: min over k<=12,m<=60 of P(non-const) * 2 sqrt(2km) =', round(worst_ratio, 4))
# a large threshold breaks it, so the threshold must be specified
print('threshold = k*m (k=2,m=10): min_r P(non-constant) =', min(p_nonconst(2, r, 20) for r in range(0, 2 * 9 + 1)))

for kk, v in ok.items():
    print(f"{'PASS' if v else 'FAIL'}  {kk}")
