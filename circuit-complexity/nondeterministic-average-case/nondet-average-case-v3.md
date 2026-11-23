# Nondeterministic average case, v3: tree-like witness cones, and why parity is a barrier

Continues [`nondet-average-case-v2.md`](nondet-average-case-v2.md). Notation as there: `C(x,w)` is a fan-in-2 nondeterministic
circuit with `n` inputs, `k_u` used witness inputs and `s` gates; `A = {x : ∃w C(x,w) accepts}`;
`S` has bias `b` on rectangles with both sides `≥ K` at every cut; `L = 1 + 1/A_L` is the frontier
constant. The *witness cone* is the set of witness inputs and gates that depend on a witness.

Status labels: **[proved here]**, **[checked]** (brute force), **[speculation]**.
Sections 1–8 were checked by one independent AI review, and its corrections are incorporated. No
human has reviewed the note, and nothing is formalized. Constants use `L ≈ 4.576`.

## 1. Theorem T: tree-like witness cones [proved here; simulation step checked]

**Hypothesis.** Every wire of the witness cone is used as a gate input at most once, counting
multiplicity (so `op(c,c)` on a cone wire `c` is excluded). The cone consists of the witness inputs
and the gates reachable from them. Wires that depend only on `x` may be reused freely, inside and
outside the cone.

**Claim.** `A` is decided by a *deterministic* circuit on the same graph over the three-letter
alphabet `𝒱 = {{0},{1},{0,1}}`, with the witness inputs replaced by the constant `{0,1}`.

**Proof.** For a wire `e` and fixed `x`, let `V_e(x) ⊆ {0,1}` be the set of values `e` takes as
`w` ranges over all witnesses. An `x`-determined wire has a singleton, a witness input has `{0,1}`.
Let `g = op(g₁,g₂)` be a cone gate. The cone below `g₁` and the cone below `g₂` share no cone wire:
a shared cone wire would have two different paths up to `g`, so some cone wire on them would have
fan-out 2. Hence they use disjoint sets of witness inputs, the pairs `(g₁,g₂)` range over
`V_{g₁} × V_{g₂}` independently, and `V_g = {op(u,v) : u ∈ V_{g₁}, v ∈ V_{g₂}}`. This is a function
of `(V_{g₁},V_{g₂})`. The circuit accepts `x` iff the accepting value lies in `V_out(x)`. ∎

`checks/v3/tree_cone_check.py` confirms the simulation on 7,496 inputs of random circuits (5,263 of them
with more than one accepting witness, 0 mismatches). With one witness bit used twice, the lifted
circuit over-approximates on 322 of 7,496 inputs, so the hypothesis is needed.

**Consequence.** The lifted circuit is deterministic, so its network has a unique satisfying
assignment and its branching program is unambiguous for every layout. Witness inputs become
constants, which only lower the cycle rank (v2, C1). A layout of width `w` gives at most
`3^{w+O(1)}` states per layer, against `2^n` inputs. So the deterministic average-case argument
applies whenever `A_L (s − k_u − n) · log₂3 ≤ (1−δ) n`:

> If the witness cone is tree-like and `s − k_u ≤ (1 + (L−1)/log₂3 − ε) n ≈ 3.26 n`, then the
> circuit agrees with `S` on at most a `1/2 + O(b) + 2^{−γn}` fraction of inputs.

