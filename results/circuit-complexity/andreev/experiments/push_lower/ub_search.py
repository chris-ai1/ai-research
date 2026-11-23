"""Upper-bound search (CP-SAT, bounded integer weights) for block-symmetric depth-2 threshold circuits
computing Andreev's function A(x,s)=x_{s mod 2}, k blocks, s in {0..m}^k.  SAT answers are genuine upper bounds
(every model is re-verified exactly on all inputs); UNSAT/UNKNOWN prove nothing (weights are bounded).
usage: python3 -I ub_search.py k m S [--tl 600] [--workers 6] [--Bb 3] [--Ba 12] [--V 40] [--dirs 'a,b;c,d;...']"""
import sys, itertools, time, argparse, json
sys.path.insert(0,'/tmp/pydeps')
from ortools.sat.python import cp_model

def points(k,m):
    N=1<<k
    for x in itertools.product((0,1),repeat=N):
        for s in itertools.product(range(m+1),repeat=k):
            b=sum((s[i]&1)<<i for i in range(k))
            yield x,s,x[b]

def search(k,m,S,tl,workers,Bb,Ba,V,dirs=None,seed=0):
    N=1<<k; P=list(points(k,m))
    md=cp_model.CpModel()
    if dirs: be=[[md.NewConstant(c) for c in dirs[j]] for j in range(S)]
    else: be=[[md.NewIntVar(-Bb,Bb,f'b{j}_{i}') for i in range(k)] for j in range(S)]
    al=[[md.NewIntVar(-Ba,Ba,f'a{j}_{c}') for c in range(N)] for j in range(S)]
    TH=Ba*N+Bb*k*m+1
    th=[md.NewIntVar(-TH,TH,f't{j}') for j in range(S)]
    v=[md.NewIntVar(0,V,f'v{j}') for j in range(S)]
    for j in range(S-1): md.Add(v[j]<=v[j+1])
    U=V*S
    u=[md.NewIntVar(-U,U,f'u{c}') for c in range(N)]
    w=[md.NewIntVar(-U,U,f'w{i}') for i in range(k)]
    for i in range(k): md.Add(w[i]>=0)          # reflection symmetry s_i -> m-s_i (with table permutation)
    tau=md.NewIntVar(-U*(N+k*m+S),U*(N+k*m+S),'tau')
    for x,s,out in P:
        terms=[]
        for j in range(S):
            g=md.NewBoolVar('')
            lin=sum(al[j][c] for c in range(N) if x[c])+sum(be[j][i]*s[i] for i in range(k) if s[i])
            md.Add(lin>=th[j]).OnlyEnforceIf(g); md.Add(lin<=th[j]-1).OnlyEnforceIf(g.Not())
            e=md.NewIntVar(0,V,''); md.Add(e==v[j]).OnlyEnforceIf(g); md.Add(e==0).OnlyEnforceIf(g.Not())
            terms.append(e)
        top=sum(terms)+sum(u[c] for c in range(N) if x[c])+sum(w[i]*s[i] for i in range(k) if s[i])
        if out: md.Add(top>=tau)
        else: md.Add(top<=tau-1)
    sol=cp_model.CpSolver(); sol.parameters.max_time_in_seconds=tl; sol.parameters.num_workers=workers
    sol.parameters.random_seed=seed
    r=sol.Solve(md)
    if r in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        val=lambda z: sol.Value(z)
        circ=dict(beta=[[val(c) for c in be[j]] for j in range(S)],alpha=[[val(c) for c in al[j]] for j in range(S)],
                  theta=[val(t) for t in th],v=[val(t) for t in v],u=[val(t) for t in u],w=[val(t) for t in w],tau=val(tau))
        return 'SAT',circ
    return {cp_model.INFEASIBLE:'INFEASIBLE(bounded weights)'}.get(r,'UNKNOWN'),None

def verify(k,m,c):
    bad=0
    for x,s,out in points(k,m):
        tot=0
        for j in range(len(c['v'])):
            lin=sum(a*xx for a,xx in zip(c['alpha'][j],x))+sum(b*ss for b,ss in zip(c['beta'][j],s))
            if lin>=c['theta'][j]: tot+=c['v'][j]
        tot+=sum(a*xx for a,xx in zip(c['u'],x))+sum(a*ss for a,ss in zip(c['w'],s))
        if (tot>=c['tau'])!=bool(out): bad+=1
    return bad==0

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('k',type=int); ap.add_argument('m',type=int); ap.add_argument('S',type=int)
    ap.add_argument('--tl',type=float,default=600); ap.add_argument('--workers',type=int,default=6)
    ap.add_argument('--Bb',type=int,default=3); ap.add_argument('--Ba',type=int,default=12); ap.add_argument('--V',type=int,default=40)
    ap.add_argument('--dirs',type=str,default=None); ap.add_argument('--seed',type=int,default=0)
    a=ap.parse_args()
    dirs=[tuple(map(int,d.split(','))) for d in a.dirs.split(';')] if a.dirs else None
    t0=time.time(); r,c=search(a.k,a.m,a.S,a.tl,a.workers,a.Bb,a.Ba,a.V,dirs,a.seed)
    ok=verify(a.k,a.m,c) if c else None
    print(f'UB k={a.k} m={a.m} S={a.S}: {r} time={time.time()-t0:.0f}s verified_exact={ok}',flush=True)
    if c: print('CIRCUIT',json.dumps(c),flush=True)
