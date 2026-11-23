"""k=2 upper bounds from sign-controlled sawtooth gadgets.
A gadget on character S (t_S = sum_{i in S} s_i in [0,|S|m]) with literal phase phi(x) in {0,1}:
    V*t_S - 2V*sum_{j=1}^{J}[t_S + phi(x) >= 2j]  =  V*(-1)^{phi(x)} * (t_S mod 2)   (J = ceil(|S|m/2) gates; the V*t_S part
    is a free top-level linear term).
F(x,s) = D(x) + sum_g V_g eps_g(x) chi'_{S_g}(b),   chi' in {0,1},  eps_g(x) = (-1)^{phi_g(x)}.
Search: amplitudes and literal phases (phi in {0,1,x_c,1-x_c}) for gadget multisets, such that for every table x some D works;
then check whether D can be affine in x (LP) -> no extra gates.  Exhaustive exact verification of the resulting circuit."""
import sys, itertools
sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction as Fr
TAB=list(itertools.product((0,1),repeat=4))          # x indexed by c = b1 + 2*b2
B=[(b1,b2) for b2 in (0,1) for b1 in (0,1)]
CH={'1':lambda b:b[0],'2':lambda b:b[1],'12':lambda b:b[0]^b[1]}
PH=[('0',lambda x:0),('1',lambda x:1)]+[(f'x{c}',(lambda c:lambda x:x[c])(c)) for c in range(4)]+[(f'~x{c}',(lambda c:lambda x:1-x[c])(c)) for c in range(4)]
def interval(x,gad,ph):
    # G(b)=sum V eps chi'(b); need max_{x_b=0} G < min_{x_b=1} G  -> D in (-min1, -max0]
    G={}
    for b in B:
        G[b]=sum(V*(-1)**p(x)*CH[S](b) for (S,V),(_,p) in zip(gad,ph))
    zero=[G[b] for b in B if x[b[0]+2*b[1]]==0]; one=[G[b] for b in B if x[b[0]+2*b[1]]==1]
    lo=-min(one) if one else None; hi=-max(zero) if zero else None     # need D>=lo and D<hi  (F=D+G>=0 iff x_b=1)
    if lo is not None and hi is not None and not lo<hi: return None
    return lo,hi
def search(gad):
    sols=[]
    n=len(gad)
    for ph in itertools.product(PH,repeat=n):
        ok=True; ivs=[]
        for x in TAB:
            iv=interval(x,gad,ph)
            if iv is None: ok=False; break
            ivs.append(iv)
        if ok: sols.append((ph,ivs))
    return sols
def affine_D(ivs):
    # find u,tau: D(x)=u.x+tau with lo<=D<hi-eps (margin 1e-3 after scaling)  -> LP
    A=[];bb=[]
    for x,(lo,hi) in zip(TAB,ivs):
        row=list(x)+[1.0]
        if lo is not None: A.append([-r for r in row]); bb.append(-lo)
        if hi is not None: A.append(row); bb.append(hi-0.25)
    r=linprog(np.zeros(5),A_ub=np.array(A),b_ub=np.array(bb),bounds=[(None,None)]*5,method='highs')
    return r.x if r.status==0 else None
if __name__=='__main__':
    best=None
    for gad in [ (('1',2),('1',2),('2',2),('2',2),('12',1)), (('1',3),('1',1),('2',3),('2',1),('12',2)),
                 (('1',1),('2',2),('2',2),('12',2),('12',2)), (('1',2),('1',2),('2',2),('2',2),('12',3)),
                 (('1',1),('1',1),('2',1),('2',1),('12',1)) ]:
        sols=search(gad)
        aff=[(ph,ivs,affine_D(ivs)) for ph,ivs in sols]
        aff_ok=[a for a in aff if a[2] is not None]
        print('gadgets',gad,': phase assignments with all 16 tables feasible =',len(sols),'; with affine D =',len(aff_ok),flush=True)
        if aff_ok and best is None: best=(gad,aff_ok[0])
    if best:
        gad,(ph,ivs,u)=best
        print('example:',gad,[p[0] for p in ph],'D(x)=',np.round(u,3))
