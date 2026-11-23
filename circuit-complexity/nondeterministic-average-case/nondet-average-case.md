# Average-case and one-sided frontier bounds for nondeterministic circuits

Status labels: **[proved here]** = full proof in this note; **[verified from source]** = checked in
the cited text, either the Lean sources in the local `cslib-frontier` clone or downloaded papers;
**[speculation]** = conjecture or heuristic.
I could not read the McGuire–Schlesinger–Williams PDF, so nothing here is attributed to it.

## 0. Summary

| # | Statement | Status |
|---|-----------|--------|
| L1 | For a nondeterministic circuit, agreement with `S` is `1/2 ± b + signedCount_S(A)/|U|^n`, where `A` is the accepted set. The complement of `A` is never needed. | proved here |
| T3 | **Multiplicity peeling.** Let `P` be any read-once NBP. Suppose every rectangle with both sides `≥ K` has `|R∩S| ≤ ρ|R∖S|`. Then `|A∩S| ≤ ρ·Σ_{y∈A∖S} M(y) + (K−1)²·size(P)`, where `M(y) ≤ min(#accepting paths of y, #states on accepting paths of y)`. With `M ≡ 1` (unambiguous) this is McGuire's peeling. | proved here; brute-force sanity check |
| T4 | **Circuits.** Take a nondeterministic circuit of fan-in 2 with `≤ (L−ε)n` gates. Then `Pr_x[x∈A∩S] ≤ ρ·E_x[1_{x∉S}·W(x)] + |U|^{−γn}`, where `W(x)` is the number of accepting witnesses of `x`. In particular: perfect soundness forces `|A| ≤ |U|^{(1−γ)n}`; circuits unambiguous on false positives have agreement `≤ 1/2 + O(b)`. | proved here (asymptotic bookkeeping mirrors the Lean proof) |
| T6 | **AM barrier.** Suppose the factor `M` in T3 could be replaced by `F(m)` with `F(m) ≤ exp((log m)^{1−γ})` (or by a constant), uniformly over programs with 2 coordinates and a large alphabet. Then the Chattopadhyay–Zuckerman extractor has `AM^cc ≥ n^{Ω(γ)}` (resp. `Ω(n)`). No explicit AM lower bound is known. | proved here, from verified sources |
| T7 | **Weighted counterexample (Q1 and Q2).** There are a partial function, a distribution `μ` and a union of `m = n^{O(log 1/ε)}` rectangles with `μ`-agreement `≥ 1−ε`, although every rectangle of `μ`-mass `≥ 2^{−Ω(n^{1/3})}` has relative bias `≤ 2^{−Ω(n^{1/3})}`. So small bias on large rectangles does **not** suffice in the weighted setting, and any valid overlap factor must be `≥ m^{Ω(1/log n)}`. | proved here from Klauck 2011 (verified from source) |
| Q1u | Uniform measure, side thresholds, all cuts, binary alphabet (the setting of `RectangleBias`): is small bias enough for nondeterministic circuits? | **open**. A positive proof through single-cut reasoning is AM-hard (T6). I expect the hypothesis-only statement to be false, but have no construction. [speculation] |
| P8 | Inner product and every `F₂`-quadratic polynomial have a monochromatic rectangle with both sides `≥ K` at some cut, for every `K ≤ 2^{(n−4)/3}`. So they satisfy neither the all-cut bias hypothesis nor the all-cut corruption hypothesis. | proved here |
| Q3 | The co-nondeterministic results are exactly the nondeterministic ones applied to `Sᶜ` and the rejecting witnesses (Section 6). | proved here |

## 1. Setting and notation

Inputs are `x ∈ U^ι` with `ι` finite (`|ι| = n`), `N := |U|^n`. A *cut* is `X ⊆ ι`. A *rectangle
for `X`* is `R = rect(X, A', B') = {x : x|_X ∈ A', x|_{Xᶜ} ∈ B'}`, with *sides* `|A'|`, `|B'|`
(Lean: `Cslib.Circuits.Frontier.rectangle`). A rectangle is *large* if both sides are `≥ K`.

Hypotheses on `S ⊆ U^ι` (all cuts, as in the Lean library):

* `Bias(K,b)` (Lean `RectangleBias S K b`): `| |R∩S| − |R|/2 | ≤ b|R|` for every large `R`.
* `Corr(K,ρ)` (new, one-sided): `|R∩S| ≤ ρ·|R∖S|` for every large `R`. Equivalently,
  `|R∖S| ≥ δ|R|` with `ρ = (1−δ)/δ`. `Bias(K,b)` implies `Corr(K, (1+2b)/(1−2b))`, and it also
  implies this for `Sᶜ`.
  `Corr(K,ρ)` with `ρ < ∞` says exactly that `S` is `K`-rectangle-free (Lean `RectangleFree`).
  An average over the `K`-subsets of both sides shows that it suffices to check `Corr` on rectangles
  whose sides have exactly `K` elements.
