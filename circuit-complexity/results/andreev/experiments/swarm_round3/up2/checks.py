# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Exact guardrails for UP2 round-three lemmas; not asymptotic inference."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
from math import comb
import random

rng = random.Random(3112026)
counts = dict(grouped_gate_inputs=0, grouped_thresholds=0, face_coefficients=0,
              conjunction_support_averages=0, identification_rows=0,
              two_baseline_cases=0)

def mobius(values, d):
    out = list(values)
    for i in range(d):
        for x in range(1 << d):
            if x >> i & 1:
                out[x] -= out[x ^ (1 << i)]
    return out

def sums(w):
    return [sum(w[i] for i in range(len(w)) if z >> i & 1)
            for z in range(1 << len(w))]

def compile_groups(w, groups, threshold):
    # All weights positive here, with signs handled by literal substitution.
    accepted = []
    def visit(level, fixed, value):
        tail = sum(w[i] for group in groups[level:] for i in group)
        if value >= threshold:
            accepted.append(dict(fixed))
            return
        if value + tail < threshold:
            return
        assert level < len(groups)
        group = groups[level]
        later = tail - sum(w[i] for i in group)
        unresolved = 0
        for bits in product((0, 1), repeat=len(group)):
            nxt = dict(fixed)
            nxt.update(zip(group, bits))
            val = value + sum(w[i] * b for i, b in zip(group, bits))
            if val < threshold <= val + later:
                unresolved += 1
            visit(level + 1, nxt, val)
        assert unresolved <= 1
    visit(0, {}, Q(0))
    return accepted

counts['grouped_identification_rows'] = 0
def check_group_identification(w, groups):
    old_group = {i: lev for lev, group in enumerate(groups) for i in group}
    width = rng.randrange(1, len(w) + 1)
    merged = [Q(0)] * width
    earliest = [len(groups)] * width
    for i, v in enumerate(w):
        if not v:
            continue
        dst = rng.randrange(width)
        merged[dst] += v * rng.choice((-1, 1))
        earliest[dst] = min(earliest[dst], old_group[i])
    new_groups = [[i for i,v in enumerate(merged) if v and earliest[i] == lev]
                  for lev in range(len(groups))]
    new_groups = [g for g in new_groups if g]
    for lev, group in enumerate(new_groups[:-1]):
        levels = sorted(sums([abs(merged[i]) for i in group]))
        assert len(set(levels)) == len(levels)
        tail = sum(abs(merged[i]) for g in new_groups[lev+1:] for i in g)
        assert min(b-a for a,b in zip(levels, levels[1:])) > tail
    assert all(len(g) <= max(map(len,groups)) for g in new_groups)
    counts['grouped_identification_rows'] += 1

for d in range(1, 9):
    for trial in range(12):
        order = list(range(d))
        rng.shuffle(order)
        support = order[:rng.randrange(1, d + 1)]
        groups = []
        while support:
            q = min(len(support), rng.randrange(1, 4))
            groups.append(support[:q])
            support = support[q:]
        w = [Q(0)] * d
        tail = Q(0)
        for group in reversed(groups):
            while True:
                local = [Q(rng.randrange(1, 50), rng.randrange(1, 8)) for _ in group]
                levels = sorted(set(sums(local)))
                if len(levels) == 1 << len(group):
                    break
            gap = min(b - a for a, b in zip(levels, levels[1:]))
            scale = (tail + 1) / gap
            for i, a in zip(group, local):
                w[i] = a * scale
            tail += sum(w[i] for i in group)
        sign = [rng.choice((-1, 1)) for _ in range(d)]
        signed = [a * b for a, b in zip(w, sign)]
        for _ in range(10):
            check_group_identification(signed, groups)
        offset = sum(w[i] for i in range(d) if sign[i] < 0)
        levels = sorted(set(sums(signed)))
        thresholds = levels + [(a + b) / 2 for a, b in zip(levels, levels[1:])]
        thresholds += [levels[0] - 1, levels[-1] + 1]
        bound = sum(1 << len(g) for g in groups)
        for threshold in thresholds:
            terms = compile_groups(w, groups, threshold + offset)
            assert len(terms) <= bound
            for x in range(1 << d):
                y = [((x >> i) & 1) if sign[i] > 0 else 1 - ((x >> i) & 1)
                     for i in range(d)]
                value = sum(all(y[i] == b for i, b in term.items()) for term in terms)
                gate = int(sum(signed[i] for i in range(d) if x >> i & 1) >= threshold)
                assert value == gate
                counts['grouped_gate_inputs'] += 1
            counts['grouped_thresholds'] += 1

