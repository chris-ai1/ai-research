#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Four-bottom parity10 feasibility, a valid restriction of both n64 targets."""
import json
from pathlib import Path
import time
from search import z3, Enc, parity_points, eval_circuit, save, label, spread

out=Path(__file__).with_name('parity10_S4_edges');out.mkdir(exist_ok=True)
pts=parity_points(10);started=time.monotonic()
e=Enc(pts,4,dict(vsym=True,usym='parity_even',seed=7))
for i in sorted(range(len(pts)),key=lambda i:(sum(pts[i][0]),pts[i][0])):e.add_point(i)
index={p:i for i,(p,y) in enumerate(pts)};clauses=0
for i,(p,y) in enumerate(pts):
    if y:
        for d in range(10):
            if not p[d]:
                q=list(p);q[d]=1;j=index[tuple(q)]
                e.so.add(z3.Or([z3.And(e.g[g,i],z3.Not(e.g[g,j])) for g in range(4)]));clauses+=1
e.so.set(timeout=180000);t0=time.monotonic();answer=e.so.check()
result=dict(status=str(answer).upper(),bottoms=4,dimension=10,points=len(pts),
            edge_clauses=clauses,solver_seconds=time.monotonic()-t0,wall_seconds=time.monotonic()-started,
            scope='Unrestricted parity10; fixed-parity-table/address restriction embeds into both n64 targets',
            solver=z3.get_version_string())
if answer==z3.unsat:
    (out/'unsat_instance.smt2').write_text(e.so.to_smt2())
    result['consequence']='Both n64 targets require at least 5 bottoms and 6 total gates.'
elif answer==z3.sat:
    c=e.circuit(e.so.model());assert not eval_circuit(c,pts);save(out/'candidate.json',candidate=c)
    result['caution']='SAT for a restriction is not an Andreev circuit.'
else:result['reason']=e.so.reason_unknown()
for lengths in ([12]*4,[7,7,6,6,6]):
    N=1<<len(lengths);x=tuple(c.bit_count()%2 for c in range(N));active=spread(lengths)[:10]
    for p,y in pts:
        a=[0]*sum(lengths)
        for d,b in zip(active,p):a[d]=b
        assert len(x)+len(a)==64 and label(x+tuple(a),lengths)==y
save(out/'summary.json',**result);print(json.dumps(result),flush=True)