* Weighted versions, for a probability measure `μ` and a *mass* threshold `θ`:
  `ρ_θ(μ,S) := sup{ μ(R∩S)/μ(R∖S) : μ(R) ≥ θ }`.

`signedCount_S(T) = |T∩S| − |T∖S|` (Lean `signedCount`). The agreement of `S` with `T` is the fraction of inputs on which membership in `S` and in `T` agree (Lean
`agreement`).

**Read-once NBP** (Lean `ReadOnceNBP`). Layers `0..T`. Step `t` reads the coordinates
`X_{t+1}∖X_t`, with `∅ = X_0 ⊆ … ⊆ X_T = ι`. There is a start state and an accept state. `size` is the number of edges.
An *accepting path* of `x` is a state sequence `(γ_0,…,γ_T)` that follows edges labelled by `x`.
`A = acc(P)`. For a state `q` at layer `t`, let `Pre(t,q)` be the set of assignments to `X_t` that
reach `q`, and `Suf(t,q)` the set of assignments to `X_tᶜ` that lead from `q` to accept. Then
`R(t,q) := rect(X_t, Pre(t,q), Suf(t,q))` is the set of inputs with an accepting path through
`(t,q)`. It lies inside `A`, by concatenation (Lean `IsAcceptingPath.splice`) [verified from
source]. For each layer `t`, `A = ⋃_q R(t,q)`: this is a *cover*, not a partition. It is a partition
when `P` is unambiguous.

**Circuits.** For a circuit `C` with `n` ordinary and `k` witness inputs, the hidden network
(Lean `Compiler.hiddenNetwork`, `Network.hide`) accepts `A_C = {x : ∃w, C(x,w) ∈ Acc}`
(`accepted_hiddenNetwork`) [verified from source]. A layout of its graph gives an NBP
(`Network.branchingProgram`). Its size is at most `|V|·|U|^{w+4} + |U|^{#unread}` at width `w`
for fan-in 2 (`size_branchingProgram_le` with `d = 3`, `m = 1`) [verified from source].

**Lemma 0 (paths = witnesses)** [proved here; an informal reading of the Lean definitions].
Let `x` be an input. Its accepting paths in the NBP of the hidden network are in bijection with
`W(x) := {w|_reach : C(x,w) ∈ Acc}`, where `reach` is the set of witness inputs that reach the
output. In particular `#paths(x) ≤ #{w ∈ U^k : C(x,w) ∈ Acc}`.

*Proof.* There are three steps.
1. `satisfies_hide_iff` says that an edge assignment `α` satisfies the hidden network on `x` iff
   `α` satisfies the full network on `(x,w)` for some `w`.
2. `satisfies_unique` says that on the full network `α` is determined by `(x,w)`: it is the trace of
   the circuit, and it records `w_j` on the out-edge of each reachable witness input. So the
   satisfying `α` for `x` correspond bijectively to `w|_reach` with `C(x,w) ∈ Acc`.
3. Paths are the sequences of frontier values of satisfying assignments
   (`accepted_branchingProgram`). The map from assignments to paths is injective, because every
   edge of the loopless graph lies on the frontier between the positions of its two endpoints. ∎

## 2. Agreement needs only the accepted set

**Lemma 1** [proved here]. Let `T ⊆ U^ι` and let `S` satisfy `||S| − N/2| ≤ bN`. The whole cube is
a rectangle for any cut with both sides `≥ K`, so `Bias(K,b)` implies this whenever
`K ≤ |U|^{⌊n/2⌋}`. Then
`agreement(S,T) = (signedCount_S(T) + |Sᶜ|)/N ∈ [1/2 − b, 1/2 + b] + signedCount_S(T)/N`.

*Proof.* `N·agreement = |T∩S| + |Tᶜ∖S| = |T∩S| + |Sᶜ| − |T∖S|`. ∎

The Lean proof (`agreement_le`) bounds `T` and `Tᶜ` separately because both are deterministic
networks. For a nondeterministic circuit, `Tᶜ` has no rectangle structure, and by Lemma 1 it is not
needed. So the whole question is about **upper-bounding `signedCount_S(A)`** for an NBP-accepted
`A`. Applying the same bound to `Sᶜ` gives the matching lower bound.

## 3. One-sided: multiplicity peeling

For an NBP `P` and an input `y`, let `p_P(y)` be the number of accepting paths of `y` and
`st_P(y)` the number of states `(t,q)` with `0<t<T` that lie on some accepting path of `y`.

