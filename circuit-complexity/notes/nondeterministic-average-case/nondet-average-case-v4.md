# One witness bit between 2.79n and 4.58n: partial progress

Continues [`nondet-average-case-v3.md`](nondet-average-case-v3.md), Section 6. Setting: `h(y,w)` has `n` inputs `y`, one witness
bit `w` and `s` fan-in-2 gates; `h_i = h(·,i)`; `S` has bias `b` on all rectangles with sides `≥ K`
at all cuts; `A_L ≈ 0.2796` is the layout constant and `L = 1 + 1/A_L ≈ 4.576`. The statement to
prove is that `{h_0 = h_1 = 1}` is split evenly by `S`. It is known for `s ≤ (1 + 1/(2A_L) − ε)n ≈
2.79n` and open up to `Ln`.

Status: **not settled.** Everything here is my own work in one session, unreviewed. Labels:
[proved here], [checked] (brute force), [experiment], [speculation].

## 1. The question is about a derivative of one circuit [proved here]

The two runs are the same circuit on two inputs that differ in one bit. So the open question is:

> Can `∂_1 T(y) = T(0,y) ⊕ T(1,y)` have small bias at all cuts, for a circuit `T` on `n+1`
> variables with fewer than `(L−ε)n` gates?

Write `v` for the value of a wire in run 0 and `d` for the XOR of its two values (its sensitivity
to `w`). The pair program carries `(v,d)` on every witness-dependent wire, and
`h_0 ⊕ h_1 = d_out`.

## 2. Theorem A: few nonlinear gates [proved here; span claim checked]

Call a gate *AND-type* if it is one of the eight gates `((u⊕a)∧(v⊕b))⊕c`, and *XOR-type* if it is
XOR or XNOR. Let `m` be the number of AND-type gates in the witness cone.

* Through an XOR-type gate, `d_out = d_1 ⊕ d_2`. Through an AND-type gate,
  `d_out = v_1 d_2 ⊕ v_2 d_1 ⊕ d_1 d_2`.
* So `d` on every cone wire is a fixed `F_2`-linear combination of the `d`'s of the `m` AND-type
  cone gates, plus a constant. On any set of `ω` cone wires the vector of `d`'s takes at most
  `2^{min(ω, m)}` values.
* The pair program, pruned to the states that occur, therefore has at most
  `2^{w_det + ω + min(ω, m) + O(1)}` states and transitions per step, instead of `2^{w_det + 2ω}`.

> **Theorem A.** For one witness bit, the two-sided bound `1/2 + O(b) + 2^{−γn}` holds whenever
> `A_L (s − n) + min(A_L (s − n), m) ≤ (1 − δ) n`.

With `m = μn`: the bound holds for `s ≤ (1 + (1−μ)(L−1) − ε) n`. That is the full `4.58n` for
`μ → 0`, `3.68n` for `μ = 1/4`, and the old `2.79n` for `μ ≥ 1/2`. Equivalently, a counterexample
with `s` gates needs at least `n − A_L(s−n)` AND-type gates in the witness cone.

`checks/v4/few_ands_check.py`: on 400 random circuits (2,292 cone wires) the linear form predicts `d`
exactly on every input, and no sampled set of wires exceeds the count.

The same argument refines Theorem P: with `k` witness bits a profile is one value plus `2^k − 1`
differences, each generated only at AND-type gates, so the cost of a cut is at most
`ω + (2^k − 1)·min(ω, m)`. [proved here, not checked separately]

Two smaller remarks. [proved here]
* Gates that read `w` directly become unary in each run, so they do not count towards `s`.
* The bound can be applied at the leaves of a decision tree on the inputs. Restricting inputs keeps
  the hypothesis on `S`. This gains nothing in general: fixing an input that feeds an XOR-type gate
  removes one gate, and progress against the `2.79n` line needs more than 2.79 gates per input.

## 3. Why the method stops here [proved here]

