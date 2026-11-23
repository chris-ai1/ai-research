"""Finite checks for the signed-identification lower bound."""
from collections import Counter
from itertools import combinations


def check_local_deletions():
    split_types = Counter()
    for gate in range(16):
        values = [(gate >> i) & 1 for i in range(4)]
        if values[::2] == values[1::2] or values[:2] == values[2:]:
            continue
        constant_signs = sum(values[b] == values[3 ^ b] for b in (0, 1))
        split_types[constant_signs] += 1
    assert split_types == {1: 8, 2: 2}


def gate_outputs(a, b, mask):
    # Free signs identify a function with its complement. The five operations
    # below exhaust the essential binary functions up to that output sign.
    for value in (a ^ b, a & b, a & (mask ^ b), (mask ^ a) & b, (mask ^ a) & (mask ^ b)):
        yield min(value, mask ^ value)


def small_circuit_sizes(d, limit):
    """Enumerate circuits, allowing arbitrary reuse of each available wire."""
    num_rows = 1 << d
    mask = (1 << num_rows) - 1
    inputs = []
    for coord in range(d):
        truth = sum(((x >> coord) & 1) << x for x in range(num_rows))
        inputs.append(min(truth, mask ^ truth))

    sizes = dict.fromkeys(inputs, 0)
    sizes[0] = 0
    layer = {tuple(sorted(inputs))}
    for depth in range(1, limit + 1):
        next_layer = set()
        for wires in layer:
            for a, b in combinations(wires, 2):
                for value in gate_outputs(a, b, mask):
                    if value == 0 or value in wires:
                        continue
                    sizes.setdefault(value, depth)
                    if depth < limit:
                        next_layer.add(tuple(sorted((*wires, value))))
        layer = next_layer
    return sizes


def meets_one_edge(accepted, d):
    for i, j in combinations(range(d), 2):
        if len({((x >> i) ^ (x >> j)) & 1 for x in accepted}) < 2:
            return False
    return True


def satisfies_bound(d, g, count, r):
    # Check count^2 >= 2^(2d-g-1-r) (3+2 sqrt(2))^r using integers.
    a, b = 1, 0
    for _ in range(r):
        a, b = 3 * a + 4 * b, 2 * a + 3 * b
    exponent = 2 * d - g - 1 - r
    scale = 1 << max(0, exponent)
    difference = (count * count << max(0, -exponent)) - scale * a
    return difference >= 0 and difference * difference >= 2 * (scale * b) ** 2


def check_four_inputs():
    d = 4
    num_rows = 1 << d
    mask = (1 << num_rows) - 1
    sizes = small_circuit_sizes(d, 4)
    checked = Counter()
    for selection in range(1, 1 << (num_rows // 2)):
        accepted = set()
        for x in range(num_rows // 2):
            if selection & (1 << x):
                accepted.update((x, x ^ (num_rows - 1)))
        truth = sum(1 << x for x in accepted)
        # Every truth table absent from the search has minimum size >= 5.
        lower = sizes.get(min(truth, mask ^ truth), 5)
        assert satisfies_bound(d, lower, len(accepted), 0)
        checked[0] += 1
        if 2 * len(accepted) <= 1 << d and meets_one_edge(accepted, d):
            assert satisfies_bound(d, lower, len(accepted), 1)
            checked[1] += 1
    assert checked[1] > 0
    print(f"Four inputs: {checked[0]} complement-closed families, {checked[1]} meeting the one-edge hypotheses.")


if __name__ == "__main__":
    check_local_deletions()
    check_four_inputs()
