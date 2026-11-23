import sys; sys.path.insert(0,"/tmp/andreev_gap/work")
from fam import *
import itertools,sys
R,T=int(sys.argv[1]),int(sys.argv[2])
pts=grid(R,T); fv=[y*(-1)**t for y,t in pts]
base={}
base.update(parallel(pts,2,1))
res=[]
cands=[(py/2,pt/2) for py in range(-4,2*R+5) for pt in range(-4,2*T+5) if not (py%2==0 and pt%2==0 and 0<=py<=2*R and 0<=pt<=2*T)]
for P in cands:
    C=dict(base); C.update(pencil(pts,P))
    n,used,st=solve_cands(pts,fv,C,tl=60)
    res.append((n,P,st))
res=[r for r in res if r[0] is not None]; res.sort(key=lambda r:(r[0],r[1]))
print(R,T,"target",2*R+T-1, res[:15],flush=True)
