"""k=2, 'one sawtooth gadget per character' feasibility with monomial amplitudes.
A gadget on character S with table form L(x)=sum_{c in C} x_c costs ceil((T_S+|C|)/2) gates and yields
   Delta * (-1)^{L(x)} * e_S   (+ functions of x alone, + free linear terms).
Functions of x alone cost O(1) at fixed k, so D(x) is free.  Feasible iff for every table x the
scores E_b(x)=sum_{S: S.b odd} A_S(x) (E_0=0) put every 1-address strictly above every 0-address."""
import sys; sys.path.insert(0,'/tmp/pydeps')
import itertools, numpy as np
from scipy.optimize import linprog
k=2; N=4
subsets=[C for r in range(1,N+1) for C in itertools.combinations(range(N),r)]
chars=[1,2,3]          # S as bitmask over blocks; address b as bitmask
tabs=[tuple((t>>c)&1 for c in range(N)) for t in range(1<<N)]
def feas(config):
    # config: list of (S, C) gadgets ; variables Delta_g
    G=len(config); rows=[]
    for x in tabs:
        Xs=[(-1)**sum(x[c] for c in C) for (S,C) in config]
        E={}
        for b in range(N):
            E[b]=[ (Xs[g] if bin(S&b).count('1')%2 else 0) for g,(S,C) in enumerate(config)]
        ones=[b for b in range(N) if x[b]]; zeros=[b for b in range(N) if not x[b]]
        for b1 in ones:
            for b0 in zeros:
                rows.append([-(E[b1][g]-E[b0][g]) for g in range(G)])   # E_b1-E_b0>=1
    A=np.array(rows,float); bb=-np.ones(len(rows))
    r=linprog(np.zeros(G),A_ub=A,b_ub=bb,bounds=[(None,None)]*G,method='highs')
    return r.status==0, (r.x if r.status==0 else None)
found=0
for C1 in subsets:
  for C2 in subsets:
    for C3 in subsets:
        ok,d=feas([(1,C1),(2,C2),(3,C3)])
        if ok: found+=1; print('(1,1,1) feasible',C1,C2,C3,d)
print('(1,1,1) feasible configs:',found)
# (2,1,1): two gadgets on S=1 (cost m), one each on S=2 (m/2) and S=12 (m): total 2.5m ; and symmetric variants
cnt=0
for C1a,C1b in itertools.combinations(subsets,2):
  for C2 in subsets:
    for C3 in subsets:
        ok,d=feas([(1,C1a),(1,C1b),(2,C2),(3,C3)])
        if ok:
            cnt+=1
            if cnt<=5: print('(2,1,1) feasible',C1a,C1b,C2,C3,np.round(d,3))
print('(2,1,1) feasible configs:',cnt)
cnt=0
for C1 in subsets:
  for C2 in subsets:
    for C3a,C3b in itertools.combinations(subsets,2):
        ok,d=feas([(1,C1),(2,C2),(3,C3a),(3,C3b)])
        if ok:
            cnt+=1
            if cnt<=5: print('(1,1,2) feasible',C1,C2,C3a,C3b,np.round(d,3))
print('(1,1,2) feasible configs:',cnt)
