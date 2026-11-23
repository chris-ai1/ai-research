---

## 4. Goal 1: searching for mixed-sign circuits that beat block-symmetric ones

### 4.1 What a winning circuit would need (all PROVED above)
- **Fixed $k$.** It must beat $\lfloor M/2\rfloor$-type parity bounds by a constant factor only (Cor. 1.5). For $k=2$ it needs at least $\mathrm{par}(2m+1)$ gates, which equals $m$ for $m\le$ PLACEHOLDER-K2. An $o(m)$ family would give sublinear depth-two parity circuits, which is open and contradicted by every exact value computed.
- **Balanced case.** Below $n^2/(24\log_2^3n)$ gates, a circuit must contain $\tilde\Omega(n^{3/2})$ non-coherent gates (Thm 3.2(2)). At $n^{2-\epsilon}$ gates these must be heavily mixed, with minority count $\tilde\Omega(n^\epsilon)$ (Thm 3.2(3)), and the circuit must use $\gtrsim\epsilon\log_2n$ sign patterns in some block (class (c)). Constructions built from a bounded number of "views" of a block, such as $s_i$ plus alternating sums, can win at most a constant factor.

### 4.2 Small sizes: methods
| method | script | outcome |
|---|---|---|
| z3 QF_LRA, full model, symmetry breaking ($v$ sorted $\ge0$; $u_{i,l}\ge0$ and sorted inside blocks, via single-bit flips + table permutation) | `andreev_min.py` | 10–20× faster than before on known cases: full (2,2) S=2 UNSAT in 1.6 s against 31–80 s with `verify_opus`. Proves full(2,3) $\ge4$ (§5). |
| sub-instances: table sets closed under $c\mapsto c\oplus e_i$, so the symmetry breaking stays valid and UNSAT transfers to $A$ | `andreev_min.py --tables` | 6 tables suffice to force 4 gates at (2,3) (177 s) |
| **table-CEGAR**: solve on a closed table set, add the orbit of a failing table, repeat (incremental z3) | `table_cegar.py` | PLACEHOLDER-TCG |
| point-CEGAR | `mscore.solve_cegar` | no gain on these instances (as found before in `verify_opus`) |
| smooth relaxation (sigmoid hidden units + skip connections, annealed to steps; truth tables then certified by exact LPs in z3 and `Fraction` re-check) | `nnsearch.py` | finds (2,2) S=3 in seconds; on (2,3) the best training error stayed at 44–133 of 1024 points for S=4..6. PLACEHOLDER-NN |
| coherent model (Boolean sign per gate and block) | `andreev_min.py --cls coherent` | PLACEHOLDER-COH |
| block-symmetric model on reduced points $(x,s)$ | `andreev_min.py --cls bsreduced` | PLACEHOLDER-BSR |

### 4.3 What the found circuits look like
- The 4-gate circuit for the 6-table sub-instance of (2,3) (`logs/sub23_S4_x1.log`) is heavily mixed. Its block-1 weights are, for example, $(-6,-7,22)$ and $(19,-22,-16)$.
- The 3-gate full (2,2) circuits found by the solver and by the relaxation are also mixed, e.g. block weights $(-7,7)$ and $(-10,19)$. But block-symmetric circuits reach 3 as well.
- Minimum **parity** circuits can contain genuinely mixed gates (§1.3) without saving anything.

Mixed signs are therefore *available* to optimal circuits, but in every instance decided so far they do not lower the gate count below the coherent/block-symmetric optimum (parity, $k=1$, (2,1), (2,2)).

## 5. Exact data (Goal 3)

All entries are exact SMT over the reals with the WLOG symmetry breaking proved in §1.3 and in the `andreev_min.py` docstring. "$\ge s$" means $S=s-1$ was refuted (UNSAT is a proof); "$=s$" also has a verified SAT circuit.
- *full*: arbitrary real weights.
- *coherent*: per-gate, per-block sign chosen by the solver.
- *b-sym*: block-symmetric.
- *addr W*: integer address weights in $[-W,W]$ with real table weights. This restricts only the address side, so it is weaker than bounding all bottom weights as `bigw/wmin.py` does; UNSAT here is therefore the stronger statement.

PLACEHOLDER-DATATABLE

## 6. What failed, and why

PLACEHOLDER-FAILED

## 7. Most promising next steps

PLACEHOLDER-NEXT

## 8. Files

| file | content |
|---|---|
| `report.md` | this report |
| `mscore.py` | encoder: point sets, gate classes, symmetry breaking, exact `Fraction` re-check of every SAT model, point-CEGAR |
| `parity_min.py`, `parity_min2.py` | exact parity minima; `parity_min2.py` adds the valid edge clauses of Prop. 1.4 |
| `parity_nosym.py` | cross-check of the parity UNSATs with weaker or no symmetry breaking |
| `parity_rigid.py` | minimum parity circuits containing a mixed gate |
| `halfslice.py` | half-slicing numbers hs$(M)$ |
| `andreev_min.py` | Andreev full / coherent / block-symmetric (`bsreduced`) / sub-instance (`--tables`) / bounded address weights (`--intaddr`) |
| `table_cegar.py` | CEGAR over table orbits |
| `nnsearch.py` | relaxation search plus exact certification |
| `random_features.py` | random-feature comparison of gate classes |
| `runs_lemma_check.py` | exact-integer check of Lemma 2.1 |
| `survival_mc2.py` | Monte Carlo for Lemmas 3.1 and 3.3 |
| `vo_min_circuit.py`, `common.py` | copies of `verify_opus/min_circuit.py` used for block-symmetric runs |
| `logs/` | every run quoted above (one line per result; SAT logs include the circuit when run with `--show`) |
| `mykill.sh` | kills only this directory's own python3/timeout processes |
