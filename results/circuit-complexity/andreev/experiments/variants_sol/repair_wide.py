# Copyright (c) 2026 Christian Reitwiessner. All rights reserved.
# Authors: Christian Reitwiessner
from research import *
c=known(3)
for seed,(delete,free) in enumerate([(0,(0,1,2)),(3,(2,3,4)),(6,(4,5,6)),(10,(7,8,9))]):
    b=Circuit([g for j,g in enumerate(c.bottom) if j!=delete],[v for j,v in enumerate(c.v) if j!=delete],c.u,c.tau)
    print('DELETE',delete,'FREE',free,flush=True)
    got=cegis(2,3,10,15,seed=410+seed,base=b,free=free,bs=False,init_counts=True)
    if got:print('FOUND',got.format(),flush=True);break
