#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Generate a complete run index from retained logs and witnesses."""
from pathlib import Path
import json,re
import engine as e
root=Path(__file__).resolve().parent;rows=[]
for d in sorted(root.iterdir()):
 if not d.is_dir() or d.name.startswith('__'):continue
 ev=[]
 if (d/'events.jsonl').exists():
  for line in (d/'events.jsonl').read_text().splitlines():
   try:ev.append(json.loads(line))
   except json.JSONDecodeError:pass
 files=list(d.glob('verified_*.json'));best=min(files,key=lambda p:int(p.stem.split('_')[-1])) if files else None
 obj=json.loads(best.read_text()) if best else None
 if (d/'summary.json').exists():
  summary=json.loads((d/'summary.json').read_text());k,m,r=[summary[t] for t in ('k','m','r')];S=summary['bottom_library'];method='MILP';status=summary['message']
 elif ev:
  info=next((x for x in reversed(ev) if 'k' in x and 'm' in x),None)
  if info is None:continue
  k,m,r=[info[t] for t in ('k','m','r')];S=info.get('S',info.get('library'));method=info.get('mode','LP')
  statuses=[x['status'] for x in ev if x.get('phase')=='learner']
  status=('learner '+statuses[-1]) if statuses else 'LP feasible'
  if any(x.get('status')=='UNKNOWN' for x in ev):status+='; checker UNKNOWN'
 else:continue
 row=dict(run=d.name,k=k,m=m,r=r,method=method,attempted_S_or_library=S,status=status,witness=str(best.relative_to(root)) if best else None,best_S=len(obj['candidate']['bottom']) if obj else None,family_symbolic=(obj.get('family') or {}).get('status') if obj else None,ordinary_symbolic=(obj.get('ordinary') or {}).get('status') if obj else None,exact_matrix=obj.get('exact_matrix') if obj else None)
 rows.append(row)
e.save(root/'campaign_matrix.json',dict(rows=rows))
lines=['<!-- Copyright (c) 2026 Christian Reitwiessner. -->','Authors: Christian Reitwiessner','','# Actual completed run matrix','','`full` denotes the separate arbitrary-table mode ($r=-1$). S counts bottoms; add one for total gates. “No witness” and UNKNOWN make no infeasibility claim. LP/MILP witness validity is independently exact even if the symbolic family checker times out.','','| Run | k,m,r | Method; attempted S/library | Best S | Family symbolic | Ordinary symbolic | Run termination |','|---|---|---|---|---|---|---|']
for x in rows:
 lines.append('| '+ ' | '.join([x['run'],f"{x['k']},{x['m']},{'full' if x['r']<0 else x['r']}",f"{x['method']}; {x['attempted_S_or_library']}",str(x['best_S']) if x['best_S'] is not None else 'no witness',str(x['family_symbolic'] or '—'),str(x['ordinary_symbolic'] or '—'),x['status']])+' |')
(root/'campaign_matrix.md').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
