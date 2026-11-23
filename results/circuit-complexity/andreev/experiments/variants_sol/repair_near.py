# Copyright (c) 2026 Christian Reitwiessner. All rights reserved.
# Authors: Christian Reitwiessner
from research import *
c=Circuit.from_json(json.load(open(ROOT+'/near_2_3.json')))
Z=((np.arange(1024)[:,None]>>np.arange(10))&1).astype(int)
for S in (8,9,10):
    b=Circuit(c.bottom+[([0]*10,0)]*(S-c.S),c.v+[0]*(S-c.S),c.u,c.tau)
    print('REPAIR_NEAR',S,flush=True)
    got=cegis(2,3,S,12,seed=500+S,base=b,free=range(c.S,S),initial_points=Z)
    if got:print('FOUND',got.format(),flush=True);break
