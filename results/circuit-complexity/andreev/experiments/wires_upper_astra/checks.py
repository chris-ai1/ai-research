#!/usr/bin/env python3
"""Exact raw-circuit and geometric checks for report.md.

Authors: Christian Reitwiessner
No external dependencies. Finite checks do not prove asymptotic claims.
"""
from itertools import product
from fractions import Fraction
from math import comb
from pathlib import Path
import hashlib
import json
import random

ROOT = Path(__file__).resolve().parent


def cube(d):
    return product((0, 1), repeat=d)


def phi(t):
    return (-1 if t % 2 else 1) * t


def evaluate(g, z):
    w, theta, coefficient = g
    return int(sum(a * b for a, b in zip(w, z)) >= theta)


def carrier(k, m, table_coeffs, T, scale):
    N, M = 1 << k, k * m
    K = sum(c != 0 for c in table_coeffs)
    d = m * T.bit_count()
    w = [-2 * c for c in table_coeffs]
    w += [int(bool(T & (1 << i))) for i in range(k) for _ in range(m)]
    gates = []
    for h in range(-K + 1, K + d + 1):
        top = scale * (-1 if K % 2 else 1) * (phi(h) - phi(h - 1))
        gates.append((tuple(w), h - sum(table_coeffs), top))
    return -scale * K, gates


def chunk_circuit(k, m, p):
    N, M, B, K, r = 1 << k, k * m, 1 << p, 1 << (k - p), k - p
    bias = N
    raw = [-2] * N + [0] * M
    main, correction = [], []
    for T in range(1, N):
        U, S = T & (B - 1), T >> p
        for u in range(B):
            coeffs = [0] * N
            for v in range(K):
                coeffs[u + (v << p)] = (-1) ** ((S & v).bit_count())
            scale = (-1) ** ((U & u).bit_count())
            b, gs = carrier(k, m, coeffs, T, scale)
            bias += b
            main.extend(gs)
    for S in range(1, K):
        T = S << p
        aw = [int(bool(T & (1 << i))) for i in range(k) for _ in range(m)]
        for h in range(1, sum(aw) + 1):
            correction.append((tuple([0] * N + aw), h, -B * (phi(h) - phi(h - 1))))
    predicted_main = (2 * N * K * (N - 1) + Fraction(3, 2) * M * N * N
                      + Fraction(m * m * k * (k + 1) * N * N, 4 * K))
    predicted_corr = Fraction(m * m * r * (r + 1) * K, 4)
    expected_s = 2 * N * (N - 1) + Fraction(B * M * N, 2) + Fraction(m * r * K, 2)
    actual_main = sum(sum(w != 0 for w in g[0]) for g in main)
    actual_corr = sum(sum(w != 0 for w in g[0]) for g in correction)
    assert actual_main == predicted_main and actual_corr == predicted_corr
    assert len(main) + len(correction) == expected_s
    return bias, raw, main + correction, len(main), actual_main, actual_corr


