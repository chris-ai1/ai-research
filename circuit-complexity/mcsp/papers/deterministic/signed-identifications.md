# Signed identifications sharpen the sparse deterministic MCSP bound

Let $N=2^n$. For $n=o(s)$ and $s=o(N/n)$, unrestricted deterministic circuits over the full binary basis deciding exact $\mathrm{MCSP}[s]$ require

$$
2N-\bigl(3-2\log_2(1+\sqrt2)+o(1)\bigr)s\log_2 s
$$

gates. The coefficient of the subtracted term is approximately $0.45689339$. At $s=n^2$ this improves the previous $2N-(4+o(1))n^2\log_2 n$ to **$2N-(0.913787+o(1))n^2\log_2 n$** (the displayed decimal is rounded upwards). The leading coefficient remains two.

The previous proof taught one accepted table and its complement, then applied Schnorr's lower bound for all-equal. We first choose identifications at the bottom gates of the given circuit. Both signs preserve complementation, but one sign can delete an additional gate. Counting the accepted tables across the resulting branches recovers part of the loss from teaching. [Teaching and the rooted circuit count](main.tex) · [Schnorr, The combinational complexity of equivalence](https://doi.org/10.1016/0304-3975(76)90073-6)

## A bound for families meeting signed identifications

Let $A\subseteq\{0,1\}^N$ be nonempty and closed under bitwise complement, and let $L=\log_2|A|$. Suppose that for every forest with at most $r$ edges on the $N$ coordinate positions, every assignment of signs $b_{ij}$ occurs in $A$ as the values $x_i\oplus x_j=b_{ij}$ on its edges. Assume $r$ is a nonnegative integer and $L+r\le N$. A $G$-gate circuit deciding membership in $A$ satisfies

$$
\boxed{\quad G\ \ge\ 2N-2L-1+2r\log_2(1+2^{-1/2}).\quad}
$$

All gates are arbitrary binary Boolean functions. Constants and complemented wires are free. The proof allows unrestricted fanout.

**Teaching bound at a leaf.** If a circuit with $g$ gates on $m$ formal inputs recognizes a nonempty complement-closed family $B$, then

$$
|B|\ \ge\ W(m,g),\qquad W(m,g)=2^{(2m-g-1)/2}.
$$

Indeed, repeated selection of the smaller nonempty side of a distinguishing coordinate teaches some member with at most $\lfloor\log_2|B|\rfloor$ coordinates. Identify those inputs with signed copies of one reference input and sign each other input relative to that member. The restricted predicate is all-equal on $m-|J|+1$ inputs, where $J$ is the teaching set. Schnorr's exact $2d-3$ bound gives the inequality. It also holds when $|J|=m$ by $g\ge0$. This argument counts formal inputs, including any that have become irrelevant. [Teaching projection](main.tex)

**Splitting at a bottom gate.** At a depth-$j$ node, each original coordinate is a signed copy of one of $m=N-j$ free representatives. The node has a nonempty complement-closed family $B$ in these representatives. Each member lifts uniquely to a member of $A$. If $j<r$, then $m>L$ and $B$ is a proper subset of the cube. A nonconstant complement-invariant predicate depending on at most two inputs must require one prescribed parity of two distinct inputs. Both parities of any two representatives occur in $B$, since joining them adds only one forest edge. The predicate therefore depends on at least three representatives. In a trimmed circuit after simplifying constants and unary gates, take a gate with both predecessors raw. These predecessors are distinct and the gate has a successor.

Identify its two inputs up to a sign, in turn using $x_i=x_j$ and $x_i=1\oplus x_j$. This merges distinct components of the forest, so both children are nonempty until depth $r$. Their accepted families partition the parent's family under lifting. On either sign the gate becomes unary or constant and can be removed. For an XOR-type gate both signs make it constant. Every other essential binary gate is a signed AND, and the sign excluding its exceptional input pair makes it constant. A constant gate also trivializes at least one successor. Thus we can choose gate counts for the two restricted circuits at most $g-1$ and $g-2$, in some order.

After deleting $e$ gates and one representative the child's weight is at least $2^{(e-2)/2}W(m,g)$. Consequently the two weights sum to at least $(1+2^{-1/2})W(m,g)$. At depth $r$ the total weight is at least $(1+2^{-1/2})^r W(N,G)$. The leaf teaching bound puts this total below or equal to $|A|$, since the leaf families lift to disjoint sets. Taking logarithms proves the boxed inequality.

## Realizing all forest signs with small inner circuits

