# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Independent checks written from the compact paper, not its checker."""
import itertools as it
import math
import random
import json
from collections import defaultdict

rng = random.Random(1152026)
results = {}

def score_check(k,m,x,s):
    N=1<<k; a=(m-1)//2
    z=sum(x[1:]); E=sum(x[1<<i] for i in range(k)); sig=sum(s)
    w=2*z+2*a*E+sig; R=2*(N-1)+2*a*k+k*m; C=N*(R+4)
    b=sum((v%2)<<i for i,v in enumerate(s))
    rsum=h2=quad=four=kshift=kW=kt=0
    for S in range(1,N):
        I=[i for i in range(k) if S>>i&1]
        Y=sum(x[c] for c in range(N) if (S&c).bit_count()%2)
        W=Y+a*sum(x[1<<i] for i in I)
        t=sum(s[i] for i in I); h=(t+1)//2
        kap=-4*(2*a+1)*(k-2*len(I))
        rsum+=-8*(W+h)**2+kap*(W+h)
        h2+=8*h*h; quad+=8*(W*W+W*t); four+=4*W*(-1)**t
        kshift+=kap*(2*h-t); kW+=kap*W; kt+=kap*t
    singles=sum(x[1<<i]*s[i] for i in range(k))
    assert four == 2*N*(b==0)*z-2*N*(b!=0)*x[b]+2*a*N*sum(x[1<<i]*((b==0)-(b==1<<i)) for i in range(k))
    assert quad == N//2*(w*w-sig*sig)+2*N*z+(4*a+2*a*a)*N*E+2*N*(1+a)*singles
    assert h2 == N//2*(sig*sig+sum(v*v for v in s))+N*(sig+1)*(b!=0)+N*sum(s[i]*(b==1<<i) for i in range(k))
    assert kshift == 2*N*(2*a+1)*sum(b==1<<i for i in range(k))
    assert kW == 2*N*(2*a+1)*(1+a)*E
    assert kt == 2*N*(2*a+1)*sig
    P=2*N+rsum+N//2*(w*w+sum(v*v for v in s))+4*N*z-2*N*(a*a+1)*E-2*a*N*sig+2*N*(1+a)*singles-C*x[0]*(b==0)
    if b==0: closed=N*(w+2)-C*x[0]
    elif b.bit_count()==1:
        i=b.bit_length()-1; closed=2*N*(1+a)*(1-x[b])-N*s[i]
    else: closed=N*(1-2*x[b])
    assert P==closed and P*(1-2*x[b])>=N
    return P

cases=0
for k,ms in [(1,range(1,9)),(2,range(1,9)),(3,range(1,6))]:
    for m in ms:
        for x in it.product(range(2),repeat=1<<k):
            for s in it.product(range(m+1),repeat=k):
                score_check(k,m,x,s); cases+=1
for k in range(4,9):
    for m in [1,2,3,4,7,8,(1<<k)//k]:
        for _ in range(50):
            x=[rng.randrange(2) for _ in range(1<<k)]
            s=[rng.randrange(m+1) for _ in range(k)]
            score_check(k,m,x,s); cases+=1
results['exact_score_identity_and_margin_cases']=cases

# Explicit list of raw affine gates, with equal address weights represented by s_i.
def compile_score(k,m):
    N=1<<k; a=(m-1)//2; n=N+k*m; B=n+2
    R=2*(N-1)+2*a*k+k*m; C=N*(R+4)
    gates=[]; aff=[0]*(N+k); const=2*N
    def gate(cf,th,wt): gates.append((tuple(cf),th,wt))
    for S in range(1,N):
        I=[i for i in range(k) if S>>i&1]
        cf=[2*((S&c).bit_count()%2) for c in range(N)]+[int(i in I) for i in range(k)]
        for i in I: cf[1<<i]+=2*a
        kap=-4*(2*a+1)*(k-2*len(I))
        for th in range(1,N+2*a*len(I)+m*len(I)+1,2): gate(cf,th,-8*th+kap)
    w=[2*int(c!=0) for c in range(N)]+[1]*k
    for i in range(k): w[1<<i]+=2*a
    for th in range(1,R+1): gate(w,th,N//2*(2*th-1))
    for i in range(k):
        cf=[0]*(N+k);cf[N+i]=1
        for th in range(1,m+1):gate(cf,th,N//2*(2*th-1))
        cf[1<<i]=B
        for ell in range(1,m+1):gate(cf,B+ell,2*N*(1+a))
    cf=[B]+[0]*(N-1)+[1]*k
    for ell in range(1,k*m+1):gate(cf,B+ell,C)
    for S in range(1,N):
        cf=[B]+[0]*(N-1)+[int(S>>i&1) for i in range(k)]
        for j in range(1,m*S.bit_count()//2+1):gate(cf,B+2*j,-4*(R+4))
    for c in range(1,N):aff[c]+=4*N
    for i in range(k):aff[1<<i]-=2*N*(a*a+1);aff[N+i]-=2*a*N
    aff[0]-=C
    expected=N*(N-1)//2+k*N*(m+a)//2+2*(N-1)+2*a*k+3*k*m+(k*m+1)//2
    assert len(gates)-(k*m)//2==expected
    merged=defaultdict(int)
    for cf,th,wt in gates:merged[(cf,th)]+=wt
    assert sum(wt!=0 for wt in merged.values())<=expected
    assert all(isinstance(wt,int) for wt in merged.values())
    for cf,th in merged:
        assert all(cf[N+i]>=0 for i in range(k))
    return const,aff,merged

compiled_cases=0
for k in range(1,6):
    for m in range(1,8):
        const,aff,gates=compile_score(k,m)
        for _ in range(80):
            x=[rng.randrange(2) for _ in range(1<<k)];s=[rng.randrange(m+1) for _ in range(k)];inp=x+s
            P=const+sum(c*t for c,t in zip(aff,inp))+sum(wt for (cf,th),wt in gates.items() if sum(c*t for c,t in zip(cf,inp))>=th)
            assert P==score_check(k,m,x,s)
            compiled_cases+=1
results['explicit_raw_gate_evaluations']=compiled_cases

# Majority vote, including zero ties, checked independently by enumerating table bits.
maj={}
for L in [1,2,4,8,16]:
    wins=tot=0
    for x in it.product(range(2),repeat=L):
        vote=int(2*sum(x)>L); wins+=vote==x[0];tot+=1
    p=1 if L==1 else math.comb(L,L//2)/(2**L)
    assert wins/tot==.5+p/2
    assert p>=1/math.sqrt(2*L)
    maj[L]=wins/tot
results['majority_agreements']=maj

# Exact distribution, every relevant integer radius, no subgaussian approximation.
maxratio=(0,None);tailcases=0
for N in [2,4,8,16,32,64]:
    for M in range(1,41):
        dist=defaultdict(float)
        for j in range(N+1):
            for h in range(M+1):
                U=N-2*j+h-M//2
                dist[U]+=math.comb(N,j)*math.comb(M,h)/2**(N+M)
        v=N+M/4
        for R in range(1,max(abs(u) for u in dist)+2):
            tail=sum(u*u*p for u,p in dist.items() if abs(u)>R)
            bd=16*v*math.exp(-R*R/(16*v))
            ratio=tail/bd
            if ratio>maxratio[0]:maxratio=(ratio,[N,M,R])
            assert tail<=bd+1e-12;tailcases+=1
results['tail_checks']={'cases':tailcases,'maximum_ratio':maxratio}

print(json.dumps(results,indent=2))
