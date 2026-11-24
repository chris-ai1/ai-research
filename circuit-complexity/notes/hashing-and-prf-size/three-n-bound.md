# Strong hashing and strongly secure PRFs cost 3n − o(n) gates

> **Unreviewed.** AI-written proofs. No human has checked any of this. This note has had no review at all, not even by a second AI agent. Treat every statement as a claim, not a theorem.

Continues `hash-seed-complexity.md` (cited as H) and `prf-lower-bound.md` (cited as P). Papers:
Fan, Li, Yang, ECCC TR21-125 (**FLY**); Alon, Hoory, Linial, *The Moore bound for irregular
graphs*, 2002 (**AHL**).

Status: my own work in one session, by proof only. Not yet reviewed. Labels: [proved here],
[follows], [not checked], [open].

Setting as in H and P: B₂ circuits with `n` inputs, `m` outputs and `2n + t` gates; terminals,
`τ`, regions as in H Theorem 1.

## 1. Results

H and P determine the cost of hashing and of PRFs up to collision probability / security
`2^{Θ(log² n)}`, where the excess over `2n` reaches `Ω(n)`. Beyond that point they only gave
`(2 + 1/8)n` and `(2 + Ω(1))n`. Here:

> **Theorem 7.** [proved here] Let `0 < η ≤ 1`. If a circuit has `t < (1 − η)n − 4m`, then some
> set `A` of at most `C log n/η` inputs has a separator from the outputs with fewer than `|A|`
> nodes.

> **Corollary 7.1 (hashing).** [follows] A `2^{-ℓ}`-almost universal hash family with `m` outputs
> needs `3n − O(n log² n/ℓ) − 4m` gates. So collision probability `2^{-ω(log² n)}` with `o(n)`
> outputs costs `3n − o(n)`.

> **Theorem 8 (PRFs).** [proved here] One-output circuits with `t < (1 − η)n − C log² n` have a
> distinguisher running in time `n^{O((log n/η)·log(log n/η))}`, for `n^{-1/2} ≤ η ≤ 1`.

> **Corollary 8.1.** [follows] A `T`-secure PRF needs `3n − O(n log³ n/log T)` gates. A PRF secure
> against time `2^{n^ε}` needs `3n − n^{1−ε+o(1)}` gates.

FLY's probabilistic construction (their Corollary 5.7 and Theorem 5.8) gives a non-uniform hash of
size `3n` with collision probability `exp(−n^{Ω(1)})`, and with Levin's trick PRFs of size
`3n + o(n)`. So, up to uniformity of the upper bound:

* almost-universal hashing with collision probability between `2^{-log³ n}` and `2^{-n^{c}}`
  costs `3n ± o(n)` gates;
