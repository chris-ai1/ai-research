Authors: Christian Reitwiessner

# Wire bounds for depth-two real threshold circuits

Status: completed research handoff, 2026-11-11. Literature attribution belongs to the cited authors; new deductions are labelled separately and carry no novelty claim. All seven groups of exact finite checks passed. The new asymptotic deductions are written proofs, not Lean formalizations.

Main finding: no unrestricted exact wire exponent above 2.5 was established. The strongest new transfer gives a matched exponent-three wire lower bound for blockwise bounded-integer address magnitudes, using semantic pruning and middle-cut density rather than assuming dense coefficients are essential (§5). Support-weighted character and table-pair inequalities give exponent $51/19$ in other explicitly restricted classes (§4). The unrestricted exact parity baseline is $\Omega(n^{32/19}/\log^{32/19}n)$ (§3).

## Scope and conventions

Investigate exact and uniform-average approximation of ordinary Andreev and parity by depth-two arbitrary-real threshold circuits. Wire count means nonzero aggregated edges, including input-to-output and hidden-gate-to-output edges. Coefficient multiplicity and repeated majority literals are not support wires. No implication $W\ge nS$ will be used without a density proof.

## Work log

- Created this report before starting research, as requested.
- Completed: local proof audit, all twelve preceding reports and round-three board, primary-source searches through 2026-11-11, wire incidence proofs, semantic density/pruning proof, and exact finite checks. The original provisional entries below are retained as a research log; their completed versions supersede them.

## Increment 1: verified source and two candidate wire transfers

[VERIFIED / KNOWN] Sauermann–Xu, *Improved Lower bound for hypercube edge slicing*, arXiv:2510.16592v1, Theorem 1.1 (18 October 2025), gives $h(d)>d^{13/19}/(10^{11}\log^{32/19}d)$ for sufficiently large $d$. The paper explicitly notes its depth-two parity wire consequence. Primary source: https://arxiv.org/html/2510.16592v1 . This is not a new slicing theorem.

[PROVED, classical Paturi–Saks reduction rederived] Write a strict parity score as $F(x)=b+u\cdot x+\sum_jv_jg_j(x)$. For every input $i$, the difference $F(1,y)-F(0,y)$ has alternating strict parity signs on the other $d-1$ bits. Only gates semantically depending on $i$ remain, with each yielding two LTFs; raw top terms reduce to the constant $u_i$. Therefore $2\deg(i)\ge h(d-1)$ and summing gives $W_{\mathrm{input\to bottom}}\ge d\,h(d-1)/2$. Full details and source verification pending below. This is a support/outdegree charge, not $W\ge dS$.

[CANDIDATE, being audited] LOW2's monotone-owner slab extraction and one-table-bit private kernels may yield $W\gtrsim kNm\,h(m-1)$: differentiate each pair's parity score in each live raw coordinate, charge at most four halfspaces per owner slab, and sum over disjoint label pairs and all k blocks. This would be a restricted $n^{51/19}$ exponent, retaining all raw top edges, not unrestricted progress.

[CANDIDATE, being audited] LOW1 round-three blockwise bounded-integer profile incidence gives a semantic cubic wire bound. Remove all irrelevant magnitude classes from each Boolean gate first (signed permutation symmetry makes relevance constant within a class). For every middle cut separating the resulting magnitude classes, at least $km/3$ address coordinates remain semantically essential, since zero can occur on only one cut side. Sum the profile incidence theorem only over middle cuts, charging each gate at most $2^{q-1}-1$ times. Expected result $W=\widetilde\Omega(n^3/[C2^q])$; this is a genuine density proof for a restricted class, including zeros, not general gate multiplication.

# Completed results and proofs (supersedes preliminary candidate labels above)

## 1. Definitions, counting conventions, and status

Put $N=2^k$, $M=km$, $n=N+M$, and
$$A_{k,m}(x,a)=x_{b(a)},\qquad b_i(a)=\sum_{l=1}^m a_{il}\pmod2.$$
Balanced means $M=\Theta(N)$; exact balance $M=N$ requires $k\mid2^k$, and $m=\lfloor N/k\rfloor$ suffices for all asymptotic statements. This is ordinary independent-table Andreev, not the code-based function $B_n$ or a hard language in $\mathsf E^{\mathsf{NP}}$.

A circuit score is
$$F(z)=\beta+u\cdot z+\sum_{j=1}^S v_j g_j(z),\qquad g_j(z)=[w_j\cdot z\ge\theta_j],$$
with arbitrary real coefficients, and output $[F\ge0]$. Delete gates with $v_j=0$, combine parallel edges, and remove constants when useful. Define
$$W_{\rm bot}=\sum_j|\operatorname{supp}w_j|,\quad W_{\rm raw}=|\operatorname{supp}u|,\quad W=W_{\rm bot}+S+W_{\rm raw}.$$
Thus gate-to-top wires and raw-to-top wires are charged. Biases are constants, not edges. Charging one bias edge per gate changes this by at most $S+1$. Counting only input-to-bottom wires omits exactly $S+W_{\rm raw}$, with $W_{\rm raw}\le n$. In a reduced circuit where each bottom has an essential input, $S\le W_{\rm bot}$; these alternatives preserve all superlinear exponents below. Forcing a strictly layered architecture can replace each raw top input by an identity bottom, adding at most $n$ gates and $n$ wires. The raw-input model is used directly in our proofs, so no such conversion is needed.

A variable is *essential* to a Boolean gate if some setting of all other inputs makes flipping it change the output. Let $d_j$ count essential address variables and $t_j$ essential table variables. Every representation of that Boolean gate needs at least $d_j+t_j$ input edges. We use these semantic counts where possible. Dense numerical coefficients may be irrelevant. Conversely $W\le(n+1)S+n$ is always an **upper** bound on wires in terms of gates, never a density lower bound. Integer coefficient magnitudes, bit length, top variation $\sum|v_j|$, and repeated majority literals are different resources. Splitting coefficient $b$ into $|b|$ unit literals changes multiplicity but not the single aggregated support edge.

PROVED below means a written mathematical proof, sometimes explicitly conditional on an identified prior theorem. VERIFIED means source/finite algebra inspection. No new Lean formalization, exhaustive literature-priority claim, or unrestricted exponent improvement is asserted.

## 2. Verified baselines for ordinary Andreev

