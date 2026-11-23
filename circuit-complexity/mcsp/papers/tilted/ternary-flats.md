# What affine tests can certify about three-choice pairs

A common output at a private AND-type gate leaves three possible input pairs. Could a dense affine hitting theorem alone give credit for all $\log_2 3$ bits of freedom in each pair? The obstruction already occurs on a single elimination path. A sparse set can pass every affine test up to the rate used in the MCSP argument and still miss the whole path. There is also a counterexample built from linear encoders whose projections usually have full rank. [Tilted elimination argument](main.tex) · [Dense affine law](../dense-circuits/main.tex)

Let $S$ fix $h$ single bits, allow three out of four patterns on each of $k$ disjoint pairs, and leave $f$ other bits free in $\mathbb F_2^N$, where $N=h+2k+f$. Its uniform mass is $2^{-h}(3/4)^k$. Write $m=h+k$, and let $U$ be uniform on the cube. All conclusions about flat intersections also hold after any invertible affine change of coordinates.

## The exact extremum

Over all affine flats $F$ of codimension $r$, the maximum of $U(S\mid F)$ is

$$
\begin{cases}
2^{-(h-r)}(3/4)^k & 0\le r\le h,\\
(3/4)^{m-r} & h\le r\le m,\\
1 & m\le r\le N.
\end{cases}
$$

On $F$ let $j$ be the rank of the $h$ prescribed bits. If they are consistent, imposing them costs probability $2^{-j}$ and leaves dimension $N-r-j$. The projection of this fiber onto the $k$ pairs has dimension at least $h+2k-r-j$, since the free block has size $f$. Reveal the pairs in order. Each pair adds zero, one or two to the prefix projection rank. At least $(m-r-j)_+$ pairs must add two. Conditional on every feasible preceding prefix each such pair is uniform on its four patterns, so the conditional success probability is at most $(3/4)^{(m-r-j)_+}$. The product with $2^{-j}$ decreases in $j$, and $j\ge(h-r)_+$.

Equality holds by spending rank first on the prescribed bits, then on allowable lines in distinct pairs. After $m$ restrictions the resulting flat lies inside $S$ and can be restricted further. In particular, leaving $t$ of those $m$ ranks unused makes the maximum density at most $(3/4)^t$.

## A sparse law with the truth-table symmetries

Let $\mathcal G$ be any group of affine permutations with $\log_2|\mathcal G|=o(N)$, and take $m,k=\Theta(N)$. This includes permutations and bit flips of the $n=\log_2 N$ address inputs and complementation of the table output. There is a $\mathcal G$-invariant distribution supported on at most $2^{m+o(N)}$ points which misses every translate $gS$ for $g\in\mathcal G$. It assigns $(1+o(1))U(F)$ to every flat of codimension at most $m-t_N$, for some $t_N=o(N)$.

Choose $t_N$ at least $10\log_2 N$ with $|\mathcal G|(3/4)^{t_N}\le N^{-10}$. On every flat in this range, the conditional mass of the entire orbit union is at most $N^{-10}$ by the extremum and a union bound. Conditioning uniform measure outside the union therefore changes each flat probability by a relative $O(N^{-10})$. Draw $2^m$ independent points from the conditioned law. Each flat expects at least $(1-o(1))2^{t_N}$ hits, so Chernoff bounds give relative error $o(1)$ simultaneously for the at most $2^{N(N+1)}$ affine tests (relative error $1/N$ suffices). Average the empirical law over the group. Its support grows by at most $|\mathcal G|$, its estimates persist, and the orbit union remains empty.

## A counterexample using linear encoders

Here take $f=0$, $h\ge1$, and write a table as $(z,a,b)$ with $z\in\mathbb F_2^h$ and $a,b\in\mathbb F_2^k$. Prescribe $z=e_1$, and forbid $a_i=b_i=1$ on each pair. An ensemble of linear spaces of dimension $m-1$ misses this $S$. For every fixed test matrix of rank $r$, its restriction to a sampled space has full rank except with probability at most $8\cdot2^{r-m}$.

Choose a uniform alternating binary $k$-by-$k$ matrix $M$ (symmetric with zero diagonal), and an independent uniform nonzero vector $c$. Take any $t$ with $c\cdot t=1$, and put

$$
L=\{(w,Mw):c\cdot w=0\},\qquad v=(t,Mt+c).
$$

Throughout $v+L$ one has $b=Ma+c$ and $a\cdot c=1$, so $a\cdot b=1$. This forces a forbidden pair. To make the whole encoder linear, choose an independent uniform binary matrix $T$ with $2k$ rows and $h-1$ columns. Use the image

$$
\{(z,\ z_1v+T(z_2,\ldots,z_h)+u):z\in\mathbb F_2^h,\ u\in L\}.
$$

It has dimension $m-1$. Its slice $z=e_1$ uses exactly $v+L$.

A nonzero pair of dual vectors $(s,d)$ annihilates $L$ precisely when $s+Md\in\{0,c\}$. For $d=0$ this has probability $1/(2^k-1)$. For $d\ne0$, the vector $Md$ is uniform on $d^\perp$. Indeed, for any desired output in $d^\perp$, choose an index where $d$ is one and use only the corresponding row and column of $M$ to realize that output. The probability of annihilating $L$ is thus at most $2^{1-k}+1/(2^k-1)\le4\cdot2^{-k}$. For a nonzero functional on the whole table with a nonzero pair part, the $h-1$ random columns of $T$ impose another independent factor $2^{-(h-1)}$. A nonzero functional supported only on $z$ cannot vanish on the image. A union bound over the nonzero rows in a rank-$r$ row space proves the full-rank estimate.

One can keep only $N^3$ independent encoders. For any rank $r\le m-\lceil10\log_2 N\rceil$, the expected failure fraction is at most $8N^{-10}$. The binomial bound for a failure fraction above $1/N$ is at most $(8eN^{-9})^{N^2}$, so some list works for every such test simultaneously. Its union has size at most $N^3 2^{m-1}$ and avoids $S$. Choosing a uniform encoder and a uniform message gives at least $(1-1/N)2^{-r}$ probability to each rank-$r$ syndrome.

The information cost of specifying the path is $h+k\log_2(4/3)$, strictly below $m$ by $k\log_2(3/2)$. These examples show why a proof using that saving needs a property of actual small address circuits or of the elimination paths producing the tests.
