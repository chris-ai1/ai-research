#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Independent checks of the identities and claims in Section 2 of explainer.md.

Written from the explainer's and paper's statements, not from the paper's script.
Run: python3 -I check_identities.py
"""
import sys
sys.path.insert(0, '/tmp/pydeps')
from fractions import Fraction as F
from itertools import product, combinations
import random

def ceil2(u):  # ceil(u/2) for integers, including negatives
    return -((-u) // 2)

def chi(S, b):  # S, b as bitmasks
    return -1 if bin(S & b).count('1') % 2 else 1

ok = {}

# ---------- Tool 1: Fourier lookup ----------
def tool1(k):
    N = 1 << k
    for x in product((0, 1), repeat=N):
        X = [sum(chi(S, c) * (1 - 2 * x[c]) for c in range(N)) for S in range(N)]
        for S in range(N):
            assert X[S] % 2 == 0 and -N <= X[S] <= N
        for b in range(N):
            assert sum(X[S] * chi(S, b) for S in range(N)) == N * (1 - 2 * x[b])
    return True
ok['tool1 Fourier lookup k<=4'] = all(tool1(k) for k in range(1, 5))

# ---------- Tool 2: staircase telescoping ----------
rng = random.Random(1)
def tool2():
    for _ in range(200):
        lo = rng.randint(-10, 5); hi = lo + rng.randint(0, 15)
        g = {u: rng.randint(-50, 50) for u in range(lo, hi + 1)}
        for L in range(lo, hi + 1):
            val = g[lo] + sum((g[t] - g[t - 1]) * (L >= t) for t in range(lo + 1, hi + 1))
            assert val == g[L]
        # equal steps except on a subset T => affine part + |T| gates
        d = rng.randint(-5, 5); T = set(rng.sample(range(lo + 1, hi + 1), min(3, hi - lo)))
        h = {lo: g[lo]}
        for t in range(lo + 1, hi + 1):
            h[t] = h[t - 1] + (d if t not in T else rng.randint(-9, 9))
        for L in range(lo, hi + 1):
            val = h[lo] + d * (L - lo) + sum((h[t] - h[t - 1] - d) * (L >= t) for t in T)
            assert val == h[L]
    return True
ok['tool2 telescoping + equal-steps remark'] = tool2()

# "ceil(u/2) and ceil(u/2)^2 change only at odd u"
ok['ceil(u/2) changes exactly at odd u (u in [-40,40])'] = all(
    (ceil2(u) != ceil2(u - 1)) == (u % 2 == 1) for u in range(-40, 41))
ok['ceil(u/2)^2 changes exactly at odd u (u in [-40,40])'] = all(
    (ceil2(u) ** 2 != ceil2(u - 1) ** 2) == (u % 2 == 1) for u in range(-40, 41))

# ---------- Tool 3 ----------
phi = lambda u: (-1) ** (u % 2) * u
ok['tool3 X(-1)^t = phi(X+t)-phi(t), X even'] = all(
    X * (-1) ** (t % 2) == phi(X + t) - phi(t) for X in range(-30, 31, 2) for t in range(-30, 31))
ok['tool3 fails for some odd X (so evenness needed)'] = any(
    X * (-1) ** (t % 2) != phi(X + t) - phi(t) for X in range(-5, 6, 2) for t in range(-5, 6))

# Tool 3 count: sum_S (2N + 2|S|m) = 2N^2 + kmN; = 3/4 n^2 at balance
def tool3count(k, m):
    N = 1 << k
    return sum(2 * N + 2 * bin(S).count('1') * m for S in range(N))
ok['tool3 count 2N^2+kmN'] = all(tool3count(k, m) == 2 * (1 << k) ** 2 + k * m * (1 << k)
                                 for k in range(1, 9) for m in range(1, 9))
ok['tool3 count = 3/4 n^2 at balance'] = all(
    F(tool3count(k, (1 << k) // k)) == F(3, 4) * (2 * (1 << k)) ** 2 for k in (1, 2, 4, 8))

# ---------- Saving 2 identity ----------
def sav2(W, t):
    return 4 * W - 8 * ceil2(2 * W + t) ** 2 + 8 * W * W + 8 * W * t + 8 * ceil2(t) ** 2
ok['saving2 identity all integers W,t in [-40,40]'] = all(
    4 * W * (-1) ** (t % 2) == sav2(W, t) for W in range(-40, 41) for t in range(-40, 41))
ok['saving2 ceilings: even t -> W+t/2, t/2; odd t -> W+(t+1)/2, (t+1)/2'] = all(
    (ceil2(2 * W + t), ceil2(t)) == ((W + t // 2, t // 2) if t % 2 == 0 else (W + (t + 1) // 2, (t + 1) // 2))
    for W in range(-20, 21) for t in range(-20, 21))

# ---------- Saving 1 and Saving 3, exact over small k ----------
def forms(k, m, x, s):
    N = 1 << k
    alpha = (m - 1) // 2
    b = sum((s[i] % 2) << i for i in range(k))
    Y = {S: sum(x[c] for c in range(N) if bin(S & c).count('1') % 2) for S in range(1, N)}
    Ynz = {S: sum(x[c] for c in range(1, N) if bin(S & c).count('1') % 2) for S in range(1, N)}
    t = {S: sum(s[i] for i in range(k) if S >> i & 1) for S in range(N)}
    e = [1 << i for i in range(k)]
    W = {S: Y[S] + alpha * sum(x[e[i]] for i in range(k) if S >> i & 1) for S in range(1, N)}
    z = sum(x[1:]); E = sum(x[ei] for ei in e); sig = sum(s)
    return N, alpha, b, Y, Ynz, t, e, W, z, E, sig

res = dict(c0_redundant=True, X_eq_4Y_minus_2absx=True, Y_range=True, saving1_sum=True,
           sumY2_formula=True, sumYt_formula=True, paper_id1=True, paper_id2=True, paper_id3=True,
           kappa_id=True, x0_id=True, shift_any_fn=True, lstar_range=True)
counter_absx = None
seen = {}
for k in range(1, 4):
    for m in range(1, 5):
        for x in product((0, 1), repeat=1 << k):
            for s in product(range(m + 1), repeat=k):
                N, alpha, b, Y, Ynz, t, e, W, z, E, sig = forms(k, m, x, s)
                absx = sum(x)
                X = {S: sum(chi(S, c) * (1 - 2 * x[c]) for c in range(N)) for S in range(N)}
                for S in range(1, N):
                    res['c0_redundant'] &= (Y[S] == Ynz[S])
                    res['X_eq_4Y_minus_2absx'] &= (X[S] == 4 * Y[S] - 2 * absx)
                    res['Y_range'] &= (0 <= Y[S] <= N // 2)
                # Saving 1 summed: sum_{S!=0} 4 Y_S chi_S(b) = 2N[b=0] z - 2N[b!=0] x_b
                lhs = sum(4 * Y[S] * chi(S, b) for S in range(1, N))
                res['saving1_sum'] &= (lhs == (2 * N * z if b == 0 else -2 * N * x[b]))
                # Saving 3 example sums
                sY2 = sum(Y[S] ** 2 for S in range(1, N))
                sYt = sum(Y[S] * t[S] for S in range(1, N))
                prod_terms = tuple(x[e[i]] * s[i] for i in range(k))
                res['sumY2_formula'] &= (4 * sY2 == N * (z * z + z))
                res['sumYt_formula'] &= (4 * sYt == N * (sig * z + sum(prod_terms)))
                # Is sum Y_S^2 a function of (|x|, sigma, products)?  record collisions
                key = (k, m, absx, sig, prod_terms)
                if key in seen and seen[key][0] != sY2 and counter_absx is None:
                    counter_absx = (k, m, seen[key][1], (x, s), seen[key][0], sY2)
                seen.setdefault(key, (sY2, (x, s)))
                # Paper's three identities
                ind = lambda p: 1 if p else 0
                id1 = sum(4 * W[S] * chi(S, b) for S in range(1, N))
                rhs1 = 2 * N * ind(b == 0) * z - 2 * N * ind(b != 0) * x[b] + 2 * alpha * N * sum(
                    x[e[i]] * (ind(b == 0) - ind(b == e[i])) for i in range(k))
                res['paper_id1'] &= (id1 == rhs1)
                w = 2 * z + 2 * alpha * E + sig
                id2 = 8 * sum(W[S] ** 2 + W[S] * t[S] for S in range(1, N))
                rhs2 = F(N, 2) * (w * w - sig * sig) + 2 * N * z + (4 * alpha + 2 * alpha ** 2) * N * E + 2 * N * (1 + alpha) * sum(prod_terms)
                res['paper_id2'] &= (id2 == rhs2)
                id3 = 8 * sum(ceil2(t[S]) ** 2 for S in range(1, N))
                rhs3 = F(N, 2) * (sig * sig + sum(si * si for si in s)) + N * (sig + 1) * ind(b != 0) + N * sum(
                    s[i] * ind(b == e[i]) for i in range(k))
                res['paper_id3'] &= (id3 == rhs3)
                kap = {S: -4 * (2 * alpha + 1) * (k - 2 * bin(S).count('1')) for S in range(1, N)}
                idk = sum(kap[S] * (F(ceil2(t[S])) - F(t[S], 2)) for S in range(1, N))
                res['kappa_id'] &= (idk == N * (2 * alpha + 1) * sum(ind(b == ei) for ei in e))
                idx0 = x[0] - x[0] * sig + F(4, N) * sum(x[0] * (t[S] // 2) for S in range(1, N))
                res['x0_id'] &= (idx0 == x[0] * ind(b == 0))
                # shifting odd coefficients: sum_{odd theta<=h}[L>=theta] = ceil(L/2) and
                # ceil(L_S/2) = W_S + t_S/2 + 1/4 - chi_S(b)/4
                for S in range(1, N):
                    L = 2 * W[S] + t[S]
                    h = N + 2 * alpha * bin(S).count('1') + bin(S).count('1') * m
                    res['lstar_range'] &= (0 <= L <= h)
                    cnt = sum(1 for th in range(1, h + 1, 2) if L >= th)
                    res['shift_any_fn'] &= (cnt == ceil2(L)) and (F(ceil2(L)) == W[S] + F(t[S], 2) + F(1, 4) - F(chi(S, b), 4))
for kk, v in res.items():
    ok['exhaustive k<=3,m<=4: ' + kk] = v
ok['sum_S Y_S^2 is a function of (|x|, sigma, x_{e_i}s_i)'] = counter_absx is None

for kk, v in ok.items():
    print(f"{'PASS' if v else 'FAIL'}  {kk}")
print('counterexample to "expressions in |x|":', counter_absx)
