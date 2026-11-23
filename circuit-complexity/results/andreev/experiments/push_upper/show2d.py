import sys; sys.path.insert(0,'/tmp/pydeps'); import numpy as np
def show(R,T,lines):
    G=np.zeros((R+1,T+1))
    for (a,b),th,w in lines:
        for y in range(R+1):
            for t in range(T+1):
                if a*y+b*t>=th: G[y,t]+=w
    pts=[(y,t) for y in range(R+1) for t in range(T+1)]
    B=np.array([[1,y,t,y*y,y*t,t*t,(-1)**t] for y,t in pts],float)
    tgt=np.array([G[y,t]-y*(-1)**t for y,t in pts])
    c,res,_,_=np.linalg.lstsq(B,tgt,rcond=None)
    print(G); print('fit coeffs [1,Y,t,Y2,Yt,t2,(-1)^t]:',np.round(c,4),' maxres',np.abs(B@c-tgt).max())
show(2,6,[((2,-1),-4,-12),((2,-1),-2,-8),((2,-1),0,-4),((0,1),5,-4),((1,2),2,4)])
show(4,4,[((0,1),4,-4),((1,1),1,12),((2,1),3,8),((2,1),5,4),((2,1),9,-4),((2,1),11,-8)])