[VERIFIED local theorem; formalization provenance reported by the repository] The current `threshold_paper/paper.tex`, Theorem `thm:lower`, proves
$$m^{3/2}N\varepsilon^2\le36\bigl(k+2+\ln(W+1)\bigr)W,$$
for $\varepsilon\ge3(k+2)/\sqrt N$. If $m\le N$, its explicit simplified version is
$$m^{3/2}N\varepsilon^2\le144(k+2)W.$$
Consequently
$$W=\Omega\left(\frac{\varepsilon^2 n^{5/2}}{\log^{5/2}n}\right).$$
Agreement is under uniform independent **all** input bits and equals at least $1/2+\varepsilon$. Exact computation sets $\varepsilon=1/2$, valid once $N\ge36(k+2)^2$. The analogous gate bound is $\Omega(\varepsilon^2 n^{3/2}/\log^2n)$.

The wire argument counts only bottoms depending on at least two live bits. Constants and one-variable functions are absorbed in the raw top affine form. Expected survivors are at most $4W/m^{3/2}$; fixed-direction threshold counting and a uniform-in-survivor-count correlation estimate give the displayed inequality. These finite lower-bound statements, and the earlier windowed upper bounds, are recorded as merged Lean results in the current paper. I inspected the mathematical argument and its provenance statements; I did not rebuild Lean or independently inspect remote PR status. Historical `RESEARCH_STATE.md` entries and `kw_applications.md` contain older log factors/statuses and must not override the current paper. In particular, unreviewed gate-only advantage extensions are not part of the formalized wire regime reported here.

[KNOWN literature ancestry / local correction] Kane–Williams, STOC 2016, supplies the restriction framework and earlier $\varepsilon^3n^{5/2}/\log^{7/2}n$ bound. The local `kane_williams_erratum.md` corrects the original proof's advantage range to $\varepsilon\gg\log n/\sqrt n$, and repairs ranks, zero weights, endpoints, and the absorption of one-variable gates. The newer local fixed-top and VC/Rademacher gate derivations at smaller advantage are hand proofs with their own review status. **They do not automatically extend the wire range:** absorbing literals changes the live top coefficients. This report uses only the documented wire regime.

[PROVED upper support audit] The simple formalized quadratic construction uses $2N^2+MN$ bottoms, with forms $X_T+t_T$ and $t_T$, where
$$X_T=\sum_c\chi_T(c)(1-2x_c),\quad t_T=\sum_{i\in T,l}a_{il},\quad \varphi(r)=(-1)^r r.$$
The exact identity is
$$\sum_T\bigl(\varphi(X_T+t_T)-\varphi(t_T)\bigr)=N(1-2x_b).$$
Indeed $X_T$ is even, so each summand equals $(-1)^{t_T}X_T=\chi_T(b)X_T$; Walsh orthogonality then selects the table entry $b$. The staircase expansion is the elementary identity $\varphi(z)=\varphi(\ell)+\sum_{r=\ell+1}^u(\varphi(r)-\varphi(r-1))[z\ge r]$ for integers $\ell\le z\le u$.
Every integer staircase is expanded into raw affine threshold gates. For a channel $T$ with $d_T=m|T|$, the first ladder has at most $2N+d_T$ gates of fan-in $N+d_T$, and the second at most $d_T$ gates of fan-in $d_T$. Thus this explicit unoptimized compilation has
$$W_{\rm bot}\le2N^3+\frac32MN^2+\frac12m^2k(k+1)N,$$
plus $2N^2+MN$ gate-to-top edges. At $M=N$ this is $(4+1/(2k))N^3+3N^2$. Merging identical gates and deleting constant cuts only decreases the count. Hence exact $W=O(n^3)$ is verified by actual support accounting. The current sharper $(5/16+o(1))n^2$ construction also gives $W\le(n+1)S+n=O(n^3)$; this is a valid **upper** conversion. The sharper exact score is a hand proof, not the merged Lean upper construction.

[VERIFIED current average upper; hand proof] The mean-square masked-window theorem in the current paper gives, for $0<\delta<1/2$,
$$S=O\bigl(n^{3/2}\sqrt{\log(1/\delta)}\bigr),\quad
W=O\bigl(n^{5/2}\sqrt{\log(1/\delta)}\bigr).$$
For $N^{-1/2}\le\varepsilon\le1/8$ it gives
$$S=O\bigl(\varepsilon^2n^{3/2}\sqrt{\log(1/\varepsilon)}\bigr),\quad
W=O\bigl(\varepsilon^2n^{5/2}\sqrt{\log(1/\varepsilon)}\bigr).$$
The earlier formalized window proof has $\sqrt{\log n}$ instead of the improved fixed-error factor. In either version, the fixed-positive-error wire exponent is **already 2.5**, and the $\varepsilon^2$ dependence already matches in the common documented lower-bound regime. The newer mask argument chooses a deterministic circuit nonuniformly by averaging; it does not prove efficient mask selection. It uses table fan-in $N$ and address fan-in at most $M$ per bottom, so the support-wire bound is honest. Additive raw top support is at most $N$ and is absorbed in these displayed parameter ranges.

Very small advantage needs separate endpoint accounting: one table-majority top gate has no bottoms, $N$ raw top wires, and advantage $\Theta(N^{-1/2})$. Never extrapolate a no-additive-term wire lower inequality below its stated regime. Concentration alone does not repair all rare inputs: when error is below $2^{-n}$, a deterministic Boolean circuit must be exact and the window radius in this argument becomes linear, restoring the cubic wire upper scale.

## 3. Parity: current primary-source bounds and raw-top-safe proof

