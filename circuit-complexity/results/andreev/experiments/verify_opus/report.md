# Independent verification of `z3_min.py` (+ `five_eighths.py`, `cpsat_min.py`)

Verifier: independent. I did not read `/tmp/andreev_gap/verify/`. The original files were not modified;
the copies used for runs are `orig_*.py` in this directory. All runs used `python3 -I` with
`/tmp/pydeps`. The machine was shared and heavily loaded (load average 15–56 on 20 cores, mostly
from other jobs), so **absolute timings are noisy**. Speedups below come from runs started
**concurrently and with the same seeds**, and are given as ranges.

## 1. Verdict

`z3_min.py` is **correct** for the model it states. The encoding is sound and complete for real
weights. The point sets and targets are right in both modes. "First SAT S" is the true minimum. I
found **no new bug in the encoding**, and both recently fixed bugs are fixed: block weights are
multiplied in through `al[j][d]*p[d]`, and the `CheckSatResult` crash is gone. Every minimum it
reports was reproduced by my own code (my own point generator, encoding and checker). Every SAT
model was verified by exact rational evaluation on all inputs.

The main problem is one of **interpretation**, not code. `blocksym` is a *restriction* of the
problem, so its UNSAT answers are **not** lower bounds for general depth-2 circuits (see 2.4).

## 2. Correctness analysis

### 2.1 Margin normalization (WLOG, for any finite point set, including coordinates in 0..m)
Take a gate $[\alpha\cdot p\ge\theta]$ on a finite set $P$. Let $\delta=\min_{p:\alpha\cdot p<\theta}(\theta-\alpha\cdot p)>0$.
Then $(\alpha,\theta)/\delta$ computes the same function on $P$, with positive points
$\ge\theta'$ and negative points $\le\theta'-1$. Only finiteness of $P$ is used; the coordinate
range (0/1 or 0..m) does not matter. The Boolean `g` is forced to equal the gate value, because the
two implications exclude each other. The top gate is normalized independently, and scaling the
bottom gates does not change their 0/1 outputs. **OK.**

### 2.2 Inputs and target
`points()` was compared with my own generator (`common.andreev_points`): same multiset of (point,
target) in both modes for every instance tested (`orig_models.py` asserts this). $b=\sum_i (s_i \bmod 2)2^i$,
with $x$ indexed by the integer $b$. **OK.**

### 2.3 "minimum = first SAT S"
Feasibility is monotone in $S$: pad with a gate that has $v_j=0$. The loop stops at the first
non-UNSAT answer and labels UNKNOWN as "undecided". **OK.** Corollary that the original does not use:
a single UNSAT at $S$ already proves $\min\ge S+1$, so the smaller $S$ need not be run. My script
uses this (`--only S`). All its symmetry breaking still admits padded circuits.

### 2.4 blocksym: sound as an upper bound, NOT a lower bound
A blocksym gate with weight $\beta_i$ on $s_i$ is the full gate with weight $\beta_i$ on every bit
of block $i$, with the same gate count, top gate included. So $\min_{full}\le\min_{blocksym}$.
The converse needs a symmetrization theorem for depth-2 threshold circuits, which does not exist
in general: averaging over block permutations does not keep the gate count.
**Consequence: blocksym UNSAT results, such as the job now running `z3_min.py blocksym 300 ... 2,3 2,4`,
do not prove lower bounds for Andreev's function.** They only say that no *block-symmetric* circuit
of that size exists. Wherever both were computed the two agree: (1,1..4), (2,1) (identical
instance), (2,2) = 3. A full-mode proof is needed for any general claim.

Blocksym is also monotone in $m$: restricting to $s_i\le m-1$ gives blocksym$(k,m-1)$, and the
same holds for full mode with extra bits set to 0. So results at small $m$ give lower bounds at
larger $m$ for free.

### 2.5 A valid sub-instance that turned out useless ("thermo")
Restricting full mode to thermometer blocks $1^{s}0^{m-s}$ gives a point set as small as
blocksym's. Its UNSAT results *are* valid general lower bounds, because it is a subset of the full
constraints. It is useless, though: on thermometer strings, parity is the affine function
$\sum_l(-1)^{l+1}a_l$. So thermo$(1,m)=1$ and thermo$(2,m)=3=$ full(2,1). Any useful sub-instance
must keep block parity non-affine. It is kept as `min_circuit.py thermo` for completeness.

