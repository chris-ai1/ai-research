#!/usr/bin/env python3
# Authors: Christian Reitwiessner
"""Exact guardrails for the review-derived score-difference and slicing transfers."""
import itertools
import json
import random
from pathlib import Path

print('Authors: Christian Reitwiessner')
root=Path(__file__).resolve().parent
out={'authors':'Christian Reitwiessner'}
# Complementing all bits swaps the two upward edge classes in even dimension.
count=0
for M in (2,4,6,8):
    for x in itertools.product((0,1),repeat=M):
        for i in range(M):
            if x[i]: continue
            y=list(x);y[i]=1
            reflected_lower=tuple(1-v for v in y)
            assert sum(reflected_lower)%2 != sum(x)%2
            count+=1
out['reflection_edge_cases']=count
# A correct T1 circuit for A_(1,m) obtained from the parity staircase.
# Verify EVERY raw input and its derived parity score, with exact integers.
count=0; differences=0
for m in range(1,11):
    S=(m+1)//2
    def score(a,x):
        t=sum(a)
        return 2*t+4*x[0]+2*x[1]-4*sum(t+x[0]>=2*j for j in range(1,S+1))-3
    for a in itertools.product((0,1),repeat=m):
        for x in itertools.product((0,1),repeat=2):
            assert int(score(a,x)>=0)==x[sum(a)%2]
            count+=1
        derived=2-4*sum(int(sum(a)+1>=2*j)-int(sum(a)>=2*j) for j in range(1,S+1))
        assert score(a,(1,0))-score(a,(0,1))==derived==2*(-1)**sum(a)
        differences+=1
out['A1_raw_inputs']=count
out['A1_difference_parity_inputs']=differences
# Independently verify cancellation and <=2g expansion for arbitrary T1 scores
# on two single-one tables, without assuming that these random scores are correct.
rng=random.Random(20261109)
k,m,N=3,3,8
count=0
for trial in range(50):
    gates=[]
    for j in range(17):
        d=rng.randrange(-1,N)
        alpha=0 if d<0 else rng.choice([-3,-2,-1,1,2,3])
        address=[rng.randrange(-3,4) for _ in range(k*m)]
        theta=rng.randrange(-5,6)
        v=rng.randrange(-4,5)
        gates.append((d,alpha,address,theta,v))
    u=[rng.randrange(-3,4) for _ in range(N)]
    ua=[rng.randrange(-3,4) for _ in range(k*m)]
    tau=rng.randrange(-5,6)
    def score_one(d,a):
        return u[d]+sum(p*q for p,q in zip(ua,a))-tau+sum(
            v*int(sum(p*q for p,q in zip(w,a))+alpha*int(dj==d)>=th)
            for dj,alpha,w,th,v in gates)
    # block zero matching, with labels represented by the low-order bit.
    for d in range(0,N,2):
        e=d+1
        fixed=[0]*(k*m)
        for i in range(1,k): fixed[i*m]=(d>>i)&1
        for a0 in itertools.product((0,1),repeat=m):
            a=list(a0)+fixed[m:]
            derived=u[d]-u[e]
            for dj,alpha,w,th,v in gates:
                if dj not in (d,e): continue
                f=sum(p*q for p,q in zip(w,a))
                derived+=v*(int(f+alpha*int(dj==d)>=th)-int(f+alpha*int(dj==e)>=th))
            assert derived==score_one(d,a)-score_one(e,a)
            count+=1
out['random_score_difference_cases']=count
# An adversarial fixed arrangement with constant drift and constant split rate.
for m in (16,64,256,1024):
    w=[1,-1]*(m//4)+[1]*(m//2)
    f=0; splits=0
    for step in w:
        splits+=int(min(f,f+step)<.5<=max(f,f+step))
        f+=step
    assert f==m//2 and splits>=m//2
out['fixed_arrangement_counterexample']='delta=1/2, W=1, split>=1/2 for all tested m'
(root/'transfer_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
print('All exact checks passed.')
