# Nondeterministic average case via the frontier method, v2: what can and cannot be removed

Status labels:
* **[proved here]**: complete proof in this note.
* **[verified from source]**: checked in the local `cslib-frontier` Lean sources (docstrings and statements) or in a paper.
* **[speculation]**: conjecture, heuristic or unverified literature claim.

This note continues [`nondet-average-case.md`](nondet-average-case.md) ("v1"). Results quoted from v1 are proved there. Numerical checks are in
[`checks/`](checks/) (Section 9).

## 0. Summary

**Target.** For every `ε>0` there is `γ>0` such that every nondeterministic (ND) fan-in-2 circuit with at most `(L−ε)n` gates
agrees with an explicit `S_n` on at most a `1/2 + O(b_n) + |U|^{−γn}` fraction of inputs.
**Status: not achieved.** The table lists what is proved and which barriers are precise.

| # | Statement | Status |
|---|---|---|
| C0 | Correction to v1, Lemma 0: accepting paths ↔ accepting restrictions of `w` to the **used** witness inputs (those with an out-edge), not those reaching the output. They agree when dead gates are pruned. | proved here + brute force (240 of 728 test inputs differ under the "reach" reading) |
| C1 | Witness-adjusted size. Every frontier statement for ND circuits holds with `s − k_u ≤ (L−ε)n` in place of `s ≤ (L−ε)n` (`k_u` = number of used witness inputs), provided `s ≤ c₀n`. | proved here from the Compiler cycle-rank count [verified from source] |
| P1 | v1's T4 main term `ρ·Σ_{x∉S} W(x)` is exactly the union bound over witnesses. The hidden-network proof only improves the residual. | proved here |
| P2 | Linear (witness-weighted) statements are free: `|E_x[(2·1_S−1)·Pr_w C(x,w)]| ≤ 4b + 2e^{−γn}`. | proved here from the Lean average-case theorem |
| L | Layer-cake lemma: bias on large rectangles controls correlation with every nonnegative product function. | proved here + brute force |
| WP | Weighted peeling for path counts of *any* read-once NBP: `|Σ(2·1_S−1)p_P| ≤ (2b+2β)Σp_P + D·(K'−1)²·size`, with `K' ≈ KD/β`. | proved here + brute force |
| **F** | **Bounded ambiguity.** At most `D` accepting witnesses per input and `s − k_u ≤ n + ((L−1)/D − ε)n` give agreement `≤ 1/2 + 2^{D+1}b + |U|^{−γn}`. Two-sided; it beats the union bound. | proved here |
| **F2** | Same, with degree `d = O(√D·log(1/δ))` in place of `D` (Chebyshev inclusion–exclusion). Agreement `≤ 1/2 + δ + O(15^d)·b + |U|^{−γn}`. | proved here + numerics for the polynomial |
| **W** | **Partial determinization.** If some layout has width `w` and *witness-width* `ω` (cone edges crossing a cut), an unambiguous NBP of width `|U|^{w−ω}·2^{|U|^ω}` accepts `A`. So `ω ≤ log_{|U|}(cn)` gives agreement `≤ 1/2 + 3b + |U|^{−γn}`. The one-sided factor `W(x)` improves to `T·|U|^{ω}`. | proved here + brute force on circuits |
| **M** | **Probability-gap ND (RP-type) circuits.** If `Pr_w[C(x,w)] ∈ {0} ∪ [α,1]` and `d(s+1) ≤ (L−ε)n` with `d = ⌈ln(2/δ)/(2 artanh√α)⌉`, then agreement `≤ 1/2 + b + δ + 3·15^d(4b + 2e^{−γn})`. This is quadratically better in `α` than OR-ing random witnesses. | proved here + numerics |
| D | **Exact reformulation (LP duality).** The hypothesis-only target for a set `A` is equivalent, up to rounding, to `1_A ≈ Σ c_R 1_R` over large rectangles with `Σ|c_R||R| = O(N)`. This property does not involve `S`. Special case N: if `A`'s complement is nearly partitioned into large rectangles, agreement is `≤ 1/2 + 5b + e`. | proved here |
| B1 | Coordinator's observation: a bias-only lemma for NBPs of width `|U|^{(1/2+θ)n}` at the balanced cut gives an explicit `AM^cc ≥ Ω(θn)`. | verified, proved here |
| B2 | Narrow NBPs (width `|U|^{θn}`, which covers witness-heavy circuits) simulate unions of `|U|^{θn/2}` boxes with `2/θ` blocks. So width-only proofs also yield NIH-multiparty NP lower bounds. | proved here; openness is speculation |
| B3 | **A circuit-level barrier.** If the ND target held uniformly in the alphabet (as Lean states its deterministic bound), then circuits with `2n₀−1` gates give unions of `|U|` arbitrary boxes. So it would imply explicit `n₀`-party NIH distributional NP lower bounds for Li's sumset extractor. | proved here; openness is speculation |
| B4 | Moment, inclusion–exclusion and hashing methods. Valiant–Vazirani isolation reduces to linear statements (P2). Moment methods need degree `≳ √(dynamic range of W)`, and the frontier budget allows a tensor degree of at most about `L/(1 + (s−n−k_u)/n)`. | proved here (approximate-degree lower bound cited) |

## 1. Setting

Inputs are `x ∈ U^n`, `N = |U|^n`. A rectangle at cut `X ⊆ [n]` is `{x : x_X ∈ P, x_{X^c} ∈ Q}`. It is *large* if
`|P|,|Q| ≥ K`.