### 2.6 Issues found (severity)

| # | file | severity | issue |
|---|------|----------|-------|
| 1 | z3_min.py (use of) | **High (interpretation)** | blocksym "minimum" is printed with no caveat. Its UNSAT values are not lower bounds for general circuits (2.4). Only full-mode UNSATs are. |
| 2 | cpsat_min.py | **Medium** | Bottom weights are restricted to $\lvert w\rvert\le3$ and top weights to $\lvert v\rvert\le4nN$, with no justification. Its UNSAT is not a proof; its "minimum" is only an upper bound on the blocksym minimum. Valid bounds are in section 3. |
| 3 | cpsat_min.py | Low | It prints `ours 5/8: {ours-1}`, but `five_eighths.py` uses exactly `formula` bottom gates (checked: gates = formula for 15 cases), so the printed number is one too small. |
| 4 | five_eighths.py | Low | For $n>16$, `correct=True` is based on 20 000 random inputs, not a proof. I re-checked **exhaustively with exact integer arithmetic** for all $n\le 24$ (k,m up to (4,2), (3,3), (2,6)): all correct, with top margin $\ge N$ on both sides (`fe_exact.py`, `fe_exact.log`). Also, it does not add `/tmp/pydeps` to `sys.path`, so it fails under `python3 -I`. |
| 5 | z3_min.py | Low | SAT circuits are never extracted or checked, there is no seed control, the per-S timeout is the only limit, and the S loop silently ends at 29. All are handled in `min_circuit.py`. |

`five_eighths.py`'s own check does what it claims for $n\le16$: exhaustive, integer-valued
weights, so the float tolerance is harmless. All its circuits are far above the computed minima
(e.g. (2,2): 43 against 3), so there is no conflict.

## 3. Independent reproduction

* **min_circuit.py**: my own z3 encoding (own point generator, symmetry breaking, different point order).
* **cpsat_check.py** (OR-Tools CP-SAT) and **milp_check.py** (HiGHS MILP, big-M) use **integer**
  weights within *proven* bounds. Argument: fix the bottom functions. The margin-1 realizations form
  a pointed polyhedron whose rows are $\pm(p,-1)$, plus the unit rows for $v_j\ge0$. A vertex is
  $B^{-1}c$ with $c\in\{0,1\}^d$. Multiplying by $\lvert\det B\rvert$ gives an integer realization
  with margin $\ge1$ and entries $\lvert\det B_i\rvert$. Full mode: after sign changes these are
  0/1 matrices, so $\lvert\det\rvert\le (d+1)^{(d+1)/2}/2^d$ (e.g. bottom ≤ 33, top ≤ 196 for
  (2,1), S=2). Blocksym: Hadamard, $(R^2+1)^{d/2}$. This is done per gate, then for the top gate
  given the bottom functions. Complementing gates so that $v_j\ge0$ and sorting by $v$ are applied
  before taking the vertex and as a relabeling, so the bounds still hold.
* Every SAT answer from every tool is re-evaluated **exactly** (`fractions.Fraction`) on all
  inputs by `common.eval_circuit`. For the original script, `orig_models.py` runs its unchanged
  encoding, extracts the model and checks it.

