# Using all three common input pairs in an MCSP gate-elimination bound

Let $N=2^n$. At the fixed inner threshold $\lfloor0.99365N/n\rfloor$, every deterministic full-binary-basis circuit deciding MCSP has **more than $2.52307N$ gates** for sufficiently large $n$. The same holds for randomized circuits with pointwise two-sided error at most $2^{-0.0104N}$. Inputs are the $N$ table entries and fanout is unrestricted.

A second construction puts the pivots in one part of an address partition and raises the coefficient at this same threshold to $2.52435$. [Address partition](address-split.md)

At a private AND-type gate, three pairs of input values give the common output. The tilted proof uses a line through two of these pairs to produce an affine certificate. To use all three, we first satisfy the restrictions on individual entries and disjoint pairs. We then correct one pivot entry for each remaining parity query. When there are many such queries, their stronger gate decrements already give the desired bound. This uses the separate cases of Chen and Kabanets and the MCSP manuscript's synthesis theorem for relations on small cells. [Chen and Kabanets, Section 4.1](https://www2.cs.sfu.ca/~kabanets/papers/linsize-eccc.pdf) · [Tilted proof](main.tex) · [Small-cell synthesis](../witnesses/local.tex)

## The cost of satisfying a path

Follow a generalized elimination path whose labels specify parity answers and private gate outputs. In each ordinary step fix one pivot input by solving for it in the queried form. The remaining inputs are still original table entries. Each private step eliminates two such entries. Choose all circuit simplifications using only the recorded answers, including the output of each private gate. Later queries then involve none of its two inputs. Complete a terminal affine output with one query, or resolve a terminal gate on two inputs by specifying their values. This changes all the step counts below by $O(1)$.

Let $O$ count ordinary steps, $R$ those querying a parity of at least two remaining inputs, $W$ private steps, and $Y$ common private outcomes. Write $r=R/N$, $y=Y/N$, and $h=(N-O-2W)/N$. Write $\ell=\log_2 3$ and let $H_2$ denote binary entropy. There are $hN$ free entries after choosing the private outcomes and the ordinary pivots. Each common pair has three choices. All nonliteral pivot values can then be solved in reverse order. The full path therefore has $2^{hN}3^Y$ inputs, with terminal refinements included in the counts. Keeping one allowable affine line at each common pair gives a flat of dimension $(h+y)N$.

**Repair lemma.** For $r\le1/2$, this path contains a table of inner size at most

$$
\big[1-h-\ell y+H_2(r)-r+o(1)\big]N/n.
$$

Omit the $R$ nonliteral queries for now. What remains is a product of $O-R$ fixed bits, $W-Y$ fixed pairs, $Y$ three-point relations, and unconstrained entries. Its negative log probability under uniform input, in bits per table entry, is

$$
d_{\rm raw}=1-h-r-\ell y .
$$

The small-cell theorem supplies a table in this product with at most $(d_{\rm raw}+o(1))N/n$ gates. To see the unconditioned version of the theorem, choose a weight layer containing at least a $1/(N+1)$ fraction of the product's words. The log size of this layer is at most $N$. The same argument with the theorem's list parameter gives at least $2^{(u-d_{\rm raw}-o(1))N}$ words of size at most $uN/n$ for $d_{\rm raw}<u\le1$ with a fixed positive lower margin. One may decrease $u$ by a vanishing amount to absorb synthesis overhead. [Counting witnesses on small cells](../witnesses/local.tex)

Change the $R$ designated pivots in reverse query order to satisfy their equations. Each pivot has coefficient one in its own equation and occurs in no later restriction. Its correction preserves every single-entry and private-pair constraint. The correction mask has weight at most $R$. Any specified mask of weight $j$ costs at most $(\log_2\binom Nj+o(N))/n$ gates, by applying the same theorem to its singleton cells on its weight layer. This costs at most $(H_2(r)+o(1))N/n$. XOR the mask with the first table. All synthesis losses are uniform for these cells of size at most two.

## Charging parity queries for the gates they eliminate

For the gap promise let the inner thresholds be $\lfloor(1-a)N/n\rfloor$ and $\lfloor(1-b)N/n\rfloor$, with $0<b\le a<1$. A circuit must accept up to the first and reject above the second. Use the tilted sampling in the manuscript with ordinary strong-branch probability $p>1/2$ and common private-outcome probability $q\ge3/4$, both strictly below one. Its entropy condition is

$$
d=1-H_2(p),\quad D=q\log_2(4q/3)+(1-q)\log_2(4(1-q)),\qquad
\kappa=d+(D-2d)_+a/q<b .
$$

Choose a sufficiently small fixed $\xi>0$. Tilt the first $\lceil(a+\xi)N/q\rceil$ private steps, as in the manuscript. With probability bounded away from zero the sampled input is rejected. On a rejecting path the affine flat bound gives $h+y\le a+o(1)$. The concentration estimate for common outcomes then excludes reaching the cutoff on a typical rejecting path and gives $y=qW/N+o(1)$. [Entropy, concentration and the rejecting-flat bound](main.tex)

Put $A=3+p$, $B=(2+2p)/q$, and $\gamma=1-p$. Every ordinary step loses at least three units of the potential counting gates and live variables, and at least four on its strong branch. For a nonliteral query, case (1) of Chen and Kabanets loses at least four on **both** branches. In case (2), only its first subcase can query a nonliteral parity, and the two decrements are at least three and five. Their tilted mean is at least four in either case. Case (3) queries an individual input. Private steps lose at least four. Capping decrements at five and applying the bounded-difference martingale estimate gives, with probability $1-o(1)$, for outer gate count $G$,

