# Verification report: `z3_min.py`, `five_eighths.py`, `cpsat_min.py`

All work is in `/tmp/andreev_gap/verify/`. The originals were not modified.
Timings come from a shared 20-core host with load average about 13, so they are noisy. I report CPU seconds, and treat differences under about 1.5x as noise.

## 1. Verdict

**The minima and UNSAT answers reported by `z3_min.py` are trustworthy for the model it states.** I found no soundness or completeness bug in the current version.

- Every SAT model I extracted was re-verified on all inputs with exact `Fraction` arithmetic. All passed.
- Every minimum I could re-derive independently matched. Two independent encodings reproduced the original's UNSAT/SAT pattern, and a third (bounded-weight) check gave no contradiction.
- `five_eighths.py` constructions evaluate correctly on all inputs, which I checked exhaustively (below).

Caveats on what the results mean:

1. **`blocksym` results are not `full` results.** A blocksym circuit is a full circuit of the same size, so blocksym-SAT implies full-SAT and full-UNSAT implies blocksym-UNSAT. The converse fails in general. A blocksym UNSAT is a lower bound only for block-symmetric circuits. A symmetrization argument is not available for threshold circuits. In every instance where I computed both modes, the minima coincided: k=1 for m≤6, and (2,1), (2,2). That is evidence, not a proof.
2. **`cpsat_min.py` is not a lower-bound tool.** Its weights are bounded (|w|≤3), so its SAT answers are genuine upper bounds but its UNSAT answers prove nothing about real weights. Its output line says "minimum bottom gates", which overstates this.

## 2. Correctness analysis of `z3_min.py`

| Question | Finding |
|---|---|
| Margin-1 normalisation, bottom gate `g → α·p ≥ θ`, `¬g → α·p ≤ θ−1` | **Sound and complete (WLOG).** On a finite point set the gap between the positive values `α·p−θ ≥ 0` and the negative values `<0` is strictly positive after shifting θ down by a small ε. Scale by `1/(2c)`, where c is the minimal margin, and shift θ by `+1/2`. This gives positives `≥ 0` and negatives `≤ −1`. The argument uses only finiteness of the point set. It does not use integrality, so it is exact for the s-coordinates in `0..m`. The top gate has the same finite-set argument, with inputs `(g, p)`. I confirmed this empirically by re-encoding with strict inequalities and no normalisation (`xcheck_strict.py`), which agrees on every instance tried. |
| Input set, target `A`, both modes | **Correct.** Full mode enumerates all `2^N · 2^{km}` tuples, with `s_i` the sum of block i's bits and `b=Σ(s_i mod 2)2^i`. Blocksym enumerates `x × {0..m}^k`. The linear forms use `al[j][d]*p[d]`, so the s-weights are applied. My `common.inputs` builds the target from real bits, via the explicit unary realisation `1^{s_i}0^{m−s_i}`, and agrees. |
| "Minimum = first SAT S" | **Valid.** Feasibility is monotone in S: add a gate with top weight 0. Each smaller S was answered UNSAT by a complete decision procedure (QF_LRA over the rationals), not by timeout. UNKNOWN is handled: the loop stops and says "undecided". |
| Blocksym as a restriction of full | **Sound.** A gate depending on a block only through its weight is an LTF in `(x,s)`. Conversely, any LTF symmetric under within-block permutations equals the LTF with the block-averaged weights. So the blocksym model is exactly "all gates and the top are block-symmetric". |
| Two fixed bugs (s-weights not applied, result-handling crash) | Confirmed fixed. `z3_blocksym.log` still holds the old traceback, which is stale. |

Remaining findings (none affect the soundness of reported minima):

