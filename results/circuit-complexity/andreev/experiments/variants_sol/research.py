# Copyright (c) 2026 Christian Reitwiessner. All rights reserved.
# Authors: Christian Reitwiessner
"""Warm-start pool synthesis and exact symbolic CEGIS for ordinary Andreev."""
import sys, os, json, time, random, itertools
sys.path[:0]=['/tmp/pydeps','/tmp/andreev_gap/variants','/tmp/andreev_gap/mixed_upper','/tmp/andreev_gap/mixed_sign','/home/user/.t3/scratch/2026-11-02-improve-upper-bound-of-andreevs-93c6aee6']
from math import lcm
import numpy as np
import z3
from fractions import Fraction as F
from scipy.optimize import linprog
from sc_circuit import Circuit
from smt_symbolic_check import check, andreev_target
from mscore import Enc
ROOT=os.path.dirname(__file__)
def target(k,m,p):
    N=1<<k
    b=sum((sum(p[N+i*m:N+(i+1)*m])%2)<<i for i in range(k))
    return p[b]
def known(m):
    """The existing Theorem G family, written directly with exact integers.
    Five staircases yield 4 floor((m+1)/2)+m bottom gates.
    """
    n=4+2*m; gs=[];v=[]
    for blocks,x,coef in [((0,),1,4),((0,),3,6),((1,),2,4),((1,),3,6),((0,1),3,-6)]:
        w=[0]*n;w[x]=1
        for block in blocks:
            for h in range(m):w[4+block*m+h]=1
        for cutoff in range(2,len(blocks)*m+2,2):
            gs.append((w[:],cutoff));v.append(coef)
    return Circuit(gs,v,[2,0,0,0]+[-2]*(2*m),1)
def save(c,name,meta):
    obj=c.to_json(); obj.update(Authors='Christian Reitwiessner',copyright='2026 Christian Reitwiessner',metadata=meta)
    with open(ROOT+'/'+name+'.json','w') as f: json.dump(obj,f,indent=2)
def counts(m):
    return np.array([list(x)+[1]*a+[0]*(m-a)+[1]*b+[0]*(m-b) for x in itertools.product((0,1),repeat=4) for a in range(m+1) for b in range(m+1)],dtype=int)
def fit(gs,Z,y,rng=None):
    from sc_circuit import int_form
    forms=[int_form(w,t) for w,t in gs]
    maxsum=max((sum(abs(a) for a in w)+abs(t) for w,t in forms),default=0)
    dt=np.int64 if maxsum<2**62 else object
    G=(Z.astype(dt)@np.array([w for w,t in forms],dtype=dt).T>=np.array([t for w,t in forms],dtype=dt)).astype(int)
    H=np.column_stack([G,Z,np.ones(len(Z),dtype=int)])
    sign=2*y-1
    # random weighted l1 encourages different sparse supports
    cost=np.ones(2*len(gs)+2*Z.shape[1]+2)
    if rng is not None: cost[:2*len(gs)]=np.tile(rng.uniform(.2,2,len(gs)),2)
    D=H.shape[1]
    # split variable layout [all positive, all negative]
    cost=np.concatenate([np.r_[rng.uniform(.2,2,len(gs)) if rng is not None else np.ones(len(gs)),np.zeros(Z.shape[1]+1)]]*2)
    r=linprog(cost,A_ub=np.hstack([-sign[:,None]*H,sign[:,None]*H]),b_ub=-np.ones(len(Z)),bounds=(0,None),method='highs')
    if not r.success:return None
    v=r.x[:D]-r.x[D:]
    # Exact rational conversion followed by exact matrix multiplication; rejects unsafe rounding.
    q=[F(float(a)).limit_denominator(100000) for a in v]
    den=lcm(*(a.denominator for a in q)); nums=[int(a*den) for a in q]
    dtype=np.int64 if sum(abs(a) for a in nums)<2**62 else object
    if np.any(sign*(H.astype(dtype)@np.array(nums,dtype=dtype))*2<den):return None
    keep=[i for i in range(len(gs)) if q[i]]
    return Circuit([gs[i] for i in keep],[q[i] for i in keep],q[len(gs):-1],-q[-1])
def sympool(c,m):
    pool={}
    def add(ws,t):
        from sc_circuit import int_form
        ws,t=int_form(ws,t); lo=sum(min(0,a) for a in ws); hi=sum(max(0,a) for a in ws)
        if t<=lo or t>hi:return
        # normalize gate complement: equivalent up to free constant at top
        comp=(tuple(-a for a in ws),1-t)
        key=min((tuple(ws),t),comp);pool[key]=key
    # input automorphisms: table complementation, address flips, block swap.
    for flip in range(4):
      for swap in (False,True):
       for outflip in (False,True):
        # z_old = transformed z_new, preserving target up to output flip
        perm=[((i>>1)|((i&1)<<1)) if swap else i for i in range(4)]
        for ws,t in c.int_bottom():
          nw=[0]*c.n; nt=t
          for i in range(4):
            j=perm[i^flip]
            nw[j]= -ws[i] if outflip else ws[i]
            if outflip:nt-=ws[i]
          for i in range(2):
            for h in range(m):
              j=4+(1-i if swap else i)*m+h; a=ws[4+i*m+h]
              if h==0 and (flip>>i)&1: nw[j]=-a;nt-=a
              else:nw[j]=a
          add(nw,nt)
    return list(pool.values())