**Theorem 3 (multiplicity peeling)** [proved here]. Let `P` be a read-once NBP of length
`T ≥ 1` and let `S` satisfy `Corr(K,ρ)` for the cuts `X_1,…,X_{T−1}` of `P`. Then
```
|A ∩ S| ≤ ρ · Σ_{y ∈ A∖S} M(y) + (K−1)²·size(P),
```
where `M(y)` is the number of times the procedure below charges `y`. It satisfies
`M(y) ≤ min(p_P(y), st_P(y))`, and `st_P(y) ≤ Σ_{0<t<T} width_t`.

Consequently `|A∩S| ≤ ρ·M*·|A∖S| + (K−1)²·size(P)` with `M* = max_{y∈A∖S} min(p_P(y), st_P(y))`.

*Proof.* Induct on the number `Φ(P)` of pairs (accepted input, accepting path), which is finite.
Fix for each accepted `x` a chosen accepting path, for instance the least one in some order. This
defines the sweep of `P` (Lean `ReadOnceNBP.sweep`), the peer classes, and `pastSide`/`futureSide`.

*Case 1: no thick state.* For every `t` and every accepted `x`, the peers of `x` at time `t` have
fewer than `K` distinct parts on one side of the cut. This is Lean's `SmallSides K`, and
`ncard_accepted_le_of_smallSides` gives `|A| ≤ (K−1)²·size(P)` [verified from source]. Hence
`|A∩S| ≤ (K−1)²·size(P)`.

*Case 2: some state is thick.* There are `t` and `x` whose peer class at time `t` has `≥ K`
distinct prefixes and `≥ K` distinct suffixes. The peers' chosen paths pass through `q = γ_x(t)`,
so `Pre(t,q)` and `Suf(t,q)` have size `≥ K`, and `R := R(t,q)` is a large rectangle inside `A`.
Here `0 < t < T`, because at `t = 0` and `t = T` one side has a single element.

Delete `q` (Lean `eraseNode`) to get `P'`. Its accepting paths are those of `P` that avoid
`(t,q)` (`isAcceptingPath_eraseNode_iff`), and `size(P') ≤ size(P)`. Let `A' = acc(P')` and
`E = A ∖ A'`. Every input of `E` has all its accepting paths through `(t,q)`, so `E ⊆ R`. Then:

* `|E∩S| ≤ |R∩S| ≤ ρ|R∖S|`.
* For `y ∈ R`: `p_{P'}(y) ≤ p_P(y) − 1`, because at least one path of `y` goes through `(t,q)`.
  Also `st_{P'}(y) ≤ st_P(y) − 1`, because `(t,q)` is gone and no state is added.
* For `y ∉ R`, nothing changes.
* `Φ(P') < Φ(P)`, since `x`'s chosen path is destroyed.

By induction, `|A'∩S| ≤ ρ·Σ_{y∈A'∖S} M'(y) + (K−1)²·size(P')`. Define `M(y) = M'(y) + 1_{y∈R}`.
Then
`|A∩S| = |E∩S| + |A'∩S| ≤ ρ|R∖S| + ρ Σ_{y∈A'∖S} M'(y) + (K−1)² size(P) ≤ ρ Σ_{y∈A∖S} M(y) + (K−1)² size(P)`.

Each charge of `y` deletes a state on an accepting path of `y` and destroys at least one of its
paths. Neither can happen more than `st_P(y)` or `p_P(y)` times. ∎

**Remarks.**
1. **Unambiguous case.** If `P` is unambiguous then `M ≡ 1` and, with
   `ρ = (1+2b)/(1−2b)`, T3 gives `signedCount_S(A) ≤ (ρ−1)|A∖S| + res ≤ 4b|A|/(1−2b) + res`. This
   is Lean's `abs_signedCount_accepted_le` up to the constant (`2b` there).
2. **The overlap factor is not the number of transitions.** The factor is the number of accepting
   computations on false positives, `Σ_{y∈A∖S} p(y)`. The residual `(K−1)²·size` is unchanged. A
   plain charging argument without peeling gives the weaker factor `#{thick charged (t,q)}`.
3. **Only the program's cuts matter.** Only the cuts `X_t` of the program enter, but a circuit
   chooses its own layout, so the circuit theorem needs all cuts.
4. **Sanity check.** `checks/peel_check.py` brute-forces random NBPs with `n = 6`, width 4,
   `K = 4` and exact `ρ` over prefix cuts. It checks each peel step, the final inequality, the
   rectangle bound on the leftover program, and `M ≤ p`. All 56 non-vacuous instances pass
   (`peel_check_output.txt`). This only checks the bookkeeping.

**Corollary 3a (perfect soundness)** [proved here]. If `A ⊆ S` and `S` is `K`-rectangle-free,
then `|A| ≤ (K−1)²·size(P)`.

*Proof.* `A` is a subset of a rectangle-free set, hence rectangle-free (`RectangleFree.subset`),
and the rectangle bound (`ncard_accepted_le`) applies. This is T3 with `A∖S = ∅`. ∎

