#!/usr/bin/env python3
# Authors: Christian Reitwiessner
# Exact finite checks of the UP2 report; no asymptotic claims inferred from tests.

import itertools
import json
import math
import random
from collections import Counter, defaultdict
from functools import cmp_to_key
from pathlib import Path

RNG = random.Random(20261111)
OUT = Path('/tmp/andreev_gap/swarm/up2/checks.json')


def angular_cmp(a, b):
    def half(v):
        return 0 if v[1] > 0 or (v[1] == 0 and v[0] >= 0) else 1
    ha, hb = half(a), half(b)
    if ha != hb:
        return -1 if ha < hb else 1
    cross = a[0] * b[1] - a[1] * b[0]
    return -1 if cross > 0 else (1 if cross < 0 else 0)


def runs(weights):
    signs = [1 if w > 0 else -1 for w in weights if w]
    return 1 + sum(a != b for a, b in zip(signs, signs[1:]))


def maximum_split(blocks):
    # Integer thresholds suffice for integer weights; each split interval is (lo,hi].
    k, m = len(blocks), len(blocks[0])
    prefixes = [[0] + list(itertools.accumulate(w)) for w in blocks]
    events = Counter()
    for q in itertools.product(range(m), repeat=k):
        base = sum(prefixes[i][q[i]] for i in range(k))
        steps = [blocks[i][q[i]] for i in range(k)]
        lo = base + sum(min(0, w) for w in steps)
        hi = base + sum(max(0, w) for w in steps)
        if lo < hi:
            events[lo + 1] += 1
            events[hi + 1] -= 1
    active = best = 0
    for t in sorted(events):
        active += events[t]
        best = max(best, active)
    return best


def check_rank_two():
    count = split_count = 0
    max_runs = 0
    for k, m in [(2, 3), (2, 6), (2, 9), (3, 4), (3, 6)]:
        for _ in range(30):
            vectors = []
            for i in range(k):
                points = [(RNG.randint(-8, 8), RNG.randint(-8, 8)) for _ in range(m)]
                nonzero = sorted([p for p in points if p != (0, 0)], key=cmp_to_key(angular_cmp))
                vectors.append(nonzero + [(0, 0)] * points.count((0, 0)))
            for j in range(8):
                rows = []
                for points in vectors:
                    u, v = RNG.randint(-20, 20), RNG.randint(-20, 20)
                    row = [u * p + v * q for p, q in points]
                    r = runs(row)
                    assert r <= 3, (points, u, v, row)
                    max_runs = max(max_runs, r)
                    rows.append(row)
                    count += 1
                actual = maximum_split(rows)
                bound = m ** k - math.prod(m - runs(row) for row in rows)
                assert actual <= bound, (rows, actual, bound)
                split_count += 1
    return {'angular_rows': count, 'split_sweeps': split_count, 'maximum_runs_seen': max_runs}


def check_polynomial():
    count = 0
    for d in range(7):
        for _ in range(200):
            t = sorted(RNG.randint(-20, 20) for _ in range(30))
            coeff = [RNG.randint(-20, 20) for _ in range(d + 1)]
            row = [sum(c * x ** j for j, c in enumerate(coeff)) * RNG.randint(1, 50) for x in t]
            assert runs(row) <= d + 1
            count += 1
    return count


