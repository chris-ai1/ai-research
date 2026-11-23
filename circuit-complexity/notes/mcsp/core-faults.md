# One flipped entry distinguishes cores of identical size

Fix $N=2^n$ and count full binary gates with free constants and wire signs. At threshold $s=n^2$, a single fixed truth-table flip can distinguish two accepted centers even when their minimum gate counts agree and their tables agree throughout the radius-one address neighborhood of that flip. In fact the minimum costs after the flip can be made to run through a whole interval of consecutive integers with $s$ in its middle.

## The cost formula

Use disjoint address groups $w,y,q,z$ of sizes $a,p,l,m$, with $p,l,m\ge1$. Fix a nonconstant core $g(w)$ and a core address $u$. For a partition $\pi$ of the $p$ coordinates into $b$ nonempty blocks set

$$
 K_\pi(y)=\bigoplus_{V\in\pi}\left(\bigwedge_{i\in V} y_i\right)\oplus (b\bmod 2)\oplus(p\bmod 2),\qquad
 B_\pi=g(w)\oplus K_\pi(y)\oplus\operatorname{Par}_m(z).
$$

The selectors $q$ are unused. The sign makes $K_\pi$ equal to full parity at $1^p$ and at every neighbor of $1^p$, for every partition. Write $B_\pi^\star$ for the result of flipping just $(u,1^p,1^l,0^m)$.

Let $A_m(g,l,u)$ be the minimum size of the table $g(w)\oplus\operatorname{Par}_m(z)$ with one flip at $(u,1^l,0^m)$, using no $y$ inputs. The odd-error lemma gives $A_{m+b}(g,l,u)=A_m(g,l,u)+2b$. The same size applies at any parity address, by signs on inputs and output. [Odd-error manuscript, Section 2](../../results/mcsp/papers/probabilistic/main.tex)

**Theorem.** For every partition $\pi$ as above,

$$
 C(B_\pi)=C(g)+m+p,\qquad C(B_\pi^\star)=A_m(g,l,u)+p+b.
$$

To prove the second identity, replace each block by its single conjunction output $v_V$. The marked point of the $y$-cube is the unique preimage of $v=1^b$. The quotient function is therefore the ordinary parity extension of $g$ on $m+b$ coordinates with one flip, up to a global sign. Computing the conjunctions adds $p-b$ gates to the quotient.

For the reverse inequality, in each block set all but one of its inputs to one. Each input being fixed is essential on a clean selector slice, where its other block members can be set to one. At least one gate disappears at every fixing, since the clean slice also depends on a $z$ input and the function cannot be the literal being fixed. On the last $b$ surviving representatives the restricted function is exactly the quotient. This proves equality and gives $A_{m+b}+p-b=A_m+p+b$.

The same argument without the flip reduces the clean table to $g$ XOR parity on $m+b$ bits. That extension costs exactly $C(g)+m+b$, by fixing its fresh essential parity inputs successively. Appending XOR gates attains the bound. Every clean table therefore has the same minimum size. All of them agree, for every $w,q,z$, when $y$ is at distance at most one from $1^p$.

For example, take $g(w)=w$, two $y$ bits, one selector, and one $z$ bit. The alternatives for $K$ are NAND and XOR. Both clean functions cost three gates. At $u=0$ the single flip raises their costs to six and seven respectively. Here $A_1=3$ because $w,z$ are two parity bits of a constant core, and with just one parity bit the fault gives the one-gate function $z\lor q$.

## A common quadratic threshold

Take $a=\lceil4\log_2 n\rceil$, choose $2\le p\le\lfloor n/2\rfloor$, and prescribe any $1\le b_0<p$. For all sufficiently large $n$ one can choose the **same** $g,u,l,m$ for all partitions so that

$$
 C(B_\pi^\star)=n^2+b-b_0 .
$$

Here $m=n-a-p-l$ and $l$ remains bounded by an absolute constant. To see this, use the path of cores in the threshold interpolation argument of the odd-error manuscript. Write $A_1(g)$ for the minimum over core locations with one selector. Along this path $A_1(g)$ starts at $O(a)$, ends at $\Omega(2^a/a)$, and its upward steps are bounded by an absolute constant. The selector and parity recurrences give
$\min_u A_m(g,l,u)=A_1(g)+(l-1)+2(m-1)$.
Consequently the cost for $b=b_0$ at a minimizing location is

$$
 A_1(g)+2(n-a)-p-l+b_0-3 .
$$

Varying $l$ from 3 through a sufficiently large fixed constant gives an integer interval wider than the maximum upward step. The first interval is below $n^2$ and the last is above it. Choose a core, selector count, and minimizing $u$ at which the displayed cost equals $n^2$. The core is nonconstant because constant cores have $A_1=O(a)$. This is an existence argument. [Odd-error manuscript, threshold interpolation](../../results/mcsp/papers/probabilistic/main.tex)

All unflipped centers are accepted. Indeed fixing an essential selector to its inactive value in a size-$n^2$ example with $b=b_0$ saves a gate and returns its clean center. The formula gives the same clean cost for all partitions. Taking $b_0$ near $p/2$ gives a linear-in-$p$ separation between the extreme perturbed costs. With $p=\Theta(\log n)$ the two examples already have a common layout with $O(\log n)$ core and selector bits. With $p=\lfloor n/2\rfloor$ the separation is $\Theta(n)$.

## What the outer predicate reads

For $p=2k$, split the $y$-coordinates into $k$ prescribed pairs. A control bit $t_i$ leaves pair $i$ as one block at zero and splits it into two singleton blocks at one. Then $b=k+|t|$. On the clean tables every control setting accepts. After the same flip, exact MCSP accepts precisely when $|t|\le b_0-k$. In particular, for $k\ge2$ one can place the cutoff at $\lfloor k/2\rfloor$.

This is an affine family of truth tables over $\mathbb F_2$. In each pair the two possible contributions, including the normalizing sign, are NAND and XOR, which differ only at $00$. Each truth-table bit is a fixed bit plus the XOR of the controls whose address pairs are $00$. To recover the controls, take $w=u$, $z=0^m$, and an inactive $q$. Read a reference bit with all pairs $11$, and for each $i$ read the entry with just that pair set to $00$. Its XOR with the reference is $1-t_i$. On the flipped family these $k+1$ entries determine the MCSP label. On the union with the clean centers, one additional read at the marked address detects the flip by comparison with the reference. The family shows exactly how the label can depend on core structure at equal clean complexity. Its controls can all be recovered from this small set of entries.