* `Bias(K,b)` (Lean `RectangleBias`): `||R∩S| − |R|/2| ≤ b|R|` on all large rectangles at all cuts, i.e.
  `|Σ_{x∈R}(2·1_S(x)−1)| ≤ 2b|R|`.
* `signedCount_S(T) = |T∩S| − |T∖S|`.
* v1, Lemma 1: `agreement(S,T) = (signedCount_S(T) + |S^c|)/N ∈ 1/2 ± b + signedCount_S(T)/N`.

An ND circuit `C(x,w)` has `n` ordinary inputs, `k` witness inputs, `s` gates of fan-in ≤ 2 over any basis on `U`, and an
acceptance set `Acc`. Its accepted set is `A = {x : ∃w C(x,w) ∈ Acc}`. A witness input is *used* if it has an out-edge;
`k_u` is the number of used ones. Let `p(x) = #{w|_used : C(x,w) ∈ Acc}` and `D = max_x p(x)`.

The *hidden network* (Lean `Compiler.hiddenNetwork`) lives on the circuit graph `G`. A layout `π` of `G` gives a read-once NBP
`P_π` (Lean `Network.branchingProgram`) [verified from source].
* The layer-`t` state is an assignment to the frontier edges `F_t`.
* Step `t` processes vertex `π(t)`. It reads `x_i` if that vertex is input `i`, guesses values on the newly opened edges, and
  checks the vertex constraint.

The *witness cone* `Z` is the set of edges whose source is a witness input or a gate reachable from one. The witness-width of
`π` is `ω(π) = max_t |F_t ∩ Z|`.

`A_L>0` denotes the layout constant (`LayoutBound 3 A_L`; Gaussian value, `L = 1 + 1/A_L ≈ 4.5625`). Lean statement:
`∀η ∃C_η`, every connected loopless max-degree-3 graph has a layout of width `≤ (A_L+η)·cycleRank + η|V| + C_η`
[verified from source, `Multigraph.lean:463`].

## 2. Verified and corrected facts

**C0 (Lemma 0, corrected)** [proved here; brute force]. The accepting paths of `x` in `P_π` are in bijection with
`{w|_used : C(x,w) ∈ Acc}`.

*Proof.* Accepting paths correspond to satisfying assignments of the hidden network on `x`. Each one is the trace of
`C(x,w)` for some `w` with `C(x,w) ∈ Acc`, and the trace is unique (`satisfies_unique`, `satisfies_hide_iff`). The trace
records `w_j` on the out-edges of every used witness, and nothing about unused ones. Every edge lies in some frontier, so
distinct assignments give distinct paths. ∎

If a used witness feeds only dead gates (gates not reaching the output), its value still changes the trace. So v1's
"reaching the output" reading is wrong unless dead gates are pruned first; pruning never changes `A`. The inequality
`p(x) ≤ #{w : C(x,w) ∈ Acc}` used in v1 is unaffected. `checks/reach_vs_used.py` finds 240 of 728 test inputs where the "reach"
count differs from the path count, and `checks/circuit_check.py` confirms the "used" count on 1064 inputs.

**C1 (cycle rank with witnesses)** [verified from source + proved here].
* `Compiler.lean` (docstring and `cycleRank_add_ncard_read_le`) proves `cycleRank(graph c) + |read| ≤ (r−1)s + 1` for the
  network of the full circuit. Here `read` counts all reachable inputs, ordinary and witness.
* The hidden network has the *same* graph (`hiddenNetwork_toMultigraph`).
* Hence at fan-in 2, `cr(G) ≤ s + 1 − n_r − k_u`. The Lean nondeterministic reduction (`exists_graph_of_nondeterministicDecides`)
  uses only the weaker `cr ≤ s − n + log_{|U|}K + 1`.

Brute force confirms `cr = s + 1 − |used inputs|` on all 51 connected random circuits tested.

Consequently every frontier bound in v1 and below holds for `s − k_u ≤ (L−ε)n`, as long as `s ≤ c₀n`. The bound on `s` is
needed because the layout bound has an additive `η|V|` with `|V| ≤ 4s+3`, and `η` must be chosen after `c₀`.

**Coordinator's AM observation** is verified as B1 in Section 6.

## 3. What v1's Theorem 4 really is

**Proposition P1 (T4 is the union bound)** [proved here]. For each `w`, `A_w = {x : C(x,w) ∈ Acc}` is decided by a
deterministic circuit with at most `s` gates, obtained by substituting constants. v1's T3 with `M ≡ 1` (unambiguous programs)
gives `|A_w∩S| ≤ ρ|A_w∖S| + res_w`. Summing over `w ∈ U^{used}`:
* `Σ_w |A_w∩S| ≥ |A∩S|`;
* `Σ_w |A_w∖S| = Σ_{x∉S} p(x)`.

So `|A∩S| ≤ ρ·Σ_{x∉S} p(x) + |U|^{k_u}·max_w res_w`, which is v1's main term exactly. The hidden-network proof gives the residual
`|U|^{A_L(s+1−n−k_u)+o(n)}` without the factor `|U|^{k_u}`. For `k_u ≥ A_Lεn/(1−A_L)`, the union-bound residual can exceed `N`.

*Moral.* Any genuinely nondeterministic theorem must beat the union bound in the main term.

**Proposition P2 (linear statements are free)** [proved here, from Lean `AverageCaseBound`, whose `γ` is uniform over
circuits with `≤ (L−ε)n` gates; verified from source, docstring of `AverageCase.lean`].
1. For a deterministic circuit `T` with `≤ (L−ε)n` gates, both `T` and its complement (flip `Acc`) obey
   `agreement ≤ 1/2 + b + e^{−γn}`. By Lemma 1, `|signedCount_S(T)|/N ≤ 4b + e^{−γn}`.
