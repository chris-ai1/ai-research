# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
import json,sys
from pathlib import Path
sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from construction import build
root=Path(__file__).resolve().parent
w=json.loads((root/'fixed_mask_witness.json').read_text())
c=build(w['k'],w['m'],w['r'],w['R'],{int(s):z for s,z in w['masks'].items()})
for key in ('gates','raw_top_weights','top_constant','top_threshold'):assert c[key]==w[key],key
k,m=w['k'],w['m'];N=1<<k;d=N+k*m
inputs=(np.arange(1<<d,dtype=np.int64)[:,None]>>np.arange(d))&1
score=inputs@np.array(w['raw_top_weights'])+w['top_constant']
for g in w['gates']:score+=g['top_weight']*(inputs@np.array(g['weights'])>=g['threshold'])
b=np.sum((inputs[:,N:].reshape(-1,k,m).sum(2)%2)*(1<<np.arange(k)),axis=1)
target=inputs[np.arange(len(inputs)),b]
errors=int(np.count_nonzero((score>=w['top_threshold'])!=target))
assert errors==w['errors']==8823
out={'Authors':'Christian Reitwiessner','serialized_raw_input_audit':'PASS','inputs':len(inputs),'bottoms':len(w['gates']),'errors':errors,'agreement_numerator':len(inputs)-errors,'agreement_denominator':len(inputs),'generic_builder_matches':True}
(root/'saved_audit.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
