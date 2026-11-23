import sys; sys.path.insert(0,'/tmp/andreev_gap/mixed_upper')
from realize import *
e=lambda c,N=4: tuple(1 if i==c else 0 for i in range(N))
atoms=[((1,0),e(1),2,0),((1,0),e(3),2,0),((0,1),e(2),2,0),((0,1),e(3),2,0),((1,1),e(3),2,0)]
for lin in (True,False):
    print('linearD',lin)
    r=realize(2,1,2,atoms,ms=range(1,9),linearD=lin)
    if r is None: print('  infeasible'); continue
    out,W,D=r
    print('  weights',[str(x) for x in W],' D',[str(x) for x in D])