2. Fix witnesses `w_1..w_j`. The circuit `∧_i C(·,w_i)` has `≤ j(s+1)` gates. Averaging over uniform `w_i` gives
   `|E_x[(2·1_S−1)·p̄(x)^j]| ≤ 4b + e^{−γn}` whenever `j(s+1) ≤ (L−ε)n`, where `p̄(x) = Pr_w[C(x,w) ∈ Acc]`.

So randomized, SBP- and "counting"-type circuits get small advantage for free. Only the OR (the threshold at `p ≥ 1`, with no
gap) is hard.

## 4. Positive results

### 4.1 Two lemmas for read-once NBPs

**Lemma L (layer cake)** [proved here; 200 random brute-force instances]. Fix a cut `X`. Suppose every rectangle at `X` with
both sides `≥ K` has `|Σ_R(2·1_S−1)| ≤ 2b|R|`. Then for all `f : U^X → ℝ_{≥0}` and `g : U^{X^c} → ℝ_{≥0}`,
```
|Σ_x (2·1_S(x)−1) f(x_X) g(x_{X^c})| ≤ 2b‖f‖₁‖g‖₁ + (K−1)(max f·‖g‖₁ + ‖f‖₁·max g).
```
*Proof.* Write `f(a)g(b) = ∫₀^∞∫₀^∞ 1[f(a)>τ]·1[g(b)>σ] dτ dσ`. The sum becomes `∫∫ Σ_{R_{τσ}}(2·1_S−1)`, with
`R_{τσ} = {f>τ}×{g>σ}`.
* If both sides of `R_{τσ}` are `≥ K`, its integrand is `≤ 2b|R_{τσ}|`. Integrating gives `≤ 2b‖f‖₁‖g‖₁`.
* Otherwise the integrand is `≤ |R_{τσ}|`. The `τ` with `|{f>τ}| < K` are those `τ ≥ f_{(K)}` (the `K`-th largest value),
  and `∫_{f_{(K)}}^{∞} |{f>τ}| dτ = Σ_a (f(a) − f_{(K)})_+ ≤ (K−1)·max f`. Multiply by `∫|{g>σ}|dσ = ‖g‖₁`. The case of `g` is
  symmetric. ∎

**Lemma WP (weighted peeling)** [proved here; brute force: 25 non-vacuous instances (2 at `K=4`, 23 at `K=2`), each peel and
the final bound checked].

*Statement.* Let `P` be a read-once NBP of length `T ≥ 1`, with path count `p_P(x)` and `D = max_x p_P(x)`. Let `S` satisfy
`Bias(K,b)` (`K ≥ 2`) at the cuts `X_1..X_{T−1}` of `P`, and let `β ∈ (0,1]`. Then
```
|Σ_x (2·1_S(x)−1)·p_P(x)| ≤ (2b+2β)·Σ_x p_P(x) + D·(K'−1)²·size(P),    K' = ⌊(K−1)D/β⌋ + 1.
```

*Definitions.* For a state `(t,q)`:
* `pre_q(a)` is the number of start→`(t,q)` paths on the prefix `a`;
* `suf_q(b)` is the number of `(t,q)`→accept paths on the suffix `b`;
* `φ_q(x) = pre_q(x_{X_t})·suf_q(x_{X_t^c})` is the number of accepting paths of `x` through `(t,q)`;
* `q` is *useful* if `φ_q ≢ 0`, and *thick* if it is useful, `0<t<T`, `(K−1)max pre_q ≤ β‖pre_q‖₁` and
  `(K−1)max suf_q ≤ β‖suf_q‖₁`.

*Proof.* Induct on the number of states.
* **Thick state exists.** Erase it (Lean `eraseNode`). A path meets layer `t` once, so `p_{P'} = p_P − φ_q`, with
  `size(P') ≤ size(P)` and `D' ≤ D`. Lemma L with `‖φ_q‖₁ = ‖pre_q‖₁‖suf_q‖₁` gives
  `|Σ(2·1_S−1)φ_q| ≤ (2b+2β)‖φ_q‖₁`. Over all peels, `Σ‖φ‖₁ ≤ Σ p_P`.
* **No thick state.**
  - For a useful `q` and any `b` with `suf_q(b) ≥ 1`, `pre_q(a) ≤ p_P(a,b) ≤ D`. So `max pre_q ≤ D`, and similarly
    `max suf_q ≤ D`.
  - Non-thickness then gives `|supp pre_q| ≤ ‖pre_q‖₁ < (K−1)D/β` or the same for `suf_q`. Layers `0` and `T` have a
    singleton side.
  - The past and future sides of the chosen-path sweep at `(t,q)` lie in `supp pre_q` and `supp suf_q`. So `P` satisfies
    `SmallSides K'`, and Lean `ncard_accepted_le_of_smallSides` gives `|acc(P)| ≤ (K'−1)²·size(P)`.
  - Hence `|Σ(2·1_S−1)p_P| ≤ Σp_P ≤ D·|acc(P)|`. ∎

**Product programs** [proved here; brute force for `j ≤ 3`]. Fix an order on each layer's states and compare paths
lexicographically.
* The *ordered `j`-fold power* `P^{(j)}` has states `(q_1,…,q_j; f_1,…,f_{j−1})`. Here `f_i = 0` means paths `i` and `i+1`
  have not yet diverged, which forces `q_i = q_{i+1}`.