**Weighted single-cut form (Theorem 3′)** [proved here]. Let `A = ⋃_{i≤m} R_i` be a union of
rectangles for one cut, `μ` a measure, and `c(y) = #{i : y ∈ R_i}`. Then
`μ(A∩S) ≤ ρ_θ·∫_{A∖S} c dμ + mθ`.

*Proof.* Let `E_i = R_i ∖ ⋃_{j<i} R_j`. If `μ(R_i) ≥ θ`, then
`μ(E_i∩S) ≤ μ(R_i∩S) ≤ ρ_θ μ(R_i∖S)`. Otherwise `μ(E_i∩S) < θ`. Sum over `i` and use
`Σ_i μ(R_i∖S) = ∫_{A∖S} c dμ`. ∎

## 4. Consequences for nondeterministic circuits

Let `A > 0` satisfy the layout hypothesis `LayoutBound 3 A` and put `L = 1 + 1/A`. For the
Gaussian layout constant, `L ≈ 4.5625`
(`eventually_gaussian_sub_mul_lt_innerSize_of_nondeterministicDecides`) [verified from source].

**Theorem 4** [proved here; the asymptotic bookkeeping copies the Lean proofs
`agreement_le_of_unread`, `agreement_le_of_layout`, `exists_graph_of_nondeterministicDecides`
and `multiaryAverageCaseBound_of_layoutBound`. I re-derived it but did not formalize it.]

Fix `ε > 0` and put `γ := Aε/2`. Let `U` be finite with `|U| ≥ 2`, and let
`S_n ⊆ U^n` satisfy `Corr(K_n, ρ_n)` on all cuts, with `log K_n = o(n)`. Then for all large `n`,
the following holds for every fan-in-2 circuit `C` with `n` ordinary inputs, any number `k` of
witness inputs, any basis and acceptance set, and at most `(L−ε)n` inner gates:
```
|A_C ∩ S_n| ≤ ρ_n · Σ_{x ∈ A_C ∖ S_n} W(x) + |U|^{(1−γ)n},     W(x) = #{w ∈ U^k : C(x,w) ∈ Acc}.
```
In normalized form: `Pr_x[x ∈ A_C∩S] ≤ ρ·E_x[1_{x∉S}·W(x)] + |U|^{−γn}`.

*Proof.* There are two cases.
* **Many unread inputs** (they carry `≥ K` assignments). Then `A_C` depends only on the read
  coordinates `Rd`, so `A_C = A_{Rd} × U^D` with `D` the unread coordinates.
  - If `|A_C| ≥ |U|K²`, split `D = D_1 ⊔ D_2` with `K ≤ |U|^{|D_2|} < |U|K`. Then `A_C` is one
    rectangle for the cut `Rd ∪ D_1`, with sides `|A_{Rd}||U|^{|D_1|} ≥ K` and `|U|^{|D_2|} ≥ K`.
    So `|A_C∩S| ≤ ρ|A_C∖S| ≤ ρ Σ W`, since `W ≥ 1` on `A_C`.
  - Otherwise `|A_C| < |U|K² ≤ |U|^{(1−γ)n}`.
* **Few unread inputs.** Apply Theorem 3 to the NBP of a layout of the hidden network, and use
  `M ≤ p ≤ W` (Lemma 0). The residual is
  `(K−1)²(|V||U|^{w+4} + K) ≤ K³(|V|+1)|U|^{w+4}`, as in `agreement_le_of_layout`.
  - The graph is the circuit graph (`hiddenNetwork_toMultigraph`). At least
    `n − log_{|U|}K` ordinary inputs are read, so its cycle rank is
    `≤ s − n + log_{|U|}K + 1` (`exists_graph_of_nondeterministicDecides`). Only witness inputs
    reaching a gate matter, so `|V| ≤ 4s + 3` (`card_vertex_le`).
  - `LayoutBound 3 A` gives a layout of width
    `w ≤ (A+η)(s − n + log K + 1) + η|V| + C_η`. With `s ≤ (L−ε)n = (1 + 1/A − ε)n`, this is
    `≤ (1 − Aε + O(η))n + o(n)`.
  - Choosing `η` small, `K³(|V|+1)|U|^{w+4} ≤ |U|^{(1−Aε/2)n}` for large `n`. ∎

**Corollary 4a (one-sided error).**
* *Perfect soundness* (`A_C ⊆ S`). If `S_n` is merely `K_n`-rectangle-free, then
  `Pr_x[x ∈ A_C] ≤ |U|^{−γn}`. So a sub-`(L−ε)n` nondeterministic circuit with no false
  positives accepts an exponentially small fraction of inputs. This strengthens the Lean
  worst-case theorem, which only says such a circuit cannot decide `S`. [proved here]
