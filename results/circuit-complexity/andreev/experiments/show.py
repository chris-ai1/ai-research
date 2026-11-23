import sys; sys.path.insert(0,'/tmp/pydeps')
exec(open('gadget_min.py').read().split('if __name__')[0])
import numpy as np
def show(R,T,D):
    pts=[(y,t) for y in range(R+1) for t in range(T+1)]
    H=dichotomies(pts,D); keys=list(H); G=len(keys)
    from scipy.optimize import milp, LinearConstraint, Bounds
    st,opt,used,_=solve(R,T,D,tl=300)
    print(f"R={R} T={T} D={D}: opt={opt}")
    # re-solve LP for weights on chosen halfplanes
    U=[k for k in keys if H[k] in used]
    A=np.array([[k[i] for k in U]+[1] for i in range(len(pts))],float)
    b=np.array([y*(-1)**t for y,t in pts],float)
    w=np.linalg.lstsq(A,b,rcond=None)[0]
    for k,wi in zip(U,w): 
        a,bb,th=H[k]; print(f"   w={wi:+.3f}  [{a}*y+{bb}*t >= {th}]  set={[p for p,v in zip(pts,k) if v]}")
    print("   const",round(w[-1],3), "resid",np.abs(A@w-b).max())
for R,T,D in [(1,3,5),(2,2,4),(2,3,5)]: show(R,T,D)
