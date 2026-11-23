# Copyright (c) 2026 Christian Reitwiessner. All rights reserved.
# Authors: Christian Reitwiessner
"""Finite guardrail computations, not proofs of asymptotic results.

Uses only the Python standard library. Run: python3 verify_claims.py
"""
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path


def entropy(p):
    return -sum(float(x) * math.log2(float(x)) for x in p if x)


def check_source_rank():
    cases = 0
    for k, m in [(1, 3), (2, 3), (3, 2)]:
        M = k * m
        for live_mask in range(1 << M):
            live = [i for i in range(M) if live_mask >> i & 1]
            d = len({i // m for i in live})
            counts = {}
            for assignment in range(1 << len(live)):
                address = 0
                for j, position in enumerate(live):
                    address ^= ((assignment >> j) & 1) << (position // m)
                counts[address] = counts.get(address, 0) + 1
            assert len(counts) == 1 << d
            assert set(counts.values()) == {1 << (len(live) - d)}
            cases += 1
    return cases


def check_all_small_sources():
    # Every nonempty flat source on three table bits.
    N, cases, worst_slack = 3, 0, 1.0
    for mask in range(1, 1 << (1 << N)):
        support = [x for x in range(1 << N) if mask >> x & 1]
        deficiency = N - math.log2(len(support))
        distance = sum(abs(Fraction(sum((x >> i) & 1 for x in support), len(support))
                           - Fraction(1, 2)) for i in range(N)) / N
        rhs_squared = math.log(2) * deficiency / (2 * N)
        slack = rhs_squared - float(distance * distance)
        assert slack >= -1e-12
        worst_slack = min(worst_slack, slack)
        cases += 1
    return cases, worst_slack


def check_compressed_address():
    # k=m=2: each of four parity fibers contains four raw addresses.
    # A binary feature is fully characterized, for this experiment, by
    # how many of each fiber's four points map to zero. All 5^4 patterns
    # are realizable, and the calculation enumerates all 16 random tables.
    N, fiber_size = 4, 4
    patterns, largest = 0, Fraction(0)
    for counts0 in itertools.product(range(fiber_size + 1), repeat=N):
        counts1 = [fiber_size - v for v in counts0]
        nonempty = sum(sum(v) > 0 for v in [counts0, counts1])
        numerator = 0
        for x in range(1 << N):
            signs = [1 if x >> i & 1 else -1 for i in range(N)]
            numerator += sum(abs(sum(v[i] * signs[i] for i in range(N)))
                             for v in [counts0, counts1])
        advantage = Fraction(numerator, 2 * (N * fiber_size) * (1 << N))
        assert advantage ** 2 <= Fraction(nonempty, 4 * N)
        largest = max(largest, advantage)
        patterns += 1
    return patterns, str(largest)


def check_random_access_leakage():
    # Exhaustive binary transcripts T on all eight tables of length three.
    N, cases = 3, 0
    for mask in range(1 << (1 << N)):
        cells = [[x for x in range(1 << N) if ((mask >> x) & 1) == t]
                 for t in range(2)]
        information = entropy([Fraction(len(v), 1 << N) for v in cells])
        errors = 0
        for cell in cells:
            for i in range(N):
                ones = sum((x >> i) & 1 for x in cell)
                errors += min(ones, len(cell) - ones)
        error = Fraction(errors, N * (1 << N))
        lower = N * (1 - entropy([error, 1 - error]))
        assert information + 1e-12 >= lower
        cases += 1
    return cases


def check_one_coordinate_circuit():
    cases = 0
    for k, m in [(1, 3), (2, 2), (3, 2)]:
        for c in range(1 << k):
            for raw in range(1 << (k * m)):
                b, equality_sum = 0, 0
                for i in range(k):
                    count = sum((raw >> (i * m + j)) & 1 for j in range(m))
                    b |= (count & 1) << i
                    desired = (c >> i) & 1
                    f = lambda s: int((s & 1) == desired)
                    equality_sum += f(0) + sum((f(r) - f(r - 1)) * (count >= r)
                                              for r in range(1, m + 1))
                for xc in (0, 1):
                    output = int(equality_sum + xc >= k + 1)
                    assert output == int(xc == 1 and b == c)
                    cases += 1
    return cases


def main():
    report = {
        "Authors": "Christian Reitwiessner",
        "copyright": "Copyright (c) 2026 Christian Reitwiessner. All rights reserved.",
        "status": "finite computations; universal proofs are in report.md",
        "coordinate_source_rank_cases": check_source_rank(),
        "flat_source_index_bound": check_all_small_sources(),
        "binary_address_feature_patterns_and_max_advantage": check_compressed_address(),
        "binary_table_transcripts": check_random_access_leakage(),
        "one_coordinate_staircase_cases": check_one_coordinate_circuit(),
    }
    target = Path(__file__).with_name("verification.json")
    target.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
