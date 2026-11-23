"""k=2: sawtooth gadgets whose phases are arbitrary integer affine functions of x, so the signs eps(x) are
+-characters (-1)^{<u,x>} of the 4 table bits (32 choices).  Configuration: two gadgets on chi_1 (amplitude 1 each),
two on chi_2 (amplitude 1 each), one on chi_12 (amplitude V12).  Find sign functions such that every table x admits a D.
(D(x) may be an arbitrary function of the 4 table bits; it costs O(1) extra x-only gates.)"""
import sys, itertools
sys.path.insert(0,'/tmp/pydeps')
import numpy as np
TAB=np.array(list(itertools.product((0,1),repeat=4)))[:,::-1]   # row r: x_c for c=0..3 (c=b1+2*b2)
TAB=np.array([[ (r>>c)&1 for c in range(4)] for r in range(16)])
Bs=[(b1,b2) for b2 in (0,1) for b1 in (0,1)]
chars=[]
for u in range(16):
    for sg in (1,-1):
        chars.append(sg*(-1)**((TAB@np.array([(u>>c)&1 for c in range(4)]))%2))
chars=np.array(chars)                                        # (32,16)
pairs=np.array([chars[i]+chars[j] for i in range(32) for j in range(i,32)])   # A_1 candidates (528,16) values in {-2,0,2}
def feasible(A1,A2,A12):
    # for each table x: max_{x_b=0} G < min_{x_b=1} G, G(b)=A1 b1 + A2 b2 + A12 (b1^b2)
    ok=np.ones(np.broadcast(A1,A2,A12).shape[:-1],dtype=bool)
    G=[A1*b1+A2*b2+A12*(b1^b2) for (b1,b2) in Bs]
    for r in range(16):
        x=TAB[r]
        one=[G[i][...,r] for i,(b1,b2) in enumerate(Bs) if x[b1+2*b2]==1]
        zero=[G[i][...,r] for i,(b1,b2) in enumerate(Bs) if x[b1+2*b2]==0]
        if one and zero:
            ok&=np.max(np.stack(zero),0)<np.min(np.stack(one),0)
    return ok
for V12 in (0.5,1.0,1.5):
    found=0; ex=None
    for k12 in range(32):
        A12=V12*chars[k12]
        # all A1 (528) x all A2 (528) at once
        ok=feasible(pairs[:,None,:],pairs[None,:,:],A12[None,None,:])
        if ok.any():
            found+=int(ok.sum())
            if ex is None:
                i,j=np.argwhere(ok)[0]; ex=(k12,i,j)
    print(f'V12={V12}: feasible sign configurations = {found}',flush=True)
    if ex:
        k12,i,j=ex
        print('   example A12 sign pattern over tables:',chars[k12].tolist())
        print('   A1 over tables:',pairs[i].tolist()); print('   A2 over tables:',pairs[j].tolist())
