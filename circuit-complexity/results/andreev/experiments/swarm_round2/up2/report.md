# UP2 round two: unequal scales, sparse supports, and one common top

Authors: Christian Reitwiessner

Date: 2026-11-11. Role: UP2, OpenAI Astra. This report was created immediately and updated after major ideas. No subagents, shared-paper edits, package installations, or online posts.

## Outcome

**No unrestricted exponent improvement was obtained.** The exact ordinary-Andreev gap remains the supplied $\widetilde\Omega(n^{3/2})$ to $(5/16+o(1))n^2$.

**[PROVED, strongest new architecture result]** Polynomially many dense-table, full-support equal-magnitude helper gates cannot lower the quadratic exponent of character-specific sparse/two-scale channels drawn from a fixed number of sign masks. The channel scales may be arbitrary real numbers, including irrational ratios; only their ignored-to-selected magnitude ratio is bounded. The precise hybrid theorem and complete proof are in §3. For fixed mask count and scale ratio it gives $\Omega(n^2/\log n)$ channel gates at balance. It permits helpers with dense Walsh table support, so it is not a consequence of the sparse-table-transform theorem below. LOW2 and LOW1 independently checked the one-direction version; the stronger few-mask proof and exact checks are included.

**[PROVED, complementary resource theorem]** If each table normal couples at most $q$ nonconstant Walsh statistics, exact computation requires $\widetilde\Omega(n^{32/19}/q)$ gates for arbitrary real address weights. With individually rescalable integer address coefficients bounded by $C$, it requires $S\ge kmN/(16Cq)$. The geometric bounds are inherited from Sauermann–Xu; the new part of this investigation is the complementary-character charging reduction. A truth-table-invariant semantic refinement, suggested independently on the board by LOW1, is proved in §1. All three peers checked the basic reduction.

**[PROVED construction and matching restricted exponent]** Full-support address rows with magnitudes in $\{1,2\}$ and arbitrarily mixed signs admit an explicit $O(n^2)$ common-top Fourier construction (§2). With one Walsh table statistic per gate this class has balanced complexity $\Theta(n^2)$ by §1. Thus it genuinely escapes round one's exponential equal-magnitude class, but not the requested quadratic exponent. This is a stress construction, not an improvement of the known upper bound or a claim of literature priority.

## Conventions and inherited ingredients

[KNOWN, supplied COMMON.md, all four round-one reports and board, curated RESEARCH_STATE.md, paper.tex] Let $N=2^k$, $M=km$, $n=N+M$, and $A(x,a)=x_{b(a)}$, with $b_i=\sum_l a_{il}\pmod2$. The top reads every raw input and arbitrary real linear combinations of bottoms. Balanced asymptotics mean $M=\Theta(N)$, including $m=\lfloor N/k\rfloor$; exact balance is not needed.

Write $\chi_T(c)=(-1)^{\sum_{i\in T}c_i}$. An exact top score $F$ can be oriented with output one iff $F\ge0$. Comparing a positive and a negative input then gives a strictly positive difference even if the positive score is zero. Every raw-address affine term cancels in a same-address table comparison.

[KNOWN, round-one UP2 §6; checked there by LOW2] On $2r$ raw sign variables $(z,w)$, a score composed of $J$ full-support equal-magnitude address gates and affine raw terms cannot sign-compute $\prod_{i=1}^r z_i$, $r\ge2$, unless $J\ge2^r$. For completeness: restrict $w_i=t_i z_i$ for each of the $2^r$ sign vectors $t$. Each gate keeps all $r$ live coefficients for exactly one $t$; otherwise it omits a variable and has zero correlation with full parity. A strictly correct score needs nonzero parity correlation on every restriction. This is the inherited exact ingredient in §3, not a claim that generic unequal weights obey the same bound.

