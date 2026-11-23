#!/usr/bin/env python3
"""Exact finite checks supporting report.md; no external dependencies.

Authors: Christian Reitwiessner
Literature and peer attribution are retained in report.md.
These checks do not replace the asymptotic proofs.
"""

from fractions import Fraction
from itertools import product
from math import comb
from pathlib import Path
import hashlib
import json
import random


ROOT = Path(__file__).resolve().parent
RESULTS = {}


def bits(d):
    return list(product((0, 1), repeat=d))


def sign(x):
    return (x > 0) - (x < 0)


def essential_support(values, d):
    # product order: variable i corresponds to bit d-1-i in the array index.
    return {
        i for i in range(d)
        if any(values[v] != values[v ^ (1 << (d - 1 - i))]
               for v in range(1 << d))
    }


def parity_checks():
    inputs = differences = edge_slices = 0
    for d in range(2, 10):
        def gates(z):
            s = sum(z)
            return [int(s >= 2 * r) for r in range(1, d // 2 + 1)]

        def score(z):
            return 2 * sum(z) - 4 * sum(gates(z)) - 1

        for z in bits(d):
            assert score(z) == 2 * (sum(z) % 2) - 1
            inputs += 1
        for i in range(d):
            remaining = [j for j in range(d) if j != i]
            feature_values = {}
            for y in bits(d - 1):
                z0 = list(y)
                z0.insert(i, 0)
                z1 = list(y)
                z1.insert(i, 1)
                deriv = score(z1) - score(z0)
                assert deriv == 2 * (-1) ** sum(y)
                # The raw top derivative is the constant 2, retaining the
                # SAME original output coefficients in the two restrictions.
                f0, f1 = gates(z0), gates(z1)
                assert deriv == 2 - 4 * sum(b - a for a, b in zip(f0, f1))
                feature_values[y] = f0 + f1
                differences += 1
            for y in bits(d - 1):
                for j in range(len(remaining)):
                    if y[j]:
                        continue
                    y1 = list(y)
                    y1[j] = 1
                    assert feature_values[y] != feature_values[tuple(y1)]
                    edge_slices += 1
        assert (d + 1) * (d // 2) + d == d * (d // 2) + d // 2 + d
    return dict(inputs=inputs, raw_top_safe_differences=differences,
                sliced_derivative_edges=edge_slices)


def phi(r):
    return (-1) ** r * r if r >= 0 else (-1 if r % 2 else 1) * r


def compile_andreev(k, m):
    ntable, maddr = 1 << k, k * m
    circuit = []
    const = 0
    for T in range(1 << k):
        chi = [(-1) ** ((T & c).bit_count()) for c in range(ntable)]
        aw = [int(bool(T & (1 << i))) for i in range(k) for _ in range(m)]
        d = sum(aw)
        const += phi(-ntable)
        for r in range(-ntable + 1, ntable + d + 1):
            circuit.append((tuple([-2 * c for c in chi] + aw),
                            r - sum(chi), phi(r) - phi(r - 1)))
        for r in range(1, d + 1):
            circuit.append((tuple([0] * ntable + aw), r,
                            -(phi(r) - phi(r - 1))))
    return const, circuit


def eval_gate(gate, z):
    w, theta, _ = gate
    return int(sum(wi * zi for wi, zi in zip(w, z)) >= theta)


def andreev_checks():
    cases = [(1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (2, 2), (2, 3), (3, 1)]
    raw_inputs = character_differences = mixed_derivatives = edges = 0
    counts = []
    for k, m in cases:
        N, M = 1 << k, k * m
        const, circuit = compile_andreev(k, m)
        expected_s = 2 * N * N + M * N
        expected_w = (2 * N ** 3 + Fraction(3, 2) * M * N * N
                      + Fraction(1, 2) * m * m * k * (k + 1) * N)
        actual_w = sum(sum(c != 0 for c in g[0]) for g in circuit)
        assert len(circuit) == expected_s
        assert actual_w == expected_w
        for z in bits(N + M):
            label = sum((sum(z[N + i * m:N + (i + 1) * m]) % 2) << i
                        for i in range(k))
            score = const + sum(g[2] * eval_gate(g, z) for g in circuit)
            assert score == N * (1 - 2 * z[label])
            raw_inputs += 1
        for T in range(1, N):
            plus = tuple((1 + (-1) ** ((T & c).bit_count())) // 2 for c in range(N))
            minus = tuple(1 - b for b in plus)
            selected = [i * m + l for i in range(k) if T & (1 << i) for l in range(m)]
            ftables = {}
            for a in bits(M):
                fp = tuple(eval_gate(g, plus + a) for g in circuit)
                fm = tuple(eval_gate(g, minus + a) for g in circuit)
                delta = sum(g[2] * (p - q) for g, p, q in zip(circuit, fp, fm))
                assert delta == -2 * N * (-1) ** sum(a[i] for i in selected)
                ftables[a] = (delta, fp, fm)
                character_differences += 1
            for i in selected:
                others = [j for j in selected if j != i]
                # Fix the ignored coordinates to zero. All selected bits are
                # tested, and each gate supplies the FOUR actual restrictions.
                ds = {}
                feats = {}
                for y in bits(len(others)):
                    a0 = [0] * M
                    for j, b in zip(others, y):
                        a0[j] = b
                    a1 = a0.copy()
                    a1[i] = 1
                    s0, p0, q0 = ftables[tuple(a0)]
                    s1, p1, q1 = ftables[tuple(a1)]
                    ds[y] = s1 - s0
                    assert ds[y] == 4 * N * (-1) ** sum(y)
                    feats[y] = p0 + q0 + p1 + q1
                    mixed_derivatives += 1
                for y in bits(len(others)):
                    for j in range(len(others)):
                        if y[j]:
                            continue
                        y1 = list(y)
                        y1[j] = 1
                        y1 = tuple(y1)
                        assert ds[y] * ds[y1] < 0 and feats[y] != feats[y1]
                        edges += 1
        counts.append(dict(k=k, m=m, bottoms=len(circuit),
                           bottom_input_wires=actual_w,
                           total_support_wires=actual_w + len(circuit)))
    return dict(raw_inputs=raw_inputs, character_differences=character_differences,
                four_restriction_derivatives=mixed_derivatives,
                covered_derivative_edges=edges, circuits=counts)


def semantic_pruning_checks():
    rng = random.Random(20261111)
    tested = removed = nonvacuous = dense_cases = 0
    for k, m in [(2, 1), (2, 2), (3, 1), (3, 2), (4, 1)]:
        M, nt = k * m, 2
        cube = bits(nt + M)
        for trial in range(320):
            magnitudes = [rng.randrange(4) for _ in range(k)]
            aw = [rng.choice((-1, 1)) * magnitudes[i] for i in range(k) for _ in range(m)]
            tw = [rng.randrange(-5, 6) for _ in range(nt)]
            weights = tw + aw
            # Includes threshold ties, half-integer cuts, constants and
            # cases where some entire magnitude class is semantically dead.
            theta2 = rng.randrange(-25, 26)
            values = [int(2 * sum(w * b for w, b in zip(weights, z)) >= theta2) for z in cube]
            ess = essential_support(values, nt + M)
            for mag in set(magnitudes) - {0}:
                relevant = [(nt + i) in ess for i in range(M) if abs(aw[i]) == mag]
                assert len(set(relevant)) == 1
            pruned = [w if i in ess or i < nt else 0 for i, w in enumerate(weights)]
            pvalues = [int(2 * sum(w * b for w, b in zip(pruned, z)) >= theta2) for z in cube]
            assert pvalues == values
            pmag = [abs(pruned[nt + i * m]) for i in range(k)]
            assert len(set(pmag)) <= len(set(magnitudes))
            assert sum(w != 0 for w in pruned[nt:]) == len(ess - set(range(nt)))
            removed += int(pruned != weights)
            nonvacuous += int(bool(ess - set(range(nt))))
            for mask in range(1, (1 << k) - 1):
                side = [i for i in range(k) if mask & (1 << i)]
                other = [i for i in range(k) if not mask & (1 << i)]
                if 3 * len(side) < k or 3 * len(other) < k:
                    continue
                if set(pmag[i] for i in side).isdisjoint(pmag[i] for i in other):
                    assert 3 * len(ess - set(range(nt))) >= M
                    dense_cases += 1
            tested += 1
    return dict(gates=tested, gates_pruned=removed,
                address_dependent_gates=nonvacuous, semantic_middle_cut_checks=dense_cases)


def incidence_checks():
    profiles = middle_density = support_pair_charges = 0
    for k in range(2, 8):
        N = 1 << k
        for mags in product(range(3), repeat=k):
            q = len(set(mags))
            cuts = 0
            for T in range(1, N - 1):
                # One representative from every unordered cut.
                if not T & 1:
                    continue
                selected = {mags[i] for i in range(k) if T & (1 << i)}
                ignored = {mags[i] for i in range(k) if not T & (1 << i)}
                if selected.isdisjoint(ignored):
                    cuts += 1
                    s = T.bit_count()
                    if 3 * s >= k and 3 * (k - s) >= k:
                        assert 3 * sum(a != 0 for a in mags) >= k
                        middle_density += 1
            assert cuts == 2 ** (q - 1) - 1
            profiles += 1
        for m in range(1, 7):
            actual = sum((m * T.bit_count()) * (m * T.bit_count() - 1) for T in range(N))
            expected = Fraction(N, 4) * (m * m * k * (k + 1) - 2 * m * k)
            assert actual == expected
        # Every table bit is in precisely one pair in the i-th pairing.
        if k <= 3:
            for support in range(1 << N):
                t = support.bit_count()
                for i in range(k):
                    touched = sum(bool(support & ((1 << c) | (1 << (c ^ (1 << i)))))
                                  for c in range(N) if not c & (1 << i))
                    assert touched <= t
                    support_pair_charges += 1
    return dict(profiles=profiles, dense_separated_middle_cuts=middle_density,
                table_support_pair_charges=support_pair_charges)


def owner_checks():
    checked = owned_cases = 0
    N = 4
    for alpha in product(range(4), repeat=N):
        total = sum(alpha)
        owners = [c for c in range(N) if 2 * alpha[c] > total]
        assert len(owners) <= 1
        for theta2 in range(-2, 2 * total + 3):
            delta = [int(2 * alpha[c] >= theta2) - int(2 * (total - alpha[c]) >= theta2)
                     for c in range(N)]
            if owners:
                owner = owners[0]
                h = int(2 * (total - alpha[owner]) < theta2 <= 2 * alpha[owner])
                assert delta[owner] == h
                for c in range(N):
                    if c != owner:
                        assert delta[c] <= -h
                owned_cases += 1
            else:
                assert all(d <= 0 for d in delta)
            checked += 1
    return dict(complementary_singleton_slab_cases=checked, owned_cases=owned_cases)


def helper_checks():
    identities = coefficients = essential_edges = 0
    for d in range(3, 35):
        f = [Fraction((-1) ** r * sum(comb(d, u) for u in range(r + 1)),
                      d * comb(d - 1, r)) for r in range(d)]
        for s in range(d + 1):
            value = ((d - s) * f[s] if s < d else 0) + (s * f[s - 1] if s else 0)
            value += (-1) ** d * 2 ** d * int(s == d)
            assert value == (-1) ** s
            identities += 1
        assert d + d * (d - 1) ** 2 == d + d * (d - 1) * (d - 1)
        assert all(f[r] != f[r - 1] for r in range(1, d))
        if d <= 8:
            cube = bits(d)
            for omit in range(d):
                for threshold in range(1, d):
                    vals = [int(sum(z) - z[omit] >= threshold) for z in cube]
                    assert essential_support(vals, d) == set(range(d)) - {omit}
                    essential_edges += d - 1
            # Arbitrary varying strict margins; the point gate has no
            # degree-(d-1) coefficient in this positive literal basis.
            for omit in range(d):
                U = [i for i in range(d) if i != omit]
                coeff = 0
                point_coeff = 0
                for v in bits(d - 1):
                    z = [0] * d
                    for i, b in zip(U, v):
                        z[i] = b
                    margin = 1 + sum((i + 2) * z[i] for i in range(d))
                    sgn = (-1) ** (len(U) - sum(v))
                    coeff += sgn * (-1) ** sum(z) * margin
                    point_coeff += sgn * int(all(z))
                assert sign(coeff) == (-1) ** (d - 1)
                assert point_coeff == 0
                coefficients += 1
    return dict(exact_rational_helper_identities=identities,
                omission_coefficients=coefficients, helper_essential_edges=essential_edges)


def lex_checks():
    checked = threshold_counts = 0
    for d in range(1, 9):
        weights = [3 ** (d - 1 - i) for i in range(d)]
        cube = bits(d)
        vals = [sum(w * b for w, b in zip(weights, z)) for z in cube]
        for theta in sorted({min(vals) - 1, max(vals) + 1} | set(vals) | {v + 1 for v in vals}):
            terms = []

            def walk(i, prefix, value):
                tail = sum(weights[i:])
                if value >= theta:
                    terms.append(prefix)
                    return
                if value + tail < theta or i == d:
                    return
                walk(i + 1, prefix + (0,), value)
                walk(i + 1, prefix + (1,), value + weights[i])

            walk(0, (), 0)
            assert len(terms) <= d
            for z, value in zip(cube, vals):
                compiled = sum(z[:len(t)] == t for t in terms)
                assert compiled == int(value >= theta)
                checked += 1
            threshold_counts += 1
    for q in range(1, 41):
        for s in range(1, q + 1):
            assert Fraction(2 ** s, s) <= Fraction(2 ** q, q)
    return dict(compiled_raw_inputs=checked, thresholds=threshold_counts)


def main():
    for name, check in [
        ("parity", parity_checks), ("andreev", andreev_checks),
        ("semantic_pruning", semantic_pruning_checks),
        ("incidence", incidence_checks), ("monotone_owner", owner_checks),
        ("point_helpers", helper_checks), ("lex_compiler", lex_checks),
    ]:
        RESULTS[name] = check()
        print(name + ": passed", flush=True)
    payload = {
        "Authors": "Christian Reitwiessner",
        "status": "all exact finite checks passed",
        "scope": "Finite algebra/support checks; asymptotic theorems remain written proofs, not formal proofs.",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "results": RESULTS,
    }
    (ROOT / "checks.json").write_text(json.dumps(payload, indent=2) + "\n")


if __name__ == "__main__":
    main()
