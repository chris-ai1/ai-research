#!/usr/bin/env python3
"""Exact-integer check of the RUNS LEMMA:
   a gate whose block functions P_i (under arrangement sigma) have rho_i monotone runs splits at most
   m^k - prod_i (m - rho_i) unit cubes of the s-grid, for EVERY threshold (i.e. every table).
For each random gate/arrangement we compute, for every cube c, the split interval (F(c^-), F(c^+)]
(F = sum_i P_i), and the maximum number of these intervals containing a common point (sweep).
Also reports how often the bound is attained.
"""
import sys, random, itertools
sys.path.insert(0, '/tmp/pydeps')


def runs(seq):
    """minimum number of maximal runs of constant sign (zeros join either side)"""
    sgn = [1 if v > 0 else -1 for v in seq if v != 0]
    if not sgn:
        return 1
    return 1 + sum(1 for a, b in zip(sgn, sgn[1:]) if a != b)


def max_split(P, k, m):
    """P[i][s] block functions; returns max over thresholds of #cubes with F(c^-) < th <= F(c^+)."""
    ev = []
    for c in itertools.product(range(m), repeat=k):
        lo = hi = 0
        for i in range(k):
            a, b = P[i][c[i]], P[i][c[i] + 1]
            lo += min(a, b); hi += max(a, b)
        if lo < hi:
            ev.append((lo, 1)); ev.append((hi, -1))   # interval (lo, hi]
    # point th: count intervals with lo < th <= hi. Sort: at equal coordinate, process closings (-1)
    # AFTER evaluating? interval (lo,hi] contains hi but not lo. Sweep over candidate th = each hi.
    his = sorted(set(h for h, t in ev if t == -1))
    los = sorted(lo for lo, t in ev if t == 1)
    hs = sorted(h for h, t in ev if t == -1)
    import bisect
    best = 0
    for th in his:
        # #lo < th  minus  #hi < th
        cnt = bisect.bisect_left(los, th) - bisect.bisect_left(hs, th)
        best = max(best, cnt)
    return best


def main():
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    worst_ratio = 0; attained = 0; total = 0; viol = 0
    for (k, m) in [(2, 4), (2, 6), (2, 9), (3, 3), (3, 5), (4, 3), (4, 4), (5, 3)]:
        for t in range(trials):
            kind = rng.choice(['coherent', 'fewruns', 'minority', 'random', 'heavy'])
            P = []; rho = []
            for i in range(k):
                if kind == 'coherent':
                    sg = rng.choice([1, -1]); w = [sg * rng.randint(0, 9) for _ in range(m)]
                elif kind == 'fewruns':
                    r = rng.randint(1, max(1, m // 2)); cuts = sorted(rng.sample(range(1, m), min(r - 1, m - 1)))
                    w = []; sg = rng.choice([1, -1]); prev = 0
                    for cpos in cuts + [m]:
                        w += [sg * rng.randint(0, 9) for _ in range(cpos - prev)]; sg = -sg; prev = cpos
                elif kind == 'minority':
                    sg = rng.choice([1, -1]); w = [sg * rng.randint(0, 9) for _ in range(m)]
                    for pos in rng.sample(range(m), rng.randint(0, 2)):
                        w[pos] = -sg * rng.randint(1, 9)
                elif kind == 'random':
                    w = [rng.randint(-9, 9) for _ in range(m)]
                else:
                    w = [rng.choice([-1, 1]) * int(2 ** rng.uniform(0, 12)) for _ in range(m)]
                # arrangement: random order of the bits; P_i = prefix sums along the arrangement
                perm = list(range(m)); rng.shuffle(perm)
                inc = [w[perm[t_]] for t_ in range(m)]
                Pi = [0]
                for v in inc: Pi.append(Pi[-1] + v)
                P.append(Pi); rho.append(runs(inc))
            bound = m ** k
            prod = 1
            for r in rho: prod *= (m - r)
            bound -= prod
            got = max_split(P, k, m)
            total += 1
            if got > bound: viol += 1; print('VIOLATION', k, m, kind, P, rho, got, bound)
            if got == bound: attained += 1
            worst_ratio = max(worst_ratio, got / bound if bound else 0)
    print(f'runs lemma: {total} gates checked (exact integers, max over all thresholds): '
          f'violations={viol}, bound attained in {attained}, max got/bound={worst_ratio:.3f}')


if __name__ == '__main__':
    main()