This is two-sided, and there is no condition on the number of witnesses or on the number of
accepting witnesses per input. (First fold subtrees that depend on witnesses only into constants
and contract the unary gates this leaves; `s − k_u` counts the remaining binary gates. This is
needed because v2's C1 assumes `s ≤ c₀n`.) Only cone wires need three values, so the sharper condition is
`w_det + ω·log₂3 ≤ (1−δ)n` for a layout with `w_det` non-cone and `ω` cone edges per cut.

Caveats.
* The Lean theorem is stated for one alphabet for inputs and wires. The statement above needs the
  mixed version (binary inputs, ternary wires). The counting is the same: in the Lean proofs the
  peeling bound for programs has a state type independent of the input alphabet, and the alphabet
  enters only through the number of program edges. The compile step for mixed alphabets is not
  formalized. A version that follows from the Lean statement as it stands, by pairing input
  bits into a 4-letter alphabet, gives only about `(L/2) n ≈ 2.29 n`.
* The same proof handles co-nondeterministic acceptance (`V_out = {accepting value}`).
* "Each witness *input* feeds one gate" alone is no restriction: a buffer gate on the witness is
  free and has arbitrary fan-out. The restriction has to cover the whole cone.

Theorem L (Section 7) extends this to cones that reuse witness-dependent wires.

## 2. Theorem E: few entry wires [proved here]

Let `m` be the number of `x`-determined wires that feed the witness cone, `s_det` the number of
gates outside the cone, `n_det` the number of inputs that feed some gate outside the cone, and `c`
the number of connected components of the part outside the cone. Then `A = g⁻¹(B)` for the
deterministic map `g : {0,1}^n → {0,1}^m` and some `B ⊆ {0,1}^m`. Lay out the network of `g` and
keep its `m` output edges open to the end. The program is unambiguous and has width at most
`A_L(s_det − n_det + c) + m + o(n)`. So

> if `s_det + (n − n_det) + c + m/A_L ≤ (L − ε) n`, agreement is at most `1/2 + O(b) + 2^{−γn}`,

for every `B`, with no condition on the cone. An entry wire costs `1/A_L ≈ 3.6` gates, and an input
that enters the cone directly costs `L`, so the theorem says nothing when most inputs do.

## 3. Barrier B5: the proof must fail for parity [proved here]

Replace "some witness accepts" by "an odd number of witnesses accept". At one cut `(a | b)`, a
read-once parity program with `O(n)` states computes inner product: guess `i`, remember `a_i`,
check `b_i`. Inner product has bias `2^{−Ω(n)}` on the rectangles of that cut with sides at least
`2^{(1/4+ε)n}`. (It has monochromatic rectangles with sides `2^{n/4}`, so this is not the regime
`log K = o(n)`; the barrier applies to arguments whose error term is `poly(K)·width`.) So any
argument that
* uses only the rectangle structure at a cut and the width, and
* still works when OR over witnesses is replaced by XOR,

is false. (Section 6 sharpens this: with one witness bit, OR and XOR are equivalent.) Valiant–Vazirani hashing, isolation by weights and counting modulo a prime all turn the
OR into exactly such a parity or count, which is why they reduce to the linear statements (v2, B4).
A proof has to use monotonicity of OR in the witness set. (This is a statement about programs at
one cut. For linear-size parity-nondeterministic *circuits* and all-cut bias I know no example.)

## 4. The two-party core, restated [proved here]

At a cut, let `U_a ⊆ [W]` be the frontier states reachable from the left on `a`, and `V_b ⊆ [W]`
those from which acceptance is reachable on `b`. Then `(a,b) ∈ A ⟺ U_a ∩ V_b ≠ ∅`, and `(U_a,V_b)`
is distributed as a *product* distribution. The target at one cut is: a set with small bias on
large rectangles has small correlation with set-intersection under every product distribution on
pairs of subsets of `[W]`, `W = 2^{θn}`.

What inclusion–exclusion gives, with `c(a,b) = |U_a ∩ V_b|` and no limit on depth:

* `|signed(A)| ≤ 2b·E[2^{c}]·N + (small rectangles)`. Bounded exponential moment suffices; a
  bound on `max c` is not needed.
* Thinning. If `c ∈ {0} ∪ [T, RT]` on all inputs, keep each state with probability `μ/T`:
  `|signed(A)|/N ≤ 2b·e^{Rμ} + e^{−μ}`, so the advantage is `O(b^{1/(R+1)})` for every `T`.
* Many scales (`c` spread over `1 … 2^k`) defeat both: the heavy inputs make every expansion
  diverge. This is the regime equivalent to Arthur–Merlin lower bounds (v2, B1).

For circuits the depth of the expansion is the number of copies of the cone, which the size
budget caps (v2, B4), so only the first bullet at depth ≤ 4 transfers.

## 5. A single cut is not enough: XOR against OR [proved here; bias claim re-derived and re-tested by the review]

Rows are pairs `(q,q') ∈ [M]²`, columns are `b ∈ [m]`, and `g, g' : [M]×[m] → {0,1}` are random.
Put `S = g(q,b) ⊕ g'(q',b)` and `A = g(q,b) ∨ g'(q',b)`. Take `M ≥ 2K`.

* `A` is a union of `2M` rectangles with `M` rows each, and a read-once nondeterministic program in
  the order `(q, q', b)` accepts it with `2M` states at the last cut: guess which of `q, q'` to keep.
* `A` agrees with `S` on 3/4 of the inputs (OR and XOR of two fair bits).
* `S` has bias at most `δ` on every rectangle of the cut `({q,q'} | {b})` with both sides `≥ K`,
  once `K ≥ C·(log(M²m))²/δ²`. For a fixed `K×K` rectangle the sum is a Rademacher chaos with
  Frobenius norm `K` and operator norm `≤ √K`, so Hanson–Wright gives `exp(−cδK^{3/2})`; there are
  at most `M^{2K} m^K` such rectangles; larger rectangles reduce to `K×K` by averaging.
* Numerics (`checks/v3/xor_or_strong.py`; signed sum over `K²`; alternating search with restarts
  and structured starts; `S` against an i.i.d. matrix): 0.568 / 0.535 at `(M,m,K) = (128,4096,64)`;
  0.469 / 0.468 at `(160,2048,80)`; 0.369 / 0.360 at `(128,4096,128)`. Structure buys the adversary
  at most about 6%.

So the following statement, which v2 listed as open, is false: *small bias on the large rectangles
of one cut bounds the correlation with a union of few large rectangles at that cut.* This does not
remove v2's barrier B1, which concerns a given explicit `S`.

`S` is far from unbiased at the other cuts. For fixed `b` it is a rank-2 function of `(q,q')`, so
it is constant on `{q : g(q,b)=0} × {(q',b) : g'(q',b)=0}`, a rectangle of the cut `({q} | {q',b})`
with sides about `M/2 ≥ K`. So the example says nothing against arguments that use the hypothesis
at every cut. (Theorem F does not apply to it either: the two-fold product program has `M²`
states, as many as rows.)

## 6. One witness bit is a deterministic problem [proved here]

Let `h(y,w)` have `n` inputs `y`, one witness bit `w` and `s ≤ (L−ε)n` gates. Write
`h_i = h(·,i)` and `A_i = h_i⁻¹(1)`, so `A = A_0 ∪ A_1`. Each `h_i` is a deterministic circuit with
`s` gates, so `|signed(A_i)| ≤ 2b|A_i| + 2^{−γn}N`. By inclusion–exclusion

`signed(A) = signed(A_0) + signed(A_1) − signed(A_0 ∩ A_1)`,

and `1[h_0 ⊕ h_1] = 1_{A_0} + 1_{A_1} − 2·1_{A_0∩A_1}`. Hence, for circuits with one witness bit,
the following are equivalent up to `O(b) + 2^{−γn}`:

1. the nondeterministic circuit `∃w h(y,w)` has small correlation with `S`;
2. the conjunction `h_0 ∧ h_1` has small correlation with `S`;
3. the derivative `∂_w h = h_0 ⊕ h_1` has small correlation with `S`.

So for one witness bit OR and XOR cannot be told apart at all (compare B5), and the question is
about a *deterministic* object: two restrictions of one small circuit.

**What the method gives.** Run the two restrictions along one layout of `h`'s graph; non-cone
edges are shared, cone edges are doubled. The pair program is unambiguous with `2^{w_det + 2ω}`
states. So all three statements hold when some layout has `w_det + 2ω ≤ (1−δ)n`, in particular
when `s ≤ (1 + (L−1)/2 − ε)n ≈ 2.79n`. (This is Theorem F at `D = 2`. The generic bound for the
doubled circuit, which has `2s+1` gates, would only give `≈ 2.29n`.)

**What is open, and why it matters.** For `2.79n < s < Ln`:

> (Q) Is there a circuit `h(y,w)` with fewer than `(L−ε)n` gates whose derivative
> `h(y,0) ⊕ h(y,1)` has small bias on all large rectangles at all cuts?

* If yes, the target is false for `S = ∂_w h`, with one witness bit: one of the four circuits
  `∃w [h(y,w) ⊕ c_w]` agrees with `S` or its complement on at least `3/4 − b` of the inputs.
  (The complement of its accepted set is the cell `{h_0 = α, h_1 = β}`, which lies inside
  `{S = α⊕β}`; the agreement with that side is `1/2 ± b` plus the density of the cell, and for each
  side one of its two cells has density at least `1/4 − b/2`.) The target would then need a property of the
  explicit set beyond bias on rectangles.
* If no for every `S`-correlated version, that is a deterministic average-case bound for
  circuits of the doubled form at total size `≈ 2(L−ε)n ≈ 9.15n`. In general, the target at size
  `cn + 1` for one witness bit implies the deterministic bound for the XOR and the AND of two
  restrictions of one circuit of size `cn`. That class has circuits of size `2cn`, but it is not
  all circuits of that size.
* I see no obstruction to (Q) having a positive answer. For `h(y,w) = T(y ⊕ w·1)` the two
  restrictions are `T` and `T∘¬`; their rectangle partitions at a cut have `2^{A_L(|T|−n)}` parts
  each, and the common refinement has more than `2^n` parts once `|T| > 2.79n`. But I also know no
  function with small bias at all cuts and a circuit of size `O(n)` with a small constant. For a
  polynomial of degree `d` to qualify one needs `(log K)^{d−1} ≳ n`, and sparse polynomials never
  qualify (set the neighbours of a small set of variables to 0). [speculation]

**Reading.** The first open case of the problem is not about nondeterminism. It asks whether the
frontier method can be pushed from `2.79n` to `Ln` for a derivative. The natural conjecture for
nondeterministic circuits is a bound with a smaller constant than the deterministic `L`.

## 7. Running the witnesses in parallel: Theorems P and L [proved here; checked]

Both theorems replace the circuit by a *deterministic* circuit on the same graph over a larger
alphabet on the cone wires. A deterministic circuit has a unique satisfying assignment, so every
layout gives an unambiguous program for `A` itself. No inclusion–exclusion is needed and the
conclusion is `1/2 + O(b) + 2^{−γn}` with the same constant as in the deterministic theorem. The
size condition is that some layout satisfies

`w_det + Σ_{e ∈ cone edges of the cut} cost(e) ≤ (1−δ) n`,     (★)

where `cost(e)` is the number of bits of the state carried by `e`. (As in Theorem T, this needs
the mixed-alphabet form of the Lean theorem, which is not formalized.)

**Theorem P (profiles).** Let `W_e` be the set of witness inputs that wire `e` depends on. Carry on
`e` its *profile*, the value of `e` as a function of the bits in `W_e`. The profile of a gate is a
function of the profiles of its inputs, and `x` is accepted iff the profile of the output is not
identically rejecting. So (★) holds with `cost(e) = 2^{|W_e|}`. Consequences:

* `k` witness bits in total: the bound holds for `s − k_u ≤ (1 + (L−1)/2^k − ε) n`, that is
  `2.79n, 1.89n, 1.45n` for `k = 1, 2, 3`. This replaces Theorem F's factor `2^{D+1} b` by `O(b)`.
* The output wire depends on every used witness bit, so this cannot help beyond
  `k_u ≈ log₂ n`. Up to there it helps when few wires of a cut depend on many witness bits.

**Theorem L (live branch points).** A *branch point* is a witness-dependent wire, witness inputs
included, that is used as a gate input at least twice, counting multiplicity. Define the live set of each wire bottom-up: `L_g` consists of those
`z ∈ L_{c₁} ∪ L_{c₂} ∪ ({c₁,c₂} ∩ branch points)` from which some path to the output avoids `g`.
Carry on `g` the relation `Ψ_g = {(β, v)}`: the values `β` of the live branch points together with
a value `v` of `g`, over all witnesses. Then `Ψ_g` is the join of `Ψ_{c₁}` and `Ψ_{c₂}`, pushed
through the gate and projected to `L_g`. The join identifies equal names: common live points, and
also a child that is itself a branch point with its occurrence in the other child's live set; `x` is accepted iff `Ψ_out`
contains the accepting value. So (★) holds with `cost(e) ≤ 2^{|L_e|+1}`, and `log₂3` when `L_e = ∅`.

*Why the join is exact.* Any wire below both inputs of `g` reaches them along two paths, and the
last common wire of those paths is a branch point from which the output is reachable avoiding
either input. So either it is live at both inputs, or it was dropped at a wire that all its paths
pass through, and that wire has taken its place. Given the common live values, the remaining
witness bits below the two inputs are disjoint. The review completed the argument with two
facts: a live point of `c₁` lying below `c₂` is live at `c₂` or equals `c₂`; and every shared wire
with a private consumer is live on both sides. Given agreement on the common names, two witnesses
splice.

*Check.* `checks/v3/live_profile_check.py` compares both liftings with brute force over all witnesses:
3,000 random circuits (28,500 inputs), 0 mismatches for either theorem. The review's independent
implementation (`checks/v3/live_adversarial.py`): 80,000 circuits including nested diamonds, ladders and equal children, up to 11
live points, and all wirings with at most 4 gates, 0 mismatches. The three details above matter:
counting fan-out by distinct gates, joining only on common live points, or not treating witness
inputs as branch points each gives over a thousand mismatches.

Theorem T is the case `L_e = ∅` everywhere. Theorem W (v2) is the other extreme: it pays
`2^{ω}` for the whole cut, however the cone is wired.

## 8. Restating the target [speculation, except where marked]

Count capacity. With `r` restrictions run in parallel, a cone wire carries `r` bits, so a graph
needs cutwidth only about `n/r` for the tuple program to reach full width `n`. Theorem P is the
matching positive statement: below `(1 + (L−1)/2^k)n` nothing can go wrong. Above that threshold
the method has no objection to a circuit whose `2^k` restrictions have a parity that is unbiased
at all cuts. For one bit the OR then agrees with it on 3/4 of inputs; for `k` bits the same
argument only gives `1/2 + 2^{−2^k}`.

* Over large alphabets this is what happens. The pair `(h_0,h_1)` of a circuit with random gate
  functions behaves like one circuit whose wires carry two symbols, and v2's barrier B3 is the case
  where the witness is a whole symbol. [heuristic; not proved for an asymptotic family]
* Over the binary alphabet it is question (Q). It depends on how small a circuit with small bias
  at all cuts can be, which is not known.

A statement that the evidence supports:

> **Conjecture.** For every `k` and `ε > 0`, nondeterministic circuits with `k` witness bits and at
> most `(1 + (L−1)/2^k − ε) n` gates beyond the witnesses have agreement at most `1/2 + O(b) + 2^{−γn}`
> with every `S` of bias `b` at all cuts [this part is Theorem P, with `γ` depending on `k`, and
> modulo the mixed-alphabet compile step], and the constant
> `(L−1)/2^k` cannot be replaced by `L−1` for all such `S`.

For unbounded `k` the positive results are the structural ones: Theorems T, E, L, W and M.

## 9. What remains

The smallest open case is one witness bit with `2.79n < s < Ln`, which is question (Q) of
Section 6. Any progress on the general problem has to settle (Q) first, and (Q) may well have a
positive answer, in which case the target as stated (every set with small bias at all cuts) is
false and Section 8 is the right statement. The remaining unchecked pieces are the mixed-alphabet compile step and v2's Theorems F, W and M.