* sub-exponentially secure PRFs cost `3n ± o(n)` gates. [the security of FLY's `3n + o(n)` PRF
  under a sub-exponential assumption follows from Levin's trick; not checked in detail]

Together with H and P, the picture for collision probability `2^{-ℓ}` (or security `2^{ℓ}`) is:
`2n + n·2^{-Θ(log² n/ℓ)}` for `ℓ ≤ c log² n`, and `3n − O(n log² n/ℓ)` up to `3n` above.

## 2. Proof of Theorem 7

Delete gates that do not reach an output. Assume no input has fan-out 0 and no two inputs share a
terminal; otherwise there is a set of at most two inputs with a smaller separator. Let

* `Q` = the non-output terminals of the form `τ(i)`; `|Q| ≥ n − m`. Split `Q = Q₂ ∪ Q₃` by
  fan-out exactly 2 or at least 3; `q₂, q₃` their sizes.
* `X` = the other non-output terminals, `x = |X|`; `P₀ = X ∪ outputs`, the *pure ports*.

Every terminal is in `Q` or in `P₀`. For a terminal `u` let `N⁺(u)` be the set of terminals
`τ(w)` over the out-neighbours `w` of `u`.

> **Lemma 9 (deficiency).** [proved here] Let `S' ⊆ Q₂`, let `S = S' ∪ (N⁺(S') ∩ Q)`, let `A` be
> the inputs whose terminals are in `S`, and `W = (S ∖ S') ∪ (N⁺(S') ∩ P₀)`. Then `W` meets every
> path from `A` to an output, `|A| ≤ 3|S'|`, and `|A| − |W| ≥ |S'| − |N⁺(S') ∩ P₀|`.

*Proof.* A path from an input of `A` reaches its terminal in `S`. If that terminal is in `S ∖ S'`
it is in `W`. If it is in `S'`, the path continues to a terminal in `N⁺(S')`, which is a pure port
in `W`, or a terminal of `Q`, hence in `S`; repeat. The circuit is acyclic and `S` contains no
output, so the path meets `W`. `|A| = |S|` because `τ` is injective. ∎

So if every set of at most `a` inputs is free of smaller separators, then
`|N⁺(S') ∩ P₀| ≥ |S'|` for every `S' ⊆ Q₂` with `|S'| ≤ a/3`.

Form a multigraph `Γ₀` on the vertex set `P₀` with one edge for each `u ∈ Q₂`: an edge between
the two pure ports in `N⁺(u)` if there are two, a loop if there is one. (If there is none, `{u}`
violates the condition.) A connected subgraph with more edges than vertices violates the
condition, with `S'` its edge set.

> **Lemma 10 (sparsity).** [proved here, using AHL] If a multigraph with loops has `V` vertices and
> at least `(1 + η)V` edges, `0 < η ≤ 1`, it has a connected subgraph with more edges than
> vertices and at most `C log V/η` edges.

*Proof.* Subdivide every edge twice; this keeps `E − V`, makes the graph simple and changes `η`
by a constant factor. Delete vertices of degree at most 1 until none is left; `E − V` does not
decrease, so the result is nonempty with minimum degree 2 and average degree `d ≥ 2 + 2η'`. By
AHL, the number of non-backtracking walks of length `k` is at least `V d (d−1)^{k−1}`, so some
directed edge starts at least `(1 + 2η')^{k−1}` of them. If the ball of radius `k + 1` around it
spans at most one edge outside a breadth-first tree, it is a tree plus one edge, and a
non-backtracking walk in such a graph is determined by its direction on the cycle, the time it
spends there and its endpoint: at most `3kV` walks. So for `k = C' log V/η` the ball spans two
non-tree edges, and these with the tree paths to the root form the subgraph. ∎

Hence `q₂ ≤ (1 + η)|P₀| ≤ (1 + η)(x + m)` with `η = O(log n/a)`.

*Counting.* As in H, `Σ (fan-out − 1)` over the non-output terminals is at most `n + t + m`.
Nodes of `Q₂` contribute 1, nodes of `Q₃` at least 2, nodes of `X` at least 1:
`q₂ + 2q₃ + x ≤ n + t + m`. With `q₃ ≥ n − m − q₂` and `x ≥ q₂/(1+η) − m`:

`t ≥ q₂ + 2(n − m − q₂) + q₂/(1+η) − m − n − m = n − 4m − q₂·η/(1+η) ≥ (1 − η)n − 4m`. ∎

In words: an input of fan-out 3 costs three gates. An input of fan-out 2 costs two, but the
inputs of fan-out 2 need almost as many pure ports as there are of them, and every pure port is a
gate of fan-out at least 2, which costs one more gate.

*Proof of Corollary 7.1.* As in H Corollary 1.1, a family in which every member has such a set
`A` of size at most `a` has a pair colliding with probability at least `(4n)^{-a}`. Take
`η = C'' log² n/ℓ`.

## 3. Proof of Theorem 8

P's Lemma 5 and Corollary 5.1 need a *sparse* triple: `Σ_k σ_k 2^k + 2^q + 1 ≤ 2^{|A|}`, which
holds when `|A| − q ≥ r` and `2^r ≥ σ + 2`.

Let `r = ⌈2 log(log n/η)⌉ + C`. Handle inputs of fan-out 0 and inputs sharing terminals as in P
Lemma 6 (a), (b) with this `r`: either they give a sparse triple with at most `2r` inputs, or
fewer than `r²` inputs are involved, and these inputs and their terminals are set aside (the
terminals are added to `P₀`). The counting of Section 2 then gives: if
`t < (1 − η)n − 4 − 3r²`, then `Γ₀` has more than `(1 + η)|P₀|` edges.

Apply Lemma 10 repeatedly, deleting the edges of each subgraph found. While fewer than `η|P₀|/2`
edges are deleted the density stays above `1 + η/2`, so this yields `r` edge-disjoint connected
subgraphs, each with more edges than vertices and at most `a₀ = C log n/η` edges. Let `S'` be the
union of their edge sets. Then `|S'| − |N⁺(S') ∩ P₀| ≥ r` and `|S'| ≤ r a₀`.

Take `A, W` from Lemma 9: `|A| ≤ 3ra₀` and `|A| − |W| ≥ r`. The nodes between `A` and `W`
(the set `D` of P) lie in the regions of the terminals in `W` and in the regions of `S'`. These
are trees. The only terminals in `D` are those of `S'`, of fan-out 2. So `D` is a forest in which
at most `4|S'|` wires enter the regions of `W`; it has at most `9|S'|` segments and `O(|S'|)`
merge nodes, and every node of `W` receives a wire from `D` or is an input of `A`. With the
choice of `r`, `2^r ≥ 9ra₀ + 2`, so the triple is sparse, and P Corollary 5.1 gives the
distinguisher in time `n^{O(ra₀)}`. ∎

For Corollary 8.1: `T`-security forces `n^{O(ra₀)} > T`, so `η ≤ O(log² n·log(log n/η)/log T)
≤ O(log³ n/log T)`.

## 4. An explicit construction near 3n [not checked; depends on a reference]

FLY's `3n` hash is non-uniform. An explicit one with `(3 + δ)n` gates seems to follow from
explicit bipartite graphs with left degree 3, right degree `3k` and girth
`Ω(log n/log k)` (I believe Füredi, Lazebnik, Seress, Ustimenko, Woldar, *Graphs of prescribed
girth and bi-degree*, 1995, gives these; the parameters need checking). Let the inputs be the left
vertices and output the parity at each right vertex: `3n − n/k` gates. An input set that is missed
induces a subgraph with left degree 3 and right degree at least 2, which in a graph of girth `g`
has at least `2^{g/4}` left vertices. So every nonzero input of weight below
`n^{Ω(1/log k)}` is detected with certainty, with no randomness. Heavier inputs are caught by the
sampled bits of H Section 3.2. With constant `k` this would give an explicit linear hash of size
`(3 + O(1/k))n` with collision probability `2^{-n^{Ω(1/log k)}}` and seed `O(ℓ + log n)`, and
sub-exponentially secure PRFs of the same size from sub-exponentially secure one-way functions.

## 5. Open

1. **[open] Uniform `3n + o(n)`.** Section 4 gives `(3 + δ)n`. Reaching `3n + o(n)` with
   collision probability `2^{-n^{Ω(1)}}` explicitly needs explicit unbalanced graphs of left
   degree 3 in which small sets have unique neighbours.
2. **[open] The transition.** For `ℓ = Θ(log² n)` the cost is `c(ℓ/log² n)·n` with `c` rising
   from 2 to 3. The two regimes are matched only up to constants in `ℓ`.
3. **[open] Lower-order term.** Is `3n − Θ(n log² n/ℓ)` the truth for large `ℓ`?
