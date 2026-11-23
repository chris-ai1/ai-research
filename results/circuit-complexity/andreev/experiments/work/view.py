import sys; sys.path.insert(0,'/tmp/pydeps')
import json, numpy as np
from fractions import Fraction
def exact_weights(pts,keys,fv):
    # solve with fractions: columns keys + const
    import itertools
    A=[[Fraction(k[i]) for k in keys]+[Fraction(1)] for i in range(len(pts))]
    b=[Fraction(v) for v in fv]
    # gaussian elimination least squares not needed: find exact solution of consistent system
    m=len(A); n=len(A[0]); M=[row[:]+[bb] for row,bb in zip(A,b)]
    piv=[];r=0
    for c in range(n):
        p=next((i for i in range(r,m) if M[i][c]!=0),None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]
        inv=1/M[r][c]; M[r]=[x*inv for x in M[r]]
        for i in range(m):
            if i!=r and M[i][c]!=0:
                fct=M[i][c]; M[i]=[x-fct*y for x,y in zip(M[i],M[r])]
        piv.append(c); r+=1
    if any(all(x==0 for x in M[i][:n]) and M[i][n]!=0 for i in range(m)): return None
    sol=[Fraction(0)]*n
    for i,c in enumerate(piv): sol[c]=M[i][n]
    return sol
def show(R,T,keys,fv=None):
    pts=[(y,t) for y in range(R+1) for t in range(T+1)]
    if fv is None: fv=[y*(-1)**t for y,t in pts]
    w=exact_weights(pts,keys,fv)
    print(f"R={R} T={T}: {len(keys)} halfplanes, const={w[-1]}")
    for k,wi in zip(keys,w):
        rows=[''.join('#' if k[pts.index((y,t))] else '.' for t in range(T+1)) for y in range(R,-1,-1)]
        print(f"  w={str(wi):>6}  "+' | '.join(rows)+"   (rows y=R..0, t left->right)")
if __name__=="__main__":
    for fn in sys.argv[1:]:
        d=json.load(open(fn)); show(d['R'],d['T'],[tuple(k) for k in d['keys']])
