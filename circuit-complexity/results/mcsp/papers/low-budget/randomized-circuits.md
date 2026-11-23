# The gate cost of randomized MCSP at small thresholds

Let $N=2^n$ and fix $0<\gamma<1$. Suppose $0\le s\le(1-\gamma)n/\log_2 n$. Let $G_{p,e}$ be the least maximum size of a distribution on full-binary-basis circuits that accepts each table in $\mathrm{MCSP}[s]$ with probability at least $p$ and each table outside it with probability at most $e$. Constants and complemented wires are free. The distribution may choose the wiring, as in the repository's probabilistic model. [Probabilistic MCSP manuscript](../probabilistic/main.tex)

**Theorem.** For any fixed $0<e<p\le1$,

$$
G_{p,e}=\bigl(1-e/p+o(1)\bigr)N.
$$

In particular, ordinary pointwise error $1/3$ costs $(1/2+o(1))N$ gates. Requiring perfect completeness while retaining false-positive probability $1/3$ costs $(2/3+o(1))N$ gates. There is also a vanishing-error range. For fixed $0<a<1$ and $0<\gamma<1-a$, if $s\le(1-a-\gamma)n/\log_2 n$, the optimal size at pointwise error $N^{-a}$ is $(1+o(1))N$, even if perfect completeness is required.

## A lower bound from one-bit changes

The all-zero table is easy. Changing it at any one address gives a point function depending on all $n$ inner inputs, which needs at least $n-1$ binary gates. Thus every one-bit neighbor of zero is hard in the stated range for large $n$.

A fixed $G$-gate outer circuit depends on at most $G+1$ table positions, by connectedness of the graph reaching its output. If it accepts the zero table, it accepts at least $N-G-1$ one-bit neighbors as well. Write $P\ge p$ for the probability of accepting zero. If $G<N-1$, summing the false-positive probabilities over the $N$ neighbors gives $Ne\ge P(N-G-1)\ge p(N-G-1)$. For $G\ge N-1$ the resulting estimate holds immediately. Hence at every integer $0\le s<n-1$,

$$
G\ge(1-e/p)N-1.
$$

## Testing a small, separated set of tables

Write $A=A_s$, $M=|A|$, and $\Delta$ for the least Hamming distance between distinct members of $A$. Two estimates control the upper bound.

- The rooted circuit census gives $\log_2 M\le(s+1)\log_2(n+s+2)+O(s+\log(s+2))$. In the fixed-error range $M\le N^{1-\gamma+o(1)}$. [Rooted circuit count](../deterministic/main.tex)
- Each $s$-gate function depends on at most $s+1$ inner variables. Two distinct such functions differ on at least one assignment of their combined variables. All extensions of that assignment witness disagreement, so $\Delta\ge2^{n-2s-2}=N^{1-o(1)}$ in this range.

Put $\lambda=1-e/p$. Sample a uniform set $J$ of $t=\lceil(\lambda+1/n)N\rceil$ table positions. For large $n$ we have $t\le N$. On those positions test whether the input agrees with some member of $A$, using the fingerprint below.

Fix a hard input $x$ and choose its nearest member $u\in A$. The probability that $J$ misses all differences from $u$ is at most $1-t/N$, since there is at least one. Every other member differs from $x$ in at least $\Delta/2$ positions by the triangle inequality and the choice of $u$. A discrepancy set of size $h$ is missed with probability at most $(1-t/N)^h$, by sampling without replacement. Consequently

$$
\Pr_J[x|_J\in A|_J]\le 1-t/N+(M-1)(1-t/N)^{\Delta/2}.
$$

Assign independent uniform labels $w_i\in\mathbb F_2^q$ to the $t$ sampled positions. Evaluate $H(z)=\bigoplus_{i:z_i=1}w_i$ and accept if $H(x|_J)$ belongs to the precomputed set $H(A|_J)$. For every nonzero difference the hash is uniform. On a sampled string outside $A|_J$ the additional false-positive probability is therefore at most $M2^{-q}$. Every sampled projection of an easy table passes. This is the universal hashing collision bound. [Carter and Wegman, Universal classes of hash functions](https://doi.org/10.1016/0022-0000(79)90044-8)

**Gate cost.** For a fixed seed, group the sampled input bits by their $q$-bit labels. Compute the parity in each nonempty group and then the parity for every nonempty prefix of labels, combining the two children when both are present. Together these parities use at most $t-1$ XOR gates, since every XOR combines disjoint subtrees of one tree on the $t$ leaves. For hash bit $j$, sum the parities of length-$j$ prefixes ending in one. Over all $j=1,\ldots,q$ this uses fewer than $2^q$ further XOR gates. Membership of the resulting $q$ bits in the precomputed set is an arbitrary Boolean lookup, implemented by a binary decision tree with at most $2^q-1$ three-gate multiplexers. Each seed thus uses at most $t+4\cdot2^q$ gates.

Choose $q=\lfloor(1-\gamma/2)n\rfloor$. Then $2^q=o(N)$ and $(M-1)(1-t/N)^{\Delta/2}+M2^{-q}=o(1/n)$. With probability $p$ use this tester and otherwise reject. Each easy input is accepted with probability $p$. Each hard input is accepted with probability at most $p(1-t/N+o(1/n))\le e$ for all sufficiently large $n$. The maximum size is at most $(\lambda+o(1))N$, proving the theorem.

## Inverse-polynomial error

Use every position, dispense with the initial random rejection, and put $q=\lceil\log_2(MN^a)\rceil$. Every easy table passes and every hard table passes with probability at most $M2^{-q}\le N^{-a}$. In the stated range the census gives $M\le N^{1-a-\gamma+o(1)}$, so $2^q=o(N)$. The gate count is at most $N+4\cdot2^q=N+o(N)$. The one-bit lower bound with $e=N^{-a}$ and $p=1-N^{-a}$ matches this to leading order, and also applies when perfect completeness is required.

The upper bounds count the gates of each fixed seed. Its nonuniform circuit description contains the sampled coordinates and the hash image of the easy tables.
