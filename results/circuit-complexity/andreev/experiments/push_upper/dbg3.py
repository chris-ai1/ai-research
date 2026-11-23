import sys; sys.path.insert(0,'/tmp/andreev_gap/push_upper'); sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from constr3 import build_dpp, closed
from circ import all_inputs, target
for k,m in [(2,1),(3,3)]:
    C=build_dpp(k,m); Z=all_inputs(C.n); P=C.eval(Z); Q=closed(k,m,Z); y,b=target(k,m,Z)
    D=P-Q; N=1<<k
    s=np.stack([Z[:,N+i*m:N+(i+1)*m].sum(1) for i in range(k)],1); sig=s.sum(1)
    for bb in range(N):
        sel=b==bb
        d=D[sel]
        # regress d on [1, sigma, s_i..., x_c...]
        X=np.hstack([np.ones((sel.sum(),1)),s[sel],Z[sel][:, :N]]).astype(float)
        c,res,_,_=np.linalg.lstsq(X,d.astype(float),rcond=None)
        print(k,m,'b=',bb,'diff range',d.min(),d.max(),'fit',np.round(c,3),'resid',np.abs(X@c-d).max())
