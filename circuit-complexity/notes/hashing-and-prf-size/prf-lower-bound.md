# Pseudorandom functions need 2n + n·2^{-O(log² n / log T)} gates

> **Unreviewed.** AI-written proofs. No human has checked any of this. One independent AI review read the proofs and its corrections are incorporated. Treat every statement as a claim, not a theorem.

Continues `hash-seed-complexity.md` (its Theorem 1 and Theorem 3 are cited as H1 and H3). Papers:
Fan, Li, Yang, ECCC TR21-125 (**FLY**); Chen, Li, Yang, ECCC TR22-086 (**CLY**).

Status: my own work in one session, by proof only. One independent AI review checked every step;
its corrections are incorporated. Nothing has been checked by a human. Labels: [proved here],
[follows], [open].

Setting: a function family `F_n` of one-output functions on `n` bits, each computed by a B₂
circuit (fan-in 2, arbitrary gates) with at most `2n + t` gates. A *distinguisher* is an oracle
algorithm that accepts every member of the family and rejects a uniformly random function with
probability at least 2/3. `F` is *T-secure* if no distinguisher runs in time `T`.

## 1. Results

> **Theorem 4.** [proved here] There are constants `C, K₀, c > 0` such that for every
> `K₀ ≤ K ≤ cn` and all large `n`: the class of one-output B₂ circuits with `2n + t` gates, `t + 3 ≤ n/(40K)`, has a
> deterministic non-adaptive distinguisher running in time `n^{O(a)}`, where
> `a = 12 log n/log K + C`.

> **Corollary 4.1.** [follows] A `T`-secure PRF family has circuits of size at least
> `2n + n·2^{-O(1 + log² n/log T)}`, for `T ≥ n^{ω(1)}`. In particular:
> * every PRF secure against polynomial time needs `2n + n^{1−o(1)}` gates (size `2n + n^{1−δ}`
>   is broken in time `n^{O(1/δ)}`);
> * for every fixed `C' > 0`, a PRF secure against time `2^{C' log² n}` needs `(2 + Ω(1))n` gates.
>   So neither sub-exponentially secure nor even `2^{log³ n}`-secure PRFs exist in size
>   `2n + o(n)`;
> * since an AC⁰[2] circuit with `w` wires converts to at most `w` B₂ gates, PRFs in AC⁰[2] need
>   `2n + n^{1−o(1)}` wires (FLY: `2n + Ω(√n)`).
>
> Security here means: no distinguisher (deterministic, accepts every member, rejects a random
> function with probability 2/3) runs in time `T`. A PRF that is `T`-secure in FLY's and CLY's
> sense (time `T`, advantage `1/T`) is secure in this sense, so the bound applies to it.

