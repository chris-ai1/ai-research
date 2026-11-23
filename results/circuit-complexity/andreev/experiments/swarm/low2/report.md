# LOW2 research report: unrestricted exact Andreev lower bounds

Authors: Christian Reitwiessner

## Final status

**No unrestricted $n^{3/2+\varepsilon}$ lower bound was obtained.** The strongest own exponent statement is the proved extension $\widetilde\Omega(n^{32/19})$ to circuits with nonnegative table-to-output paths, despite arbitrarily dense table normals and arbitrary mixed-sign address weights (§4). With individually bounded integer address normals it gives $\widetilde\Omega(n^2)$. The slicing exponent itself is inherited from Sauermann–Xu; the owner-slab extraction is the additional reduction. LOW1 and UP2 checked it, and exact finite checks passed.

The unrestricted research produced exact common-score obstructions: a positive dependence of 56 nonzero oriented rectangle rows (§5.1), and Fourier interpolation duals (§7). My polynomial random-central-pool theorem (§8) is superseded, for even address dimension, by UP2's stronger all-threshold radial-kernel dual (§8.6), which I audited. UP2 subsequently superseded both random-pool results with a deterministic pairing proof giving $2^{m\lfloor k/2\rfloor}$ gates for the full-support equal-magnitude address class (§8.7); I checked that proof too. Together with LOW1's geometric/joint-entropy construction, these results separate the known proof relaxations from actual top-score feasibility. None changes the unrestricted exponent.

The best next target is an asymptotic forced positive dependence among oriented table/address rectangle rows for arbitrary small direction libraries, allowing circuit-dependent weights concentrated on rare inputs. The exact finite certificates give a concrete condition to pursue; no such universal theorem is claimed.

## Restart and scope

This is the OpenAI Astra restart of LOW2, 2026-11-11. The target is an exponent above $3/2$ for unrestricted exact depth-two threshold circuits computing ordinary Andreev's function. No additional agents are used and the shared paper is not edited. All mathematical claims below will be explicitly labelled; an unproved proposed route is not a lower bound.

[KNOWN, COMMON.md] Balanced parameters are $N=2^k=km$ and $n=2N$. Known unrestricted bounds are $\widetilde\Omega(n^{3/2})$ and $O(n^2)$. Constant error has exponent $3/2$, so any improvement must use exactness. Per-gate restriction-survival counting and ordinary bipartite communication measures do not suffice.

[KNOWN, user correction] Drift conclusions apply only to eligible blocks whose weights are globally comparable with the maximum address weight; eligibility can be empty. The corrected review_coherence report and paper Section 6, Theorem 12, will be used rather than any broad zero-sum assertion.

## Work log

- Read COMMON.md and the initial shared board. Loading the corrected coherence review and research state before proposing candidate lemmas.

## 1. Exact cone feasibility and why correlation is insufficient

[KNOWN, finite separation / Farkas; compare one_table_bit/report.md §6.2] For a fixed bottom library let $\Phi(x,a)$ contain the constant, every raw input, and every bottom gate. Put $y=2A-1$. Exact computation with arbitrary top weights is equivalent to $w\cdot y\Phi\ge1$ on the finite input set: any weak-positive/strict-negative threshold realization can first shift its intercept by less than the least negative gap, and then scale the positive minimum margin. The equivalent obstruction is a probability measure $\mu$ with $\mathbb E_\mu[y\Phi]=0$. Necessity follows by averaging a positive margin; sufficiency is finite-dimensional separation. This is a general tool, not a new theorem or exponent.

[CONJECTURE, posted to board] Seek circuit-dependent exact annihilating measures supported on rare tables and addresses. This evades marginal gate-survival accounting because it tests one jointly realizable top score; it uses no communication partition. It is compatible with the constant-error upper bound because its support need not resemble the uniform law. It is not a proposed large natural property of arbitrary Boolean functions. The missing step is constructing such a measure for **every** library of fewer than $n^{3/2+\varepsilon}$ unrestricted gates. Tiny individual correlations do not replace exact annihilation when top weights are unbounded.

[KNOWN / guardrail] Slicing every hypercube edge is not sufficient for top-score feasibility: coordinate thresholds slice every edge, but their affine span cannot sign-represent parity on two or more coordinates. Uniform parity-signed mass annihilates all their features. This already appears in the archived one-table-bit report; it is not claimed as new.

## 2. A rare-table attack on the literal masked truncation score

[PROVED; specialization of the inherited hard-clipping obstruction, not a new lower bound] UP1 proposed

$$P=2RX_\varnothing+\sum_{r=1}^R\sum_{S\ne\varnothing}\eta_{r,S}\bigl(f_W(X_S+D_{r,S})+f_W(X_S-D_{r,S})\bigr),$$

where $f_W(u)=(-1)^u u[|u|\le W]$ and $D_{r,S}=|a_S\oplus z_{r,S}|-\lfloor |S|m/2\rfloor$. If $W<N-\lceil km/2\rceil$, this fails for every $R$ and every choice of masks. Choose a nonempty $T\subseteq[k]$ and table signs $\xi_c=\chi_T(c)$. Walsh orthogonality gives $X_T=N$ and $X_S=0$ for $S\ne T$. The bound $|D_{r,T}|\le\lceil |T|m/2\rceil$ implies $|N\pm D_{r,T}|>W$, so the $T$ contribution vanishes. For all other $S$, oddness of $f_W$ gives $f_W(D)+f_W(-D)=0$. The free term is zero as well. Hence $P\equiv0$, while lookup is the nonconstant parity $\chi_T(b)$. At balance this rules out every $W=o(N)$ literal aggregate, irrespective of mask count.

