# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
import json
print('# Authors: Christian Reitwiessner')
results=[]
for k in range(1,17):
 N=1<<k;r=2;levels=0
 while r<=N:
  nxt=r+2*max(1,r*r//(8*N));levels+=1
  for t in range(r,min(nxt,N+2),2):assert 4*N*(t-r)<=t*t
  r=nxt
 results.append({'N':N,'positive_steps':levels})
print(json.dumps(results,indent=2))
with open('/tmp/andreev_gap/upper_astra/quantizer_results.json','w') as f:
 json.dump({'authors':'Christian Reitwiessner','results':results},f,indent=2)
