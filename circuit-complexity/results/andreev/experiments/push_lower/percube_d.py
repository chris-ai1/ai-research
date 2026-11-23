"""Per-cube splitting statistics of construction (d) (all gates block-symmetric).  For random tables x,
average over unit cubes c of d_c(x) = #gates splitting c, versus the information bound D_0 of Theorem A,
and per-gate split fractions versus the coherent bound (m^k-(m-1)^k)/m^k and the Ball bound."""
import sys, itertools, math
sys.path.insert(0,'/tmp/pydeps'); sys.path.insert(0,'/tmp/andreev_gap/linear_trick')
import numpy as np
from constr_d import build
rng=np.random.default_rng(3)
for k,m in [(4,4),(5,5),(6,6)]:
    gates,K,lin,N,n=build(k,m); S=len(gates)
    W=np.array([g[0] for g in gates]); T=np.array([g[1] for g in gates])
    al=W[:,:N]; be=np.stack([W[:,N+i*m] for i in range(k)],1)
    assert np.allclose(W[:,N:].reshape(S,k,m),be[:,:,None]), 'not block-symmetric'
    cubes=np.array(list(itertools.product(range(m),repeat=k)),dtype=float)
    base=cubes@be.T                                   # (cubes, gates)
    lo=base+np.minimum(be,0).sum(1); hi=base+np.maximum(be,0).sum(1)
    tot=[]; fr=[]
    for _ in range(4):
        x=rng.integers(0,2,N).astype(float); th=T-al@x
        split=(lo<th-1e-9)&(th-1e-9<=hi)              # thresholds integral, values integral: robust
        tot.append(split.sum(1).mean()); fr.append(split.mean(0).max())
    L=math.log2(S+1); D0=(2**k-k-1-L)/(k+L)
    print(f'k={k} m={m} N={N} S={S}: mean #splitting gates per cube = {np.mean(tot):.1f}; information bound D_0={D0:.2f}; '
          f'max per-gate split fraction={max(fr):.3f} (coherent bound {(m**k-(m-1)**k)/m**k:.3f}, Ball {2*math.sqrt(2*k)/m:.3f})',flush=True)
