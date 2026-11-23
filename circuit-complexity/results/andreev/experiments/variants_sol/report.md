<!-- Copyright (c) 2026 Christian Reitwiessner. All rights reserved. -->
Authors: Christian Reitwiessner

# PATH 2: constructive SMT experiments for ordinary Andreev

## Result

**No improved full-domain construction was found.** In particular, this work does not improve the leading $5/16$ constant, the $d''$ construction, or the known 11-bottom-gate construction for $(k,m)=(2,3)$. All sizes below count bottom gates; add **one top gate**, which reads both bottom outputs and raw inputs.

The most concrete new search artifact is a mixed-sign **7-bottom-gate failed candidate**, correct on 968/1024 inputs of $A_{2,3}$. Its 56 failures are confined to inputs having an address block exactly `011`. This candidate is **not a circuit for ordinary Andreev**. The concentration of its error on two small arrangement classes is a plausible local-repair target; no successful repair or asymptotic pattern was obtained.

Known constructions were saved and symbolically rechecked: $(2,3)$ has 11 bottom + 1 top; $(2,4)$ has 12 + 1; $(2,6)$ has 18 + 1. These are baselines, not discoveries.

## Exact target-circuit CEGIS

`research.py:cegis` integrates the existing unrestricted-real `mscore.Enc` learner with a frozen rational candidate and `smt_symbolic_check.check`. The target consists of $k$ block-XOR circuits and a balanced mux over **all** $2^k$ symbolic table bits. No target truth table is constructed in this learner/checker loop.

The free search starts from 24 random concrete inputs; each symbolic SAT counterexample is checked with exact arithmetic, labelled by ordinary Andreev, and appended to the incremental learner. Checker UNSAT is full-domain equivalence. Checker or learner UNKNOWN never certifies anything. The seven-gate unrestricted $(2,3)$ run reached 114 learner calls and 137 selected points before its 45-second solver budget expired with UNKNOWN. It found no verified circuit.

Warm-started searches fix selected bottom gates from a good circuit, delete a gate, free selected remaining bottom gates, and resynthesize **all** top weights and direct input wires. Free gates may have arbitrary real weights; the wider repairs permit genuinely mixed signs. No input or gate symmetry breaking is imposed. Optional block symmetry is an explicit search restriction.

Unit negative margins in the learner are legitimate for each unrestricted real free gate: finite strict separation can be scaled independently. Frozen gates are first converted to integer weights and an integer cutoff, so a false gate has value at most cutoff minus one. All top parameters remain unrestricted and can be scaled to a unit negative margin. There are no bounded bottom weights in these searches.

For local repairs, the initial count representatives are only **training examples**. When free/mixed gates are present they do not stand for the full domain. Symbolic checking caught this distinction immediately. No candidate was accepted from representative-point agreement.

## Experiments and budgets

Budgets are solver/loop budgets, excluding some initialization/encoding work. Runs are finished; no background solver remains from this task.

| Experiment | Budget | Result |
|---|---:|---|
| Free real $(2,3)$, 7 bottoms, symbolic target CEGIS | 45 s | UNKNOWN after 114 calls / 137 examples |
| Delete each of the 11 known $(2,3)$ gates, free one neighboring remaining bottom, block symmetric | 6 s each, 11 attempts | 10 restricted learner UNSAT; 1 UNKNOWN |
| Delete a known gate, free three bottoms with arbitrary mixed signs, $(2,3)$, 10 bottoms | 15 s each, 4 attempts | Each produced partial candidates and symbolic counterexamples, then UNKNOWN |
| $(2,6)$: delete gate 0, 9, or 17 from known 18; free one remaining bottom, block symmetric | 10 s each, 3 attempts | All UNKNOWN; not a 17-gate impossibility result |
| Warm-start pool LP, $(2,3)$, representative inputs plus symbolic counterexamples | 30 restarts, then 5 diagnostic restarts | Refuted 7--10-gate candidates; retained verified known 11 |
| Warm-start pool LP, $(2,3)$, all 1024 bit inputs | 20 completed fast restarts | Best 11; other supports 12--18 or larger |
| Warm-start pool LP, $(2,4)$, representative inputs plus symbolic checker | 10 restarts | Best known 12 retained; no improvement |
| 60-gate pool: known $(2,3)$ gates plus $d''$ gates; bounded top weights/cutoff in $[-64,64]$; ask at most 10 selected gates | 50 s cap | HiGHS reported infeasible; numerical restricted evidence only |
| Retain seven near-candidate gates, add one / two / three arbitrary free bottoms and refit top on all 1024 inputs | 12 s each | One additional gate: exact restricted UNSAT. Two or three: UNKNOWN |

A preliminary slow full-input pruning run was stopped when replaced by the faster implementation; it is not included as a completed restart campaign. An initial 3-restart representative-only run was also diagnostic, not evidence of a construction. LPs use rational reconstruction and exact arithmetic to check their concrete constraints before a candidate reaches the symbolic checker. The fixed-pool MILP is a SAT finder, and its infeasibility message is **not** promoted to an exact SMT UNSAT or an unrestricted lower bound.

The pools combine known gates, input automorphisms (address-bit flips with the induced table permutation, block swap, and global table complementation), and $d''$ gates. Address flips introduce mixed signs. They are candidate generators, not symmetry restrictions on all circuits.

