# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Optional fixed-candidate checks; requires z3-solver, no synthesis search."""
import json
from pathlib import Path
import z3
from rules import rank_m2_program, smt_miter

out = {'Authors': 'Christian Reitwiessner',
       'copyright': 'Copyright (c) 2026 Christian Reitwiessner',
       'solver_version': z3.get_version_string(), 'checks': []}
for k, m in [(2, 2), (3, 2), (2, 3)]:
    solver = z3.Solver()
    solver.set(timeout=10000)
    solver.from_string(smt_miter(rank_m2_program().compile(k, m)))
    status = str(solver.check())
    assert status == ('unsat' if m == 2 else 'sat'), (k, m, status)
    out['checks'].append({'k': k, 'm': m, 'miter': status})
Path(__file__).with_name('miter_results.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out, indent=2))
