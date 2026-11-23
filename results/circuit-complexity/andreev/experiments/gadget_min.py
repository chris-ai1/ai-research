import itertools, math, sys, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
def dichotomies(pts, D):
    seen={}
    for a in range(-D,D+1):
        for b in range(-D,D+1):
            if (a,b)==(0,0) or math.gcd(abs(a),abs(b))!=1: continue
            vals=sorted(set(a*y+b*t for y,t in pts))
            for th in vals[1:]:
                key=tuple(int(a*y+b*t>=th) for y,t in pts)
                if key not in seen and any(key) and not all(key): seen[key]=(a,b,th)
    return seen
def solve(R,T,D=6,f=lambda y,t: y*(-1)**t, tl=600):
    pts=[(y,t) for y in range(R+1) for t in range(T+1)]
    H=dichotomies(pts,D); keys=list(H)
    G=len(keys); P=len(pts); B=4*(R+1)*(T+1)+8
    # vars: w(G), z(G), c
    nv=2*G+1
    A=[];lb=[];ub=[]
    for i,p in enumerate(pts):
        row=np.zeros(nv); row[:G]=[k[i] for k in keys]; row[-1]=1
        A.append(row); lb.append(f(*p)); ub.append(f(*p))
    for j in range(G):
        r=np.zeros(nv); r[j]=1; r[G+j]=-B; A.append(r); lb.append(-np.inf); ub.append(0)
        r=np.zeros(nv); r[j]=1; r[G+j]=B; A.append(r); lb.append(0); ub.append(np.inf)
    c=np.zeros(nv); c[G:2*G]=1
    integ=np.zeros(nv); integ[G:2*G]=1
    bl=np.r_[[-B]*G,[0]*G,-1e6]; bu=np.r_[[B]*G,[1]*G,1e6]
    res=milp(c,constraints=LinearConstraint(np.array(A),lb,ub),integrality=integ,bounds=Bounds(bl,bu),options={'time_limit':tl})
    used=[H[keys[j]] for j in range(G) if res.x is not None and res.x[G+j]>0.5]
    return res.status, (round(res.fun) if res.x is not None else None), used, G
if __name__=="__main__":
    for R,T in [(1,1),(1,2),(1,3),(1,4),(2,1),(2,2),(2,3),(2,4),(3,2),(3,3),(4,2),(4,4)]:
        st,opt,used,G=solve(R,T)
        print(f"R={R} T={T}: min halfplanes={opt} (status {st}, candidates {G}); ours 2R+2T={2*R+2*T}; dirs={sorted(set((a,b) for a,b,_ in used))}",flush=True)
