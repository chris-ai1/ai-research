import sys; sys.path.insert(0,"/tmp/andreev_gap/work")
from fam import *
import json
dirs=eval(sys.argv[1]); tl=float(sys.argv[2])
for a in sys.argv[3:]:
    R,T=map(int,a.split(','))
    pts=grid(R,T); fv=[y*(-1)**t for y,t in pts]
    C={}
    for (p,q) in dirs: C.update(parallel(pts,p,q))
    n,used,st=solve_cands(pts,fv,C,tl=tl)
    print(json.dumps(dict(R=R,T=T,best=n,status=st,cands=len(C),dirs=sorted(set(u[1][1:3] for u in used)) if used else None)),flush=True)
    if used:
        for k,info,w in sorted(used,key=lambda u:u[1][1:]): print("    ",info[1:],round(w,4))
