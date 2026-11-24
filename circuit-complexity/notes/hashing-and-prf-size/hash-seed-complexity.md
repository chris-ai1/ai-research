# Almost-universal hashing in 2n + o(n) gates: optimal seed and optimal excess

> **Unreviewed.** AI-written proofs. No human has checked any of this. One independent AI review read the proofs and its corrections are incorporated. Treat every statement as a claim, not a theorem.

Papers: Chen, Li, Yang, ECCC TR22-086 rev. 1 (**CLY**); Fan, Li, Yang, ECCC TR21-125 rev. 1
(**FLY**). Numbering of their statements is theirs.

Status: my own work in two sessions, by proof only (no computations). One independent AI review
checked every proof step; its corrections are incorporated. Nothing has been checked by a human. Labels: [proved here],
[follows, not rechecked in detail], [open]. This version replaces the first one; its Theorem 1
(excess `O(n/k + ℓn/r)`) is subsumed by Theorem 3 below.

Notation: `n` inputs, `m` outputs, logarithms base 2. A hash family is `2^{-ℓ}`-almost universal if
every pair `x ≠ y` collides with probability at most `2^{-ℓ}`. Size means the number of gates of a
B₂ circuit (fan-in 2, any gates), and the *excess* of a circuit is its size minus `2n`.

## 1. Results

| | Before | Here |
|---|---|---|
| Size of a `2^{-ℓ}`-almost universal hash, `ω(log n) ≤ ℓ ≤ c₀ log² n/log log n` | `2n + O(nℓ/log² n)`, which is `2n + O(n/log log n)` at the top [CLY] | `2n + n·2^{-Ω(log² n/ℓ)}` (Theorem 3) |
| Seed length | `O(ℓ log^{1+β} n)` [CLY] | `O(ℓ)`, optimal (Theorem 3) |
| Lower bound on the size, any B₂ circuits, any (also nonlinear) hash | `2n − 2m` [FLY Thm 7.6] | `2n + n·2^{-O(log² n/ℓ)} − 3m` (Theorem 1) |
| Collision probability below `2^{-4 log² n − O(log n)}` | open whether `2n + o(n)` is possible [FLY, "major technical open problem"] | impossible for `m = o(n)`: size at least `(2 + 1/8)n − 3m` (Corollary 1.2) |

So for `ω(log n) ≤ ℓ ≤ c₀ log² n/log log n` and output length `m ≤ n^{1−Ω(1)}` the optimal size is
`2n + n·2^{-Θ(log² n/ℓ)}`, attained by an explicit linear family with seed `Θ(ℓ)`. (The qualifier on
`m` is needed: a single layer with `n/k` outputs is a hash with fewer than `2n` gates.)

## 2. Lower bound: small sets of inputs with small separators

> **Theorem 1 (separator).** [proved here] Let `C` be a B₂ circuit with `n` inputs, `m` outputs and
> `2n + t` gates, `m ≥ 1`. Put `v = t + 3m` and suppose `v ≤ n/(4K)` for some `K ≥ 2` (`t` may be
> negative). Then there are a
> set `A` of at most `a_K = 4 log n / log K + 6` inputs and a set `W` of fewer than `|A|` nodes such
> that every path from `A` to an output passes through `W`.

> **Corollary 1.1.** [proved here] Under the same hypothesis, for every fixed assignment to the
> inputs outside `A`, two assignments to `A` give the same outputs. Hence every family of such
> circuits has a pair `x ≠ y` that collides with probability at least `(4n)^{-a_K}`.
> A `2^{-ℓ}`-almost universal family with `6 log n + 12 < ℓ ≤ (4 log n + 6)(log n + 2)` therefore
> has a member with `t ≥ n · 2^{-4 log n (log n + 2)/(ℓ − 6 log n − 12) − 2} − 3m`. For larger `ℓ`,
> `t > n/8 − 3m`.

> **Corollary 1.2.** [proved here] If the collision probability is below
> `2^{-(4 log n + 6)(log n + 2)}`, then some member has more than `(2 + 1/8)n − 3m` gates.

This holds for arbitrary gates and arbitrary (also nonlinear) hash functions. FLY ask for an
almost-universal hash "in 2n size circuits with inverse sub-exponential collision probability" and
give a non-uniform `3n` construction as partial progress. Corollary 1.2 says that `2n + o(n)` is
impossible there when `m = o(n)`, and already once `ℓ` is slightly above `4 log² n`. (For
`m ≥ n/24` the bound is vacuous.)

