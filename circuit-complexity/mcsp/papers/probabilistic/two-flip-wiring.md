# A three-halves gate lower bound for small-threshold randomized MCSP

Let $N=2^n$. For every integer $0\le s\le n-3$, probabilistic circuits deciding exact $\mathrm{MCSP}[s]$ with pointwise two-sided error $e=o(1/N)$ require **$(3/2-o(1))N$ gates**. At error $1/N$ they require **$(9/8-o(1))N$ gates**. The basis contains all binary Boolean gates, with free negations, constants and unrestricted fanout. Size is the maximum gate count of a circuit in the distribution.

The lower bound uses the constant tables and the $n$ raw literal tables. A circuit that accepts them and rejects their one-bit changes must transmit the value of each tested position through its private path. A second test on two-bit changes forces the signals on some of those paths to agree across all the accepted tables. The literal tables distinguish every pair of positions, limiting how often the same wire can supply the needed value.

The existing probabilistic manuscript proves $2N-O(N/n+eN^2+N\sqrt{eN})$ gates for $n-2\le s\le c_0N/n$ for an absolute $c_0>0$. Together the two bounds give at least $(3/2-o(1))N$ throughout $0\le s\le c_0N/n$ at $e=o(1/N)$. At small thresholds the known upper bound at error $N^{-a}$, for fixed $0<a<1$ in its stated range, is $(1+o(1))N$. [Probabilistic MCSP manuscript](main.tex) · [Small-threshold randomized upper bound](https://github.com/chris-ai1/ai-research/pull/15)

## Cutting a circuit at its branching vertices

Consider a circuit on $d$ bits accepting a list of centers that includes $0^d$ and $1^d$. The **profile** of a wire is its vector of values on the centers. Let $b_1$ be the number of input positions for which flipping that bit at some center is also accepted. Let $b_2$ be the number of unordered pairs for which flipping both bits at $0^d$ is accepted. Delete these $b_1$ positions from consideration and one endpoint of each of the $b_2$ pairs. The remaining marked set $X$ has $|X|\ge d-b_1-b_2$. A marked single flip is rejected at every center, and a marked double flip is rejected at zero.

Trim the circuit to its output, absorbing unary gates and constants. Write $d'$ for the number of raw inputs used and $g$ for the gate count. We have $d'\ge d-b_1$. Define $E=g-d'+1$. Counting the $2g$ gate inputs shows that $E$ is the sum of outdegree minus one over all nonoutput vertices. A branching vertex has outdegree at least two. If there are $R$ branching raw inputs and $B$ branching gates, then $R+B\le E$ and at most $2E$ edges leave branching vertices. A constant output satisfying the hypotheses has $b_1=d$ and gives the bounds below trivially.

Cut each outgoing edge of every branching vertex, leaving a new formal leaf at its destination. The resulting components are binary trees rooted at the branching vertices and the output. A branching raw input is a one-vertex tree. Each marked raw occurs at its own original vertex once. Every other leaf in the trees is a cut edge or an unmarked raw, so there are at most $2E+d'-|X|$ such leaves. A marked raw in a tree cannot affect any incoming cut signal in that tree. Its only path out passes through the root, and a path back into the tree would give a cycle. This decomposition uses the critical paths of Chen, Li and Yang. [Chen, Li and Yang, CCC 2022, §4.4](https://doi.org/10.4230/LIPIcs.CCC.2022.23)

In a tree with at least two marked raws, follow a marked leaf $i$ up to its first gate $G$ whose other input subtree also contains a marked raw $j$. Flipping either $i$ or $j$ alone at a center must toggle its own input signal to $G$ and change $G$. The opposite subtree is unaffected. At zero, flipping both therefore toggles both signals. If $G$ were XOR or XNOR, its value and the final output would be unchanged, contradicting rejection of the double flip. Every other essential binary gate has just one input pair at which both single flips change its output. Consequently $G$ receives this same pair at **every** center.

In particular the signal arriving from the $i$ side is constant across the centers. The raw $i$ changes between the two constant centers, so the part of its path strictly below $G$ must use at least one other leaf. The leaves on these exclusive parts are disjoint for different marked raws: every subtree counted here contains exactly its one marked raw. Call the other leaves used by this part its auxiliary leaves.

If there is exactly one auxiliary leaf, the signal going into $G$ is a single binary gate on $i$ and that leaf. It must transmit a flip of $i$ at every center. For a nonlinear gate this forces the partner to its unique noncanalizing value at every center, giving a fixed signed copy of $i$ as output. That output varies. Thus the gate is XOR or XNOR, and the auxiliary leaf has the profile of $i$ up to complementation.

**Counting with distinct input profiles.** Suppose all $d$ raw profiles are distinct up to complementation. A marked raw with only one auxiliary leaf must obtain it from an internal branching gate. An original raw or a cut copy of a different raw has the wrong profile, and $i$ has only its one outgoing edge. A given branching gate can serve in this way for at most one $i$. If $U$ marks occur in trees with at least two marks, their exclusive parts therefore consume at least $2U-B$ auxiliary leaves.

Write $S_r,S_g$ for the numbers of marks in single-mark trees rooted at a raw and at a gate, respectively. We have $S_r\le R$ and $S_g\le B+1$, counting the output. Every single-mark tree rooted at a gate has at least one other leaf. These leaves are disjoint from the auxiliary leaves already counted. Thus

$$
 2U-B+S_g\le 2E+d'-|X|,
 \qquad |X|=U+S_r+S_g .
$$

It follows that $3|X|\le 2E+d'+B+2S_r+S_g\le 4E+d'+1$. Substituting $g=d'-1+E$ gives

$$
\boxed{\displaystyle
g\ge\frac{3d'+3|X|-5}{4}
 \ge \frac{6d-6b_1-3b_2-5}{4}.}
$$

## Applying the count to MCSP

Take as centers the two constants and the $n$ projections $a\mapsto a_j$. Each has inner size zero. The profiles at two distinct addresses differ on some projection, and the row for the zero table precludes complementary profiles.

A one-entry change to a constant needs all $n$ inner variables. A one-entry change to a projection still needs all of them for $n\ge2$. Along its own axis there is an unaffected edge witnessing dependence, and along each other axis the changed entry witnesses dependence. A two-entry change to zero needs at least $n-1$ variables, since independence of two axes would make its weight a multiple of four. Connectedness forces at least $n-1$ gates for the singleton changes and $n-2$ gates for the double changes. All are hard when $s\le n-3$.

A random seed accepts all $n+2$ centers with probability at least $1-(n+2)e$. Unconditionally $\mathbb E b_1\le(n+2)Ne$ and $\mathbb E b_2\le\binom N2e$, counting acceptance on the designated changed inputs. Conditioning on accepting the centers and averaging the boxed inequality gives, whenever $(n+2)e<1$,

$$
G\ge\frac{6N-5}{4}
-\frac{\bigl(6(n+2)N+3\binom N2\bigr)e}{4(1-(n+2)e)} .
$$

At $e=c/N$ for fixed $c>0$ this is $(3/2-3c/8-o(1))N$. Taking $c=1$ or taking $e=o(1/N)$ gives the two claimed bounds.

## How far the two constant inputs alone can go

For the all-equal predicate $\mathrm{EQ}_d$, only the two constants are centers and every raw has the same profile. The same proof still charges one auxiliary leaf for each of the $U$ marks. The number of single-mark trees is at most $E+1$, so $|X|\le (2E+d'-|X|)+(E+1)$. Hence

$$
g\ge\frac{2d'+2|X|-4}{3}
 \ge\frac{4d-4b_1-2b_2-4}{3}.
$$

For $d\ge3$ and pointwise error $e$, some seed accepts both centers and has $4b_1+2b_2\le(8d+2\binom d2)e/(1-2e)$ when $e<1/2$. Thus every unrestricted probabilistic all-equal circuit has size at least $(4/3-o(1))d$ for $e=o(1/d)$. A uniform random partition into triples gives size $4d/3+O(1)$ and error $O(d^{-2})$. In particular the optimal size is $(4/3+o(1))d$ at $e=d^{-a}$ for every fixed $1<a<2$. All-equal on $N-o(N)$ inputs is a teaching projection of sparse MCSP. The extra literal centers in MCSP give the larger coefficient above. [Teaching projection](../deterministic/main.tex) · [Random block tests](https://github.com/chris-ai1/ai-research/pull/14)

There is also a sharp bound at $e=c/d$ for fixed $c>0$. The last inequality gives $(4/3-c/3-o(1))d$. Any seed accepting zero ignores at least $d-G-1$ positions and accepts the corresponding single flips. Summing their error probabilities gives the additional bound $G\ge d(1-e/(1-e))-1$. Together these attain the leading coefficient $\max\{1,(4-c)/3\}$ from below.

For the matching upper bound, take a uniformly permuted partition with $h$ blocks of size two and $m$ of size three, where $2h+3m=d$. Check equality within every block and conjoin the checks, using $2d-2(h+m)-1=(4d-2h)/3-1$ gates. Both constants pass. Weight two passes with probability $h/\binom d2$.

Uniformly over $h,m$, every weight $3\le k\le d/2$ passes with probability $O(d^{-2})$, and complementation handles the other half. A weight-three input passes exactly when its ones comprise a triple, of probability $m/\binom d3$. For $k\ge4$, expose the block of a remaining one until all ones are covered or a block is mixed. At each step, even a single partner must be a remaining one, of conditional probability at most $(k-1)/(d-1)$. After a monochromatic block the ratio can only decrease. At least $\lceil k/3\rceil$ successful steps are needed. For $4\le k\le6$ two steps suffice for the bound, for $7\le k\le12\log_2 d$ use three, and above this range each step succeeds with probability at most $1/2$. Weight one always fails.

Choose the greatest feasible $h\le\min\{d/2,(c/d)\binom d2\}$. The congruence changes it by at most two from the integer cutoff for large $d$. This gives error at most $c/d$ and size $(\max\{1,(4-c)/3\}+o(1))d$. Taking the least feasible $h\in\{0,1,2\}$ gives the triple bound used above for $e=d^{-a}$.

The finite checker tests the gate inequalities on four-input functions, verifies all the designated MCSP labels at $3\le n\le6$, and enumerates partitions into pairs and triples through ten inputs. [Reproduce the finite checks](check_two_flip_wiring.py)
