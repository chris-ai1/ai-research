"""Run the ORIGINAL z3_min.py encoding unchanged (source patched only to return the solver), verify models exactly."""
import sys, time, re
sys.dont_write_bytecode=True
sys.path.insert(0,'/tmp/pydeps'); sys.path.insert(0,'/tmp/andreev_gap/verify')
src=open('/tmp/andreev_gap/z3_min.py').read()
src=src.split("if __name__=='__main__':")[0]
old="r=so.check(); return 'SAT' if r==z3.sat else ('UNSAT' if r==z3.unsat else 'UNKNOWN')"
assert old in src
src=src.replace(old,"r=so.check(); return ('SAT' if r==z3.sat else ('UNSAT' if r==z3.unsat else 'UNKNOWN')),so,(al,th,v,u,tau)")
ns={}; exec(src,ns)
from common import *
def run(k,m,mode,Smax=12,tl=600):
    res=[]
    for S in range(Smax):
        t0=time.time(); r,so,vars_=ns['feasible'](k,m,S,mode,tl); dt=time.time()-t0
        ok=None
        if r=='SAT':
            al,th,v,u,tau=vars_; M=so.model()
            e=lambda x: zq(M.eval(x,model_completion=True))
            g=[([e(a) for a in al[j]],e(th[j])) for j in range(S)]
            ok=verify_circuit(k,m,mode,g,[e(x) for x in v],[e(x) for x in u],e(tau))
        res.append((S,r,round(dt,1),ok))
        if r!='UNSAT': break
    return res
if __name__=='__main__':
    mode=sys.argv[1]; tl=int(sys.argv[2])
    for km in sys.argv[3:]:
        k,m=map(int,km.split(',')); print(mode,k,m,run(k,m,mode,tl=tl),flush=True)