def prune(m,restarts,full=False):
    rng=np.random.default_rng(917+m); c=known(m); Z=counts(m); y=np.array([target(2,m,p) for p in Z])
    if full:
        Z=((np.arange(1<<(4+2*m))[:,None]>>np.arange(4+2*m))&1).astype(int)
        y=np.array([target(2,m,p) for p in Z])
    assert np.array_equal(c.eval_batch(Z),y)
    pool=sympool(c,m)
    # Add all d'' gates, which remain block symmetric.
    sys.path.insert(0,'/tmp/andreev_gap/push_upper')
    from constr3 import build_dpp
    pool+=Circuit.from_push_upper(build_dpp(2,m)).int_bottom()
    print('POOL',m,'initial',c.S,'pool',len(pool),flush=True)
    best=c; besterr=float("inf")
    for r in range(restarts):
        cc=fit(pool,Z,y,rng)
        if cc is None:continue
        gs=list(cc.bottom); order=list(range(len(gs)));rng.shuffle(order)
        for j in order:
            if gs[j] is None: continue
            trial=[g for i,g in enumerate(gs) if g is not None and i!=j]
            found=fit(trial,Z,y)
            if found is not None:gs[j]=None
        cc=fit([g for g in gs if g is not None],Z,y)
        if cc and cc.S<best.S:
            # Exact full-domain symbolic proof, no count-domain assumption needed.
            proof=check(cc.to_json(),andreev_target(2,m),10000)
            print('IMPROVED',m,cc.S,proof,flush=True)
            if proof['status']=='COUNTEREXAMPLE':
                p=proof['point']; assert cc.eval(p)!=target(2,m,p)
                if m<=4:
                    zz=((np.arange(1<<(4+2*m))[:,None]>>np.arange(4+2*m))&1).astype(int)
                    yy=np.array([target(2,m,row) for row in zz])
                    errors=int(np.sum(cc.eval_batch(zz)!=yy))
                    print('REJECTED_EXACT_ERRORS',cc.S,errors,'of',len(zz),flush=True)
                    if errors<besterr:
                        besterr=errors;save(cc,f'near_2_{m}',dict(status='REFUTED_NOT_A_CONSTRUCTION',k=2,m=m,full_domain_errors=errors,points=len(zz),counterexample=p))
                Z=np.vstack([Z,p]); y=np.r_[y,target(2,m,p)]
            if proof['status']=='VERIFIED':
                best=cc;save(best,f'best_2_{m}',dict(k=2,m=m,proof=proof))
        print('RESTART',m,r,'support',cc.S if cc else None,'best',best.S,flush=True)
    save(best,f'best_2_{m}',dict(k=2,m=m,baseline=c.S,proof=check(best.to_json(),andreev_target(2,m),10000)))
    return best

def cegis(k,m,S,seconds,seed=1,base=None,free=(),bs=False,init_counts=False,initial_points=None):
    """No target enumeration. Arbitrary real learner; fixed gates use exact >=/<.
    Free real gates use normalized unit separation, valid with unrestricted scaling.
    No input or gate symmetries are imposed; free may be any chosen gate indices.
    """
    rng=random.Random(seed); n=(1<<k)+k*m
    pts=[]; seen=set()
    for _ in range(24):
        p=tuple(rng.randrange(2) for _ in range(n))
        if p not in seen:seen.add(p);pts.append((p,target(k,m,p)))
    if init_counts:
        pts=[(tuple(map(int,p)),target(k,m,p)) for p in counts(m)]; seen={p for p,y in pts}
    if initial_points is not None:
        pts=[(tuple(map(int,p)),target(k,m,p)) for p in initial_points]; seen={p for p,y in pts}
    opts=dict(vsym=False,seed=seed)
    if bs:opts.update(cls='blocksym',blocks=[list(range((1<<k)+i*m,(1<<k)+(i+1)*m)) for i in range(k)])
    enc=Enc(pts,S,opts)
    # Freeze bottom weights. Enc's negative margin may fail for fractional frozen
    # gates, so first integerize them (integer cutoff guarantees unit separation).
    if base:
        for j,(ws,t) in enumerate(base.int_bottom()):
            if j not in free:
                enc.so.add(enc.th[j]==t,*[a==w for a,w in zip(enc.al[j],ws)])
    for i in range(len(pts)):enc.add_point(i)
    start=time.monotonic(); it=0
    while time.monotonic()-start<seconds:
        enc.so.set(timeout=max(1,int(1000*(seconds-(time.monotonic()-start)))))
        r=enc.so.check(); it+=1
        if r!=z3.sat:
            print('CEGIS',k,m,S,'learner',str(r),'round',it,'points',len(pts),flush=True);return None
        c=Circuit.from_mscore(enc.circuit(enc.so.model()))
        proof=check(c.to_json(),andreev_target(k,m),min(10000,max(1,int(1000*(seconds-(time.monotonic()-start))))))
        print('CEGIS',k,m,S,'round',it,'points',len(pts),proof['status'],flush=True)
        if proof['status']=='VERIFIED':
            save(c,f'cegis_{k}_{m}_{S}_{seed}',dict(k=k,m=m,proof=proof,rounds=it,points=len(pts)));return c
        if proof['status']=='UNKNOWN':return None
        p=proof['point'];assert p not in seen
        assert c.eval(p)!=target(k,m,p)
        seen.add(p);pts.append((p,target(k,m,p)));enc.add_point(len(pts)-1)
    return None
if __name__=='__main__':
    if sys.argv[1] in ('prune','prunefull'):prune(int(sys.argv[2]),int(sys.argv[3]),sys.argv[1]=='prunefull')
    elif sys.argv[1]=='cegis':cegis(*map(int,sys.argv[2:6]))