| # | Severity | Finding |
|---|---|---|
| 1 | Low (labelling) | The printed `ours 5/8` value is the number of gates in `five_eighths.build`, which includes the gate `[x_0≥1]`. In the stated model (top reads inputs directly) that gate is free. `cpsat_min.py` prints `ours-1`, `z3_min.py` does not, so the two scripts disagree by one. |
| 2 | Low | `for S in range(0,30)` prints nothing if all 30 values are UNSAT. A "no circuit up to S=29" message would be better. |
| 3 | Medium (usability) | The scan proves UNSAT for S=0..min−1 separately. By monotonicity, UNSAT at S=min−1 alone proves everything below it. With no symmetry breaking the proof at the largest S times out. For example, blocksym (2,3) at S=3 is UNKNOWN after 500 s in the original encoding. |
| 4 | Low–medium | `cpsat_min.py`: bounded weights make UNSAT meaningless as a lower bound (see the caveat above). The bound `tau ∈ ±V(S+D)` uses `D=N+k` and ignores that the s-coordinates reach m, so the top threshold range is slightly too narrow in principle. With `V=4(N+km)N` it is unlikely to bind. |
| 5 | Info | `five_eighths.py` `check()` samples 20000 random inputs when n>16, so (4,3) and (5,4) are only sampled. It is exhaustive for n≤16. Gate count is over-reported for k=1: at N=2 the coefficient `(M/2N−2)·Δφ` is 0, so some "gates" are inert. For (1,3) it reports 14 gates, of which 11 are non-trivial. This is conservative (still a valid upper bound). |

## 3. Cross-check results

Verification column: ✓ means the SAT circuit passed an exact-rational check on all inputs.

### 3.1 Minima (S = least number of bottom gates)

| Instance | Original `z3_min` | My strict-LRA encoding (`xcheck_strict.py`) | Dichotomy enumeration + LP (`xcheck_enum.py`) | `min_circuit.py` | Exact check |
|---|---|---|---|---|---|
| blocksym (1,1) | 1 | 1 | 1 | 1 | ✓ |
| blocksym (1,2) | 1 | 1 | 1 | 1 | ✓ |
| blocksym (1,3) | 2 | 2 | 2 | 2 | ✓ |
| blocksym (1,4) | 2 | 2 | 2 | 2 | ✓ |
| blocksym (1,5) | 3 | 3 | – | 3 | ✓ |
| blocksym (1,6) | 3 | 3 | – | 3 | ✓ |
| blocksym (1,8) | 4 | – | – | 4 | ✓ |
| blocksym (1,10) | – | – | – | 5 | ✓ |
| blocksym (1,12) | – | – | – | 6 | ✓ |
| blocksym (2,1) | 3 | 3 | – | 3 | ✓ |
| blocksym (2,2) | 3 | 3 | – | 3 | ✓ |
| full (1,1) | 1 | 1 | 1 | 1 | ✓ |
| full (1,2) | 1 | 1 | 1 | 1 | ✓ |
| full (1,3) | 2 | 2 | – | 2 | ✓ |
| full (1,4), (1,5) | 2, 3 | – | – | 2, 3 | ✓ |
| full (1,6) | – | – | – | 3 | ✓ |
| full (2,1) | 3 | – | – | 3 | ✓ |
| full (2,2) | 3 | – | – | 3 | ✓ |

For k=1 the minimum is ⌈m/2⌉ in every case computed. That is a sanity pattern and not a proof.

- The dichotomy enumeration involves no SMT and no big-M. It lists every threshold dichotomy of the input points by DFS with LP feasibility (52, 149, 318, 579 of them mod complement for blocksym (1,1)–(1,4)). For each S-subset it asks an LP whether a top gate separates the target.
- Soundness was also confirmed for the symmetry-broken version on every instance where the unbroken answer is known: blocksym (2,1), (2,2), (2,4) S=3, (2,5) S=3, and (2,3) S=3 with sym-only vs sym+sym2.
- Original-column values for full (1,4) and (1,5) are taken from the existing `z3_full.log`; all other original values were re-run by me through `orig_run.py` with exact model verification.

Lower-bound (UNSAT) frontier:

| Instance | Proven (all by `min_circuit.py`) |
|---|---|
| blocksym (2,3) | S=3 UNSAT → min ≥ 4; S=4 UNSAT (398 s CPU) → **min ≥ 5**; S=5 UNKNOWN at 1500 s |
| blocksym (2,4) | S=4 UNSAT (199 s CPU) → **min ≥ 5**; S=5 UNKNOWN at 1500 s |
| blocksym (2,5) | S=4 UNSAT (19.5 s CPU) → **min ≥ 5** |
| blocksym (2,6) | S=4 UNSAT (51.3 s CPU) → **min ≥ 5** |

I did not find upper bounds (SAT) for these at S=5; I did not search beyond S=5.

### 3.2 Other encodings

- **HiGHS big-M MILP** (`milp_bm.py`, integer weights |w|≤3): SAT at the right S for (1,1), (1,2), (1,3), with verified circuits. For (2,1) at S=1 it was UNKNOWN after 60 s, where z3 answers UNSAT in 0.1 s. So MILP is far worse than SMT here, and only a bounded-weight check anyway.
- **CP-SAT** (`cpsat_min.py` code, |w|≤3): (2,1) S=2 UNKNOWN after 100 s; (2,2) S=2 "UNSAT" (bounded weights) after 94.8 s; S=3 SAT in 1.5 s. Consistent with z3, but it proves nothing about real weights.

### 3.3 Checking `five_eighths.py`

Its `check()` really evaluates every gate (`(Z@W.T) >= T` then `@V + K`) and compares with the block-parity target. I re-checked independently in `check58.py`:

- Exact integer arithmetic.
- Exhaustive over all `(x,s)` with `s ∈ {0..m}^k`.
- An assertion that every gate is block-uniform, which makes this equal to an exhaustive check over all `N+km` input bits.
- A target recomputed from the real bits.

Result: **0 mismatches** on all of the following (each exhaustive):

| k | m values |
|---|---|
| 1 | (1,1), (1,3) |
| 2 | 1, 2, 3, 4 |
| 3 | 1, 2, 3, 4 |
| 4 | 1, 2 (up to 5.3M inputs) |

Gate counts equal `(N−1)(N+2)+3kmN/2+1` in every case. The constructions are therefore valid upper bounds, and the computed minima never exceed them: for example (2,1) min is 3 against 30 gates when the free x_0 gate is subtracted.

## 4. Efficiency findings

Setup: z3 5.3.3, one thread per run. Times are CPU seconds, taken from single instances on the loaded host, so each cell is one sample. "orig" is the `z3_min.py` encoding, re-implemented in `min_circuit.py --enc twosided --no-sym --no-sym2`. Its timing matched the real `z3_min.py` on (2,1) and (2,2).

| Instance (blocksym) | orig | + `--sym` | + `--sym2` (default of `min_circuit.py`) | Speedup orig → default |
|---|---|---|---|---|
| (2,1) S=2 UNSAT | 28.6 | 6.7 | **1.2** | ~24x |
| (2,2) S=2 UNSAT | 0.9 | 0.5 | 0.4 | ~2x |
| (2,3) S=3 UNSAT | not solved (>212 s, UNKNOWN at 500 s) | 55.9 | **2.8** | **>75x** |
| (2,4) S=3 UNSAT | 26.8 | 4.7 | 1.7 | ~16x |
| (2,5) S=3 UNSAT | 63.2 | 9.9 | 5.4 | ~12x |
| (2,6) S=3 UNSAT | – | – | 6.2 | – |
| (2,3) S=4 UNSAT | – | – | 398 | orig and `--sym` alone not measured; without sym2 still UNKNOWN after 638 s CPU (1500 s wall) |
| full (2,2) S=2 UNSAT (orig_run, wall) | 239 s | – | 1.8 | ~130x (wall vs CPU) |

Summary of what helps:

