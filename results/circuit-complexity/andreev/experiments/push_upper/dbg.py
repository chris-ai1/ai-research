import sys; sys.path.insert(0,'/tmp/pydeps')
import sys; sys.path.insert(0,'/tmp/andreev_gap/push_upper')
import numpy as np, constr2
from circ import Circuit
import constr
k,m=3,3
orig_fin=Circuit.finalize
def fin_dbg(s):
    d={}; dup=0
    for w,t,v in zip(s.W,s.T,s.V):
        key=(w.tobytes(),t)
        if key in d: dup+=1; d[key][2]+=v
        else: d[key]=[w,t,v]
    zero=sum(1 for x in d.values() if x[2]==0)
    const=0
    for w,t,v in d.values():
        lo=int(np.minimum(w,0).sum()); hi=int(np.maximum(w,0).sum())
        if v!=0 and (t<=lo or t>hi): const+=1
    print('raw',len(s.W),'dups',dup,'zero-coef after merge',zero,'constant',const)
    return orig_fin(s)
Circuit.finalize=fin_dbg
constr2.build_dp(k,m)
