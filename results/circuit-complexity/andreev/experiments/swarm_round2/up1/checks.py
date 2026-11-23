# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Exact guardrails for the round-two UP1 hand proofs; no asymptotic inference."""
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parent
counts = {}
rng = random.Random(20261111)


def chi(s, c):
    return -1 if (s & c).bit_count() % 2 else 1


# Mixed support-dependent incidence directions, including odd unequal weights.
incidence_cases = 0
for k, m in [(1, 1), (1, 3), (2, 1), (2, 2), (3, 1), (3, 2)]:
    ntable = 1 << k
    edges = [(rng.randrange(ntable), i, rng.choice([-3, -1, 1, 3]))
             for i in range(k) for _ in range(m)]
    for address in product([0, 1], repeat=k*m):
        divergence = [0] * ntable
        for bit, (v, i, w) in zip(address, edges):
            divergence[v] += w * bit
            divergence[v ^ (1 << i)] -= w * bit
        ds = [sum(chi(s, c) * divergence[c] for c in range(ntable)) // 2
              for s in range(ntable)]
        label = sum((sum(address[i*m:(i+1)*m]) % 2) << i for i in range(k))
        assert all((-1 if ds[s] % 2 else 1) == chi(s, label)
                   for s in range(ntable))
        assert 4 * sum(d*d for d in ds) == ntable * sum(d*d for d in divergence)
        for table in product([0, 1], repeat=ntable):
            signs = [1-2*x for x in table]
            xs = [sum(chi(s, c)*signs[c] for c in range(ntable))
                  for s in range(ntable)]
            cross = sum(w*bit*(signs[v]-signs[v ^ (1 << i)])
                        for bit, (v, i, w) in zip(address, edges))
            assert 2 * sum(x*d for x, d in zip(xs, ds)) == ntable * cross
            # Every cross product is one raw Boolean AND threshold.
            raw = 2 * sum(w*(int(bit + table[v ^ (1 << i)] >= 2)
                             - int(bit + table[v] >= 2))
                          for bit, (v, i, w) in zip(address, edges))
            assert raw == cross
            incidence_cases += 1
counts['incidence_table_address_cases'] = incidence_cases

# Exact square-staircase accounting for arbitrary signed incidence degrees.
square_cases = 0
for lower in range(-12, 1):
    for upper in range(0, 13):
        for value in range(lower, upper+1):
            expanded = lower*lower + sum((2*t-1)*int(value >= t)
                                         for t in range(lower+1, upper+1))
            assert expanded == value*value
            square_cases += 1
counts['signed_square_staircases'] = square_cases


def kernel(u, v, lam, threshold):
    return (int(u + lam*v >= threshold) + int(-u - lam*v >= threshold)
            - int(u - lam*v >= threshold) - int(-u + lam*v >= threshold))

# Include exact equality thresholds, which test strict/weak endpoint treatment.
kernel_cases = 0
for u in list(range(-8, 0)) + list(range(1, 9)):
    for v in list(range(-8, 0)) + list(range(1, 9)):
        for lam in [Fraction(1, 8), Fraction(1, 3), Fraction(1), Fraction(3), Fraction(8)]:
            a, b = abs(u), abs(v)
            thresholds = {Fraction(1, 2), Fraction(1), Fraction(7),
                          abs(a-lam*b), a+lam*b,
                          abs(a-lam*b)+Fraction(1, 13), a+lam*b+Fraction(1, 13)}
            for t in thresholds:
                if t <= 0:
                    continue
                expected = (1 if u*v > 0 else -1) * int(abs(a-lam*b) < t <= a+lam*b)
                assert kernel(u, v, lam, t) == expected
                kernel_cases += 1
counts['exact_kernel_endpoint_cases'] = kernel_cases

# Dyadic sign-only sum: every individual term has the correct sign or vanishes.
dyadic_cases = 0
minimum_active, maximum_active = 10**9, 0
for rbound in [1, 2, 3, 8, 17, 32]:
    exponent = (rbound-1).bit_length()
    lams = [Fraction(2)**q for q in range(-exponent, exponent+1)]
    ts = [Fraction(2)**p for p in range(exponent+1)]
    for a in range(1, rbound+1):
        for b in range(1, rbound+1):
            active = sum(int(abs(a-lam*b) < t <= a+lam*b) for lam in lams for t in ts)
            assert active >= 1
            minimum_active = min(minimum_active, active)
            maximum_active = max(maximum_active, active)
            dyadic_cases += 4  # Four sign choices have the same unsigned count.
counts['dyadic_sign_inputs'] = dyadic_cases
counts['dyadic_active_count_range'] = [minimum_active, maximum_active]

# Exact finite low-degree obstruction: every monomial of degree < d is orthogonal.
ortho_cases = 0
for d in range(2, 8):
    for subset in range(1 << d):
        if subset == (1 << d)-1:
            continue
        corr = sum(chi((1 << d)-1, a)*chi(subset, a) for a in range(1 << d))
        assert corr == 0
        ortho_cases += 1
counts['low_degree_parity_orthogonalities'] = ortho_cases