* Its edges are `j`-tuples of `P`-edges with a common label. When a pair first diverges it must step to `q'_i < q'_{i+1}`,
  and the corresponding `f'_i` becomes `1`. The accept state has all flags `1`.
* It is read-once on the same layers, accepting paths of `x` ↔ `j`-subsets of accepting paths of `x`, so
  `p_{P^{(j)}} = binom(p_P, j)`.
* `width ≤ 2^{j−1}W^j` and `size ≤ 2^{j−1}·size(P)^j`.

### 4.2 Theorem F (bounded ambiguity)

**Theorem F** [proved here]. Fix `ε>0`, `c₀`, `D ≥ 1`. Let `S_n` satisfy `Bias(K_n,b_n)` on all cuts, with `log K_n = o(n)`.
There is `γ>0` such that for all large `n` the following holds. Let `C` be any ND fan-in-2 circuit with
* `s ≤ c₀n` gates,
* `p(x) ≤ D` for all `x`,
* `s − k_u ≤ n + ((L−1)/D − ε)n`.

Then
```
|signedCount_S(A_C)| ≤ (2b + 2|U|^{−γn})(2^D−1)|A_C| + |U|^{(1−γ)n},
agreement(S_n, A_C) ≤ 1/2 + 2^{D+1}b_n + 2^{D+1}|U|^{−γn}.
```
The matching lower bound follows by applying the same to `S^c`.

*Proof.*
1. **Many unread inputs** (`≥ log_{|U|}K` ordinary ones). `A = A'×U^{D'}` is a cylinder. Split `D' = D_1 ⊔ D_2` with
   `K ≤ |U|^{|D_2|} < |U|K`. Then `A` is one rectangle at the cut `Rd∪D_1`, and so is `A^c`. Each is either large or has
   `< |U|K²` elements, so `|signedCount(A)| ≤ 2b|A| + |U|K²`. This is the argument of Lean's `agreement_le_of_unread`, which
   uses only the cylinder structure.
2. **Few unread inputs.** Take the `LayoutBound` layout. Using C1, `w ≤ (A_L+η)(s+1−n−k_u+log_{|U|}K) + η(4s+3) + C_η`,
   and `size(P) ≤ |V||U|^{w+4} + K` (Lean `size_branchingProgram_le`).
3. **Inclusion–exclusion.** Since `0 ≤ p ≤ D`, `1[p ≥ 1] = Σ_{j=1}^{D}(−1)^{j+1}binom(p,j)`. Hence
   `signedCount(A) = Σ_j (−1)^{j+1} Σ_x (2·1_S−1)·binom(p(x),j)`.
4. **Apply WP to each `P^{(j)}`**, with max path count `binom(D,j)` and `β = |U|^{−γn}`. The cuts of `P^{(j)}` are those of `P`.
   Since `Σ_j binom(p,j) ≤ 2^D − 1` on `A` and `= 0` off `A`, the main terms sum to `(2b+2β)(2^D−1)|A|`.
5. **Residual.** It is `≤ C_D·(K/β)²·size(P)^D`. Its `log_{|U|}` is
   `D·A_L(s−n−k_u) + O(Dη c₀ n) + O(D(log K + C_η + log n)) + 2γn ≤ (1 − A_L Dε + O(Dηc₀) + 2γ)n + o(n)`.
   Take `η` small in terms of `(D, c₀, ε)` and `γ = A_L Dε/8`.
6. Lemma 1 finishes. ∎

*Comments.*
* `D=1` (unambiguous circuits) allows `s ≤ (L−ε)n + k_u`.
* `D=2` allows `s − k_u ≤ (1 + 1.78 − ε)n`.
* The union bound gives only the one-sided `|A∩S| ≤ ρD|A∖S|`.

**Refinement (witness sharing)** [proved here]. Every accepting path of `x` carries the same values on non-cone frontier edges
(those values are functions of `x`). Restrict `P^{(j)}` to tuples with equal non-cone parts. This keeps every accepting tuple
and gives width `≤ 2^{j−1}|U|^{w−ω+jω}`. So the condition `D·w ≲ (1−γ)n` in F relaxes to `w + (D−1)ω ≲ (1−γ)n`.

**Theorem F2 (approximate inclusion–exclusion)** [proved here; the polynomial is checked numerically].

*Statement.* Same hypotheses as F, with `D ≥ 2`, but with `d := ⌈ln(2/δ)/(2·artanh(D^{−1/2}))⌉ ≤ ⌈(√D/2)·ln(2/δ)⌉` in place of
`D` in the size condition. Then
```
agreement ≤ 1/2 + b + δ + (1 + 2·15^d)(2b + 2|U|^{−γn}) + |U|^{−γn}.
```

*Proof.*
1. **The polynomial.** Let `α = 1/D`, `a = (1+α)/(1−α)`, `c = 2/(1−α)`, and `q(t) = 1 − T_d(a−ct)/T_d(a)`, with `T_d` the
   Chebyshev polynomial.
   - `q(0) = 0`.
   - On `[α,1]` the argument of `T_d` lies in `[−1,1]`, so `|q−1| ≤ 1/T_d(a)`.
   - `arccosh a = 2 artanh √α`, so `1/T_d(a) ≤ 2e^{−2d·artanh√α} ≤ δ`.
   - Expanding, `Σ_i |q_i| ≤ 1 + 2((r+√(r²+1))/(a+√(a²−1)))^d ≤ 1 + 2·15^d`, with `r = a + c ≤ 7` for `α ≤ 1/2`.
