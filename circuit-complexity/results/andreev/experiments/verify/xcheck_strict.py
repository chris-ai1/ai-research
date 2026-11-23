"""Independent encoding #1: z3 QF_LRA WITHOUT margin normalisation (strict inequalities, exact semantics
g <-> alpha.p >= theta ; top: out <-> sum >= tau, strict otherwise), different gate-output encoding
(real variable e_jp in {0,v_j}) and different point enumeration (common.inputs)."""
import sys, time
sys.dont_write_bytecode=True
sys.path.insert(0,'/tmp/pydeps'); sys.path.insert(0,'/tmp/andreev_gap/verify')
import z3
from common import *
def feasible(k,m,S,mode,tl):
    P=list(inputs(k,m,mode)); D=len(P[0][0])
    so=z3.Solver(); so.set('timeout',tl*1000)
    al=[[z3.Real(f'A{j}_{d}') for d in range(D)] for j in range(S)]
    th=[z3.Real(f'T{j}') for j in range(S)]; v=[z3.Real(f'V{j}') for j in range(S)]
    u=[z3.Real(f'U{d}') for d in range(D)]; tau=z3.Real('tau')
    for pi,(p,out) in enumerate(P):
        es=[]
        for j in range(S):
            lin=sum((al[j][d]*int(p[d]) for d in range(D)),z3.RealVal(0))
            g=z3.Bool(f'G{j}_{pi}')
            so.add(g==(lin>=th[j]))                       # exact semantics, no margin
            e=z3.Real(f'E{j}_{pi}')
            so.add(z3.Implies(g,e==v[j]),z3.Implies(z3.Not(g),e==0))
            es.append(e)
        top=sum(es,z3.RealVal(0))+sum((u[d]*int(p[d]) for d in range(D)),z3.RealVal(0))
        so.add((top>=tau) if out else (top<tau))          # strict
    r=so.check()
    if r==z3.sat:
        M=so.model(); e=lambda x: zq(M.eval(x,model_completion=True))
        g=[([e(a) for a in al[j]],e(th[j])) for j in range(S)]
        return 'SAT',verify_circuit(k,m,mode,g,[e(x) for x in v],[e(x) for x in u],e(tau))
    return ('UNSAT' if r==z3.unsat else 'UNKNOWN'),None
if __name__=='__main__':
    mode=sys.argv[1]; tl=int(sys.argv[2])
    for km in sys.argv[3:]:
        k,m=map(int,km.split(',')); res=[]
        for S in range(10):
            t0=time.time(); r,ok=feasible(k,m,S,mode,tl); res.append((S,r,round(time.time()-t0,1),ok))
            if r!='UNSAT': break
        print('strict',mode,k,m,res,flush=True)
