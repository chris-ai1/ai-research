# Isolating a prescribed pattern on an arbitrary block

Fix the inner threshold $s$ and specify a block of truth-table bits. On that block one can obtain every minterm as a restriction of exact MCSP, up to a block size asymptotic to the logarithm of the number of accepted tables.

Write $N=2^n$, and let $A_s$ be the set of truth tables of circuits on $n$ inputs with at most $s$ gates over the full binary basis, with free constants and complemented wires. For a nonempty class $A$ of tables define $I(A)$ as the largest $q\le N$ with the following property. For every set $Q$ of at most $q$ positions and every labeling $b$ of $Q$, there is a fixing of the positions outside $Q$ for which $b$ is the **unique** accepted assignment on $Q$. The fixing may depend on both $Q$ and $b$.

**Theorem.** Put $T=s\log_2 s$. If $n=o(s)$ and $T^3=o(N)$, then

$$
I(A_s)=(1+o(1))T.
$$

In particular this holds at $s=n^2$, with $I(A_s)=(2+o(1))n^2\log_2 n$. One can prescribe some of the positions in $Q$ in advance and leave the rest free. Isolate the combined labeling and then fix the prescribed positions.

## A periodic extension gives an isolated labeling

Index the positions by $\mathbf F_2^n$. Suppose a class $A$ is invariant under address translations. Let a linear map $M$ be injective on $Q$, and suppose some table $f(x)=h(Mx)$ in $A$ realizes $b$ on $Q$. If

$$
|\ker M|>\log_2 |A|,
$$

then $b$ can be isolated on $Q$.

Indeed, the sets $Q+t$ for $t\in\ker M$ are pairwise disjoint. If $x+t=y+u$ with $x,y\in Q$, applying $M$ gives $Mx=My$, hence $x=y$ and $t=u$. On each copy, $f$ carries the translated labeling $b$.

Suppose isolation fails. Every accepted table matching $b$ on $Q$ then has a second accepted table agreeing everywhere outside $Q$ and differing somewhere on $Q$. Translation invariance gives the same rule on each copy. Starting at $f$, choose any subset of the copies and apply the rule once on each chosen copy. Earlier changes leave all later copies available. The final table records the chosen subset exactly as the copies where it differs from $f$. This gives at least $2^{|\ker M|}$ accepted tables, a contradiction. The starting table need not itself be an isolating witness.

## The size of the block

Fix $0<\delta<1$ and set $q=\lfloor(1-\delta)T\rfloor$. It suffices to handle blocks of exactly $q$ bits, since any smaller labeled block can be extended to size $q$ and the extra bits fixed after isolation. For a given block $Q$, choose a binary linear hash with $r=\lceil 2\log_2 q\rceil$ output bits. Two different addresses collide with probability $2^{-r}$ for a uniformly random matrix, so the expected number of colliding pairs on $Q$ is less than one. Fix an injective choice on $Q$.

The hash costs $o(s)$ gates throughout $n=o(s)$. For $s>n^2$ use the direct $O(n\log s)$ construction. For $s\le n^2$, there are $O(\log n)$ parity outputs. Partition the output rows into a constant number of groups of size at most $\lfloor(\log_2 n)/2\rfloor$. Within each group, sum the input bits having the same column pattern. These sums cost at most $n$ gates. Each output combines at most $\sqrt n$ sums, so the total cost over the groups is $O(n)$.

On the $q$ points of $M(Q)$, prescribe the labels $b$. Chashkin's partial-function synthesis theorem in the full binary basis extends these labels to a function $h$ on $r$ inputs of size at most

$$
(1+o(1))\frac{q}{\log_2 q}+O(r)=(1-\delta+o(1))s.
$$

Here $r=O(\log q)$, $\log q\sim\log s$, and the synthesis bound holds on an arbitrary domain of size $q\ge r$ for every choice of labels. Thus the composite table $h(Mx)$ belongs to $A_s$. The rooted circuit census gives $\log_2|A_s|\le (s+1)\log_2(n+s+2)+O(s+\log(s+2))=(1+o(1))T$. [Deterministic manuscript, Theorem 1](../../results/mcsp/papers/deterministic/main.pdf)

The hash leaves enough disjoint copies for the isolation argument, since

$$
|\ker M|\ge N/2^r\ge N/(2q^2)\gg T .
$$

Complemented input wires make $A_s$ invariant under address translations. The periodic-extension argument now isolates $b$. Since $\delta$ was arbitrary, $\liminf I(A_s)/T\ge 1$. Conversely, even realizing every labeling on one $p$-bit block requires $2^p$ different accepted tables. Hence $I(A_s)\le\log_2|A_s|$, which proves the matching upper bound.

The quadratic loss in the number of disjoint translates can occur for an actual block. Take complementary $d$-dimensional subspaces $U,V$ of a $2d$-dimensional address subspace $H$, and set $Q=U\cup V$. Then $q=2^{d+1}-1$ and $Q+Q=H$. Two translates of $Q$ meet exactly when their offsets belong to the same coset of $H$. Thus a largest disjoint family has exactly $N/2^{2d}=4N/(q+1)^2$ copies, even if every address translation is available. For blocks of size comparable with $T$, obtaining more than $\log_2|A_s|$ disjoint translates by this argument runs into the cubic scale. The size of an isolatable block beyond that scale remains open here.

## A communication consequence

Give Alice any $p\le I(A_s)$ positions and Bob the rest. Their $0$-$1$ communication matrix contains the $2^p$-dimensional identity as a submatrix. For each possible row $b$, use the outside fixing that isolates it as the corresponding column. The ordinary rank over **every** field is therefore exactly $2^p$. Exact deterministic communication costs precisely $p$ bits when Bob outputs the answer. Each accepting rectangle covers at most one diagonal entry of this identity, and Alice can send her entire row.

## Sources and verification

The extension to previous signed identifications and to affine spaces of allowed changes recovers isolated patterns in residual MCSP circuits. [Isolation after signed identifications](signed-isolation.md)

The disjoint-translate argument comes from Samuel Schlesinger's *Structure from optimality* research notes, where decision-tree interpolation gave blocks of order $n^2$ at $s=n^2$. The improvement here uses A. V. Chashkin's partial synthesis bound on the **hashed** domain. The deterministic manuscript uses the same synthesis theorem for teaching sets. The outside fixing in the present argument is existential. [Chashkin, Theorem 6.1 (2024)](https://library.keldysh.ru/mvk.asp?id=2024-152&lg=e)

[LocalIsolation.lean](formal/LocalIsolation.lean) checks the combinatorial step that maps each subset of disjoint copies to a distinct accepted table under the stated change rule. The hash, synthesis and circuit estimates are the written argument above.
