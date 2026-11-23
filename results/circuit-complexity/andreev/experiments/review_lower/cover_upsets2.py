"""Corner covers by 1-sets of sign-coherent k=2 gates = up-sets in orientation (+,+) or (+,-)
(reflecting both coordinates gives complements of up-sets, which have the same corner cuts).
Exact cover number (HiGHS MILP) and LP value; compare with lines (cover_check.py)."""
import sys; sys.path.insert(0,'/tmp/pydeps'); sys.path.insert(0,'/tmp/andreev_gap/review_lower')
import numpy as np
from cover_check import upset_cutsets, solve
for m in map(int, sys.argv[1:]):
    sq, S1 = upset_cutsets(m)
    pos = {s: i for i, s in enumerate(sq)}
    # reflect s2 -> m-1-b on squares (a,b) -> (a, m-1-b)
    refl = [frozenset(pos[(sq[e][0], m - 1 - sq[e][1])] for e in s) for s in S1]
    allS = sorted(set(S1) | set(refl), key=len, reverse=True); maximal = []
    for s in allS:
        if not any(s <= t for t in maximal): maximal.append(s)
    res, lpv, duv, w = solve(sq, maximal)
    bnd = [i for i, (a, b) in enumerate(sq) if a in (0, m - 1) or b in (0, m - 1)]
    print(f'COHERENT (up-sets, both orientations) m={m}: maximal cut-sets={len(maximal)}  cover number={round(res.fun)}  LP={lpv:.4f}  '
          f'(m-1={m-1});  dual weight on boundary={w[bnd].sum():.3f}', flush=True)