The pair program is two copies of the circuit laid out together. Any other layout of the doubled
graph is bounded only by its cycle rank `2s − n`, which gives `2.29n`. To beat `2.79n` in general
one has to show that the two runs cannot both use the full width, and for AND-type gates I found no
such constraint: `(v,d) = (y_2, y_1)` already arises on the wire `(w ∧ y_1) ⊕ y_2`.

## 4. Experiment: no sign that a derivative is richer than a circuit of the same size [experiment]

`checks/v4/derivative_search.py` (recorded output in `checks/v4/search_n12.txt`) searches, at a fixed number of gates, for a circuit whose output
("direct") or whose derivative in one input ("derivative") looks random at every sampled cut. The
measure is the largest singular value of the ±1 communication matrix divided by
`√rows + √cols`, maximised over cuts; it is about 1.0 for a random function. `n = 12`, 6,000 steps
of local search, 6 restarts, 42 search cuts, score reported on 36 fresh cuts. `x` is the number of
gates beyond the number of inputs.

| x | direct, best | derivative, best |
|---|---|---|
| 2 | 1.60 | 2.00 |
| 6 | 1.60 | 2.00 |
| 8 | 1.13 | 1.89 |
| 10 | 1.13 | 1.60 |
| 12 | 1.41 | 1.41 |
| 16 | 1.33 | 1.41 |
| 20 | 1.13 | 1.27 |
| 26 | 1.13 | 1.13 |
| 32 | 1.00 | 0.94 |

If the two runs behaved like one circuit with twice the wire capacity, a derivative with `x` extra
gates should match a direct circuit with about `2x`. The table shows the opposite: the derivative
needs at least as many gates as the direct circuit, and about three times as many to reach 1.13.

This is weak evidence. `n = 12` is far from the asymptotic regime, the measure rewards quadratic
forms (which a direct circuit gets with one AND per term, a derivative only from cubic terms), and
local search may simply be worse at derivatives. It does not support my earlier guess that the
answer to the question in Section 1 is yes.

## 5. Theorem H: only the entropy of the difference matters [proved here]

Notation as in Section 2. For an input `y` let `D(y) ∈ {0,1}^m` record, for every AND-type gate of
the witness cone, whether its output differs between the two runs. By Section 2, `D(y)` determines
`d` on every cone wire.

> **Theorem H.** Let `𝒟 ⊆ {0,1}^m` with `Pr_y[D(y) ∉ 𝒟] ≤ η`. If
> `A_L (s − n) + log₂|𝒟| ≤ (1 − δ) n`, then the circuit agrees with `S` on at most a
> `1/2 + O(b) + O(η) + 2^{−γn}` fraction of inputs.

*Proof.* Take the pair program along a layout of width `w_det + ω ≤ A_L(s−n) + o(n)` and add to
its state the part of `D` generated at the gates processed so far. The update is local: when a gate
is processed, the pair values on its edges are part of the state. Accept if both runs accept and
the final `D` lies in `𝒟`. The program is deterministic, hence unambiguous, and it accepts
`B' = {y : h_0 = h_1 = 1, D(y) ∈ 𝒟}`. Remove every state that no accepted input reaches. In a
remaining state, the run-0 values on the frontier take at most `2^{w_det+ω}` values, and the
differences on the frontier together with the recorded part of `D` are a function of `D(y) ∈ 𝒟`.
So each layer has at most `2^{w_det + ω}·|𝒟|` states, and `O(1)` times as many transitions. The
peeling bound for unambiguous read-once programs gives
`|excess(B')| ≤ 2b|B'| + poly(K)·n·2^{w_det+ω}|𝒟|`, and `|B ∖ B'| ≤ η 2^n`. The equivalences of v3
§6 turn this into the statement for the nondeterministic circuit. ∎

So a single run is charged its usual `A_L(s−n)` bits, and the second run is charged only the
(smooth max-) entropy `H_η` of the difference pattern. In these terms:

* the general `2.79n` bound is `H ≤ ω`;
* Theorem A is `H_0 ≤ m`;
* at size `s`, a counterexample needs `H_η ≥ n − A_L(s−n)`. Just below `Ln` this is a small multiple
  of `n`: with `s = (L−ε)n` the second run only has to supply `A_L ε n` bits.

