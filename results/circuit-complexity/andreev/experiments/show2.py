import sys; sys.path.insert(0,'/tmp/pydeps')
exec(open('gadget_min.py').read().split('if __name__')[0])
import numpy as np
for R,T,D in [(2,3,3),(3,2,3),(1,4,6)]:
    pts=[(y,t) for y in range(R+1) for t in range(T+1)]
    H=dichotomies(pts,D)
    st,opt,used,_=solve(R,T,D,tl=200)
    U=[k for k in H if H[k] in used]
    A=np.array([[k[i] for k in U]+[1] for i in range(len(pts))],float)
    b=np.array([y*(-1)**t for y,t in pts],float)
    w=np.linalg.lstsq(A,b,rcond=None)[0]
    print(f"R={R} T={T}: opt={opt} const={w[-1]:.2f}")
    for k,wi in sorted(zip(U,w[:-1]),key=lambda z:H[z[0]]):
        a,bb,th=H[k]; grid=["".join('#' if k[pts.index((y,t))] else '.' for y in range(R+1)) for t in range(T,-1,-1)]
        print(f"  w={wi:+.2f} [{a}y{bb:+d}t>={th}]  rows(t high->low): {' '.join(grid)}")
