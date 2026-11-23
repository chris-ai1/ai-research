# Zero-test MILP: min #halfspaces H_j on grid G=[0,m]^k so that g = sum v_j H_j + lam.s + mu
# has g=0 where b(s)!=0 and g>=1 where b(s)=0  (b(s)=parities of s).  Candidates: all directions
# with integer coords |a_i|<=D (primitive), all distinct thresholds.
import sys; sys.path.insert(0,'/tmp/pydeps')
import itertools, math, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
def run(k,m,D,tl,target='zero'):
    pts=np.array(list(itertools.product(range(m+1),repeat=k)))
    par=pts%2; b0=(par.sum(1)==0)
    cand=[];seen=set()
    for a in itertools.product(range(-D,D+1),repeat=k):
        if all(x==0 for x in a) or math.gcd(*[abs(x) for x in a])!=1: continue
        # canonical sign: first nonzero positive
        fn=[x for x in a if x!=0][0]
        if fn<0: continue
        L=pts@np.array(a); vals=np.unique(L)
        for th in vals[1:]:
            col=(L>=th).astype(np.int8); key=col.tobytes()
            if key in seen: continue
            seen.add(key); cand.append((a,int(th),col))
    J=len(cand); P=len(pts)
    H=np.array([c[2] for c in cand]).T.astype(float)   # P x J
    M=50.0
    # vars: v(J), z(J), lam(k), mu(1)
    nv=2*J+k+1
    A=[];lo=[];hi=[]
    rowsG=np.hstack([H,np.zeros((P,J)),pts.astype(float),np.ones((P,1))])
    for p in range(P):
        A.append(rowsG[p]); 
        if b0[p]: lo.append(1.0); hi.append(np.inf)
        else: lo.append(0.0); hi.append(0.0)
    # |v_j|<=M z_j
    for j in range(J):
        r=np.zeros(nv); r[j]=1; r[J+j]=-M; A.append(r); lo.append(-np.inf); hi.append(0)
        r=np.zeros(nv); r[j]=1; r[J+j]=M; A.append(r); lo.append(0); hi.append(np.inf)
    c=np.zeros(nv); c[J:2*J]=1
    integ=np.zeros(nv); integ[J:2*J]=1
    lb=np.full(nv,-np.inf); ub=np.full(nv,np.inf); lb[J:2*J]=0; ub[J:2*J]=1
    res=milp(c,constraints=LinearConstraint(np.array(A),lo,hi),integrality=integ,bounds=Bounds(lb,ub),options={'time_limit':tl,'disp':False})
    if res.x is None: return None,J,res
    used=[(cand[j][0],cand[j][1],round(res.x[j],4)) for j in range(J) if res.x[J+j]>0.5]
    return used,J,res
if __name__=='__main__':
    k,m,D,tl=map(int,sys.argv[1:5])
    used,J,res=run(k,m,D,tl)
    print(f"k={k} m={m} D={D} cands={J} status={res.status} msg={res.message[:60]} obj={res.fun} bound={getattr(res,'mip_dual_bound',None)} charcount={sum(bin(S).count('1')*m//2 for S in range(1,1<<k))}")
    if used:
        for u in used: print('  ',u)