Barrier audit: this uses a fully structured, uniformly rare table, not survival or communication; uniform average-case guarantees do not protect that table. The full $5n^2/16$ construction retains the missing tails and is unaffected. The one-table-bit kernel construction does not have this scalar truncation form. The truncated average-case circuit is allowed to fail here. Posted as ATTACK to UP1; table-side repairs remain possible and are not excluded.

## 3. Dense syntactically table-monotone circuits: candidate reduction

[CONJECTURE / proof under audit, posted to board] Consider circuits whose top score is coordinatewise monotone in the table **syntactically**: after complementing bottom outputs to make $v_j\ge0$, all $\alpha_{jc}\ge0$, and all raw table coefficients $u_c\ge0$. This permits arbitrarily dense table normals and arbitrary real mixed-sign address normals. It is not a normalization of arbitrary Andreev circuits.

The candidate reduction extracts private nonnegative slab kernels from dominant table coefficients. For gate $j$ write $A_j=\sum_c\alpha_{jc}$. There is at most one $d$ with $\alpha_{jd}>A_j/2$; call it the owner. For owned gates put

$$h_j(a)=[A_j-\alpha_{jd}<\theta_j-\gamma_j\cdot a\le\alpha_{jd}],\qquad K_c(a)=u_c+\sum_{j:\mathrm{owner}(j)=c}v_jh_j(a).$$

Compare the actual scores on $e_c$ and $\mathbf1-e_c$. For owned $j$ the difference is $h_j$ if $c=d$, and is at most $-h_j$ otherwise: the negative slab $(\alpha_{jc},A_j-\alpha_{jc}]$ contains the positive owner slab $(A_j-\alpha_{jd},\alpha_{jd}]$. For unowned $j$ the difference is nonpositive. Correctness gives $D_{b(a)}(a)>0$, while these pointwise inequalities give

$$D_c(a)\le K_c(a)-\sum_{d\ne c}K_d(a).$$

Thus $K_{b(a)}>\sum_{c\ne b(a)}K_c$ everywhere. This converts many-table-bit gates into private dominating slab kernels without an activity estimate. The known matching/table-pair slicing argument should give $S\ge(N/4)\operatorname{slice}(m)=\widetilde\Omega(n^{32/19})$. Full tie-safe proof, exact checks, novelty audit and peer objections are pending before promoting this to PROVED.

Barrier audit: random signed-table normals are excluded by the stated syntactic monotonicity; random mixed address signs are still allowed, so a marginal survival proof would still stop at $3/2$. Extreme complementary tables, which are exponentially rare under the uniform table distribution, supply exact inequalities. No communication lower bound is used. This is not a largeness/natural-property argument. The unrestricted quadratic Fourier circuit uses signed table coefficients and is outside the restricted class. The one-table-bit bound is the inherited downstream ingredient, not a claimed rediscovery.

## 4. The private-kernel theorem, now proved

[PROVED; new application/reduction within this investigation, no exhaustive novelty claim] Let $S_+$ be the number of table-reading gates in an exact circuit for $A_{k,m}$ satisfying the syntactic table-monotonicity hypotheses of §3. Address-only gates may be arbitrarily numerous and have arbitrary real top weights; they cancel in all comparisons. Then

$$S_+\ge\frac N4\operatorname{slice}(m)
 =\Omega\!\left(\frac{Nm^{13/19}}{\log^{32/19}m}\right)
 =\widetilde\Omega(n^{32/19})$$

at balance. In fact the bound counts just the gates with an owner. For bounded integer address normals (each gate individually rescalable to entries in $[-C,C]$),

$$S_+\ge \frac{Nm}{16C}.$$

The geometric exponents and bounded-normal inequality are inherited from Sauermann–Xu, not newly proved here. The extension is from one-table-bit gates to arbitrarily dense table normals under a sign restriction on every table-to-output path.

### Complete proof

Write the score as

$$F(x,a)=q(a)+\sum_cu_cx_c+\sum_jv_j[\alpha_j\cdot x+\gamma_j\cdot a\ge\theta_j],$$

with $v_j,u_c,\alpha_{jc}\ge0$ for table-reading gates; $q$ contains all table-independent score terms. Complementing a bottom output with negative $v_j$ makes its top coefficient positive, with a threshold adjusted on the finite domain to implement the complement including ties. The hypothesis requires that the resulting table coefficients are nonnegative. This simultaneous sign condition is substantive, not WLOG.

Let $A_j=\sum_c\alpha_{jc}$ and $T_j(a)=\theta_j-\gamma_j\cdot a$. The contribution of gate $j$ to $D_c=F(e_c,a)-F(\mathbf1-e_c,a)$ is

$$v_j\bigl([\alpha_{jc}\ge T_j]-[A_j-\alpha_{jc}\ge T_j]\bigr).$$

If every coefficient is at most $A_j/2$, this is nonpositive for every $c$. Otherwise there is a unique owner $d$ with $\alpha_{jd}>A_j/2$. Define

$$h_j(a)=[A_j-\alpha_{jd}<T_j(a)\le\alpha_{jd}].$$

For $c=d$ the difference equals $v_jh_j$. For $c\ne d$, $\alpha_{jc}\le A_j-\alpha_{jd}<\alpha_{jd}\le A_j-\alpha_{jc}$, so whenever $h_j=1$ the difference is $-v_j$; otherwise it remains nonpositive. Therefore with

