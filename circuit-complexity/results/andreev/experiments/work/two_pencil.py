import sys; sys.path.insert(0,"/tmp/andreev_gap/work")
from fam import *
from multiprocessing import Pool
import itertools, json
R,T=int(sys.argv[1]),int(sys.argv[2]); target=int(sys.argv[3])
pts=grid(R,T); fv=[y*(-1)**t for y,t in pts]
cands=[('P',(py/2,pt/2)) for py in range(-3,2*R+4) for pt in range(-3,2*T+4) if not (py%2==0 and pt%2==0 and 0<=py<=2*R and 0<=pt<=2*T)]
cands+=[('D',(a,b)) for a in range(0,4) for b in range(-3,4) if (a,b)!=(0,0) and math.gcd(a,abs(b))==1 and (a>0 or b>0)]
def fam(c): return pencil(pts,c[1]) if c[0]=='P' else parallel(pts,*c[1])
def run(pair):
    C={}; C.update(fam(pair[0])); C.update(fam(pair[1]))
    C.update(parallel(pts,1,0)); C.update(parallel(pts,0,1))
    n,used,st=solve_cands(pts,fv,C,tl=30)
    return (n,pair,st)
if __name__=="__main__":
    pairs=list(itertools.combinations(cands,2))
    print(len(pairs),flush=True)
    with Pool(8) as p: res=p.map(run,pairs,chunksize=4)
    res=[r for r in res if r[0] is not None]; res.sort(key=lambda r:r[0])
    print("best",res[0][0],"target",target)
    for r in res[:40]: print(r)
    json.dump([(r[0],r[1]) for r in res],open(f'twopen_{R}_{T}.json','w'))
