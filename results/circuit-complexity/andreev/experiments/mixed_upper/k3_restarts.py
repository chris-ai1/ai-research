"""k=3 pure-parity monomial atoms (p=2, alpha in {0,1}^8): randomized reweighted-L1 + random prune orders,
then MILP (HiGHS, big-M) over the union of all supports found."""
import sys; sys.path.insert(0,'/tmp/andreev_gap/mixed_upper')
from periodic_lp import *
k=3; N=8
dom=PDomain(k,1,2); atoms=Atoms(dom,1.0)
for b in itertools.product((0,1),repeat=3):
    if not any(b): continue
    for a in itertools.product((0,1),repeat=N):
        atoms.add(b,a,2,0)
A=len(atoms.spec); cost=np.array(atoms.cost)
print('atoms',A,flush=True)
rng=np.random.default_rng(int(sys.argv[1]) if len(sys.argv)>1 else 0)
union=set(); best=None
for rs in range(12):
    wts=cost*rng.uniform(0.5,1.5,A)
    for it in range(6):
        r=lp_weighted_l1(dom,atoms,wts)
        w=r[0]; mx=np.abs(w).max()
        supp=[j for j in range(A) if abs(w[j])>1e-7*mx]
        wts=cost*rng.uniform(0.8,1.2,A)/(np.abs(w)+1e-3*mx)
    for t in range(3):
        order=list(rng.permutation(supp))
        sel=order[:]
        i=0
        while i<len(sel):
            tr=sel[:i]+sel[i+1:]
            if feasible(dom,atoms,tr): sel=tr
            else: i+=1
        c=sum(atoms.cost[j] for j in sel); union|=set(sel)
        if best is None or c<best[1]: best=(sel,c)
    print(f' restart {rs}: support {len(supp)} best so far {best[1]} union {len(union)}',flush=True)
print('BEST heuristic slope',best[1])
for j in best[0]: print('   ',atoms.spec[j])
r=min_cost_milp(dom,atoms,sel=sorted(union),time_limit=900)
if r: print('MILP on union: slope',r[1],'dual bound',r[2],'status',r[3]); [print('   ',atoms.spec[j]) for j in r[0]]