* *Few false-positive witnesses.* If `Σ_{x∉S} W(x) ≤ τ·|U|^n`, then
  `Pr[A_C∩S] ≤ ρτ + |U|^{−γn}`. If false positives are counted without multiplicity, the
  guarantee requires `τ` roughly below `1/(ρ·max W)`. [proved here]

**Corollary 4b (two-sided, unambiguous on false positives)** [proved here]. Suppose `S_n`
satisfies `Bias(K_n, b_n)` and every false positive of `C` has exactly one accepting witness on
`reach`. Then
`agreement(S_n, A_C) ≤ 1/2 + b + 4b/(1−2b) + |U|^{−γn}`.
In general,
`agreement ≤ 1/2 + b + (ρ−1)Pr[A∖S] + ρ·E[1_{x∉S}(W(x)−1)] + |U|^{−γn}`, with `ρ = (1+2b)/(1−2b)`.

*Proof.* Lemma 1 and Theorem 4. ∎

## 5. Can the multiplicity factor be avoided? Two-sided bias? (Q1, Q2)

### 5.1 Single-cut instances are distributional NP protocols

Take `ι = {1,2}` and `U = {0,1}^{n'}` (`N₀ := 2^{n'}` values per coordinate). A union of `m`
rectangles `X_q × Y_q` is exactly the accepted set of a 3-layer NBP with `m` middle states and
`size ≤ 2mN₀`. An input's paths correspond to the rectangles containing it, so `p(y) = c(y)`.
The only nontrivial cut is `{1}|{2}`: the trivial cuts have a side of size 1. So
`Corr(K,ρ)`/`Bias(K,b)` for such `S` is the single-cut two-party condition. A union of `m`
rectangles is a cost-`log m` nondeterministic protocol.

**Lemma 5** [proved here; both parts are standard].
1. *Averaging.* If `AM_ε(f) ≤ c`, i.e. some distribution over NP protocols of cost `c` errs with
   probability `≤ ε` on every input, then for every `μ` some NP protocol of cost `c`, a union of
   `≤ 2^c` rectangles, has `μ`-error `≤ ε`. This is the easy half of Klauck 2003, Lemma 3,
   `AM_ε(f) = max_μ N^μ_ε(f)` [verified from source].
2. *Amplification.* `AM_ε(f) ≤ O(log(1/ε))·AM_{1/4}(f)`. Repeat `O(log 1/ε)` times and let Merlin
   certify a majority. For fixed coins, a majority of unions of rectangles is a union of
   intersections of rectangles.

### 5.2 The AM barrier

Let `E : {0,1}^{n'} × {0,1}^{n'} → {0,1}` be a `(k, 1/8)` two-source extractor. For all
`X', Y'` with `|X'|,|Y'| ≥ 2^k`, `|Pr_{X'×Y'}[E=1] − 1/2| ≤ 1/8`: sets of size `≥ 2^k` are flat
sources of min-entropy `≥ k`.
Chattopadhyay–Zuckerman give an explicit one with `k = log^{O(1)} n'`, computable in
`poly(n')` time [verified from source: the abstract and theorem statement as reported on the ECCC
and Annals pages]. Put `S = E^{-1}(1)` and `K = 2^k`. Then `Bias(K, 1/8)`, so `ρ ≤ 5/3`, and
`|S| ≥ (3/8)N₀²`.

**Theorem 6 (barrier)** [proved here]. Let `F : ℕ → ℝ_{≥1}` be nondecreasing. Suppose that for
every 2-coordinate NBP with `m` middle states and every `S` with `Corr(K,ρ)`:

  (H_F)  `|A∩S| ≤ ρ·F(m)·|A∖S| + (K−1)²·size(P)`.

Then for every `ε ≤ 1/8`:
`N^{unif}_ε(E) ≥ min{ n' − 2k − 4, log₂ F^{−1}(3/(40ε)) }`, where `F^{−1}(v) = min{m : F(m) ≥ v}`.
Hence:
* if `F ≤ C` is constant, then `AM_{1/4}(E) = Ω(n')`;
* if `F(m) ≤ exp((log m)^{1−γ})`, then `AM_{1/4}(E) ≥ n'^{Ω(γ)}`.

Both would be explicit superlogarithmic `AM^cc` lower bounds. Göös–Pitassi–Watson state that it
"even remains open to prove communication lower bounds against … AM … for any explicit function"
[verified from source].

*Proof.* Let `A` be a union of `m ≤ N₀/(16K²)` rectangles with uniform error `≤ εN₀²` against `S`.
Then `|A∖S| ≤ εN₀²` and `|A∩S| ≥ (3/8 − ε)N₀²`. Also `(K−1)²·size ≤ 2K²mN₀ ≤ N₀²/8`. (H_F) gives
`(1/4 − ε) ≤ (5/3)F(m)ε`, so `F(m) ≥ 3/(40ε)`. That proves the first claim.
* For constant `F`, take `ε < 3/(40C)`, so no `m` qualifies. Then
  `N^{unif}_ε(E) ≥ n' − 2k − 4`, and by Lemma 5, `AM_{1/4}(E) ≥ (n' − 2k − 4)/O(log 1/ε)`.