## 6. Corollaries: what the witness bit must do [proved here]

Call a gate a *death* for `y` if one of its inputs differs between the two runs and its output does
not. The set `Δ(y)` of deaths determines the set of wires on which the runs differ (start at `w`
and propagate through every gate that is not a death), hence it determines `D(y)`. Let

* `ν = E_y |Δ(y)|`, the expected number of deaths;
* `τ_e = Pr_y[the runs differ on wire e]`;
* `κ = 1 + Σ_e τ_e (fan-out(e) − 1)`, the cycle rank weighted by the probability of a difference
  (the unweighted sum is `s − n`).

Counting uses of differing wires gives `|Δ(y)| ≤ 1 + Σ_{e differing} (fan-out(e) − 1)`, so
`ν ≤ κ`. By Markov, `|Δ(y)| ≤ cν` except with probability `1/c`, and there are at most
`C(s, ≤ cν)` such sets.

> **Corollary H1.** For every `c > 1`: if `A_L(s − n) + log₂ C(s, ≤ cν) ≤ (1−δ) n`, the agreement
> is at most `1/2 + O(b) + O(1/c) + 2^{−γn}`. The same holds with `κ` in place of `ν`.

Consequences, for every fixed ratio `s/n < L`:

* If the difference dies in `o(n)` places on average, the bound holds at the full constant `L`.
* If the witness-weighted cycle rank `κ` is `o(n)`, likewise. For instance, this holds when the
  wires that are re-used are rarely affected by the witness.
* A counterexample must have `ν = Ω(n)` and `κ = Ω(n)`: flipping the witness bit has to start a
  difference that is copied `Ω(n)` times by fan-out and killed at `Ω(n)` gates, on average over
  the inputs. The constants follow from `s·h(cν/s) ≥ n − A_L(s−n)`.

Why copying is unavoidable: along a path without fan-out the difference can die only once, so its
pattern carries `O(log n)` bits. Every further independent bit needs another copy of the
difference, and each copy uses one unit of the cycle rank at a wire where the runs differ.

## 7. A criterion that needs no layout [proved here]

Let `L` be a set of gates and inputs that is closed under predecessors and contains all inputs
except a set `Y` with `3 log₂ K ≤ |Y| ≤ δn`. The values on the edges leaving `L` are a function of
the inputs in `L`. If the pair vector on these edges takes at most `2^{(1−2δ)n}` values (counted as
in Theorem H), then the bound holds, whatever the size of the circuit. This is the information
bottleneck at a single cut: inputs in `L` with the same value on the cut are interchangeable.
It is independent of the sweep argument, and it is useless for circuits in which every gate depends
on almost every input.

## 8. Why I do not see a general improvement of 2.79 [assessment; the last item is speculation]

* Counting states cannot do better without a constraint on the difference pattern: per wire, a
  mixture of XOR-type and AND-type gates keeps both the value and the difference close to uniform.
* I found no gain from cutting the two runs at different times. The rectangle on which both
  states are constant then has the variables in between fixed, and its guaranteed sides are those
  of the earlier cut on the left and of the later cut on the right.
* Restricting inputs, re-laying out the doubled circuit, and prefix cuts were covered in
  Sections 2, 3 and 7.
* What remains is to show that `Ω(n)` copies and deaths cannot be arranged so that the difference
  pattern has `n − A_L(s−n)` bits of entropy *and* the circuit keeps cycle rank `s − n`. Each copy
  of the difference is a unit of cycle rank, and the layout bound already spends cycle rank on
  width. Whether the same unit can pay for both is the open point. [speculation]

## 9. Where this leaves the problem

* Proved: the bound for one witness bit up to `2.79n` in general; up to `Ln` whenever the entropy
  of the difference pattern is below `n − A_L(s−n)` (Theorem H), in particular with few AND-type
  gates in the cone (Theorem A), with `o(n)` expected deaths, or with `o(n)` witness-weighted
  cycle rank (Corollary H1).
* Open: circuits with `2.79n < s < Ln` in which the witness bit starts a difference that is copied
  and killed `Ω(n)` times.