*Proof of Corollary 1.1 from Theorem 1.* Fix the inputs outside `A`. By induction along a
topological order, every node that cannot be reached from `A` without meeting `W` is a function of
the values on `W` and of the fixed inputs. All outputs are such nodes or lie in `W`. So the `2^{|A|}` assignments to `A`
give at most `2^{|W|} < 2^{|A|}` output vectors. The pairs `x ≠ y` whose supports lie in a common
set of at most `a` inputs number at most `(4n)^a`, and every circuit in the family collides on one
of them. Averaging gives the bound. For the last claims: whenever `K ≥ 2` and
`(4 log n/log K + 6)(log n + 2) < ℓ`, some member has `t + 3m > n/(4K)`. ∎

*Proof of Theorem 1.* Delete gates from which no output is reachable; this only decreases `t`.
Call a node a *terminal* if it is an output or its fan-out is not 1. Every non-output terminal now
has fan-out at least 2, unless it is an input of fan-out 0, in which case `A = {that input}`,
`W = ∅`. For a node `u` let `τ(u)` be the first terminal on the path that starts at `u` and
follows the unique out-wire while the current node is not a terminal. Every path from `u` to an
output passes through `τ(u)`.

*Merging.* If `τ(i) = τ(j)` for inputs `i ≠ j`, take `A = {i, j}`, `W = {τ(i)}`. Assume not.

*Counting.* The fan-outs sum to at most `2(2n + t)` over `3n + t` nodes, so
`Σ_u (fan-out(u) − 1) ≤ n + t`, and outputs contribute at least `−1` each. Hence
`Σ_{u non-output} (fan-out(u) − 1) ≤ n + t + m`. Let `Q` be the set of non-output terminals of the
form `τ(i)`; `|Q| ≥ n − m`. Let `Q₂ ⊆ Q` be those of fan-out exactly 2, and `X` the non-output
terminals outside `Q`. Each node of `Q` contributes at least 1 to the sum, each node of `Q∖Q₂` at
least 2, each node of `X` at least 1. So `|Q∖Q₂| + |X| ≤ t + 2m`. Define the *ports*
`P = outputs ∪ X ∪ (Q∖Q₂)`. Then `|P| ≤ v`, `|Q₂| ≥ n − v`, and every terminal lies in `Q₂ ∪ P`.

*Types.* Call an input `i` good if `v_i := τ(i) ∈ Q₂`. Its two out-wires lead to terminals
`a_i, b_i ∈ Q₂ ∪ P` (the `τ` of the two successors), and every path from `i` to an output passes
through `a_i` or `b_i`.
* Type 0: `a_i = v_j` and `b_i = v_{j'}` are both in `Q₂`. Take `A = {i, j, j'}`,
  `W = {v_j, v_{j'}}`. (If `j = j'` the sizes are 2 and 1.)
* Type 1: `a_i = v_j ∈ Q₂` and `b_i = p ∈ P`. If another type-1 input `i'` has the same port `p`
  and partner `j'`, take `A = {i, i', j, j'}` and `W = {v_j, v_{j'}, p}`. If `j = i'`, take
  `W = {v_{j'}, p}` instead (then `|A| = 3`); symmetrically if `j' = i`; if `j = j'` then
  `|A| = 3`, `|W| = 2`. (`j = i'` and `j' = i` cannot both hold, since the circuit is acyclic.) In
  all cases `W` separates and `|W| = |A| − 1`. Otherwise every port has
  at most one type-1 input, so there are at most `v` of them.
* Type 2: both `a_i, b_i ∈ P`. There are at least `n − 2v` such inputs. They are the edges of a
  multigraph `Γ` (loops allowed) on at most `v` vertices.

*A bicyclic subgraph.* `Γ` has at least `δ·|V(Γ)|` edges with `δ = ⌊(n − 2v)/v⌋ > 4K − 3`.
Deleting vertices of degree below `δ` leaves a nonempty subgraph of minimum degree at least `δ`.
Run breadth-first search from a vertex. If the ball of radius `D` spans at most one non-tree edge,
then counting degrees of the vertices at depth below `D` gives
`δ·|B_{D−1}| ≤ 2|B_D|`, so `|B_D| ≥ (δ/2)^D`. Hence the ball of radius
`D₀ = ⌊log v / log(δ/2)⌋ + 1` spans two non-tree edges. These two edges together with the tree
paths from their endpoints to the root form a connected subgraph `U` with one more edge than
vertices and at most `4D₀ + 2` edges. Take `A = E(U)` and `W = V(U)`. Since `δ/2 > K`,
`|A| ≤ 4 log n/log K + 6`. ∎

