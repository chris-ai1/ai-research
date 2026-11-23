import sys, itertools, time; sys.path.insert(0,'/tmp/pydeps')
import z3
def points(k,m,mode):
    N=1<<k
    for x in itertools.product((0,1),repeat=N):
        if mode=='blocksym':
            for s in itertools.product(range(m+1),repeat=k):
                yield x+s, x[sum((s[i]%2)<<i for i in range(k))]
        else:
            for a in itertools.product((0,1),repeat=k*m):
                s=[sum(a[i*m:(i+1)*m]) for i in range(k)]
                yield x+a, x[sum((s[i]%2)<<i for i in range(k))]
def feasible(k,m,S,mode,tl):
    P=list(points(k,m,mode)); D=len(P[0][0])
    so=z3.SolverFor('QF_LRA'); so.set('timeout',tl*1000)
    al=[[z3.Real(f'a{j}_{d}') for d in range(D)] for j in range(S)]
    th=[z3.Real(f't{j}') for j in range(S)]; v=[z3.Real(f'v{j}') for j in range(S)]
    u=[z3.Real(f'u{d}') for d in range(D)]; tau=z3.Real('tau')
    for pi,(p,out) in enumerate(P):
        terms=[]
        for j in range(S):
            g=z3.Bool(f'g{j}_{pi}'); lin=z3.Sum([al[j][d]*p[d] for d in range(D) if p[d]]+[z3.RealVal(0)])
            so.add(z3.Implies(g,lin>=th[j]), z3.Implies(z3.Not(g),lin<=th[j]-1))
            terms.append(z3.If(g,v[j],z3.RealVal(0)))
        top=z3.Sum(terms+[u[d]*p[d] for d in range(D) if p[d]]+[z3.RealVal(0)])
        so.add(top>=tau if out else top<=tau-1)
    r=so.check(); return 'SAT' if r==z3.sat else ('UNSAT' if r==z3.unsat else 'UNKNOWN')
if __name__=='__main__':
    mode=sys.argv[1]; tl=int(sys.argv[2])
    for km in sys.argv[3:]:
        k,m=map(int,km.split(',')); N=1<<k
        res=[]
        for S in range(0,30):
            t0=time.time(); r=feasible(k,m,S,mode,tl); res.append(f"{S}:{r}[{time.time()-t0:.0f}s]")
            if r!='UNSAT':
                tag='minimum' if r=='SAT' else 'undecided at'
                print(f"==> {mode} k={k} m={m} (n={N+k*m}): {tag} s={S}   trace {' '.join(res)}   [ours 5/8: {(N-1)*(N+2)+3*k*m*N//2+1}, 3/4: {2*N*N+k*m*N}]",flush=True); break
