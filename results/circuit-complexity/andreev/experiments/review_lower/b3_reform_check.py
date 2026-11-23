"""Referee: exact check of Lemma B3 step 1.  sigma uniform permutation of [m], c uniform in {0..m-1}, independent.
live bit l = sigma(c+1), fixed-ones set A = {sigma(1..c)}.  Claim: Pr[l, A] = (1/m) * int_0^1 q^|A| (1-q)^(m-1-|A|) dq
 = (1/m) * 1/(m * C(m-1,|A|))   for every l and every A subset of [m]\{l}."""
import itertools
from fractions import Fraction
from math import comb, factorial
for m in range(1, 7):
    cnt = {}
    for perm in itertools.permutations(range(m)):
        for c in range(m):
            key = (perm[c], frozenset(perm[:c]))
            cnt[key] = cnt.get(key, 0) + 1
    total = factorial(m) * m; bad = 0; nkeys = 0
    for l in range(m):
        rest = [t for t in range(m) if t != l]
        for r in range(m):
            for A in itertools.combinations(rest, r):
                nkeys += 1
                p = Fraction(cnt.get((l, frozenset(A)), 0), total)
                beta = Fraction(1, m) * Fraction(1, m * comb(m - 1, r))
                if p != beta: bad += 1
    print(f'm={m}: {nkeys} (l,A) pairs, mismatches with the Beta-mixture formula = {bad}')
