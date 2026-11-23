# 2D gadget MILP: min #halfplanes H_j on grid Y in [0,R], t in [0,T] with
#   sum_j v_j H_j  ==  Y*(-1)^t  + q(Y,t) + a*(-1)^t     (q quadratic, a free)   [mode 'q']
# mode 'qa': additionally allow +c*t*(-1)^t (the residue garbage) -> should reproduce ridge-only count
import sys; sys.path.insert(0,'/tmp/pydeps')
import itertools, math, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
def cands(pts,D):
    out=[];seen=set()
    for a in itertools.product(range(-D,D+1),repeat=pts.shape[1]):
        if all(x==0 for x in a) or math.gcd(*[abs(x) for x in a])!=1: continue
        if [x for x in a if x!=0][0]<0: continue
        L=pts@np.array(a)
        for th in np.unique(L)[1:]:
            col=(L>=th).astype(np.int8); key=col.tobytes()
            if key in seen: continue
            seen.add(key); out.append((a,int(th),col))
    return out
def run(R,T,D,tl,mode,M=64.0):
    pts=np.array([(y,t) for y in range(R+1) for t in range(T+1)])
    Y=pts[:,0].astype(float); t=pts[:,1].astype(float); sg=(-1.0)**t
    C=cands(pts,D); J=len(C); P=len(pts)
    H=np.array([c[2] for c in C]).T.astype(float)
    basis=[np.ones(P),Y,t,Y*Y,Y*t,t*t,sg]
    if mode=='qa': basis.append(t*sg)
    B=np.array(basis).T; nb=B.shape[1]
    nv=2*J+nb
    Aeq=np.hstack([H,np.zeros((P,J)),-B]); rhs=Y*sg
    rows=[Aeq]; lo=[rhs]; hi=[rhs]
    I=np.eye(J); Z=np.zeros((J,nb))
    rows.append(np.hstack([I,-M*I,Z])); lo.append(np.full(J,-np.inf)); hi.append(np.zeros(J))
    rows.append(np.hstack([I,M*I,Z])); lo.append(np.zeros(J)); hi.append(np.full(J,np.inf))
    A=np.vstack(rows); lo=np.concatenate(lo); hi=np.concatenate(hi)
    c=np.zeros(nv); c[J:2*J]=1
    integ=np.zeros(nv); integ[J:2*J]=1
    lb=np.full(nv,-np.inf); ub=np.full(nv,np.inf); lb[J:2*J]=0; ub[J:2*J]=1
    res=milp(c,constraints=LinearConstraint(A,lo,hi),integrality=integ,bounds=Bounds(lb,ub),options={'time_limit':tl})
    used=[] if res.x is None else [(C[j][0],C[j][1],round(res.x[j],3)) for j in range(J) if res.x[J+j]>0.5]
    return res,used,J
if __name__=='__main__':
    R,T,D,tl=map(int,sys.argv[1:5]); mode=sys.argv[5]
    res,used,J=run(R,T,D,tl,mode)
    print(f"R={R} T={T} D={D} mode={mode} cands={J} obj={res.fun} dual={getattr(res,'mip_dual_bound',None)} ridge+res={R+T} ridge={R+(T+1)//2}",flush=True)
    for u in used: print('   ',u)