for d in range(1, 8):
    vals = [(-1) ** x.bit_count() * rng.randrange(1, 1000) for x in range(1 << d)]
    for base in range(1 << d):
        coeff = mobius([vals[x ^ base] for x in range(1 << d)], d)
        for u, c in enumerate(coeff):
            assert c * (-1) ** (base.bit_count() + u.bit_count()) > 0
            counts['face_coefficients'] += 1
    for r in range(d + 1):
        signs = [rng.randrange(2) for _ in range(r)]
        total = 0
        for base in range(1 << d):
            values = [int(all(((x ^ base) >> i) & 1 == signs[i] for i in range(r)))
                      for x in range(1 << d)]
            total += sum(c != 0 for c in mobius(values, d))
        assert Q(total, 1 << d) == Q(3, 2) ** r
        counts['conjunction_support_averages'] += 1

for d in range(2, 25):
    for trial in range(100):
        w = []
        tail = 0
        for _ in range(d):
            v = tail + rng.randrange(1, 20)
            w.append(v * rng.choice((-1, 1)))
            tail += v
        rng.shuffle(w)
        merged = [0] * rng.randrange(1, d + 1)
        for v in w:
            merged[rng.randrange(len(merged))] += v * rng.choice((-1, 1))
        nonzero = sorted((abs(v) for v in merged if v), reverse=True)
        assert all(v > sum(nonzero[i + 1:]) for i, v in enumerate(nonzero))
        counts['identification_rows'] += 1

for _ in range(4000):
    D = rng.randrange(1, 25)
    L = rng.randrange(1, 8)
    a = Q(rng.randrange(-20, 21), rng.randrange(1, 15))
    b = Q(rng.randrange(-20, 21), rng.randrange(1, 15))
    W = max(abs(a), abs(b))
    if W == 0:
        continue
    lo = Q(rng.randrange(-200, 201), rng.randrange(1, 15))
    width = Q(rng.randrange(0, 2 * L + 1)) * W
    theta = Q(rng.randrange(-200, 201), rng.randrange(1, 15))
    bad = sum(lo + a*s + b*t < theta <= lo + a*s + b*t + width
              for s in range(D + 1) for t in range(D + 1))
    assert bad <= (D + 1) * (2 * L + 1)
    counts['two_baseline_cases'] += 1

# Last groups may have repeated subset sums; no final injectivity assumption.
counts['colliding_final_group_inputs'] = 0
for d in range(2, 9):
    w = [Q(4*d)] + [Q(1)] * (d - 1)
    groups = [[0], list(range(1, d))]
    for _ in range(100):
        check_group_identification(w, groups)
    for threshold in range(6*d):
        terms = compile_groups(w, groups, threshold)
        for x in range(1 << d):
            value = sum(all(((x >> i) & 1) == b for i,b in term.items()) for term in terms)
            assert value == int(sum(w[i] for i in range(d) if x >> i & 1) >= threshold)
            counts['colliding_final_group_inputs'] += 1

counts['bridge_occupation_identities'] = 0
def choose(n, r):
    return comb(n, r) if 0 <= r <= n else 0
for h in range(0, 71):
    for q in range(h // 2 + 1):
        delta = h - 2*q
        den = comb(h, q)
        for y in range(-q-1, h-q+2):
            marked = 0
            for t in range(h + 1):
                if (t+y) % 2 == 0 and (h-t+delta-y) % 2 == 0:
                    marked += choose(t,(t+y)//2)*choose(h-t,(h-t+delta-y)//2)
            distance = max(-y, y-delta, 0)
            expected_numerator = sum(comb(h+1,j) for j in range(q-distance+1))
            assert marked == expected_numerator
            assert marked * (delta+1) <= den * (h+1)
            counts['bridge_occupation_identities'] += 1

result = {'Authors': 'Christian Reitwiessner', 'status': 'VERIFIED EXACT', 'counts': counts}
Path(__file__).with_name('checks.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
