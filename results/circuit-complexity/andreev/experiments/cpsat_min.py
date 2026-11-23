import sys, itertools, time; sys.path.insert(0,'/tmp/pydeps')
from ortools.sat.python import cp_model
def points(k,m):
    N=1<<k
    for x in itertools.product((0,1),repeat=N):
        for s in itertools.product(range(m+1),repeat=k):
            b=sum((s[i]%2)<<i for i in range(k))
            yield x+s, x[b]
def feasible(k,m,S,W=3,V=None,tl=120):
    N=1<<k; P=list(points(k,m)); D=N+k
    V=V or 4*(N+k*m)*N
    md=cp_model.CpModel()
    al=[[md.NewIntVar(-W,W,'') for _ in range(D)] for _ in range(S)]
    TH=W*(N+k*m)+1
    th=[md.NewIntVar(-TH,TH,'') for _ in range(S)]
    v=[md.NewIntVar(-V,V,'') for _ in range(S)]
    u=[md.NewIntVar(-V,V,'') for _ in range(D)]   # top reads inputs directly
    tau=md.NewIntVar(-V*(S+D),V*(S+D),'')
    for j in range(S-1): md.Add(th[j]<=th[j+1])   # weak symmetry breaking
    for p,out in P:
        terms=[]
        for j in range(S):
            g=md.NewBoolVar('')
            lin=sum(al[j][d]*p[d] for d in range(D) if p[d])
            md.Add(lin>=th[j]).OnlyEnforceIf(g); md.Add(lin<=th[j]-1).OnlyEnforceIf(g.Not())
            e=md.NewIntVar(-V,V,''); md.Add(e==v[j]).OnlyEnforceIf(g); md.Add(e==0).OnlyEnforceIf(g.Not())
            terms.append(e)
        top=sum(terms)+sum(u[d]*p[d] for d in range(D) if p[d])
        if out: md.Add(top>=tau)
        else: md.Add(top<=tau-1)
    sol=cp_model.CpSolver(); sol.parameters.max_time_in_seconds=tl; sol.parameters.num_workers=8
    r=sol.Solve(md)
    return {cp_model.OPTIMAL:'SAT',cp_model.FEASIBLE:'SAT',cp_model.INFEASIBLE:'UNSAT'}.get(r,'UNKNOWN')
if __name__=='__main__':
    for k,m in [tuple(map(int,a.split(','))) for a in sys.argv[1:]]:
        N=1<<k; ours=(N-1)*(N+2)+3*k*m*N//2+1; old=2*N*N+k*m*N
        line=[]
        for S in range(0,40):
            t0=time.time(); r=feasible(k,m,S); line.append(f"s={S}:{r}({time.time()-t0:.0f}s)")
            print(f"k={k} m={m}: "+" ".join(line),flush=True) if r!='UNSAT' else None
            if r=='SAT': print(f"==> k={k} m={m}: minimum bottom gates (block-symmetric, |w|<=3) = {S}  [ours 5/8: {ours-1}, 3/4: {old}]",flush=True); break
            if r=='UNKNOWN': print(f"==> k={k} m={m}: undecided at s={S}",flush=True); break