| instance | original z3_min | min_circuit (z3, mine) | CP-SAT, proven bounds | MILP, proven bounds | orig SAT model exact check | five_eighths UB |
|---|---|---|---|---|---|---|
| blocksym (1,1) | 1 | 1 | 1 | 1 | OK | 8 |
| blocksym (1,2) | 1 | 1 | 1 | 1 | OK | 11 |
| blocksym (1,3) | 2 | 2 | 2 | 2 | OK | 14 |
| blocksym (1,4) | 2 | 2 | 2 | 2 | OK | 17 |
| blocksym (1,5), (1,6) | not run (full (1,5) = 3 in z3_full.log) | 3, 3 | – | – | – | 20, 23 |
| blocksym (2,1) = full (2,1) | 3 | 3 | ≥2 (S=1 UNSAT 3 s; S=2 UNKNOWN 1 h) | ≥2 (S=2 UNKNOWN 1 h) | OK | 31 |
| blocksym (2,2) | 3 | 3 | – | ≥2 (S=2 UNKNOWN 1 h) | OK | 43 |
| blocksym (2,3) | ≥4 (S=3 UNSAT; S=4 UNKNOWN at 2400 s) | ≥4 (S=4 UNKNOWN at 3600 s, single and 32-cube) | – | – | – | 55 |
| blocksym (2,4) | – | **≥5** (S=4 UNSAT, 317 s, portfolio 3) | – | – | – | 67 |
| full (1,1) | 1 | 1 | 1 | 1 | OK | 8 |
| full (1,2) | 1 | 1 | 1 | 1 | OK | 11 |
| full (1,3) | 2 | 2 | 2 | 2 | OK | 14 |
| full (1,4) | 2 | 2 | 2 | 2 | OK | 17 |
| full (2,1) | 3 | 3 | ≥2 | ≥2 | OK | 31 |
| full (2,2) | 3 | 3 | – | – | (SAT verified by min_circuit) | 43 |
| full (2,3) | – | ≥3 (from (2,2) by restriction); S=3 UNKNOWN (1 h on 6-core cubes; 50 min with a 4-seed portfolio) | – | – | – | 55 |

All SAT and UNSAT answers agree wherever two tools finished. The k=2, S=2 UNSAT cases are confirmed
by two independently written z3 encodings: the original, and mine under 6 symmetry/tactic
configurations and many seeds, all UNSAT. CP-SAT and MILP with the proven (large) weight bounds
could not finish them within 1 h. Everything else is certified by a non-z3 method as well.

## 4. Efficiency

The decisive cost is the **last UNSAT** ($S=\min-1$). Smaller S take <5 % of the time (e.g. blocksym
(2,3): S≤2 together 1–3 s, against 40–280 s for S=3). So incremental solving across S could save
at most a few percent and was not pursued. Use `--only S` instead: one UNSAT already proves
$\min\ge S+1$.

### 4.1 What helped (fair: same seeds, run concurrently; "orig" = my script with the original's encoding, `--sym none --tactic qflra --order natural`)

| instance (UNSAT) | orig-equivalent | new default (1 core) | speedup | 3-seed portfolio (3 cores, wall) |
|---|---|---|---|---|
| full (2,1) S=2, 4 seeds | 26.5–31.2 s (mean 29.7) | 5.0–9.7 s (mean 7.5) | **4.0×** | 4.5 s |
| full (2,2) S=2, 3 seeds | 74.9–81.9 s (mean 78.8) | 31.2–49.9 s (mean 42.5) | **1.9×** | – |
| blocksym (2,3) S=3, 5 seeds | 59–283 s (mean 152, median 134) | 40–78 s (mean 56, median 43) | **2.7×** (mean) | 23–27 s (≈6× vs. orig mean) |

The actual original `z3_min.py`, run once, took 15–25 s / 58–145 s / 141 s on these three, which
is inside the orig-equivalent ranges.

The new defaults are:
* **Sign + permutation symmetry breaking on the top weights (`--sym vpos+sort`)**: $v_j\ge0$
  (complement the gate: $(\alpha,\theta,v)\to(-\alpha,1-\theta,-v)$, $\tau\to\tau-v$, margins kept)
  and $v_1\le\dots\le v_S$. This was the single biggest gain. It is an arithmetic constraint, which
  LRA propagates well. Sweep on full (2,1) S=2, 12 concurrent runs: none 57–106 s, comp 66–70,
  comp+lex 65–68, **vpos+sort 21–25**.
* **`arith.solver=2`** (the old z3 simplex): comp+lex 66 → 38 s, vpos+sort 22 → 18 s on average; on
  blocksym (2,3) S=3 within noise (72/165 against 126/141 s).
* **Seed portfolio (`--portfolio P`)**: z3's run time varies ~5× across seeds, so running P seeds
  and taking the first answer gives good wall-clock gains (above).

