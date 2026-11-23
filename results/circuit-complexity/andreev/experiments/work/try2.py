import sys; sys.path.insert(0,"/tmp/andreev_gap/work")
from fam import *
R,T=int(sys.argv[1]),int(sys.argv[2])
pts=grid(R,T); fv=[y*(-1)**t for y,t in pts]
for P in [(0,-0.5),(-0.5,-1),(-1.5,-2),(-5.5,-6),'par1-1']:
    C={}; C.update(parallel(pts,2,1))
    C.update(parallel(pts,1,-1) if P=='par1-1' else pencil(pts,P))
    n,used,st=solve_cands(pts,fv,C,tl=300)
    print(R,T,P,"best",n,"status",st,"target",2*R+T-1,flush=True)
    if n and P==(0,-0.5):
        for k,info,w in used: print("   ",info[0],info[1:],round(w,3),''.join(map(str,k)))
