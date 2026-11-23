# Quadratic elimination paths can contain no affine plane

The MCSP affine synthesis theorem supplies a small circuit for a truth table in every affine space of sufficiently small codimension. One way to try to extend gate elimination to quadratic substitutions would be to find a large affine space inside each surviving path. A path with $2^{\lfloor N/10\rfloor}$ tables can already contain no affine plane. We give the construction, a version with a small circuit for path membership, and a sufficient condition under which affine synthesis still applies. [Affine synthesis](../../results/mcsp/papers/affine/main.tex)

## The substitution model

Let $N=2^n$. A path fixes distinct truth-table bits in sequence. The right-hand side of each substitution uses only bits that remain after that substitution. Allow arbitrary affine right-hand sides over $\mathbb F_2$ and signed products of two surviving bits,

$$
x_k=(x_i+\alpha)(x_j+\beta)+\gamma.
$$

After $T$ such substitutions the solution set has $2^{N-T}$ points, since every assignment to the remaining bits extends uniquely in reverse order. An affine plane consists of four distinct points $x,x+s,x+t,x+s+t$.

This product occurs in Lemma 5.3, case 4.2.2.2, of Golovnev, Kulikov, Smal and Tamaki. Their Corollary 5.4 obtains a correlation bound up to $(2.6-o(1))N$ gates under a quadratic extractor hypothesis. The second construction below realizes a plane-free path under their gate-selection rules on a small circuit. Whether such a path arises on a circuit deciding MCSP is a further question. [Gate Elimination: Circuit Size Lower Bounds and #SAT Upper Bounds, §5.2](https://www.golovnev.org/papers/gate_elimination.pdf)

## A path with no affine plane

**Proposition.** For every $N\ge 10$ there is a path with $d=\lfloor N/10\rfloor$ free bits whose solution set contains no affine plane. All product substitutions come first and their triples of raw coordinates are pairwise disjoint.

Take $m=3d$ pairs of linear forms $L_i,M_i$ on $\mathbb F_2^d$. On $d+3m=10d$ bits use the graph

$$
\Pi=\{(u,(a_i,b_i,z_i)_{i=1}^m): a_i=L_i(u),\quad b_i=M_i(u),\quad z_i=a_ib_i\}.
$$

Eliminate all $z_i$ first, then the $a_i,b_i$. Fix any padding bits to zero. Projection to $u$ is linear and one-to-one on the graph, so an affine plane in the graph would project to a plane with independent directions $s,t$. The sum of the four values of the coordinate $z_i$ on that plane is

$$
L_i(s)M_i(t)+L_i(t)M_i(s).
$$

Choose all forms independently and uniformly. For each fixed independent pair $s,t$, their evaluations give a uniform binary $2\times2$ matrix. Exactly six of its sixteen values have nonzero determinant. The probability that every coordinate misses these directions is $(5/8)^m$. There are fewer than $4^d$ ordered direction pairs. The probability of missing any pair is therefore at most

$$
4^d(5/8)^{3d}=(125/128)^d<1.
$$

Some fixed choice detects every pair. The determinant is independent of the base point, so that one choice rules out all affine planes at once.

## An accepting leaf of a small circuit

**Proposition.** For every fixed $\varepsilon>0$ there are infinitely many truth-table lengths $N=2^n$ and unrestricted full-binary-basis circuits of size at most $(1+\varepsilon)N$ with the following property. A legal choice of topological order and pivots in Lemma 5.3 gives one accepting leaf containing $2^{\Omega_\varepsilon(N)}$ points and no affine plane. This leaf is the circuit's whole accepting set.

Use a family of binary linear encoders $E:\mathbb F_2^d\to\mathbb F_2^\ell$ of constant rate, relative distance at least $\delta>0$, and linear-size encoding circuits. Spielman's construction supplies such a family. Choose each pair of forms by sampling two coordinates of $E$ independently and uniformly, with replacement. Use fresh $a_i,b_i$ in each triple, even when code coordinates repeat. [Spielman, Linear-Time Encodable and Decodable Error-Correcting Codes](https://www.cs.yale.edu/homes/spielman/PAPERS/linearTimeIT.pdf)

For independent directions $s,t$, write $v_j=(E(s)_j,E(t)_j)$. A random $j$ has $v_j\ne0$ with probability at least $\delta$ because $E(s)$ has weight at least $\delta\ell$. Fix such a $j$. A nonzero linear functional annihilating $v_j$ maps the columns $v_k$ to the codeword of a nonzero combination of $s,t$. At least a $\delta$ fraction of the $v_k$ therefore lie outside the span of $v_j$. The probability of a nonzero determinant is at least $\delta^2$. Set $m=Kd$ for a fixed integer $K$ with $4(1-\delta^2)^K<1$. The same union bound supplies a plane-free graph.

To realize the leaf, use a linear-size XOR encoder for $E$. Spielman's recursive encoding composes fixed-width linear maps at the check nodes, each implementable by a constant number of binary XORs. Omit identically zero code coordinates before sampling, which can only improve relative distance. Add one raw bit for the output of each encoder gate and one further bit $w$ with $w=u_1$. Each new coordinate is determined by $u$. Projection to the original graph is one-to-one, so these additional coordinates preserve the absence of planes. [Spielman, §§2 and 5, especially Definition 16 and Proposition 17](https://www.cs.yale.edu/homes/spielman/Research/ITsuperc.pdf)

Build the membership circuit as a chain of ANDs, starting with the equality $w=u_1$. Its successive tests are the following.

1. Check all equalities between $a_i,b_i$ and their designated raw encoder coordinates (or message bits). Use a distinct XNOR gate for each equality.
2. Check each encoder gate equation in reverse topological order. Use a separate XOR tree for each equality between a raw output and the sum of its two raw predecessors. Insert any zero-padding literal tests after these equations.
3. Check every equation $z_i=a_ib_i$, with a private AND $A_i$ for the product and a private XNOR $D_i$ comparing it with $z_i$.

There are $N_0=O(d)$ unpadded bits and $G_0=O(d)$ unpadded gates. Choose the least power of two $N$ at least both $N_0$ and $(G_0-N_0)/\varepsilon$. Each padding literal costs one more binary gate in the chain, so $G_0+N-N_0\le(1+\varepsilon)N$ and $N=\Theta_\varepsilon(d)$.

Order all product gates $A_i$ first. Each of its two inputs feeds exactly that gate and its own copy check from step 1. Both copy checks are XOR-type. The only successor of $A_i$ is the XOR-type gate $D_i$, whose other input $z_i$ has fanout one. These are exactly the hypotheses of case 4.2.2.2. Take the branch $z_i=a_ib_i$, so $D_i$ passes and its conjunction gate disappears. All other triples retain their wiring. Repeat until the product tests are gone.

The first remaining AND now combines the check $w=u_1$ on the left with the next test on the right. Every internal gate of either input tree has fanout one. The left tree contains a fanout-one input $w$, so case 3.1 permits trivializing the right test. Choose its copy bit, encoder output bit, or padding bit as the pivot. This pivot has no other remaining use, since the copy checks precede the encoder checks and the encoder checks are in reverse topological order. On the passing branch the AND disappears and $w=u_1$ becomes the left side of the next AND. Finally the affine terminal case enforces $w=u_1$. Every assignment to $u$ followed these same branches, and every accepted input satisfies all their equations. [Elimination cases 3.1 and 4.2.2.2, Lemma 5.3](https://www.golovnev.org/papers/gate_elimination.pdf)

## Which affine information survives

A small vertex cover of the product inputs gives a positive result. Form a graph with an edge $\{i,j\}$ for each product substitution. If its edges have a vertex cover of size $v$, fixing the $v$ bits in that cover makes every product affine. Each nonempty part is then defined by at most $T+v$ affine equations in the original coordinates. In particular, every point on the path lies in an affine subspace of dimension at least $N-T-v$ contained in the path. A distribution that approximates the uniform mass of every flat of codimension at most $T+v$ to relative error $\eta$ approximates the mass of the entire path to the same relative error, by summing over these disjoint parts.

For the plane-free path $\Pi$, affine tests alone can give an accurate picture of large flats while missing the entire path. In any affine $k$-flat $F$, each nonzero difference of two points of $\Pi\cap F$ comes from at most one unordered pair. Two distinct pairs with the same difference would be disjoint and would form a plane. Consequently

$$
\binom{|\Pi\cap F|}{2}\le 2^k-1,\qquad
\frac{|\Pi\cap F|}{|F|}=O(2^{-k/2}).
$$

Let $U$ be uniform on all tables. Conditioning $U$ to avoid $\Pi$ changes the mass of every $k$-flat by a multiplicative factor $1+O(2^{-k/2})$. Even a distribution with support at most $2^{cN}$ can exhibit this behavior at the ranks relevant to dense MCSP. For fixed $0<c<1$, draw $2^{\lfloor cN\rfloor}$ independent samples from the conditional law. Every flat of codimension $r\le cN-10\log_2 N$ has expected count $\Omega(N^{10})$. The multiplicative Chernoff bound with tolerance $1/N$ and a union bound over at most $2^{N(N+1)}$ flats give a single empirical distribution with mass $(1+o(1))2^{-r}$ on every such flat and zero on $\Pi$.

The unshifted graph contains the all-zero truth table, so MCSP accepts a point of this very example. The obstruction concerns the inference from affine subspaces or affine-test statistics. A transfer to MCSP could still exploit additional constraints on its own accepting or rejecting paths, choose different elimination steps, or synthesize an easy table using the quadratic equations directly.
