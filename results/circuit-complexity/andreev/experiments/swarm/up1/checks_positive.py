# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Exact checks of sparse lookup and depth-two guarded composition."""
from itertools import product, combinations
from math import ceil, log
from random import Random
from pathlib import Path
import json


def chi(s,c):
    return -1 if (s&c).bit_count()%2 else 1


def phi(u):
    return -u if u%2 else u


def stair(u,lo,hi):
    return phi(lo)+sum((phi(t)-phi(t-1))*(u>=t) for t in range(lo+1,hi+1))


def sparse_score(Q,ones,counts,m,h,raw=False):
    value=0
    for S in Q:
        L=sum(chi(S,c) for c in ones)
        t=sum(s for i,s in enumerate(counts) if S>>i&1)
        if raw:
            M=S.bit_count()*m
            value+=stair(2*L+t,-2*h,2*h+M)-stair(t,0,M)
        else:
            value+=2*L*(-1 if t%2 else 1)
    return value-len(Q)


def guard_feature(z,U,r,weights,theta):
    L=sum(w*b for w,b in zip(weights,z))
    B=sum(abs(w) for w in weights)+abs(theta)+1
    return int(B*(U-r)+L-theta>=0)-int(U>=r+1)


def main():
    rng=Random(7112026)
    kernel_results=[]
    for k,h in [(8,1),(10,2),(12,3)]:
        N=1<<k
        q=min(N,ceil(18*h*h*log(4*N)))
        for attempt in range(100):
            Q=list(range(N)) if q==N else [rng.randrange(N) for _ in range(q)]
            deviations=[sum(chi(S,d) for S in Q) for d in range(1,N)]
            maxdev=max(map(abs,deviations))
            if 3*h*maxdev<=q:
                break
        else:
            raise AssertionError('No sampled code found within deterministic attempt budget')
        # Exact empirical-bias check certifies every sparse table by the proof.
        assert 3*h*maxdev<=q
        for _ in range(100):
            ones=rng.sample(range(N),rng.randrange(h+1))
            counts=[rng.randrange(4) for _ in range(k)]
            b=sum((s%2)<<i for i,s in enumerate(counts))
            score=sparse_score(Q,ones,counts,3,h)
            assert (score>=0)==(b in ones)
        kernel_results.append({'k':k,'h':h,'q':q,'attempt':attempt,
                               'max_abs_nonzero_character_sum':maxdev})
    sparse_cases=0
    for k,m,h in [(2,3,1),(3,2,2),(3,3,1)]:
        N=1<<k
        Q=list(range(N))
        for weight in range(h+1):
            for ones in combinations(range(N),weight):
                for counts in product(range(m+1),repeat=k):
                    b=sum((s%2)<<i for i,s in enumerate(counts))
                    direct=sparse_score(Q,ones,counts,m,h)
                    raw=sparse_score(Q,ones,counts,m,h,True)
                    assert direct==raw and (raw>=0)==(b in ones)
                    sparse_cases+=1
    guard_cases=0
    for d in range(1,8):
        for _ in range(10):
            weights=[rng.randrange(-5,6) for _ in range(d)]
            theta=rng.randrange(-10,11)
            for z in product((0,1),repeat=d):
                U=sum(z[:max(1,d//2)])
                g=int(sum(w*b for w,b in zip(weights,z))>=theta)
                for r in range(-1,d+1):
                    v=guard_feature(z,U,r,weights,theta)
                    assert v==int(U==r)*g
                    guard_cases+=1
    # Replace an arbitrary incorrect score by a correct lookup score on |x|<=1.
    # Compile every bottom term of the replacement difference using the lemma.
    k,m,h=2,2,1
    N=1<<k
    D=N+k*m
    Q=list(range(N))
    h1_const=-len(Q)
    h1_terms=[]
    for S in Q:
        M=S.bit_count()*m
        form=[2*chi(S,c) for c in range(N)]+[int(S>>i&1) for i in range(k) for _ in range(m)]
        tform=[0]*N+[int(S>>i&1) for i in range(k) for _ in range(m)]
        h1_const+=phi(-2*h)-phi(0)
        for t in range(-2*h+1,2*h+M+1):
            h1_terms.append((phi(t)-phi(t-1),form,t))
        for t in range(1,M+1):
            h1_terms.append((-(phi(t)-phi(t-1)),tform,t))
    h0_const=3
    h0_terms=[(rng.randrange(-4,5),[rng.randrange(-3,4) for _ in range(D)],rng.randrange(-5,6))
              for _ in range(7)]
    diff_terms=h1_terms+[(-v,w,t) for v,w,t in h0_terms]
    diff_const=h1_const-h0_const
    hybrid_cases=0
    for z in product((0,1),repeat=D):
        U=sum(z[:N])
        h0=h0_const+sum(v*(sum(wi*zi for wi,zi in zip(w,z))>=t) for v,w,t in h0_terms)
        h1=h1_const+sum(v*(sum(wi*zi for wi,zi in zip(w,z))>=t) for v,w,t in h1_terms)
        guarded=diff_const*int(U<=h)
        guarded+=sum(v*guard_feature(z,U,r,w,t) for r in range(h+1) for v,w,t in diff_terms)
        score=h0+guarded
        assert score==(h1 if U<=h else h0)
        if U<=h:
            b=sum((sum(z[N+i*m:N+(i+1)*m])%2)<<i for i in range(k))
            assert (score>=0)==bool(z[b])
        hybrid_cases+=1
    result={'authors':'Christian Reitwiessner','status':'all exact checks passed',
            'sampled_sparse_codes':kernel_results,'exhaustive_sparse_raw_gate_cases':sparse_cases,
            'guard_identity_cases':guard_cases,'full_raw_hybrid_cases':hybrid_cases}
    Path(__file__).with_name('checks_positive.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
