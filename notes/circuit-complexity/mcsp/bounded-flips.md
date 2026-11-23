# Circuits on bounded changes to parity extensions

A four-site test fixes almost every entry of a truth table at a baseline and varies the remaining entries. Suppose the baselines come from a parity extension of one small core, with all permutations and signs of the address inputs allowed. Even the exact MCSP labels on **every** table within a fixed Hamming distance of **every** such baseline admit a deterministic circuit of size $2N+O(N^{1-\eta})$, for a constant $\eta>0$. For all orientations of one small core, a sublinear additive cost also suffices for up to $\lfloor\log_2 n\rfloor-1$ flips. This bounds what any list of those tests can force about the size of an outer circuit.

Work over the full binary basis with free signs and constants. Let $n$ be the number of address bits and $N=2^n$ the number of table entries. All circuits below are nonuniform.

## Reading the locations of a bounded number of flips

Fix an integer $t\ge1$. There is a binary linear map $S$ on $N$ bits with the following properties.

- All outputs of $S$ together cost at most $2N$ XOR gates.
- Given $S(e)$ for a word of Hamming weight at most $t$, a circuit of size $O_t(N^{1-\delta_t})$ returns the list of its nonzero positions, with a length or presence flags. Here $\delta_t>0$ depends only on $t$.

