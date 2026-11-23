#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Independent exact checks of the revised paper's scores and gate accounting.

The exact gates are symmetric within each address block. Enumerating every
block count therefore covers every raw address arrangement, not just samples.
These finite checks guard the algebra; the paper supplies the all-size proofs.
"""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import random

def construction(k,m):
    N=1<<k;n=N+k*m;alpha=(m-1)//2;B=n+2
    R=2*(N-1)+2*alpha*k+k*m;C=N*(R+4)
    gates={}
    def gate(table,blocks,threshold,weight):
        key=tuple(table)+tuple(blocks)+(threshold,)
        gates[key]=gates.get(key,0)+weight
    zero=[0]*N;unit=lambda i:[int(j==i) for j in range(k)]
    for S in range(1,N):
        blocks=[(S>>i)&1 for i in range(k)]
        W=[int((S&c).bit_count()%2)+alpha*int(c>0 and c&(c-1)==0 and S&c!=0) for c in range(N)]
        kap=-4*(2*alpha+1)*(k-2*S.bit_count())
        for level in range(1,N+2*alpha*S.bit_count()+m*S.bit_count()+1,2):
            gate([2*v for v in W],blocks,level,-8*level+kap)
        for j in range(1,m*S.bit_count()//2+1):
            gate([B]+[0]*(N-1),blocks,B+2*j,-4*C//N)
    ww=[2*int(c!=0)+2*alpha*int(c>0 and c&(c-1)==0) for c in range(N)]
    for level in range(1,R+1):gate(ww,[1]*k,level,(N//2)*(2*level-1))
    for i in range(k):
        for level in range(1,m+1):
            gate(zero,unit(i),level,(N//2)*(2*level-1))
            gate([B*int(c==1<<i) for c in range(N)],unit(i),B+level,2*N*(1+alpha))
    for level in range(1,k*m+1):gate([B]+[0]*(N-1),[1]*k,B+level,C)
    gates={key:value for key,value in gates.items() if value}
    direct=[4*N*int(c!=0)-2*N*(alpha*alpha+1)*int(c>0 and c&(c-1)==0)-C*int(c==0) for c in range(N)]
    direct += [-2*alpha*N]*k
    def evaluate(x,s):
        point=tuple(x)+tuple(s)
        return 2*N+sum(v*z for v,z in zip(direct,point))+sum(v for key,v in gates.items() if sum(a*b for a,b in zip(key[:-1],point))>=key[-1])
    def closed(x,s):
        b=sum((v%2)<<i for i,v in enumerate(s))
        w=2*sum(x[1:])+2*alpha*sum(x[1<<i] for i in range(k))+sum(s)
        if b==0:return N*(w+2)-C*x[0]
        if b&(b-1)==0:
            i=b.bit_length()-1
            return 2*N*(1+alpha)*(1-x[b])-N*s[i]
        return N*(1-2*x[b])
    bound=N*(N-1)//2+k*N*(m+alpha)//2+2*(N-1)+2*alpha*k+3*k*m+(k*m+1)//2
    assert len(gates)<=bound
    return evaluate,closed,len(gates),bound

def exact_checks():
    records=[]
    for k in range(1,4):
        N=1<<k
        for m in range(1,5):
            evaluate,closed,gates,bound=construction(k,m);cases=0;margin=10**9
            for x in product((0,1),repeat=N):
                for s in product(range(m+1),repeat=k):
                    P=evaluate(x,s);assert P==closed(x,s),(k,m,x,s,P,closed(x,s))
                    b=sum((v%2)<<i for i,v in enumerate(s))
                    margin=min(margin,(1-2*x[b])*P);cases+=1
            assert margin>=N
            records.append(dict(k=k,m=m,bottoms=gates,bound=bound,cases=cases,minimum_signed_score=margin))
    rng=random.Random(73)
    for k,m in [(4,4),(5,6),(6,10),(8,32)]:
        evaluate,closed,gates,bound=construction(k,m);N=1<<k
        for _ in range(20):
            x=[rng.randrange(2) for _ in range(N)];s=[rng.randrange(m+1) for _ in range(k)]
            assert evaluate(x,s)==closed(x,s)
        records.append(dict(k=k,m=m,bottoms=gates,bound=bound,sampled_cases=20))
    return records

def mask_checks():
    k=m=2;N=4;results=[]
    phi=lambda u:(-1 if u%2 else 1)*u
    for R in (1,2,3,4):
        def f(u):return phi(u) if abs(u)<=R else 0
        for U in range(-10,11):
            assert sum((f(l)-f(l-1))*int(U>=l) for l in range(-R,R+2))==f(U)
        crosses={(s,t):0 for s in range(1,N) for t in range(s+1,N)}
        diagonal=Fraction(0)
        for x in product((0,1),repeat=N):
            X={S:sum((-1 if (S&c).bit_count()%2 else 1)*(1-2*x[c]) for c in range(N)) for S in range(1,N)}
            for a in product((0,1),repeat=k*m):
                means={}
                for S in range(1,N):
                    positions=[i*m+t for i in range(k) if S>>i&1 for t in range(m)]
                    M=len(positions);h=M//2;errors=[]
                    for z in product((0,1),repeat=M):
                        d=sum(a[i]^bit for i,bit in zip(positions,z))-h
                        eta=-1 if (sum(z)+h)%2 else 1
                        errors.append(eta*(f(X[S]+d)+f(X[S]-d)-phi(X[S]+d)-phi(X[S]-d)))
                    means[S]=Fraction(sum(errors),len(errors))
                    diagonal+=Fraction(sum(e*e for e in errors),len(errors))
                for S,T in crosses:crosses[S,T]+=means[S]*means[T]
        assert all(v==0 for v in crosses.values())
        results.append(dict(radius=R,cross_moments_zero=True,mean_square_error=str(diagonal/256)))
    return results

if __name__=='__main__':
    out=dict(Authors='Christian Reitwiessner',exact_construction=exact_checks(),masked_moments=mask_checks(),
             scope='Finite exact checks of raw gate formulas and paper algebra; not a substitute for universal proofs')
    Path(__file__).with_name('upper_update_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