## 3. Upper bound

### 3.1 The detector has range `n^{1−ε}` with `O(ℓ/log n)`-wise independence

CLY's detector places the inputs on the edges of a graph `G` of girth `g` by a permutation `σ` and
outputs the parity at each vertex. An input `x` with support `S` is missed iff `σ(S)` is an even
edge set. CLY and FLY analyse this by conditioning on all but `g/3` of the images, which needs
`|S|`-wise independence, hence seed `r log n` for range `r`.

> **Lemma 2.** [proved here] Let `G` have `n' ≥ n` edges, maximum degree `Δ` and girth `g`. Let
> `1 ≤ j ≤ g − 1` and let `σ : [n] → E(G)` be injective and `(j+1)`-wise `δ`-dependent. Then for
> every `S ⊆ [n]` of size `w ≥ g`,
> `Pr[σ(S) is even] ≤ e·w·(2eΔw/(n' − j))^j + (ew)^{j+1} δ`.
> For `0 < |S| < g` the probability is 0.

*Proof.* An even edge set is a union of connected even subgraphs, each of which contains a cycle
and so has at least `g` edges. Hence if `σ(S)` is even, some `j + 1` of its edges form a connected
subgraph. So there are a `(j+1)`-subset `R ⊆ S` and a tree on `R` such that the images of every
two tree-neighbours share a vertex. Fix `R` and the tree. Under exact `(j+1)`-wise independence
reveal the images root first: each of the `j` non-root elements must land on one of at most
`2(Δ − 1)` edges adjacent to its parent's image, out of at least `n' − j` free edges. So the
probability is at most `(2Δ/(n' − j))^j`, plus `δ` in the almost-independent case. There are at
most `C(w, j+1)(j+1)^{j−1} ≤ (ew)^{j+1}` choices of `R` and the tree. ∎

**Corollary 2.1.** Fix `ε ∈ (0,1)`. With `j = ⌈(ℓ + log n + 3)/(ε log n)⌉ ≤ g − 1` and
`δ = 2^{-ℓ-1}(en)^{-(j+1)}`, the detector misses each fixed nonzero `x` of weight at most
`r = n^{1−ε}/(8eΔ)` with probability at most `2^{-ℓ}` (take `n'` a power of 2 below `2n`). The permutation of Kaplan–Naor–Reingold
(CLY Thm 2.8) needs seed `O(j log n + log(1/δ)) = O((ℓ + log n)/ε)`.

### 3.2 Heavy inputs

Inputs of weight above `r` are caught by outputting raw input bits at sampled positions, which
costs no gates. A set of density `μ = r/n'` is hit with probability `1 − 2^{-ℓ}` by a standard
hitter: `O(ℓ)` steps of a walk on a constant-degree expander whose vertices are the pairs
`(α, β)` of field elements, each giving the `⌈4/μ⌉` positions `αi + β`. By pairwise independence
and Chebyshev one step misses with probability at most `1/4`, and CLY Lemma 2.11 gives the rest.
Seed `2 log n + O(ℓ)`; number of sampled bits `b = O(ℓ/μ) = O(ℓ Δ n^ε)`. [proved here; standard]

### 3.3 The hash

> **Theorem 3.** [proved here, using CLY's components] For every constant `c₀ > 0` there are
> constants `c, k₀ > 0` such
> that for `ω(log n) ≤ ℓ ≤ c₀ log² n/log log n` and every `k₀ ≤ k ≤ 2^{c log² n/ℓ}` there is a
> linear `2^{-ℓ}`-almost universal hash family with output length `O(ℓ)`, seed length `O(ℓ)` and
> B₂ size `2n + O(n/k)`.

*Proof.* One *layer* on `N` inputs with parameter `k`: a graph with `Θ(N/k)` vertices, at least
`N` edges, degree `Δ = O(k)` and girth `g ≥ c_g log N/log k` (CLY Thm 2.12), the permutation of
Corollary 2.1 with `ε = 1/2`, and the sampled bits of 3.2. The condition `j ≤ g − 1` holds when
`log k ≤ c log² N/ℓ`. The layer costs at most `2N` gates, has seed `O(ℓ)`, outputs
`O(N/k) + O(ℓ k √N) = O(N/k)` bits, and two distinct inputs collide with probability at most
`2·2^{-ℓ}` (the two-case argument of CLY Lemma 3.2, with the new detector and sampler). CLY's
graphs exist for `k` up to a factor 3, which the `O(·)` absorbs.

Apply a first layer with the given `k`, then layers with parameter `k' = 2^{c log² n/(2ℓ)}`, which
is at least a fixed power of `log n`, until the length is below `n/(kℓ)`. This takes `O(1)`
layers. Finish with the expander-walk hash of CLY Construction 4 (seed `O(log n + ℓ)`, cost
`length × O(ℓ) ≤ O(n/k)`). Collision probabilities add (CLY Prop. 3.7), and running everything
with `ℓ + O(1)` in place of `ℓ` gives `2^{-ℓ}`. The total size is
`2n + 2·O(n/k)(1 + 1/k' + …) + O(n/k)`. ∎

Remarks.
* *Seed.* For `m < n`, `ℓ` bits are necessary: with fewer than `2^ℓ` functions, a pair that collides for one of
  them collides with probability above `2^{-ℓ}`, and no function is injective.
* *Size.* By Corollary 1.1 the excess `n·2^{-Θ(log² n/ℓ)}` is optimal up to the constant in the
  exponent, for `m ≤ n^{1−Ω(1)}`. As written, the construction gives exponent constant slightly
  below `1/2` (it could approach 1 with `ε → 1`), against `4` in the lower bound. Part of the gap
  is the gap in the extremal girth problem.
* *Larger `ℓ`.* With `k` a constant the same proof gives size `(2 + O(1/k))n` for
  `ℓ ≤ c log² n/log k`, matching Corollary 1.2 up to constants. The number of layers is then
  `O(log log n)`, so the seed is `O(ℓ log log n)`. [follows, not rechecked in detail]
* *Uniformity.* All components are the strongly explicit ones CLY use, plus an explicit hitter, so
  the family should be locally explicit and POLYLOGTIME-uniform in CLY's sense. [not rechecked]

## 4. Consequences [follow from CLY's proofs with the new hash; not rechecked in detail]

CLY's magnification theorems use the hash through its size, its seed length (the kernel instance
is seed plus hash value) and its explicitness.

* **Sparse NP languages (CLY Thm 4.1, 1.2, 1.3).** For a `2^{s}`-sparse language the threshold
  becomes `2n + n·2^{-Ω(log² n/s)}` in place of `2n + O(ns/log² n)`. The kernel has `O(s)` bits
  instead of `O(s log³ n)`. At CLY's parameters (`s = log² n/log log n`) the threshold is
  `2n + n/log^{Ω(1)} n` instead of `2n + O(n/log log n)`, and the conclusion
  `NTIME[2^n] ⊄ SIZE[2^{n^{1/5}}]` becomes `NTIME[2^n] ⊄ SIZE[2^{n^{1/2}}]` (pad the kernel to
  length `(log n/2c)²` instead of `(log n/2c)⁵`).
* **MCSP (CLY Thm 4.3, 1.6).** With `g = s log s`: if `MCSP[s]` has no probabilistic circuits of
  size `2N + N·2^{-Ω(log² N/g)}` and error `2^{-Ω(g)}`, then `P ⊄ SIZE[2^{N^c}]`. At `s = n`
  the threshold is `2N + N^{1 − Ω(1/log log N)}`, where CLY have
  `2N + O(N log log N/log N)`. Row 1b of [the MCSP project](../../results/mcsp/) claims `2N − O(N/log N)` in a regime
  that covers this one.
* **PRFs (CLY Thm 5.4–5.8).** `2^{Ω(ℓ)}`-secure PRFs of size `2n + n·2^{-Ω(log² n/ℓ)}`, for
  instance `2n + n^{1−o(1)}` for every superpolynomial security `n^{ω(1)}` that is at most
  `2^{c₀ log² n/log log n}`, under the same assumptions.
* **Limits of the method.** By Theorem 1, any kernelization that computes one hash value by a
  B₂ circuit and needs collision probability `2^{-ℓ}` costs at least
  `2n + n·2^{-O(log² n/ℓ)}` minus three times the hash length. So the thresholds above cannot be
  lowered by a better hash, and sparsity beyond `2^{O(log² n)}` cannot be handled at `2n + o(n)`
  this way. This says nothing about other kernelizations.

## 5. Open

1. **PRFs.** Theorem 1 gives collisions, which say nothing about one-bit functions. The extension
   to PRFs is in `prf-lower-bound.md`.
2. **The constant.** For collision probability `2^{-ω(log² n)}`, Corollary 1.2 gives `(2 + 1/8)n`.
   `three-n-bound.md` claims `3n − o(n)`, matching FLY's non-uniform `3n`; that note is unreviewed.
3. **[open] The exponent.** Close the gap between about `1` and `4` in `n·2^{-γ log² n/ℓ}`.