2. **Binomial basis.** Put `r(p) = q(p/D) = Σ_{j=1}^{d} c_j binom(p,j)`. Since `p^i = Σ_j S(i,j)·j!·binom(p,j)` with Stirling
   numbers `S(i,j) ≥ 0`, and `Σ_j S(i,j) j! binom(D,j) = D^i`, we get
   `B := Σ_j |c_j| binom(D,j) ≤ Σ_i |q_i| ≤ 1 + 2·15^d`.
3. **Error.** `1_A − r(p)` vanishes off `A` and is `≤ δ` on `A`. Apply WP to `P^{(j)}` for `j ≤ d`:
   `|signedCount(A)| ≤ δ|A| + (2b+2β)·B·|A| + B·Σ_{j≤d} res_j`. The residual analysis is that of F with `d` in place of `D`. ∎

Numerics (`checks/binom_output.txt`): `B^{1/d}` stays between 3.0 and 5.4 for `D ≤ 1024`, consistent with the bound 15.

### 4.3 Theorem W (partial determinization by witness-width)

**Theorem W (program level)** [proved here; brute force on 60 random circuits].

*Construction.* Let `P = P_π` and split each state as `α_t = (d_t, u_t)`, with `d_t` on `F_t∖Z` and `u_t` on `F_t∩Z`. Define
`P'` with:
* states `(d, G)`, where `G ⊆ U^{F_t∩Z}` is nonempty;
* start and accept states `((),{()})`;
* an edge `(d,G) →_σ (d',G')` iff `G' = {u' : ∃u∈G, (d,u)→_σ(d',u') in P} ≠ ∅`.

*Claims.*
1. `P'` is a read-once NBP on the layers of `P`.
2. `acc(P') = acc(P)`.
3. `P'` is unambiguous.
4. `width_t(P') ≤ |U|^{|F_t∖Z|}(2^{|U|^{|F_t∩Z|}} − 1)` and `size(P') ≤ |U|^4·Σ_t width_t(P')`.

*Proof.*
* **2, (⊆).** Along an accepting `P'`-path, every `u ∈ G_t` is reachable in `P` through states with first parts
  `d_0..d_t` (induction on `t`). Since `() ∈ G_T`, `P` accepts.
* **2, (⊇).** Along an accepting `P`-path, `u_t ∈ G_t` by induction, where `G` is the forward image along the `d_t`.
* **3.** An accepting `P'`-path yields an accepting `P`-path with the same `d`-sequence. Every accepting `P`-path of `x` has as
  its `d`-sequence the trace values of non-cone edges, which depend on `x` alone (C0). So the `d`-sequence is unique, and it
  determines the `G`'s.
* **4.** The width bound is a count. For the size: given `σ` and `d'`, the successor is unique, and a step opens at most 3
  edges and reads at most one symbol. ∎