$$K_c(a)=u_c+\sum_{j:\operatorname{owner}(j)=c}v_jh_j(a)\ge0$$

we have $D_c\le K_c-\sum_{d\ne c}K_d$. If $b(a)=c$, the two compared circuit outputs are one and zero, so $D_c>0$ even with the usual weak-positive/strict-negative threshold convention. Hence

$$K_{b(a)}(a)>\sum_{c\ne b(a)}K_c(a).$$

Fix a block index $i$. Pair the $N$ table labels as $\{c,c\oplus e_i\}$ and fix all other address blocks to their common parity values. For a pair $\{c,d\}$, $K_c-K_d$ is strictly positive when the live block parity selects $c$, and strictly negative when it selects $d$. It is a constant plus the slab indicators owned by $c$ or $d$, each slab being the difference of two raw halfspaces. Every live-cube edge must change at least one of those halfspace outputs, otherwise the score would have equal endpoint values despite opposite strict signs. Each halfspace threshold can be moved slightly without changing its finite Boolean truth table, ensuring that every changed edge is sliced in its interior. Thus

$$2(s_c+s_d)\ge\operatorname{slice}(m),$$

where $s_c$ counts gates owned by $c$. Summing the $N/2$ disjoint pairs proves the first inequality. By [Sauermann–Xu, *Improved lower bound for hypercube edge slicing*, Theorem 1.1](https://arxiv.org/html/2510.16592v1), $\operatorname{slice}(m)=\Omega(m^{13/19}/\log^{32/19}m)$. By their [*Nondegenerate hyperplane covers of the hypercube*, Corollary 1.2](https://arxiv.org/html/2507.00773v2), the bounded-normal version is $\operatorname{slice}_C(m)\ge m/(4C)$, proving the second display. These primary theorem statements were read directly.

The kernels also yield an explicit reduction to the one-table-bit model. For an owned gate set $\Delta_j=2\alpha_{jd}-A_j>0$ and

$$g'_j(x_d,a)=[\Delta_jx_d+\gamma_j\cdot a\ge\theta_j-(A_j-\alpha_{jd})].$$

Then $g'_j(1,a)-g'_j(0,a)=h_j(a)$ and

$$(2x_d-1)h_j(a)=2g'_j(x_d,a)-g'_j(0,a)-g'_j(1,a).$$

The score $\sum_c(2x_c-1)K_c(a)$ therefore uses one table-reading bottom and two address-only bottoms per owned gate, plus free table-affine terms. Dominance makes its sign exactly the selected table bit. The original dense table coefficients need not be sparse or globally comparable to anything.

### Checks, limits and attribution

[VERIFIED] `verify_monotone.py` checks 443,180 coordinate inequalities over all coefficient vectors in $\{0,1,2,3\}^r$, $2\le r\le6$, at every relevant threshold atom and intervening interval, plus 2,496 exact three-gate conversion identities. Threshold arithmetic is rational, including boundary equalities. LOW1 independently checked the containment and sign steps on the board. These finite checks support the proof but are not its asymptotic justification.

[REFUTED extension] The owner argument cannot be extended merely by allowing signed table normals: $\alpha=(1,-1,1,-1)$, $T=0$ gives the gate-difference vector $(1,-1,1,-1)$, with two positive entries sharing one gate. For larger balanced sign vectors it gives $\Theta(N)$ positive entries. The unrestricted exact and truncated Fourier circuits use precisely such mixed table directions, so the theorem does not constrain them. Raw $u_c\ge0$ is also used: otherwise the extracted $K_c$ can be negative and pairwise dominance no longer follows from the displayed inequality.

A targeted archive/web search found no occurrence of this particular owner-slab extraction; that is not an exhaustive priority determination. The one-table-bit lower bound and its $32/19$ exponent were explicitly inherited and must not be advertised as new here. This is the strongest proved model extension from this run so far, not progress on the unrestricted exponent.

## 5. Global feasibility is stronger than four-point collisions

[KNOWN from LOW1's concurrent work] LOW1 produced $\widetilde O(N)$ complete ladders on $Q_i(x)+L_i(a_i)$ passing every isolated table-swap parity representation for every background. A four-input signed rectangle detects their failure to share one top gate. The detailed construction is in `../low1/report.md` §2. It answered LOW2's request for a concrete library and shows that local pairwise realizability is substantially too weak.

[VERIFIED EXACT FINITE CERTIFICATE] `dual_probe.py` generated dense signed-input $\pm1$ libraries for $A_{2,2}$. A selected 64-bottom library passes **all** four-input table-pair/address-pair collision tests but still admits no top score. `dual_certificate.json` supplies 63 inputs with strictly positive rational masses, summing to one, such that

$$\sum_t\mu_t(2A(x_t,a_t)-1)\Phi(x_t,a_t)=0$$

for every bottom, every raw input and the constant. `certify_dual.py` reconstructs the rational basic solution by exact elimination and checks every equality, positivity, normalization, and every candidate rectangle. It uses only the Python standard library. A four-point collision here means an incomparable table pair $x,x'$ and labels with opposite forced differences for which $g_j(x,a)-g_j(x',a)=g_j(x,a')-g_j(x',a')$ for all bottoms. None exists in the selected library; this does not exclude other shapes of small certificate.

The LP search itself is floating point; its 64-bottom obstruction was promoted to exact only after rational reconstruction. Other numerical library results in `dual_probe.json` are diagnostic, not asymptotic claims. In particular 64 is not a lower bound for $A_{2,2}$, which has a different known 3-bottom exact circuit. The observation identifies the need for constraints combining different table pairs; it does not yet supply a uniform family lower bound.

## 6. Fast candidate triage: why the other proposed routes did not yield an exponent

Each item is a specified failure, not a claim that all methods in a broad area are impossible. All remain compatible with the quadratic exact circuit, the one-table-bit kernel circuit, and the truncated average-case circuit.

### 6.1 Threshold degree and rational numerator degree

[PROVED elementary observation; no novelty claim] Ordinary Andreev has threshold degree exactly $km+1$. In signed table coordinates $\xi_c$, its exact Fourier expansion is linear in the table and has address degree at most $km$, giving the upper bound. Set the original table bits to $x_c=y\oplus |c|$, a literal substitution in the single live bit $y$. The resulting target is parity on $km+1$ bits, whose threshold degree is $km+1$: a lower-degree polynomial has zero correlation with the full character, whereas a strictly correct sign polynomial has positive correlation. Substitution cannot increase degree. This proves the lower bound.

[DEAD-END] A target obstruction consisting only of polynomial threshold degree therefore sees $\Theta(n)$ at balance, a value already achieved by parity with $O(n)$ threshold gates. Clearing a positive rational denominator gives the same numerator sign obstruction. Degree alone supplies no table factor $N$ and no separation from this linear-gate example. Classical [Paturi–Saks, *Approximating Threshold Circuits by Rational Functions*](https://doi.org/10.1006/inco.1994.1059) explicitly assumes polynomially bounded weights for its strong wire application; the primary publisher abstract was inspected, while full-text access returned HTTP 403. No stronger unrestricted-weight statement was imported. A rational route involving weight, simultaneous table coordinates, or special numerator structure remains conceivable, but no such invariant was proved.

Barrier audit: degree uses exactness and avoids ordinary communication, but cannot beat the linear parity example even before confronting the survival barrier. The known approximate circuit may have high exact degree, so approximate degree cannot simply replace exact degree in this calculation. No natural-proofs claim is involved.

### 6.2 Ordinary sign-rank after restriction, and multi-party repartitioning

[DEAD-END, elementary monotonicity] Restricting rows and columns of a communication matrix cannot increase its communication complexity or sign-rank. A fixed substitution assigning each new variable to only one party also preserves the inherited protocol. Thus a restriction cannot destroy the $O(k)$ protocol in the sense needed to evade it. A projection mixing variables across parties would require a new reduction and would generally fail to preserve raw threshold gates. The brief's suggestion of a submatrix whose restriction destroys the low protocol is therefore not a viable route as stated.

[PROVED elementary observation] Even the natural many-party partition is cheap: each of the $k$ address-block parties sends its parity to the table party, which outputs the selected bit. The exact tensor has the expansion

$$A(x,a_1,\ldots,a_k)=\sum_{c\in\{0,1\}^k}x_c\prod_{i=1}^k[|a_i|\bmod2=c_i],$$

of tensor rank at most $N$. This does not exclude sophisticated tensor norms, but shows that passing from matrices to this ordinary tensor does not create a hidden $Nm$ rank. Arbitrary threshold features can themselves have high rank; no low per-gate tensor rank was established. These arguments do not exploit rare inputs, so they do not explain why exact complexity should exceed the approximate $3/2$ exponent.

### 6.3 Wire-to-gate conversion and dense gates

[DEAD-END, exact accounting] For $S$ bottom gates on $n$ raw inputs, including the top input wires,

$$W\le(n+1)S+n.$$

Consequently the known $\widetilde\Omega(n^{5/2})$ wire lower bound gives only $\widetilde\Omega(n^{3/2})$ gates. Forcing gates to be dense does not improve this inference: that is the regime closest to the upper bound $W\asymp nS$. To obtain a larger gate exponent by this route, one needs an **upper** bound on the useful average fan-in in a hypothetical small correct circuit, or a new larger wire lower bound. Random signed dense gates and the dense Fourier construction show why sparsity cannot be assumed. This conversion also inherits the approximate-computation barrier of the original wire bound.

### 6.4 Topology of the continuous extension

[REFUTED naive inference] The $2^{M-1}$ positive vertices of $M$-bit parity do not force $2^{M-1}$ connected positive components in a real extension. A score depending only on $\sum_i a_i$, with alternating signs on integer layers, computes parity using $O(M)$ threshold gates. Its positive regions can be entire connected slabs between successive half-integer hyperplanes. Boolean vertices of equal Hamming weight are connected through non-Boolean points inside such a slab. Therefore counting Boolean islands as Betti components is invalid without an additional constraint on the extension.

[DEAD-END so far] A literal straight line contains at most two Boolean-cube vertices. Long Boolean chains are polygonal, and a mixed-sign linear form is a signed prefix walk on them, not a one-crossing function. Replacing raw addresses by count vectors restores straight lines only for block-symmetric gates, where the inherited coherent theorem already applies. No unrestricted topological invariant surviving these issues was obtained. These precise failures are compatible with random signed gates and do not rely on uniform-error approximation.

### 6.5 Truth-table compression and fixed feature dimensions

[KNOWN / concurrent UP2 result] Pure threshold-shift counting yields only roughly one parameter per table bit, not the desired address replication factor. UP2 sharpened the low-dimensional special case: if the table normals span dimension $r$, then

$$2^N\le(N+1)\sum_{i=0}^r\binom{NS}{i}.$$

I checked simultaneous strictification and the free raw table term. In a fixed bottom-pattern cell, that term is one scalar and contributes at most $N+1$ output patterns across fixed representatives of the $N$ labels. Thus polynomial size needs $r=\Omega(N/\log N)$. The full-rank Walsh directions of the exact and approximate constructions satisfy this requirement. No extra gate exponent follows for unrestricted rank. The proof belongs to UP2; it is not a LOW2 result.

[DEAD-END] A small threshold circuit does not by itself compress an arbitrary table below $N$ bits: weights are arbitrary reals, there are at least $N$ relevant degrees of freedom in the known constructions, and a valid information argument must count realizable patterns rather than the written numeral length. Similarly the De Morgan formula lower bound cannot transfer without a proved simulation that counts the top threshold's duplication of bottom formulas. No simulation strong enough for a gate exponent above $3/2$ was established; no contradiction with the known formula bound is claimed.

### 6.6 Symmetry averaging and tiny correlations

[DEAD-END] Averaging an exact dual over block permutations preserves its annihilation equations only if the feature library is stable under those permutations (or all orbit equations were already imposed). An arbitrary mixed-sign bottom library has no such invariance. Averaging the **score** over all parity-preserving input symmetries does preserve correctness, but can introduce the entire orbit of every gate, with no controlled size. Likewise a small nonzero correlation does not give a dual annihilator when the top weights can be scaled without bound. These are the concrete obstacles to the first cone proposal; the finite 63-point certificate is evidence of a missing collective invariant, not a general construction of one.

### 6.7 Formula and projection amplification

[DEAD-END / missing reduction] Identifying raw variables or replacing them by literals preserves threshold gates; assigning table entries nonlinear functions of new variables generally does not. Thus embedding a hard table generated by parities, products, a code, or a small formula must charge the new composition depth. Ordinary Andreev's formula lower bound and lower bounds for modified/code-based Andreev functions do not transfer automatically to this target. No model-preserving embedding with a stronger gate bound was found. Exactness alone does not repair a depth violation.

### 5.1 Positive dependence entirely within oriented rectangles

[VERIFIED EXACT; requested by LOW1] For the same 64-bottom library, build every row

$$R(x,x';a,a')=g(x,a)-g(x',a)-g(x,a')+g(x',a')$$

with selected table differences $x_{b(a)}-x'_{b(a)}=1$ and $x_{b(a')}-x'_{b(a')}=-1$. Exact correctness forces $v\cdot R>0$, and all free affine top terms cancel. There are 1,536 such rows with a fixed convention ordering the table pair; every row is nonzero. Nevertheless 56 rows have strictly positive rational coefficients, summing to one, whose weighted vector sum is zero. The complete certificate is `oriented_certificate.json`, recovered and checked by `oriented_probe.py` using exact rational elimination after floating-point support discovery. Thus even without four-point collisions, the **cone of oriented rectangles** can refute a whole library. This is stronger structure on the certificate than §5's unrestricted input dual, but still finite-model evidence, not a general lower-bound exponent.

