# Verify (d'): exhaustive for every (k,m) with n<=20; adversarial+random above.  Also checks that the top sum of (d')
# equals the closed form  P = N - 2N x_b + [b=0](2N|x| - 2N^2 x_0)  exactly (same as (d)).
import sys; sys.path.insert(0,'/tmp/andreev_gap/push_upper'); sys.path.insert(0,'/tmp/pydeps')
import numpy as np, time
from circ import all_inputs, adversarial_inputs, target, check
from constr2 import build_dp, count_dp
def closed(k,m,Z):
    N=1<<k; y,b=target(k,m,Z); X=Z[:,:N].astype(np.int64)
    return N-2*N*y+(b==0)*(2*N*X.sum(1)-2*N*N*X[:,0])
mode=sys.argv[1]
if mode=='exh':
    pairs=[(1,m) for m in range(1,19)]+[(2,m) for m in range(1,9)]+[(3,m) for m in range(1,5)]+[(4,1)]
else:
    pairs=[(4,2),(4,3),(4,4),(4,6),(4,8),(5,3),(5,4),(5,5),(5,6),(6,3),(6,4),(6,5),(6,6),(7,2),(7,3),(8,1)]
for k,m in pairs:
    t0=time.time(); C=build_dp(k,m)
    Z=all_inputs(C.n) if mode=='exh' else adversarial_inputs(k,m,nrand=6000 if k>=7 else 12000)
    ok,marg,bad=check(C,Z); P=C.eval(Z); cf=np.array_equal(P,closed(k,m,Z))
    print(f"(k,m)=({k},{m}) n={C.n} gates={C.size()} formula={count_dp(k,m)} inputs={len(Z)} correct={ok} wrong={bad} min|P|={marg} P==closed_form={cf} maxcoef={max(abs(v) for v in C.V)} t={time.time()-t0:.0f}s",flush=True)
