"""Solve the k=3 (2,2,2,2,2,2,1) arbitrary-amplitude model, then test which amplitude functions are
threshold functions of the 8 table bits (LP)."""
import sys; sys.path.insert(0,'/tmp/pydeps')
import numpy as np, itertools
from ortools.sat.python import cp_model
from scipy.optimize import linprog
k=3; N=8; chars=list(range(1,N)); W=8
cnt={1:2,2:2,4:2,3:2,5:2,6:2,7:1}
gad=[(S,j) for S in chars for j in range(cnt[S])]
md=cp_model.CpModel()
Dl={g:md.NewIntVar(1,W,'') for g in gad}
tau={}
par=lambda v: bin(v).count('1')&1
for t in range(1<<N):
    a={}
    for g in gad:
        tau[g,t]=md.NewBoolVar('')
        a[g]=md.NewIntVar(-W,W,'')
        md.Add(a[g]==Dl[g]).OnlyEnforceIf(tau[g,t]); md.Add(a[g]==-Dl[g]).OnlyEnforceIf(tau[g,t].Not())
    D=md.NewIntVar(-100*W,100*W,'')
    for b in range(N):
        e=sum(a[g] for g in gad if par(g[0]&b))+D
        if (t>>b)&1: md.Add(e>=1)
        else: md.Add(e<=-1)
sol=cp_model.CpSolver(); sol.parameters.max_time_in_seconds=300; sol.parameters.num_workers=3
st=sol.Solve(md); print('status',sol.StatusName(st))
X=np.array([[(t>>c)&1 for c in range(N)] for t in range(1<<N)],float)
def is_thr(f):
    # exists w,theta: (2f-1)(w.x - theta) >= 1
    s=2*np.array(f)-1
    A=-s[:,None]*np.hstack([X,-np.ones((len(X),1))])
    r=linprog(np.zeros(N+1),A_ub=A,b_ub=-np.ones(len(X)),bounds=[(None,None)]*(N+1),method='highs')
    return r.status==0
if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    for g in gad:
        f=[sol.Value(tau[g,t]) for t in range(1<<N)]
        print('gadget',g,'Delta',sol.Value(Dl[g]),'threshold fn:',is_thr(f),'#ones',sum(f))