Let $h(d)$ be the minimum number of affine hyperplanes slicing every edge of the $d$-cube in its interior; put $h(0)=0$. [KNOWN / VERIFIED] Sauermann–Xu, Theorem 1.1, gives
$$h(d)=\Omega(d^{13/19}/\log^{32/19}d).$$
Source: [Improved Lower bound for hypercube edge slicing](https://arxiv.org/html/2510.16592v1), 18 October 2025. This log exponent is **32/19**, not the 32/12 typo appearing in the 2026 slicing-upper paper.

### 3.1 Paturi–Saks differentiation, including shortcut wires

[KNOWN reduction; PROVED explicit support version] Suppose $F$ computes $d$-bit parity. For each variable $i$, set
$$D_iF(y)=F(x_i=1,y)-F(x_i=0,y).$$
The two target values are opposite, so $D_iF$ has strict alternating signs on the remaining $d-1$ variables, with one fixed global orientation. This holds even when positive-class top scores are zero: negative-class scores are strictly negative. The raw affine contribution is exactly the constant $u_i$. Every bottom independent of $i$ cancels. If $e_i$ bottoms essentially depend on $i$, then $D_iF$ is a constant plus a linear combination of at most $2e_i$ LTFs, using coefficients $v_j,-v_j$ inherited from the **same** original top.

Each edge of the $(d-1)$-cube must change at least one of those LTFs, since the score has opposite strict signs at its endpoints. Move each threshold slightly downward to preserve its finite truth table while removing all ties; every changed edge is then genuinely sliced. Therefore
$$2e_i\ge h(d-1),\qquad
\boxed{W_{\rm bot}\ge\sum_i e_i\ge\frac d2h(d-1).} \tag{P}
$$
Equivalently choose an input of small bottom outdegree $e_i\le W_{\rm bot}/d$ and differentiate there. This is the gate-wire reduction, not an assumption that all gates are dense. A raw edge $x_i\to\mathrm{top}$ cannot evade it, because differentiation turns it into a constant. Remaining raw edges cancel. The reduction also yields $S\ge h(d-1)/2$ with arbitrary raw top wires. Without shortcuts, the direct first-layer slicing argument gives $S\ge h(d)$; the asymptotic exponent is the same.

The original source is [Paturi–Saks, *On Threshold Circuits for Parity*, FOCS 1990](https://cseweb.ucsd.edu/~paturi/myPapers/pubs/PaturiSaks_1990_focs.pdf), Lemmas 1–2, pp. 399–400. Their model charges a constant-one source and states a gate/edge inequality with additive terms. Our derivative formulation avoids needing to translate those terms or silently omit raw top wires.

Thus the verified unrestricted exact bounds are
$$\boxed{\Omega\left(\frac{d^{32/19}}{\log^{32/19}d}\right)\le W_{\oplus_d}\le O(d^2),}
\qquad
\Omega\left(\frac{d^{13/19}}{\log^{32/19}d}\right)\le S_{\oplus_d}\le O(d).$$
The exact gate lower exponent is **13/19**, not merely $1/2$.

### 3.2 Explicit upper construction and average case

[PROVED elementary upper] For $s=\sum_i x_i$,
$$s-2\sum_{r=1}^{\lfloor d/2\rfloor}[s\ge2r]=s\bmod2.$$
Threshold this score at $1/2$. It has $\lfloor d/2\rfloor$ bottom gates and exactly $(d+1)\lfloor d/2\rfloor+d$ support edges before optional simplification, including the $d$ raw top edges. All weights and thresholds are polynomial integers (double the final score to avoid $1/2$). This supplies $O(d^2)$ even in the polynomial-weight class.

[KNOWN / VERIFIED] Kane–Williams Theorem 1.4 proves that uniform **99% agreement** with parity has gate complexity $\Theta(\sqrt d)$ and wire complexity $\Theta(d^{3/2})$, with lower bounds for arbitrary-real LTF-of-LTF and upper bounds already for majority-of-majority. Their circuit definition explicitly permits raw top inputs. Source: [Kane–Williams, author PDF](https://cseweb.ucsd.edu/~dakane/depth2LTF.pdf), Theorem 1.4 and Section 4. A central Hamming-layer window gives the upper bound. The restriction proof leaves two live variables; if every bottom reduces to a constant or literal, the remaining circuit is a single LTF, which cannot agree with two-bit parity above $3/4$. The expected number of nontrivial bottoms is $O(S/\sqrt d)$ or $O(W/d^{3/2})$. Thus near-perfect approximation and exact parity have different known exponents. No claim about all arbitrarily small positive advantages is inferred from the 99% statement.

For an explicit support audit of the average upper, take integers $L,U$ surrounding $d/2$ at distance $O(\sqrt d)$ so the binomial probability of $L\le s\le U$ is at least $0.99$. In the exact score above, replace all threshold cuts at $2r\le L$ by their constant value one, retain only $L<2r\le U$, and replace all cuts above $U$ by zero. The resulting score is identical on every retained layer and uses $O(\sqrt d)$ gates, each with $d$ input edges, plus $d$ raw top edges. Chernoff's inequality supplies the stated interval. This accounts for actual wires, with no multiplicity conversion.

### 3.3 Weight restrictions and literature cutoff

[KNOWN / VERIFIED] Paturi–Saks Theorem 3 gives $\Omega(d^2/\log^2d)$ wires when **all weights have polynomially bounded integer representations**, including the necessary bias/threshold convention. Merely allowing arbitrary real weights of small absolute size is not this restriction: positive rescaling can make any real gate's coefficients small. The 1994 rational-approximation paper is the fuller continuation; the 1990 primary PDF already verifies the stated depth-two theorem.

[KNOWN / PROVED consequence] Sauermann–Xu, [*Nondegenerate hyperplane covers of the hypercube*](https://arxiv.org/html/2507.00773v2), Corollary 1.2, gives $h_C(d)\ge d/(4C)$ for normals individually rescalable to integer entries in $[-C,C]$. Applying (P) gives $W_{\rm bot}\ge d(d-1)/(8C)$, with arbitrary real top weights and thresholds. Fixed $C$ therefore has exact quadratic wire complexity. For $C=d^{O(1)}$ this estimate need not beat Paturi–Saks; the hypotheses differ.

Primary-source browsing was conducted through the requested cutoff 2026-11-11. The 2026 [Soiffer–Itty–Rosin–Bruell–DiCicco–Sárközy–Offstein–Reichman paper](https://arxiv.org/html/2602.16807v1) explicitly still identifies the Sauermann–Xu exponent as the best slicing lower bound and improves the *slicing upper constant*. Slicing is only necessary for threshold-of-threshold parity, so that upper construction is not automatically a parity circuit. The October 2025 paper itself explicitly announces its wire consequence. Targeted searches for later unrestricted or polynomial-weight parity wire improvements, the 2026 source's references, and the recent sigmoid paper did not identify a stronger applicable parity theorem. **This verifies the quoted baseline, not an exhaustive proof that no stronger theorem exists.**

The [November 2026 Li–Reichman–Williams–Wu sigmoid report](https://eccc.weizmann.ac.il/report/2026/311/) concerns a different activation/weight/margin model. [Nag's September 2026 near-cubic wire preprint](https://eccc.weizmann.ac.il/report/2026/167/) concerns a language in $\mathsf E^{\mathsf{NP}}$, not ordinary Andreev or parity; its page also contains review concerns. Neither supplies the unrestricted bound sought here. No unreviewed claim is promoted to an Andreev theorem.

## 4. New wire incidence deductions from the character and table-pair arguments

These are new deductions *within this investigation*, with no literature-priority claim. Their ingredients are the classical Paturi–Saks differentiation, the cited slicing theorem, UP2 round-two character differences, LOW1's semantic refinement, and LOW2's owner extraction. Unlike multiplying a gate bound by $n$, the proofs charge individual essential incidences.

### 4.1 A support-weighted semantic character inequality

Define $\mathcal A_j$ to be the nonempty block sets $T$ for which
$$h_{j,T}(a)=g_j(x_T^+,a)-g_j(x_T^-,a),\qquad
x_{T,c}^{\pm}=(1\pm\chi_T(c))/2,$$
is nonconstant. Let $d_{j,T}$ count the selected raw coordinates in blocks $T$ on which this difference essentially depends, and put $d_T=m|T|$. Then
$$\boxed{\sum_j\sum_{T\in\mathcal A_j}d_{j,T}
\ \ge\ \frac14\sum_{T\ne\varnothing}d_T h(d_T-1).} \tag{CW}
$$

**Proof.** The actual score difference between $x_T^+$ and $x_T^-$ has strict sign $\chi_T(b(a))$. Raw address terms and all pure-address bottoms cancel; table-only terms are constant. Fix ignored blocks arbitrarily. Differentiate this difference in a selected coordinate $i$. Its score now has full parity signs on the other $d_T-1$ selected bits. A gate with $h_{j,T}$ independent of $i$ cancels; any remaining gate contributes at most four LTFs (two table settings times two values of $i$), with the original common coefficients and appropriate signs. Thus $4e_{T,i}\ge h(d_T-1)$, where $e_{T,i}$ counts gates whose difference globally essentially depends on $i$. Global essential dependence is a safe overcount of dependence after the fixing. Sum over $i$ and then $T$. Ties are handled exactly as in (P). This proves (CW).

If $|\mathcal A_j|\le Q$ for every mixed gate, then $d_{j,T}\le d_j$ gives
$$\boxed{W_{\rm address}\ge\frac1{4Q}\sum_{T\ne\varnothing}d_T h(d_T-1)
=\Omega\left(\frac{n^{51/19}}{Q\log^{32/19}n}\right).} \tag{CW1}
$$
Here $W_{\rm address}$ counts input-to-bottom address edges, and therefore is at most the full $W$. For $\Omega(N)$ middle characters, $d_T=\Theta(M)=\Theta(n)$, which proves the asymptotic estimate. This exponent $51/19\approx2.6842$ exceeds 2.5 for fixed $Q$, but the activity cap is substantive. In the bounded-integer-address-normal model,
$$\boxed{W_{\rm address}\ge\frac1{16CQ}\sum_T d_T(d_T-1)
=\frac{N\bigl(m^2k(k+1)-2mk\bigr)}{64CQ}.} \tag{CW2}
$$
Thus fixed $C,Q$ has an $\Omega(n^3)$ lower bound, matched by the ordinary Fourier ladders and the full-support two-scale variant. It permits arbitrary raw top terms and pure-address helpers. Written Walsh support at most $Q$ implies the semantic activity cap, but the semantic formulation also covers truth-table-preserving dense perturbations.

Without the activity cap, (CW) is still an unrestricted weighted tradeoff. It does **not** yield a better unrestricted exponent: a bottom can have $|\mathcal A_j|=N-1$, even with only one essential table bit. This capacity is realized by the examples in round-three UP2 §2.5 / LOW2 §2.3. A general upper bound on useful weighted activity would be new information, not a consequence of coefficient density.

### 4.2 A table-support/address-support product inequality

[PROVED] For completely unrestricted exact circuits, with semantic $t_j,d_j$ as in §1,
$$\boxed{\sum_j t_jd_j\ge\frac{Nkm}{8}h(m-1).} \tag{TD}
$$

**Proof.** Fix a block $i$, and pair labels $\{c,c\oplus e_i\}$. Compare the single-one tables $e_c,e_d$ and fix every other address block to their common label bits. The actual top-score difference sign-computes parity on the $m$ raw bits in block $i$, up to orientation. Differentiate in a live coordinate $l$. Each surviving gate supplies at most four LTFs on the remaining $m-1$ bits; raw top terms cancel or become constants. Therefore at least $h(m-1)/4$ gates must have a nonzero differentiated contribution. A gate can occur only if it depends on coordinate $(i,l)$ and on at least one of the table bits $c,d$. In the disjoint pairing for block $i$, at most $t_j$ pairs touch its essential table support. Sum over the $N/2$ pairs, all $m$ coordinates, and all $k$ blocks. A gate is charged at most $t_jd_j$, proving (TD).

If $t_j\le t$, then
$$W_{\rm address}\ge\frac{Nkm}{8t}h(m-1)
=\Omega\left(\frac{n^{51/19}}{t\log^{45/19}n}\right).$$
For individually rescalable integer address bound $C$, this becomes
$$W_{\rm address}\ge\frac{Nkm(m-1)}{32Ct}=\Omega(n^3/(Ct\log n)).$$
The one-table-bit subclass has $t=1$. This is a valid wire upgrade of the earlier subclass gate bound; unrestricted dense table dependence loses the factor $t$. There is no inference from (TD) to unrestricted exponent greater than 2.5: $t_jd_j\le\min\{N d_j,Mt_j\}$ can be large per edge.

### 4.3 Dense monotone owner slabs: the same bound without a table-fan-in cap

[PROVED consequence of LOW2's extraction] Orient each mixed bottom's output so its top coefficient $v_j>0$, and assume all its table weights $\alpha_{jc}\ge0$ and all raw top table coefficients $u_c\ge0$. Pure-address features can have arbitrary coefficients. This is a restriction on every table-to-output path, not WLOG for general Andreev circuits.

Let $A_j=\sum_c\alpha_{jc}$. If $\alpha_{jc}>A_j/2$, call $c$ the unique owner and put
$$h_j(a)=[A_j-\alpha_{jc}<\theta_j-\gamma_j\cdot a\le\alpha_{jc}],\quad
K_c(a)=u_c+\sum_{j:\,\operatorname{owner}(j)=c}v_jh_j(a).$$
LOW2's endpoint-safe inequalities give $K_c\ge0$ and
$$K_{b(a)}(a)>\sum_{c\ne b(a)}K_c(a).$$
For completeness, on complementary singleton tables a gate's own positive difference is $h_j$, every nonowner difference is at most $-h_j$, and an unowned gate has only nonpositive differences. Raw table terms obey the same dominating inequality because $u_c\ge0$. The actual positive selected-table difference forces the strict dominance above.

For each label pair $\{c,c\oplus e_i\}$, $K_c-K_d$ sign-computes block-$i$ parity after fixing other blocks. Differentiating in each live coordinate uses at most four halfspaces **per owner slab**, giving the same $h(m-1)/4$ incidence demand. Every owner belongs to exactly one pair for each block. Summing yields
$$\boxed{W_{\rm address}\ge\frac{Nkm}{8}h(m-1)
=\Omega(n^{51/19}/\log^{45/19}n).} \tag{OW}
$$
It suffices to count semantic dependence of $h_j$, which is at most the original gate's address dependence. An irrelevant coordinate cannot reappear in its two-table difference. Hence this is not a syntactic-density argument. Bounded integer address normals give $W_{\rm address}\ge Nkm(m-1)/(32C)$, exponent three for fixed $C$. These bounds count only owner-gate address edges, so adding unowned or pure-address helpers cannot evade them.

The sign condition is essential. A signed dense table row may have many positive complementary-singleton responses. Even one tiny negative coefficient can invalidate the owner-slab containment (round-two LOW2 §4.1). The exact and approximate ordinary Fourier circuits need not satisfy the path signs. No unrestricted exponent follows from (OW).

## 5. Strongest profile result: a semantic cubic wire lower bound

[PROVED, conditional only on the fully stated profile lemma proved below and its cited skew-cover ingredient] For fixed bounded integer address magnitudes constant within each block, exact ordinary Andreev has wire exponent **three**, even with arbitrary signed dense table normals, arbitrary within-block sign masks, raw top wires, arbitrary real top coefficients, and arbitrary pure-address/pure-table helpers. This is a restricted-class result. Its gate exponent was already two in LOW1 round three. The extra power here has a proved **semantic density** justification, including zero-support blocks and alternative threshold representations.

### 5.1 Semantic pruning lemma

Suppose a Boolean bottom admits a representation
$$\gamma_{j,i,l}=\sigma_{j,i,l}a_{j,i},\qquad
\sigma_{j,i,l}\in\{-1,1\},\quad a_{j,i}\in\{0,\ldots,C\},$$
after a positive gate-specific rescaling. Its table coefficients and threshold are arbitrary real. Let $q_j$ count distinct block magnitudes, including zero if present.

[PROVED] There is such a representation in which **every nonzero address coefficient is essential**, without increasing $C$ or $q_j$.

**Proof.** Complement each negative-sign address coordinate. In the new variables, all coordinates of one nonzero magnitude enter the threshold symmetrically, across all blocks and for every fixed table. Swapping two of them preserves the Boolean gate. Essential dependence is therefore identical for every coordinate in that magnitude class: if one has a witness, swap it to obtain a witness for any other. Delete a wholly irrelevant class by fixing all its original raw bits to zero; the function on the full domain is unchanged because each deleted coordinate is irrelevant. All blocks of that class now have magnitude zero. The blockwise property and the integer bound remain. If zero was absent, deleting at least one positive class adds at most the one zero class, so the total number of distinct magnitudes does not increase. Repeat. The surviving support equals semantic address dependence, hence is a lower bound on the support of **any** numerical realization of this Boolean gate. This proves the claim.

This is why simply adding tiny coefficients to a sparse function does not create a spurious wire lower bound here. We apply the profile argument to the pruned allowed representations, not to an artificially dense original one.

### 5.2 Finite cubic transfer

Let $S$ be the number of useful structured mixed bottoms after pruning, and suppose $q_j\le q$, $q\ge2$. Put
$$r=\max\{2,\lceil\log_2(S+1)\rceil\},\quad
D=m-(k-1)r>0,\quad L_*=r\lfloor k^2/4\rfloor,$$
$$B_k=\frac12\sum_{s=\lceil k/3\rceil}^{\lfloor2k/3\rfloor}\binom ks=\Theta(N).$$
All cuts in this sum are nontrivial for $k\ge2$. Then
$$\boxed{W_{\rm address}\ge
\frac{M B_k D}{12(2^{q-1}-1)(2CL_*+1)}.} \tag{PW}
$$
For at most two block magnitudes, the sharper tree form is
$$\boxed{W_{\rm address}\ge
\frac{M B_k D}{12(2C(k-1)r+1)}.} \tag{PW2}
$$
Consequently, in the balanced growing-$k$ family,
$$W=\Omega\left(\frac{n^3}{C(2^{q-1}-1)\log^4n}\right),$$
and for two magnitudes
$$W=\Omega(n^3/(C\log^3n)).$$
Fixed $C$ gives $q\le C+1$, so both have exponent three. No hypothesis on top coefficient size is needed.

**Profile incidence lemma (LOW1 round three §3, using LOW2 graph isolation).** For a cut $\{T,T^c\}$, say a gate is separated if its sets of block magnitudes on the two sides are disjoint. Count only separated gates whose actual complementary-$T$ table difference is nonconstant. Their number $E_T$ satisfies
$$E_T\ge\frac{D}{4(2Cr|T|(k-|T|)+1)}. \tag{PI}
$$
With two magnitude classes one can replace $|T|(k-|T|)$ by $k-1$.

**Proof of the lemma, included to expose all hypotheses.** Use the complete bipartite block graph of the cut. Reserve $r$ disjoint selected/ignored raw-bit pairs per graph edge; this leaves at least $D$ unused coordinates in every block. There are $L=r|T|(k-|T|)$ selected and $L$ ignored live bits, initially independent. Take one block on each side and identify $D$ unused paired baseline coordinates as bits $z_1,\ldots,z_D$ to be fixed later. For a separated gate, each baseline coefficient is a nonzero integer $\pm a\pm b$, since the magnitudes differ across the cut. Its range on the $2L$ live bits has width at most $2CL$. At either character table, the baseline assignments leaving it nonconstant lie in at most $2CL+1$ integer level hyperplanes. Every such hyperplane has all $D$ coefficients nonzero.

If $2E_T(2CL+1)<D/2$, those level hyperplanes cannot cover the $D$-cube, by the known skew-cover bound $D/2$ (Sauermann–Xu Theorem 1.1; see also its attribution of the earlier skew-cover consequence to Linial–Radhakrishnan). Pick an uncovered baseline, making every active separated gate constant at both tables. Now identify each ignored live bit with a random literal of its selected partner. Every nonseparated gate has an equal-magnitude edge, with $r$ independent pairs there; it retains all $L$ coordinates with probability at most $2^{-r}$. A zero-zero pair only helps. Since $S2^{-r}<1$, there is one choice making every remaining gate omit a live variable. Inactive table differences are already constants. Pure-address terms cancel between the two tables; pure-table terms are constants; affine-after-table helpers have degree at most one. Their actual common score thus has zero full-live-parity correlation, contradicting its strict required parity signs for $L\ge2$. This proves (PI). For two classes, a connected bipartite spanning tree suffices: a different two-color profile has a monochromatic edge. This gives $L=(k-1)r$.

**Proof of (PW).** Use the pruned representations of §5.1 and sum (PI) only over middle unordered cuts. A separated gate cannot have zero blocks on both sides: otherwise zero belongs to both magnitude sets. Thus at least one entire side consists of nonzero blocks. Both sides have at least $k/3$ blocks, so this gate has at least $M/3$ **essential** address inputs. A row with $q_j$ magnitude classes is separated by at most $2^{q_j-1}-1$ unordered cuts, since each class must lie wholly on one side. Therefore, if $H$ is the number of semantically dense gates charged,
$$(2^{q-1}-1)H\ge\sum_{T\text{ middle}}E_T
\ge\frac{B_kD}{4(2CL_*+1)},\qquad W_{\rm address}\ge(M/3)H.$$
Combine these inequalities. The tree replacement proves (PW2).

For the asymptotic simplification, first dispose of $W\ge n^3$, where the claimed lower conclusion is automatic. Otherwise $S\le W<n^3$, since each useful bottom has a top edge, so $r=O(\log n)$ and $D=\Theta(m)$. This avoids erroneously assuming a small gate count in a wire-minimization problem.

The exact $O(n^3)$ wire upper is already in this class: the basic Fourier ladders have block magnitudes $0,1$, and UP2's full-support variant has $1,2$. Hence the restricted exact wire exponent is matched. The average-case masked construction also lies in the class and costs $O(n^{5/2})$ wires for fixed error; there is no contradiction because (PI) uses exact rare character tables.

### 5.3 Helpers with no cancellation do not automatically erase the cubic bound

[PROVED consequence with explicit prior ingredient] LOW1 round-three §4.6 allows $F$ additional mixed gates whose address normals are superincreasing in a gate-specific order. Replace $r$ above by
$$r=\left\lceil\log_{4/3}\bigl(16(S+6F+1)\bigr)\right\rceil.$$
Its proof first makes separated structured gates constant as above, then charges the expected complemented-monomial support of every remaining feature. Nonseparated structured differences have normalized budget at most $(3/4)^r$; a difference of two superincreasing restricted thresholds has budget at most $6(3/4)^L$. Raw-address/pure-address terms cancel. A strict parity score needs every monomial position in every complemented basis, whereas the available expected budget is below $1/16$ outside affine positions. This is a genuine helper charge, not their removal for free. Literal identification preserves superincrease because the earliest coefficient in a merged group dominates all later original coefficients.

Consequently (PI), and hence the **same semantic cubic wire transfer**, hold with this $r$. For polynomially many such helpers the exponent remains three. If there are already more than $n^3$ useful helpers, their top wires alone give the desired lower bound. UP2 round-three §1.6 extends the argument to separated subset-sum groups of width polylogarithmic in $n$, with its explicitly enlarged $r$; this retains exponent three up to the corresponding polylogarithms. This last extension is a consequence of that stated group-closure theorem, not an independently formalized result here.

### 5.4 Arbitrary-real two-scale profiles with a mask resource

[PROVED transfer from LOW2 round-three §3.5] Suppose mixed bottoms have at most two magnitudes constant by original block, arbitrary real ratios (one may be zero), and at most $R$ masks per unordered two-class profile. Uniform one-magnitude rows and arbitrary pure-address/pure-table helpers are allowed as in LOW2's model. Put $r=\max\{2,\lceil\log_2(S+1)\rceil\}$, $h=m-(k-1)r$, and $B=2(k-1)r+1$. That theorem gives, for each profile,
$$2E_T B\ge h/R-R+1,$$
when $h>0$ and $h/R-R\ge0$. It uses two independent random-prefix baselines and the exact shuffled-walk occupation bound; no integer or ratio premise is imported.

The pruning lemma still holds for arbitrary real magnitude classes. Deleting one of two positive classes leaves the same unordered profile, with zero on that side; mask completions on zero coordinates may reuse the original masks. Thus pruning does not increase the per-profile mask cap. A useful separated middle-profile row again has at least $M/3$ essential address inputs. Summing only middle profiles gives
$$\boxed{W_{\rm address}\ge\frac{M B_k}{6B}(h/R-R+1).} \tag{RW}
$$
If $R^2\le h/2$, this implies $W=\Omega(n^3/(R\log^3n))$. In particular $R=n^\eta$ for fixed $\eta<1/2$ forces wire exponent $3-\eta>2.5$ in this class. The ratio of magnitudes is unrestricted, but the mask budget and blockwise constancy are substantive.

If instead one substitutes the unrestricted number $E_T$ of profile gates for $R$, the theorem gives only $E_T\gtrsim\sqrt{m/(k\log S)}$ per profile (unless it is already larger). Multiplying by the now **proved** middle-profile semantic density and summing restores only exponent 2.5. This is a rigorous explanation of why that self-substitution does not solve the unrestricted wire problem.

## 6. Costed parity helpers and arithmetic wire consequences

### 6.1 One full point gate forces quadratic support wires

[PROVED new support consequence; face/omission observation attributed to UP2 round three] Let $d\ge3$. Suppose a strict parity score has exactly one fully dependent bottom, and it is a conjunction of one literal per input (a point indicator). Every other bottom misses at least one input. Then
$$W_{\rm bot}\ge d^2,\qquad W\ge d^2+d+1.$$

**Proof.** Complement variables so the unique full gate is $z_1\cdots z_d$. In this basis every coefficient of the multilinear polynomial of a strict parity score is nonzero. Indeed the coefficient on $U$ is
$$\sum_{V\subseteq U}(-1)^{|U|-|V|}F(1_V),$$
and all summands have the same strict sign. In particular every degree-$(d-1)$ coefficient is nonzero. The full point gate has no such coefficient. Raw affine top terms have degree at most one, which is smaller than $d-1$. A helper can contribute to the coefficient on $[d]\setminus\{i\}$ only if it essentially depends on every variable in that set. Since it is not full-dependent, its essential support must be **exactly** that set. Distinct omissions require distinct helpers. Therefore at least $d$ helpers each need $d-1$ actual input edges, and the full gate needs $d$: total at least $d^2$. Their $d+1$ nonzero top edges are additional. This proof uses semantic essential dependence and remains true under arbitrary redundant coefficient padding.

It does **not** prove $d^2$ helper gates, nor apply to an arbitrary full-dependent survivor. A central majority can already supply lower-degree coefficients. LOW1's exact one-point-plus-$d(d-1)$-helper construction has $d+d(d-1)^2$ input-to-bottom wires, hence cubic rather than quadratic wires. This gives a real quadratic-to-cubic gap for that restricted parity architecture; its claimed polynomial helper construction is compatible with our necessity.

The inherited helper construction can be checked without an oracle. Set $s=\sum_i z_i$ and, for $0\le r\le d-1$,
$$f(r)=\frac{(-1)^r}{d\binom{d-1}{r}}\sum_{u=0}^r\binom du.$$
Then
$$(-1)^s=\sum_{i=1}^d f(s-z_i)+(-1)^d2^d[s=d].$$
For $s<d$ the sum is $(d-s)f(s)+sf(s-1)=(-1)^s$, by the binomial identities $(d-s)\binom ds=d\binom{d-1}s$ and $s\binom ds=d\binom{d-1}{s-1}$; the endpoint $s=d$ gives the displayed correction. Each $f(s-z_i)$ is a constant plus $d-1$ nonzero threshold jumps on the other $d-1$ variables. Each such threshold depends on every one of those variables. This proves the stated cubic input-edge count of that particular construction, not an optimality claim.

### 6.2 Lexicographic arithmetic: charge support directly

[KNOWN ingredient / PROVED transfer] Basu–Bhatnagar–Gopalan–Lipton, [*Polynomials that Sign Represent Parity and Descartes' Rule of Signs*](https://arxiv.org/html/math/0702773), Theorem 6.5, gives at least $(3/2)^M$ literal-conjunction terms for a strict parity sign representation (constant included). UP2 round-three §1 supplies an exact compiler: a superincreasing threshold with address support $p_j$ is a disjoint sum of at most $p_j$ prefix conjunctions, for every table fixing.

Take the full-character complementary-table difference. Raw and arbitrary pure-address terms cancel, table-only features give a constant, and each mixed gate gives two such expansions. Thus
$$1+2\sum_{j\text{ mixed}}p_j\ge(3/2)^M,$$
and
$$\boxed{W_{\rm address}\ge\bigl((3/2)^M-1\bigr)/2.}$$
This charges a compiler's actual support budget, rather than multiplying its gate bound by $M$. For ordered subset-sum-gap groups of maximum width $q$, the group cost $D_j=\sum_B2^{|B|}$ is at most $(2^q/q)p_j$, since $2^s/s\le2^q/q$ for $1\le s\le q$. Therefore
$$W_{\rm address}\ge\frac{q}{2^{q+1}}\bigl((3/2)^M-1\bigr).$$
As always the small separated-group hypothesis is substantial: putting an arbitrary normal into one width-$M$ group makes the estimate vacuous. If a gate has only a semantic short-conjunction expansion, charge that expansion directly; one cannot infer a wire lower bound from an artificially long numerical representation. For superincreasing representations, fixing irrelevant coordinates preserves superincrease, so the argument can use essential support.

### 6.3 Spectrum/permanent and paired-cancellation limits

[VERIFIED inherited inequalities; PROVED accounting observations] Paired cancellation on a selected/ignored half cube requires at least one fully dependent survivor on each literal restriction. The averaged permanent inequality and its soft helper variant in LOW1 rounds two/three are valid necessary constraints. A gate capable of depending on all $d$ merged variables must touch at least one original coordinate in each pair, hence at least $d$ original address variables. This does give a legitimate density charge for gates actually used in that covering argument. In the full-equal-magnitude class a nonconstant Boolean gate has all $M$ address variables essential by signed symmetry, so its exponential gate theorem also implies exponential support wires with a factor $M$.

For unrestricted directions, however, one support-aligned row or a generic all-distinct row can have survival probability one. The scalar covering demand then charges only $\Omega(d)$ support, regardless of the number of pairings. Discarding missing-variable helpers and demanding a slicing-sized survivor bank is false: the exact one-full-gate helper identity disproves it. The soft monomial budget correctly charges a helper with $s$ live essential variables by $2^{s-d}$; it can yield an exponential **heterogeneous restricted-class** theorem with superincreasing and histogram helpers, but no general polynomial wire improvement follows from that budget alone.

Dense full-sign pools passing all prior ordinary-edge/transcript tests use $\widetilde O(n^{3/2})$ gates and at most $\widetilde O(n^{5/2})$ support edges. Hence those specific relaxations have an explicit exponent-2.5 wire barrier, just as their gate barrier is exponent 1.5. They are not valid Andreev circuits: the paired/common-score dual rejects them. This is a barrier to the stated relaxation, not a proof that stronger exact wire lower bounds are impossible.

## 7. What the results do and do not settle

[PROVED / VERIFIED] With the support-wire convention of §1, the verified unrestricted exact ordinary-Andreev interval remains
$$\Omega(n^{5/2}/\log^{5/2}n)\ \le\ W_A(n)\ \le\ O(n^3).$$
For uniform fixed positive error, the exponent is already 2.5; the current mean-square upper removes the previous extra square-root logarithm, but is not yet formalized. The lower $\varepsilon^2$ tradeoff is used only for $\varepsilon\ge3(k+2)/\sqrt N$. Exact parity has the verified interval $\Omega(n^{32/19}/\log^{32/19}n)$ to $O(n^2)$, whereas 99% average agreement has wire complexity $\Theta(n^{3/2})$ and gate complexity $\Theta(\sqrt n)$.

[PROVED, strongest new transfer] The bounded-integer blockwise class has a matched exact wire exponent three by §5. This conclusion permits semantically dense signed table dependence and unlimited within-block masks. The original gate result belongs to LOW1/LOW2; the additional wire theorem comes from pruning irrelevant magnitude classes and proving density on the middle cuts. Its arbitrary-real two-level counterpart retains a per-profile mask resource: $\Omega(n^3/(R\log^3n))$ for $R^2\le(m-O(\log^2n))/2$. The semantic character and table/address product inequalities in §4 provide independent, explicitly support-weighted tradeoffs. None removes all structural restrictions.

[REFUTED extension; credited to LOW2 round three] One cannot drop the bounded-integer premise in the skew-cover proof by calling each bad region a real band. Take $D$ baseline pairs, with selected/ignored weights $1,-(1+\eta)$, and identify each pair to a baseline bit $z_i$. Reserve $L$ selected and $L$ ignored independent live bits with the same weights. The threshold's linear form is
$$\sum_{j=1}^L u_j-(1+\eta)\sum_{j=1}^L v_j-\eta\sum_{i=1}^D z_i.$$
If $0<\eta D<L$, its live minimum is negative and its live maximum is positive at **every** baseline assignment. Thus this single gate remains nonconstant on every live cube, although all $D$ baseline coefficients are nonzero. A single real band covers the entire baseline cube. This refutes that proposed argument, not a circuit lower bound or the integer theorem. The two-baseline mask argument avoids precisely this small-difference problem; its unrestricted-mask self-substitution nevertheless yields only exponent 2.5 (§5.4).

[CONJECTURE / best next research target] Seek a wire-weighted common-score obstruction for arbitrary-real two-level blockwise profiles with unrestricted masks. Preserve both table versions and charge the actual dense address supports after semantic pruning. A useful new result must beat the square-root exceptional-profile requirement obtained by replacing $R$ with the number of profile gates, or combine distinct character profiles through their **common** output coefficients. Ordinary slicing, survivor-only permanent cover, tiny negative-path perturbation arguments, and magnitude-free real-band covers do not establish that step. A successful two-level theorem would still leave heterogeneous magnitudes within a block as a separate obstacle to an unrestricted result.

## 8. Reproducibility, evidence, and attribution

[VERIFIED] Run the owned standard-library check suite with

```bash
python3 -I /tmp/andreev_gap/wires_astra/checks.py
```

It checks 1,020 parity inputs, 4,096 raw-top-safe differentiated scores, and 14,846 derivative edges; eight compiled Fourier circuits on all 3,512 inputs; 338 character differences, 338 four-restriction derivatives, and 638 associated edges; 1,600 blockwise gates including 907 semantically pruned cases and 1,776 density checks; 3,276 magnitude profiles and 800 table-pair support charges; 4,352 monotone singleton/slab cases; 624 exact rational helper identities and all omission supports through dimension eight; and 131,580 raw inputs for 773 lexicographic cuts. These are exact finite checks of the indicated algebra and support claims, not computational proofs of the asymptotic theorems. No solver or dependency installation was used.

Artifacts: [full report](/tmp/andreev_gap/wires_astra/report.md), [check program](/tmp/andreev_gap/wires_astra/checks.py), [check results](/tmp/andreev_gap/wires_astra/checks.json), and [source/reading manifest](/tmp/andreev_gap/wires_astra/evidence.json). The manifest pins the local files by SHA-256 at handoff and records primary-source URLs, theorem locations, and search scope. It is not a claim of exhaustive literature coverage.

Local baseline sources inspected: [current paper](/home/user/.t3/scratch/2026-11-02-improve-upper-bound-of-andreevs-93c6aee6/threshold_paper/paper.tex), [research state](/home/user/.t3/scratch/2026-11-02-improve-upper-bound-of-andreevs-93c6aee6/research_backup/docs/RESEARCH_STATE.md), [KW applications](/home/user/.t3/scratch/2026-11-02-improve-upper-bound-of-andreevs-93c6aee6/kw_applications.md), and [KW erratum](/home/user/.t3/scratch/2026-11-02-improve-upper-bound-of-andreevs-93c6aee6/kane_williams_erratum.md).

All completed preceding reports were inspected: round one [UP1](/tmp/andreev_gap/swarm/up1/report.md), [UP2](/tmp/andreev_gap/swarm/up2/report.md), [LOW1](/tmp/andreev_gap/swarm/low1/report.md), [LOW2](/tmp/andreev_gap/swarm/low2/report.md); round two [UP1](/tmp/andreev_gap/swarm_round2/up1/report.md), [UP2](/tmp/andreev_gap/swarm_round2/up2/report.md), [LOW1](/tmp/andreev_gap/swarm_round2/low1/report.md), [LOW2](/tmp/andreev_gap/swarm_round2/low2/report.md); round three [UP1](/tmp/andreev_gap/swarm_round3/up1/report.md), [UP2](/tmp/andreev_gap/swarm_round3/up2/report.md), [LOW1](/tmp/andreev_gap/swarm_round3/low1/report.md), [LOW2](/tmp/andreev_gap/swarm_round3/low2/report.md), and the [append-only board](/tmp/andreev_gap/swarm_round3/board.md). In particular, §5 reproduces the full bounded-palette/profile proof before adding the semantic wire charge, and §5.4 identifies the exact inherited finite mask inequality being transferred. Peer ingredient attribution and classical literature attribution are retained throughout. The WIRES additions have not received a new independent referee or Lean audit.

All work is saved in the requested directory except the authorized append-only WIRES board posts. No subagents, dependency installation, shared-paper edits, or online posts were made.