We use the high-girth graph incidence map of Fan, Li and Yang. The extra step is to use copies of a small graph so the locations can be recovered with a sublinear number of gates. [Fan, Li and Yang](https://eccc.weizmann.ac.il/report/2021/125/) and [Chen, Li and Yang, Section 1.4.1](https://doi.org/10.4230/LIPIcs.CCC.2022.23)

Take $b=2^{\lfloor\epsilon n\rfloor}$, where $\epsilon>0$ will be small in terms of $t$. A simple graph exists with $b$ edges, $v=\lceil b^{1-1/(4t)}\rceil$ vertices and girth greater than $2t$. To see this, take independent edges with expected edge count $4b$. The expected number of cycles of any fixed length $3\le j\le 2t$ is $O_t((b/v)^j)$. Their total expectation is $O_t(\sqrt b)$. Some graph has at least $b$ more edges than short cycles. Delete one edge from each surviving short cycle, then keep $b$ edges.

Divide the inputs into blocks of $b$ and use the same graph in every block, with its edges labeled by input positions. Output one parity of the incident bits per vertex. The gate count is at most the $2N$ incidences, and the total number of outputs is $L=O(Nb^{-1/(4t)})$. Two edge sets of size at most $t$ with the same syndrome would have an even-degree symmetric difference of at most $2t$ edges. Every nonempty even-degree subgraph contains a cycle. The girth therefore gives uniqueness.

There are at most $2t$ nonzero syndrome bits. List their block and vertex indices in $O_t(L\log N)$ gates. For example, prefix ORs select the first remaining one, its binary index can be assembled from those selection bits, and the procedure is repeated at most $2t$ times. Every nonempty block of at most $t$ edges appears in this list. Group its vertex indices by block using comparisons on the list. For one block, at most $2t$ vertex names and their presence flags specify the syndrome. A hardwired table on $O_t(\log b)$ bits returns the unique edge list when it exists, at cost $b^{O_t(1)}$. Reuse the same table design for each of the at most $2t$ blocks. Joining the decoded edge names to their block indices takes $O_t(\log N)$ more gates. Taking $\epsilon$ sufficiently small makes both $L\log N$ and $b^{O_t(1)}$ at most $O_t(N^{1-\delta_t})$.

## Several possible baselines

Fix $k\ge1$ and $M=N^{o(1)}$ known centers. Let $F$ be the predicate of interest. Suppose that for each center $c$, given the list of up to $k$ changed addresses, the label of the modified table can be read by a circuit of size $N^{o(1)}$, uniformly in the size bound over centers. Then there is a circuit of size $2N+O(N^{1-\eta_k})$ agreeing with $F$ everywhere within distance $k$ of any center.

For every pair of different centers, select all positions on which they differ if their distance is at most $2k$, and select any $2k+1$ disagreements otherwise. Let $D$ be the union of these choices. Score each center by its distance from the input on $D$, capped at $k+1$, and flag the centers with minimum score. All scores and flags can be computed in $O_k(M^3+1)$ gates by counting up to $k+1$ per center and comparing the scores.

To check ties, choose a genuine center $c$ within distance $k$ of the input $X$. Every flagged center $c'$ has score at most the score of $c$, hence at most $k$. If $c,c'$ differed at more than $2k$ positions, their sampled distance would exceed the sum of their scores. Thus they differ only at positions of $D$. Outside $D$ they have the same distance from $X$, and inside $D$ the flagged center is at least as close. Therefore $d(X,c')\le k$.

Compute $S(X)$ once with $t=k$. For each center $c$, the vector $S(X)\oplus S(c)$ is obtained with free wire signs. Decode it and evaluate the label circuit for $c$. Output the OR of the labels of the flagged centers. On the promise, there is at least one flag and every flagged label equals $F(X)$. The shared encoder costs at most $2N$. The $M$ decoders cost $O_k(MN^{1-\delta_k})$ and the remaining gates cost $N^{o(1)}$. For example one can take $\eta_k=\delta_k/2$ for all sufficiently large $N$.

## Application to fixed-threshold MCSP

Consider centers $h(y)\oplus\operatorname{Par}(z)$ with $r$ core inputs, $l$ unused inputs and $n-r-l$ parity inputs, where $r+l=O(\log n)$. Fix any threshold $s$. For a fixed core and any assignment of its distinguished address axes, the label of at most $k$ changes has a small description. Record the core and unused bits at every changed address in list order. Among the parity coordinates count how many columns display each binary pattern down the list. These data determine the ordered addresses up to a permutation of the parity coordinates. Such permutations preserve both the center and the gate count of the perturbed address function.

There are $2^{O_k(r+l)}(n+1)^{2^k}=n^{O_k(1)}$ possible descriptions, with the constant in the bound on $r+l$ fixed. The counts can be computed from the address list with $\operatorname{poly}_k(n)$ gates. The exact MCSP answer for each attainable description can be hardwired in a table of polynomial size in $n$. This is the nonuniform step that avoids finding optimal inner circuits during recognition.

Allow all signed permutations of the address axes and either output sign. Even with the core coordinates ordered, there are at most $2^{O(r+l+1)}n^{r+l}=N^{o(1)}$ distinct centers, since signs on parity coordinates only affect the overall sign. The theorem for several centers applies, and also permits $N^{o(1)}$ different fixed cores subject to the same bound on distinguished axes.

### A radius growing with the address length

For all signed orientations of one such core, the bound for $1\le k\le\lfloor\log_2 n\rfloor-1$ is

$$
  2N+O\!\left(N\,2^{-\Omega(n/(\log n)^2)}\right).
$$

Here are the quantitative bounds behind this extension. Take $b=2^{\lfloor n/(16k)\rfloor}$ and $v=\lceil b^{1-1/(4k)}\rceil$. The short-cycle expectation in the random graph is at most $2k\,C^{2k}\sqrt b=o(b)$ for an absolute $C$, since $k=O(\log n)$. There are $O(N\,2^{-\Omega(n/k^2)})$ syndrome bits. Extracting and grouping the at most $2k$ nonzero indices costs this number times $\operatorname{poly}(n)$. Each block lookup takes at most $2k(\lceil\log_2 v\rceil+1)$ input bits including the flags. Direct lookup of the edge list therefore costs at most $b^{2k}2^{O(k)}\operatorname{poly}(n)=2^{n/8+o(n)}$ gates. The center count $2^{O((\log n)^2)}$ and the polynomial costs of arithmetic are absorbed by the saving in the syndrome length.

It remains to bound the number of MCSP labels to hardwire. For a nonempty list of $j\le k$ changes, translate the parity coordinates so the first marked address has parity-coordinate vector zero. This address translation preserves the baseline up to a global output sign, which is free and restores the original baseline. Now only $2^{j-1}$ column types remain. Their counts sum to the number of parity coordinates. Put $a=\lfloor n/4\rfloor$, so $2^{j-1}\le a$. The number of histograms is at most $\binom{n+a}{a}\le 2^{(\log_2(5e)/4+o(1))n}$. The exponent coefficient is less than $0.95$. There are only $2^{O((\log n)^2)}$ choices of the marked core and unused bits, list lengths, and centers. Compare the computed histogram and distinguished bits against each accepting description and OR the matches. Every comparison costs $\operatorname{poly}(n)$ gates. This lookup contributes at most $2^{0.95n+o(n)}$ gates even though the naive binary encoding of all counts can be much longer than $n$ bits. The empty list has one label per center.

Consequently these neighborhoods of small-core parity extensions at $s=n^2$ cannot force a $2N+\Omega(N/\log\log N)$ lower bound through their labels alone. Perturbations larger than this radius, or a family with many more distinct cores, fall outside the growing-radius argument.

## Geometric tests with an arbitrary unknown core

There is a stronger barrier when the prescribed labels can be computed from the changed addresses alone. It applies to **all** small-core truth functions at once. Write a center as $P_n\oplus g(x_J)$, where $P_n$ is full address parity, $|J|\le d=O(\log n)$, and $g$ is an arbitrary truth table on $J$. This includes a parity extension with $O(\log n)$ core and unused bits, since their parity can be absorbed into $g$.

Suppose an input is within distance $k$ of some such center. Both the relevant coordinates and the truth table of the center may be unknown. For each assignment to each set of at most $2d$ coordinates, choose $2k+1$ distinct full addresses extending it, and let $D$ be their union. For $k=O(\log n)$ this is possible and $|D|=2^{O((\log n)^2)}$. Two different centers disagree everywhere above at least one assignment to the union of their distinguished coordinate sets. Thus they disagree on at least $2k+1$ positions of $D$.

Enumerate the $2^{O((\log n)^2)}$ possible sets $J$. For each assignment to $J$, take a majority of $X\oplus P_n$ on its $2k+1$ chosen extensions to construct a candidate $\hat g_J$. A genuine layout recovers its whole truth table. Test whether $P_n\oplus\hat g_J$ differs from $X$ on at most $k$ positions of $D$. A genuine candidate passes and every passing candidate equals that same center, by the preceding distance bound. All these majority and distance tests together cost $2^{O((\log n)^2)}$ gates.

Compute the common incidence syndrome $S(X)$ once. For each candidate, each bit of $S(P_n\oplus\hat g_J)$ is a known affine form in its at most $2^d$ recovered truth-table bits, hence costs $O(2^d)$ gates. There are $L$ forms per layout. The extra factor for all layouts and truth-table bits is $2^{O((\log n)^2)}$, which is absorbed by the saving in $L$. Decode the difference for each passing layout as above. Thus any $N^{o(1)}$-gate predicate of the list of changed addresses can be evaluated on this promise at size $2N+O_k(N^{1-\eta_k})$ for fixed $k$, and at size $2N+N\,2^{-\Omega(n/(\log n)^2)}$ for $k=O(\log n)$.

For example, consider baselines calibrated one gate below the odd minimum in a fiber. On the prescribed tests accept the baseline, reject singletons and triples, accept a double exactly at distance one or two, and for four changes accept whenever the XOR of their four addresses is zero. This last rule agrees with every rejection obtained from two pairs of distinct displacements and every positive coordinate-square test. It also agrees with all the rejections the full conjecture about two individually affordable pairs of different displacements would supply. These geometric labels alone therefore allow a near-$2N$ circuit even if arbitrarily many different cores are used. Exact MCSP on the other four-flip configurations may require additional information about the core. [Odd-error construction](../../../results/circuit-complexity/mcsp/papers/probabilistic/main.tex) and [four-flip conjecture and partial result](https://github.com/chris-ai1/ai-research/pull/5)
