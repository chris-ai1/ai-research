# Copyright (c) 2026 Christian Reitwiessner. All rights reserved.
# Authors: Christian Reitwiessner
"""Exact sanity checks for the Krawtchouk and coherence proof identities."""
from math import comb
from fractions import Fraction as Q
import random
import json
from pathlib import Path

def choose(n,k):
    return comb(n,k) if 0 <= k <= n else 0

def K(d,x,n):
    return sum((-1)**u*choose(x,u)*choose(n-x,d-u) for u in range(d+1))

def fourier_scaled(M,d,t):
    return sum((-1)**u*choose(d,u)*choose(M-d,v)
               for u in range(d+1) for v in range(M-d+1) if u+v>=t)

counts={"coefficient_identity":0,"consecutive_nonvanishing":0,"recurrence":0,"mask_generating_identity":0,"normalized_two_degree_coherence":0}
for M in range(2,25):
    for t in range(1,M+1):
        for d in range(1,M+1):
            lhs=fourier_scaled(M,d,t)*comb(M-1,d-1)
            rhs=-comb(M-1,t-1)*K(d-1,t-1,M-1)
            assert lhs==rhs
            counts['coefficient_identity']+=1
        for r in range(1,M):
            assert K(r-1,t-1,M-1)!=0 or K(r,t-1,M-1)!=0
            counts['consecutive_nonvanishing']+=1
        for r in range(2,M):
            n,x=M-1,t-1
            assert r*K(r,x,n)==(n-2*x)*K(r-1,x,n)-(n-r+2)*K(r-2,x,n)
            counts['recurrence']+=1
for M in range(2,81):
    for s in range(M%2,M+1,2):
        for d in range(1,min(9,M+1)):
            lhs=K(d,(M-s)//2,M)
            rhs=sum((-1)**b*choose((M-s)//2,b)*choose(s,d-2*b) for b in range(d//2+1))
            assert lhs==rhs
            counts['mask_generating_identity']+=1
rng=random.Random(561833)
for _ in range(300):
    M=rng.randint(8,40)
    r=rng.randint(2,min(7,M-1))
    t,u=rng.randint(1,M),rng.randint(1,M)
    x=rng.randint(0,M)
    a,b=[fourier_scaled(M,d,t) for d in (r,r+1)]
    c,d=[fourier_scaled(M,deg,u) for deg in (r,r+1)]
    q0,q1=comb(M,r),comb(M,r+1)
    ip=a*c*K(r,x,M)+b*d*K(r+1,x,M)
    nj=a*a*q0+b*b*q1
    nl=c*c*q0+d*d*q1
    delta=max(abs(Q(K(r,x,M),q0)),abs(Q(K(r+1,x,M),q1)))
    assert ip*ip <= delta*delta*nj*nl
    counts['normalized_two_degree_coherence']+=1
out={"authors":"Christian Reitwiessner","status":"exact finite identities verified; asymptotic theorem relies on written proof","checks":counts}
Path(__file__).with_name('fourier_identity_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