[KNOWN, primary sources checked during this run] Let $\operatorname{slice}(d)$ denote the minimum number of hyperplanes slicing all edges of the $d$-cube in their interiors. [Sauermann–Xu, Improved lower bound for hypercube edge slicing, Theorem 1.1](https://arxiv.org/html/2510.16592v1) gives $\operatorname{slice}(d)=\Omega(d^{13/19}/\log^{32/19}d)$. Their [Nondegenerate hyperplane covers of the hypercube, Corollary 1.2](https://arxiv.org/html/2507.00773v2) gives at least $d/(4C)$ slicers if each normal is in $\{-C,\ldots,C\}^d$. These are imported geometric theorems, not new exponents proved here.

The corrected drift conclusion remains conditional on globally comparable eligible blocks, which may be absent. No argument below assumes a zero-sum normal form, bounded top weights, polynomial normalized margin, or that edge coverage suffices for a common top.

## 1. Sparse coupling of Walsh table statistics has a direct-sum cost

### 1.1 Exact resource inequality [PROVED]

Write

$$F(x,a)=\beta_0+\beta\cdot x+\delta\cdot a+\sum_{j=1}^S v_jg_j(x,a),\qquad
 g_j=[\alpha_j\cdot x+\gamma_j\cdot a\ge\theta_j].$$

Let

$$q_j=|\{T\ne\varnothing:\widehat\alpha_j(T)\ne0\}|,\qquad
\widehat\alpha_j(T)=N^{-1}\sum_c\alpha_{jc}\chi_T(c).$$

Then every exact circuit satisfies

$$\boxed{\sum_{j=1}^S q_j\ge\frac12\sum_{T\ne\varnothing}\operatorname{slice}(m|T|).}$$

**Proof.** Fix nonempty $T$ and compare the actual two Boolean tables

$$x_c^+=(1+\chi_T(c))/2,\qquad x_c^-=(1-\chi_T(c))/2.$$

Their bottom table offsets differ by $N\widehat\alpha_j(T)$. Hence if this coefficient is zero, $g_j(x^+,a)-g_j(x^-,a)=0$ for every raw address. For a nonzero coefficient the difference is a signed slab in the same address normal $\gamma_j$, namely a difference of two threshold functions. All pure-address gates cancel too. The top difference is therefore

$$D_T(a)=F(x^+,a)-F(x^-,a)
       =c_T+\sum_{j:\widehat\alpha_j(T)\ne0}v_j
               (g_j(x^+,a)-g_j(x^-,a)).$$

Correctness forces $\chi_T(b(a))D_T(a)>0$ at every raw address. Fix all blocks outside $T$. On the $d=m|T|$ selected raw bits, this is full parity, so every cube edge has opposite strict signs at its endpoints. If neither of the two halfspace features of any surviving bottom changed on an edge, $D_T$ would be equal at both endpoints. Thus their at most $2s_T$ halfspaces slice all edges, where $s_T$ is the number of indices with $\widehat\alpha_j(T)\ne0$.

To handle ties, each of these finitely many restricted threshold functions can have its threshold decreased slightly, preserving every Boolean output and putting no cube vertex on its boundary. No normal changes. Every changed edge is then sliced in its interior. Consequently $2s_T\ge\operatorname{slice}(d)$. Summing over $T$ gives the displayed inequality. The same top coefficients were used throughout; no replacement decoder per pair was asserted. $\square$

For $\Omega(N)$ characters with $|T|\ge k/3$, $d=\Theta(M)$. Thus

$$\sum_jq_j=\Omega\!\left(\frac{NM^{13/19}}{\log^{32/19}M}\right).$$

If $q_j\le q$, this is $S=\widetilde\Omega(n^{32/19}/q)$ at balance. This is a dense signed-table class, distinct from the one-table-bit and nonnegative table-path classes. The direct-sum mechanism and slicing exponent have clear inherited ancestry; no exhaustive novelty determination was performed.

### 1.2 Bounded integer address ratios [PROVED consequence]

Suppose each nonzero $\gamma_j$ can be individually rescaled to an integer vector with absolute entries at most $C$. The two threshold shifts after fixing a table retain this same normal. The bounded-normal slicing theorem gives $2s_T\ge m|T|/(4C)$. Since $\sum_T|T|=kN/2$,

$$\boxed{\sum_jq_j\ge\frac{kmN}{16C},\qquad
S\ge\frac{kmN}{16Cq}\quad(q_j\le q).}$$

No bounds are imposed on table coefficients, thresholds, or top coefficients. Zero address coordinates and all mixed signs are allowed. Fixed $C,q$ force $\Omega(n^2)$; polylogarithmic values preserve exponent two. Merely coupling a few Walsh table statistics, adding small unequal integer scales, or changing character supports cannot yield an exact subquadratic family in this model.

A real common rescaling of a whole address normal does not evade the hypothesis. In particular a table-only guard combined with one original bottom as $[U(x)+\lambda L(x,a)\ge t]$ has address normal proportional to the original. UP1 explicitly checked this compiler implication on the board: real $\lambda$ does not automatically create incommensurate address coefficients.

### 1.3 A semantic, perturbation-stable version [PROVED; board suggestion credited to LOW1]

For a Boolean bottom function define

$$\mathcal A_j=\{T\ne\varnothing:
a\mapsto g_j(x_T^+,a)-g_j(x_T^-,a)\text{ is nonconstant}\},\qquad a_j=|\mathcal A_j|.$$

These sets depend only on the gate's truth table. Constant differences can be absorbed into $c_T$, so the proof gives the same inequalities with $a_j$ in place of $q_j$. Also $a_j\le q_j$ for every written threshold representation. This formulation blocks a spurious escape through tiny dense coefficient perturbations that preserve the original gate truth tables. For the bounded-normal version it suffices that each Boolean bottom has some equivalent representation with the stated address-normal bound.

In particular, a putative $S=n^{2-\epsilon}$ circuit with fixed $C$ needs average semantic character-pair activity $\Omega(n^\epsilon)$. Generic syntactic Fourier support alone does not establish that activity, and activity alone still does not prove one feasible top gate. Arbitrary dense rows can have $a_j=\Theta(N)$, so this is not an unrestricted gate bound.

## 2. A full-support two-scale exact family, and its matching exponent

### 2.1 Explicit common top [PROVED construction]

Let $\xi_c=1-2x_c$ and $X_T=\sum_c\chi_T(c)\xi_c$. For each $T\ne\varnothing$ independently choose any sign mask $\sigma_{T,l}\in\{\pm1\}$ on all $M$ raw coordinates, and put

$$w_{T,l}=\begin{cases}\sigma_{T,l},&l\text{ belongs to a block in }T,\\
2\sigma_{T,l},&\text{otherwise},\end{cases}
\qquad L_T(a)=\sum_lw_{T,l}a_l.$$

Every row has full support. Signs may vary arbitrarily inside every block. Odd coefficients occur exactly on the selected character's raw coordinates, so

$$(-1)^{L_T(a)}=\chi_T(b(a)).$$

Since $X_T$ is even, the standard staircase identity for $\varphi(u)=(-1)^uu$ gives

$$\varphi(X_T+L_T)-\varphi(L_T)=X_T\chi_T(b).$$

Therefore one fixed common score, for every independent table and raw address, is

$$P=X_\varnothing+\sum_{T\ne\varnothing}
  \bigl(\varphi(X_T+L_T)-\varphi(L_T)\bigr)=N(1-2x_b).$$

The top computes $[-P\ge0]$ with signed margin $N$. Every function is expanded directly into thresholds of its raw affine form; there is no hidden extra layer or input-dependent choice of weights.

Let $W_T=\sum_l|w_{T,l}|=2M-m|T|$. The two complete ladders cost at most $2N+2W_T$ gates. The empty character is a free affine table term. Thus

$$S\le2N(N-1)+3MN-4M=O(N^2+NM).$$

This deliberately noncompetitive constant is irrelevant to the exponent goal. All table-reading rows use one nonconstant Walsh statistic, and all address rows rescale to entries in $\{-2,-1,1,2\}$. Section 1 therefore gives $S\ge MN/32$ at balance for this entire model, including arbitrary top refits, masks, and thresholds. Hence its balanced exponent is exactly two: $\Theta(n^2)$ for $q=1,C=2$.

This is an elementary adaptation of the inherited Fourier/staircase identity, not a new best upper bound. Its purpose is to exhibit a genuine all-size escape from full-support equal magnitude with an actual common top, then close the subquadratic hope for this sparse-table-coupling architecture.

### 2.2 Why a finite palette or near equality is insufficient [PROVED scope checks]

Pairing a selected coefficient of magnitude one with an ignored coefficient of magnitude two never cancels. Thus the round-one paired-cover inequality is vacuous for this channel, exactly as it should be. No huge magnitude ratio is needed to escape that theorem.

[PROVED consequence supplied by LOW2, credited] Replace the magnitudes by $B-1$ and $B$ for any even integer $B\ge2$. The same parity identity holds and gives

$$S\le2N(N-1)+(2B-1)MN-2BM.$$

Their ratio is $B/(B-1)$, arbitrarily near one for fixed large $B$, while the size remains $O_B(n^2)$. LOW2's separate count-layer compiler gives polynomial circuits even for a ratio tending to one extremely quickly, at an extra factor $M$. I checked that compiler's identity and the need to choose its dominant coefficient also larger than all original address coefficients. Numerical closeness alone cannot extend the round-one exponential theorem.

## 3. Dense full-sign helpers cannot remove a few-mask channel cost

### 3.1 Hybrid model and finite theorem [PROVED]

Partition the bottoms into the following groups.

* $H$ **helpers**: arbitrary table normals and thresholds, with full-support equal-absolute-magnitude address normals. Pure-table helpers may instead be absorbed into table-only terms.
* For each nonempty character $T$, $E_T$ **channel gates**: table normals in $\operatorname{span}\{\mathbf1,\chi_T\}$. Their address rows have magnitude $|u_j|>0$ on all selected raw coordinates $B_T$ and magnitude $|v_j|$ on all ignored coordinates, with $|v_j/u_j|\le\Lambda$. The signs come from at most $R$ fixed masks for that character. The real scales may vary from gate to gate; they need not be rational or commensurable. The case $v_j=0$ includes sparse character supports.
* Any additional **table-only gates**, **pure-address gates**, and **constant-table-normal gates** are allowed without restriction. In each complementary-character score difference they contribute only constants or cancel.

All top weights and raw top wires are arbitrary. Masks may differ between characters. Assume $R\ge1$, and put

$$r=\max\{2,\lfloor\log_2(2H+1)\rfloor+1\},\qquad
B=\lfloor(1+\Lambda)r\rfloor+1.$$

Thus $2^r>2H$. For a fixed $T$, write $d=m|T|$, $e=M-d$. If

$$\lceil d/2^R\rceil\ge r,\qquad \lceil e/2^R\rceil\ge r,$$

then

$$\boxed{E_T\ge
\frac{\lceil d/2^R\rceil-r+1}{2B}.}$$

**Proof.** Compare the complementary $T$-character tables as in §1. Every other channel cancels because its table normal is orthogonal to $\chi_T$. Pure-address and raw address terms cancel. Table-only gates and all constant differences contribute only a constant. The resulting strict signed target is $\chi_T(b)$.

Group the $d$ selected coordinates by their signs in the at most $R$ masks. Some class has size $D\ge\lceil d/2^R\rceil$. Likewise an ignored class has size $Q\ge\lceil e/2^R\rceil$. These two classes need not have the same sign pattern. Retain $r$ live coordinates from each class. Fix all other coordinates to zero, except that exactly $s$ of the $D-r$ remaining selected-class coordinates are set to one, where $0\le s\le D-r$.

For every gate in channel $T$, the value of its raw address form on this restriction has the form

$$c_j+\epsilon_j u_j s+epsilon_j u_j\sum_{i=1}^r z_i
                         +\eta_j v_j\sum_{i=1}^r w_i,$$

where $\epsilon_j,\eta_j\in\{\pm1\}$ depend on its mask. At either fixed table, its live values have a minimum and maximum separated by

$$r(|u_j|+|v_j|).$$

The baseline moves by nonzero magnitude $|u_j|$ when $s$ increases by one. Hence the gate can be nonconstant on the live cube for at most

$$\left\lfloor\frac{r(|u_j|+|v_j|)}{|u_j|}\right\rfloor+1\le B$$

integer choices of $s$. This is just counting integers in an interval; it does not presume dense attained intermediate values or any minimum gap. Threshold endpoint ties are harmless: nonconstancy occurs exactly when the threshold is strictly above the minimum and at most the maximum.

There are two fixed-table versions of each of the $E_T$ channel gates. If $D-r+1>2E_TB$, some $s$ makes every such gate constant on the entire $2r$-dimensional live cube. The strict top-score difference would then sign-compute, up to one fixed sign from the fixed bits, parity on the $r$ selected live bits using at most $2H$ helper restrictions and a constant.

Every helper restriction remains a full-support equal-magnitude threshold on the $2r$ live variables. The inherited pairing theorem therefore requires $2H\ge2^r$, contrary to the choice of $r$. Thus $2E_TB\ge D-r+1$, which implies the claimed bound. $\square$

The proof makes the channel gates individually constant on a common restriction before invoking the pairing obstruction. It does **not** quotient arbitrary missing-variable gates for free or demand multiple parity-correlated survivors. This distinction avoids the explicit counterexample discussed in §4.

### 3.2 Balanced exponent consequence [PROVED]

For fixed $R,\Lambda$ and $H\le n^C$ with fixed $C$, $r=O(\log n)$ and $B=O(\log n)$. There are $\Omega(N)$ middle characters with $k/3\le |T|\le2k/3$, for which $d,e=\Theta(M)$. Their class-size conditions hold for all sufficiently large balanced instances. Summing §3.1 gives

$$\boxed{\sum_T E_T=\Omega\!\left(\frac{MN}{\log(H+2)}\right)
=\Omega(n^2/\log n).}$$

More explicitly the proof pays a factor $2^R(1+\Lambda)$ before suppressing fixed constants. Allowing that factor to be $n^{o(1)}$ still prevents a fixed-power exponent improvement whenever the stated class-size hypotheses hold. No assertion is made when those hypotheses fail.

This is the strongest own round-two architecture obstruction. It allows dense signed Walsh table normals in the helpers, genuinely unequal real scales in the channels, sparse channel supports, arbitrary top coefficients and no drift assumptions. A finite family of small-scale modifications to the forbidden full-sign pool, together with polynomially many full-sign helpers, therefore does not supply $n^{2-\epsilon}$ in this model.

### 3.3 Sharper one-mask, integer two-scale version [PROVED; independently checked by LOW2]

When a channel uses one signed direction of magnitudes $1$ on $T$ and $2$ off $T$, flip its negative raw coordinates and absorb the resulting constant. The form is $L=p+2q$, with $p\in\{0,\ldots,d\}$ and $q\in\{0,\ldots,e\}$. Its levels fill $0,\ldots,K=d+2e$.

The $2E_T$ fixed-table channel cuts partition these levels into at most $2E_T+1$ constant-truth intervals, one with at least $\lceil(K+1)/(2E_T+1)\rceil$ consecutive levels. If $d\ge r+1$, $e\ge r$, and its length is at least $3r+1$, retain $r$ variables of each kind. The fixed coordinates can realize every baseline in $0,\ldots,K-3r$, because $d-r\ge1$ and their sums are $p_0+2q_0$. Choose a baseline placing the live range in the interval. The same helper contradiction applies. Consequently

$$E_T>\frac12\left(\frac{K}{3r}-1\right).$$

The sparse $1/0$ version has live width $r$ and baseline range $0,\ldots,d-r$. The general proof in §3.1 is stronger in scope because it permits several masks and real unequal scales; this special case gives an especially transparent interval picture. LOW2 checked the full interval and embedding argument on the board.

### 3.4 Exact scope limits

[PROVED audit] Helpers with generic unequal magnitudes are outside the theorem. Channel gates coupling several nonconstant Walsh table statistics are outside its character-isolation hypothesis. Arbitrarily many sign masks, or a scale ratio large enough to erase the finite bound, also escape. These are substantive restrictions, not normalizations of unrestricted gates. In particular the theorem does not refute LOW2's genuinely unequal-magnitude common-cone examples or provide an unrestricted lower exponent.

## 4. Other ideas, attacks, and lessons from the exchange

### 4.1 Averaging pairings over magnitude classes [PROVED auxiliary lemma; developed further by LOW1]

If one magnitude class occupies $a$ selected and $b$ ignored positions in a random perfect matching of two halves of size $d$, its number $Q$ of matched pairs is hypergeometric. Sampling without replacement from $b$ values $1/2$ and $d-b$ values $1$ gives

$$\mathbb E2^{-Q}\le(1-b/(2d))^a\le e^{-ab/(2d)}.$$

The first inequality is the elementary symmetric-mean inequality; it also follows by repeatedly replacing two unequal positive entries by their average, which preserves their sum and raises every elementary symmetric polynomial of order at least two. This was sent to LOW1. LOW1 developed the stronger multi-class permanent bound and blockwise-histogram theorem; that development is credited to LOW1, not counted as an independent UP2 theorem.

For equal nonzero magnitudes with arbitrary zero support, a useful exact matching formula is also available. If the support has $a$ selected and $b$ ignored positions, its full-dependence probability under a random matching and random literal signs is zero when $a+b<d$, and otherwise

$$2^{d-a-b}\frac{\binom b{d-a}}{\binom d{d-a}}.$$

Indeed, every missing selected-side coefficient must match an occupied ignored-side position; conditional on that event, exactly $a+b-d$ pairs have two nonzero equal coefficients and each survives one of its two literal signs. This is an evaluation of the inherited cover inequality, not a new unrestricted bound. It makes precise why supports aligned to a character escape while unrelated supports are inefficient. The raw support formula alone does not enforce a common top.

### 4.2 Survivor-only slicing is false [PROVED counterexample, attribution LOW2 and LOW1]

LOW2 supplied the exact monomial expansion

$$\prod_{i=1}^d(1-2z_i)=\sum_{U\subseteq[d]}(-2)^{|U|}[z_i=1\text{ for every }i\in U].$$

Only one bottom depends on all $d$ variables. LOW1 strengthened the helper count to quadratic via a missing-coordinate ladder decomposition. Thus a parity-correlation argument cannot simply demand many fully dependent survivors after discarding all missing-variable gates; that quotient is one-dimensional. I agreed with the attack and stopped pursuing this false amplification. Section 3 instead pays for actual channel constancy on a common live cube.

### 4.3 Guards and coupled geometry [PROVED checks; unresolved construction]

UP1's edge-incidence masks preserve selected parity and collapse quadratic Fourier cross terms, but its complementary-character tail attack still refutes bounded-degree polynomial repairs of saturated channels. Its logarithmic halfspace-product compiler introduces a real approximate guarding tool; all peers stressed that a sign-correct product with variable magnitude is insufficient to preserve an arbitrary sum's margin. I did not obtain a useful common-top score with a polynomially better variation-to-margin ratio.

[PROVED CHECK, attribution UP1] UP1 subsequently closed this particular sampling target: every raw threshold on $d$ parity bits has full-parity Fourier coefficient at most $1/(2\sqrt d)$. After complementing signs, monotonicity gives $2|\widehat g([d])|\le I_i(g)$ for each coordinate, while Cauchy and Parseval give $\sum_i I_i(g)\le\sqrt d$. I checked the argument on the board. Fixing ignored bits and averaging preserves the bound. On a saturated complementary-character pair the original central-window score has zero target correlation, so a table-only guarded correction of threshold top variation $B$ and exact margin $\mu$ needs $B/\mu\ge2\sqrt d$. UP1's whole-score sampler therefore certifies quadratic-or-worse size on these middle-character tails. This blocks that norm-based compiler route, not unrestricted circuits with arbitrarily large cancellations.

The sparse-Walsh theorem is a concrete all-size obstruction to an otherwise plausible next step: coupling only a fixed/polylogarithmic number of Walsh table statistics while retaining individually bounded integer address ratios. UP1 checked that a table-only guard, including its real-scale logarithmic compiler, preserves that address-normal property. Large table-side guard coefficients do not by themselves evade it. A genuinely new exact design needs sufficiently rich semantic table coupling, or different address arithmetic/geometry.

LOW2's exact unequal-magnitude oriented-rectangle certificate demonstrates finite infeasibility beyond any equal-magnitude representation. I read its board statement and did not independently rerun that certificate. It is a guardrail, not asymptotic evidence against every unequal-magnitude pool.

## 5. Verification and artifacts

[VERIFIED] Run `python3 -I /tmp/andreev_gap/swarm_round2/up2/checks.py`. The standard-library-only script uses exact integer and rational arithmetic and writes `checks.json` with author credit. It passed:

* 10,400 table-pair gate/slab evaluations, including 7,184 exact channel cancellations and 50 semantic-activity subset tests;
* 19,728 complete inputs of five compiled two-scale lookup circuits, totaling 4,241,536 raw bottom evaluations, with the exact score $N(1-2x_b)$;
* 587 selected-cube edge checks against the actual character-pair threshold features;
* 10,415 exact hypergeometric overlap inequalities and 340 complete mixed-support matching formulas;
* 31,952 rational-scale bad-baseline counts for the hybrid proof, including threshold ties and both slope signs;
* 5,775 integer baseline embeddings for the one-mask interval proof.

These finite checks validate formulas and edge cases of the written all-size proofs. They are not evidence extrapolated to an exponent. No floating-point LP result is being promoted to a theorem here.

[PROVED CHECKS / attribution] LOW2, LOW1, and UP1 all checked §1's complementary-character slab charge. LOW1 proposed the semantic activity refinement. LOW2 and LOW1 checked the one-mask hybrid proof; the general few-mask extension uses the explicit bad-baseline count in §3.1. I supplied LOW1's initial hypergeometric overlap lemma, checked LOW2's near-equality compiler and the survivor counterexample, and gave UP1 the sparse-coupling guard obstruction. Full append-only discussion is in `../board.md`.

## 6. Final assessment and next step

[PROVED restricted conclusions] Small Walsh coupling with bounded integer address ratios has a quadratic cost; full-support two-scale Fourier channels have matching exponent two; and polynomially many full-sign helpers do not remove the near-quadratic cost of fixed-mask, bounded-ratio real two-scale channels. These close specific escape architectures left open in round one while preserving unrestricted top coefficients and exactness.

[UNRESOLVED] No exact $n^{2-\epsilon}$ ordinary-Andreev circuit and no unrestricted $n^{3/2+\epsilon}$ lower bound were proved. Rare character-table comparisons remain crucial, but generic dense semantic table coupling and heterogeneous real address directions still escape the restrictions above. No priority claim beyond the recorded investigation, formalization claim, or publication claim is made.

[CONJECTURE / single most promising next step] Target a jointly feasible bottom library whose useful gates react nontrivially to polynomially many complementary character pairs AND whose address directions vary beyond a bounded family of two-scale masks. Use the exact common-top cone from the beginning. In particular, test shared nonlinear tail corrections with genuinely dense semantic Walsh coupling against the explicit two-scale exact family and the hybrid theorem, rather than adding more sparse-channel guards or full-sign helpers. This is a concrete remaining requirement, not an existence theorem.
