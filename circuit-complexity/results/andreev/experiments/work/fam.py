import sys; sys.path.insert(0,'/tmp/pydeps'); sys.path.insert(0,'/tmp/andreev_gap/work')
import numpy as np, math
from scipy.optimize import milp, LinearConstraint, Bounds
def canon(key):
    key=tuple(int(x) for x in key)
    if key[0]==1: key=tuple(1-x for x in key)
    return key
def parallel(pts,a,b):
    v=sorted(set(a*y+b*t for y,t in pts)); out={}
    for th in v[1:]:
        k=canon([a*y+b*t>=th for y,t in pts])
        if any(k): out[k]=('par',a,b,th)
    return out
def pencil(pts,P):
    py,pt=P; out={}
    angs=sorted(set(round(math.atan2(y-py,t-pt)%math.pi,12) for y,t in pts))
    angs=angs+[angs[0]+math.pi]
    for i in range(len(angs)-1):
        th=(angs[i]+angs[i+1])/2
        dy,dt=math.sin(th),math.cos(th)
        k=canon([(dt*(y-py)-dy*(t-pt))>0 for y,t in pts])
        if any(k) and not all(k): out[k]=('pen',P,th)
    return out
def solve_cands(pts,fv,C,tl=300,B=None):
    keys=list(C); G=len(keys); P=len(pts)
    if B is None: B=4*P+8
    K=np.array(keys,float).T
    nv=2*G+1
    A=np.zeros((P+2*G,nv)); A[:P,:G]=K; A[:P,-1]=1
    lb=list(fv); ub=list(fv)
    for j in range(G):
        A[P+2*j,j]=1;A[P+2*j,G+j]=-B; lb.append(-np.inf); ub.append(0)
        A[P+2*j+1,j]=1;A[P+2*j+1,G+j]=B; lb.append(0); ub.append(np.inf)
    c=np.zeros(nv); c[G:2*G]=1
    integ=np.zeros(nv); integ[G:2*G]=1
    res=milp(c,constraints=LinearConstraint(A,lb,ub),integrality=integ,bounds=Bounds(np.r_[[-B]*G,[0]*G,-1e6],np.r_[[B]*G,[1]*G,1e6]),options={'time_limit':tl})
    if res.x is None: return None,None,res.status
    used=[keys[j] for j in range(G) if res.x[G+j]>0.5]
    return round(res.fun),[(k,C[k],res.x[keys.index(k)]) for k in used],res.status
def grid(R,T): return [(y,t) for y in range(R+1) for t in range(T+1)]
