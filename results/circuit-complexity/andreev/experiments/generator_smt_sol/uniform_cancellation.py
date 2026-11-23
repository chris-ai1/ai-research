#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""All-m coefficient search: ladder weights tied per Walsh amplitude channel."""
import sys,itertools,json,math
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from scipy.optimize import milp,linprog,Bounds,LinearConstraint
from scipy.sparse import csr_matrix,hstack,vstack,eye
import engine as e
from constructions import atoms3
from audit import exhaustive
root=Path(__file__).resolve().parent;atoms=atoms3();J=len(atoms);rows=[]
for mask in range(256):
 x=[mask>>c&1 for c in range(8)];H=[int(sum((-1)**((s&c).bit_count()%2)*x[c] for c in range(8))>=r) for s,r,w in atoms]
 for b in range(8):
  chis=[(-1)**((s&b).bit_count()%2) for s,r,w in atoms]
  rows.append([(2*x[b]-1)*v for v in [chi*(2*h-1)+2*h for chi,h in zip(chis,H)]+H+x+[-1]])
A=np.array(rows,dtype=np.int64);D=A.shape[1];M=100.;sel=hstack([eye(2*J),csr_matrix((2*J,D-2*J))]);C=vstack([hstack([csr_matrix(A),csr_matrix((len(A),2*J))]),hstack([sel,-M*eye(2*J)]),hstack([-sel,-M*eye(2*J)])]).tocsc();cost=np.array([100*s.bit_count() for s,r,w in atoms]+[1]*J)
res=milp(np.r_[np.zeros(D),cost],integrality=np.r_[np.zeros(D),np.ones(2*J)],bounds=Bounds(np.r_[np.full(D,-M),np.zeros(2*J)],np.r_[np.full(D,M),np.ones(2*J)]),constraints=LinearConstraint(C,np.r_[np.ones(len(A)),np.full(4*J,-np.inf)],np.r_[np.full(len(A),np.inf),np.zeros(4*J)]),options={'time_limit':120,'disp':True})
summary=dict(status=int(res.status),message=res.message,objective=res.fun,dual_bound=getattr(res,'mip_dual_bound',None))
if res.x is not None:
 inds=[i for i in range(2*J) if res.x[D+i]>.5]+list(range(2*J,D));fit=linprog(np.zeros(len(inds)),A_ub=-A[:,inds],b_ub=-np.ones(len(A)),bounds=[(None,None)]*len(inds),method='highs');assert fit.success
 q=[F(0)]*D
 for j,v in zip(inds,fit.x):q[j]=F(float(v)).limit_denominator(100000)
 scale=math.lcm(*(v.denominator for v in q));minimum=min(A.astype(object)@np.array([int(v*scale) for v in q],dtype=object));assert minimum>0
 summary.update(A=list(map(str,q[:J])),C=list(map(str,q[J:2*J])),raw_table=list(map(str,q[2*J:-1])),tau=str(q[-1]),exact_minimum=str(minimum),exact_cases=len(A),weighted_channel_cost=sum(s.bit_count() for (s,r,w),v in zip(atoms,q[:J]) if v),standalone_gates=sum(bool(v) for v in q[J:2*J]))
 records=[]
 for m in [3,4,6]:
  bottom=[];v=[];u=list(q[2*J:-1])+[F(0)]*(3*m);tau=q[-1]
  for j,(s,r,w) in enumerate(atoms):
   al=[(-1)**((s&c).bit_count()%2) for c in range(8)];addr=[6*int(bool(s>>i&1)) for i in range(3) for z in range(m)]
   if q[j]:
    for ell in range(s.bit_count()*m//2+1):bottom.append((al+addr,12*ell+r));v.append(4*q[j])
   if q[J+j]:bottom.append((al+[0]*(3*m),r));v.append(q[J+j])
   tau+=q[j]
   for i in range(3):
    for z in range(m):u[8+i*m+z]-=2*q[j]*int(bool(s>>i&1))
  c=dict(bottom=bottom,v=list(map(str,v)),u=list(map(str,u)),tau=str(tau));exact=exhaustive(c,3,m,range(256));assert exact['status']=='VERIFIED';symbolic=e.independent.check(c,e.independent.andreev_target(3,m),timeout_ms=5000)
  e.save(root/('uniform_cancellation_m%d.json'%m),dict(k=3,m=m,r=-1,candidate=c,ordinary_exact=exact,ordinary_symbolic=symbolic));records.append(dict(m=m,bottoms=len(bottom),exact=exact,symbolic=symbolic))
 summary['instances']=records
e.save(root/'uniform_cancellation_results.json',summary);print(summary,flush=True)