def check_register_cells():
    count = fixed_points = 0
    for N in [2, 4, 8]:
        for _ in range(80):
            S = RNG.randint(1, 8)
            alpha = [RNG.randint(-15, 15) for _ in range(N)]
            q = [RNG.randint(-5, 5) for _ in range(S)]
            # These arbitrary per-label shifts relax the raw-address halfspace constraint.
            shift = [[RNG.randint(-20, 20) for _ in range(N)] for j in range(S)]
            beta = [RNG.randint(-4, 4) for _ in range(N)]
            top = [RNG.randint(-5, 5) for _ in range(S)]
            offsets = [RNG.randint(-10, 10) for _ in range(N)]
            cells = defaultdict(list)
            for x in itertools.product([0, 1], repeat=N):
                scalar = sum(a * z for a, z in zip(alpha, x))
                pattern = tuple(tuple(int(q[j] * scalar + shift[j][b] >= 0) for j in range(S)) for b in range(N))
                cells[pattern].append(x)
            assert len(cells) <= N * S + 1
            for pattern, tables in cells.items():
                self_tables = []
                output_patterns = set()
                for x in tables:
                    c = sum(a * z for a, z in zip(beta, x))
                    output = tuple(int(c + offsets[b] + sum(v * h for v, h in zip(top, pattern[b])) >= 0) for b in range(N))
                    output_patterns.add(output)
                    if output == x:
                        self_tables.append(x)
                assert len(output_patterns) <= N + 1
                for u, v in itertools.combinations(output_patterns, 2):
                    assert all(a <= b for a, b in zip(u, v)) or all(b <= a for a, b in zip(u, v))
                assert sum(sum(x) == N // 2 for x in self_tables) <= 1
                fixed_points += len(self_tables)
                count += 1
    return {'cells_checked': count, 'self_consistent_tables_seen': fixed_points}


def check_dense_pairs():
    count = 0
    for N in [2, 4, 8]:
        for eta in itertools.product([-1, 1], repeat=N):
            for W in [1, 3]:
                for t in range(-W - 1, W + 2):
                    for c in range(N):
                        actual = int(t + W * eta[c] >= 0)
                        reconstructed = int(t >= W) + ((1 + eta[c]) // 2) * int(-W <= t < W)
                        assert actual == reconstructed
                        count += 1
    return count


def check_symmetric_spectral_bound():
    count = 0
    examples = []
    for M in range(2, 19):
        for d in range(1, M + 1):
            largest = 0
            for r in range(M + 2):
                numerator = sum((-1) ** s * math.comb(d, s) * math.comb(M - d, t)
                                for s in range(d + 1) for t in range(M - d + 1) if s + t >= r)
                assert 4 * math.comb(M, d) * numerator ** 2 <= 2 ** (2 * M)
                largest = max(largest, abs(numerator))
                count += 1
            if M % 4 == 0 and d == M // 2:
                examples.append({'M': M, 'd': d, 'max_coefficient_numerator': largest,
                                 'denominator': 2 ** M, 'orbit_size': math.comb(M, d)})
    return {'threshold_degree_cases': count, 'middle_degree_examples': examples}


def check_character_restriction():
    count = 0
    for k, m in [(2, 2), (2, 3), (3, 2)]:
        N, M = 2 ** k, k * m
        for T in range(1, N):
            d = T.bit_count() * m
            for _ in range(20):
                alpha = [RNG.randint(-6, 6) for _ in range(N)]
                sigma = [RNG.choice([-1, 1]) for _ in range(M)]
                theta = RNG.randint(-8, 8)
                numerator = 0
                for y in [-1, 1]:
                    x = [(1 + y * (-1) ** ((T & c).bit_count())) // 2 for c in range(N)]
                    for a in itertools.product([0, 1], repeat=M):
                        b = sum((sum(a[i * m:(i + 1) * m]) % 2) << i for i in range(k))
                        label = y * (-1) ** ((T & b).bit_count())
                        assert label == 2 * x[b] - 1
                        g = int(sum(u * v for u, v in zip(alpha, x)) + sum(u * v for u, v in zip(sigma, a)) >= theta)
                        numerator += label * g
                denominator = 2 ** (M + 1)
                assert 4 * math.comb(M, d) * numerator ** 2 <= denominator ** 2
                count += 1
    return count



def check_maximal_fourier():
    count = 0
    largest_ratio_numerator = 0
    largest_ratio_denominator = 1
    for M in range(1, 9):
        n = 2 ** M
        signs = [[(-1) ** ((a & B).bit_count()) for B in range(n)] for a in range(n)]
        for trial in range(16):
            if trial < 12:
                w = [RNG.randint(-100, 100) for _ in range(M)]
                order = sorted(range(n), key=lambda a: sum(w[i] for i in range(M) if (a >> i) & 1), reverse=True)
            else:
                order = list(range(n))
                RNG.shuffle(order)
            current = [0] * n
            maxima = [0] * n
            for a in order:
                for B, sign in enumerate(signs[a]):
                    current[B] += sign
                    maxima[B] = max(maxima[B], abs(current[B]))
            total = sum(v * v for v in maxima)
            assert total <= (M + 1) ** 2 * n ** 2
            if total * largest_ratio_denominator > largest_ratio_numerator * n ** 2:
                largest_ratio_numerator = total
                largest_ratio_denominator = n ** 2
            # Each size-d orbit obeys the same total-square budget.
            for d in range(M + 1):
                orbit_total = sum(maxima[B] ** 2 for B in range(n) if B.bit_count() == d)
                assert orbit_total <= (M + 1) ** 2 * n ** 2
            count += 1
    return {'orders_checked': count, 'largest_sum_of_squared_maxima':
            {'numerator': largest_ratio_numerator, 'denominator': largest_ratio_denominator}}



def check_paired_cancellation():
    full_sign_rows = general_rows = correlations = 0
    for d in range(2, 7):
        ts = list(itertools.product([-1, 1], repeat=d))
        for row in itertools.product([-1, 1], repeat=2 * d):
            u, v = row[:d], row[d:]
            survivors = [t for t in ts if all(a + b * c != 0 for a, b, c in zip(u, t, v))]
            assert survivors == [tuple(a * b for a, b in zip(u, v))]
            full_sign_rows += 1
        for _ in range(200):
            u = [RNG.randint(-2, 2) for _ in range(d)]
            v = [RNG.randint(-2, 2) for _ in range(d)]
            survivors = sum(all(a + b * c != 0 for a, b, c in zip(u, t, v)) for t in ts)
            if any(a == b == 0 for a, b in zip(u, v)):
                predicted = 0
            else:
                q = sum(abs(a) == abs(b) and a != 0 for a, b in zip(u, v))
                predicted = 2 ** (d - q)
            assert survivors == predicted
            general_rows += 1
            if d <= 4:
                theta = RNG.randint(-5, 5)
                for t in ts:
                    coeff = [a + b * c for a, b, c in zip(u, t, v)]
                    if 0 in coeff:
                        corr = sum(math.prod(z) * int(sum(a * b for a, b in zip(coeff, z)) >= theta) for z in ts)
                        assert corr == 0
                        correlations += 1
    return {'full_sign_rows': full_sign_rows, 'general_pair_rows': general_rows,
            'missing_variable_parity_correlations': correlations}



def check_full_sign_partial_parity_upper():
    from math import factorial
    inputs = gate_evaluations = 0
    for d in range(2, 6):
        M = 2 * d
        masks = list(itertools.product([-1, 1], repeat=d))
        for a in itertools.product([-1, 1], repeat=M):
            z, w = a[:d], a[d:]
            direct = compiled = 0
            for sigma in masks:
                L = sum(u * v for u, v in zip(sigma, z)) + sum(w)
                factor = math.prod(sigma)
                direct += factor * L ** d
                ladder = (-M) ** d
                for r in range(1, M + 1):
                    level = -M + 2 * r
                    ladder += (level ** d - (level - 2) ** d) * int(L >= level)
                    gate_evaluations += 1
                assert ladder == L ** d
                compiled += factor * ladder
            target = 2 ** d * factorial(d) * math.prod(z)
            assert direct == compiled == target
            inputs += 1
    return {'raw_inputs': inputs, 'raw_bottom_evaluations': gate_evaluations}


def main():
    results = {'authors': 'Christian Reitwiessner', 'seed': 20261111,
               'rank_two': check_rank_two(), 'polynomial_rows': check_polynomial(),
               'rank_one_cells': check_register_cells(), 'dense_pair_identity_cases': check_dense_pairs(),
               'symmetric_spectral': check_symmetric_spectral_bound(),
               'raw_character_restriction_cases': check_character_restriction(),
               'maximal_fourier': check_maximal_fourier(),
               'paired_cancellation': check_paired_cancellation(),
               'partial_parity_upper': check_full_sign_partial_parity_upper(), 'status': 'all passed'}
    OUT.write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
