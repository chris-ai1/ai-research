"""Verify the strict inequalities in optimum.md, using exact fractions."""

from fractions import Fraction as F


def ln_bounds(x):
    """Bound ln(x) for x >= 1 by summing the positive atanh series."""
    assert x >= 1
    y = (x - 1) / (x + 1)
    partial = 2 * sum(y**i / i for i in range(1, 32, 2))
    tail = 2 * y**33 / (33 * (1 - y**2))
    return partial, partial + tail


LN2_LOW, LN2_HIGH = ln_bounds(F(2))


def log2_bounds(x):
    if x < 1:
        low, high = log2_bounds(1 / x)
        return -high, -low
    low, high = ln_bounds(x)
    return low / LN2_HIGH, high / LN2_LOW


def bernoulli_divergence(p, reference):
    on_low, on_high = log2_bounds(p / reference)
    off_low, off_high = log2_bounds((1 - p) / (1 - reference))
    return (p * on_low + (1 - p) * off_low,
            p * on_high + (1 - p) * off_high)


def check_row(a, b, p, q, entropy_limit, gate_floor):
    d_low, d_high = bernoulli_divergence(p, F(1, 2))
    _, private_high = bernoulli_divergence(q, F(3, 4))
    entropy_high = d_high + max(0, private_high - 2 * d_low) * a / q
    gates = 2 + p - a * max(3 + p, (2 + 2 * p) / q)
    assert entropy_high < entropy_limit <= b
    assert gates > gate_floor


def check_optimum():
    p_low, p_high = F(".54580359979"), F(".54580359980")
    assert p_low**2 < 7 * (1 - p_low)**4
    assert p_high**2 > 7 * (1 - p_high)**4
    d_low, _ = bernoulli_divergence(p_low, F(1, 2))
    _, d_high = bernoulli_divergence(p_high, F(1, 2))
    private_low, _ = bernoulli_divergence(F(6, 7), F(3, 4))
    assert private_low > 2 * d_high
    ell_low, ell_high = log2_bounds(F(7, 4))
    # d(p) increases throughout the bracket. Phi increases in ell and
    # decreases in d when p and the other argument are held fixed.
    g_low = 1 + (1 + p_low) * ell_low / (ell_low + 2 * d_high)
    g_high = 1 + (1 + p_high) * ell_high / (ell_high + 2 * d_low)
    assert F("2.5229339574") < g_low <= g_high < F("2.5229339576")
    a_low = F(6, 7) * d_low / (ell_high + 2 * d_low)
    a_high = F(6, 7) * d_high / (ell_low + 2 * d_high)
    assert F(".0063405695") < a_low <= a_high < F(".0063405697")


if __name__ == "__main__":
    rows = [
        (".00565", ".00565", ".543317", ".8526", ".0056497", "2.52286"),
        (".007", ".00565", ".543101", ".8523", ".0056490", "2.51775"),
        (".00565", ".00565", ".543275", ".8525", ".0056390", "2.52281"),
        (".00635", ".00635", ".545836", "6/7", ".0063495", "2.52293"),
    ]
    for row in rows:
        check_row(*map(F, row))
    assert F(rows[2][4]) < F(".00564")
    check_optimum()
    print("Verified four parameter rows and the sharp coefficient bracket.")
