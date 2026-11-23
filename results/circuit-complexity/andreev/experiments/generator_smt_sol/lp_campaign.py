#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Heuristic sparse top fitting over complete finite count grids; exact integer certification.
Floating point is used only in optimization, never in acceptance of a witness.
"""
import sys, time, itertools, json, math, argparse, os, random
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from scipy.optimize import linprog
import engine as e
from audit import tables,exhaustive

def run(k,m,r,rounds,out):
 root=Path(out);root.mkdir(exist_ok=True);log=open(root/'events.jsonl','w');start=time.monotonic()
 def event(**d):
  d['elapsed']=time.monotonic()-start;log.write(json.dumps(d,default=str)+'\n');log.flush();print(json.dumps(d,default=str),flush=True)
 tabs=list(range(1<<(1<<k))) if r<0 else list(tables(k,r))
 lib=e.library(k,m);N=1<<k
 # Symmetric count compression cannot be used after partial address complementation.
 # Instead lift each signed gate's output on all raw address points below.
 if int(os.environ.get('MIXED','0')):
  original=lib['bottom'][:];rng0=random.Random(71)
  for turn in range(int(os.environ['MIXED'])):
   flips=[]
   for i in range(k):
    group=rng0.sample(range(m),min(2,m if m%2==0 else m-1));flips += [N+i*m+j for j in group]
   for w,t in original:
    lib['bottom'].append(([(-a if i in flips else a) for i,a in enumerate(w)],t-sum(w[i] for i in flips)))
 S=len(lib['bottom']);D=S+N+(k*m if int(os.environ.get('MIXED','0')) else k)+1;ss=np.array(list(itertools.product(range(m+1),repeat=k)),dtype=np.int64)
 al=np.array([w[:N] for w,t in lib['bottom']],dtype=np.int64);be=np.array([w[N::m] for w,t in lib['bottom']],dtype=np.int64);th=np.array([t for w,t in lib['bottom']]);data=[]
 if int(os.environ.get('MIXED','0')):
  raw=np.array(list(itertools.product(range(2),repeat=k*m)),dtype=np.int64)
  ss=raw.reshape(-1,k,m).sum(axis=2)
  address=raw@np.array([w[N:] for w,t in lib['bottom']],dtype=np.int64).T
 else:raw=None;address=ss@be.T
 bidx=sum((ss[:,i]%2)<<i for i in range(k))
 for tab in tabs:
  x=np.array([tab>>c&1 for c in range(N)],dtype=np.int64);g=(address+al@x>=th).astype(np.int64)
  features=np.column_stack([g,np.tile(x,(len(ss),1)),raw if raw is not None else ss,-np.ones(len(ss),dtype=np.int64)])
  data.append((2*x[bidx]-1)[:,None]*features)
 A=np.vstack(data);event(phase='matrix',k=k,m=m,r=r,tables=len(tabs),rows=len(A),library=S,columns=D)
 cost=np.ones(S);best=S+1;rng=np.random.default_rng(1)
 for it in range(rounds):
  obj=np.r_[cost,np.zeros(D-S),cost,np.zeros(D-S)]
  t=time.monotonic();res=linprog(obj,A_ub=np.hstack([-A,A]),b_ub=-np.ones(len(A)),bounds=(0,None),method='highs',options={'time_limit':90})
  event(phase='lp',iteration=it,status=int(res.status),message=res.message,seconds=time.monotonic()-t)
  if not res.success:break
  weights=res.x[:D]-res.x[D:];support=np.flatnonzero(abs(weights[:S])>1e-7)
  # Rational recovery followed by arbitrary-precision exact certification on every row.
  rational=[F(float(w)).limit_denominator(100000) for w in weights];scale=math.lcm(*(w.denominator for w in rational));integers=[int(w*scale) for w in rational]
  # Python ints (object dtype), no overflow. >=1 score on both labels is conservative.
  minscore=min(A.astype(object)@np.array(integers,dtype=object));event(phase='exact_matrix',support=len(support),minimum=str(minscore),scale=str(scale))
  if minscore<=0:break
  inds=[j for j in range(S) if rational[j]]
  c=dict(bottom=[lib['bottom'][j] for j in inds],v=[str(rational[j]) for j in inds],u=[str(w) for w in rational[S:S+N]]+([str(w) for w in rational[S+N:-1]] if raw is not None else [str(rational[S+N+i]) for i in range(k) for _ in range(m)]),tau=str(rational[-1]))
  family=e.check(c,k,m,r,timeout=15000,batch=1);full=e.independent.check(c,e.independent.andreev_target(k,m),timeout_ms=10000)
  event(phase='certification',bottoms=len(inds),family=family,ordinary=full)
  assert family['status'] in ('UNSAT','UNKNOWN')
  if family['status'] in ('UNSAT','UNKNOWN'):
   e.save(root/('verified_%d.json'%len(inds)),dict(k=k,m=m,r=r,candidate=c,family=family,ordinary=full,exact_matrix=dict(minimum=str(minscore),scale=str(scale),rows=len(A))))
  if len(inds)<best:best=len(inds)
  cost=1/(abs(weights[:S])+0.1)*(0.95+0.1*rng.random(S))
 event(phase='finished',best=best)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--k',type=int);p.add_argument('--m',type=int);p.add_argument('--r',type=int);p.add_argument('--rounds',type=int,default=5);p.add_argument('--out');a=p.parse_args();run(a.k,a.m,a.r,a.rounds,a.out)
