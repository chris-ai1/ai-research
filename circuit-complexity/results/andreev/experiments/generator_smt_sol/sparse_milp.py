#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Bounded sparse support heuristic; exact top refit and generic symbolic certification."""
import sys, argparse, itertools, time, math
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from scipy.optimize import milp,linprog,Bounds,LinearConstraint
from scipy.sparse import csr_matrix,hstack,vstack,eye
import engine as e
from audit import tables
p=argparse.ArgumentParser();p.add_argument('--k',type=int,default=3);p.add_argument('--m',type=int,default=3);p.add_argument('--r',type=int,default=1);p.add_argument('--seconds',type=int,default=180);p.add_argument('--out',required=True);a=p.parse_args();root=Path(a.out);root.mkdir(exist_ok=True);k,m,r=a.k,a.m,a.r;N=1<<k;lib=e.library(k,m);S=len(lib['bottom']);D=S+N+k+1;ss=np.array(list(itertools.product(range(m+1),repeat=k)),dtype=np.int64);tabs=list(tables(k,r)) if r>=0 else list(range(1<<N));al=np.array([w[:N] for w,t in lib['bottom']]);be=np.array([w[N::m] for w,t in lib['bottom']]);th=np.array([t for w,t in lib['bottom']]);bidx=sum((ss[:,i]%2)<<i for i in range(k));data=[]
for tab in tabs:
 x=np.array([tab>>c&1 for c in range(N)]);g=(ss@be.T+al@x>=th).astype(np.int64);features=np.column_stack([g,np.tile(x,(len(ss),1)),ss,-np.ones(len(ss),dtype=np.int64)]);data.append((2*x[bidx]-1)[:,None]*features)
A=np.vstack(data);M=100.;select=hstack([eye(S),csr_matrix((S,D-S))]);zero=csr_matrix((len(A),S));cons=vstack([hstack([csr_matrix(A),zero]),hstack([select,-M*eye(S)]),hstack([-select,-M*eye(S)])]).tocsc();lower=np.r_[np.ones(len(A)),np.full(2*S,-np.inf)];upper=np.r_[np.full(len(A),np.inf),np.zeros(2*S)];start=time.monotonic()
res=milp(np.r_[np.zeros(D),np.ones(S)],integrality=np.r_[np.zeros(D),np.ones(S)],bounds=Bounds(np.r_[np.full(D,-M),np.zeros(S)],np.r_[np.full(D,M),np.ones(S)]),constraints=LinearConstraint(cons,lower,upper),options={'time_limit':a.seconds,'mip_rel_gap':0,'disp':True})
summary=dict(k=k,m=m,r=r,bottom_library=S,top_and_bottom_output_coefficient_bound=M,status=int(res.status),message=res.message,seconds=time.monotonic()-start,objective=res.fun,dual_bound=getattr(res,'mip_dual_bound',None))
if res.x is not None:
 inds=[j for j in range(S) if res.x[D+j]>.5];cols=inds+list(range(S,D));B=A[:,cols]
 fit=linprog(np.zeros(len(cols)),A_ub=-B,b_ub=-np.ones(len(A)),bounds=[(None,None)]*len(cols),method='highs')
 assert fit.success
 q=[F(float(w)).limit_denominator(100000) for w in fit.x];scale=math.lcm(*(w.denominator for w in q));ints=np.array([int(w*scale) for w in q],dtype=object);minimum=min(B.astype(object)@ints);summary['exact_minimum']=str(minimum);summary['support']=len(inds)
 if minimum>0:
  v=q[:len(inds)];u=q[len(inds):-1];c=dict(bottom=[lib['bottom'][j] for j in inds],v=list(map(str,v)),u=list(map(str,u[:N]))+[str(u[N+i]) for i in range(k) for _ in range(m)],tau=str(q[-1]));family=e.check(c,k,m,r,timeout=30000,batch=1);full=e.independent.check(c,e.independent.andreev_target(k,m),timeout_ms=10000);summary.update(family=family,ordinary=full)
  assert family['status']!='SAT'
  e.save(root/('verified_%d.json'%len(inds)),dict(k=k,m=m,r=r,candidate=c,family=family,ordinary=full,exact_matrix=dict(minimum=str(minimum),rows=len(A))))
e.save(root/'summary.json',summary);print(summary,flush=True)
