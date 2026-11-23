<!-- Copyright (c) 2026 Christian Reitwiessner. -->
Authors: Christian Reitwiessner

# Independent research bounce

The generator semantics and family-coverage claims are sound: one common threshold circuit sees all evaluated table bits, and generic bounded-size LUT descriptions are universally covered. The construction circuit does not see the description. The size-one/two family results must remain distinct from ordinary-Andreev results.

## What the generator encoding saves

The fair unrestricted baseline is a symbolic checker on $N=2^k$ independent table bits, not an explicit enumeration of $2^N$ truth tables. A circuit description has $O(r\log(k+r))$ bits. This can be substantially smaller than $N$ only while its image omits many tables. Covering all $2^N$ tables requires at least $N$ description bits by counting, hence $r\log(k+r)=\Omega(N)$. Alias descriptions can make generic-circuit checking slower than independent raw-table checking. There remain $N$ possible table weights per bottom in either encoding.

The practical role is a curriculum and family oracle: use small generators to reveal candidate structure, then expand the family and always challenge the candidate with arbitrary raw tables. Exact examples show that the $k=3,r=2$ family excludes majority3 (mask 232) and a three-input multiplexer (mask 202), while containing three-input parity (mask 150). Thus passing $r=2$ does not mean that the troublesome three-variable spectra are exhausted.

## Auditing the uniform extension route

Let $H=[h_s\ge r]$ and let $L_{s,r}$ be the full address-ladder sum. The existing identity is

$$\chi_s(b)(2H-1)=4L_{s,r}-2H-2t_s-1.$$

Therefore coefficients $A_{s,r}$ on ladder sums and residual table-only coefficients $C_{s,r}$ give the finite coefficient-search score

$$D(x)+\sum_{s,r}A_{s,r}\bigl(\chi_s(b)(2H-1)+2H\bigr)+\sum_{s,r}C_{s,r}H.$$

It is implemented at arbitrary $m$ using ladder coefficients $4A_{s,r}$, table-only coefficients $C_{s,r}$, raw-address linear term $-2\sum A_{s,r}t_s$, and constant $-\sum A_{s,r}$. This is algebraically correct and finite verification on all table/parity pairs proves the resulting **uniform-in-$m$** family once the ladder range condition is checked. Vanishing $C$ terms save constants. Vanishing whole $A$ channels save ladder slope. The 49-bottom $A_{3,3}$ witness deletes only table-only gates, so that witness alone does not establish a slope improvement.

## General-Andreev implications and a useful obstruction

In any separable Fourier score $F(x,b)=D(x)+\sum_{t\in\mathcal S}f_t(x)\chi_t(b)$, every nonempty character $s$ must occur if the score correctly represents all tables. Apply it to $x_b=(1+\chi_s(b))/2$. Strict sign correctness forces $\mathbb E_b[F(x,b)\chi_s(b)]>0$, whereas a missing character gives zero by orthogonality. This explains why low-generator-family circuits can drop high-degree character channels: the relevant parity tables are outside those families.

Even one independent full ladder for every character costs

$$\sum_{s\ne\varnothing}\left\lfloor\frac{|s|m}{2}\right\rfloor=\Theta(km2^k).$$

At balance $km=2^k$, this is quadratic. Thus optimizing amplitude channels can improve constants, but this separate-full-ladder architecture cannot yield a fixed-power subquadratic bound merely by reducing each character to constantly many amplitudes. Shared hyperplanes across characters, cancellation between overlapping ladders, or a different address representation are needed.

A generator decomposition also needs **composability**. A collection of sign-correct circuits for simple generated tables cannot just be summed to represent an arbitrary table: uncontrolled margins can change the output. An exact-value score decomposition, quantitatively controlled margins, or bottom-level conditional gating is required. This is the bridge that a general construction would need to supply.

## Bounded extension experiment

`weighted_atoms.py` searches all 56 $k=3$ coarse Walsh channels $(s,r)$, $1\le s<8$, $-3\le r\le4$. It minimizes $\sum |s|$ over active channels, the resource proportional to the coefficient of $m$ in independent ladders. The inherited 13-channel construction has weighted cost 21, giving slope $21/2$. The model includes a free affine table term, arbitrary signed real channel coefficients, coefficient bound 100 during support discovery, and a 180-second MILP budget. A feasible support is refit without coefficient bounds and accepted only after exact rational reconstruction and arbitrary-precision integer verification on all 2048 table/parity pairs. Numerical dual bounds are not mathematical lower-bound certificates. Final result is in `weighted_atoms.json`.