1. **Symmetry breaking on gates (`--sym`).** Complementing a gate maps `(α,θ,v) → (−α, 1−θ, −v)` and `τ → τ−v`, and gates can be permuted. So WLOG `0 ≤ v_0 ≤ … ≤ v_{S−1}`. This gave 2–5x on UNSAT proofs.
2. **Symmetry breaking on inputs (`--sym2`).** This uses the symmetries of Andreev's function and gave a further 2–20x:
   - Reflect `s_i → m−s_i`, together with `x_c → x_{c xor e_i}` when m is odd (parity flips). In full mode, flip one bit of block i with the same table permutation.
   - This flips the sign of the top weight on that coordinate, so WLOG all those top weights are ≥ 0.
   - Permuting blocks, or bits within a block, lets the top weights be sorted.
   - It needs the top gate to read inputs directly. It is disabled with `--no-top-direct`.
   - Combined, `--sym` and `--sym2` are 12–>75x faster than the original on the hard UNSAT cases.
3. **Lower bound needs only one call.** By monotonicity, UNSAT at S=L−1 proves "S<L impossible". The `--lb L` mode does exactly this.
4. **Incremental solving across S** (`--min --incr SMAX`: one solver with SMAX gate slots and assumptions that force `v_j=0` for disabled gates). This gave only about 1.3–1.7x on a full scan, for example total CPU 1.9 s vs 2.9 s on (2,2), and 3.3 s vs 5.0 s on (2,4). It needs SMAX ≥ the minimum. I kept it as an option; the default is fresh solvers.
5. **What did not help:**
   - *Lazy point generation (CEGAR)* is slower on UNSAT and left (2,3) S=3 UNKNOWN. Off by default (`--cegar`).
   - *One-sided encoding* (`--enc onesided`: half the implications, valid once v≥0) was never better than the two-sided one on a significant case, and 2x worse at (2,6). Default is two-sided.
   - *MILP/HiGHS and CP-SAT* are orders of magnitude slower than z3 on this problem (section 3.2).
6. **Not tried, but likely valuable:** a symmetry-breaking rule on the x-weights (the table-bit permutations are not yet used), a proof certificate for UNSAT, and a multi-process split of the search space.

Best speedup: **>75x** on blocksym (2,3) S=3 (not solvable by the original in 500 s; 2.8 s CPU here), and ~130x on full (2,2) S=2.

## 5. Recommended script: `/tmp/andreev_gap/verify/min_circuit.py`

Same model as `z3_min.py`. Defaults: z3 QF_LRA, `--sym` and `--sym2` on, no CEGAR, two-sided encoding. Every SAT model is re-verified on all inputs with exact rationals, and the exit code is 2 if that fails.

```
python3 -I min_circuit.py --k 2 --m 3 --S 3                  # decide one S
python3 -I min_circuit.py --k 2 --m 3 --lb 5 --tl 3600       # try to PROVE "S<5 impossible" (decides only S=4)
python3 -I min_circuit.py --k 2 --m 3 --min --tl 600         # ascending scan, first SAT = exact minimum
python3 -I min_circuit.py --k 2 --m 3 --min --incr 8 --show  # incremental scan + print the circuit
python3 -I min_circuit.py --mode full --k 2 --m 1 --min      # full mode instead of blocksym
```

Flags `--no-sym`, `--no-sym2`, `--cegar`, `--enc onesided`, `--no-top-direct` reproduce the older variants for comparison.

Output lines are `RESULT <mode> k m S SAT|UNSAT|UNKNOWN time cpu ... verified_exact=True`, followed by `PROVEN (...)`, `MINIMUM`, or `LOWER BOUND ... undecided`. `PROVEN` names the model (blocksym or full), so a blocksym proof is not mistaken for a full one.

Note: `--lb` applies to the model as run, including `--no-top-direct` if you pass it, which changes the model rather than just a speed option.

## 6. Files

- `common.py`: independent input enumeration, target `A`, and exact circuit verification.
- `orig_run.py`: runs the original encoding unchanged (source patched only to return the solver) and verifies models.
- `xcheck_strict.py`, `xcheck_enum.py`, `milp_bm.py`: the independent encodings.
- `check58.py`: exhaustive re-check of `five_eighths.py`.
- `mc_dev.py`: development copy; `min_circuit.py` is the final version.
- `bench*.sh`, `bench_*.out`: benchmark drivers and outputs.
