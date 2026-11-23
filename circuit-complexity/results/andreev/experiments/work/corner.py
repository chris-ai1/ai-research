import sys; sys.path.insert(0,"/tmp/andreev_gap/work")
from fam import *
from dich import all_dichotomies
import json
tl=float(sys.argv[1])
for a in sys.argv[2:]:
    R,T=map(int,a.split(','))
    pts=grid(R,T); fv=[y*(-1)**t for y,t in pts]
    H=all_dichotomies(pts)
    idx={p:i for i,p in enumerate(pts)}
    def crosses(k,seg):  # seg list of points along a boundary line; dichotomy non-constant on it
        return len(set(k[idx[p]] for p in seg))>1
    row0=[(0,t) for t in range(T+1)]; rowR=[(R,t) for t in range(T+1)]
    col0=[(y,0) for y in range(R+1)]; colT=[(y,T) for y in range(R+1)]
    C={}
    C.update(parallel(pts,2,1)); C.update(parallel(pts,0,1)); C.update(parallel(pts,1,0))
    for k,v in H.items():
        if (crosses(k,row0) and crosses(k,col0) and not crosses(k,rowR) and not crosses(k,colT)) or \
           (crosses(k,rowR) and crosses(k,colT) and not crosses(k,row0) and not crosses(k,col0)): C[canon(k)]=v
    n,used,st=solve_cands(pts,fv,C,tl=tl)
    print(json.dumps(dict(R=R,T=T,best=n,status=st,cands=len(C),target=2*R+(3*T)//2-2,par=2*R+2*T-2)),flush=True)
    if n: json.dump(dict(R=R,T=T,keys=[list(u[0]) for u in used]),open(f'corner_{R}_{T}.json','w'))
