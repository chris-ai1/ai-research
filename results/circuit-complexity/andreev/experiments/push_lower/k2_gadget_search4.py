import sys, itertools
sys.path.insert(0,'/tmp/pydeps'); sys.path.insert(0,'/tmp/andreev_gap/push_lower')
import numpy as np
from k2_gadget_search3 import TAB,Bs,lits,sums
def solutions(cfg,maxsol=5):
    A1,C1=sums(cfg['1']); A2,C2=sums(cfg['2']); A12,C12=sums(cfg['12']); sols=[]
    for k12,a12 in enumerate(A12):
        ok=np.ones((len(A1),len(A2)),dtype=bool)
        for r in range(16):
            x=TAB[r]
            Gb=[A1[:,None,r]*b1+A2[None,:,r]*b2+a12[r]*(b1^b2) for (b1,b2) in Bs]
            one=[g for g,(b1,b2) in zip(Gb,Bs) if x[b1+2*b2]==1]; zero=[g for g,(b1,b2) in zip(Gb,Bs) if x[b1+2*b2]==0]
            if one and zero:
                ok&=np.maximum.reduce([np.broadcast_to(z,ok.shape) for z in zero])<np.minimum.reduce([np.broadcast_to(o,ok.shape) for o in one])
            if not ok.any(): break
        for i,j in np.argwhere(ok):
            sols.append((C1[i],C2[j],C12[k12]))
            if len(sols)>=maxsol: return sols
    return sols
if __name__=='__main__':
    for cfg in [{'1':[2,1],'2':[2,1],'12':[1]},{'1':[2,1],'2':[2,1],'12':[2]},{'1':[2,1],'2':[2,1],'12':[3]},
                {'1':[3,1],'2':[3,1],'12':[2]},{'1':[3,1],'2':[3,1],'12':[1]},{'1':[3,2],'2':[3,2],'12':[1]},
                {'1':[2,1],'2':[1],'12':[2,1]},{'1':[2,1],'2':[2,1],'12':[2,1]}]:
        s=solutions(cfg,3)
        print(cfg,'->',len(s),'solutions (first few):',s[:2],flush=True)
