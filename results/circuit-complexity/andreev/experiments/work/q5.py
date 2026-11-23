import sys; sys.path.insert(0,"/tmp/andreev_gap/work")
from fam import *
from dich import all_dichotomies
import json
phi=lambda u:(-1)**(u%2)*u
C=int(sys.argv[1]); tl=float(sys.argv[2])
for T in range(1,int(sys.argv[3])+1):
    pts=grid(1,T)
    for name,f in [("x0(-1)^t",lambda x,t:x*(-1)**t),("-2phi(t)-C x0(-1)^t",lambda x,t:-2*phi(t)-C*x*(-1)**t),("-4G(t)-C x0(-1)^t",lambda x,t:-(2*phi(t)-(-1)**t)-C*x*(-1)**t)]:
        fv=[f(*p) for p in pts]
        H=all_dichotomies(pts)
        n,used,st=solve_cands(pts,fv,H,tl=tl,B=20*C+20*T)
        ours={"x0(-1)^t":T+1,"-2phi(t)-C x0(-1)^t":T+(T+1)//2+1,"-4G(t)-C x0(-1)^t":T-1+(T+1)//2+1}[name]
        print(json.dumps(dict(T=T,C=C,func=name,min=n,status=st,construction=ours,old=2*T+2 if name!="x0(-1)^t" else T+2)),flush=True)
