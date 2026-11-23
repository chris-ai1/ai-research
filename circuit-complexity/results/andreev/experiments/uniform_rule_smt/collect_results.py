#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Recover exact sample corpora and summarize the completed experiment runs."""
import json
from pathlib import Path
from itertools import product
from experiment import samples, save, target

ROOT=Path(__file__).resolve().parent
rows=[]
for directory in sorted(ROOT.iterdir()):
    if not directory.is_dir() or not (directory/'configuration.json').exists():
        continue
    cfg=json.loads((directory/'configuration.json').read_text())
    result=json.loads((directory/'summary.json').read_text())
    events=[json.loads(s) for s in (directory/'events.jsonl').read_text().splitlines()]
    # Preserve early runs faithfully: they predate explicit sample-policy metadata.
    policy=cfg.get('sample_policy','xor_corners' if directory.name=='coupled33_xor_curriculum' else 'legacy')
    count=cfg.get('requested_examples_per_size',4 if 'curriculum' in directory.name else 48)
    points=set()
    for k,m in cfg['sizes']:
        initial=list(product((0,1),repeat=(1<<k)+k*m)) if cfg['kind']=='calibration' else samples(k,m,count,cfg['seed'],xor_corners=policy=='xor_corners')
        points.update((k,m,tuple(p)) for p in initial)
    initial_count=len(points)
    assert initial_count==cfg['initial_points'],(directory.name,initial_count,cfg['initial_points'])
    for event in events:
        if event['phase']=='checker':
            points.update((event['k'],event['m'],tuple(p)) for p in event.get('points',[]))
    assert len(points)==result['examples']
    save(directory/'examples.json',dict(Authors='Christian Reitwiessner',sample_policy=policy,
         examples=[dict(k=k,m=m,point=list(p),target=target(k,m,p)) for k,m,p in sorted(points)]))
    learner=[e for e in events if e['phase']=='learner']
    checks=[e for e in events if e['phase']=='checker']
    rows.append(dict(run=directory.name,**result,initial_examples=initial_count,
                     sample_policy=policy,gate_counts=cfg['bottoms'],learner_call_seconds=[round(e['seconds'],4) for e in learner],
                     checker_counterexamples=sum(len(e.get('points',[])) for e in checks)))
save(ROOT/'campaign_results.json',dict(Authors='Christian Reitwiessner',runs=rows))
for row in rows:
    print(row['run'],row['result'],round(row['wall_seconds'],3),'seconds',row['learner_call_seconds'])