LOW1 independently proved that $O(n^{3/2})$ random dense majority libraries can satisfy every un-oriented table-pair/address-edge nonconstancy demand. Our positive-dependence certificate addresses exactly the missing shared-orientation condition and therefore does not conflict with that barrier. An asymptotic forced-dependence theorem for arbitrary small libraries is still missing.

## 7. A Fourier dual that can remove top-weight bounds for a fixed library

[PROVED criterion; application to general libraries remains CONJECTURE] Fix a table for which the target on raw address signs is $\chi_T$, with $|T|\ge2$. Let $\mathcal U$ be any collection of other address subsets with $|U|\ge2$. For a fixed bottom library define $a_j=\widehat g_j(T)$ and $L_{Uj}=\widehat g_j(U)$. If

$$a=L^\top\lambda,\qquad\sum_{U\in\mathcal U}|\lambda_U|<1,$$

then no affine combination of those bottoms and raw inputs sign-computes $\chi_T$.

*Proof.* For a strict sign-correct score $F$, $\widehat F(T)=\mathbb E|F|>0$, while $|\widehat F(U)|\le\mathbb E|F|$. All free affine top features have zero Fourier coefficients at $T$ and at every $U\in\mathcal U$. Hence

$$\widehat F(T)=\sum_U\lambda_U\widehat F(U)\le\|\lambda\|_1\widehat F(T)<\widehat F(T),$$