* For `F(m) ≤ exp((log m)^{1−γ})`, take `ln(1/ε) ≈ (n'/2)^{1−γ}`. Then
  `log m ≥ (ln(3/(40ε)))^{1/(1−γ)} ≈ n'/2` before (H_F) can hold, so
  `AM_{1/4}(E) ≥ Ω(n')/O(n'^{1−γ}) = Ω(n'^{γ})`. ∎

So T3's factor `M ≤ m` (giving only `N_ε ≥ log(1/ε)`, which is trivial) is essentially the best
that single-cut reasoning can be expected to prove. Two caveats:
* The barrier is for proofs that work at the generality of the abstract NBP lemma, which is how
  the Lean `ReadOnceNBP` lemmas are stated (any `ι`, `U`). It does not apply to arguments that use
  the fact that the program comes from a `(L−ε)n`-gate circuit.
* For a binary-alphabet version one would need an explicit `S ⊆ {0,1}^n` with small bias at *all*
  cuts and polylog `log K`. That is an extractor for two independent sources interleaved by an
  unknown partition. Chattopadhyay–Zuckerman (CCC 2016) handle high entropy. A search snippet of
  Chattopadhyay–Liao (arXiv 2110.12652) claims polylog-entropy interleaved extractors, but I did
  not verify that this covers unequal and arbitrary splits [speculation]. Given such an `S`, the
  embedding (read `x`, guess `q`, read `y`; size `O(m·2^{n/2})`) carries the barrier over to
  binary NBPs.

### 5.3 A genuine counterexample in the weighted setting (Q1 and Q2)

Klauck (2011) gives a partial function `f` with `AM(f) = O(log n)` and `PP(f) = Ω(n^{1/3})`
[verified from source]. He notes that because PP coincides with discrepancy, `f` has
polynomial-size, small-error rectangle covers under every distribution, "yet for some
distribution on the inputs every individual rectangle is either exponentially small, or has error
exponentially close to 1/2", so that "any attempt to prove lower bounds for AM-protocols by
considering the properties (error and size) of individual rectangles alone must fail"
[verified from source, intro of arXiv:1101.0523].

**Theorem 7** [proved here from the verified facts]. Let `μ` be that distribution, `S = f^{-1}(1)`
and `θ = 2^{−cn^{1/3}/2}`.
1. **Small bias does not suffice.** For every `ε ≥ 2^{−c' n^{1/3}/log n}` there is a union `A` of
   `m ≤ n^{O(log 1/ε)}` rectangles with `μ`-agreement `≥ 1−ε`. Every rectangle of `μ`-mass `≥ θ`
   has relative bias `≤ θ`. So "bias `b` on large rectangles ⇒ agreement `≤ 1/2 + O(b) + mθ`" fails
   for unions of rectangles in the weighted, mass-threshold setting.
2. **The overlap factor is needed.** Any `F` making `μ(A∩S) ≤ F(m)ρ_θ μ(A∖S) + mθ` valid on these
   instances has `F(m) ≥ m^{Ω(1/log n)}` (for `m ≤ 2^{Θ(n^{1/3})}`). Compare Theorem 3′, which has
   `F = max c ≤ m`.

*Proof.* `disc_μ(f) ≤ 2^{−cn^{1/3}} = θ²`. So for `μ(R) ≥ θ`,
`|μ(R∩S) − μ(R∖S)| ≤ θ² ≤ θμ(R)`, `ρ_θ ≤ (1+θ)/(1−θ)`, and `μ(S) = 1/2 ± θ²`.

By Lemma 5, `AM_ε(f) = O(log n · log 1/ε)`, which gives `A` with `μ(A Δ S) ≤ ε` and
`m = n^{O(log 1/ε)}`. Lemma 1, in weighted form, gives agreement `≥ 1 − ε`.

For part 2, `1/2 − θ² − ε ≤ F(m)(1+3θ)ε + mθ`. While `mθ ≤ 1/8` this forces
`F(m) ≥ 1/(8ε) = m^{Ω(1/log n)}`. ∎

**What this does *not* settle (Q1u).** Klauck's `μ` is non-uniform and not a product
distribution, `f` is partial, and the threshold is on mass. The Lean hypothesis `RectangleBias`
uses the uniform measure, *side* thresholds (bias must be small even on `K×K` rectangles of mass
`K²/N`) and all cuts. That hypothesis is much stronger and hereditary.

