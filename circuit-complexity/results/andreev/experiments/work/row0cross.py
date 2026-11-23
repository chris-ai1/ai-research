import sys; sys.path.insert(0,"/tmp/andreev_gap/work")
from fam import *
from dich import all_dichotomies
import json
tl=float(sys.argv[1])
for a in sys.argv[2:]:
    R,T=map(int,a.split(','))
    pts=grid(R,T); fv=[y*(-1)**t for y,t in pts]
    H=all_dichotomies(pts)
    r0=[i for i,(y,t) in enumerate(pts) if y==0]
    C={}
    C.update(parallel(pts,2,1)); C.update(parallel(pts,0,1))
    for k,v in H.items():
        if len(set(k[i] for i in r0))>1: C[canon(k)]=v
    n,used,st=solve_cands(pts,fv,C,tl=tl)
    print(json.dumps(dict(R=R,T=T,best=n,status=st,cands=len(C),target=2*R+(3*T)//2-2,par=2*R+2*T-2)),flush=True)
    if n: json.dump(dict(R=R,T=T,keys=[list(u[0]) for u in used]),open(f'r0x_{R}_{T}.json','w'))
