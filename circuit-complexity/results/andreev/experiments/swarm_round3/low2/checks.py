# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
# Mathematical ancestry: UP2 paired restrictions and baseline sweeping;
# LOW2 connected-profile isolation; independent two-baseline refinement UP2.
"""Exact guardrails for the round-three profile-isolation theorem."""
from fractions import Fraction as Q
from itertools import product
from math import ceil, log2
from pathlib import Path
import json
import random

ROOT = Path(__file__).resolve().parent
rng = random.Random(310211)
counts = {}

def tree_edges(k, target):
    left = [i for i in range(k) if (target >> i) & 1]
    right = [i for i in range(k) if not (target >> i) & 1]
    return [(left[0], j) for j in right] + [(i, right[0]) for i in left[1:]]

def canonical(k, mask):
    return min(mask, mask ^ ((1 << k) - 1))

n = 0
for k in range(2, 9):
    for target in range(1, (1 << k) - 1):
        edges = tree_edges(k, target)
        assert len(edges) == k - 1
        for other in range(1 << k):
            all_different = all(((other >> i) ^ (other >> j)) & 1 for i, j in edges)
            assert all_different == (other in (target, target ^ ((1 << k) - 1)))
            n += 1
counts['connected_profile_tests'] = n

n = 0
scales = [Q(0), Q(1, 7), Q(1), Q(3, 2), Q(17), Q(1000)]
for _ in range(14000):
    a, b = rng.choice(scales), rng.choice(scales)
    if a == b == 0:
        continue
    live = rng.randrange(1, 12)
    D = rng.randrange(0, 16)
    eps, eta = rng.choice([-1, 1]), rng.choice([-1, 1])
    u = [rng.choice([-1, 1]) * a for _ in range(live)]
    v = [rng.choice([-1, 1]) * b for _ in range(live)]
    low = sum(min(0, w) for w in u + v)
    high = sum(max(0, w) for w in u + v)
    assert high - low == live * (a + b)
    theta = rng.choice([low, high, Q(rng.randrange(-100, 100), 7)])
    bound = (live * (a + b) // max(a, b)) + 1
    for fixed in range(D + 1):
        bad = 0
        for sweep in range(D + 1):
            s, t = (sweep, fixed) if a >= b else (fixed, sweep)
            shift = eps * a * s + eta * b * t
            bad += low + shift < theta <= high + shift
        assert bad <= bound <= 2 * live + 1
        n += 1
counts['rational_bad_baseline_slices'] = n

# Direct, complete signed restriction counts for small heterogeneous examples.
n = 0
for k in range(2, 5):
    for target in range(1, (1 << k) - 1):
        edges = tree_edges(k, target)
        for other in range(1 << k):
            if canonical(k, other) == canonical(k, target):
                continue
            for r in range(1, 4):
                a, b = rng.choice([(0, 2), (1, 3), (7, 0), (3, 3)])
                pairs = []
                for i, j in edges:
                    for _ in range(r):
                        u = (a if (other >> i) & 1 else b) * rng.choice([-1, 1])
                        v = (a if (other >> j) & 1 else b) * rng.choice([-1, 1])
                        pairs.append((u, v))
                surviving = 0
                for signs in product([-1, 1], repeat=len(pairs)):
                    surviving += all(u + t * v for (u, v), t in zip(pairs, signs))
                assert surviving <= 2 ** (len(pairs) - r)
                n += 1
counts['exhaustive_pairing_survival_tests'] = n

# Construct an actual two-table exact input/rectangle dual.  Pure-address
# helpers are deliberately outside the two-scale model.
k, m, target, G, R = 3, 100, 1, 12, 1
N, M = 1 << k, k * m
r = max(2, ceil(log2(G + 1)))
L = (k - 1) * r
D = (m - (k - 1) * r + (1 << R) - 1) // (1 << R)
B = 2 * L + 1
assert 2 * B < D + 1   # One exceptional-profile gate is insufficient.
used = [0] * k
pairs = []
for i, j in tree_edges(k, target):
    for _ in range(r):
        pairs.append((i * m + used[i], j * m + used[j]))
        used[i] += 1
        used[j] += 1
assert len(pairs) == L and len(set(sum(([a, b] for a, b in pairs), []))) == 2 * L

profiles = [target] + [2, 3] * 4 + [0, 0, 2]
gates = []
profile_masks = {}
for j, profile in enumerate(profiles):
    a, b = rng.choice([(1, 3), (0, 7), (11, 0)]) if profile else (2, 2)
    if j == 0:
        a, b = 1, 3
    mask = [rng.choice([-1, 1]) for _ in range(M)]
    if profile:
        mask = profile_masks.setdefault(canonical(k, profile), mask)
    address = [mask[q] * (a if (profile >> (q // m)) & 1 else b) for q in range(M)]
    gates.append({'profile': profile, 'scales': [a, b], 'mask': mask,
                  'table': [rng.choice([-5, -3, -1, 1, 3, 5]) for _ in range(N)],
                  'address': address, 'threshold': rng.randrange(-12, 13)})
assert len(gates) == G

# For the only exceptional gate, R=1.  Pick the larger sign class separately
# in a selected and ignored block, after reserving all live coordinates.
sweep_groups = []
for block in [0, 1]:
    rest = list(range(block * m + used[block], (block + 1) * m))
    groups = [[q for q in rest if gates[0]['mask'][q] == s] for s in [-1, 1]]
    group = max(groups, key=len)
    assert len(group) >= D
    sweep_groups.append(group[:D])

plus = [(1 + (-1) ** ((target & c).bit_count())) // 2 for c in range(N)]
minus = [1 - x for x in plus]

def constant(gate, table, fixed):
    offset = sum(a * b for a, b in zip(gate['table'], table))
    offset += sum(a * b for a, b in zip(gate['address'], fixed))
    live_weights = [gate['address'][q] for pair in pairs for q in pair]
    low = offset + sum(min(0, a) for a in live_weights)
    high = offset + sum(max(0, a) for a in live_weights)
    return not (low < gate['threshold'] <= high)

good_baseline = None
for s, t in product(range(D + 1), repeat=2):
    fixed = [0] * M
    for q in sweep_groups[0][:s] + sweep_groups[1][:t]:
        fixed[q] = 1
    if all(constant(gates[0], tab, fixed) for tab in [plus, minus]):
        good_baseline = (s, t, fixed)
        break
assert good_baseline is not None
s, t, fixed = good_baseline

good_signs = None
for signs in product([-1, 1], repeat=L):
    if all(any(gate['address'][u] + sign * gate['address'][v] == 0
               for (u, v), sign in zip(pairs, signs)) for gate in gates[1:]):
        good_signs = signs
        break
assert good_signs is not None

helpers = [
    {'table': [0] * N, 'address': [rng.randrange(-1000, 1001) for _ in range(M)],
     'threshold': rng.randrange(-1000, 1001)} for _ in range(3)]
helpers += [{'table': [rng.randrange(-10, 11) for _ in range(N)],
             'address': [0] * M, 'threshold': rng.randrange(-10, 11)} for _ in range(2)]
all_gates = gates + helpers

def outputs(table, address):
    return [int(sum(c * x for c, x in zip(g['table'], table)) +
                sum(c * a for c, a in zip(g['address'], address)) >= g['threshold'])
            for g in all_gates]

def addressed(z):
    a = fixed.copy()
    for (u, v), sign, bit in zip(pairs, good_signs, z):
        a[u] = bit
        a[v] = bit if sign == 1 else 1 - bit
    return a

signed_sums = [0] * (len(all_gates) + N + M + 1)
rectangle_sum = [0] * len(all_gates)
rows_nonzero = 0
cache = {}
for z in product([0, 1], repeat=L):
    a = addressed(z)
    label = sum((sum(a[i*m:(i+1)*m]) % 2) << i for i in range(k))
    pair_values = []
    for tab in [plus, minus]:
        vals = outputs(tab, a)
        y = 2 * tab[label] - 1
        features = vals + tab + a + [1]
        signed_sums = [q + y * f for q, f in zip(signed_sums, features)]
        pair_values.append(vals)
    cache[z] = (2 * plus[label] - 1, pair_values)
assert not any(signed_sums)
for z, (y, vals) in cache.items():
    if y != 1:
        continue
    zz = (1-z[0],) + z[1:]
    yy, vals2 = cache[zz]
    assert yy == -1
    row = [p - q - pp + qq for p, q, pp, qq in zip(vals[0], vals[1], vals2[0], vals2[1])]
    rectangle_sum = [a + b for a, b in zip(rectangle_sum, row)]
    rows_nonzero += any(row)
assert not any(rectangle_sum)
counts['explicit_dual_inputs'] = 2 ** (L + 1)
counts['exact_feature_annihilation_equations'] = len(signed_sums)
counts['positive_oriented_rectangle_rows'] = 2 ** (L - 1)
counts['nonzero_oriented_rectangle_rows'] = rows_nonzero

# Dense semantic Walsh activity fixture: all T != empty react nonconstantly.
# Rational tiny mixed table coefficients; the chosen normal has two scales.
n = 0
for k0 in range(2, 7):
    N0 = 1 << k0
    alpha = [Q(2)] + [Q((-1)**c, 8 * N0) for c in range(1, N0)]
    for T in range(1, N0):
        xp = [(1 + (-1)**((c & T).bit_count())) // 2 for c in range(N0)]
        xm = [1-x for x in xp]
        diffs = []
        for address_shift in [0, 2]:
            diffs.append(int(sum(c*x for c,x in zip(alpha,xp))+address_shift >= 1) -
                         int(sum(c*x for c,x in zip(alpha,xm))+address_shift >= 1))
        assert diffs == [1, 0]
        n += 1
counts['dense_semantic_character_activities'] = n

artifact = {'authors': ['Christian Reitwiessner'], 'status': 'VERIFIED EXACT',
            'k': k, 'm': m, 'target': target, 'G': G, 'R': R, 'r': r,
            'L': L, 'D': D, 'B': B, 'baseline': [s, t], 'fixed': fixed,
            'pairs': pairs, 'literal_signs': good_signs, 'gates': all_gates,
            'description': 'Uniform mass on two complementary character tables and all live assignments; positive oriented-rectangle dependence.',
            'counts': counts}
(ROOT / 'profile_dual_certificate.json').write_text(json.dumps(artifact, indent=2) + '\n')
(ROOT / 'checks.json').write_text(json.dumps({'authors': ['Christian Reitwiessner'], 'counts': counts}, indent=2) + '\n')
print(json.dumps(counts, sort_keys=True))
