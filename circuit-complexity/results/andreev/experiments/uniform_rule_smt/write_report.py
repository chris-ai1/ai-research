#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Render an evidence-based report from completed run summaries."""
import json
from pathlib import Path

root=Path(__file__).resolve().parent
rows=json.loads((root/'campaign_results.json').read_text())['runs']
table=['| Run | Shared real holes | Bottom budgets | Samples, initial → final | Learner calls (seconds) | Wall seconds | Result |',
       '|---|---:|---|---|---|---:|---|']
for r in rows:
    table.append('| '+ ' | '.join([r['run'],str(r['parameters']),','.join(map(str,r['gate_counts'])),
         f"{r['initial_examples']} → {r['examples']}",', '.join(f'{v:.3f}' for v in r['learner_call_seconds']),
         f"{r['wall_seconds']:.3f}",r['result']])+' |')
success=[r['run'] for r in rows if r['kind']!='calibration' and r['result']=='VERIFIED_TRAINING_SIZES_ONLY']
outcome=('Finite training-size successes: '+', '.join(success)) if success else 'No new exact ordinary-Andreev circuit was certified. No asymptotic improvement was found.'
text=r'''<!-- Copyright (c) 2026 Christian Reitwiessner. -->
Authors: Christian Reitwiessner

# Actual shared-rule SMT experiment

## Outcome

OUTCOME

The affine-rule learner, fixed-candidate checker, exact candidate evaluation and multi-size counterexample loop are now implemented and were run. This is a bounded experiment with fixed public feature skeletons, not a search of the full AST grammar. The known m=2 rank family was recovered by fitting its shared top rule and verified on an untrained k=3 instance. That is a calibration, not a new construction.

## Targets and model

The principal training set is $(k,m)=(2,2),(3,3),(4,3),(4,4)$, with total raw-input sizes n=8,17,28,32. Each checker keeps all $2^k$ independent table bits and all km raw address bits. No generated-table restriction is used. One identical parameter tuple must fit every training size. Bottom gates and the top use >= ties; negative learner examples use strict <0. No per-gate unit margin, weight-magnitude bound, symmetry normalization, or bounded integer restriction is imposed. Parameters are reals during synthesis and exact rationals when extracted.

There are T gate types, and each type emits gates indexed by $0\le u<N$, $0\le r<m$. Thus S=TNm, plus one top; a valid all-size family with constant T would be $O(n^2/\log n)$ at balance. The count alone is not a construction: correctness is still unknown. Top weights and raw direct terms also follow shared rules.

For each of bottom table weights, address weights, thresholds and top weights there are q numerical holes per type. Direct table, direct address and top threshold rules each have q global holes. Total learned parameters: $(4T+3)q$. The two main skeletons use T1,q2 (14 holes; 8/24/48/64 bottoms) and T2,q3 (33 holes; 16/48/96/128 bottoms).

## Precise feature languages actually searched

All features below are PUBLIC functions of size, gate and coordinate indices. Learning coefficients of these features stays affine; no input bit appears in a feature generator. `experiment.Template.build` is the executable specification. Zero-based block and position indices are i,t. Define $\chi_u(c)=(-1)^{\operatorname{popcount}(u\mathbin{\&}c)}$.

The table feature menu is $[c=u]$, $\chi_u(c)$, and $\chi_{u\oplus1}(c)+[c=u\oplus1]$. The 14-hole skeleton uses the first two, the 33-hole skeleton all three. Thus dense multi-table-bit bottom gates are permitted.

For type h and row (u,r), the positional address features are

$$2^i(-1)^{\operatorname{popcount}((u\oplus((r+1)(i+1))\oplus h)\mathbin{\&}t)},$$
$$3^i(-1)^{\operatorname{popcount}((u+(h+1)(r+1)+i)\mathbin{\&}(t\oplus(t\!\gg\!1)))},$$
$$2^t(-1)^{\operatorname{popcount}((u\oplus((i+1)(h+1)))\mathbin{\&}(t+r))}.$$

The coupled address features are $2^i$ times 1 at t0 and $2\operatorname{bit}(u,i)-1$ otherwise; a second profile $3^i(-1)^{\operatorname{popcount}((u\oplus((r+1)(i+1))\oplus(h+1))\mathbin{\&}t)}$; and a row-local perturbation $2^i[t=r](2\operatorname{bit}(u,i)-1)$. These allow row-dependent directions, mixed signs and different magnitudes; they are not a single coherent direction with shifted thresholds.

The threshold menu is $(u+1,N(r+1),1)$; the top menu $(1,(-1)^r,(-1)^{\operatorname{popcount}(u)})$. Direct table features are $(1,(-1)^{c\mathbin{\&}1},c+1)$; direct address features $(m2^i[t=0],(-1)^t,(i+1)[t=m-1])$; top threshold features $(m,1,N)$. Each q-width rule uses the first q features, with independent named holes unless a field is explicitly frozen in a diagnostic. Public arithmetic powers and bit operations are evaluated outside SMT. All generated coefficients remain affine in the holes.

## Actual runs

TABLE

Wall time includes compilation and checking; solver calls are monotonic wall durations on a shared host. These are not controlled scaling benchmarks. Outer budgets are soft between calls; each call was explicitly bounded. A run stopping on the first UNKNOWN may use less than its outer budget. There were no manual interruptions of the recorded learner calls; Z3 sometimes reports its timeout as `canceled` rather than `timeout`.

The 14- and 33-hole initial joint runs each had 187 concrete samples across all four sizes. Their learner formulas had 6872 and 13744 activation Booleans respectively, despite the small numerical parameter counts. Each timed out on its first 60-second learner call.

The first small-curriculum run started from 16 total points. It fitted those points in about 13 seconds, but its hidden top weights were all zero, so it was merely a raw-affine partial fit. The full checkers refuted it at every training size, adding four exact counterexamples per size. Relearning on 32 points then timed out. This partial SAT model is explicitly refuted, not a circuit result.

The strengthened curriculum adds both XOR and complemented-XOR tables on four raw-address corners for each size. This prevents a raw-affine-only fit. It started from 48 points, produced a nontrivial candidate in about 39 seconds, and was again refuted at every size. All hidden top coefficients were active; all its table rows were nonliteral, and its relevant gate signs were not globally reorientable to coherent signs. After adding 16 exact counterexamples, relearning on 64 points timed out at 60 seconds. That tests genuinely mixed shared-rule candidates, but proves no circuit or general impossibility.

Two fixed-bottom diagnostics took the respective refuted candidate's bottom rules and fitted only the 15 remaining shared top/direct parameters to the larger corpus. Both were UNSAT in milliseconds, with no activation Booleans. This excludes only those frozen rules plus the declared top feature menu. It illustrates that fixed-bottom refitting is cheap here; it does not prove that every possible top over the library is impossible or that all shared-rule difficulty comes from a single source.

The dedicated n32-only positional run uses 64 bottoms, 14 holes, 48 samples, 3072 activation Booleans and a 300-second learner-call limit. Its recorded result is in the table above. Its parameters are not coupled to other sizes in this ablation; even success there would need multi-size and all-input checking. It is neither a free unrestricted n32 synthesis run nor a full grammar search.

## Calibration, verification, and implementation soundness

The calibration freezes known rank bottoms and fits only three shared top-rule parameters on EVERY raw input at (k,m)=(1,2),(2,2). It recovers the scalar multiple $(v,d,\tau)=(1/2,-1/2,1/2)$ of the known rank top rule. Arbitrary-table miters verify both training sizes and the held-out (3,2) case. It does not establish a new family or optimum.

`test_experiment.py` has four meaningful tests: 24 fixed-parameter learner/compiler equivalence comparisons, exact preservation under freezing, known-rank miter/tie handling and detection of an invalid zero rule. All passed. SAT learner models are independently evaluated using exact Fraction arithmetic on every accumulated sample before the symbolic checker. Every checker counterexample is likewise independently evaluated, then retained permanently. Checker UNSAT only verifies that fixed circuit at that finite size. No all-size theorem follows from the calibration or finite tests.

`rules.py` preserves the existing credited compiler/raw representation. The new learner uses Boolean activation equivalences and exact linear arithmetic with ITE for learned top weights. No real-times-real multiplication is hidden in the encoding. Coefficients are serialized as rational strings; integer positional features have explicitly generated magnitudes. Each sample corpus is preserved in examples.json, and checker witnesses are in events.jsonl. latest.json always labels an intermediate model UNPROVED_CANDIDATE; a later checker event can and does refute it. There is no accepted universal witness from a timed-out run.

## Reproduction and artifacts

Run from this directory with Python3; Z3 is loaded from /tmp/pydeps. The recorded version is 5.3.3. Use FRESH output directories: the driver rejects overwriting an existing event log. Exact model choices and individual calls may vary with the solver version, seed and host load.

```sh
python3 test_experiment.py
python3 experiment.py --kind calibration --timeout 30 --budget 90 --out replay_calibration
python3 experiment.py --kind positional --types 1 --width 2 --legacy-samples --timeout 60 --budget 180 --out replay_positional14
python3 experiment.py --kind coupled --types 2 --width 3 --legacy-samples --timeout 60 --budget 180 --out replay_coupled33
python3 experiment.py --kind coupled --types 2 --width 3 --legacy-samples --examples 4 --timeout 60 --budget 240 --out replay_weak_curriculum
python3 experiment.py --kind coupled --types 2 --width 3 --examples 4 --seed 11 --timeout 60 --budget 180 --out replay_xor_curriculum
python3 experiment.py --kind positional --types 1 --width 2 --only32 --legacy-samples --timeout 300 --budget 360 --out replay_n32_long
```

Early runs predate XOR-corner seeding; `--legacy-samples` deliberately preserves their old policy. The strengthened policy is the default for subsequent runs. `collect_results.py` reconstructs and verifies the exact sample corpora from the declared seeds/policies and saved checker events, then writes campaign_results.json. `write_report.py` renders this report from completed summaries. Frozen-bottom runs additionally specify --freeze-bottom PATH/TO/latest.json; the source models are preserved. They use no independent per-size fitted parameters.

## Interpretation and next bottleneck

This experiment validates an operational shared-rule loop on independent raw tables and reaches balanced n32 with meaningful gate budgets and a five-minute call. It does not validate the particular proposed feature families as adequate for the exact function. No restricted UNSAT is promoted to an unrestricted lower bound; UNKNOWN excludes no candidate.

The principal demonstrated obstacle is that reducing numerical holes leaves thousands of activation choices and strong cross-size constraints. More useful next experiments would alter the structural skeleton or use proof-motivated bottom features, rather than interpreting a timeout as evidence against an asymptotic construction. Fixed-bottom top fitting can cheaply screen proposed structures, but cannot discover directions outside the pool. A full structural-language enumerator and all-size proof engine remain unimplemented. No new constant, exponent, or logarithmic saving is claimed.
'''
text=text.replace('OUTCOME',outcome).replace('TABLE','\n'.join(table))
(root/'report.md').write_text(text)
print(outcome)
