#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Exact finite guardrails for LOW1 round two; no asymptotic inference."""

from collections import Counter
from fractions import Fraction
from itertools import permutations, product
from math import comb, factorial
from pathlib import Path
import json
import random


def permanent(matrix):
    n = len(matrix)
    dp = [Fraction(0)] * (1 << n)
    dp[0] = Fraction(1)
    for mask in range(1 << n):
        row = mask.bit_count()
        if row == n:
            continue
        for col in range(n):
            if not (mask >> col) & 1:
                dp[mask | (1 << col)] += dp[mask] * matrix[row][col]
    return dp[-1]


def cancellation_matrix(u, v):
    return [[Fraction(sum(x + t * y != 0 for t in (-1, 1)), 2)
             for y in v] for x in u]


def helper_values(d):
    return [Fraction((-1) ** r * sum(comb(d, h) for h in range(r + 1)),
                     d * comb(d - 1, r)) for r in range(d)]


def helper_gate_score(z):
    d = len(z)
    s = sum(z)
    f = helper_values(d)
    score = d * f[0] + (-1) ** d * 2 ** d * (s == d)
    for i in range(d):
        for r in range(1, d):
            score += (f[r] - f[r - 1]) * (s - z[i] >= r)
    return score


def check_helpers():
    layers = raw = 0
    for d in range(2, 101):
        f = helper_values(d)
        for s in range(d + 1):
            score = ((d - s) * f[s] if s < d else 0)
            score += s * f[s - 1] if s else 0
            score += (-1) ** d * 2 ** d * (s == d)
            assert score == (-1) ** s, (d, s, score)
            layers += 1
    for d in range(2, 10):
        for z in product((0, 1), repeat=d):
            assert helper_gate_score(z) == (-1) ** sum(z)
            raw += 1
    return {"exact_layer_identities": layers, "raw_gate_scores": raw}


def check_cancellation():
    rng = random.Random(20261111)
    cases = restrictions = missing_corr = 0
    for d in range(2, 6):
        for sample in range(10):
            u = [rng.choice((-2, -1, 0, 1, 2)) for _ in range(d)]
            v = [rng.choice((-2, -1, 0, 1, 2)) for _ in range(d)]
            matrix = cancellation_matrix(u, v)
            expected = permanent(matrix) * (2 ** d)
            retained = 0
            for pi in permutations(range(d)):
                for signs in product((-1, 1), repeat=d):
                    row = [u[i] + signs[i] * v[pi[i]] for i in range(d)]
                    full = all(row)
                    retained += full
                    restrictions += 1
                    if not full and sample < 2:
                        threshold = rng.randrange(-3, 4)
                        corr = sum(
                            (-1) ** sum(x < 0 for x in z)
                            * (sum(w * x for w, x in zip(row, z)) >= threshold)
                            for z in product((-1, 1), repeat=d)
                        )
                        assert corr == 0
                        missing_corr += 1
            assert retained == expected, (u, v, retained, expected)
            a, b = Counter(map(abs, u)), Counter(map(abs, v))
            energy = 2 * a[0] * b[0] + sum(a[t] * b[t] for t in a if t)
            deficit = sum(1 - x for row in matrix for x in row)
            assert deficit == Fraction(energy, 2)
            cases += 1
    return {"exact_permanent_survival_cases": cases,
            "literal_restrictions": restrictions,
            "zero_parity_correlations": missing_corr}


def check_one_class():
    checks = 0
    for d in range(2, 31):
        for a in range(d + 1):
            for b in range(d + 1):
                moment = sum(Fraction(comb(b, q) * comb(d - b, a - q),
                                      comb(d, a) * 2 ** q)
                             for q in range(max(0, a - (d - b)), min(a, b) + 1))
                assert moment <= (1 - Fraction(b, 2 * d)) ** a
                checks += 1
    return {"exact_hypergeometric_moment_bounds": checks}


def check_bregman_small():
    # Raise the Brégman inequality to lcm(1,...,d) to avoid floating arithmetic.
    checks = 0
    for d, common_power in ((2, 2), (3, 6), (4, 12)):
        for flat in product((0, 1), repeat=d * d):
            matrix = [flat[i * d:(i + 1) * d] for i in range(d)]
            rows = [sum(row) for row in matrix]
            p = permanent(matrix)
            if not all(rows):
                assert p == 0
            else:
                bound = 1
                for r in rows:
                    bound *= factorial(r) ** (common_power // r)
                assert p ** common_power <= bound
            checks += 1
    return {"exact_binary_bregman_instances": checks}


def check_soft_permanent():
    # A rational variant of the proof: use a fixed rational row-majorant.
    # This independently tests Bernoulli averaging on arbitrary soft matrices.
    checks = 0
    rng = random.Random(11)
    for d in range(2, 5):
        for _ in range(20):
            matrix = [[rng.choice((Fraction(0), Fraction(1, 2), Fraction(1)))
                       for _ in range(d)] for _ in range(d)]
            uncertain = [(i, j) for i in range(d) for j in range(d)
                         if matrix[i][j] == Fraction(1, 2)]
            total = Fraction(0)
            for outcomes in product((0, 1), repeat=len(uncertain)):
                binary = [row[:] for row in matrix]
                for (i, j), bit in zip(uncertain, outcomes):
                    binary[i][j] = bit
                total += permanent(binary)
            assert total / (2 ** len(uncertain)) == permanent(matrix)
            checks += 1
    return {"exact_bernoulli_permanent_averages": checks}


def check_histogram_energy():
    rng = random.Random(7)
    checks = 0
    for d in range(2, 61):
        for q in range(1, min(d, 12) + 1):
            a = Counter(rng.randrange(q) for _ in range(d))
            energy = 2 * a[0] ** 2 + sum(a[t] ** 2 for t in a if t)
            assert energy * q >= d * d
            checks += 1
    return {"exact_balanced_histogram_energy_bounds": checks}


def main():
    result = {"Authors": "Christian Reitwiessner",
              "status": "VERIFIED: exact finite guardrails, not asymptotic evidence"}
    for check in (check_helpers, check_cancellation, check_one_class,
                  check_bregman_small, check_soft_permanent, check_histogram_energy):
        result.update(check())
    path = Path(__file__).with_name("verification.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
