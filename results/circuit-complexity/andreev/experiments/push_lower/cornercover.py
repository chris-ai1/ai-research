"""k=2: tau_m = least number of lines such that EVERY unit square of the grid {0..m}^2 has a corner cut
(the line separates exactly one of its 4 vertices from the other three).
In the block-symmetric model with the XOR table x_b=b1^b2, the circuit restricted to a unit square computes
XOR/XNOR of the two live coordinates; that needs a bottom gate whose restriction is AND/OR-like, i.e. a corner cut.
So  min #gates (k=2, blocksym) >= tau_m.
All combinatorial types of lines w.r.t. the vertex set are obtained by perturbing lines through 2 vertices
(4 perturbations each); we use exact integer arithmetic for the perturbed lines."""
import sys, itertools
sys.path.insert(0,'/tmp/pydeps')
import numpy as np

def cut_sets(m):
    V=np.array([(a,b) for a in range(m+1) for b in range(m+1)],dtype=np.int64)
    idx={(a,b):i for i,(a,b) in enumerate(map(tuple,V))}
    sq=[(a,b) for a in range(m) for b in range(m)]
    corners=np.array([[idx[(a,b)],idx[(a+1,b)],idx[(a,b+1)],idx[(a+1,b+1)]] for a,b in sq])
    sets=set()
    P=[tuple(v) for v in V]
    # line through p,q: normal n=(-(q2-p2), q1-p1); value n.(v-p). Perturb: n.(v-p)*E + eps1*rot + eps2 ... use
    # lexicographic perturbation: sign( n.(v-p) , t1*(d.(v-p)) , t2 ) with d=q-p direction, t1,t2 in {+1,-1}:
    # i.e. rotate slightly about p (term d.(v-p)) and translate (constant term) -> all generic neighbours.
    for i in range(len(P)):
        for j in range(i+1,len(P)):
            p=np.array(P[i]); q=np.array(P[j]); d=q-p; n=np.array([-d[1],d[0]])
            f0=(V-p)@n; f1=(V-p)@d
            for t1 in (1,-1):
                for t2 in (1,-1):
                    # sign of f0 + eps*t1*f1 + eps^2*t2 (eps->0+)
                    s=np.where(f0!=0,np.sign(f0),np.where(f1!=0,np.sign(t1*f1),t2))
                    side=(s>0).astype(np.int64)
                    cnt=side[corners].sum(axis=1)
                    cut=frozenset(np.nonzero((cnt==1)|(cnt==3))[0].tolist())
                    if cut: sets.add(cut)
    # keep maximal sets only
    sets=sorted(sets,key=len,reverse=True)
    maximal=[]
    for s in sets:
        if not any(s<=t for t in maximal): maximal.append(s)
    return sq,maximal

def solve(m,tl=600):
    from ortools.sat.python import cp_model
    sq,S=cut_sets(m)
    M=cp_model.CpModel(); y=[M.NewBoolVar(f'y{i}') for i in range(len(S))]
    for e in range(len(sq)):
        M.AddBoolOr([y[i] for i,s in enumerate(S) if e in s])
    M.Minimize(sum(y))
    sol=cp_model.CpSolver(); sol.parameters.max_time_in_seconds=tl; sol.parameters.num_workers=4
    r=sol.Solve(M)
    # LP relaxation
    from scipy.optimize import linprog
    A=np.zeros((len(sq),len(S)))
    for i,s in enumerate(S):
        for e in s: A[e,i]=1
    lp=linprog(np.ones(len(S)),A_ub=-A,b_ub=-np.ones(len(sq)),bounds=[(0,None)]*len(S),method='highs')
    return len(S), max(len(s) for s in S), sol.StatusName(r), sol.ObjectiveValue(), sol.BestObjectiveBound(), lp.fun

if __name__=='__main__':
    for m in map(int,sys.argv[1:]):
        ns,mx,st,ub,lb,lpv=solve(m)
        print(f'm={m}: maximal cut-sets={ns} max|set|={mx} (2m-1={2*m-1})  tau: status={st} best={ub:.0f} bound={lb:.2f}  LP={lpv:.3f}  m^2/(2m-1)={m*m/(2*m-1):.3f}',flush=True)
