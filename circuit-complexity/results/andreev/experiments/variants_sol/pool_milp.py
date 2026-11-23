# Copyright (c) 2026 Christian Reitwiessner. All rights reserved.
# Authors: Christian Reitwiessner
"""Bounded top-weight MILP SAT finder; exact-rational refit and symbolic proof."""
from research import *
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy import sparse
m=int(sys.argv[1]); B=64; c=known(m)
sys.path.insert(0,'/tmp/andreev_gap/push_upper')
from constr3 import build_dpp
pool=list(c.int_bottom())+Circuit.from_push_upper(build_dpp(2,m)).int_bottom()
# All bottom gates are block symmetric; all count vectors suffice for the MILP.
Z=counts(m); y=np.array([target(2,m,p) for p in Z]); sign=2*y-1
G=np.array([[int(sum(w*p for w,p in zip(ws,row))>=t) for ws,t in pool] for row in Z])
H=np.column_stack([G,Z,np.ones(len(Z))]); Q=len(pool); D=H.shape[1]
A=sparse.hstack([sparse.csr_matrix(sign[:,None]*H),sparse.csr_matrix((len(Z),Q))])
link=sparse.lil_matrix((2*Q,D+Q))
for j in range(Q):
    link[2*j,j]=1;link[2*j,D+j]=-B
    link[2*j+1,j]=-1;link[2*j+1,D+j]=-B
card=sparse.csr_matrix(np.r_[np.zeros(D),np.ones(Q)][None,:])
A=sparse.vstack([A,link,card]).tocsr(); lo=np.r_[np.ones(len(Z)),np.full(2*Q,-np.inf),-np.inf];hi=np.r_[np.full(len(Z),np.inf),np.zeros(2*Q),c.S-1]
print('MILP',m,'pool',Q,'baseline',c.S,'bound',B,flush=True)
r=milp(np.r_[np.zeros(D),np.ones(Q)],integrality=np.r_[np.zeros(D),np.ones(Q)],bounds=Bounds(np.r_[np.full(D,-B),np.zeros(Q)],np.r_[np.full(D,B),np.ones(Q)]),constraints=LinearConstraint(A,lo,hi),options={'time_limit':50})
print('RESULT',r.message,'objective',r.fun,'dual',r.mip_dual_bound,flush=True)
if r.x is not None:
    gs=[g for j,g in enumerate(pool) if r.x[D+j]>.5]
    cc=fit(gs,Z,y)
    if cc:
        p=check(cc.to_json(),andreev_target(2,m),10000);print('EXACT',cc.S,p,flush=True)
        if p['status']=='VERIFIED':save(cc,f'milp_2_{m}',dict(k=2,m=m,proof=p));print(cc.format(),flush=True)
