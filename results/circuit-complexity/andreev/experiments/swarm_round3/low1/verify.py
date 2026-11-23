# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Exact guardrails for round-three LOW1; not asymptotic inference."""
from fractions import Fraction
from itertools import product, permutations
from math import comb, factorial
from pathlib import Path
import json
import random

rng = random.Random(11032026)
counts = {}

def mobius(values, d):
    out = list(values)
    for i in range(d):
        for mask in range(1 << d):
            if mask >> i & 1:
                out[mask] -= out[mask ^ (1 << i)]
    return out

# Every coefficient of any strict parity score, in every flipped basis.
count = 0
for d in range(2, 8):
    for trial in range(5):
        values = [(-1)**z.bit_count() * rng.randrange(1, 1000) for z in range(1 << d)]
        for base in range(1 << d):
            coeff = mobius([values[z ^ base] for z in range(1 << d)], d)
            for u, c in enumerate(coeff):
                assert c * (-1)**((base.bit_count() + u.bit_count()) % 2) > 0
                count += 1
counts['strict_parity_face_coefficients'] = count

# Preservation of superincreasing magnitudes by arbitrary disjoint pair sums.
count = 0
for d in range(2, 7):
    for trial in range(35):
        w = []
        for _ in range(2*d):
            w.append(sum(w) + rng.randrange(1, 6))
        w = [v * rng.choice((-1, 1)) for v in w]
        rng.shuffle(w)
        for signs in product((-1, 1), repeat=d):
            merged = sorted((abs(w[2*i] + signs[i]*w[2*i+1]) for i in range(d)), reverse=True)
            assert all(merged[i] > sum(merged[i+1:]) for i in range(d))
            count += 1
counts['superincreasing_pair_identifications'] = count

# Exact average monomial support of superincreasing thresholds, all offsets.
count = 0
for d in range(2, 7):
    for trial in range(4):
        w = [3**i * rng.choice((-1, 1)) for i in range(d)]
        rng.shuffle(w)
        vals = [sum(w[i] for i in range(d) if z >> i & 1) for z in range(1 << d)]
        cuts = [min(vals)-1] + sorted(set(vals)) + [max(vals)+1]
        for cut in cuts:
            truth = [int(v >= cut) for v in vals]
            support_sum = sum(sum(c != 0 for c in mobius([truth[z ^ base] for z in range(1 << d)], d)) for base in range(1 << d))
            assert Fraction(support_sum, 1 << d) <= 3 * Fraction(3, 2)**d
            count += 1
counts['lex_threshold_average_support'] = count

# Exact helper expectation equals the permanent of A=(1+C)/2.
count = 0
for d in range(2, 6):
    for trial in range(14):
        u = [rng.randrange(-3, 4) for _ in range(d)]
        v = [rng.randrange(-3, 4) for _ in range(d)]
        matrix = [[sum(Fraction(1 if u[i]+s*v[j] == 0 else 2, 2) for s in (-1, 1))/2 for j in range(d)] for i in range(d)]
        per = Fraction(0)
        brute = Fraction(0)
        for p in permutations(range(d)):
            term = Fraction(1)
            for i in range(d):
                term *= matrix[i][p[i]]
            per += term
            for signs in product((-1, 1), repeat=d):
                s = sum(u[i]+signs[i]*v[p[i]] != 0 for i in range(d))
                brute += Fraction(2**s, 2**d)
                count += 1
        brute /= factorial(d) * 2**d
        assert brute == per / factorial(d)
counts['helper_permanent_restrictions'] = count

# Incidence of profile-separating unordered cuts: exactly 2^(q-1)-1.
count = 0
for k in range(2, 8):
    for levels in product(range(3), repeat=k):
        q = len(set(levels))
        exceptional = 0
        for mask in range(1, (1 << k)-1):
            if not (mask & 1):
                continue
            selected = {levels[i] for i in range(k) if mask >> i & 1}
            ignored = {levels[i] for i in range(k) if not (mask >> i & 1)}
            separated = selected.isdisjoint(ignored)
            equal_edge = any(levels[i] == levels[j] for i in range(k) if mask >> i & 1 for j in range(k) if not(mask >> j & 1))
            assert separated != equal_edge
            exceptional += separated
            count += 1
        assert exceptional == 2**(q-1)-1
counts['magnitude_class_cut_incidences'] = count

# On all graph pairs, a nonseparated profile has survival <= 2^-r.
count = 0
for k in range(2, 7):
    for trial in range(150):
        mask = rng.randrange(1, (1 << k)-1)
        levels = [rng.randrange(4) for _ in range(k)]
        edges = [(i,j) for i in range(k) if mask >> i & 1 for j in range(k) if not(mask >> j & 1)]
        r = rng.randrange(2, 5)
        prob = Fraction(1)
        for i,j in edges:
            for _ in range(r):
                u = levels[i] * rng.choice((-1,1))
                v = levels[j] * rng.choice((-1,1))
                prob *= Fraction(sum(u+t*v != 0 for t in (-1,1)), 2)
        if any(levels[i] == levels[j] for i,j in edges):
            assert prob <= Fraction(1, 2**r)
        count += 1
counts['profile_graph_survival_products'] = count

# Every bad baseline is on one of at most W+1 integer hyperplanes;
# all baseline coefficients are nonzero for separated block magnitudes.
count = 0
for a in range(4):
    for b in range(4):
        if a == b:
            continue
        for D in range(2, 7):
            for L in range(1, 5):
                coeff = [a*rng.choice((-1,1)) + b*rng.choice((-1,1)) for _ in range(D)]
                assert all(c != 0 for c in coeff)
                live = [a*rng.choice((-1,1)) for _ in range(L)] + [b*rng.choice((-1,1)) for _ in range(L)]
                lo = sum(min(0,c) for c in live)
                hi = sum(max(0,c) for c in live)
                W = hi-lo
                assert W == L*(a+b)
                baseline = [sum(coeff[i] for i in range(D) if z >> i & 1) for z in range(1 << D)]
                for theta2 in range(2*(min(baseline)+lo)-1, 2*(max(baseline)+hi)+2):
                    bad_levels = {v for v in baseline if 2*(v+lo) < theta2 <= 2*(v+hi)}
                    assert len(bad_levels) <= W+1
                    count += 1
counts['integer_bad_baseline_bands'] = count

# Prior quadratic-helper counterexample remains exact and has positive charge.
count = 0
for d in range(2, 32):
    f = [Fraction((-1)**r * sum(comb(d,u) for u in range(r+1)), d*comb(d-1,r)) for r in range(d)]
    for s in range(d+1):
        helper = (d-s)*f[s] if s<d else Fraction(0)
        if s:
            helper += s*f[s-1]
        assert helper + (-1)**d * 2**d * (s==d) == (-1)**s
        count += 1
    assert Fraction(d*(d-1), 2) + 3*Fraction(3,4)**d >= 1-Fraction(d+1,2**d)
counts['quadratic_helper_layer_identities'] = count

out = {'Authors':'Christian Reitwiessner', 'status':'all exact checks passed', 'checks':counts,
       'scope':'Finite algebraic guardrails only. Universal claims use the report proofs and cited hyperplane-cover theorem.'}
Path(__file__).with_name('verification.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out, indent=2))
