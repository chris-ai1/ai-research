#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Construct and exactly check a paired dual with unequal, varying supports."""

from collections import Counter
from itertools import product
from pathlib import Path
import json
import random


def main():
    rng = random.Random(19731111)
    d, size = 10, 32
    histogram = [0, 0, 1, 1, 1, 1, 3, 3, 3, 3]
    gates = []
    for _ in range(size):
        halves = []
        for _ in range(2):
            values = histogram[:]
            rng.shuffle(values)
            halves.append([w * rng.choice((-1, 1)) for w in values])
        assert Counter(map(abs, halves[0])) == Counter(map(abs, halves[1]))
        gates.append({"u": halves[0], "v": halves[1],
                      "table_weights": [rng.choice((-3, -2, -1, 1, 2, 3))
                                        for _ in range(4)],
                      "threshold": rng.randrange(-12, 13)})
    for attempt in range(1, 100001):
        matching = list(range(d))
        rng.shuffle(matching)
        signs = [rng.choice((-1, 1)) for _ in range(d)]
        live = [[g["u"][i] + signs[i] * g["v"][matching[i]] for i in range(d)]
                for g in gates]
        if all(0 in row for row in live):
            break
    else:
        raise AssertionError("The deterministic finite search found no dual.")

    # k=2 character table: x_b=1 iff the first address-block parity is even.
    table = [1, 1, 0, 0]  # labels 00,01,10,11
    sums = [0] * (1 + 4 + 2 * d + size)
    for z in product((-1, 1), repeat=d):
        w = [0] * d
        for i in range(d):
            w[matching[i]] = signs[i] * z[i]
        address_bits = [(1 - t) // 2 for t in (*z, *w)]
        label = (-1) ** sum(address_bits[:d])
        assert label == 2 * table[2 * (sum(address_bits[:d]) % 2)
                                    + sum(address_bits[d:]) % 2] - 1
        outputs = []
        for g in gates:
            score = (sum(a * x for a, x in zip(g["table_weights"], table))
                     + sum(a * x for a, x in zip(g["u"], z))
                     + sum(a * x for a, x in zip(g["v"], w)))
            outputs.append(int(score >= g["threshold"]))
        features = [1, *table, *address_bits, *outputs]
        sums = [total + label * value for total, value in zip(sums, features)]
    assert all(total == 0 for total in sums), sums
    certificate = {
        "Authors": "Christian Reitwiessner",
        "status": "VERIFIED exact nonnegative dual on 1024 inputs",
        "selected_dimension": d, "bottom_count": size,
        "table": table, "address_coordinates": "signs z,w; bits=(1-sign)/2",
        "histogram_per_half": histogram, "gates": gates,
        "matching": matching, "identification_signs": signs,
        "missing_live_coordinates": [[i for i, x in enumerate(row) if x == 0]
                                     for row in live],
        "uniform_mass_per_point": "1/1024",
        "all_labelled_feature_sums": sums,
        "search_attempts": attempt,
        "note": "Missing-live-coordinate proof holds for all thresholds and table normals."
    }
    Path(__file__).with_name("paired_dual_certificate.json").write_text(
        json.dumps(certificate, indent=2) + "\n")
    print(json.dumps({"status": certificate["status"], "gates": size,
                      "feature_equations": len(sums), "search_attempts": attempt}))


if __name__ == "__main__":
    main()