## Readable seven-gate near-solution

Write address bits as $(a_{11},a_{12},a_{13})$ and $(a_{21},a_{22},a_{23})$, and set
$$s_1=a_{11}+a_{12}+a_{13},\qquad r_i=a_{i1}-a_{i2}-a_{i3}.$$
The gates are
$$g_0=[s_1-x_3\ge1],\quad g_1=[s_1-x_3\ge3],$$
$$g_2=[r_1-x_0\ge0],\quad g_3=[r_2-x_0\ge0],\quad g_4=[-r_2-x_1\ge0],$$
$$g_5=[r_1+r_2-x_0\ge1],\quad g_6=[r_1+r_2-x_0\ge-1].$$
Its top output is
$$[-4g_0-4g_1-6g_2-6g_3-8g_4+6g_5+6g_6+2x_2+2s_1-4r_2\ge-3].$$
`near_2_3.json` contains these exact integer coefficients and explicitly labels the candidate REFUTED_NOT_A_CONSTRUCTION. `analyze.py` confirms equality of the formula and serialized candidate on every input.

The erroneous block-pattern pairs, with counts over the 16 possible tables, are:

| Block 1 | Block 2 | Wrong tables |
|---|---|---:|
| 011 | 000 | 4 |
| 011 | 100 | 4 |
| 011 | 110 | 4 |
| 011 | 101 | 4 |
| 100 | 011 | 8 |
| 010 | 011 | 8 |
| 001 | 011 | 8 |
| 011 | 011 | 8 |
| 111 | 011 | 8 |

Thus all inputs avoiding `011` in both blocks are correct. This is an arrangement defect, not a parity-only defect. Its natural extension $r_i=a_{i1}-\sum_{j>1}a_{ij}$, with the same seven thresholds/top formula, has respectively 0/64, 0/256, 56/1024, and 608/4096 errors for $m=1,2,3,4$. The successful $m\le2$ cases are worse than the known three-gate circuits. The candidate therefore supplies no improved family.

## Known family: independent integer formula and general verification

For reproducibility, `known(m)` now directly writes the existing five-staircase Theorem G construction, avoiding a numerical LP for the baseline. Its score is
$$T=4\left\lfloor\frac{s_1+x_1}{2}\right\rfloor+6\left\lfloor\frac{s_1+x_3}{2}\right\rfloor+4\left\lfloor\frac{s_2+x_2}{2}\right\rfloor+6\left\lfloor\frac{s_2+x_3}{2}\right\rfloor-6\left\lfloor\frac{s_1+s_2+x_3}{2}\right\rfloor+2x_0-2s_1-2s_2.$$
Output is $[T\ge1]$. Every floor is the sum of even-threshold gates. This uses
$$4\left\lfloor\frac{m+1}{2}\right\rfloor+m$$
bottom gates, hence $3m$ for even $m$ and $3m+2$ for odd $m$.

Using $b_i=s_i\bmod2$, the score reduces to
$$T=\begin{cases}
2x_0 & b=00,\\
2x_0+4x_1-2 & b=10,\\
2x_0+4x_2-2 & b=01,\\
2x_0+4x_1+4x_2+12x_3-10 & b=11.
\end{cases}$$
In each case the designated table bit is 1 exactly when $T\ge1$. This is a proof for all $m$, but **is a restatement of the known family**, not a new upper bound. Exact symbolic rechecks for $m=3,4,6$ completed in approximately 0.003, 0.013, and 0.179 seconds in the final run. This measures these fixed candidates only, not general verifier scalability.

## Reproduction and artifacts

All files created here credit Christian Reitwiessner. Only this directory was changed; other agents' files and jobs were left intact. No material was posted online.

Run with `OPENBLAS_NUM_THREADS=1 python3 /tmp/andreev_gap/variants_sol/<script>`:

- `analyze.py`: exact failed-candidate diagnostics, neighboring $m$, and symbolic baseline checks.
- `research.py cegis 2 3 7 45`: unrestricted-real symbolic-target CEGIS.
- `research.py prune 3 30`: warm-start mixed-pool LP with symbolic counterexamples.
- `research.py prunefull 3 20`: full-input warm-start pruning.
- `research.py prune 4 10`: neighboring parameter search.
- `repair.py 3`: eleven one-free-gate deletion repairs.
- `repair_wide.py`: four mixed-sign three-free-gate deletion repairs.
- `larger.py`: three $(2,6)$ deletion searches.
- `repair_near.py`: exact full-input repairs of the failed candidate.
- `pool_milp.py 3`: bounded numerical fixed-pool SAT search.

The scripts add `/tmp/pydeps` themselves. They use the existing `/tmp/andreev_gap/mixed_sign/mscore.py`, `/tmp/andreev_gap/push_upper/constr3.py`, and associated local modules. Local copies of `sc_circuit.py` and `smt_symbolic_check.py` are included. Baseline witnesses are `baseline_2_3.json`, `baseline_2_4.json`, `baseline_2_6.json`; `best_2_*.json` also contain retained baselines, not improved discoveries. Logs with corresponding script names record every conclusion above.

The next focused constructive question is whether changing the mixed bottom gates themselves, rather than merely adding one gate, can repair the `011` defect below 11 bottoms. Two- and three-added-gate repairs remain UNKNOWN. Nothing here supports extrapolating the failed candidate to a better asymptotic upper bound.