$$
G+N\ge A O+4W+\gamma R-o(N),\qquad
G/N\ge 2+p-Ah-By+\gamma r-o(1).
$$

The second inequality uses the common-count estimate before the cutoff. A terminal step contributes only a bounded error to the capped sum. [Elimination cases (1)–(4)](https://www2.cs.sfu.ca/~kabanets/papers/linsize-eccc.pdf)

Write $\alpha=\ell-1$, $\Delta=B-A$, and $E(r)=H_2(r)-r$. Suppose $0<\Delta\le A\alpha$ and choose $0<r_0<1/2$ satisfying

$$
E(r_0)\le\alpha a,\qquad
\Delta\big(\log_2((1-r_0)/r_0)-1\big)\ge\alpha\gamma .
$$

Then every deterministic circuit for the promise satisfies

$$
\boxed{\quad G/N\ge 2+p-Ba+\gamma r_0-o(1).\quad}
$$

Indeed, if $r\ge r_0$, use $Ah+By\le B(h+y)\le Ba+o(1)$. If $r\le r_0$, the repair lemma on a rejecting path gives $h+\ell y\le a+E(r)+o(1)$. Combine this with $h+y\le a+o(1)$ using respective weights $\Delta/\alpha$ and $A-\Delta/\alpha$. This gives $Ah+By\le Aa+\Delta E(r)/\alpha+o(1)$. Since $E'$ is decreasing, $\gamma r-\Delta E(r)/\alpha$ is decreasing up to $r_0$. Substitution of $r_0$ and $E(r_0)\le\alpha a$ proves the bound.

| $a$ | $b$ | $p$ | $q$ | $r_0$ | $\kappa$ below | Gate count strictly above |
| --- | --- | --- | --- | --- | --- | --- |
| .00635 | .00635 | .545836 | $6/7$ | .000305 | .0063495 | $2.52307N$ |
| .00565 | .00565 | .543317 | .8526 | .000268 | .0056497 | $2.52298N$ |
| .007 | .00565 | .543104 | .8523 | .000342 | .0056497 | $2.51791N$ |

The strict rational margins absorb the $o(1)$ term. The numerical certificate checks every hypothesis and gate coefficient in the table. [Rational-arithmetic check](check_private_pairs.py)

## Exponentially accurate randomized circuits

The same lower bound holds for pointwise two-sided error $2^{-eN}$ whenever $e>\kappa+H_2(r_0)$. All three rows admit $e=0.0104$. The argument uses two common distributions on easy tables, since the circuit may assign an erroneous label to any given path.

Fix a deterministic circuit with a fixed positive gate margin below the boxed bound. Take $a'>a$ so close that its gate count still lies below the bound with $a'$ in place of $a$. Use a cutoff at $a''>a'$ sufficiently near $a$, and write $\kappa''=d+(D-2d)_+a''/q$, so $\kappa''<b$ and $\kappa''+H_2(r_0)<e$. With tilted probability $1-o(1)$ the potential and common-count estimates hold. If the cutoff is reached, at least $a'N$ common pairs are present. Otherwise $y=qW/N+o(1)$. Each such path satisfies at least one of the following conditions.

1. $h+y\ge a'$.
2. $r<r_0$ and $h+\ell y>a'+E(r)$.

Indeed, violating both alternatives before the cutoff gives the algebra of the deterministic proof with $a'$ and contradicts the gate margin. This argument uses only the circuit size.

For paths of the first kind, the dense affine law on easy tables gives at least $(1-o(1))$ times their uniform mass. Each common three-point set is the half-sum of the indicators of its three affine lines. Taking products gives the required positive weighted expression in flats of dimension $(h+y)N$. [Dense affine law](../dense-circuits/main.tex) · [Fractional representation and change of measure](confidence.tex)

For the second kind use the uniform law on all tables of inner size at most $\lfloor(1-a)N/n\rfloor$. Apply the list version of the repair lemma at pre-repair rate $u=1-a-H_2(r)-o(1)$. Its margin $u-d_{\rm raw}$ is at least $a'-a-o(1)$. Repairing can identify at most $2^R$ words per output since all nonpivot entries are preserved. Thus the number of easy tables on the path is at least

$$
2^{[h+\ell y-a-H_2(r)-o(1)]N}.
$$

The circuit census gives at most $2^{(1-a+o(1))N}$ easy tables in total. As the path's uniform mass is $2^{(h+\ell y-1)N}$, this second common law gives at least $2^{-(H_2(r_0)+o(1))N}$ times that mass. Mix the two laws equally to obtain this last estimate for both kinds of paths.

The manuscript's likelihood-ratio estimate gives their union uniform mass at least $2^{-(\kappa''+o(1))N}$. Let $u_+$ be uniform false-positive mass on required no inputs and $u_-$ false-negative mass under the common mixture. The good paths labeled one have uniform mass at most $u_++2^{-(b-o(1))N}$ by the census. Those labeled zero have uniform mass at most $2^{(H_2(r_0)+o(1))N}u_-$. Summing and averaging over circuit coins contradicts pointwise error $2^{-eN}$. All fixed margins and estimates are uniform over circuits of the stated size.
