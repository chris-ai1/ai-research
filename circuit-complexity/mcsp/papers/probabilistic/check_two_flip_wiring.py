"""Finite checks for the two-flip gate bound. Run with Python 3.10 or later."""

from collections import Counter
from itertools import combinations
from math import comb


def circuit_sizes(arity, limit):
    """Enumerate gate DAGs, identifying a signal with its free complement."""
    rows = 1 << arity
    mask = (1 << rows) - 1
    raws = [sum(1 << j for j in range(rows) if j & (1 << i)) for i in range(arity)]
    wires = tuple(sorted(min(raw, raw ^ mask) for raw in raws))
    sizes = {raw: 0 for raw in (0, *wires)}
    layer = {wires}
    for depth in range(1, limit + 1):
        following = set()
        for available in layer:
            for a, b in combinations(available, 2):
                outputs = (a ^ b, a & b, a & (mask ^ b), (mask ^ a) & b,
                           (mask ^ a) & (mask ^ b))
                for output in outputs:
                    value = min(output, mask ^ output)
                    if not value or value in available:
                        continue
                    sizes.setdefault(value, depth)
                    if depth < limit:
                        following.add(tuple(sorted((*available, value))))
        layer = following
    return {f: cost for x, cost in sizes.items() for f in (x, x ^ mask)}


def check_gate_bounds():
    d = 4
    ones = (1 << d) - 1
    sizes = circuit_sizes(d, 4)
    checked = 0
    for centers in [(0, ones), (0, ones, 3, 5), (0, ones, 3, 5, 6)]:
        profiles = [tuple((center >> i) & 1 for center in centers) for i in range(d)]
        distinct = len(set(profiles)) == d  # The zero center rules out complements.
        for truth in range(1 << (1 << d)):
            if not all((truth >> center) & 1 for center in centers):
                continue
            b1 = sum(any((truth >> (center ^ (1 << i))) & 1 for center in centers)
                     for i in range(d))
            b2 = sum((truth >> ((1 << i) | (1 << j))) & 1
                     for i, j in combinations(range(d), 2))
            lower = sizes.get(truth, 5)
            assert 3 * lower >= 4 * d - 4 * b1 - 2 * b2 - 4
            if distinct:
                assert 4 * lower >= 6 * d - 6 * b1 - 3 * b2 - 5
            checked += 1
    return checked


def check_mcsp_labels():
    checked = 0
    for n in range(3, 7):
        N = 1 << n
        easy = circuit_sizes(n, n - 3)
        centers = [0, (1 << N) - 1]
        centers.extend(sum(1 << a for a in range(N) if a & (1 << i)) for i in range(n))
        assert all(center in easy for center in centers)
        assert all((center ^ (1 << i)) not in easy for center in centers for i in range(N))
        assert all(((1 << i) | (1 << j)) not in easy for i, j in combinations(range(N), 2))
        checked += (n + 2) * N + comb(N, 2)
    return checked


def partitions(sites):
    if not sites:
        yield ()
        return
    first, *rest = sites
    for extra in (1, 2):
        for group in combinations(rest, extra):
            block = (first, *group)
            remaining = [i for i in rest if i not in group]
            for tail in partitions(remaining):
                yield (sum(1 << i for i in block), *tail)


def check_block_tests():
    checked = 0
    for d in range(2, 11):
        accepted = Counter()
        totals = Counter()
        for blocks in partitions(range(d)):
            pairs = sum(block.bit_count() == 2 for block in blocks)
            totals[pairs] += 1
            unions = [0]
            for block in blocks:
                unions += [word | block for word in unions]
            accepted.update((pairs, word) for word in unions)
        for pairs, count in totals.items():
            triples = (d - 2 * pairs) // 3
            by_weight = Counter()
            for i in range(pairs + 1):
                for j in range(triples + 1):
                    by_weight[2 * i + 3 * j] += comb(pairs, i) * comb(triples, j)
            for word in range(1 << d):
                k = word.bit_count()
                assert accepted[pairs, word] * comb(d, k) == count * by_weight[k]
        checked += sum(totals.values())
    return checked


if __name__ == "__main__":
    print(f"Four-input functions with specified centers: {check_gate_bounds()}")
    print(f"Hard MCSP changes at small thresholds: {check_mcsp_labels()}")
    print(f"Partitions into pairs and triples: {check_block_tests()}")