A heuristic: take a random union of rectangles with random multiplicity patterns and `S`
depending on the coverage multiplicity. The family of `K×K` grids inside it seems rich enough
(grids sharing `r` common rectangles have multiplicity `r + Poisson(λ)`) to force the acceptance
probability `g(c) ≡ 1/2`. So naive overlap constructions fail in the uniform-sides setting
[speculation].

I could neither construct a uniform-sides counterexample nor prove the positive statement. By
Theorem 6, proving the positive statement for explicit `S` by NBP reasoning would give AM lower
bounds. For *random* `S` the nondeterministic average-case bound is true but trivial: there are
`2^{O(m log nm)}` NBPs of size `m`, and Hoeffding with a union bound gives agreement
`≤ 1/2 + O(√(m log(nm)/2^n))` for all of them simultaneously [proved here]. Even more simply,
`2^{O(s log s)}` circuits of size `s` gives the same for circuits. So the content of any frontier
statement is about explicit or structured `S`.

## 6. Co-nondeterministic circuits (Q3)

Let `A'_C = {x : ∀w, C(x,w) ∈ Acc} = (B)ᶜ`, where `B = {x : ∃w, C(x,w) ∉ Acc}` is a
nondeterministic set (acceptance set `Accᶜ`). Since `agreement(S, A'_C) = agreement(Sᶜ, B)`,
every statement above transfers with `S ↔ Sᶜ`, accepting witnesses replaced by *refuting*
witnesses `W_rej(x) = #{w : C(x,w) ∉ Acc}`, and the hypothesis `Corr` on `Sᶜ`
(`|R∖S| ≤ ρ'|R∩S|` on large `R`) [proved here]:

* **One-sided (Theorem 4 for `B`, `Sᶜ`).**
  `#{x ∉ S : x ∉ A'_C} ≤ ρ'·#{(x,w) : x ∈ S, C(x,w) ∉ Acc} + |U|^{(1−γ)n}`.
  Correct rejections are bounded by the refutations of members of `S`.
* **Perfect completeness** (`S ⊆ A'_C`). If `Sᶜ` is `K`-rectangle-free, i.e. `S` meets every
  large rectangle, then `|U^n ∖ A'_C| ≤ |U|^{(1−γ)n}`. Such a co-nondeterministic circuit
  below `(L−ε)n` gates accepts almost every input, so it errs on almost all of `Sᶜ`.
