import sys,re; sys.path.insert(0,'/tmp/andreev_gap/mixed_upper')
from realize import *
txt=open('logs/per_k3_bs_P2.log').read().split('after prune')[1]
atoms=[]
for line in txt.splitlines():
    if 'cost' in line and '((' in line:
        nums=[int(v) for v in re.findall(r'np\.int64\((-?\d+)\)',line)]
        tail=re.findall(r'\),\s*(\d+),\s*(\d+)\)\s*cost',line)[0]
        atoms.append((tuple(nums[0:3]),tuple(nums[3:11]),int(tail[0]),int(tail[1])))
rr=realize(3,1,2,atoms,ms=[11,15,20],linearD=True,bits_max_n=0)
out,W,D=rr
for (m,G,ok,okb,mn) in out: print('m',m,'gates',G,'formula',-(-27*m//2)+12,'ok',ok)
json_atoms=[(list(b),list(a),p,r,str(w)) for (b,a,p,r),w in zip(atoms,W)]
import json; json.dump({'atoms':json_atoms,'D_linear':[str(v) for v in D]},open('k3_family.json','w'),indent=1)