a contradiction. Equivalently the positive probability distribution

$$\mu(a)=2^{-M}\left(1-\chi_T(a)\sum_U\lambda_U\chi_U(a)\right)$$

annihilates all label-signed features, where $M=km$ and $T\notin\mathcal U$ ensures normalization. This dual is exact and has no top-weight restriction. It is a standard Fourier/separation construction, not a claimed new general lower-bound technique.

[CONJECTURE, posted to UP2] For full-support equal-magnitude address rows, their Fourier coefficients have the form $c_{j,|U|}\prod_{i\in U}\sigma_{ji}$. UP2's small middle-degree coefficient bound alone yields only top-variation/margin hardness. If low-degree moment rows interpolate that middle-degree row with $\ell_1$ norm below one, the criterion above would remove the top-weight assumption. Random well-conditioned sign moment matrices are a possible test family.

[OBSTACLE] A uniform conditioning claim is false without additional assumptions: repeated directions can be arbitrarily ill-conditioned, and extreme-threshold gates (for example a point indicator) have equally tiny coefficients at **all** Fourier degrees. Therefore dividing an exponentially small middle-degree coefficient by a presumed polynomial lower singular value is not justified for unrestricted thresholds. This is the exact missing ingredient, not an overlooked margin normalization.

### 7.1 Exact proof of principle for the Fourier criterion