Then Lean's `abs_signedCount_accepted_le` (unambiguous programs) gives `|signedCount_S(A)| ≤ 2b|A| + (K−1)²size(P')`.

**Corollary W1 (circuits)** [proved here]. Suppose a layout satisfies `w(π) + log_{|U|}(2)·|U|^{ω(π)} ≤ (1−2γ)n − O(log n + log K)`.
Then agreement `≤ 1/2 + 3b + |U|^{−γn}`.
* In particular, if the witness cone has at most `log_{|U|}(c n)` edges (`c` small in terms of `γ`), then *every* layout has
  `ω` that small. So the `LayoutBound` layout works whenever `s − k_u ≤ (L−ε)n`.
* For such circuits the union bound gives only a one-sided factor `|U|^{|Z|}`.

**Corollary W2 (refined multiplicity in v1's T3)** [proved here]. In v1's peeling, the number of charges of `y` is at most
`st(y)`, the number of states on accepting paths of `y`. Those states have first part `d_t(y)`, so
`st(y) ≤ Σ_{0<t<T}|U|^{|F_t∩Z|}`. Hence `|A∩S| ≤ ρ·min(p(y)-weighted, T·|U|^{ω})·|A∖S| + res`.

Bounded witness-width cutwidth (`ω = O(1)`) gives error `≥ 1/poly(n)`. That is only weak average-case hardness, unless `ω` is
logarithmic and W1 applies.

### 4.4 Theorem M (probability-gap / RP-type ND circuits)

**Theorem M** [proved here from P2]. Let `p̄(x) = Pr_{w∈U^k}[C(x,w) ∈ Acc] ∈ {0} ∪ [α,1]` for all `x`, with `α ≤ 1/2`. Let
`d = ⌈ln(2/δ)/(2 artanh√α)⌉` and `d(s+1) ≤ (L−ε)n`. Then
```
agreement(S, A_C) ≤ 1/2 + b + δ + (1+2·15^d)(4b + 2e^{−γn}).
```
*Proof.* Use `q` from F2 with this `α`.
* `1_A − q(p̄)` is `0` off `A` (since `p̄ = 0` and `q(0) = 0`) and `≤ δ` on `A`.
* `E[(2·1_S−1)q(p̄)] = Σ_{j≥1} q_j E[(2·1_S−1)p̄^j]`, and each term is `≤ |q_j|(4b+e^{−γn})` by P2 for `j ≤ d`. ∎

Covering `A` by an OR of `r` random witnesses needs `r ≈ ln(1/δ)/α` copies. Chebyshev needs `d ≈ ln(2/δ)/(2√α)`: a quadratic
saving.

### 4.5 Explicit sets

* Li's one-bit sumset extractor ([Li23], Thm 7.13, as cited in Lean `SumsetBridge.lean` [verified from source: the docstring;
  the paper was not re-read]) gives `Bias(2^{c(ε')log n}, ε')` on all cuts, for each fixed `ε'`.
  - So F, F2, W and M hold for this explicit `S_n` with `b = ε'` fixed, e.g. F gives agreement `≤ 1/2 + 2^{D+1}ε' + |U|^{−γn}`.
  - For **vanishing** bias, Lean's `PolynomialWitness.lean` gives degree-4 polynomials with `b_n = n^{−β}`. They have short
    descriptions but are chosen nonconstructively [verified from source].

## 5. Exact reformulation: the target is a property of the circuits alone

Let `𝓡` be the set of large rectangles (all cuts, sides `≥ K`). For `A ⊆ U^n` define
```
Φ_b(A) := min_c [ 2b·Σ_R |c_R||R| + ‖1_A − Σ_R c_R 1_R‖₁ ] / N.
```

**Theorem D** [proved here].
1. Every `S` with `Bias(K,b)` has `signedCount_S(A)/N ≤ Φ_b(A)`.
2. Conversely, let `τ > 0` and `K ≥ C(n log|U|)/τ²`. Then some `S` with `Bias(K, b+τ)` has
   `signedCount_S(A)/N ≥ Φ_b(A) − O(N^{−1/2})`.

*Proof.*
* **(1)** Let `g = 2·1_S − 1`. Then `⟨g,1_A⟩ = Σ c_R⟨g,1_R⟩ + ⟨g, e⟩ ≤ 2bΣ|c_R||R| + ‖e‖₁`.
* **(2), duality.** `max{⟨g,1_A⟩ : ‖g‖_∞ ≤ 1, |⟨g,1_R⟩| ≤ 2b|R| ∀R∈𝓡}` is the support function of an intersection of two
  polyhedra, both containing 0. It equals the infimal convolution of their support functions, which is exactly `N·Φ_b(A)`.
  This is finite LP duality, so there is no gap.
* **(2), rounding.** Take an optimal `g` and set `f = (1+g)/2`. Sample `S` with `Pr[x∈S] = f(x)` independently.
  - A rectangle with sides `≥ K` is the uniform average of its `K×K` subrectangles, so it suffices to control those.
    There are `≤ 2^n|U|^{2Kn}` of them.
  - By Hoeffding and a union bound, all of them have bias `≤ b+τ` with probability `≥ 3/4`.
  - `⟨2·1_S − 1, 1_A⟩` deviates from its mean by `O(√N)` with probability `≥ 3/4`. ∎

**Corollary N (complement partition)** [proved here]. Suppose `A^c` contains disjoint large rectangles `R_i` covering all but
`eN` of it. Take `c = 1` on the whole cube (a large rectangle when `K ≤ |U|^{⌊n/2⌋}`) and `c = −1` on the `R_i`. Then
`Φ_b(A) ≤ 4b + e`, and agreement `≤ 1/2 + 5b + e`.

*Consequences.*
* The hypothesis-only target for a class of ND circuits is *equivalent* (up to `τ`, constants and rounding) to
  `Φ_b(A_C) = O(b) + |U|^{−γn}` for every circuit in the class. That is an `S`-free statement about ND circuits.
* For deterministic circuits, frontier peeling supplies partitions of `A` and of `A^c`, so `Φ_b ≤ 2b + o(1)`. This is the Lean
  proof in disguise.
* A counterexample to the hypothesis-only target is exactly an ND-small `A` with large `Φ_b(A)`. Necessary features
  [proved here]:
  1. `A^c` is not nearly partitionable into large rectangles (N).
  2. At *every* layer of every layout, most of `A`'s mass lies in small atoms of the Venn arrangement `{R(t,q)}_q`. Large
     atoms are rectangles at `X_t` inside `A` and carry signed count `≤ 2b|atom|`.
  3. False positives are covered many times (v1, T3).

  I found no such circuit.

For 2-party unions of `m` rectangles, "`Φ_b(A) = O(b) + o(1)` for all `A` with `m ≤ 2^{cn'}`" is an `S`-free combinatorial
statement. By B1 it would imply `AM^cc ≥ cn'` for *every* two-source extractor in the uniform, side-threshold sense. Its
failure would mean a non-explicit such extractor with cheap uniform-distribution NP protocols. Both directions are open
[speculation].

## 6. Barriers

**B1 (NBP width; coordinator's observation)** [proved here; verified].

*Statement.* Let `𝒫_W` be the read-once NBPs of width `≤ W` in some fixed order. Suppose that for some `S` with prefix-cut
`Bias(K,b)`, every `P ∈ 𝒫_W` has agreement `≤ 1/2 + β`. Then every union of `m ≤ W/|U|^{⌈n/2⌉}` rectangles at the balanced
cut has agreement `≤ 1/2 + β`.

*Proof.* The simulating NBP guesses `q ∈ [m]` and stores `x_L` verbatim. At the middle layer it keeps `q` only if
`x_L ∈ P_q`, then stores `x_R` and finally checks `x_R ∈ Q_q`. Its width is `≤ m|U|^{⌈n/2⌉}`. ∎

By Klauck's averaging (`AM_ε(f) ≥ N^{μ}_ε(f)` for every `μ`; v1, Lemma 5, verified from source), `AM_{1/4}(S) ≥ log m`. Circuit
NBPs have width `|U|^{(1−A_Lε)n+o(n)}`, so a lemma covering them gives `AM ≥ Ω(n)` for Li's extractor. Explicit superlogarithmic
`AM^cc` lower bounds are open [verified from source: GPW, as quoted in v1].

**B2 (narrow NBPs)** [proved here; openness is speculation]. Witness-heavy circuits have narrow programs: with `k_u` large,
`w ≈ A_L(s−n−k_u)`. But an NBP of width `|U|^{θn}` still simulates any union of `m = |U|^{θn/2}` *boxes* `×_i A^i_q` over
`⌈2/θ⌉` consecutive blocks of `θn/2` coordinates. It guesses `q`, stores the current block, checks it at the block end and
resets, for width `m|U|^{θn/2}`.

So a width-only proof at any width `|U|^{θn}` yields `⌈2/θ⌉`-party number-in-hand (NIH) distributional NP lower bounds of cost
`(θ/2)n log|U|`. Boxes are rectangles under any grouping, so these are weaker than 2-party AM bounds. I know of no explicit
bound of this kind [speculation].

**B3 (circuit-level barrier for alphabet-uniform statements)** [proved here; openness is speculation].

*Facts used.* Lean states the deterministic `AverageCaseBound` "uniform over the alphabet" [verified from source]. Its
residual bound `K³(|V|+1)|U|^{w+4}` has `U`-independent constants. So the deterministic bound holds for all `U` once
`n ≥ n₀(ε)`, with `K ≤ |U|^{cn}`.

*Statement.* Suppose the ND target held in this alphabet-uniform form. Take `n = n₀` coordinates over `U = {0,1}^ℓ`. The
circuit `∃w∈U : ∧_{i≤n₀} h_i(x_i, w)` has
* gates `h_i(x_i,w) = [x_i ∈ A^i_w]` (arbitrary binary gates over `U`),
* an AND chain,
* `2n₀−1 ≤ (L−ε)n₀` gates and one witness.

It accepts an arbitrary union of `|U| = 2^ℓ` boxes. Li's extractor on `n₀ℓ` bits has `Bias(poly(n₀ℓ), ε')` at all coordinate
cuts. The target would therefore give: every union of `2^ℓ` boxes in `({0,1}^ℓ)^{n₀}` agrees with Li's extractor on
`≤ 1/2 + O(ε') + 2^{−γn₀ℓ}` of inputs. That is an explicit `n₀`-party NIH distributional NP lower bound of cost `ℓ`.

*Moral.* Over large alphabets, circuit structure gives nothing beyond NIH-AM hardness. A proof of the target must use the
fixed (e.g. binary) alphabet, where such box unions need exponential size.

**B4 (moments, inclusion–exclusion, isolation)** [proved here, except for the cited approximate-degree fact].
1. *Isolation.* Valiant–Vazirani inside the NBP (pairwise-independent `h(w)=Σ_j H_j(w_j)+b`, width `×2^J`) gives
   `Σ_{x∈S}Pr_h[x∈A_h] ≤ ρ2^{−J}Σ_{x∉S}p(x) + 2^J·res` for each `J`.
   - Every such inequality follows from the linear statement (P2) by Markov's inequality.
   - The profile "true positives have `p = 1`, false positives have `p = 2^k`" satisfies all of them at every level while
     having agreement `≈ 1`. So isolation cannot beat the union bound abstractly.
2. *Moments.* Any argument using only `E[(2·1_S−1)binom(p,j)]` (or `p̄^j`) for `j ≤ d` needs a degree-`d` polynomial with
   `r(0) = 0` and `|r−1| ≤ δ` on `[1,R]`, where `R` is the dynamic range of `p`. By LP duality this is equivalent to
   ruling out two distributions on `{0..R}` that match the first `d` moments but differ in their mass at `0`.
   - The approximate degree of this step function is `Θ(√R)` for constant `δ` (Nisan–Szegedy, Paturi; standard, not
     re-fetched).
   - For general ND circuits `R` can be `|U|^{k_u}`, so `d` is exponential.
   - The frontier budget for `j`-fold products is `j(s+1−k_u) ≤ (L−ε)n` (P2 with C1). Since `s+1−k_u ≥ n`, this forces
     `j ≤ 4`. F and F2 use the bounded-range case `R = D`, and M the case of a multiplicative gap.

## 7. Attempt log (why each route stops)

1. **Fix witnesses / union bound.** Equals v1's T4 main term (P1). It gives no two-sided bound.
2. **Valiant–Vazirani hashing in the NBP.** Its level inequalities follow from linear statements; the abstract counterprofile
   is in B4.1.
3. **Linear, randomized or counting normalisation.** Free (P2), but it does not control the OR.
4. **Tensor powers + Linial–Nisan / Kahn–Linial–Samorodnitsky approximate inclusion–exclusion.**
   - It needs degree `√R` (B4.2), and the budget allows `j ≤ 4`.
   - It works for bounded ambiguity (F, F2) and gap circuits (M).
   - The `|U|^{jk}` residual of naive averaging is avoided by WP on `P^{(j)}`.
5. **Spectral / Lindsey for quadratic forms.**
   - Exact: `rank(1_A)` for a union of `m` rectangles can reach `2^m − 1` via inclusion–exclusion.
   - Approximate: approximate rank `≲ m^{O(√m)}` via OR approximation. That beats Lindsey's `2^{n/4}` only for `m = Õ(n²)`.
   - Quadratic forms also fail all-cut bias (v1, P8).
6. **Full subset construction.** Width `2^{|U|^w}`. Forward determinization of the non-cone part also fails, because frontier
   edges whose source lies to the right must be *guessed*: the programs are unambiguous, not deterministic. Keeping `d` as a
   guess and determinizing only the cone gives W.
7. **Nonnegative product decompositions (WAPP-type).**
   - Exact nonnegative rank of a union of few rectangles can be exponential (NOT-EQUAL is `J−I`, full rank).
   - Approximate versions are the AM question again: `NP ⊆ WAPP` with small loss would contradict B1's openness
     [speculation on the exact known status].
   - Lemma L only covers rank-1 terms.
8. **Per-witness tuple tracking of all runs.** Unambiguous with width `|U|^{w+ω(|U|^{k_u}−1)}`, so useful only for
   `k_u = O(log log n)`.
9. **Using the rejecting program `B = {∃w rejecting}` together with T4.** Bounds by `Σ p + Σ p_rej ≈ |U|^{k_u}N`, which is
   useless.
10. **Counterexample constructions.**
    - Random subsets of `A` fail: thick states give large rectangles inside `A`, where `S` must have density 1/2.
    - The overlap patterns of 2-party unions (NEQ, `∃i x_i=y_i`) have complements that partition into large rectangles, so N
      applies.
    - Section 5 lists the necessary features; none was realised.
11. **Recursion on rectangle sides.** `Pre(t,q)` is itself ND-small. But the overlap problem recurs at every level and no
    potential closes [speculation].

## 8. Status of the target and what to try next

* **Target (all witnesses, `1/2 + O(b) + |U|^{−γn}`, `s ≤ (L−ε)n`): open.**
  - By D, the hypothesis-only version is equivalent to an `S`-free property `Φ_b(A_C) = O(b) + o(1)` of small ND circuits.
  - By B1–B3, any proof must use the binary (fixed) alphabet and the gate structure, not only width or bias.
* **Strongest proved two-sided statements:** F/F2 (ambiguity `D`, size `n + k_u + ((L−1)/d − ε)n`), W (logarithmic
  witness-width), M (probability gap), C1 (`s − k_u` accounting).
* **Strongest proved one-sided statement:** v1's T4 with factor `min(p(x), T|U|^{ω})` (W2), for `s − k_u ≤ (L−ε)n`.
* **Suggested next step [speculation].** Prove `Φ_b(A) = O(b)` for ND circuits over `{0,1}` whose witness cone is a *formula*
  (fan-out 1). There the cone's frontier values might be compressible by a ledger, as in `Ledger/*.lean` or the Kirchhoff
  compression in `Dual/Kirchhoff.lean`.

## 9. Numerical checks ([`checks/`](checks/), run with `python3 -I`)

* `circuit_check.py` → `circuit_output.txt`. 60 random ND circuits (`n ≤ 5`, `k ≤ 3`, `s ≤ 8`), random layouts, 1064 inputs
  (525 ambiguous), max width 13, max `ω` 9. Checked:
  - hidden NBP acceptance;
  - C0: path count = number of accepting used-witness restrictions;
  - W: `P'` is unambiguous, accepts the same set and obeys the width bound;
  - C1: `cr = s + 1 − |used inputs|` on 51 connected graphs.
* `reach_vs_used.py`: the "reach the output" reading of v1's Lemma 0 fails on 240 of 728 inputs.
* `nbp_check.py`, `peel_k2.py` → `peel_output.txt`. Checked:
  - Lemma L on 200 random matrices;
  - `P^{(j)}` path counts `= binom(p,j)` for `j ≤ 3`, and the alternating identity;
  - WP: per-peel bound, pointwise removed mass `= φ_q`, terminal small supports, and the final inequality, on 25 non-vacuous
    instances (`n = 6`, exact prefix-cut bias).
* `cheb_check.py`, `binom_basis_check.py` → `cheb_output.txt`, `binom_output.txt`. The Chebyshev step polynomial's error and
  coefficient bounds (M, F2); binomial-basis mass for `D ≤ 1024`.

These are bookkeeping checks at tiny sizes, where the residuals dominate. They do not test the asymptotics.

## 10. Sources

* Local Lean (`cslib-frontier` clone), all [verified from source]:
  - `Nondeterministic.lean`: `hiddenNetwork`, `hiddenNetwork_toMultigraph`, `accepted_hiddenNetwork`,
    `exists_graph_of_nondeterministicDecides`.
  - `Compiler.lean`: cycle-rank count with reachable inputs.
  - `BranchingProgram.lean`: `SmallSides`, `ncard_accepted_le_of_smallSides`, `abs_signedCount_accepted_le` with `2b`.
  - `Network.lean`; `Multigraph.lean` (`LayoutBound`).
  - `AverageCase.lean`: `AverageCaseBound`, uniform over the alphabet.
  - `SumsetBridge.lean` (Li23 citation), `PolynomialWitness.lean`, `Ledger/*`, `Dual/Kirchhoff.lean`, `ThresholdTop.lean`.
* v1 note and its sources:
  - Klauck CCC 2003 (arXiv cs/0208006): `AM_ε = max_μ N^μ_ε`.
  - Klauck CCC 2011 (arXiv 1101.0523).
  - Göös–Pitassi–Watson, ECCC TR15-049: explicit AM lower bounds open.
  - Chattopadhyay–Zuckerman.
* Approximate degree of OR / step functions: N. Nisan, M. Szegedy, *On the degree of Boolean functions as real polynomials*
  (1994); R. Paturi, *On the degree of polynomials that approximate symmetric Boolean functions* (STOC 1992); N. Linial,
  N. Nisan, *Approximate inclusion–exclusion* (1990); J. Kahn, N. Linial, A. Samorodnitsky (1996). Cited from memory, not
  re-fetched in this session.
* X. Li, *Two source extractors for asymptotically optimal entropy, and (many) more*, ECCC TR23-023. Cited via the Lean
  docstring, not re-read.