Together with the construction (H3 plus Levin's trick, CLY Thm 5.4), which gives `2^{Ω(ℓ)}`-secure
PRFs of size `2n + n·2^{-Ω(log² n/ℓ)}` for `ω(log n) ≤ ℓ ≤ c₀ log² n/log log n` assuming
sub-exponentially secure one-way functions:

> **Corollary 4.2.** [follows] For `n^{ω(1)} ≤ T ≤ 2^{c₀ log² n/log log n}`, the smallest size of a
> `T`-secure PRF is `2n + n·2^{-Θ(log² n/log T)}` (the upper bound under the assumption above).

FLY prove `2n − O(1)` and construct `2n + o(n)`. They pose the problem of a `2n`-size hash with
inverse sub-exponential collision probability, "which would lead to constructions of
sub-exponentially secure PRFs in `2n + o(n)` size circuits". Corollary 4.1 says such PRFs do not
exist in B₂ circuits, by any route.

## 2. Why collisions are not enough, and what replaces them

H1 finds a set `A` of inputs and a separator `W` with `|W| < |A|`. For one-bit outputs this alone
says nothing: every Boolean function of `A` factors through one bit. What is special is *how* the
values on `W` depend on `A`. Between `A` and `W` the circuit is a union of trees, so the values on
`W` are determined by a few path types, and those types can depend on the rest of the circuit only
through the values of earlier separator nodes. That leaves too few possible functions.

## 3. The type lemma

Fix a circuit, a set `A` of inputs and a set `W` of nodes that meets every path from `A` to the
output, and is minimal with this property; order `W = (w₁, …, w_q)` topologically. Let `D` be the
set of nodes outside `W` that are reachable from `A` by a path avoiding `W`. (After deleting gates
that do not reach the output, every out-neighbour of a node of `D` lies in `D ∪ W`, and the output
is not in `D`.)

In `D ∪ W` call a gate a *pass node* if exactly one of its in-wires comes from `D`, and a *merge
node* if both do. A *segment* is a maximal path of pass nodes in which only the last may have
fan-out at least 2 or lie in `W`. For a segment `S` let `k(S)` be the least index of a separator node
reachable from `S` inside `D ∪ W`. Let `σ_k` be the number of segments with `k(S) = k`. The
*shape* consists of the graph obtained from `D ∪ W` by contracting segments, the gates at merge
nodes, and the numbers `k(S)`. Its *size* is the number of nodes of the contracted graph.

> **Lemma 5 (types).** [proved here] Fix the inputs outside `A` to `z`, and write `y` for the
> assignment to `A` and `ω_k(y)` for the value of `w_k`.
> 1. Every segment computes one of the four unary functions of its entry value. Which one is a
>    function `θ_S` of `z` and of `(ω_1(y), …, ω_{k(S)−1}(y))` only.
> 2. Hence `f(y, z) = Ψ_z(ω(y))`, where `ω` belongs to the family `Ω` of maps obtained from the
>    shape by choosing, for every segment `S`, a function `θ_S : {0,1}^{k(S)−1} → {4 types}`.
>    `log₂|Ω| ≤ Σ_k σ_k 2^k`.
> 3. A uniformly random function of `y` is of the form `Ψ∘ω` with `ω ∈ Ω` with probability at most
>    `2^{Σ_k σ_k 2^k + 2^q − 2^{|A|}}`.
> 4. Whether a given function of `y` is of that form can be decided in time `2^{O(|A| + σ)}`,
>    `σ = Σ σ_k`.

*Proof.* (1) A pass node has one in-neighbour `u` outside `D` (or in `W`). If `u ∉ W`, then `u` is
not reachable from `A` without meeting `W`, so its value is a function of `z` and of the
separator nodes above it. Each of those has a path through `u` and the pass node to every
separator node reachable from the segment, so it comes strictly before `w_{k(S)}`. With that
in-neighbour fixed, a binary gate is one of the four unary functions, and so is a composition of
them. (2) Evaluate the separator nodes in order: `ω_k(y)` is obtained from `y`, the merge gates
and the types of the segments with `k(S) ≤ k`. Since `W` separates, `f` is a function of `ω` and
`z`. A map `θ_S` has `4^{2^{k(S)−1}}` possibilities. (3) A fixed `ω` has at most `2^q` fibres, and
a random function is constant on all of them with probability at most `2^{2^q − 2^{|A|}}`. Take
the union over `Ω`. (4) Recurse on `k` with the set `Y` of assignments that share the values
`ω_{<k}`: try each choice of the types of the segments with `k(S) = k`, split `Y` by `ω_k`, and
recurse on both parts; at the end check that the function is constant on `Y`. The choices for
different prefixes are independent, so the time is `2^{|A|}·Π_k (2·4^{σ_k})`. ∎

> **Corollary 5.1 (test).** [proved here] Call a triple (A, W, shape) *sparse* if
> `Σ_k σ_k 2^k + 2^q + 1 ≤ 2^{|A|}`. If a circuit contains a sparse triple with `|A| ≤ a` and
> shape of size `O(a)` (so there are `2^{O(a log a)}` shapes to try), the following test accepts it: for every set `A` of at most `a` inputs and every
> sparse shape on it, query the function on `A`'s subcube for `N = ⌈4a log n⌉` fixed distinct
> assignments `z` to the other inputs, and accept if for some (A, shape) all `N` restrictions have the form
> `Ψ∘ω`, `ω ∈ Ω`. A random function passes one (A, shape, z) with probability at most 1/2,
> independently over `z`, so it is accepted with probability at most
> `n^a·2^{O(a log a)}·2^{-N} < 1/3`. Time `n^{O(a)}`.

## 4. Every small circuit contains a sparse triple

> **Lemma 6 (structure).** [proved here] Let a one-output circuit have `2n + t` gates and put
> `v = t + 3`. If `v ≤ n/(40K)` with `K₀ ≤ K ≤ cn`, the circuit contains a sparse triple with
> `|A| ≤ 12 log n/log K + C` and shape of size `O(|A|)`. (In every case below `D` is a forest
> inside regions, with at most `|A| + 5` merge nodes, and every node of `W` has an in-wire from
> `D`.)

*Proof.* Notation as in H1: terminals, `τ`, regions (the region of a terminal `p` is the in-tree
of nodes `u` with `τ(u) = p`; its leaves are wires leaving other terminals). Fix `r = 8`.

**(a) Inputs of fan-out 0.** `A = {i}`, `W = ∅`: the function ignores `x_i`. Sparse.

**(b) Merging.** Let `M` be the number of inputs that share their terminal with another input. If
`M ≥ r²`, either one region contains `r + 1` inputs or `r` regions contain two each. Take those
inputs as `A` and their terminals as `W`. In the first case `q = 1` and `σ ≤ 2r + 1`; in the
second `q = r`, `|A| = 2r`, `σ_k = 3`. Both are sparse for `r = 8`. Otherwise treat these fewer
than `r²` inputs, and their terminals, as exceptional.

**(c) Counting.** As in H1, with `Q` the non-output terminals of the remaining inputs, `Q₂ ⊆ Q`
those of fan-out 2, and ports `P` = the output, the other non-output terminals, `Q∖Q₂`, and the
exceptional terminals: `|P| ≤ v + 2r²` and `|Q₂| ≥ n − v − 2r²` (the count of H1, with fewer than
`r²` inputs removed). The number of wires leaving
terminals is at most `n + t` plus the number of terminals, so at most `4v + 6r²` wires leave
ports. Call an input *good* if `τ(i) ∈ Q₂`, and *simple* if moreover its fan-out is 2 (so
`τ(i) = i`). A good input that is not simple has a non-trivial region, which receives at least one
wire from a terminal.

**(d) Type 0** (good, both out-wires of `τ(i)` enter regions of `Q₂`-terminals). If there are at
least `5r` such inputs, `r` of them, `I`, are pairwise not targets of each other (each has two
targets, so the conflict graph is 4-degenerate). Let `J` be the inputs whose regions they enter.
`A = I ∪ J`, `W = {τ(j) : j ∈ J}`, `|A| − q = r`. The only terminals in `D∖W` are `τ(i)`, `i ∈ I`,
so `σ ≤ 7r`, and `(7r + 1)2^q + 1 ≤ 2^{q+r}`. Sparse.

**(e) Type 1** (good, one out-wire enters the region of a `Q₂`-terminal `τ(j(i))`, the other the
region of a port `p(i)`). The map `i ↦ j(i)` has a 3-colouring with no `i` and `j(i)` of the same
colour. If there are at least `3(|P| + r)` type-1 inputs, one colour class has `|P| + r`, and it
contains a set `I` with `|I| ≤ 2r` that uses at most `|I| − r` ports. Let `J = j(I)`.
`A = I ∪ J`, `W = {τ(j)} ∪ p(I)`, `|A| − q ≥ r`, `σ ≤ 6|I| ≤ 12r`, and `2^r ≥ 12r + 2`. Sparse.

**(f) The clean graph.** Otherwise there are fewer than `5r` type-0 and `3(|P| + r)` type-1
inputs. Non-simple good inputs number at most (wires from ports) + 2·(type 0) + (type 1). So at
least `n − 11v − O(r²)` inputs are simple with both wires entering port regions. They are the
edges of a multigraph `Γ_c` on at most `v + 2r²` ports, of density at least `20K` for large `n`. As in H1,
pass to a subgraph of minimum degree `δ ≥ 24`. If a breadth-first ball `B_D` spans at most 5
non-tree edges then `δ|B_{D−1}| ≤ 2|B_D| + 8`, which gives `|B_D| ≥ (δ/4)^D`. So some ball of
radius `D₀ ≤ log n/log(5K) + 1` spans 6 non-tree edges. These and the tree paths to the root form
`U` with `|E(U)| = |V(U)| + 5` and at most `12 D₀ + 6` edges; delete vertices of degree 1.
`A = E(U)`, `W = V(U)`. Inside the region of a port `p`, `D` is the tree spanned by the
`deg_U(p)` entering wires and the root, with at most `2 deg_U(p) − 1` segments, all with
`k(S) = p`. Since `Σ_p (deg_U(p) − 2) = 10`,
`Σ_k σ_k 2^k ≤ 23·2^q + 3·2^q`, and `26·2^q + 2^q + 1 ≤ 2^{q+5}`. Sparse. ∎

Theorem 4 is Lemma 6 plus Corollary 5.1. For Corollary 4.1, a `T`-secure family must have
`n^{O(a)} > T`, so `log K ≤ O(1 + log² n/log T)` and `t + 3 > n/(40K)`.

*Consistency with the known constructions.* FLY's `2n + o(n)` PRF falls under case (f) with
`K = Θ(log n)`: the test takes time `2^{O(log² n/log log n)}`, above the security FLY claim. For
that linear circuit the test amounts to guessing a short cycle of the graph.

## 5. Open

1. **The constant for strong security.** This note gives `(2 + Ω(1))n`. `three-n-bound.md` claims
   `3n − o(n)`, matching FLY's non-uniform `3n + o(n)`; that note is unreviewed.
2. **[open] Unconditional upper bound?** The upper bound needs one-way functions; the lower bound
   does not.
3. **[open] Other models.** The argument counts wires in B₂ circuits and transfers to AC⁰[2]
   wires. FLY's TC⁰ bounds are a different regime.
