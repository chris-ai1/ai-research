# Copyright (c) 2026 Christian Reitwiessner. All rights reserved.
# Authors: Christian Reitwiessner
from research import *
m=6;c=known(m)
print('BASELINE',c.S,check(c.to_json(),andreev_target(2,m),5000),flush=True)
for delete in (0,c.S//2,c.S-1):
    b=Circuit([g for j,g in enumerate(c.bottom) if j!=delete],[v for j,v in enumerate(c.v) if j!=delete],c.u,c.tau)
    free=[min(delete,b.S-1)]
    print('DELETE',delete,'FREE',free,flush=True)
    cegis(2,m,b.S,10,seed=delete+301,base=b,free=free,bs=True,init_counts=True)
