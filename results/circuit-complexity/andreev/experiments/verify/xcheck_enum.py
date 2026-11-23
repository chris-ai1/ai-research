"""Independent encoding #2 (no SMT, no big-M): exhaustive enumeration of all threshold dichotomies of the
input point set (via DFS + LP feasibility, scipy/HiGHS), then for every S-subset of dichotomies (mod complement)
an LP decides whether a top gate over (gate outputs, inputs) separates the target. Exact up to LP tolerance
(margin LPs with unit margin; a positive answer is re-verified in exact arithmetic is not needed for UNSAT claims)."""
import sys, itertools, time
sys.dont_write_bytecode=True
sys.path.insert(0,'/tmp/pydeps'); sys.path.insert(0,'/tmp/andreev_gap/verify')
import numpy as np
from scipy.optimize import linprog
from common import *
def sep(X,y):
    """is there (w,t) with w.X_i >= t (y=1) and w.X_i <= t-1 (y=0)?  X: n x d"""
    n,d=X.shape
    # variables (w,t); constraints  -(w.x - t) <= 0 for y=1 ; (w.x - t) <= -1 for y=0
    sgn=np.where(y==1,-1.0,1.0)
    Aub=np.hstack([X*sgn[:,None], -sgn[:,None]]); bub=np.where(y==1,0.0,-1.0)
    r=linprog(np.zeros(d+1),A_ub=Aub,b_ub=bub,bounds=[(None,None)]*(d+1),method='highs')
    return r.status==0
def dichotomies(X):
    n=len(X); out=[]
    def rec(i,lab):
        if i==n: out.append(tuple(lab)); return
        for b in (0,1):
            lab.append(b)
            if sep(X[:i+1],np.array(lab)): rec(i+1,lab)
            lab.pop()
    # fix first label 0 (mod complement)
    lab=[0]; rec(1,lab)
    return out
def run(k,m,mode,Smax):
    P=list(inputs(k,m,mode)); X=np.array([p for p,_ in P],float); y=np.array([o for _,o in P])
    t0=time.time(); D=dichotomies(X); print(f'  {mode} k={k} m={m}: {len(P)} points, {len(D)} dichotomies mod complement ({time.time()-t0:.1f}s)',flush=True)
    D=np.array(D)
    for S in range(0,Smax+1):
        found=False
        for comb in itertools.combinations(range(len(D)),S):
            F=np.hstack([D[list(comb)].T.astype(float),X]) if S else X
            if sep(F,y): found=True; break
        print(f'  S={S}: {"SAT" if found else "UNSAT"}',flush=True)
        if found: return S
if __name__=='__main__':
    mode=sys.argv[1]
    for km in sys.argv[2:]:
        k,m=map(int,km.split(',')); print('enum',mode,k,m,'min =',run(k,m,mode,3),flush=True)
