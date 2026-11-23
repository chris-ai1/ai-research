"""k=2 sawtooth-gadget configurations with LITERAL phases (signs in {+-1, +-(-1)^{x_c}}: no floor corrections).
For a multiset of gadgets per character (with amplitudes), decide whether sign functions exist such that every
table x admits D(x).  Exhaustive (vectorised).  Cost of a configuration = sum over gadgets of ceil(|S| m / 2)."""
import sys, itertools
sys.path.insert(0,'/tmp/pydeps')
import numpy as np
TAB=np.array([[ (r>>c)&1 for c in range(4)] for r in range(16)])
Bs=[(b1,b2) for b2 in (0,1) for b1 in (0,1)]
lits=[np.ones(16),-np.ones(16)]+[(-1.0)**TAB[:,c] for c in range(4)]+[-(-1.0)**TAB[:,c] for c in range(4)]
lits=np.array(lits)                                    # 10 sign functions
def sums(amps):
    out={}
    for combo in itertools.product(range(10),repeat=len(amps)):
        v=sum(a*lits[i] for a,i in zip(amps,combo)); out[tuple(v)]=combo
    keys=list(out); return np.array(keys),[out[k] for k in keys]
def check(cfg):
    A1,_=sums(cfg['1']); A2,_=sums(cfg['2']); A12,_=sums(cfg['12'])
    G=None; cnt=0
    for a12 in A12:
        ok=np.ones((len(A1),len(A2)),dtype=bool)
        for r in range(16):
            x=TAB[r]
            Gb=[A1[:,None,r]*b1+A2[None,:,r]*b2+a12[r]*(b1^b2) for (b1,b2) in Bs]
            one=[g for g,(b1,b2) in zip(Gb,Bs) if x[b1+2*b2]==1]; zero=[g for g,(b1,b2) in zip(Gb,Bs) if x[b1+2*b2]==0]
            if one and zero:
                mx=np.maximum.reduce([np.broadcast_to(z,ok.shape) for z in zero]); mn=np.minimum.reduce([np.broadcast_to(o,ok.shape) for o in one])
                ok&=mx<mn
            if not ok.any(): break
        cnt+=int(ok.sum())
    return cnt
if __name__=="__main__":
  cfgs=[ {'1':[1,1],'2':[1,1],'12':[1]}, {'1':[1,1],'2':[1,1],'12':[1,1]}, {'1':[2,1],'2':[2,1],'12':[2,1]},
       {'1':[1,1],'2':[1,1],'12':[2,1]}, {'1':[1,1,1],'2':[1,1,1],'12':[1]}, {'1':[1,1,1],'2':[1,1,1],'12':[1,1]},
       {'1':[1,1],'2':[1,1],'12':[1,1,1]}, {'1':[2,1,1],'2':[2,1,1],'12':[1,1]}, {'1':[1,1,1,1],'2':[1,1,1,1],'12':[1,1]},
       {'1':[1,1],'2':[1,1],'12':[1,1,1,1]} ]
  for cfg in cfgs:
      c=check(cfg); cost=lambda m: sum(len(cfg[S])*((len(S)*m+1)//2 if S!='12' else m) for S in cfg)
      print(f'{cfg}: feasible sign assignments = {c};  gate cost ~ {len(cfg["1"])+len(cfg["2"])}*ceil(m/2) + {len(cfg["12"])}*m',flush=True)
