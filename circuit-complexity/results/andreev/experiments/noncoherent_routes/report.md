# Further constructions with mixed address signs

Authors: Christian Reitwiessner

Date: 13 November 2026

## Result and priorities

This pass gives explicit exact quadratic circuits with incompatible within-block sign patterns, and develops two exact joint table/address primitives: an adaptive slab whose width depends on the table, and a single gate packing different table thresholds on different address slices. A Walsh mask family supplies address normals that cannot all have few sign changes under any common ordering or bit reorientation. These are construction ingredients, not a better asymptotic upper bound. The existing $(5/16+o(1))n^2$ exact bound remains unchanged.

The strongest candidate is a joint sum of dense-table adaptive slabs with row-dependent address normals, potentially allowing diagonal sharing. Its unresolved requirement is a strict correct sign on every independent table and every raw address. No global decoder satisfying that requirement was obtained. The finite checks verify the identities and the quadratic circuits; no solver search or claimed small-instance improvement is hidden in them.

A subsequent pass in [Exact decoding from adaptive slabs](followup.md) proves a dense-table decoder and a parity-restoration identity, and supplies two independently checked finite circuits from a specified atom dictionary. Neither improves the known bounds.

## Model and inherited constraints

Write $N=2^k$, $y_c=1-2x_c$, $b_i(a)=\sum_j a_{i,j}\pmod2$, and $n=N+km$, with $km\asymp N$. The circuit receives the raw bits $x,a$, not computed block parities, table codewords, or mask choices. Every gate and coefficient is fixed before the input is known.

Relevant prior work was read before proposing these routes: `coarse_mixed_general`, `asymptotic_creative_astra`, `asymptotic_creative_astra_pass2`, `exact_creative_astra`, `coefficient_language_astra`, `one_table_bit`, `swarm/up2`, and `eth_transfer`.

Their restrictions matter. A single common input reorientation is essentially the coherent construction again. A fixed pair of linear statistics per block still admits a common ordering with few sign runs. Independent full parity ladders remain quadratic, even with mixed masks. Few periodic positional queries have a scalable counterexample. A scalar shrinkage of Walsh coefficients fails for explicit tables. These results concern their specified architectures, not every mixed-sign circuit.

## 1. An explicit exact family with incompatible masks

Let

$$X_S(x)=\sum_c(-1)^{S\cdot c}y_c.$$

For every nonempty $S\subseteq[k]$, choose integer weights $w_{S,i,j}$ that are odd on blocks $i\in S$ and zero on the other blocks. Their signs and magnitudes may differ across gates and inside blocks. Define the raw linear form

$$t_S(a)=\sum_{i,j}w_{S,i,j}a_{i,j}.$$

Oddness gives $(-1)^{t_S(a)}=(-1)^{S\cdot b(a)}$. Since $X_S$ is even, with $\varphi(u)=(-1)^u u$ we obtain the exact identity

$$N y_{b(a)}=X_\varnothing+\sum_{S\ne\varnothing}
\bigl(\varphi(X_S+t_S)-\varphi(t_S)\bigr).$$

Let $\ell_S=\sum\min(w_{S,i,j},0)$, $h_S=\sum\max(w_{S,i,j},0)$, and $V_S=h_S-\ell_S=\sum|w_{S,i,j}|$. Expanding the two integer staircases costs at most $2N+2V_S$ bottom gates. Thus

$$G\le 2N(N-1)+2\sum_{S\ne\varnothing}V_S.$$

The gates are thresholds of $X_S+t_S$ or $t_S$, hence affine in the original bits; $X_\varnothing$ and the staircase constants go directly to the top. The score is exact, not merely sign-correct.

For $\pm1$ address weights, $\sum_SV_S=mkN/2$ and

$$G\le2N(N-1)+mkN.$$

