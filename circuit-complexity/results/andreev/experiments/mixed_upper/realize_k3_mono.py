import sys,re; sys.path.insert(0,'/tmp/andreev_gap/mixed_upper')
from realize import *
txt=open('logs/per_k3_bs_P2.log').read().split('after prune')[1]
atoms=[]
for line in txt.splitlines():
    if 'cost' in line and '((' in line:
        nums=[int(v) for v in re.findall(r'np\.int64\((-?\d+)\)',line)]
        tail=re.findall(r'\),\s*(\d+),\s*(\d+)\)\s*cost',line)[0]
        b=tuple(nums[0:3]); a=tuple(nums[3:11]); p=int(tail[0]); r=int(tail[1])
        atoms.append((b,a,p,r))
print(len(atoms),'atoms; slope',sum(sum(abs(v) for v in b)/p for b,a,p,r in atoms))
for lin in (True,False):
    print('linearD',lin)
    rr=realize(3,1,2,atoms,ms=[1,2,3,4,5,6,8,10],linearD=lin,bits_max_n=20)
    if rr is None: print('  infeasible'); continue
    out,W,D=rr; print('  weights',[str(x) for x in W]); print('  D',[str(x) for x in D][:12])
    break
