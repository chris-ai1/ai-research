#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Collect completed n64 unrestricted small-budget feasibility runs."""
import json
from pathlib import Path
from search import save

root=Path(__file__).resolve().parent
rows=[]
for directory in sorted(root.iterdir()):
    p=directory/'summary.json'
    if not p.is_file():continue
    row=json.loads(p.read_text());row['run']=directory.name
    if (directory/'configuration.json').exists():row['configuration']=json.loads((directory/'configuration.json').read_text())
    rows.append(row)
certificate=json.loads((root/'parity_certificate/parity8_S3.json').read_text())
save(root/'campaign_results.json',runs=rows,parity8_certificate=certificate)
table=['| Run | Bottom budget | Solver result | Solver seconds | Wall seconds |',
       '|---|---:|---|---:|---:|']
table.append(f"| parity8 restriction (both n64 targets) | 3 | {certificate['status']} | {certificate['solver_seconds']:.3f} | {certificate['wall_seconds']:.3f} |")
for row in rows:
    table.append(f"| {row['run']} | {row['bottoms']} | {row.get('result',row.get('status'))} | {row['solver_seconds']:.3f} | {row['wall_seconds']:.3f} |")
text=r'''<!-- Copyright (c) 2026 Christian Reitwiessner. -->
Authors: Christian Reitwiessner

# n=64: small-gate UNSAT experiment

## Instances and goal

The user requested n64 with small bottom-gate budgets, aiming for UNSAT. These runs use **unrestricted real bottom and top weights**, direct raw inputs at the top, and exact QF_LRA. They do not restrict a coefficient grammar, signs, weight magnitude, or a table-generator family. Every finite sample is a valid raw input, so UNSAT can prove a lower bound for the full target.

There is no exactly balanced equal-block instance at n64: k5 would require m=32/5. We declare both models precisely:

- `balanced`: N32 independent table bits and five parity blocks of lengths (7,7,6,6,6), giving32 address bits and64 inputs. This is the unequal-block version of the ordinary indexing-of-parities function, explicitly not an equal-block A_(k,m).
- `equal`: standard equal-block A_(4,12), with16 table bits and48 address bits, giving64 inputs. It is not the exactly balanced split.

The target in both cases is x_b, with b formed from the block parities. Counts below are BOTTOM gates; add one top gate. No optimality claim or asymptotic improvement is made.

## Actual outcomes

TABLE

Solver time excludes point encoding and SMT export, and may include several learner/checker calls. Host load and time limits differ; these timings are experiment records rather than a controlled scaling benchmark. UNKNOWN makes no infeasibility claim. A finite-subset SAT would not be an Andreev circuit without a full-domain miter UNSAT.

## Why the three-bottom UNSAT applies at n64

Fix every table bit to x_c=popcount(c) mod2. The target becomes parity of every address bit. Leave eight raw address coordinates free and fix all other address bits to zero. The remaining function is parity8. This restriction keeps every bottom gate an unrestricted LTF and keeps the top an LTF of bottom outputs and raw inputs: fixed table/address contributions merely shift thresholds. No gate is added.

The script explicitly constructs all256 corresponding64-bit raw inputs for BOTH target conventions and checks their labels. Exact SMT then proves that parity8 has no three-bottom circuit with raw top inputs. Hence neither n64 target has a circuit with at most three bottoms. The resulting lower bound is at least FOUR bottoms, FIVE total gates. This is a restriction-transfer result and a rerun of a known small parity obstruction, not evidence that general n64 synthesis or optimization has been solved.

The exported `parity_certificate/parity8_S3_unsat.smt2` was replayed successfully with Z3; `replay.json` records that call. This is a replayable SMT instance, not a Lean theorem or independently checked proof trace. All saved labels/embeddings and the encoder semantics are explicit.

## Direct n64 feasibility checks

For budget S, the driver starts with a parity cube of dimension min(2S+2,10) plus128 concrete points drawn from multiple spike, character and arbitrary independent tables and raw address arrangements. This gives132 points at S0,144 at S1,192 at S2, and1152 at S4/S5. Any duplicate point is removed. All input coefficients remain free reals; parameter count is S*66+65 (329 reals at S4,395 at S5). Initial and final actual corpora are saved in JSON.

If a learner model is SAT, every training point is reevaluated with exact Fractions, then a fixed-candidate symbolic miter searches ALL independent table/address bits for a counterexample. Counterexamples are exactly checked and retained. Only checker UNSAT would certify a full circuit. All calls are individually timed and bounded. No candidate is accepted on samples alone.

Direct UNSAT exports `unsat_instance.smt2`. The ordinary runs use only gate complementation and permutation to make top gate-output weights nonnegative and sorted. Each unrestricted finite gate can be independently rescaled to unit negative margin without changing its Boolean behavior; this is WLOG here, unlike in a shared-rule grammar. The same applies to the unrestricted top. There is no finite weight bound.

The `input_symmetry` variants additionally normalize direct address weights to nonnegative and sorted within blocks. This is WLOG for the FULL Andreev target: flipping one raw address bit and simultaneously permuting table labels by that block's parity flip preserves the target and changes the sign of that direct coefficient. Within-block permutations preserve all parities. These transformations preserve the gate count and unrestricted weight model. If a full circuit exists, some normalized full circuit fits every selected sample; consequently UNSAT of the normalized sample problem still excludes the full circuit. We do not claim every arbitrary sample-only classifier can be normalized while retaining its sample labels, nor impose this normalization on a shared coefficient language.

## Reduced parity10 edge experiment

An additional probe attempts to exclude FOUR bottoms by embedding parity10 in either n64 target. The complete1024-point parity cube is solved with valid parity symmetries and redundant edge clauses. For even dimension, input-flip plus output-complement symmetries allow nonnegative sorted direct weights. Gate-output weights are also nonnegative. Along an edge from odd to even Hamming weight, the required output drops while the direct term cannot decrease; therefore some bottom gate must turn off. The OR of those off-transition conditions is necessary and does not restrict valid circuits.

If this probe is UNSAT it transfers an at-least-five-bottom lower bound to both n64 targets. If UNKNOWN it supplies no stronger bound; if SAT it supplies only a parity-restriction circuit, not an Andreev circuit. Its actual outcome is listed above. The embedding labels are checked over every parity10 point.

## Soundness checks, files and reproduction

Four tests pass in `test_search.py`: all256 parity8 embeddings for both n64 models; variable-block symbolic checker correctness on a known rank fixture and a false circuit; exact sample dimensions/labels/deduplication/serialization; and full-cube correctness after the input-symmetry normalization of a known fixture. The known-fixture test is a guardrail, not a replacement for the symmetry proof.

`mscore.py`, `smt_symbolic_check.py`, and `rules.py` preserve the earlier encoder/checker/compiler, with provenance in environment.json. The search/parity-edge/test/report drivers are newly authored. A serialization-helper keyword bug in the initial launch was corrected before the successful direct learner calls; the parity8 solve was rerun so only complete recorded runs are used. No failed initialization is counted as SAT, UNSAT or timeout.

```sh
python3 test_search.py
python3 search.py --certificate --timeout 180 --out replay_parity8
python3 search.py --S 4 --timeout 600 --budget 660 --out replay_balanced_S4
python3 search.py --blocks 12,12,12,12 --S 4 --timeout 600 --budget 660 --out replay_equal_S4
python3 search.py --S 5 --timeout 300 --budget 360 --out replay_balanced_S5
python3 search.py --S 4 --input-symmetry --timeout 300 --budget 360 --out replay_balanced_S4_sym
python3 search.py --blocks 12,12,12,12 --S 4 --input-symmetry --timeout 300 --budget 360 --out replay_equal_S4_sym
python3 parity10_edges.py
```

Use fresh output directories. Z3 is loaded from /tmp/pydeps; no truth-table enumeration over all2^64 raw inputs occurs. UNSAT instances are preserved, as are explicit embeddings, corpus points, call logs, solver version and exact model scope. A timeout is recorded as UNKNOWN, never as a lower bound. Unrelated processes were preserved.
'''
(root/'report.md').write_text(text.replace('TABLE','\n'.join(table)))
print('\n'.join(table))