[VERIFIED EXACT FINITE] `fourier_probe.py` computes symmetric-threshold Fourier coefficients by the exact integer Krawtchouk sum

$$2^M\widehat h(U)=\sum_{u=0}^{|U|}\sum_{v=0}^{M-|U|}(-1)^u\binom{|U|}{u}\binom{M-|U|}{v}[u+v\ge t],$$

then multiplies by the product of the coordinate-mask signs on $U$. For a fixed 24-gate pool on $M=12$ variables, with central threshold counts between 5 and 8, it finds and exactly reconstructs a representation of the six-variable target-character row using 24 rows of degree two or three. Its coefficient norm is

$$\|\lambda\|_1=\frac{13921289}{25109631}<1.$$

Every interpolation equation is checked with rational arithmetic. `fourier_certificate.json` contains the masks, thresholds, target, selected subsets and exact coefficients. Therefore this particular full-support mixed-sign library cannot sign-compute that character with **any** real top weights or affine direct terms. Larger tested pools are only numerical diagnostics in `fourier_probe.json`, not exact certificates or asymptotic theorems. This evidence supports investigating moment interpolation, but does not establish a new gate exponent in a model.

## 8. Polynomial random central-majority pools cannot compute middle-degree parity

[PROVED below; new derivation in this run, literature priority unestablished] Fix any constant $p>0$. Let $M$ tend to infinity, $S\le M^p$, and let $\sigma_1,\ldots,\sigma_S$ be independent uniform vectors in $\{\pm1\}^M$. With probability $1-o(1)$ over these masks, the following holds **simultaneously for every choice** of integers

$$M/4\le t_j\le3M/4,$$

and every $T\subseteq[M]$ of size $\lfloor M/2\rfloor$: no arbitrary real affine combination of the gates

$$g_j(a)=[|a\oplus z_j|\ge t_j],\qquad (-1)^{z_{ji}}=\sigma_{ji},$$

and the raw inputs sign-computes $\chi_T(a)$. Thresholds may be chosen after seeing all masks. The result imposes **no bound** on the top coefficients or normalized margin.

This is an asymptotic exact-feasibility theorem for a random-direction model with non-extreme thresholds, not a lower bound for unrestricted ordinary Andreev. In an Andreev circuit with these random full-support address normals, it implies that exact correctness on a middle-character table requires at least one threshold outside the stated interval (or another address direction). It does not control how such exceptional gates combine. A polynomial ordinary-Andreev lower bound does not follow merely by calling thresholds extreme.

### 8.1 Low-degree mask columns have uniformly small coherence

Choose a fixed integer $r\ge2$ with $r>2p$; for large $M$ it is smaller than $\lfloor M/2\rfloor-1$. Let $\mathcal U$ contain all subsets of sizes $r$ and $r+1$, and let $q=|\mathcal U|$. By the elementary Rademacher tail bound and a union bound over the at most $M^{2p}$ mask pairs, with probability $1-o(1)$,

$$|\langle\sigma_j,\sigma_l\rangle|\le C_p\sqrt{M\log M}\quad(j\ne l).$$

Condition on this event. For $z_i=\sigma_{ji}\sigma_{li}$, put $s=|\sum_i z_i|$. Flipping all $z_i$ changes a degree-$d$ monomial sum only by a sign, so assume its sum is $s\ge0$. The generating polynomial is

$$\prod_{i=1}^M(1+z_i u)=(1-u^2)^{(M-s)/2}(1+u)^s.$$

Consequently for each fixed $d$,

$$\left|\sum_{|U|=d}\prod_{i\in U}z_i\right|
\le\sum_{b=0}^{\lfloor d/2\rfloor}\binom{(M-s)/2}{b}\binom{s}{d-2b}
\le C_d(\sqrt M+s)^d.$$

After division by $\binom Md$, the normalized degree-$d$ mask-column inner product is at most

$$\delta_d=O_{p,d}\bigl((\log M/M)^{d/2}\bigr).$$

This applies at both $d=r$ and $d=r+1$.

### 8.2 Consecutive low Fourier levels cannot both vanish

For the unmasked Hamming threshold $h_t=[|a|\ge t]$, let $c_{t,d}$ denote its Fourier coefficient at any size-$d$ subset. A coordinate difference gives exactly

$$c_{t,d}=-2^{-M}\binom{M-1}{t-1}
\frac{K_{d-1}(t-1;M-1)}{\binom{M-1}{d-1}},$$

where

$$K_s(x;n)=\sum_{u=0}^s(-1)^u\binom xu\binom{n-x}{s-u}$$

is the integer Krawtchouk polynomial at the integer argument $x$. In particular $|c_{t,1}|=2^{-M}\binom{M-1}{t-1}$. The recurrence

$$sK_s(x;n)=(n-2x)K_{s-1}(x;n)-(n-s+2)K_{s-2}(x;n)$$

for $s\ge2$, together with $K_0=1$, shows that $K_{r-1}$ and $K_r$ cannot both vanish when $r\le n$. Otherwise recurrence downward forces $K_0=0$. At least one is a nonzero integer, of absolute value at least one. Therefore

$$\max\{|c_{t,r}|,|c_{t,r+1}|\}\ge |c_{t,1}|/M^r.$$

