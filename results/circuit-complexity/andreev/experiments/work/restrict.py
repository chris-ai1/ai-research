import sys; sys.path.insert(0,"/tmp/andreev_gap/work")
from fam import *
from dich import all_dichotomies
import json
mode=sys.argv[1]; tl=float(sys.argv[2])
for a in sys.argv[3:]:
    R,T=map(int,a.split(','))
    pts=grid(R,T); fv=[y*(-1)**t for y,t in pts]
    H=all_dichotomies(pts)
    row0=[i for i,(y,t) in enumerate(pts) if y==0]; rowR=[i for i,(y,t) in enumerate(pts) if y==R]
    def ok(k):
        c0=len(set(k[i] for i in row0))==1
        cR=len(set(k[i] for i in rowR))==1
        return c0 if mode=='row0' else (c0 and cR)
    C={k:v for k,v in H.items() if ok(k)}
    n,used,st=solve_cands(pts,fv,C,tl=tl)
    print(json.dumps(dict(mode=mode,R=R,T=T,best=n,status=st,cands=len(C),target=2*R+T-1)),flush=True)
    if n: json.dump(dict(R=R,T=T,keys=[list(u[0]) for u in used]),open(f'restr_{mode}_{R}_{T}.json','w'))
