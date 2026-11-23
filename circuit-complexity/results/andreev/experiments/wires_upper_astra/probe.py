#!/usr/bin/env python3
"""Finite exploration of monochromatic raw-affine guards.

Authors: Christian Reitwiessner
The search is complete only for its specified bounded positive integer
profiles, modulo coordinate permutations and sign complementation.
"""
from collections import Counter
from itertools import combinations_with_replacement, product
from math import comb
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def profile_counts(weights):
    counts = Counter({(0, 0): 1})
    for w in weights:
        nxt = counts.copy()
        for (value, parity), number in counts.items():
            nxt[value + w, 1 - parity] += number
        counts = nxt
    return counts


def search(k, m, C):
    profiles = list(combinations_with_replacement(range(1, C + 1), m))
    counters = [profile_counts(p) for p in profiles]
    best = None
    examined = admissible = 0
    for inds in combinations_with_replacement(range(len(profiles)), k):
        total = Counter({(0, 0): 1})
        for block, ind in enumerate(inds):
            new = Counter()
            for (a, label), count_a in total.items():
                for (b, parity), count_b in counters[ind].items():
                    new[a + b, label | (parity << block)] += count_a * count_b
            total = new
        by_value = {}
        for (value, label), count in total.items():
            by_value.setdefault(value, []).append((label, count))
        for value, entries in by_value.items():
            if len(entries) == 1:
                admissible += 1
                label, size = entries[0]
                if best is None or size > best['size']:
                    best = dict(size=size, level=value, label=label,
                                block_weights=[profiles[i] for i in inds])
        examined += 1
    bound = comb(m, m // 2) ** k
    return dict(k=k, m=m, coefficient_bound=C,
                profile_orbits=examined, monochromatic_levels=admissible,
                largest_section=best, product_central_binomial=bound,
                fiber_size=2 ** (k * (m - 1)),
                exceeds_product_bound=best['size'] > bound)


def main():
    cases = [(2, 3, 4), (2, 4, 4), (2, 5, 4), (2, 6, 3),
             (3, 3, 4), (3, 4, 3), (4, 2, 4)]
    results = []
    for case in cases:
        row = search(*case)
        results.append(row)
        print(case, row['profile_orbits'], row['largest_section'], flush=True)
    payload = dict(Authors='Christian Reitwiessner', results=results,
                   status='finite search only; no asymptotic conclusion')
    (ROOT / 'probe.json').write_text(json.dumps(payload, indent=2) + '\n')


if __name__ == '__main__':
    main()
