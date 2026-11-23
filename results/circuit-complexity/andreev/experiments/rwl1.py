import sys; sys.path.insert(0,"/tmp/pydeps")
import sys, math, numpy as np
sys.path.insert(0,'/tmp/pydeps')
from scipy.optimize import linprog
def dich(pts,D):
    seen={}
    for a in range(-D,D+1):
        for b in range(0,D+1):
            if (a,b)==(0,0) or math.gcd(abs(a),b)!=1 or (b==0 and a<0): continue
            vals=sorted(set(a*y+b*t for y,t in pts))
            for th in vals[1:]:
                key=tuple(int(a*y+b*t>=th) for y,t in pts)
                comp=tuple(1-v for v in key)
                if key not in seen and comp not in seen: seen[key]=(a,b,th)
    return seen
def sparse(R,T,iters=12,f=lambda y,t:y*(-1)**t):
    pts=[(y,t) for y in range(R+1) for t in range(T+1)]
    H=dich(pts,max(R,T)+2); K=np.array(list(H),float).T  # P x G
    P,G=K.shape; b=np.array([f(*p) for p in pts],float)
    A=np.hstack([K,-K,np.ones((P,1)),-np.ones((P,1))])
    c=np.ones(2*G+2); c[-2:]=0
    best=None
    for it in range(iters):
        r=linprog(c,A_eq=A,b_eq=b,bounds=(0,None),method='highs')
        w=r.x[:G]-r.x[G:2*G]
        sup=np.abs(w)>1e-7
        # verify exact with support only
        Ks=np.hstack([K[:,sup],np.ones((P,1))]); ws=np.linalg.lstsq(Ks,b,rcond=None)[0]
        if np.abs(Ks@ws-b).max()<1e-6:
            cnt=int(sup.sum()); best=cnt if best is None else min(best,cnt)
        cw=1/(np.abs(w)+1e-3); c=np.r_[cw,cw,0,0]
    return best,G
for R,T in [(1,4),(2,2),(2,3),(3,3),(4,4),(5,5),(6,6),(4,8),(8,4),(8,8),(10,5),(10,10)]:
    b,G=sparse(R,T)
    print(f"R={R} T={T}: sparse solution {b} halfplanes (cands {G}); R+T={R+T}; ours 2R+2T={2*R+2*T}",flush=True)