Put $T=s\log_2 s$. For every fixed $0<\eta<1$ take $r=\lfloor(1-\eta)T\rfloor$. A forest with $j\le r$ edges has independent binary incidence rows, as seen by deleting leaves. It involves at most $2r$ positions. We show that every syndrome of these rows occurs in a table of size at most $s$.

First map the $n$-bit addresses linearly to $m=\min(n,\lceil2\log_2(2r)\rceil+1)$ bits, injectively on the positions involved. If $m=n$, use the identity. Otherwise a random matrix has collision probability $2^{-m}$ for each distinct pair, so the union bound gives a suitable map. The address circuit for the map costs $o(s)$ gates. To see this when $s\le n^2$, there are $m=O(\log n)$ parity outputs. Divide them into groups of at most $\lfloor(\log_2 n)/2\rfloor$ rows. Within one group, bucket the $n$ input bits by their column pattern and XOR the bits in each nonempty bucket. Each output is a sum of at most $\sqrt n$ bucket values. A constant number of groups costs $O(n)=o(s)$. When $s>n^2$, even the direct $O(n\log s)$ cost is $o(s)$.

On this shorter address the same rows still have rank $j$, since the map was injective on their support. There is room to extend them to rank $r$ because $r=o(N)$ and $2^m\ge r$. The repository's polynomial-rank affine interpolation theorem realizes every syndrome by an address circuit of size $(1+o(1))r/\log_2 r$. Its range condition is $m^{30}\le r\le 2^m$, which holds here since $m=O(\log r)$. The original $n$-bit table is the composition of the hash and this circuit. Its cost is $(1-\eta+o(1))s$, so it fits the threshold for large $n$. Only interpolation on the shorter address is needed. [Affine interpolation, polynomial-rank theorem](../affine/sparse-sharp.tex) · [Parent manuscript](../affine/main.tex)

Finally, the rooted circuit census gives $L\le(s+1)\log_2(n+s+2)+O(s+\log(s+2))=(1+o(1))T$. Here $T=o(N)$, so $L+r\le N$ for large $n$. Substitute in the boxed inequality and then let $\eta$ decrease to zero. The coefficient is $2-2\log_2(1+2^{-1/2})=3-2\log_2(1+\sqrt2)$.

## What a circuit below $2N$ would have to do

The same calculation localizes the remaining loss. Trim the circuit after every identification. Call an internal node of the restriction tree *weak* if every bottom gate is nonlinear, has just one successor, and the gate's common output value fails to make that successor constant. The common value is the output on the three inputs other than the exceptional pair. Whether a successor becomes constant is tested with its other input still free.

At any other node choose a bottom gate witnessing the failure of one of these conditions. An XOR-type bottom gate deletes at least two gates on each sign, giving weight multiplier at least $2$. If a bottom gate has at least two successors, the constant sign deletes all three gates, giving multiplier at least $2^{-1/2}+2^{1/2}=3/\sqrt2$. The same estimate holds when the common value of a nonlinear bottom gate makes its unique successor constant. That successor cannot be the circuit output at these depths in the sparse regime. The restricted class is nonempty on both signs, and its size is smaller than a whole child cube. A constant successor therefore trivializes at least one more gate. At a weak node the guaranteed multiplier is $M=1+2^{-1/2}$.

Put $c_*=2\log_2(2/M)=3-2\log_2(1+\sqrt2)$. If $G\le 2N-\delta T$ for fixed $\delta>0$, there is a path on which at least $(\delta/c_*-o(1))T$ stages are weak. To see this, choose feasible depths $r=T-o(T)$ by letting the fixed interpolation margin tend to zero sufficiently slowly. At each split assign branch probabilities proportional to the two guaranteed child weight factors. The sum of the leaf weights is at least $W(N,G)$ times the expected product of the node multipliers, by expanding the expectation over paths. This sum is at most $|A_s|\le 2^{T+o(T)}$, while $W(N,G)\ge 2^{(\delta T-1)/2}$. On some path the product is therefore at most $2^{(1-\delta/2)T+o(T)}$. With $k$ weak nodes the product is at least $2^{r-k}M^k$, which gives the claim.

For comparison, if the circuit permits a choice with the $3/\sqrt2$ multiplier at every node through depth $T-o(T)$, the same proof gives $G\ge 2N+(\log_2(9/8)-o(1))T$. This last estimate is conditional on the choices throughout the restriction tree. Establishing further savings at the weak nodes is open.

[Finite checks of the gate cases and the four-input bound](check_signed_identifications.py)
