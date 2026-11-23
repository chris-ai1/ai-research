# One-sided randomized circuits for sparse MCSP

Let $N=2^n$. Consider a distribution on arbitrary fan-in-two Boolean circuits, each with at most $G$ gates, unrestricted fanout, free constants and free complemented wires. Suppose every truth table of circuit size greater than $s$ is rejected with probability one, and every table of size at most $s$ is accepted with probability at least $p>1/2$.

**Theorem.** Writing $A_s$ for the set of tables of size at most $s$, we have

$$
G\ge 2N-2\lfloor\log_2|A_s|\rfloor-1.
$$

In particular, exact $\mathrm{MCSP}[s]$ needs $(2-o(1))N$ gates throughout $0\le s=o(N/n)$, even at constant completeness $p=2/3$. At $s=n^2$ the explicit estimate is $2N-(4+o(1))n^2\log_2 n$ gates. The same finite bound holds for membership in any nonempty complement-closed family $A$ on $N$ bits upon replacing $A_s$ by $A$.

## Fixing one seed on the teaching projection

Choose a table $L\in A$ and a nonempty set $J$ of at most $\lfloor\log_2|A|\rfloor$ positions whose labels uniquely identify $L$ within $A$. Such a pair exists by repeatedly choosing a distinguishing position and retaining its smaller nonempty side. Complement closure makes the opposite labels on $J$ teach $\overline L$.

On $J$ use the signed bits $L_i\oplus v$ of one input $v$. At every other position use $L_i\oplus v_i$ for its own input $v_i$. This is the deterministic teaching projection onto the all-equal predicate $\mathrm{EQ}_d$ on $d=N-|J|+1$ bits. Its two constant inputs map to $L$ and $\overline L$. Every other input matches one of them on $J$ and differs somewhere else, hence lies outside $A$. [Deterministic teaching projection and circuit census](../deterministic/main.tex)

A seed accepts both $L$ and $\overline L$ with probability at least $2p-1>0$. Almost surely it rejects every negative input simultaneously, since there are finitely many. Some seed thus computes $\mathrm{EQ}_d$ exactly on the projection, which adds no gates. For $d\ge2$, Schnorr's exact $2d-3$ bound proves the theorem. At $d=1$ the stated lower estimate is trivial. The rooted circuit census gives $\log_2|A_s|=o(N)$ when $s=o(N/n)$ and $\log_2|A_s|\le(2+o(1))n^2\log_2 n$ at $s=n^2$. [C. P. Schnorr, The combinational complexity of equivalence](https://doi.org/10.1016/0304-3975(76)90073-6) · [Circuit count](../deterministic/main.tex)

The same argument applies to the gap promise $C(f)\le s$ versus $C(f)>t$ if $L$ has size at most $s$ and $J$ teaches it among **all** tables of size at most $t$. Every nonconstant projected input is then a promised negative. In particular the deterministic manuscript's additive-gap bound $2N-2|J|-1$ for its constructed teaching sets carries over at the same completeness and perfect soundness. [Promise teaching sets and their sizes](../deterministic/main.tex)

## The completeness threshold on all-equal

For $d\ge2$, the minimum size for $\mathrm{EQ}_d$ with perfect soundness and pointwise completeness $p$ is exactly

$$
\begin{cases}
d-1 & 0<p\le1/2,\\
2d-3 & 1/2<p\le1.
\end{cases}
$$

For $p\le1/2$ choose uniformly between testing for the all-zero input and testing for the all-one input. Each minterm costs $d-1$ gates. Conversely some seed accepts at least one constant input and rejects every nonconstant input. Flipping any one bit of that accepted input shows that all $d$ inputs are essential, which needs at least $d-1$ binary gates. For $p>1/2$ the common-seed argument and the deterministic all-equal circuit give equality.

## Allowing false positives on the projection

A single teaching projection has a different limit for two-sided pointwise error. Fix an integer $b\ge2$, and first let $d=bm$ with $m\ge2$. Partition the positions uniformly into $m$ blocks of size $b$. Accept when each block is constant. The two constant inputs always pass, and the circuit for each partition uses at most

$$
m(2b-3)+(m-1)=2d-2d/b-1
$$

gates. Within each block compare the other $b-1$ inputs to the first and conjoin the results. One final conjunction checks all blocks.

For an input of weight $bk$ the probability of acceptance is $P_k=\binom mk/\binom d{bk}$, since its set of ones must be a union of whole blocks. An input of any other weight has acceptance probability zero. The maximum over nonconstant inputs is exactly

$$
P_1=P_{m-1}=\frac1{\binom{d-1}{b-1}}.
$$

Indeed $P_k=P_{m-k}$ and the consecutive ratio is
$P_{k+1}/P_k=\prod_{j=1}^{b-1}(bk+j)/(b(m-k-1)+j)$, at most one for $2k+1\le m$. For arbitrary large $d$, repeat one input until $d'=b\lceil d/b\rceil$ positions are present. This preserves both constant and nonconstant inputs. The size is at most $2(1-1/b)d+O(b)$ and the false-positive probability at most $1/\binom{d'-1}{b-1}$.

For example, on even $d$ a random perfect matching uses $d-1$ gates and errs with probability at most $1/(d-1)$ on each nonconstant input. For every fixed $a>0$, choosing a fixed $b>a+1$ gives error at most $d^{-a}$ for all sufficiently large $d$, with a leading gate coefficient strictly below two. Thus a lower bound obtained solely from $\mathrm{EQ}_{N-o(N)}$ cannot give $(2-o(1))N$ gates for randomized MCSP at any fixed inverse-polynomial two-sided error. The existing small-error MCSP proof also tests other hard tables. [Probabilistic MCSP manuscript](main.tex)

## Optimality among tests that compare within blocks

Suppose each seed accepts exactly the inputs constant on the blocks of some partition. The block sizes, the distribution over partitions, and the circuits realizing their predicates may be arbitrary. For $2\le b\le d$ and worst-case false-positive probability $\varepsilon$, every such distribution has maximum gate count

$$
G\ge 2(1-1/b)d-1-2\varepsilon\sum_{k=1}^{b-1}(1-k/b)\binom dk.
$$

For a seed with $c$ blocks, identify one representative from each block with a single input. Its predicate becomes $\mathrm{EQ}_{d-c+1}$, so its circuit needs at least $2(d-c)-1$ gates (trivially also when $c=d$). Write $c_k$ for the number of blocks of size $k$. A fixed weight-$k$ input is accepted whenever its set of ones is an entire block. Summing over inputs gives $\mathbb E c_k\le\varepsilon\binom dk$ for $0<k<d$. Since $c-d/b=\sum_k(1-k/b)c_k$, discarding the nonpositive terms for $k\ge b$ and taking expectations proves the bound.

In particular, at error $d^{-a}$ for any fixed **noninteger** $a>0$, the optimal leading coefficient in this class is $2-2/b$ with $b=\lfloor a\rfloor+2$. The correction in the lower bound is $O(d^{b-1-a})=o(d)$, and uniform blocks of size $b$ attain the error target. For example, at error $d^{-3/2}$ the optimal size is $(4/3+o(1))d$ among all such tests.
