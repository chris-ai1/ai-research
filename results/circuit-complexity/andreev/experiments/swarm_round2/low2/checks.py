# Copyright (c) 2026 Christian Reitwiessner. All rights reserved.
# Authors: Christian Reitwiessner
"""Exact guardrails for LOW2 round-two identities; no asymptotic inference."""
from itertools import product
from fractions import Fraction as Q
from pathlib import Path
import json
import random

rng = random.Random(2112026)
counts = {"paired_audit": 0, "compiler_inputs": 0, "near_equal_ratios": 0,
          "semantic_stability": 0, "one_survivor_parity": 0,
          "compiled_partial_parity": 0}
for d in range(2, 6):
    for _ in range(40):
        sig = [rng.choice((-1, 1)) for _ in range(2*d)]
        served = []
        for t in product((-1, 1), repeat=d):
            live = [sig[i]+t[i]*sig[d+i] for i in range(d)]
            if all(live): served.append(t)
            else:
                threshold = rng.randint(-2*d, 2*d)
                correlation = sum(
                    (1 if sum(live[i]*z[i] for i in range(d)) >= threshold else 0)
                    * __import__('math').prod(z)
                    for z in product((-1, 1), repeat=d))
                assert correlation == 0
            counts['paired_audit'] += 1
        assert served == [tuple(sig[i]*sig[d+i] for i in range(d))]

for M in range(1, 6):
    for _ in range(25):
        alpha = [rng.randint(-4, 4) for _ in range(2)]
        gamma = [rng.randint(-4, 4) for _ in range(M)]
        theta = Q(rng.randint(-8, 8), 2)
        Lbound = sum(map(abs,alpha+gamma))+abs(theta)
        B = int(1000*(Lbound+1))
        assert Q(B+max(gamma), B+min(gamma)) <= Q(1001,1000)
        counts['near_equal_ratios'] += 1
        for v in product((0,1), repeat=M+2):
            L = sum(a*b for a,b in zip(alpha+gamma, v))-theta
            U = sum(v[2:])
            compiled = sum(B*(U-r)+L >= 0 for r in range(M+1))-U
            assert compiled == (L >= 0)
            counts['compiler_inputs'] += 1
        sig = [rng.choice((-1,1)) for _ in range(M)]
        theta0 = Q(2*rng.randint(-M,M)+1,2)
        perturb = [Q(rng.randint(-2,2), 10*M) for _ in range(M)]
        assert sum(map(abs,perturb)) < Q(1,2)
        for z in product((-1,1),repeat=M):
            old = sum(s*t for s,t in zip(sig,z))-theta0
            new = old+sum(e*t for e,t in zip(perturb,z))
            assert (old >= 0) == (new >= 0)
            counts['semantic_stability'] += 1

for d in range(2,7):
    for z in product((0,1),repeat=d):
        score = sum((-2)**len(U) * int(all(z[i] for i in U))
                    for mask in range(1<<d)
                    for U in [[i for i in range(d) if mask>>i&1]])
        assert score == (-1)**sum(z)
        counts['one_survivor_parity'] += 1

# Compile the usual selected-count parity staircase on all 2d raw bits.
for d in range(2,5):
    M = 2*d
    B = 10000*M
    for a in product((0,1),repeat=M):
        U, s = sum(a), sum(a[:d])
        score = 1
        for h in range(1,d+1):
            original = int(s>=h)
            expanded = sum(B*(U-r)+s-h >= 0 for r in range(M+1))-U
            assert original == expanded
            score += 2*((-1)**h)*expanded
        assert score == (-1)**s
        counts['compiled_partial_parity'] += 1
# Full raw near-equal two-scale Walsh staircase (UP2 mechanism).
counts['near_equal_walsh_scores'] = 0
counts['near_equal_raw_bottom_evaluations'] = 0
k,m,N,M = 2,2,4,4
phi = lambda u: (-1 if u%2 else 1)*u
for B in (2,4,20):
    for x in product((0,1),repeat=N):
        X = [sum(((-1)**((T&c).bit_count()))*(1-2*x[c]) for c in range(N))
             for T in range(N)]
        for a in product((0,1),repeat=M):
            score = X[0]
            for T in range(1,N):
                w=[(B-1 if (T>>(i//m))&1 else B) * (1 if (i+T)%3 else -1)
                   for i in range(M)]
                L=sum(wi*ai for wi,ai in zip(w,a))
                low=sum(min(wi,0) for wi in w)
                high=sum(max(wi,0) for wi in w)
                def staircase(value,lo,hi):
                    counts['near_equal_raw_bottom_evaluations'] += hi-lo
                    return phi(lo)+sum((phi(r)-phi(r-1))*int(value>=r)
                                       for r in range(lo+1,hi+1))
                compiled=staircase(X[T]+L,low-N,high+N)-staircase(L,low,high)
                assert compiled==X[T]*((-1)**sum(a[i] for i in range(M) if T>>(i//m)&1))
                score+=compiled
            b=(sum(a[:m])%2)+2*(sum(a[m:])%2)
            assert score==N*(1-2*x[b])
            counts['near_equal_walsh_scores'] += 1

out = {'authors': 'Christian Reitwiessner', 'status': 'VERIFIED', 'checks': counts}
Path(__file__).with_name('checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
