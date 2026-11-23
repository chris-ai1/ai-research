# Copyright (c) 2026 Christian Reitwiessner. All rights reserved.
# Authors: Christian Reitwiessner
from research import *
m=int(sys.argv[1]);base=known(m)
for delete in range(base.S):
    gs=[g for j,g in enumerate(base.bottom) if j!=delete]
    bs=Circuit(gs,[v for j,v in enumerate(base.v) if j!=delete],base.u,base.tau)
    free=[min(delete,len(gs)-1)]
    print('REPAIR',m,'delete',delete,'free',free,flush=True)
    c=cegis(2,m,len(gs),6,100+delete,base=bs,free=free,bs=True,init_counts=True)
    if c is not None:
        print('FOUND',m,c.S,flush=True);print(c.format(),flush=True);break
