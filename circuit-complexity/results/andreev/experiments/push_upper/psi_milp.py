# Residue test: min #halfspaces so that F = sum v_j H_j + lam.s + mu satisfies
#   |F - Psi| <= 1-eps at b(s)!=0,   F >= -(sigma+2)+eps at b(s)=0 ,  Psi(s)=sum_i s_i [b(s)=e_i]
import sys; sys.path.insert(0,'/tmp/pydeps')
import itertools, math, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

def run2(k,m,D,tl,eps=0.05,M=200.0):
    pts=np.array(list(itertools.product(range(m+1),repeat=k))); par=pts%2; wt=par.sum(1)
    psi=np.where(wt==1,(pts*par).sum(1),0).astype(float); sig=pts.sum(1).astype(float)
    cand=[];seen=set()
    for a in itertools.product(range(-D,D+1),repeat=k):
        if all(x==0 for x in a) or math.gcd(*[abs(x) for x in a])!=1: continue
        if [x for x in a if x!=0][0]<0: continue
        L=pts@np.array(a)
        for th in np.unique(L)[1:]:
            col=(L>=th).astype(np.int8); key=col.tobytes()
            if key in seen: continue
            seen.add(key); cand.append((a,int(th),col))
    J=len(cand); P=len(pts); H=np.array([c[2] for c in cand]).T.astype(float)
    nv=2*J+k+1
    G=np.hstack([H,np.zeros((P,J)),pts.astype(float),np.ones((P,1))])
    lo=np.where(wt>0,psi-1+eps,-(sig+2)+eps); hi=np.where(wt>0,psi+1-eps,np.inf)
    I=np.eye(J); Z=np.zeros((J,k+1))
    A=np.vstack([G,np.hstack([I,-M*I,Z]),np.hstack([I,M*I,Z])])
    LO=np.concatenate([lo,np.full(J,-np.inf),np.zeros(J)]); HI=np.concatenate([hi,np.zeros(J),np.full(J,np.inf)])
    c=np.zeros(nv); c[J:2*J]=1; integ=np.zeros(nv); integ[J:2*J]=1
    lb=np.full(nv,-np.inf); ub=np.full(nv,np.inf); lb[J:2*J]=0; ub[J:2*J]=1
    res=milp(c,constraints=LinearConstraint(A,LO,HI),integrality=integ,bounds=Bounds(lb,ub),options={'time_limit':tl})
    used=[] if res.x is None else [(cand[j][0],cand[j][1],round(res.x[j],3)) for j in range(J) if res.x[J+j]>0.5]
    return res,used,J
if __name__=='__main__':
    k,m,D,tl=map(int,sys.argv[1:5])
    res,used,J=run2(k,m,D,tl)
    cc=sum((bin(S).count('1')*m+1)//2 for S in range(1,1<<k))
    print(f"PSI k={k} m={m} D={D} cands={J} obj={res.fun} dual={getattr(res,'mip_dual_bound',None)} residue-charcount={cc}",flush=True)
    for u in used: print('   ',u)
