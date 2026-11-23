# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Raw-coordinate exact rank circuits and central-hyperplane covers."""
from itertools import product
from pathlib import Path
import json
META={'Authors':'Christian Reitwiessner','copyright':'Copyright (c) 2026 Christian Reitwiessner'}
OUT=Path(__file__).resolve().parent

def paired_rank(k,m):
    N=1<<k;r=(m+1)//2;H=1<<(r*k)
    rank=[0]*(k*m)
    for p in range(r):
        for i in range(k):rank[i*m+2*p]=1<<(p*k+i)
    gates=[]
    for C in range(H):
        wa=rank.copy();label=0
        for p in range(r):
            label^=(C>>(p*k))&(N-1)
            if 2*p+1<m:
                for i in range(k):wa[i*m+2*p+1]=(2*((C>>(p*k+i))&1)-1)*(1<<(p*k+i))
        gates.append(dict(c=label,table_weight=1,address_weights=wa,threshold=C+1,top_weight=1))
    return dict(META,k=k,m=m,gates=gates,top_raw_address=[-z for z in rank],top_constant=-1)

def cover44():
    k=m=4;N=16;code=[(t,)*4 for t in range(4)]+[tuple((i+t)%4 for i in range(4)) for t in range(4)]
    gates=[]
    for c in range(N):
        for z in code:
            for eta in (-1,1):
                wa=[];const=0
                for i,t in enumerate(z):
                    e=[t&1,t>>1,((c>>i)&1)^(t&1)^(t>>1),0]
                    wa.extend(eta*3**i*(1-2*v) for v in e)
                    const+=eta*3**i*(sum(e)-2)
                gates.append(dict(c=c,table_weight=1,address_weights=wa,threshold=1-const,top_weight=1))
    return dict(META,k=k,m=m,gates=gates,top_raw_address=[0]*16,top_constant=-128)

def verify_all_tables_symbolically(w):
    """All addresses; exact affine dependence on every independent table bit."""
    k=w['k'];m=w['m'];N=1<<k;H=len(w['gates'])
    count=0;minimum=10**30
    for a in product((0,1),repeat=k*m):
        b=sum((sum(a[i*m:(i+1)*m])%2)<<i for i in range(k))
        base=w['top_constant']+sum(v*z for v,z in zip(w['top_raw_address'],a))
        coeff=[0]*N
        for g in w['gates']:
            z=sum(v*t for v,t in zip(g['address_weights'],a))-g['threshold']
            f0=int(z>=0);f1=int(z+g['table_weight']>=0)
            base+=g['top_weight']*f0
            coeff[g['c']]+=g['top_weight']*(f1-f0)
        # The top convention is score>=0; the rank circuit has negative class -1 and positive class 0.
        max0=base+sum(max(0,coeff[c]) for c in range(N) if c!=b)
        min1=base+coeff[b]+sum(min(0,coeff[c]) for c in range(N) if c!=b)
        assert max0<0 and min1>=0,(k,m,a,base,coeff)
        minimum=min(minimum,-max0,min1+1);count+=1
    return dict(k=k,m=m,bottoms=H,total_gates=H+1,raw_addresses=count,independent_tables_per_address=1<<N,all_tables_verified=True,integer_classification_gap=minimum)

def supplied_general_count(k,m):
    # Count copied mathematically from the supplied push_upper/constr3.py count_dpp.
    # This is only a comparison, not an authorship claim for that construction.
    N=1<<k;odd=m if m%2 else m-1;alpha=(odd-1)//2;cp=odd;total=0
    for s in range(1,N):
        size=s.bit_count();T=size*m;kap=-4*cp*(k-2*size)
        total+=sum(-8*t+kap!=0 for t in range(1,N+2*alpha*size+T+1,2))+T//2
    total+=2*(N-1)+2*alpha*k+k*m+3*k*m-(k*m)//2
    return total

if __name__=='__main__':
    results=[]
    for k,m in [(1,2),(2,2),(3,2),(4,2),(2,3),(2,4)]:
        w=paired_rank(k,m);r=verify_all_tables_symbolically(w);results.append(r);print(r,flush=True)
        if (k,m)==(3,2):(OUT/'exact_k3_m2.json').write_text(json.dumps(w,indent=2)+'\n')
    # NumPy accelerates the same exact all-table coefficient proof for the 256-gate circuit.
    import sys
    sys.path.insert(0,'/tmp/pydeps')
    import numpy as np
    w=cover44();A=np.array(list(product((0,1),repeat=16)),dtype=np.int64)
    gs=w['gates'];W=np.array([g['address_weights'] for g in gs],dtype=np.int64)
    th=np.array([g['threshold'] for g in gs],dtype=np.int64)
    B=np.array([sum((sum(a[4*i:4*i+4])%2)<<i for i in range(4)) for a in A])
    base=np.full(len(A),w['top_constant'],dtype=np.int64);coeff=np.zeros((len(A),16),dtype=np.int64)
    for start in range(0,len(gs),32):
        D=A@W[start:start+32].T-th[start:start+32]
        E=(D>=0).astype(np.int64);Z=(D==-1).astype(np.int64)
        base+=E.sum(axis=1)
        for j,g in enumerate(gs[start:start+32]):coeff[:,g['c']]+=Z[:,j]
    truecoef=coeff[np.arange(len(A)),B].copy();coeff[np.arange(len(A)),B]=0
    assert np.all(coeff==0) and np.all(base<0) and np.all(base+truecoef>0)
    assert np.array_equal(2*base,-truecoef)
    r=dict(k=4,m=4,bottoms=256,total_gates=257,raw_addresses=len(A),independent_tables_per_address=65536,all_tables_verified=True,minimum_signed_margin=int(np.min(-base)),supplied_general_count=supplied_general_count(4,4))
    results.append(r);print(r,flush=True)
    w['verification']=r
    (OUT/'exact_k4_m4.json').write_text(json.dumps(w,indent=2)+'\n')
    (OUT/'construction_checks.json').write_text(json.dumps(dict(META,results=results),indent=2)+'\n')
