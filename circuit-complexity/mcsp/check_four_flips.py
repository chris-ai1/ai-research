"""Classify four flips of four-bit parity on the active side of one selector.

Run with python3 check_four_flips.py. Requires python-sat with CaDiCaL 1.9.5.
"""
from collections import Counter
from functools import reduce
from itertools import combinations, permutations, product
from operator import xor

from pysat.formula import IDPool
from pysat.solvers import Solver


def signed(literal, positive):
    if positive:
        return literal
    return not literal if isinstance(literal, bool) else -literal


class CircuitSearch:
    """SAT encoding of signed, full-binary circuits with at most a gate budget."""

    def __init__(self, variables, budget):
        self.variables = variables
        self.budget = budget
        self.variable_id = IDPool().id
        self.solver = Solver(name="cadical195")
        for gate in range(variables, variables + budget):
            self.add_gate(gate)

    def clause(self, *terms):
        if not any(term is True for term in terms):
            self.solver.add_clause([term for term in terms if term is not False])

    def wire(self, source, address):
        if source < self.variables:
            return bool(address & (1 << source))
        return self.variable_id(("wire", source, address))

    def add_gate(self, gate):
        select = [[self.variable_id(("select", gate, pin, i)) for i in range(gate)]
                  for pin in range(2)]
        for choices in select:
            self.clause(*choices)
            for first, second in combinations(choices, 2):
                self.clause(-first, -second)
        # Distinct ordered sources suffice. Projections let us pad shorter circuits.
        for left in range(gate):
            for right in range(left + 1):
                self.clause(-select[0][left], -select[1][right])
        # Complement any wire that evaluates to 1 at the all-zero input and
        # absorb that sign into its readers. Every gate can therefore send 00 to 0.
        operations = {(a, b): self.variable_id(("op", gate, a, b)) if a or b else False
                      for a, b in product(range(2), repeat=2)}
        for address in range(2 ** self.variables):
            pins = [self.variable_id(("pin", gate, pin, address)) for pin in range(2)]
            for pin, choices in enumerate(select):
                for source, chosen in enumerate(choices):
                    value = self.wire(source, address)
                    self.clause(-chosen, -pins[pin], value)
                    self.clause(-chosen, pins[pin], signed(value, False))
            out = self.wire(gate, address)
            for (a, b), value in operations.items():
                mismatch = [signed(pins[0], not a), signed(pins[1], not b)]
                self.clause(*mismatch, -out, value)
                self.clause(*mismatch, out, signed(value, False))

    def realizes(self, sites):
        def output(address):
            parity = (address & 15).bit_count() % 2
            active = self.variables == 4 or bool(address & 16)
            return parity ^ (active and (address & 15) in sites)

        last_gate = self.variables + self.budget - 1
        targets = [signed(self.wire(last_gate, x), output(x) ^ output(0))
                   for x in range(2 ** self.variables)]
        return self.solver.solve(assumptions=targets)


def four_site_orbits():
    permutations_of_bits = [
        [sum(((x >> i) & 1) << j for i, j in enumerate(p)) for x in range(16)]
        for p in permutations(range(4))
    ]
    remaining = set(combinations(range(16), 4))
    while remaining:
        sites = min(remaining)
        orbit = {tuple(sorted(p[x] ^ shift for x in sites))
                 for p in permutations_of_bits for shift in range(16)}
        remaining.difference_update(orbit)
        yield sites, len(orbit)


if __name__ == "__main__":
    restricted, full = CircuitSearch(4, 5), CircuitSearch(5, 6)
    counts = Counter()
    for sites, multiplicity in four_site_orbits():
        # The selector is essential. Fixing it saves at least one gate in any
        # circuit, so failure of the four-input test excludes a six-gate solution.
        easy = restricted.realizes(sites) and full.realizes(sites)
        plane = reduce(xor, sites) == 0
        counts[(plane, easy)] += multiplicity
        print(sites, multiplicity, "plane", plane, "easy", easy, flush=True)
    print("counts by (plane, easy)", dict(counts))
    assert counts == {(True, True): 140, (False, False): 1680}