### 4.2 What did not help (measured, kept as options)
* Boolean **lex ordering of gate truth tables** (`comp+lex`), and the **lex-leader of gate 0 under the
  full symmetry group of A** (`--glex`: table complement, address XOR / bit flips, permutations
  inside blocks, block swaps; |G| = 16 for (2,1), 256 for full (2,2), 9216 for full (2,3)). Correct
  (all minima reproduced), but on blocksym (2,3) S=3 they took 480–690 s against 40–165 s for
  vpos+sort. The many auxiliary Booleans slow the SMT search.
* **Valid cuts** (`--cuts 1`): a threshold gate is never XOR on an axis square; it is monotone along
  lines; on XOR squares of A some bottom gate must be non-additive. No gain (19–25 s against 13–24 s).
* **Redundancy cuts** (`--nonred 1`, sequential S only): a minimum circuit has no constant,
  dictator or duplicate/complementary gate, and $v_j\ne0$. No clear gain (41/82 s against 39/102 s).
* **CEGAR on points**: needs 54–60 of 64 points before UNSAT, and 2–4× slower because z3 is slower
  in incremental mode.
* **Cube-and-conquer** (`--jobs/--cube`): splitting on gate-output literals does not make cubes
  easier. Sum of cube times ≈ 7–8× a single run, with no wall-clock gain (blocksym (2,3) S=3: 78 s
  on 8 cores against 40–78 s on 1).
* **CP-SAT / HiGHS with proven integer bounds**: very fast for k=1, but **UNKNOWN after 1 h** on
  (2,1) S=2, which z3 solves in 5–30 s. Fine as certificates for small cases, not as a main engine.

### 4.3 Frontier reached (UNSAT for S as large as possible)
* blocksym (2,3): $\ge4$ proved (UNSAT S=3, 23–78 s). S=4 was UNKNOWN after 1 h (single, and 8-core cubes).
  blocksym (2,4): **$\ge5$ proved** (S=4 UNSAT in 317 s wall, 3-seed portfolio, by `min_circuit.py`). This is new, and is a blocksym-only statement.
* full (2,3): $\ge3$ (inherited from full (2,2)). S=3 is UNKNOWN after 1 h (6-core cubes) and after 50 min (4-seed portfolio).
* For general circuits, the best proved bound per instance is the full-mode result: full (2,1) = full (2,2) = 3.

Suggestions for larger instances: run full mode with `--portfolio` (blocksym UNSAT does not
transfer), and look for **sub-instances** that keep block parity non-affine (e.g. two coordinates
per block taking all 4 patterns, with the other bits fixed). These give valid general lower bounds
on far fewer points than full mode.

## 5. Improved script

`/tmp/andreev_gap/verify_opus/min_circuit.py` (needs `common.py` from the same directory)

```
python3 -I min_circuit.py full 2,2                      # exact minimum, scans S=0,1,...
python3 -I min_circuit.py full 2,3 --only 3 --tl 3600 --portfolio 4   # UNSAT => min >= 4
python3 -I min_circuit.py blocksym 2,3 --only 4 --tl 3600 --show       # SAT => prints exact circuit
```
* Modes: `full`, `blocksym` (restriction; prints a warning), `thermo` (valid but weak sub-instance).
* Every SAT model is checked exactly on **all** inputs before it is reported; an error is raised
  otherwise. Every UNSAT is a proof (all constraints added are WLOG, as argued in the code comments
  and above).
* Output: `S=..: UNSAT (proved) | SAT (verified exactly ...) | UNKNOWN`, then
  `RESULT ...: minimum = s` / `lower bound >= L (proved)` / `S=s -> UNSAT => minimum >= s+1 (proved)`.
* Options: `--tl` (per S), `--total`, `--start/--upto/--only`, `--sym`, `--tactic`, `--portfolio`,
  `--seed`, and the experimental `--cuts --nonred --cegar --glex --jobs/--cube`.

Other files: `common.py` (points and exact checker), `cpsat_check.py`, `milp_check.py`,
`orig_models.py`, `fe_exact.py`, `bench_fair.sh`, logs (`fair/`, `bench/`, `*.log`).
