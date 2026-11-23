#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Second-review diagnostics, directly transcribed from the revised paper.

Checks the displayed identities individually, finite count arithmetic,
truncated-binomial tails, and complete joint-mask mean squares.
"""
from itertools import product
from math import comb, exp
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import random
import json

rng = random.Random(202611112)
counts = defaultdict(int)
sign = lambda v: 1 if v % 2 == 0 else -1
phi = lambda v: sign(v)*v

def check(k,m,x,s):
    N=2**k
    alpha=(m-1)//2
    z=sum(x[1:]); E=sum(x[1<<i] for i in range(k)); sigma=sum(s)
    w=2*z+2*alpha*E+sigma
    R=2*(N-1)+2*alpha*k+k*m
    C=N*(R+4)
    b=sum((v%2)<<i for i,v in enumerate(s))
    Ws=[]; ts=[]; ks=[]
    for S in range(1,N):
        W=sum(x[c] for c in range(N) if (S&c).bit_count()%2)+alpha*sum(x[1<<i] for i in range(k) if S>>i&1)
        t=sum(s[i] for i in range(k) if S>>i&1)
        kap=-4*(2*alpha+1)*(k-2*S.bit_count())
        Ws.append(W);ts.append(t);ks.append(kap)
        assert 4*W*sign(t)==4*W-8*((2*W+t+1)//2)**2+8*W*W+8*W*t+8*((t+1)//2)**2
    xe_s=sum(x[1<<i]*s[i] for i in range(k))
    assert sum(4*W*sign(t) for W,t in zip(Ws,ts)) == 2*N*(b==0)*z-2*N*(b!=0)*x[b]+2*alpha*N*sum(x[1<<i]*((b==0)-(b==1<<i)) for i in range(k))
    assert 8*sum(W*W+W*t for W,t in zip(Ws,ts)) == (N//2)*(w*w-sigma*sigma)+2*N*z+(4*alpha+2*alpha*alpha)*N*E+2*N*(1+alpha)*xe_s
    assert 8*sum(((t+1)//2)**2 for t in ts) == (N//2)*(sigma*sigma+sum(si*si for si in s))+N*(sigma+1)*(b!=0)+N*sum(s[i]*(b==1<<i) for i in range(k))
    assert sum(kap*(t%2) for kap,t in zip(ks,ts))==2*N*(2*alpha+1)*sum(b==1<<i for i in range(k))
    assert sum(kap*W for kap,W in zip(ks,Ws))==2*N*(2*alpha+1)*(1+alpha)*E
    assert sum(kap*t for kap,t in zip(ks,ts))==2*N*(2*alpha+1)*sigma
    assert N*x[0]*(b==0)==N*x[0]-N*x[0]*sigma+4*sum(x[0]*(t//2) for t in ts)
    P=2*N+sum(-8*((2*W+t+1)//2)**2+kap*((2*W+t+1)//2) for W,t,kap in zip(Ws,ts,ks))+(N//2)*(w*w+sum(si*si for si in s))+4*N*z-2*N*(alpha*alpha+1)*E-2*alpha*N*sigma+2*N*(1+alpha)*xe_s-C*x[0]*(b==0)
    if b==0:closed=N*(w+2)-C*x[0]
    elif b.bit_count()==1:closed=2*N*(1+alpha)*(1-x[b])-N*s[b.bit_length()-1]
    else:closed=N*(1-2*x[b])
    assert P==closed and (1-2*x[b])*P>=N
    counts['score_identity_inputs']+=1

for k,ms in [(1,range(1,5)),(2,range(1,5)),(3,range(1,4))]:
    for m in ms:
        for x in product((0,1),repeat=2**k):
            for s in product(range(m+1),repeat=k):check(k,m,x,s)
for k in range(1,8):
    for m in [1,2,3,4,7,16,33]:
        for _ in range(30):check(k,m,[rng.randrange(2) for _ in range(2**k)],[rng.randrange(m+1) for _ in range(k)])

for k in range(1,13):
    N=2**k
    for m in range(1,34):
        alpha=(m-1)//2
        main=sum((N+2*alpha*S.bit_count()+m*S.bit_count()+1)//2 for S in range(1,N))
        floor=sum(m*S.bit_count()//2 for S in range(1,N))
        R=2*(N-1)+2*alpha*k+k*m
        gate_sum=main+floor+R+3*k*m-(k*m)//2
        bound=N*(N-1)//2+k*N*(m+alpha)//2+2*(N-1)+2*alpha*k+3*k*m+(k*m+1)//2
        assert gate_sum==bound
        if k*m==N:assert bound+1==5*N*N//4-k*N//2+6*N-2*k-1
        counts['finite_gate_count_parameters']+=1

for N in [2,4,8,16,32,64]:
    for M in range(1,21):
        v=N+M/4
        law=defaultdict(int)
        for j in range(N+1):
            for h in range(M+1):law[N-2*j+h-M//2]+=comb(N,j)*comb(M,h)
        total=2**(N+M)
        for R in range(1,N+M+3):
            tail=sum(u*u*weight for u,weight in law.items() if abs(u)>R)/total
            assert tail<=16*v*exp(-R*R/(16*v))*(1+1e-12)
            counts['binomial_tail_bounds']+=1

# Sum complete independent mask collections, rather than using products of
# conditional means to test the mean-square decomposition itself.
k=2;m=1;N=4
for r in [1,2]:
    q=2**r
    active={S:[i for i in range(r) if S>>i&1] for S in range(1,q)}
    masks={S:list(product((0,1),repeat=len(ids))) for S,ids in active.items()}
    for R in [1,2,3,4,5]:
        cross=defaultdict(int);square=0;diagonal=0;disagree=0;vote_correct=0;trials=0
        for x in product((0,1),repeat=N):
            X={S:sum(sign((S&c).bit_count()+x[c]) for c in range(N)) for S in range(q)}
            for a in product((0,1),repeat=k):
                target=x[a[0]+2*a[1]]
                exact=2*sum(X[S]*sign(sum(a[i] for i in range(r) if S>>i&1)) for S in range(q))
                vote=int(-exact>=(0 if q==N else 2*q))
                for zs in product(*(masks[S] for S in active)):
                    err=[]
                    for S,z in zip(active,zs):
                        D=sum(a[i]^h for i,h in zip(active[S],z))-len(z)//2
                        eta=sign(sum(z)+len(z)//2)
                        us=[X[S]+D,X[S]-D]
                        raw=eta*sum(phi(u) for u in us)
                        truncated=eta*sum(phi(u) for u in us if abs(u)<=R)
                        err.append(truncated-raw)
                    delta=sum(err);square+=delta*delta;diagonal+=sum(e*e for e in err)
                    new=int(-(exact+delta)>=(0 if q==N else 2*q))
                    disagree+=(new!=vote);vote_correct+=(vote==target);trials+=1
                    if new!=vote:assert abs(delta)>=2*q
                    counts['complete_joint_mask_cases']+=1
        assert square==diagonal
        v=N+r*m/4
        assert square/trials<=64*(q-1)*v*exp(-R*R/(16*v))
        assert disagree/trials<=16*v/q*exp(-R*R/(16*v))
        L=N//q
        p=Fraction(1) if L==1 else Fraction(comb(L,L//2),2**L)
        assert Fraction(vote_correct,trials)==Fraction(1,2)+p/2

out={'Authors':'Christian Reitwiessner','status':'PASS','checks':dict(counts),'scope':'Finite diagnostics; mathematical all-size audit is in round2.md.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
