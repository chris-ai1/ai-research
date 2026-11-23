# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Independent finite checks of masks, monotone cubes, and literal pairing."""
import itertools as it
import json
import random
rng=random.Random(9112026)
results={}
phi=lambda u:(1 if u%2==0 else -1)*u

mask_cases=0
for m in [1,2,3]:
    k=2;N=4
    active={S:[i*m+j for i in range(k) if S>>i&1 for j in range(m)] for S in range(1,N)}
    masks={S:list(it.product(range(2),repeat=len(active[S]))) for S in active}
    for R in [1,2,3,5]:
        cross={(1,2):0,(1,3):0,(2,3):0}
        for x in it.product(range(2),repeat=N):
            X={S:sum((-1)**((S&c).bit_count()+x[c]) for c in range(N)) for S in active}
            for a in it.product(range(2),repeat=k*m):
                means={}
                for S,coords in active.items():
                    M=len(coords);t=sum(a[j] for j in coords);total=0
                    for z in masks[S]:
                        D=sum(a[j]^h for j,h in zip(coords,z))-M//2
                        eta=(-1)**(sum(z)+M//2)
                        exact=eta*(phi(X[S]+D)+phi(X[S]-D))
                        assert exact==2*X[S]*(-1)**t
                        trunc=eta*sum(phi(u) for u in [X[S]+D,X[S]-D] if abs(u)<=R)
                        total+=trunc-exact
                        mask_cases+=1
                    means[S]=total
                for S,T in cross:cross[S,T]+=means[S]*means[T]
        assert all(v==0 for v in cross.values())
results['mask_identity_cases']=mask_cases
results['cross_character_sums']='exactly zero for each pair, k=2, m=1,2,3, radii 1,2,3,5'

# Arbitrary unequal coherent weights, every threshold at/around attained values.
cubecases=0
for k in range(1,5):
    for m in range(1,5):
        cubes=list(it.product(range(m),repeat=k))
        for trial in range(20):
            ori=[rng.choice([-1,1]) for _ in range(k)]
            weights=[[ori[i]*rng.randrange(5) for _ in range(m)] for i in range(k)]
            pref=[[sum(w[:h]) for h in range(m+1)] for w in weights]
            intervals=[]
            for q in cubes:
                lo=tuple(q[i]+int(ori[i]<0) for i in range(k))
                hi=tuple(q[i]+int(ori[i]>0) for i in range(k))
                intervals.append((sum(pref[i][lo[i]] for i in range(k)),sum(pref[i][hi[i]] for i in range(k))))
            values=set(v for pair in intervals for v in pair)
            thresholds=sorted({2*v+d for v in values for d in [-1,0,1]})
            for th2 in thresholds:
                split=sum(2*lo<th2<=2*hi for lo,hi in intervals)
                assert split<=m**k-(m-1)**k;cubecases+=1
            starts=[q for q in cubes if any(not 0<=q[i]-ori[i]<m for i in range(k))]
            covered=[]
            for start in starts:
                line=[];q=start
                while all(0<=v<m for v in q):
                    line.append(q);q=tuple(q[i]+ori[i] for i in range(k))
                covered+=line
                for qa,qb in zip(line,line[1:]):
                    assert tuple(qa[i]+int(ori[i]>0) for i in range(k))==tuple(qb[i]+int(ori[i]<0) for i in range(k))
            assert len(covered)==len(set(covered))==m**k
            assert len(starts)==m**k-(m-1)**k
results['coherent_cube_threshold_tests']=cubecases

paircases=0
for d in range(2,6):
    signs=list(it.product([-1,1],repeat=d))
    for sig in signs:
        for tau in signs:
            full=[]
            for t in signs:
                coeff=[sig[i]+t[i]*tau[i] for i in range(d)]
                if all(coeff):full.append(t)
                for th in [-2*d,0,2*d]:
                    corr=sum(((-1)**sum(z<0 for z in v))*int(sum(c*z for c,z in zip(coeff,v))>=th) for v in signs)
                    if not all(coeff):assert corr==0
                    paircases+=1
            assert full==[tuple(sig[i]*tau[i] for i in range(d))]
results['pairing_and_missing_coordinate_correlation_checks']=paircases
print(json.dumps(results,indent=2))
