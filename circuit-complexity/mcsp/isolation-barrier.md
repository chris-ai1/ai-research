# A sparse language with isolated patterns and linear membership circuits

Suppose that on every specified block of at most $q$ bits, each labeling occurs as the **unique** accepted assignment for some fixing of the other bits. Call this property *isolation on $q$ bits*. It forces at least $2^q$ accepted words. It also forces an identity submatrix of order $2^q$ across every cut with a side of size $q$. How much circuit size follows from these properties?

**Theorem.** Let $N=2^n$. For each fixed $D$ and every $1\le q\le n^D$, for all sufficiently large $n$ there is a class $C\subseteq\{0,1\}^N$ with

* isolation on $q$ bits and minimum Hamming distance greater than $q$,
* closure under bitwise complement and $\log_2|C|\le q+O(\log(nq))$, and
* a deterministic, nonuniform membership circuit of $O(N)$ full binary gates.

Thus even isolation within an additive $O(\log(nq))$ of the counting limit is compatible with linear circuit size. In fact the repository's [deterministic membership bound](papers/deterministic/main.pdf) gives at least $2N-2\lfloor\log_2|C|\rfloor-1$ gates for the same example. The obstruction concerns superlinear growth. The leading constant in the upper bound leaves room for stronger linear lower bounds.

## One sparse map shared by many small linear spaces

Work over $\mathbf F_2$. Use $M=\lceil\sqrt N\rceil$ bits for a prefix and $K=N-M$ for the rest. First fix a $K\times M$ matrix $E$ with at most six ones per row and with every $q$ or fewer rows linearly independent.

To obtain $E$, sample six column indices independently with replacement in each row and take their parity vector. If $t$ rows sum to zero, their $6t$ samples occupy at most $3t$ columns. For large $n$, $3q\le M$. The probability of a dependence of weight at most $q$ is at most

$$
\sum_{t=1}^{q} {K\choose t}{M\choose 3t}(3t/M)^{6t}
\ \le\ \sum_{t=1}^{q}\left(27e^4 Kt^2/M^3\right)^t
\ =o(1).
$$

The last bound uses $Kq^2/M^3=O(q^2/\sqrt N)$. Evaluating this one fixed map on any $M$ bits costs at most $5K$ XOR gates.

Set $m=q+2$ and $L=nq+1$. Independently choose pairs of uniformly random binary $M\times m$ matrices $(H_i,P_i)$ for $1\le i\le L$. The possible words are

$$
w(i,u,c)=(H_i u,\ E P_i u)+c\,\mathbf 1_N,
\qquad u\in\mathbf F_2^m,\quad c\in\mathbf F_2 .
$$

This gives at most $L2^{m+1}$ words. Complementation toggles $c$. We choose the matrices to have two properties.

1. **Every small projection is onto.** Fix any $q$ positions. The corresponding rows of the block diagonal map $\operatorname{diag}(I_M,E)$ are independent. For each $i$, projecting the $m$ columns of the stacked matrix $(H_i;P_i)$ through those rows therefore gives a uniform $q\times m$ matrix. Its rows fail to have rank $q$ with probability at most $(2^q-1)2^{-m}<1/4$, by a union bound over nonzero row combinations. The probability some set of $q$ positions fails for all $L$ choices is at most $N^q4^{-L}=o(1)$. Smaller sets inherit surjectivity. Moreover, in a successful space each labeling already has at least $2^{m-q}=4$ seeds with $c=0$.
2. **The prefix distinguishes the words.** Within one space, two different seeds $u,u'$ have uniformly random prefix difference, even after adding fixed signs. The same holds across different spaces if at least one seed is nonzero. A pair with the same index and seed but opposite signs has prefix distance $M$. The zero seeds in different spaces denote the same two constant words. In the random cases the probability of prefix distance at most $q$ is $2^{-M}\sum_{j=0}^q{M\choose j}=2^{-M+o(M)}$. There are at most $(L2^{m+1})^2=2^{o(M)}$ pairs. Thus, except for the repeated representations of the constants, all distinct representations have prefix distance greater than $q$ with probability $1-o(1)$.