For even $m$, alternating magnitudes $1,3$ within each active block give $\sum_SV_S=mkN$ and $G\le2N(N-1)+2mkN$. These are quadratic benchmarks, not improvements over the refined existing construction.

A concrete genuinely incompatible family uses $w_{S,i,j}=(-1)^{S\cdot j}$ on active blocks, interpreting the column index as a binary vector (or modulo $N$). For $k\ge2,m\ge3$, rows $S=\{1\}$ and $S=\{1,2\}$ have patterns that are neither equal nor complementary in their common block. No common bit flip can make both coherent there. Multiplying by positive odd magnitudes preserves this property. The checks instantiate both versions on every raw input of $A_{2,4}$.

The purpose of this family is to make clear that constructing a noncoherent circuit itself is straightforward. A better bound requires exploiting the distinct masks jointly, rather than summing their complete ladders independently.

## 2. Table-dependent width with two gates

Let $H(x)$ be an odd integer affine table form and let $L(a)$ be any integer affine raw-address form. Then

$$\boxed{[2L+H\ge0]-[2L-H\ge0]
=\operatorname{sgn}(H)\,[2|L|<|H|].}$$

For positive $H$, the gates differ exactly when $-H<2L<H$; oddness avoids ties. Negative $H$ reverses the sign. Each displayed gate is an ordinary threshold of raw inputs.

Unlike a fixed slice, this atom selects a window whose width changes with the table. For $H=y_1+\cdots+y_5$, the active integer values of $L$ form a window of width 1, 3, or 5 according to $|H|$. Dense table rows therefore control both the contribution's sign and which addresses receive it. Arbitrarily large table coefficients do not increase the two-gate count, although their bit lengths still belong to a description-cost analysis.

An exact target is

$$F(x,a)=A(x,a)+\sum_{j=1}^R v_j\operatorname{sgn}(H_j(x))
[2|L_j(a)|<|H_j(x)|],$$

with $A$ affine and

$$y_{b(a)}F(x,a)>0\quad\text{for every }x,a.$$

A successful construction costs at most $2R$ bottoms and one top. Setting $R=O(Nm)$ would give $O(n^2/\log n)$ at balance. This is a sufficient condition, not an existence theorem.

Why this is a worthwhile relaxation: the active set depends jointly on the table and address. It is not a fixed address feature times a scalar table quantizer, so the earlier fixed-dictionary or scalar-Walsh-shrinker arguments cannot simply be applied. Dense $H_j$ also avoids the assumption that each gate reads one table bit. It remains a restricted class of general raw gates and may have other obstructions.

What is still missing: these atoms do not automatically contain the parity factor. A lone wide window with the sign of a large Walsh coefficient is not a replacement for $X_S(-1)^{t_S}$. Signed cancellation across differently positioned, differently oriented atoms must perform the decoding. Using a common $L$ or separately repeating a complete periodic family for every character would give away the intended saving.

## 3. One gate can pack many different table thresholds

A useful alternative to independent localized products is the exact identity, for integers $H,L$ with $|H|\le B$,

$$\boxed{[H+L\ge0]=[L\ge B]
+\sum_{t=-B}^{B-1}[L=t]\,[H\ge-t].}$$

If $L$ is above or below the displayed range the value is constant; inside it only one slice contributes. The right side describes what the gate does, not an implementation that pays for each product. The left side implements the whole expression with one raw gate.

Thus the table test may change from slice to slice while sharing both the table normal and the mixed address normal. An independent two-gate slice compiler can overcount badly if its thresholds line up diagonally in this way. The same observation applies with integer slopes and offsets in $H+\lambda L-\theta$.

A concrete design problem is to build an all-table decoding identity in localized atoms and then organize its nonzero terms into a small number of such diagonal patterns. Any address-only baseline such as $[L\ge B]$ must be cancelled or included in the gate count. Incompatible normals cannot be merged just because their thresholds have a convenient ordering. Different table code rows can share a diagonal only if they really are thresholds of the same affine table form.

