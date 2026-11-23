"""Exhaustive check of the ring lemma for k=2: every line cuts a corner of at most 4 of the 4(m-1) boundary unit
squares of the m x m grid of unit squares (vertices {0..m}^2).  All combinatorial line types are enumerated
(perturbations of lines through two vertices), exact integer arithmetic."""
import sys; sys.path.insert(0,'/tmp/pydeps')
import numpy as np
def check(m):
    V=np.array([(a,b) for a in range(m+1) for b in range(m+1)],dtype=np.int64)
    idx={(a,b):i for i,(a,b) in enumerate(map(tuple,V))}
    sq=[(a,b) for a in range(m) for b in range(m)]
    bnd=np.array([a in (0,m-1) or b in (0,m-1) for a,b in sq])
    corners=np.array([[idx[(a,b)],idx[(a+1,b)],idx[(a,b+1)],idx[(a+1,b+1)]] for a,b in sq])
    best=0; besttot=0
    n=len(V)
    for i in range(n-1):
        d=V[i+1:]-V[i]                       # all partners j>i at once
        nrm=np.stack([-d[:,1],d[:,0]],1)
        f0=(V-V[i])@nrm.T                    # (n_vertices, n_pairs)
        f1=(V-V[i])@d.T
        for t1 in (1,-1):
            for t2 in (1,-1):
                s=np.where(f0!=0,np.sign(f0),np.where(f1!=0,np.sign(t1*f1),t2))
                side=(s>0).astype(np.int64)
                cnt=side[corners].sum(axis=1)           # (n_squares, n_pairs)
                cut=(cnt==1)|(cnt==3)
                best=max(best,int((cut&bnd[:,None]).sum(0).max()))
                besttot=max(besttot,int(cut.sum(0).max()))
    return best,besttot
for m in map(int,sys.argv[1:]):
    b,t=check(m); print(f'm={m}: max boundary squares cut by one line = {b} (lemma: <=4); max squares cut = {t} (2m-1={2*m-1})',flush=True)