Fix matrices satisfying both properties. To isolate a labeling of a block, choose a word with that labeling and fix everything outside the block to that word. A second accepted completion would be within distance $q$.

## Recognizing the union with one evaluation of the sparse map

Let $h$ be the supplied prefix. For each $i$, the map $(u,c)\mapsto H_i u+c\mathbf 1_M$ is injective by the prefix property. Hardwire an invertible set of $m+1$ rows, recover a candidate $(u_i,c_i)$ from those prefix bits, and check the predicted prefix against all of $h$. The cost per index is $O(m^2+Mm)$. Also compute $P_i u_i$ at cost $O(Mm)$.

Reject if no prefix matches. Otherwise select the first matching index and use its $M$ intermediate bits and its sign. A fixed priority circuit and selectors cost $O(LM)$ gates. Multiple matches occur only for a constant prefix, where all predictions agree. Apply $E$ **once** to the selected intermediate bits, add the selected sign, and compare against the supplied tail. This accepts exactly the stated class. The total cost is

$$
O\bigl(L(Mm+m^2)+N\bigr)=O(N),
$$

since $L,m$ are polynomial in $n$ and $M=\lceil\sqrt N\rceil$. The choices of matrices and pivot rows are nonuniform.

## Adding easy truth tables

Fix in advance a family $S$ with $\log_2(|S|+1)$ polynomial in $n$. For every nonzero seed, its prefix is uniform, even after adding a fixed sign. The same prefix-distance union bound over all such seeds and all words in $S$ gives probability $o(1)$ of any distance at most $q$. Impose this additional condition when choosing the matrices. Each requested labeling has a nonzero seed by property 1. Its word is now isolated in $C\cup S$ as well. The extra recognition cost is one circuit for membership in $S$ and one OR gate.

For example, take $q\ge n^2$ and let $S$ consist of all affine functions of the $n$ address bits and the two Hamming balls of radius $n$ around the constant tables. These are all YES inputs of full-binary MCSP at threshold $n^2$. A table with $1\le t\le n$ exceptions can be written as an OR of $t$ address minterms, with at most $tn-1$ gates and a free output sign. Every affine table takes at most $n-1$ XORs. Also $|S|\le 2^{n+1}+2(n+1)N^n$, so the enlarged class still has log-cardinality at most $q+O(\log(nq))$.

One can recognize $S$ with $O(N)$ gates. Recover the affine coefficients from the origin and unit addresses, then check the predicted values in Gray-code order with one XOR per step. A balanced tree of binary additions computes the weight for the two ball tests in $O(\sum_{j\ge1}jN/2^j)=O(N)$ gates. This union is complement-closed and has distance one, since it accepts zero and the unit vectors. Address-translation symmetry and containment of *all* size-$n^2$ truth tables remain additional properties of MCSP. The construction bounds the power of a proposed lower-bound argument, and gives no upper bound for MCSP.

## Finite check and provenance

The [finite checker](experiments/check_isolation_barrier.py) exhausts a 16-bit example with two spaces, a 12-bit prefix and four shared output rows. It tests membership on every input, including both shared constant words, and all 480 choices of a pair of coordinates and a labeling. It repeats the isolation check after adjoining the radius-one balls. These small parameters illustrate the decoder and the added words. The existence argument for growing $q$ is the one above.

Samuel Schlesinger's *Structure from optimality* notes posed this obstruction and constructed a linear-size recognizer using reversible recurrences, sparse expansion and the finite-field small-bias construction of Alon, Goldreich, Håstad and Peralta. The proof here uses the sparse expansion with a short list of random linear spaces and a shared decoder to obtain the additive log-cardinality estimate. The use of unique neighbors for independence in sparse maps goes back to Siegel and is developed by Christiani and Pagh. [Alon et al., §5](https://www.wisdom.weizmann.ac.il/~oded/PSX/aghp.pdf) · [Siegel (2004)](https://doi.org/10.1137/S0097539701386216) · [Christiani and Pagh, §§III–IV](https://arxiv.org/abs/1408.2157)
