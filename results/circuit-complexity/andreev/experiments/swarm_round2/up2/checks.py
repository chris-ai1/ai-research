# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Exact guardrails for UP2 round two; no asymptotic inference from checks."""
from fractions import Fraction
from itertools import product
from math import comb
from pathlib import Path
import json
import random

OUT = Path(__file__).resolve().parent
rng = random.Random(2026111102)
counts = {}

def chi(t, c):
    return -1 if (t & c).bit_count() % 2 else 1

def phi(z):
    return (-1 if z % 2 else 1) * z

def ladder(z, low, high):
    assert low <= z <= high
    return phi(low) + sum((phi(t) - phi(t - 1)) * (z >= t)
                          for t in range(low + 1, high + 1))

# Compare actual table offsets, exact gate differences, and half-open slabs.
checks = cancellations = slabs = semantic = 0
for k, m, repeats in [(2, 2, 30), (3, 2, 20)]:
    N, M = 1 << k, k * m
    addresses = list(product((0, 1), repeat=M))
    for _ in range(repeats):
        coeff = [0] * N
        for t in rng.sample(range(N), rng.randint(1, min(4, N))):
            coeff[t] = rng.choice((-3, -2, -1, 1, 2, 3))
        alpha = [sum(coeff[t] * chi(t, c) for t in range(N))
                 for c in range(N)]
        gamma = [rng.randrange(-2, 3) for _ in range(M)]
        theta = Fraction(rng.randrange(-12, 13), 2)
        active = []
        for T in range(1, N):
            xp = [(1 + chi(T, c)) // 2 for c in range(N)]
            xm = [1 - u for u in xp]
            ap = sum(u * v for u, v in zip(alpha, xp))
            am = sum(u * v for u, v in zip(alpha, xm))
            assert ap - am == N * coeff[T]
            diffs = []
            for a in addresses:
                A = sum(u * v for u, v in zip(gamma, a))
                delta = int(ap + A >= theta) - int(am + A >= theta)
                if ap > am:
                    want = int(theta - ap <= A < theta - am)
                elif am > ap:
                    want = -int(theta - am <= A < theta - ap)
                else:
                    want = 0
                assert delta == want
                slabs += 1
                if not coeff[T]:
                    assert delta == 0
                    cancellations += 1
                diffs.append(delta)
                checks += 1
            if len(set(diffs)) > 1:
                active.append(T)
        assert all(coeff[T] for T in active)
        semantic += 1
counts.update(table_pair_gate_values=checks, half_open_slab_checks=slabs,
              exact_channel_cancellations=cancellations,
              semantic_activation_subset_checks=semantic)

# Actual raw-gate compilation of the full-support odd/even-scale construction.
# X_T is even; L_T has odd coefficients exactly on the character's blocks.
# Every table/address input is used for each instance.
cases = gates_evaluated = edges = 0
instances = []
for k, m in [(1, 2), (2, 2), (2, 3), (3, 1), (3, 2)]:
    N, M = 1 << k, k * m
    rows = {}
    gate_count = 0
    for T in range(1, N):
        row = [rng.choice((-1, 1)) * (1 if T & (1 << (l // m)) else 2)
               for l in range(M)]
        lo, hi = sum(min(w, 0) for w in row), sum(max(w, 0) for w in row)
        rows[T] = (row, lo, hi)
        gate_count += 2 * N + 2 * (hi - lo)
    expected = 2 * N * (N - 1) + 3 * M * N - 4 * M
    assert gate_count == expected
    min_margin = None
    addresses = list(product((0, 1), repeat=M))
    for x in product((0, 1), repeat=N):
        xi = [1 - 2 * v for v in x]
        X = [sum(chi(T, c) * xi[c] for c in range(N)) for T in range(N)]
        for a in addresses:
            b = sum((sum(a[i*m:(i+1)*m]) % 2) << i for i in range(k))
            score = X[0]
            for T, (row, lo, hi) in rows.items():
                L = sum(w * v for w, v in zip(row, a))
                assert (-1 if L % 2 else 1) == chi(T, b)
                part = ladder(X[T] + L, lo - N, hi + N) - ladder(L, lo, hi)
                assert part == X[T] * chi(T, b)
                score += part
            assert score == N * xi[b]
            margin = xi[b] * score
            min_margin = margin if min_margin is None else min(min_margin, margin)
            cases += 1
            gates_evaluated += gate_count
    # On complementary character tables, test nonconstant difference and
    # actual threshold boundary coverage on every selected-coordinate edge.
    for T, (row, lo, hi) in rows.items():
        selected = [l for l in range(M) if T & (1 << (l // m))]
        for bits in product((0, 1), repeat=len(selected)):
            a = [0] * M
            for l, v in zip(selected, bits):
                a[l] = v
            L = sum(w * v for w, v in zip(row, a))
            for pos, l in enumerate(selected):
                if bits[pos]:
                    continue
                Lp = L + row[l]
                # xi = +/- chi_T gives X_T = +/-N. Bottom gates of
                # other characters and pure-address ladders cancel.
                assert any((N + L >= cut) != (N + Lp >= cut) or
                           (-N + L >= cut) != (-N + Lp >= cut)
                           for cut in range(lo - N + 1, hi + N + 1))
                edges += 1
    instances.append(dict(k=k, m=m, bottoms=gate_count, min_signed_margin=min_margin))
counts.update(compiled_lookup_inputs=cases, raw_bottom_evaluations=gates_evaluated,
              character_pair_selected_edges=edges, instances=instances)

# Elementary overlap bound supplied to LOW1: exact rational verification of
# E[2^-Q] <= (1-b/(2d))^a for Q hypergeometric(d,b,a).
checks = 0
for d in range(1, 31):
    for a in range(d + 1):
        for b in range(d + 1):
            val = sum((Fraction(comb(b, q) * comb(d-b, a-q), comb(d, a) * (1 << q))
                       for q in range(max(0, a-(d-b)), min(a, b)+1)), Fraction())
            assert val <= Fraction(2*d - b, 2*d) ** a
            checks += 1
counts['hypergeometric_overlap_checks'] = checks

# General mixed support pair-cover formula, for equal nonzero magnitudes.
checks = 0
from itertools import permutations
for d in range(1, 5):
    perms = list(permutations(range(d)))
    for A in range(1 << d):
        for B in range(1 << d):
            a, b = A.bit_count(), B.bit_count()
            exact = Fraction()
            for p in perms:
                n_both = 0
                possible = True
                for i in range(d):
                    u, v = (A >> i) & 1, (B >> p[i]) & 1
                    if not (u or v):
                        possible = False
                        break
                    if u and v:
                        n_both += 1
                if possible:
                    exact += Fraction(1, 1 << n_both)
            exact /= len(perms)
            want = (Fraction(comb(b, d-a), comb(d, d-a) * (1 << (a+b-d)))
                    if a+b >= d else Fraction())
            assert exact == want
            checks += 1
counts['mixed_support_matching_formula_checks'] = checks

# Exact baseline-interval checks for the hybrid theorem with arbitrary rational
# scales. The proof itself uses only |b/a|, and applies to real scales as well.
checks = 0
for r in range(2, 6):
    for D in range(r, 13):
        for aa in [Fraction(-2), Fraction(-1, 3), Fraction(1), Fraction(3, 2)]:
            for bb in [Fraction(-3), Fraction(-1, 2), Fraction(0), Fraction(2, 3), Fraction(2)]:
                live = [aa*p + bb*q for p in range(r+1) for q in range(r+1)]
                all_levels = sorted(set(aa*u+v for u in range(D-r+1) for v in live))
                thresholds = set(all_levels)
                thresholds.update((x+y)/2 for x, y in zip(all_levels, all_levels[1:]))
                width = r * (abs(aa)+abs(bb)) / abs(aa)
                bound = width.numerator // width.denominator + 1
                for threshold in thresholds:
                    bad = 0
                    for u in range(D-r+1):
                        actual = len({aa*u+v >= threshold for v in live}) > 1
                        assert actual == (aa*u+min(live) < threshold <= aa*u+max(live))
                        bad += actual
                    assert bad <= bound
                    checks += 1
counts['hybrid_bad_baseline_checks'] = checks

checks = 0
for d in range(3, 13):
    for e in range(2, 13):
        for r in range(2, min(d-1, e)+1):
            K = d + 2*e
            baselines = {p + 2*q for p in range(d-r+1) for q in range(e-r+1)}
            assert baselines == set(range(K-3*r+1))
            for baseline in baselines:
                assert baseline + 3*r <= K
                checks += 1
counts['hybrid_integer_interval_embeddings'] = checks

(OUT / 'checks.json').write_text(json.dumps(dict(authors='Christian Reitwiessner',
                                               status='VERIFIED', **counts), indent=2) + '\n')
print(json.dumps(counts, indent=2))
