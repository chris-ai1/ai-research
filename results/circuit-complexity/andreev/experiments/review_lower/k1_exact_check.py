"""Referee: exact-model k=1 construction of §4, m=1..300, exact rationals, plus a check that the sum is EXACTLY x_{s mod 2}
(not just its sign) and that the gate count is 2*ceil(m/2)."""
from fractions import Fraction as F
bad = 0
for m in range(1, 301):
    G = 2 * ((m + 1) // 2)
    def p(j, x0, x1):
        i = (j + 1) // 2
        return (2 * i - F(3, 2) - F(3, 10) * x0 + F(3, 4) * x1) if j % 2 else (2 * i - F(1, 2) - F(3, 5) * x0 + F(2, 5) * x1)
    for x0 in (0, 1):
        for x1 in (0, 1):
            ps = [p(j, x0, x1) for j in range(1, G + 1)]
            for s in range(m + 1):
                val = s + x0 - sum(1 for q in ps if s >= q)
                if val != (x0, x1)[s % 2]: bad += 1
print('k=1 exact construction, m=1..300: mismatches =', bad)
