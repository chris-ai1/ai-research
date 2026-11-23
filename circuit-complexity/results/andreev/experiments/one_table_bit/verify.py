# Copyright (c) 2026 Christian Reitwiessner. All rights reserved.
# Authors: Christian Reitwiessner
"""Independent integer checks for report.md; Python standard library only."""

import itertools
import json
from pathlib import Path


def bits(v, length):
    return tuple((v >> i) & 1 for i in range(length))


def submasks(c):
    t = c
    while t:
        yield t
        t = (t - 1) & c


def build(k, m):
    """Gate = (block-count weights, table index or None, beta, theta, top)."""
    gates = []
    shared = {}
    for c in range(1, 1 << k):
        for t in submasks(c):
            direction = bits(t, k)
            extent = t.bit_count() * m
            beta = extent + 1
            for r in range(1, extent + 1):
                coefficient = 2 * k ** c.bit_count() * (-1) ** (t.bit_count() + r)
                gates.append((direction, c, beta, r + beta, 2 * coefficient))
                shared[t, r] = shared.get((t, r), 0) - coefficient
    table_gates = len(gates)
    for (t, r), coefficient in shared.items():
        assert coefficient != 0
        gates.append((bits(t, k), None, 0, r, coefficient))
    assert table_gates == k * m * 3 ** (k - 1)
    assert len(gates) == k * m * (3 ** (k - 1) + 2 ** (k - 1))
    return gates, table_gates


def affine_score(k, counts, gates):
    # Raw top term is 2*x_empty - 1. Evaluate each actual gate at x_c=0,1.
    constant = -1
    coefficients = [2] + [0] * ((1 << k) - 1)
    for direction, c, beta, theta, top in gates:
        value = sum(w * s for w, s in zip(direction, counts))
        zero = int(value >= theta)
        constant += top * zero
        if c is not None:
            one = int(value + beta >= theta)
            coefficients[c] += top * (one - zero)
    return constant, coefficients


def check_construction(k, m, raw):
    gates, table_gates = build(k, m)
    if raw:
        addresses = (
            tuple(sum(a[i*m:(i+1)*m]) for i in range(k))
            for a in itertools.product((0, 1), repeat=k*m)
        )
    else:
        # All raw gates were constructed block-symmetric: these are every orbit.
        addresses = itertools.product(range(m + 1), repeat=k)
    checked, min_margin = 0, None
    for counts in addresses:
        b = sum((s % 2) << i for i, s in enumerate(counts))
        constant, coefficients = affine_score(k, counts, gates)
        expected = [(2*k) ** c.bit_count() if (c & b) == c else 0
                    for c in range(1 << k)]
        assert coefficients == [2*v for v in expected]
        assert constant == -sum(expected)
        # Exact worst-case scores over all independent table bits.
        negative_max = constant + sum(max(w, 0) for c, w in enumerate(coefficients) if c != b)
        positive_min = constant + coefficients[b] + sum(min(w, 0) for c, w in enumerate(coefficients) if c != b)
        assert negative_max < 0 < positive_min
        margin = min(-negative_max, positive_min)
        min_margin = margin if min_margin is None else min(min_margin, margin)
        checked += 1
    return dict(k=k, m=m, bottoms=len(gates), table_bottoms=table_gates,
                addresses_or_orbits=checked, raw=raw, minimum_margin=min_margin)


def check_dominance():
    checked = 0
    for w in itertools.product(range(-2, 3), repeat=3):
        for intercept in range(-6, 7):
            for b in range(3):
                exact = all((intercept + sum(t*v for t, v in zip(x, w)) >= 0) == bool(x[b])
                            for x in itertools.product((0, 1), repeat=3))
                off_plus = sum(max(v, 0) for c, v in enumerate(w) if c != b)
                off_minus = sum(min(v, 0) for c, v in enumerate(w) if c != b)
                interval = intercept + off_plus < 0 <= intercept + w[b] + off_minus
                gap2 = w[b] - sum(abs(v) for c, v in enumerate(w) if c != b)
                remainder2 = 2 * intercept + sum(w)
                centered = gap2 > 0 and -gap2 <= remainder2 < gap2
                assert exact == interval == centered
                checked += 1
    return checked


