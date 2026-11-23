# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Finite falsification tests for the proposed unmasked approximation proof.

All identities use exact integers. These tests supplement the all-size proof.
Outputs are confined to the directory containing this script.
"""
from itertools import product
from math import comb, exp
from pathlib import Path
import json


def sign(u):
    return -1 if u % 2 else 1


def phi(u):
    return sign(u) * u


def truncated(u, radius):
    return phi(u) if abs(u) <= radius else 0


def compiled(u, radius):
    return sum((truncated(t, radius) - truncated(t - 1, radius))
               * (u >= t) for t in range(-radius, radius + 2))


counts = {"odd_pair_moments": 0, "table_involutions": 0,
          "conditional_error_moments": 0, "full_score_inputs": 0,
          "compiled_values": 0, "average_tail_bounds": 0,
          "majority_agreement_cases": 0}

for radius in range(1, 12):
    for u in range(-30, 31):
        assert compiled(u, radius) == truncated(u, radius)
        counts["compiled_values"] += 1

for k in range(1, 4):
    N = 1 << k
    tables = list(product((-1, 1), repeat=N))
    H = [[sign((s & c).bit_count()) for c in range(N)]
         for s in range(N)]
    coefficients = [[sum(h * v for h, v in zip(row, table))
                     for row in H] for table in tables]
    for s in range(N):
        for t in range(s):
            u = next(u for u in range(N)
                     if ((s ^ t) & u).bit_count() % 2)
            for table, X in zip(tables, coefficients):
                transformed = [sign((t & u).bit_count()) * table[c ^ u]
                               for c in range(N)]
                assert sum(h * v for h, v in zip(H[s], transformed)) == -X[s]
                assert sum(h * v for h, v in zip(H[t], transformed)) == X[t]
                counts["table_involutions"] += 1
            for radius in (1, 2, 3, 5):
                # The second factor is deliberately not odd.
                assert sum(truncated(X[s], radius) * (X[t] + 2) ** 4
                           for X in coefficients) == 0
                counts["odd_pair_moments"] += 1
    for m in (1, 2, 3):
        for r in range(k + 1):
            q = 1 << r
            active = range(1, q)
            v = N + r * m / 4
            for radius in (1, 2, 3, 5, 8):
                total_squared = 0
                total_vote_correct = 0
                for block_counts in product(range(m + 1), repeat=k):
                    multiplicity = 1
                    b = 0
                    for i, c in enumerate(block_counts):
                        multiplicity *= comb(m, c)
                        b |= (c % 2) << i
                    t = [sum(c for i, c in enumerate(block_counts)
                             if s & (1 << i)) for s in range(q)]
                    d = [t[s] - (m * s.bit_count()) // 2 for s in range(q)]
                    eta = [sign((m * s.bit_count()) // 2) for s in range(q)]
                    cross = {(s, j): 0 for s in active for j in range(1, s)}
                    sum_square, sum_diagonal = 0, 0
                    for table, X in zip(tables, coefficients):
                        exact = 2 * sum(X[s] * sign(t[s]) for s in range(q))
                        cell = sum(table[c] for c in range(N)
                                   if (c & (q - 1)) == (b & (q - 1)))
                        assert exact == 2 * q * cell
                        errors = [0] + [eta[s] * (
                            truncated(X[s] + d[s], radius)
                            + truncated(X[s] - d[s], radius))
                            - 2 * X[s] * sign(t[s]) for s in active]
                        for s in active:
                            assert eta[s] * (phi(X[s] + d[s])
                                             + phi(X[s] - d[s])) == 2 * X[s] * sign(t[s])
                        error = sum(errors)
                        approx = exact + error
                        threshold = 0 if q == N else 2 * q
                        vote = -exact >= threshold
                        output = -approx >= threshold
                        if vote != output:
                            assert abs(error) >= 2 * q
                        total_vote_correct += multiplicity * (vote == (table[b] < 0))
                        sum_square += error ** 2
                        sum_diagonal += sum(e ** 2 for e in errors)
                        for s, j in cross:
                            cross[s, j] += errors[s] * errors[j]
                        counts["full_score_inputs"] += 1
                    assert all(value == 0 for value in cross.values())
                    assert sum_square == sum_diagonal
                    counts["conditional_error_moments"] += len(cross) + 1
                    total_squared += multiplicity * sum_square
                input_count = (1 << N) * (1 << (k * m))
                L = N // q
                if L == 1:
                    assert total_vote_correct == input_count
                else:
                    # Avoid rounding the exact central-binomial advantage.
                    assert (2 * total_vote_correct - input_count) * (1 << L) == input_count * comb(L, L // 2)
                counts["majority_agreement_cases"] += 1
                bound = 64 * (q - 1) * v * exp(-radius ** 2 / (16 * v))
                assert total_squared / input_count <= bound + 1e-12
                counts["average_tail_bounds"] += 1

# Parent integration check: build actual raw-input bottom gates and the
# common affine top score, then compare against the numerical construction.
counts["raw_gate_score_inputs"] = 0
for k, m in ((1, 2), (2, 1), (2, 2)):
    N = 1 << k
    for r in range(k + 1):
        q = 1 << r
        for radius in (1, 3, N + k * m):
            gates = []
            for S in range(1, q):
                table_weights = [-2 * sign((S & c).bit_count()) for c in range(N)]
                center = m * S.bit_count() // 2
                eta = sign(center)
                for direction in (-1, 1):
                    address_weights = [direction * bool(S & (1 << i))
                                       for i in range(k) for j in range(m)]
                    for level in range(-radius, radius + 2):
                        weight = eta * (truncated(level, radius)
                                        - truncated(level - 1, radius))
                        if weight:
                            gates.append((table_weights + address_weights,
                                          level + direction * center, weight))
            for point in product((0, 1), repeat=N + k * m):
                x, a = point[:N], point[N:]
                score = 2 * N - 4 * sum(x) + sum(
                    weight for coefficients, threshold, weight in gates
                    if sum(w * bit for w, bit in zip(coefficients, point)) >= threshold)
                expected = 2 * sum(1 - 2 * bit for bit in x)
                b = sum((sum(a[i*m:(i+1)*m]) % 2) << i for i in range(k))
                for S in range(1, q):
                    X = sum(sign((S & c).bit_count()) * (1 - 2*x[c]) for c in range(N))
                    center = m * S.bit_count() // 2
                    D = sum(a[i*m+j] for i in range(k) if S & (1 << i) for j in range(m)) - center
                    expected += sign(center) * (truncated(X + D, radius)
                                                 + truncated(X - D, radius))
                assert score == expected
                if radius == N + k * m and q == N:
                    assert (-score >= 0) == x[b]
                counts["raw_gate_score_inputs"] += 1

result = {"Authors": "Christian Reitwiessner", "status": "passed", **counts}
Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