# Finite approximate product bank. Float logs choose the candidates ONLY;
# every saved gate, top coefficient, error certificate and evaluation is rational.
# The hand proof supplies asymptotic existence independently of this experiment.
rbound, number, eta = 8, 8192, Fraction(1, 100)
denominator = 1 << 30
log_l0, log_l1 = math.log(float(eta/rbound)), math.log(float(rbound/eta))
log_t0, log_t1 = math.log(float(eta)), math.log(float(2*rbound*rbound/eta))
bank_rng = random.Random(2026111101)
bank = []
for _ in range(number):
    lam_num = round(denominator * math.exp(bank_rng.uniform(log_l0, log_l1)))
    threshold_num = round(denominator * math.exp(bank_rng.uniform(log_t0, log_t1)))
    assert lam_num > 0 and threshold_num > 0
    bank.append([lam_num, threshold_num])


def kernel_numerator(u, v, lam_num, threshold_num):
    return (int(denominator*u + lam_num*v >= threshold_num)
            + int(-denominator*u - lam_num*v >= threshold_num)
            - int(denominator*u - lam_num*v >= threshold_num)
            - int(-denominator*u + lam_num*v >= threshold_num))

signed_counts = {}
for u in list(range(-rbound, 0)) + list(range(1, rbound+1)):
    for v in list(range(-rbound, 0)) + list(range(1, rbound+1)):
        signed_counts[u, v] = sum(kernel_numerator(u, v, *row) for row in bank)
        assert signed_counts[u, v] * u * v > 0
lo, hi = min(map(abs, signed_counts.values())), max(map(abs, signed_counts.values()))
scale = Fraction(2, lo+hi)
error = Fraction(hi-lo, hi+lo)
assert error < Fraction(1, 4), error
for (u, v), value in signed_counts.items():
    assert abs(scale*value - (1 if u*v > 0 else -1)) <= error

# Use the SAME certified bank in an explicit raw-input guarded branch score.
# This artificial fixture is not claimed to compute Andreev.
hybrid_cases = 0
max_score_error = Fraction(0)
for bits in product([0, 1], repeat=8):
    table, address = bits[:4], bits[4:]
    u = 2*sum(table)-3
    v0 = 2*(address[0]+address[1]-1)+1
    v1 = 2*(table[0]-table[1]+address[2]-address[3])+1
    guard, g0, g1 = int(u > 0), int(v0 > 0), int(v1 > 0)
    ideal = (2*g1-1) if guard else (2*g0-1)
    def approximate_and(v, g):
        return Fraction(guard+g, 2) + (scale*signed_counts[u, v]-1)/4
    compiled = 2*g0-1 + 2*approximate_and(v1, g1) - 2*approximate_and(v0, g0)
    assert (compiled > 0) == (ideal > 0)
    assert abs(compiled-ideal) <= error
    max_score_error = max(max_score_error, abs(compiled-ideal))
    hybrid_cases += 1

certificate = {
    'Authors': 'Christian Reitwiessner',
    'status': 'VERIFIED EXACT FINITE; sampling and range theorem proved separately',
    'range': rbound,
    'denominator': denominator,
    'lambda_threshold_numerators': bank,
    'top_scale_per_four_gate_kernel': str(scale),
    'minimum_absolute_kernel_sum': lo,
    'maximum_absolute_kernel_sum': hi,
    'uniform_product_error': str(error),
}
(ROOT/'product_bank.json').write_text(json.dumps(certificate, separators=(',', ':'))+'\n')
counts['product_bank'] = {
    'raw_thresholds_before_merging': 4*number,
    'grid_pairs': len(signed_counts),
    'minimum_absolute_kernel_sum': lo,
    'maximum_absolute_kernel_sum': hi,
    'rational_top_scale': str(scale),
    'exact_uniform_error': str(error),
    'hybrid_inputs': hybrid_cases,
    'maximum_exact_hybrid_score_error': str(max_score_error),
}
# Unate parity coefficient bound and its intermediate influence inequalities.
# Integer computations: correlations and influences are scaled by 2**d.
parity_bound_cases = 0
for d in range(2, 7):
    weight_rows = list(product([-2, -1, 0, 1, 2], repeat=d)) if d <= 3 else [tuple(rng.randrange(-5, 6) for _ in range(d)) for _ in range(60)]
    vertices = list(product([0, 1], repeat=d))
    for weights in weight_rows:
        linear = [sum(w*x for w, x in zip(weights, z)) for z in vertices]
        for threshold in range(min(linear)-1, max(linear)+2):
            gates = [int(value >= threshold) for value in linear]
            correlation = sum(((-1)**sum(z))*g for z, g in zip(vertices, gates))
            influences = [sum(gates[index] != gates[index ^ (1 << (d-1-i))]
                              for index in range(1 << d)) for i in range(d)]
            assert all(2*abs(correlation) <= influence for influence in influences)
            assert sum(influences)**2 <= d*(1 << (2*d))
            assert 4*d*correlation*correlation <= (1 << (2*d))
            parity_bound_cases += 1
counts['arbitrary_weight_parity_correlation_cases'] = parity_bound_cases
result = {'Authors': 'Christian Reitwiessner', 'status': 'all exact checks passed', 'checks': counts}
(ROOT/'checks.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
