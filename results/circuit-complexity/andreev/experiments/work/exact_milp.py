import sys; sys.path.insert(0,'/tmp/pydeps'); sys.path.insert(0,'/tmp/andreev_gap/work')
import numpy as np, time, json
from scipy.optimize import milp, LinearConstraint, Bounds
from dich import all_dichotomies
def solve(R,T,f=None,tl=600,B=None,ub=None):
    if f is None: f=lambda y,t: y*(-1)**t
    pts=[(y,t) for y in range(R+1) for t in range(T+1)]
    H=all_dichotomies(pts); keys=list(H); G=len(keys); P=len(pts)
    if B is None: B=4*P+8
    nv=2*G+1
    K=np.array(keys,float).T
    A=np.zeros((P+2*G+(1 if ub else 0),nv)); lb=[];ubv=[]
    A[:P,:G]=K; A[:P,-1]=1
    b=np.array([f(*p) for p in pts],float); lb+=list(b); ubv+=list(b)
    for j in range(G):
        A[P+2*j,j]=1;A[P+2*j,G+j]=-B; lb.append(-np.inf); ubv.append(0)
        A[P+2*j+1,j]=1;A[P+2*j+1,G+j]=B; lb.append(0); ubv.append(np.inf)
    if ub: A[-1,G:2*G]=1; lb.append(0); ubv.append(ub)
    c=np.zeros(nv); c[G:2*G]=1
    integ=np.zeros(nv); integ[G:2*G]=1
    bl=np.r_[[-B]*G,[0]*G,-1e6]; bu=np.r_[[B]*G,[1]*G,1e6]
    t0=time.time()
    res=milp(c,constraints=LinearConstraint(A,lb,ubv),integrality=integ,bounds=Bounds(bl,bu),options={'time_limit':tl,'disp':False})
    used=[keys[j] for j in range(G) if res.x is not None and res.x[G+j]>0.5]
    lbnd=getattr(res,'mip_dual_bound',None)
    return dict(R=R,T=T,status=int(res.status),best=(round(res.fun) if res.x is not None else None),dual=lbnd,G=G,time=time.time()-t0,used=[[H[k][0],H[k][1],H[k][2]] for k in used],keys=[list(k) for k in used])
if __name__=="__main__":
    R,T,tl=int(sys.argv[1]),int(sys.argv[2]),float(sys.argv[3])
    r=solve(R,T,tl=tl)
    print(json.dumps({k:v for k,v in r.items() if k not in('keys','used')}),flush=True)
    json.dump(r,open(f'/tmp/andreev_gap/work/milp_{R}_{T}.json','w'))