Recommended order: finish the uniform table-only cancellation test; search smaller weighted channel cost at $k=3$ and then $k=4$; treat these as fixed-$k$/constant improvements. For growing $k$, prioritize a shared-gate identity with an explicit cost and margin accounting, rather than increasing generic generator size until the solver loses tractability.

The bounded weighted-channel search ended at its 180-second limit with weighted cost 21, not below the inherited value. The exact rational refit has margin 1 (integer-scaled minimum 2). Its numerical dual bound is 13; this is not an exact lower bound. No slope improvement was found.

A simpler useful coefficient identity emerged. The original thirteen channels already satisfy

$$F(x,b)=4\sum_{c=0}^7 x_c-16+3\sum_{(s,r)\in\mathrm{atoms3}}\chi_s(b)(2[h_s(x)\ge r]-1),\qquad (2x_b-1)F(x,b)\ge3$$

for all 2048 table/parity pairs. `uniform_atom_diagnostic.json` records zero errors and exact minimum margin 3. Expanding the existing ladder identity yields the same all-$m$ gate count with especially simple integer parameters: every ladder coefficient is 12; every table-only coefficient is $-6$; every direct table coefficient is 4; every direct raw-address coefficient is $-42$; top threshold is 55. The constant is $-16-3\cdot13=-55$. The count stays $6\lfloor m/2\rfloor+6m+\lfloor3m/2\rfloor+26$. This simplifies coefficients relative to the inherited construction, without claiming fewer gates. `uniform_model.py` gives the explicit circuit and independently checks representative full domains; `uniform_model.json` stores its results.

## Audit of the six-gate uniform cancellation improvement

I independently inspected `uniform_cancellation.py` and the exact coefficients in `uniform_cancellation_results.json`. The algebra and universal-$m$ extension are correct. This conclusion does not rely on a solver's numerical optimality report.

For each of the thirteen original atoms, $h_s\in[-4,4]$ and $r\in\{0,1\}$, so $q=h_s-r\in[-5,4]$. Write $H=[q\ge0]$, $t=t_s$ and

$$L=\sum_{\ell=0}^{\lfloor |s|m/2\rfloor}[6t+h_s\ge12\ell+r].$$

If $t=2v$, all terms with $\ell<v$ are true, the term $\ell=v$ equals $H$, and larger terms are false; hence $L=v+H$. If $t=2v+1$, exactly the terms $\ell\le v$ are true, giving $L=v+1$. Both cases hold at the endpoints $0\le t\le |s|m$ for every integer $m\ge1$. Therefore

$$4L-2t-1=\chi_s(b)(2H-1)+2H$$

without a residual error or an assumption on the size of $m$.

Let $u$, $\tau$, $A_j$, $C_j$ be the saved exact rational coefficients. The verified finite score is

$$Q(x,b)=u\cdot x-\tau+\sum_j A_j\bigl(\chi_{s_j}(b)(2H_j-1)+2H_j\bigr)+\sum_jC_jH_j.$$

All 2048 table/parity rows have signed margin at least 1: the saved integer-scaled minimum is 16 and the common denominator is 16. The raw circuit score obtained from ladder weights $4A_j$, standalone weights $C_j$, direct address contribution $-2\sum_jA_jt_{s_j}$, and top threshold $\tau+\sum_jA_j$ is **exactly $Q(x,b)$**. In particular the plus sign on the threshold correction is correct. Thus the finite certificate proves ordinary Andreev correctness for all $m\ge1$, not just the three tested values. Threshold ties are harmless because the signed margin is positive.

All thirteen $A_j$ are nonzero, while exactly seven $C_j$ are nonzero. Six singleton amplitude ladders contribute $6\lfloor m/2\rfloor+6$ gates; six pair ladders contribute $6m+6$; the triple ladder contributes $\lfloor3m/2\rfloor+1$; the seven standalone gates give

$$S_3^{\mathrm{new}}(m)=6\lfloor m/2\rfloor+6m+\lfloor3m/2\rfloor+20.$$

Add one top gate for total size. This saves six bottoms uniformly from the inherited fixed-$k=3$ formula. It yields $S=48,62,83$ at $m=3,4,6$, respectively. The slope remains $21/2$. This is an ordinary-Andreev fixed-$k$ upper-bound improvement; it establishes no growing-$k$ balanced leading-constant improvement and no subquadratic bound. The independent symbolic timeouts are UNKNOWN, but the all-table finite coefficient certificate plus the exact ladder identity already constitute a proof for every $m$.
