# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Exact guardrails for shuffled-bridge occupation and two-baseline sweeping."""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb
from pathlib import Path
import json
import random

root = Path(__file__).resolve().parent
rng = random.Random(314159)
counts = {}

# An independent marked-time convolution counts visits without using the
# formal-power-series proof or its partial-binomial answer.
def paths(length, displacement):
    if abs(displacement) > length or (length + displacement) % 2:
        return 0
    return comb(length, (length + displacement) // 2)

n = 0
for h in range(0, 81):
    for q in range(h // 2 + 1):
        delta = h - 2 * q
        denominator = comb(h, q)
        for a in range(-q - 1, h - q + 2):
            marked = sum(paths(s, a) * paths(h-s, delta-a) for s in range(h+1))
            dist = max(0, -a, a-delta)
            stated = sum(comb(h+1, i) for i in range(q-dist+1))
            assert marked == stated
            assert Q(marked, denominator) <= Q(2*(h+1), delta+2)
            assert Q(marked, denominator) <= Q(h+1, delta+1)
            n += 1
counts['exact_marked_walk_identities_and_bounds'] = n

# Brute-force common reorientations check the inherited existence lemma,
# then exact subset weights check the conditional two-baseline estimate.
n = 0
marginal_cases = 0
for _ in range(70):
    h = rng.randrange(3, 9)
    R = rng.randrange(1, 3)
    masks = [[rng.choice([-1, 1]) for _ in range(h)] for _ in range(R)]
    bound = Q(h, R) - R
    flip = next(z for z in product([-1, 1], repeat=h)
                if all(abs(sum(a*b for a,b in zip(mask,z))) >= bound for mask in masks))
    for mask in masks:
        steps = [a*b for a,b in zip(mask, flip)]
        drift = abs(sum(steps))
        for width in range(1, 5):
            for lower in range(-h-2, h+2):
                probability = Q(0)
                for subsetbits in product([0, 1], repeat=h):
                    s = sum(subsetbits)
                    value = sum(t*b for t,b in zip(steps,subsetbits))
                    if lower <= value < lower + width:
                        probability += Q(1, (h+1)*comb(h,s))
                assert probability <= Q(2*width, drift+2)
                assert probability <= Q(width, drift+1)
                marginal_cases += 1
        n += 1
counts['common_reorientation_mask_cases'] = n
counts['exact_random_prefix_interval_probabilities'] = marginal_cases

(root / 'bridge_checks.json').write_text(json.dumps({'authors': ['Christian Reitwiessner'], 'counts': counts}, indent=2)+'\n')
print(json.dumps(counts, sort_keys=True))