def check_pair_extraction(k, m):
    gates, _ = build(k, m)
    pairs, edges = 0, 0
    for c in range(1 << k):
        for d in range(c + 1, 1 << k):
            relevant = [g for g in gates if g[1] in (c, d)]
            features, signs = {}, {}
            for z in itertools.product((0, 1), repeat=m):
                counts = []
                for i in range(k):
                    if ((c ^ d) >> i) & 1:
                        counts.append(sum(z) + ((1 - 2*z[0]) if ((c >> i) & 1) else 0))
                    else:
                        counts.append((c >> i) & 1)
                _, coeff = affine_score(k, counts, gates)
                difference = coeff[c] - coeff[d]
                assert difference * (1 if sum(z) % 2 == 0 else -1) > 0
                signs[z] = difference
                features[z] = tuple(int(sum(w*s for w, s in zip(g[0], counts)) + g[2]*t >= g[3])
                                    for g in relevant for t in (0, 1))
            for z in features:
                for i in range(m):
                    if z[i] == 0:
                        other = z[:i] + (1,) + z[i+1:]
                        assert signs[z] * signs[other] < 0
                        assert features[z] != features[other]
                        edges += 1
            pairs += 1
    return dict(k=k, m=m, all_label_pairs=pairs, sliced_edges_checked=edges)


def check_two_column(k):
    n = 1 << k
    checked = 0
    for u in range(n):
        for v in range(n):
            c0 = -u
            weights = []
            for c in range(n):
                target = sum((1 << i) * (((c >> i) & 1) + (1 - 2*((c >> i) & 1))*((v >> i) & 1))
                             for i in range(k))
                assert target == v ^ c
                zero = int(u - target >= 1)
                one = int(u - target + 1 >= 1)
                c0 += zero
                weights.append(one - zero)
            assert c0 == 0
            assert weights == [int(c == u ^ v) for c in range(n)]
            checked += 1
    return dict(k=k, m=2, addresses=checked, bottoms=n)


def main():
    result = {
        "Authors": "Christian Reitwiessner",
        "copyright": "Copyright (c) 2026 Christian Reitwiessner. All rights reserved.",
        "status": "Exact integer finite checks; not proofs of imported asymptotic theorems.",
        "dominance_cases": check_dominance(),
        "construction": [],
        "pair_extraction": [],
        "inherited_two_column": [],
    }
    for k, maximum_m in [(1, 8), (2, 5), (3, 4), (4, 4), (5, 3)]:
        for m in range(1, maximum_m + 1):
            result["construction"].append(check_construction(k, m, raw=(k*m <= 12)))
    for k, m in [(2, 3), (3, 3), (4, 2)]:
        result["pair_extraction"].append(check_pair_extraction(k, m))
    for k in range(1, 7):
        result["inherited_two_column"].append(check_two_column(k))
    # Uniform parity is an exact Farkas certificate for coordinate features.
    for m in range(2, 9):
        data = list(itertools.product((0, 1), repeat=m))
        assert sum((-1)**sum(z) for z in data) == 0
        assert all(sum((-1)**sum(z)*z[i] for z in data) == 0 for i in range(m))
    result["coordinate_dictionary_dual_dimensions"] = list(range(2, 9))
    destination = Path(__file__).with_name("verification.json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print("Authors: Christian Reitwiessner")
    print("PASS:", result["dominance_cases"], "dominance cases;",
          len(result["construction"]), "construction instances;")
    print("PASS: pair extraction", result["pair_extraction"])
    print("PASS: exact coordinate-feature LP dual for dimensions 2..8")
    print("PASS: inherited two-column construction for k=1..6")
    print("Saved", destination)


if __name__ == "__main__":
    main()
