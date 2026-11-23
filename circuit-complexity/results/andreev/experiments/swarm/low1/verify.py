# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Exact finite checks for LOW1. Mathematical source attribution is in report.md."""
from fractions import Fraction
from itertools import product
from math import comb
from pathlib import Path
import json
import random

OUT = Path(__file__).parent

def central_conditional(M, h):
    t = -(M % 2)
    central = Fraction(comb(M, (M + t) // 2), 2 ** M)
    if h % 2:
        p0 = Fraction(0)
    else:
        p0 = Fraction(comb(h, h // 2) * comb(M-h, (M-h+t)//2),
                      comb(M, (M+t)//2))
    return central, p0

bounds = []
for M in range(2, 121):
    for h in range(1, M):
        p, p0 = central_conditional(M, h)
        assert p0 <= Fraction(2, 3), (M, h, p0)
        bounds.append((M, h, str(p0)))

rectangles = []
for n in range(3, 13):
    M = n-1
    for h in range(1, M):
        hits = 0
        for signs in product((-1,1), repeat=n):
            total = sum(signs)
            B = sum(signs[:h])
            e = signs[-1]
            vals = [int(v >= 0) for v in
                    (total, total-2*B, total-2*e, total-2*B-2*e)]
            hits += vals[0]-vals[1]-vals[2]+vals[3] != 0
        actual = Fraction(hits, 2**n)
        pc, p0 = central_conditional(M, h)
        assert actual == 2*pc*(1-p0), (n, h, actual, pc, p0)
        rectangles.append({'n':n, 'h':h, 'probability':str(actual)})

ladder_checks = 0
for k in (1,2,3):
    N = 2**k
    for m in range(1,6):
        for sig in product((-1,1), repeat=m):
            q = sig.count(-1)
            p = m-q
            for background_sum in range(N//2):
                for z in product((0,1), repeat=m):
                    L = sum(s*a for s,a in zip(sig,z))
                    value = 0
                    for r in range(-q+1,N//2+p+1):
                        diff = int(background_sum+1+L>=r)-int(background_sum+L>=r)
                        assert diff == int(L==r-background_sum-1)
                        value += (-1)**(r-background_sum-1)*diff
                    assert value == (-1)**sum(z)
                    ladder_checks += 1

# Full finite all-table-pair/all-address-edge coverage, not just a sample.
k,m = 2,2
N,D = 2**k,k*m
n = N+D
rng = random.Random(20261111)
R = 128
normal_set = set()
while len(normal_set) < R:
    normal_set.add(tuple(rng.choice((-1,1)) for _ in range(n)))
normals = sorted(normal_set)
table_vectors = list(product((-1,1),repeat=N))
address_vectors = list(product((-1,1),repeat=D))
edge_signatures = []
min_distinct = R
for a in address_vectors:
    for coord in range(D):
        if a[coord] != -1:
            continue
        ap = list(a)
        ap[coord] = 1
        sigs = []
        for x in table_vectors:
            signature = []
            for normal in normals:
                tx = sum(w*v for w,v in zip(normal[:N],x))
                at = sum(w*v for w,v in zip(normal[N:],a))
                atp = sum(w*v for w,v in zip(normal[N:],ap))
                signature.append(int(tx+at>=0)-int(tx+atp>=0))
            sigs.append(tuple(signature))
        assert len(set(sigs)) == 2**N
        for x in range(2**N):
            for xp in range(x):
                witness_count = sum(v!=w for v,w in zip(sigs[x],sigs[xp]))
                assert witness_count > 0
                min_distinct = min(min_distinct,witness_count)
        edge_signatures.append(True)

# Four-point dual for the Q_i ladder pool including every raw feature.
x = (1,0,0,1)
xp = (0,1,1,0)
a = (0,0,0,0)
ap = (0,0,0,1)
inputs = [(x,a),(xp,a),(x,ap),(xp,ap)]
labels = [1,-1,-1,1]
for i in range(N+D):
    assert sum(lab*(xx+aa)[i] for lab,(xx,aa) in zip(labels,inputs)) == 0
for i in range(k):
    table_labels = [c for c in range(N) if (c >> (k-1-i)) & 1]
    for sigma in product((-1,1),repeat=m):
        neg = sigma.count(-1)
        pos = m-neg
        for r in range(-neg+1,N//2+pos+1):
            values = []
            for xx,aa in inputs:
                Q = sum(xx[c] for c in table_labels)
                L = sum(s*v for s,v in zip(sigma,aa[i*m:(i+1)*m]))
                values.append(int(Q+L>=r))
            assert sum(lab*v for lab,v in zip(labels,values)) == 0

multi_rectangle_cases = 0
for size in range(3,15):
    for h in range(1,size-1):
        for ell in range(1,size-h):
            exact = Fraction(0)
            for bias_count in (0,1):
                remaining = size-h-ell+bias_count
                witness_count = 0
                for hb in range(h+1):
                    B = 2*hb-h
                    for lc in range(ell+1):
                        C = 2*lc-ell
                        for ur in range(remaining+1):
                            U = 2*ur-remaining
                            vals = [int(v>=0) for v in
                                    (U+B+C,U-B+C,U+B-C,U-B-C)]
                            if vals[0]-vals[1]-vals[2]+vals[3]:
                                witness_count += comb(h,hb)*comb(ell,lc)*comb(remaining,ur)
                exact += Fraction(witness_count,2**(size+bias_count+1))
            chosen_bias = (size-ell)%2
            M = size-ell+chosen_bias
            pc,p0 = central_conditional(M,h)
            c = 1 if ell%2 else 2
            pC = Fraction(comb(ell,(ell+c)//2),2**ell)
            lower = pC*pc*(1-p0)/4
            assert exact >= lower > 0, (size,h,ell,exact,lower)
            multi_rectangle_cases += 1

result = {
    'Authors':'Christian Reitwiessner',
    'hypergeometric_bound_cases':len(bounds),
    'exact_rectangle_probabilities':rectangles,
    'ladder_identity_cases':ladder_checks,
    'multi_coordinate_rectangle_cases':multi_rectangle_cases,
    'full_pool':{'k':k,'m':m,'gates':R,'edges':len(edge_signatures),
                 'table_pairs_per_edge':comb(2**N,2),
                 'minimum_witness_gates':min_distinct},
    'four_point_dual':'passed',
    'status':'All exact finite checks passed; asymptotic claims require report proofs.'
}
(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({key:value for key,value in result.items() if key!='exact_rectangle_probabilities'},indent=2))
