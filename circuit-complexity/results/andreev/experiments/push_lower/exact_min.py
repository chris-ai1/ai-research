"""Exact-sum model: the top linear form must equal an affine function of the output EXACTLY,
   sum_j v_j g_j(p) + u.p - tau = A(p)  for all inputs p   (equivalently = c(-1)^{x_b}+d with c!=0).
z3 QF_LRA, block-symmetric inputs (x,s), margin-1 normalisation for bottom gates (WLOG on finite point sets).
Symmetry breaking: gate complementation (v_j>=0, sorted), reflections s_i->m-s_i (w_i>=0), block permutation (w sorted).
Every SAT model is re-verified exactly with Fractions.   usage: exact_min.py k m Smax [tl]"""
import sys, itertools, time
sys.path.insert(0,'/tmp/pydeps')
from fractions import Fraction
import z3
def pts(k,m):
    N=1<<k; P=[]
    for x in itertools.product((0,1),repeat=N):
        for s in itertools.product(range(m+1),repeat=k):
            P.append((x+s, x[sum((s[i]&1)<<i for i in range(k))]))
    return P
def fr(v): return Fraction(v.numerator_as_long(),v.denominator_as_long())
def decide(k,m,S,tl):
    N=1<<k; P=pts(k,m); D=N+k
    so=z3.SolverFor('QF_LRA')
    al=[[z3.Real(f'a{j}_{d}') for d in range(D)] for j in range(S)]; th=[z3.Real(f't{j}') for j in range(S)]
    v=[z3.Real(f'v{j}') for j in range(S)]; u=[z3.Real(f'u{d}') for d in range(D)]; tau=z3.Real('tau')
    for j in range(S):
        so.add(v[j]>=0)
        if j: so.add(v[j-1]<=v[j])
    for i in range(k):
        so.add(u[N+i]>=0)
        if i: so.add(u[N+i-1]<=u[N+i])
    for pi,(p,out) in enumerate(P):
        terms=[]
        for j in range(S):
            g=z3.Bool(f'g{j}_{pi}'); lin=z3.Sum([al[j][d]*p[d] for d in range(D) if p[d]]+[z3.RealVal(0)])
            so.add(z3.Implies(g,lin>=th[j]),z3.Implies(z3.Not(g),lin<=th[j]-1)); terms.append(z3.If(g,v[j],z3.RealVal(0)))
        so.add(z3.Sum(terms+[u[d]*p[d] for d in range(D) if p[d]]+[z3.RealVal(0)])-tau==out)
    so.set('timeout',int(tl*1000)); r=so.check()
    if r!=z3.sat: return ('UNSAT' if r==z3.unsat else 'UNKNOWN'),None
    M=so.model(); e=lambda t: fr(M.eval(t,model_completion=True))
    G=[([e(a) for a in al[j]],e(th[j])) for j in range(S)]; V=[e(t) for t in v]; U=[e(t) for t in u]; T=e(tau)
    ok=all(sum((vj for (a,t),vj in zip(G,V) if sum(aa*c for aa,c in zip(a,p))>=t),Fraction(0))+sum(uu*c for uu,c in zip(U,p))-T==out for p,out in P)
    return 'SAT',ok
if __name__=='__main__':
    k,m,Smax=map(int,sys.argv[1:4]); tl=float(sys.argv[4]) if len(sys.argv)>4 else 600
    for S in range(0,Smax+1):
        t0=time.time(); r,ok=decide(k,m,S,tl)
        print(f'EXACT blocksym k={k} m={m} S={S}: {r} ({time.time()-t0:.1f}s){" verified_exact="+str(ok) if r=="SAT" else ""}',flush=True)
        if r!='UNSAT': break
