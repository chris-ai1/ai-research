# Copyright (c) 2026 Christian Reitwiessner. All rights reserved.
# Authors: Christian Reitwiessner
"""Exact finite checks for the private-kernel extraction; no asymptotic inference."""
from itertools import product
from fractions import Fraction
import json
from pathlib import Path

out = {"authors": "Christian Reitwiessner", "status": "exact finite checks"}
checks = 0
owners_seen = set()
for n in range(2, 7):
    for alpha in product(range(4), repeat=n):
        total = sum(alpha)
        owners = [c for c in range(n) if 2 * alpha[c] > total]
        assert len(owners) <= 1
        levels = sorted(set([0, total] + list(alpha) + [total-a for a in alpha]))
        thresholds = set(map(Fraction, levels))
        thresholds.update(Fraction(a+b, 2) for a, b in zip(levels, levels[1:]))
        thresholds.update([Fraction(-1), Fraction(total+1)])
        for t in thresholds:
            d = [int(a >= t) - int(total-a >= t) for a in alpha]
            kernels = [0] * n
            if owners:
                c = owners[0]
                h = int(total-alpha[c] < t <= alpha[c])
                kernels[c] = h
                owners_seen.add(c)
                assert d[c] == h
            for c in range(n):
                assert d[c] <= 2*kernels[c] - sum(kernels), (alpha, t, c, d, kernels)
                checks += 1
out["coordinate_inequalities"] = checks
out["owner_indices_checked"] = sorted(owners_seen)

# For an owned gate, replacing it by g'(x_c) keeps precisely its owner slab.
conversion_checks = 0
for n in range(2, 5):
    for alpha in product(range(4), repeat=n):
        total = sum(alpha)
        for c in range(n):
            if 2*alpha[c] <= total:
                continue
            delta = 2*alpha[c]-total
            for twice_t in range(-2, 2*total+3):
                t = Fraction(twice_t, 2)
                h = int(total-alpha[c] < t <= alpha[c])
                for bit in (0, 1):
                    qbit = int(delta*bit >= t-(total-alpha[c]))
                    q0 = int(0 >= t-(total-alpha[c]))
                    q1 = int(delta >= t-(total-alpha[c]))
                    assert 2*qbit-q0-q1 == (2*bit-1)*h
                    conversion_checks += 1
out["three_gate_conversion_checks"] = conversion_checks

# A common wrong extension: allowing signed table normals destroys owner locality.
alpha = (1, -1, 1, -1)
t = 0
D = [int(a >= t)-int(sum(alpha)-a >= t) for a in alpha]
assert D == [1, -1, 1, -1]
out["signed_counterexample"] = {"alpha": alpha, "threshold": t, "differences": D}
print(json.dumps(out, indent=2))
Path(__file__).with_name("monotone_checks.json").write_text(json.dumps(out, indent=2)+"\n")