* **Two-sided.** `Bias` is symmetric under `S ↔ Sᶜ`. A co-ND circuit that is unambiguous on
  false negatives (each `x ∈ S ∖ A'_C` has one refuting witness) has agreement `≤ 1/2 + O(b) + |U|^{−γn}`.
  In general the status is that of Section 5: open in the uniform setting, false in the weighted
  setting (apply Theorem 7 to `¬f`, which is also in AM, since Klauck's `f ∈ AM ∩ coAM` per
  Göös–Pitassi–Watson's summary; the complement statement is my reading).
* **Worst case.** Deciding `S` co-nondeterministically means deciding `Sᶜ` nondeterministically,
  so the Lean theorem gives `s > (L−ε)n` whenever `Sᶜ` is dense and rectangle-free
  (`DenseRectangleFree`).

## 7. Which explicit sets satisfy the hypotheses?

**Proposition 8** [proved here]. Let `f : F₂^n → F₂` be any polynomial of degree `≤ 2`, let
`K ≥ 2`, `k := ⌈log₂K⌉ + 1`, and `n ≥ 3k + 1`. Then at a cut `X` with `|X| = k` there is a
rectangle with both sides `≥ K` on which `f` is constant. For `IP(x,y) = Σ x_i y_i` there are
rectangles of *both* colors with sides `2^{n−1}` at a cut that splits the pairs `(x_i, y_i)`.

*Proof.* Write `f(p,q) = f₁(p) + f₂(q) + pᵀCq` for `p ∈ F₂^X` and `q ∈ F₂^{Xᶜ}`.
* The map `q ↦ (Cq, f₂(q))` takes `≤ 2^{k+1}` values. So some fiber
  `B' = {q : Cq = c₀, f₂(q) = e}` has size `≥ 2^{n−2k−1} ≥ K`.
* On `F₂^X × B'`, `f = g(p) + e` with `g(p) = f₁(p) + p·c₀`. One value of `g` is taken on
  `≥ 2^{k−1} ≥ K` points `A'`, and `f` is constant on `A' × B'`.
* For IP with `X = {x_i, y_i : i ≤ n/2}`, `IP = IP_L + IP_R`, and `{IP_L = a} × {IP_R = a'}` gives
  both colors. ∎

So inner product and quadratic forms violate `Bias(K,b)` for every `b < 1/2` and every
`K ≤ 2^{(n−4)/3}`, and one of `S`, `Sᶜ` violates `Corr`. They are usable only through
single-cut arguments such as the Lindsey/cut-rank argument in
`Frontier/Correlation/Rectangle.lean`, not through the all-cuts frontier hypotheses.

Other candidates:
* **Two-source extractors** satisfy the hypotheses at *one* cut (Section 5.2). That is enough for
  the large-alphabet 2-coordinate statements and for the barrier, but not for circuits.
* **Random sets** satisfy `Bias((n+1)³, 1/(n+1))` and dense rectangle-freeness at `K = n+2`
  (`exists_rectangleBias_family`, `exists_rectangleFree_family` in `Witness.lean`)
  [verified from source]. They are non-explicit, and for them counting already gives everything.
* **All-cut explicit sets with `log K = o(n)`** would have to be interleaved-source extractors
  (bias) or dispersers (rectangle-freeness, which suffices for Corollary 4a) for arbitrary splits.
  I could not verify such constructions or the paper's choice [speculation].

## 8. Literature

* H. Klauck, *Rectangle Size Bounds and Threshold Covers in Communication Complexity*, CCC 2003.
  https://arxiv.org/abs/cs/0208006
  - Lemma 3: `AM_ε = max_μ N^μ_ε`.
  - Theorem 1: `MA_ε ≥ Ω(√bound^{(1)}_ε)` and `AM_ε ≤ O(bound^{(1)}_ε + log 1/ε)`. So the
    one-sided rectangle bound sits between MA and AM.
  - Theorem 2 (WHICH): distributional NP with zero error vs deterministic distributional
    complexity.
  - Theorems 6–7 separate approximate-majority covers from one-sided bounds and from PP.
  - Fact 4: PP ≈ discrepancy. [verified from source]
* H. Klauck, *On Arthur Merlin Games in Communication Complexity*, CCC 2011.
  https://arxiv.org/abs/1101.0523
  - A partial function in AM (cost `O(log n)`) with PP `Ω(n^{1/3})`.
  - The "rectangle barrier" for AM lower bounds. [verified from source]
* M. Göös, T. Pitassi, T. Watson, *The Landscape of Communication Complexity Classes*, ICALP 2016
  / Comput. Complexity 2018. https://eccc.weizmann.ac.il/report/2015/049
  - Corruption ≡ SBP [GW14]; discrepancy ≡ PP [Kla07]; `SBP ⊆ AM`; `coNP ⊄ SBP`.
  - Explicit AM (even AM∩coAM) lower bounds are open. [verified from source]
* M. Göös, T. Watson, *Communication complexity of set-disjointness for all probabilities*
  (corruption characterizes SBP). https://eccc.weizmann.ac.il/report/2014/055
  [cited via GPW]
* A. Razborov, *On the distributional complexity of disjointness*, 1992 (corruption lemma)
  [cited via Klauck 2003, Fact 1].
* E. Chattopadhyay, D. Zuckerman, *Explicit two-source extractors and resilient functions*,
  Annals of Math. 2019. https://eccc.weizmann.ac.il/report/2015/119 [abstract verified]
* E. Chattopadhyay, D. Zuckerman, *New extractors for interleaved sources*, CCC 2016.
  https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2016.7 [abstract via search]
* E. Chattopadhyay, J.-J. Liao, *Extractors for sum of two sources*, https://arxiv.org/abs/2110.12652
  (interleaved-source application) [not verified].
* M. Göös, S. Lovett, R. Meka, T. Watson, D. Zuckerman, *Rectangles are nonnegative juntas*
  (SBP/WAPP characterizations), STOC 2015 [not fetched].

Lean sources used, all under `CslibFrontier/Computability/Circuit/Frontier/`:
* `Sweep.lean` (`ncard_le_mul_transitionCount`).
* `BranchingProgram.lean` (`ncard_accepted_le_of_smallSides`, `eraseNode`,
  `isAcceptingPath_eraseNode_iff`, `abs_signedCount_accepted_le`).
* `Network.lean`, `Projection.lean` (`hide`, `satisfies_hide_iff`), `Compiler/Network.lean`
  (`satisfies_unique`).
* `Nondeterministic.lean`, `AverageCase.lean`, `Rectangle.lean`, `Witness.lean`.

**Formalization note.** Theorem 3 is a small modification of
`ReadOnceNBP.abs_signedCount_accepted_le`. Induct on the number of accepting
`(input, path restricted to Fin (length+1))` pairs instead of `|accepted|`. Take `R` to be the
full rectangle of the deleted state rather than the peer class, and replace `RectangleBias` with
`Corr`. Lemma 0 needs injectivity of `frontierValues` on satisfying assignments.

## 9. Experiments

`checks/peel_check.py` (run with `python3 -I peel_check.py 60`) brute-forces Theorem 3's
bookkeeping on random small NBPs. Output is in `checks/peel_check_output.txt`: 56 non-vacuous
instances, all checks pass. At this size the residual dominates, so the experiment checks the
proof, not the asymptotics.
