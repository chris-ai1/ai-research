"""Independent encoding #3: MILP with big-M (HiGHS via scipy.optimize.milp), INTEGER weights bounded by B (gates) / C (top).
SAT answers are genuine circuits (re-verified exactly); 'infeasible' only means 'no circuit with those weight bounds'."""
import sys, time, itertools
sys.dont_write_bytecode=True
sys.path.insert(0,'/tmp/pydeps'); sys.path.insert(0,'/tmp/andreev_gap/verify')
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
from fractions import Fraction
from common import *
def solve(k,m,mode,S,B=3,C=40,tl=300):
    P=list(inputs(k,m,mode)); D=len(P[0][0]); n=len(P)
    TH=B*max(sum(p) for p,_ in P)+1
    # variable layout
    idx={}; cnt=0
    def new(name,lo,hi,integer):
        nonlocal cnt; idx[name]=cnt; lb.append(lo); ub.append(hi); it.append(integer); cnt+=1; return cnt-1
    lb=[];ub=[];it=[]
    al=[[new(('a',j,d),-B,B,1) for d in range(D)] for j in range(S)]
    th=[new(('t',j),-TH,TH,1) for j in range(S)]
    v=[new(('v',j),-C,C,1) for j in range(S)]
    u=[new(('u',d),-C,C,1) for d in range(D)]
    tau=new('tau',-10*C*(S+sum(max(p) for p,_ in P)),10*C*(S+sum(max(p) for p,_ in P)),1)
    g=[[new(('g',j,i),0,1,1) for i in range(n)] for j in range(S)]
    e=[[new(('e',j,i),-C,C,0) for i in range(n)] for j in range(S)]
    rows=[];lo=[];hi=[]
    def row(coefs,l,h): rows.append(coefs); lo.append(l); hi.append(h)
    for i,(p,out) in enumerate(P):
        Lp=B*sum(p)+TH
        for j in range(S):
            c={al[j][d]:p[d] for d in range(D) if p[d]}; c[th[j]]=-1
            # g=1 -> lin-th >=0  :  lin-th >= -Lp(1-g)  ->  lin-th - Lp*g >= -Lp
            c1=dict(c); c1[g[j][i]]=-Lp; row(c1,-Lp,np.inf)
            # g=0 -> lin-th <= -1 : lin-th <= -1 + (Lp+1) g
            c2=dict(c); c2[g[j][i]]=-(Lp+1); row(c2,-np.inf,-1)
            # e = v*g
            row({e[j][i]:1,g[j][i]:-C},-np.inf,0); row({e[j][i]:1,g[j][i]:C},0,np.inf)
            row({e[j][i]:1,v[j]:-1,g[j][i]:2*C},-np.inf,2*C); row({e[j][i]:1,v[j]:-1,g[j][i]:-2*C},-2*C,np.inf)
        c={e[j][i]:1 for j in range(S)}
        for d in range(D):
            if p[d]: c[u[d]]=p[d]
        c[tau]=-1
        if out: row(c,0,np.inf)
        else: row(c,-np.inf,-1)
    A=lil_matrix((len(rows),cnt))
    for r,c in enumerate(rows):
        for kk,vv in c.items(): A[r,kk]=vv
    t0=time.time()
    res=milp(np.zeros(cnt),constraints=LinearConstraint(A.tocsr(),lo,hi),integrality=np.array(it),bounds=Bounds(lb,ub),options={'time_limit':tl,'disp':False})
    dt=time.time()-t0
    if res.status==0 or (res.x is not None and res.status==1):
        x=np.round(res.x).astype(int)
        gates=[([Fraction(int(x[al[j][d]])) for d in range(D)],Fraction(int(x[th[j]]))) for j in range(S)]
        ok=verify_circuit(k,m,mode,gates,[Fraction(int(x[a])) for a in v],[Fraction(int(x[a])) for a in u],Fraction(int(x[tau])))
        return 'SAT',dt,ok
    return ('INFEASIBLE(bounded)' if res.status==2 else 'UNKNOWN(status %d)'%res.status),dt,None
if __name__=='__main__':
    mode=sys.argv[1]; B=int(sys.argv[2]); tl=int(sys.argv[3])
    for km in sys.argv[4:]:
        k,m=map(int,km.split(',')); out=[]
        for S in range(0,8):
            r,dt,ok=solve(k,m,mode,S,B=B,C=max(40,10*B),tl=tl); out.append((S,r,round(dt,1),ok))
            if not r.startswith('INFEAS'): break
        print('milp',mode,'B=',B,k,m,out,flush=True)
