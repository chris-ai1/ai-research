# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Bounded SAT witness search; exact recheck of every returned witness."""
import sys,itertools,json,time
sys.path[:0]=['/tmp/pydeps','/tmp/andreev_gap/mixed_upper']
from lpcore import Domain,Pool
from ortools.sat.python import cp_model
import numpy as np
m=int(sys.argv[1]); budget=float(sys.argv[2]); target=int(sys.argv[3]); mode=sys.argv[4] if len(sys.argv)>4 else 'unit'
dom=Domain(2,[[m],[m]]); pool=Pool(dom)
A=[tuple(int(i==j) for i in range(4)) for j in range(4)]
if mode=='pair':
 A+= [tuple((int(i==j)-int(i==l)) for i in range(4)) for j in range(4) for l in range(4) if j!=l]
for a in A:
 for b in [(1,0),(0,1),(1,1),(1,-1)]: pool.add_direction(a,b)
G=pool.columns(np.arange(dom.P),range(len(pool))).astype(int)
md=cp_model.CpModel(); M=64
v=[md.NewIntVar(-M,M,'v%d'%j) for j in range(len(pool))]; z=[md.NewBoolVar('z%d'%j) for j in range(len(pool))]
for w,on in zip(v,z): md.Add(w==0).OnlyEnforceIf(on.Not())
md.Add(sum(z)<=target)
mu=[md.NewIntVar(-M,M,'mu%d'%j) for j in range(4)]; nu=[md.NewIntVar(-M,M,'nu%d'%j) for j in range(2)]; c=md.NewIntVar(-4*M,4*M,'c')
for r in range(dom.P):
 t=sum(v[j] for j in np.flatnonzero(G[r]))+sum(mu[j] for j in range(4) if dom.X[r,j])+sum(int(dom.C[r,j])*nu[j] for j in range(2))+c
 md.Add(int(dom.sig[r])*t>=1)
sol=cp_model.CpSolver(); sol.parameters.max_time_in_seconds=budget; sol.parameters.num_workers=4; sol.parameters.random_seed=7
print('START',m,target,mode,'pool',len(pool),'points',dom.P,flush=True)
t0=time.time(); st=sol.Solve(md); print('END',sol.StatusName(st),'seconds',time.time()-t0,flush=True)
if st in (cp_model.FEASIBLE,cp_model.OPTIMAL):
 gates=[dict(alpha=pool.alpha[j].tolist(),beta=pool.beta[j].tolist(),theta=pool.theta[j],weight=sol.Value(v[j])) for j in range(len(pool)) if sol.Value(v[j])]
 out=dict(m=m,gates=gates,mu=[sol.Value(q) for q in mu],nu=[sol.Value(q) for q in nu],constant=sol.Value(c))
 score=G@np.array([sol.Value(q) for q in v])+dom.X@np.array(out['mu'])+dom.C@np.array(out['nu'])+out['constant']
 assert min(score*dom.sig)>=1
 print(json.dumps(out),flush=True)
 with open('/tmp/andreev_gap/mixed_upper_sol/witness_%d_%d.json'%(m,len(gates)),'w') as f: json.dump(dict(Authors='Christian Reitwiessner',**out),f,indent=2)