Let $H_2$ denote binary entropy. Uniformly for the stated threshold interval, the elementary binomial entropy estimate gives

$$|c_{t,1}|\ge 2^{-(1-H_2(1/4))M-O(\log M)}.$$

The exact values of the polynomial factors will not matter. Here $H_2(1/4)>1/2$ is essential.

### 8.3 Conditioning is uniform over adaptive thresholds

Let $L$ be the $q\times S$ matrix of Fourier coefficients at $U\in\mathcal U$. Its column $j$ has entries

$$L_{Uj}=c_{t_j,|U|}\prod_{i\in U}\sigma_{ji}.$$

Write $b_j=\|L_{\cdot j}\|_2>0$ and $D_{\cdot j}=L_{\cdot j}/b_j$. Each normalized column has norm one. Its inner product with another column is a sum of the degree-$r$ and degree-$(r+1)$ mask inner products multiplied by the corresponding two normalized amplitude products. Cauchy–Schwarz in these two amplitudes bounds the sum of their absolute products by one. Hence

$$|\langle D_{\cdot j},D_{\cdot l}\rangle|\le\max(\delta_r,\delta_{r+1})=:\delta.$$

This estimate is uniform over all threshold choices and their signs/zeros. Since $S\delta=o(1)$ for $r>2p$, the Gram matrix $D^\top D$ has minimum eigenvalue at least $1-(S-1)\delta\ge1/2$ for large $M$. Moreover $b_j\ge |c_{t_j,1}|/M^r$ by §8.2.

### 8.4 Interpolating the middle-degree row with norm below one

Put $d=\lfloor M/2\rfloor$ and $a_j=\widehat g_j(T)$. Symmetry and Parseval give

$$|a_j|\le\frac1{2\sqrt{\binom Md}}=2^{-M/2+O(\log M)}.$$

Thus for $h_j=a_j/b_j$,

$$\max_j|h_j|\le2^{-(H_2(1/4)-1/2)M+O_r(\log M)}.$$

The well-conditioned full-column-rank matrix $D$ has a solution to $D^\top\lambda=h$ with $\|\lambda\|_2\le\sqrt2\|h\|_2$ (take the least-norm solution). It follows that

$$\|\lambda\|_1\le\sqrt q\|\lambda\|_2
\le\sqrt{2qS}\max_j|h_j|=2^{-\Omega(M)}<1.$$

Since $L_{\cdot j}=b_jD_{\cdot j}$, this is precisely $L^\top\lambda=a$. Section 7's exact Fourier dual proves the theorem. The mask event and all estimates are independent of the threshold choices and of the particular size-$d$ set $T$, so the claimed simultaneous quantifiers hold. No union bound over the exponentially many target characters or thresholds is needed.

### 8.5 Scope and barrier audit

This uses exact pointwise sign correctness on a structured character table, not survival counting or a communication rank. Random signed address gates can pass marginal survival and slicing tests while their common score is ruled out by this Fourier dual. Constant-error circuits are unaffected: the argument needs $\widehat F(T)=\mathbb E|F|$, which can fail under any sign errors. There is no asserted large natural property or cryptographic contradiction.

The theorem does not cover the exact quadratic circuit: its character-supported address normals are not independent full-support random masks, and its ladders range over extreme offsets. The one-table-bit kernel circuit likewise lies outside the random/full-support hypotheses. The truncated average-case construction only guarantees uniform-input error and uses per-character supports, so it is not refuted. Arbitrary real normal magnitudes, repeated normals, and unrestricted extreme thresholds remain substantial open cases. The strong conclusion for a random library must not be presented as an unrestricted exponent change.

### 8.6 Verification and supersession by UP2's stronger radial dual

[VERIFIED] `verify_fourier_identities.py` passed 4,899 exact symmetric-coefficient identities, 4,600 consecutive-level nonvanishing checks, 4,301 Krawtchouk recurrence checks, 13,377 mask generating-function identities and 300 normalized two-degree coherence inequalities. These are formula checks, not a substitute for the asymptotic argument.

[IMPORTANT SCOPE / ATTRIBUTION UPDATE] While §8 was being written, UP2 developed a stronger exact radial-kernel dual that permits **all thresholds** on polynomially many projectively separated full-sign directions (even $M$). I audited the proof on the board; LOW1 and UP1 also checked it. Thus §8 is a subsidiary derivation illustrating low-degree interpolation, not the strongest frontier for these libraries and not counted as an independent exponent improvement. A literature search found related bounded-norm/fixed-representation learning statements but did not establish novelty of §8 or UP2's theorem; no priority assertion is made.

Here is the checked mechanism, attributed to UP2. Identify raw addresses with their sign vectors for this paragraph. For $d=M/2$, put

$$\kappa_\sigma(a)=\binom Md^{-1}\sum_{|U|=d}\chi_U(\sigma)\chi_U(a).$$

At Hamming distance $t$ from $\sigma$, this is zero for odd $t$, and $(-1)^{t/2}\binom{M/2}{t/2}/\binom Mt$ for even $t$. Its absolute value is at most $1/(M-1)$ except at the center and antipode, and exponentially small at distances in $[M/8,7M/8]$. If every pair of centers is at distance in $[M/4,3M/4]$, the interpolation matrix $K_{ij}=\kappa_{\sigma_j}(\sigma_i)$ is exponentially close to identity for polynomially many centers. Solve $Kc=(\chi_T(\sigma_i))_i$ and set $P=\sum_jc_j\kappa_{\sigma_j}$. Then $P=\chi_T$ at the centers and antipodes, and $|P|<1$ everywhere else: at most one kernel can be near a center/antipode, with contribution $O(1/M)$; all remaining contributions are exponentially small. The coefficients obey $\|c\|_\infty\le2$ for large $M$.

