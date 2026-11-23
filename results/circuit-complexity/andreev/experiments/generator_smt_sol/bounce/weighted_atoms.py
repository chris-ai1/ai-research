#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Sparse sign-coarse Walsh reconstruction, cost weighted by address ladder slope."""
import sys,itertools,json,time,math
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint,linprog
from scipy.sparse import csr_matrix,hstack,vstack,eye
root=Path(__file__).resolve().parent
k=3;N=8;atoms=[(s,r) for s in range(1,8) for r in range(-3,5)];P=len(atoms);D=P+9;rows=[]
for mask in range(256):
 x=np.array([mask>>i&1 for i in range(N)])
 h={s:sum((-1)**((s&c).bit_count()%2)*x[c] for c in range(N)) for s in range(1,8)}
 for b in range(8):
  feat=[(-1)**((s&b).bit_count()%2)*(2*int(h[s]>=r)-1) for s,r in atoms]+list(x)+[-1]
  rows.append((2*x[b]-1)*np.array(feat))
A=np.array(rows);M=100.;select=hstack([eye(P),csr_matrix((P,D-P))]);cons=vstack([hstack([csr_matrix(A),csr_matrix((len(A),P))]),hstack([select,-M*eye(P)]),hstack([-select,-M*eye(P)])]).tocsc();objective=np.r_[np.zeros(D),[s.bit_count() for s,r in atoms]]
start=time.monotonic();res=milp(objective,integrality=np.r_[np.zeros(D),np.ones(P)],bounds=Bounds(np.r_[np.full(D,-M),np.zeros(P)],np.r_[np.full(D,M),np.ones(P)]),constraints=LinearConstraint(cons,np.r_[np.ones(len(A)),np.full(2*P,-np.inf)],np.r_[np.full(len(A),np.inf),np.zeros(2*P)]),options={'time_limit':180,'disp':True})
summary=dict(Authors='Christian Reitwiessner',status=int(res.status),message=res.message,objective=res.fun,dual_bound=getattr(res,'mip_dual_bound',None),seconds=time.monotonic()-start)
if res.x is not None:
 inds=[j for j in range(P) if res.x[D+j]>.5];cols=inds+list(range(P,D));B=A[:,cols];fit=linprog(np.zeros(len(cols)),A_ub=-B,b_ub=-np.ones(len(A)),bounds=[(None,None)]*len(cols),method='highs');assert fit.success
 q=[F(float(w)).limit_denominator(100000) for w in fit.x];scale=math.lcm(*(w.denominator for w in q));minimum=min(B.astype(object)@np.array([int(w*scale) for w in q],dtype=object));summary.update(atoms=[dict(s=atoms[j][0],r=atoms[j][1],weight=str(q[t])) for t,j in enumerate(inds)],table_weights=list(map(str,q[len(inds):-1])),threshold=str(q[-1]),scale=scale,exact_minimum=str(minimum));assert minimum>0
(root/'weighted_atoms.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary,flush=True)
