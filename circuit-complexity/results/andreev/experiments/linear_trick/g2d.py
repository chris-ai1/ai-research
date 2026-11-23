import sys; sys.path.insert(0,'/tmp/pydeps')
import numpy as np, math, time, json
from scipy.optimize import milp, LinearConstraint, Bounds
def dich(pts,D):
    seen={}
    for a in range(0,D+1):
        for b in range(-D,D+1):
            if (a,b)==(0,0) or math.gcd(a,abs(b))!=1 or (a==0 and b<0): continue
            vals=sorted(set(a*y+b*t for y,t in pts))
            for th in vals[1:]:
                key=tuple(int(a*y+b*t>=th) for y,t in pts)
                if key not in seen: seen[key]=(a,b,th)
    return seen
def solve(R,T,f,D=3,tl=300):
    pts=[(y,t) for y in range(R+1) for t in range(T+1)]
    H=dich(pts,D); keys=list(H); G=len(keys); P=len(pts); B=8*P
    K=np.array(keys,float).T
    nv=2*G+3  # w,z, affine a0,a1,a2
    A=np.zeros((P+2*G,nv)); lb=[];ub=[]
    A[:P,:G]=K; A[:P,-3]=1; A[:P,-2]=[p[0] for p in pts]; A[:P,-1]=[p[1] for p in pts]
    b=[f(*p) for p in pts]; lb+=b; ub+=b
    for j in range(G):
        A[P+2*j,j]=1;A[P+2*j,G+j]=-B; lb.append(-np.inf); ub.append(0)
        A[P+2*j+1,j]=1;A[P+2*j+1,G+j]=B; lb.append(0); ub.append(np.inf)
    c=np.zeros(nv); c[G:2*G]=1; integ=np.zeros(nv); integ[G:2*G]=1
    bl=np.r_[[-B]*G,[0]*G,[-1e5]*3]; bu=np.r_[[B]*G,[1]*G,[1e5]*3]
    res=milp(c,constraints=LinearConstraint(A,lb,ub),integrality=integ,bounds=Bounds(bl,bu),options={'time_limit':tl})
    used=[(H[keys[j]],round(res.x[j],3)) for j in range(G) if res.x is not None and res.x[G+j]>0.5]
    return res.status,(round(res.fun) if res.x is not None else None),used,G
if __name__=="__main__":
    R,T,D,tl=map(int,sys.argv[1:5])
    t0=time.time()
    st,opt,used,G=solve(R,T,lambda y,t:y*(-1)**t,D,tl)
    print(f"R={R} T={T} D={D} st={st} best={opt} G={G} 2R+T={2*R+T} 2R+2T={2*R+2*T} {time.time()-t0:.0f}s")
    for u in sorted(used): print("  ",u)
