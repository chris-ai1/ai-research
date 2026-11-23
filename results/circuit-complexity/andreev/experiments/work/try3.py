import sys; sys.path.insert(0,"/tmp/andreev_gap/work")
from fam import *
R,T=int(sys.argv[1]),int(sys.argv[2])
pts=grid(R,T); fv=[y*(-1)**t for y,t in pts]
for PL in [(0,-0.5),(0.25,-0.5),(0.5,-0.5),(-0.5,-0.5),(0,-1),(0.5,-1)]:
  for PR in [(0,T+0.5),(0.25,T+0.5),(0.5,T+0.5),(-0.5,T+0.5),(0,T+1),(0.5,T+1)]:
    C={}; C.update(pencil(pts,PL)); C.update(pencil(pts,PR))
    n,used,st=solve_cands(pts,fv,C,tl=120)
    print(R,T,PL,PR,"best",n,"st",st,"target",2*R+T-1,flush=True)
