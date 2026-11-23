"""Explicit block-symmetric k=2 circuit with 4*ceil(m/2) + m + E gates (E = x-only gates for D, here computed),
from the sawtooth-gadget solution  F = D(x) + [2X0 + X2] b1 + [2X0 + X1] b2 + 2X0 (b1 xor b2),  X_c=(-1)^{x_c},
table index c = b1 + 2*b2.  Gadget  V*(-1)^{x_c}*(t mod 2) = V*t - 2V*sum_{j=1}^{J} [t + x_c >= 2j],  J=ceil(T/2).
Verified exhaustively over all (x,s) with exact integer arithmetic."""
import sys, itertools, math
sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from scipy.optimize import linprog
TAB=[tuple((r>>c)&1 for c in range(4)) for r in range(16)]
GAD=[('1',2,0),('1',1,2),('2',2,0),('2',1,1),('12',2,0)]     # (character, amplitude, table bit controlling the sign)
def Gval(x,b1,b2):
    tot=0
    for S,V,c in GAD:
        chi={'1':b1,'2':b2,'12':b1^b2}[S]; tot+=V*(-1)**x[c]*chi
    return tot
def D_intervals():
    iv=[]
    for x in TAB:
        G={(b1,b2):Gval(x,b1,b2) for b1 in (0,1) for b2 in (0,1)}
        one=[G[b] for b in G if x[b[0]+2*b[1]]]; zero=[G[b] for b in G if not x[b[0]+2*b[1]]]
        lo=-min(one) if one else None; hi=-max(zero) if zero else None   # need lo <= D < hi
        iv.append((lo,hi))
    return iv
def fit_D(iv):
    """D(x) = u.x + t0 + sum_e w_e [x == point_e] for the fewest x-only point gates; brute force over E."""
    for E in range(0,17):
        for pts in itertools.combinations(range(16),E):
            A=[];bb=[]
            for r,(x,(lo,hi)) in enumerate(zip(TAB,iv)):
                row=list(x)+[1.0]+[1.0 if r==p else 0.0 for p in pts]
                if lo is not None: A.append([-v for v in row]); bb.append(-lo)
                if hi is not None: A.append(row); bb.append(hi-0.5)
            res=linprog(np.zeros(5+E),A_ub=np.array(A),b_ub=np.array(bb),bounds=[(None,None)]*(5+E),method='highs')
            if res.status==0: return E,pts,res.x
    return None
def build(m,Dfit):
    E,pts,coef=Dfit
    gates=[]   # (alpha[4], beta[2], theta, v)
    lin_s=np.zeros(2); 
    for S,V,c in GAD:
        beta={'1':(1,0),'2':(0,1),'12':(1,1)}[S]; T=m*sum(beta); J=(T+1)//2
        lin_s+=V*np.array(beta)
        a=[0,0,0,0]; a[c]=1
        for j in range(1,J+1): gates.append((tuple(a),beta,2*j,-2*V))
    for p in pts:   # point indicator [x == TAB[p]]  as threshold gate
        y=TAB[p]; a=tuple(1 if y[c] else -1 for c in range(4)); gates.append((a,(0,0),sum(y),coef[5+pts.index(p)]))
    u=coef[:4]; t0=coef[4]
    return gates,u,t0,lin_s
def verify(m,gates,u,t0,lin_s):
    bad=0; minmarg=1e9
    for x in TAB:
        for s1 in range(m+1):
            for s2 in range(m+1):
                F=t0+sum(uu*xx for uu,xx in zip(u,x))+lin_s[0]*s1+lin_s[1]*s2
                for a,be,th,v in gates:
                    if sum(aa*xx for aa,xx in zip(a,x))+be[0]*s1+be[1]*s2>=th: F+=v
                out=x[(s1&1)+2*(s2&1)]
                if (F>=0)!=bool(out): bad+=1
                minmarg=min(minmarg,F if out else -F)
    return bad,minmarg
if __name__=='__main__':
    iv=D_intervals(); Dfit=fit_D(iv)
    print('D(x) needs',Dfit[0],'extra x-only gates; affine part u =',np.round(Dfit[2][:5],3))
    for m in range(1,13):
        gates,u,t0,lin_s=build(m,Dfit); bad,mg=verify(m,gates,u,t0,lin_s)
        print(f'k=2 m={m}: gates={len(gates)} (formula 4*ceil(m/2)+m+{Dfit[0]} = {4*((m+1)//2)+m+Dfit[0]})  errors={bad}  min margin={mg:.3f}',flush=True)