def check_chunks():
    circuits = inputs = semantic_witnesses = 0
    records = []
    for k, m in [(1, 1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 1)]:
        N, M = 1 << k, k * m
        for p in range(k + 1):
            bias, raw, gates, main_count, wm, wc = chunk_circuit(k, m, p)
            for z in cube(N + M):
                label = sum((sum(z[N + i * m:N + (i + 1) * m]) % 2) << i for i in range(k))
                score = bias + sum(w * b for w, b in zip(raw, z))
                score += sum(g[2] * evaluate(g, z) for g in gates)
                assert score == N * (1 - 2 * z[label])
                inputs += 1
            if m >= 2:
                for g in gates[:main_count]:
                    support = [i for i, w in enumerate(g[0]) if w]
                    for i in support:
                        others = [j for j in support if j != i]
                        found = False
                        for a in cube(len(others)):
                            z = [0] * (N + M)
                            for j, b in zip(others, a):
                                z[j] = b
                            v0 = evaluate(g, z)
                            z[i] = 1
                            if evaluate(g, z) != v0:
                                found = True
                                break
                        assert found
                        semantic_witnesses += 1
            records.append(dict(k=k, m=m, prefix_bits=p, bottoms=len(gates),
                                main_input_wires=wm, correction_input_wires=wc,
                                total_support_wires=wm + wc + len(gates) + N))
            circuits += 1
    for k in range(1, 12):
        N = 1 << k
        for m in (1, 2, 5, N // k):
            M = k * m
            for p in range(k + 1):
                B, K, r = 1 << p, 1 << (k - p), k - p
                wm = B * sum((2 * K + m * T.bit_count()) * (K + m * T.bit_count())
                             for T in range(1, N))
                assert wm == 2 * N * K * (N - 1) + Fraction(3, 2) * M * N ** 2 + Fraction(m * m * k * (k + 1) * N ** 2, 4 * K)
                assert wm >= Fraction(3, 2) * M * N ** 2
    return dict(circuits=circuits, all_independent_inputs=inputs,
                semantic_coordinate_witnesses=semantic_witnesses, records=records)


def check_haar():
    coefficient_rows = reconstruction_inputs = 0
    for k in range(1, 7):
        N = 1 << k
        # Exact coefficients of every independent table sign at each address.
        for b in range(N):
            for c in range(N):
                value = Fraction(1, N)
                for p in range(k):
                    mask = (1 << p) - 1
                    if (b & mask) == (c & mask):
                        value += Fraction((-1) ** (((b >> p) & 1) + ((c >> p) & 1)), N >> p)
                assert value == int(b == c)
                coefficient_rows += 1
        if k <= 3:
            for x in cube(N):
                y = [1 - 2 * a for a in x]
                for b in range(N):
                    score = sum(y)
                    for p in range(k):
                        for u in range(1 << p):
                            H = sum((-1) ** ((c >> p) & 1) * y[c] for c in range(N)
                                    if c & ((1 << p) - 1) == u)
                            for U in range(1 << p):
                                score += (-1) ** ((U & u).bit_count() + ((U | (1 << p)) & b).bit_count()) * H
                    assert score == N * y[b]
                    reconstruction_inputs += 1
        for m in (1, 2, 5):
            p = k - 1
            lower = (1 << p) * sum((m * (U.bit_count() + 1)) ** 2 for U in range(1 << p))
            assert lower == Fraction(N * N * m * m * k * (k + 3), 16)
    return dict(all_table_coefficient_checks=coefficient_rows,
                explicit_table_address_checks=reconstruction_inputs)


def check_guards():
    rng = random.Random(20261111)
    input_checks = paired_signs = full_scores = 0
    for d in range(1, 8):
        zs = list(cube(d))
        for trial in range(100):
            lw = [rng.randrange(-3, 4) for _ in range(d)]
            lb = rng.randrange(-4, 5)
            L = [lb + sum(w * b for w, b in zip(lw, z)) for z in zs]
            if not any(L):
                continue
            qw = [rng.randrange(-4, 5) for _ in range(d)]
            qb = rng.randrange(-5, 6)
            Q = [qb + sum(w * b for w, b in zip(qw, z)) for z in zs]
            D = 1 + max(abs(q) for q in Q)
            for z, l, q in zip(zs, L, Q):
                lhs = int(l == 0) * int(q >= 0)
                rhs = int(D * l + q >= 0) - int(l > 0)
                assert lhs == rhs
                input_checks += 1
                for x in (0, 1):
                    y = 1 - 2 * x
                    assert int(l == 0) * y == int(2 * l + y >= 0) - int(2 * l - y >= 0)
                    paired_signs += 1
                F = 3 + sum((i - 2) * b for i, b in enumerate(z)) - 7 * int(q >= 0)
                compiled = 3 * (int(l >= 0) - int(l > 0))
                for i, b in enumerate(z):
                    compiled += (i - 2) * (int(2 * l + 2 * b - 1 >= 0) - int(l > 0))
                compiled -= 7 * rhs
                assert compiled == int(l == 0) * F
                full_scores += 1
    return dict(gated_threshold_inputs=input_checks,
                paired_table_sign_inputs=paired_signs, gated_entire_scores=full_scores)


def check_midpoints():
    forms = monochromatic = 0
    for k in (2, 3):
        for m in range(1, 6):
            vectors = list(product(range(m + 1), repeat=k))
            for weights in product(range(1, 8), repeat=k):
                levels = {}
                for s in vectors:
                    value = sum(w * a for w, a in zip(weights, s))
                    levels.setdefault(value, []).append(s)
                for rows in levels.values():
                    colors = {tuple(a % 2 for a in s) for s in rows}
                    if len(colors) == 1:
                        assert len(rows) == 1
                        monochromatic += 1
                forms += 1
    # The count-grid proof must NOT be extrapolated to unequal coefficients.
    weights = [1, 3, 2, 2]
    points = [z for z in cube(4) if sum(a * b for a, b in zip(weights, z)) == 4]
    assert len(points) == 2
    assert {(sum(z[:2]) % 2, sum(z[2:]) % 2) for z in points} == {(0, 0)}
    assert {(sum(z[:2]), sum(z[2:])) for z in points} == {(0, 2), (2, 0)}
    return dict(blockwise_forms=forms, monochromatic_levels=monochromatic,
                heterogeneous_scope_counterexample=points)


def mul(a, b, r):
    modulus = {1: 0b11, 2: 0b111, 3: 0b1011}[r]
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & (1 << r):
            a ^= modulus
    return result


def check_affine_plane():
    entries = 0
    rows = []
    for r in (1, 2, 3):
        q, N = 1 << r, 1 << (2 * r)
        points = list(product(range(q), repeat=2))
        lines = [{(x, mul(a, x, r) ^ b) for x in range(q)}
                 for a in range(q) for b in range(q)]
        lines += [{(b, y) for y in range(q)} for b in range(q)]
        assert len(lines) == q * q + q
        for b in points:
            active = [line for line in lines if b in line]
            assert len(active) == q + 1
            for c in points:
                assert sum(c in line for line in active) - 1 == q * int(b == c)
                entries += 1
        rows.append(dict(q=q, points=N, lines=len(lines), table_support_per_line=q))
    return dict(exact_all_table_coefficient_checks=entries, geometries=rows)


def main():
    results = {}
    for name, function in [('prefix_chunk_compiler', check_chunks),
                           ('haar_decoder', check_haar), ('affine_guard_compiler', check_guards),
                           ('monochromatic_midpoint_bound', check_midpoints),
                           ('affine_plane_decoder', check_affine_plane)]:
        results[name] = function()
        print(name + ': passed', flush=True)
    payload = dict(Authors='Christian Reitwiessner', status='all exact checks passed',
                   script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   results=results)
    (ROOT / 'checks.json').write_text(json.dumps(payload, indent=2) + '\n')


if __name__ == '__main__':
    main()