For **every** radial gate $h_i$ around center $\sigma_i$, of any threshold,

$$\langle P,h_i\rangle=c_{i,d}(Kc)_i=c_{i,d}\chi_T(\sigma_i)=\langle\chi_T,h_i\rangle.$$

Thus the nonnegative measure $2^{-M}(1-\chi_TP)$ exactly annihilates all label-signed radial features, constants and raw inputs. Its mass is $1-\widehat P(T)>0$; divide by this mass when calling it a probability distribution. The top can be strictified on the finite cube, so nonzero mass contradicts an exact sign-correct score. Unlike my low-degree proof, this never divides by a small or zero radial coefficient. Full details and the theorem belong to `../up2/report.md`.

[COMBINED CONSEQUENCE, attribution LOW1 + UP2] On the even-$k$ balanced subsequence, polynomial iid full-sign address directions are projectively separated with overwhelming probability. LOW1's $\widetilde O(n^{3/2})$ random dense-majority library simultaneously meets every standard table-pair slicing condition and joint cube transcript entropy demand. UP2's dual nevertheless excludes any exact ordinary-Andreev circuit on that direction pool, even after arbitrary table coefficients, thresholds, top weights and repeated ladder cuts are chosen. Thus geometric coverage **and joint information** can both succeed while exact common-score feasibility fails. This is a rigorous separation of proof relaxations, not an improved unrestricted gate exponent.

### 8.7 Further supersession: UP2's deterministic full-sign pairing bound

[PROVED CHECK, theorem due to concurrent UP2 work] UP2 subsequently found a simpler, stronger argument for the entire full-support equal-magnitude address class. I audited it on the board. Fix a character table selecting $d=m\lfloor k/2\rfloor$ raw address bits and fix one address block if $k$ is odd. Pair each selected sign $z_i$ with an unselected sign $w_i$. For every $t\in\{\pm1\}^d$, impose the literal-identification restriction $w_i=t_i z_i$. The target remains parity on the $d$ live bits.

A gate with address row $G(\sigma,\tau)$ now has coefficient $G(\sigma_i+t_i\tau_i)$ on $z_i$. It involves every live bit only for the **unique** restriction $t_i=\sigma_i\tau_i$ for all $i$. On every other restriction it omits a variable and its unique multilinear polynomial has degree at most $d-1$. If no bottom involves all live bits, their affine combination, including raw top inputs, has degree less than $d$ for $d\ge2$, and hence zero full-parity correlation. Exact sign correctness, after strictification, requires positive full-parity correlation. Every one of the $2^d$ restrictions therefore requires a distinct gate:

$$S\ge2^{m\lfloor k/2\rfloor}=2^{\Omega(n)}\quad\text{at balance}.$$

This allows arbitrary table coefficients, all thresholds, arbitrary real top weights, and arbitrary repeated/full-sign directions. It does **not** allow zeros or unequal address magnitudes within a gate. Pure-table gates are irrelevant. The known quadratic construction uses character-dependent zero coefficients and is unaffected.

This theorem supersedes both my central random-pool result and the separated-direction exact infeasibility conclusion for this full-sign class. The radial dual remains an independent explicit certificate and may guide more general magnitude/support extensions; it is no longer necessary to obtain impossibility in the full-sign class. The proof is elementary enough that priority should be checked carefully; LOW2 endorses correctness, not novelty. Attribution is UP2 throughout. The unrestricted exponent remains unchanged.


## 9. Final handoff, board exchange, and artifacts

[PROVED / VERIFIED as marked above] Main own artifacts:

- `report.md`: complete proofs, hypotheses, dead ends and provenance.
- `verify_monotone.py`, `monotone_checks.json`: private-kernel extraction and conversion checks.
- `dual_certificate.json`, `certify_dual.py`: exact positive input-distribution certificate for a fixed 64-bottom library; every four-point collision test fails to detect it.
- `oriented_certificate.json`, `oriented_probe.py`: exact positive dependence of 56 nonzero oriented rows, answering LOW1's request.
- `fourier_certificate.json`, `fourier_probe.py`: exact Fourier interpolation certificate for a fixed central majority pool; other entries in `fourier_probe.json` remain numerical diagnostics.
- `verify_fourier_identities.py`, `fourier_identity_checks.json`: exact Krawtchouk, recurrence and coherence checks supporting §8.

The board was used throughout: I posted the owner extraction and Fourier criteria as candidates, supplied the character-table attack to UP1, requested explicit libraries, received LOW1's local-realizability counterlibrary, checked its stronger joint geometric/information barrier, provided an exact oriented-cone certificate, and checked UP2's table-rank, margin, dyadic and radial-dual arguments. UP1 strengthened the initial mask attack to arbitrary top weights over the whole truncated library; that stronger proof is in UP1's report. UP1 also identified that the known skew-cover theorem already gives the all-width window-cover cost, so its elementary rounding lemma is not a new cover frontier. These attributions and supersessions are retained deliberately.

No new unrestricted circuit or gate lower-bound exponent, exhaustive novelty certification, Lean formalization, or publication is claimed. All task-owned computations finished. No additional agents were created and no shared-paper files were edited.