The prior modular rank construction already exploits one special form of sharing. Its failure for a few periodic channels is a reason to let the table normals, address normals, and offsets vary per packed group, and to permit dense table rows. It is not evidence that such a more flexible family is feasible. The new observation here is the explicit multi-slice interpretation and its connection to adaptive slabs; there is no claim of novelty priority for these elementary identities.

## 4. Choosing masks that cannot hide a common simple orientation

A nominally mixed design can still depend on only two shared statistics per block, or become few-run after reordering coordinates. For $m=2^h$, consider all Walsh sign masks

$$\sigma_r(j)=(-1)^{r\cdot j},\qquad r,j\in\mathbb F_2^h.$$

For any two distinct columns $j,j'$, exactly half the rows have different signs there. Consequently, under any ordering of the columns and any common bit reorientation,

$$\sum_r\bigl(\text{number of sign changes in row }r\bigr)
=\frac{m(m-1)}2.$$

At least one row has at least $(m-1)/2$ changes. Common bit flips merely interchange which half of the masks change across an adjacent pair, leaving the count intact. Positive row-dependent magnitudes do not affect this argument.

These masks are a useful ingredient for the adaptive-slab or packed-gate architecture. They certify that a family containing all of them does not have a common bounded-run orientation. They do not certify that it computes Andreev or that every gate is sufficiently useful.

For a candidate generator, the table-code index can also choose the mask, rather than allocating all $m$ masks separately to every Fourier character. At balance $N\ge m$, so the $N$ table-row indices already suffice to expose all Walsh masks. Additional gate indices can control offsets, a second table character, and positive magnitudes such as 1 and 3. Fixed unequal scales across blocks and varying supports avoid accidentally forcing every address row to have full support with one global magnitude, a class excluded in `swarm/up2`.

The resulting generator has enough freedom to evade the specific inherited assumptions: dense table normals, many mask directions, varying magnitudes, row-specific offsets, and joint table-dependent selection. This is a design checklist for a candidate construction, not a proof that these freedoms are sufficient. In particular no unrestricted circuit upper bound follows from a mask family alone.

## 5. Shared correction and comparator routes

The preceding ETH investigation remains relevant. A Fourier-supported correction of rank $r$ costs $O(rn)$ through the existing exact product compiler, but its main term still contains shifted lookups. The productive additional question is whether the main term and correction can share adaptive or diagonally packed gates. Merely choosing mixed masks in the residual does not make the main term cheaper.

The exact $m=2$ comparison-count construction also remains a model: its unwanted strict comparisons cancel to a raw affine function, leaving the requested bit at equality. A generalization needs another identity making the total nuisance contribution affine or cheaply realizable. Pairing all columns still costs $N^{\lceil m/2\rceil}$ and is unusable at balance. Calling the comparison targets permutations is insufficient without specifying their raw affine forms, the exposed table code, and the cancellation count. This pass establishes no new cancellation identity of that strength.

These routes are distinct from adding copies of a coherent circuit or introducing mixed gates that cancel to zero. The intended mixed gates must carry useful joint table/address information.

## Verification and limits

`python3 experiments/noncoherent_routes/verify.py` uses only the standard library and writes `verification.json`.

It checks all 4,096 raw inputs of $A_{2,4}$ for each explicit mixed odd-weight circuit, including the staircase gate outputs and the absence of a common coherent reorientation. It checks the adaptive slab on 1,312 integer pairs, diagonal packing on 475 pairs, all 384 order/reorientation combinations for the four-column Walsh masks, and 651 distinct-column checks for larger masks. The symbolic proofs explain their general scope.

These are exact arithmetic checks of building blocks and baseline circuits. This initial pass had no fitted solver certificate. The linked follow-up adds finite certificates, but neither pass establishes a new finite gate record, improved asymptotic bound, or independent formal verification. No manuscript changes are warranted by these results.
