# Authors: Christian Reitwiessner
"""Bounded exact checks for the research report; no external dependencies."""
import itertools
import json
import random
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent

def bit(v, i):
    return (v >> i) & 1

def sign(v):
    assert v != 0
    return 1 if v > 0 else -1

def rank_check():
    rng = random.Random(719)
    Q, D = 8, 21
    rows = [([rng.randrange(-3, 4) for _ in range(Q)], rng.randrange(-3, 4)) for _ in range(Q)]
    M = 1 + max(2 * (sum(abs(v) for v in alpha) + abs(theta)) + 1 for alpha, theta in rows)
    tests = 0
    for x in itertools.product((0, 1), repeat=Q):
        ell = [2 * (sum(a * b for a, b in zip(alpha, x)) - theta) + 1 for alpha, theta in rows]
        for T in range(D + 1):
            gates = sum(2 * M * (T - r) + ell[r % Q] >= 0 for r in range(D + 1))
            assert gates - T == (ell[T % Q] > 0)
            tests += 1
    return dict(Q=Q, D=D, M=M, exhaustive_cases=tests)

def slice_check():
    tests = 0
    for x in itertools.product((0, 1), repeat=5):
        ell = 2 * (3*x[0] - 2*x[1] + 5*x[2] - x[3] + x[4] - 2) + 1
        M = 30
        assert abs(ell) < M
        for Z in range(-9, 10):
            difference = int(2*M*Z + ell >= 0) - int(2*M*Z - ell >= 0)
            assert difference == sign(ell) * int(Z == 0)
            tests += 1
    for y in itertools.product((-1, 1), repeat=3):
        rows = ((1,1,1),(1,1,-1),(1,-1,1),(-1,1,1))
        code = [sign(sum(a*b for a,b in zip(row,y))) for row in rows]
        for i in range(3):
            assert sum(row[i]*e for row,e in zip(rows,code)) == 2*y[i]
    return dict(exhaustive_slice_cases=tests, exact_three_bit_code_cases=8)

def averaging_check(k, L):
    rng = random.Random(1000 + k)
    N, m = 1 << k, (1 << k)//k
    assert m - 1 > 1 << L
    masks = [[[rng.choice((-1, 1)) for _ in range(m)] for _ in range(k)] for _ in range(L)]
    permutations = []
    for _ in range(L):
        p = list(range(k))
        rng.shuffle(p)
        permutations.append(p)
    pairs = []
    for i in range(k):
        signatures = {}
        for j in range(1, m):
            signature = tuple(masks[l][i][j] for l in range(L))
            if signature in signatures:
                pairs.append((signatures[signature], j))
                break
            signatures[signature] = j
        else:
            raise AssertionError('pigeonhole failure')
    # Arbitrary, nonliteral Boolean code rows: exact averaging does not use their form.
    y = [1 if (bit(c,0) ^ bit(c,1)) else -1 for c in range(N)]
    code = []
    for l in range(L):
        code.append([sign(3*y[(r*13+l)%N] - 2*y[(r*7+3*l)%N] + y[(r*5+1)%N] + 1)
                     for r in range(N)])
    totals = []
    histogram_tests = 0
    for b in range(4):
        total = 0
        for l in range(L):
            p = permutations[l]
            offset = sum((1 << p[i])*(sum(s < 0 for s in masks[l][i]) + masks[l][i][0]*bit(b,i)) for i in range(k))
            deltas = [2*(1 << p[i])*masks[l][i][pairs[i][0]] for i in range(k)]
            hist = Counter((offset + sum(deltas[i]*bit(t,i) for i in range(k))) % N for t in range(N))
            expected = {r: 2 for r in range(offset % 2, N, 2)}
            assert dict(hist) == expected
            total += (l+1)*sum(count*code[l][r] for r,count in hist.items())
            histogram_tests += 1
        totals.append(total)
    assert totals[0] + totals[3] == totals[1] + totals[2]
    return dict(k=k, N=N, m=m, L=L, pairs=pairs, histogram_tests=histogram_tests,
                four_corner_score_sums=totals,
                affine_four_corner_identity=True)

results = {
    'authors': 'Christian Reitwiessner',
    'rank_identity': rank_check(),
    'gated_code_identity': slice_check(),
    'balanced_rank_counterexamples': [averaging_check(6,3), averaging_check(8,4), averaging_check(10,6)],
}
(OUT/'checks.json').write_text(json.dumps(results, indent=2)+'\n')
print(json.dumps(results, indent=2))
