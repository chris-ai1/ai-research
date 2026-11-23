# UP2 — alternative exact depth-two architectures

Authors: Christian Reitwiessner

Date: 2026-11-11. Agent: UP2 (OpenAI Astra). Status: completed research handoff; originally saved immediately on restart and updated after each major idea. No additional agents; no edits to shared paper.

## Outcome at handoff

[PROVED] Strongest architecture obstruction (§6): if each bottom address row is full-support with one absolute magnitude per gate, then $S\ge2^{m\lfloor k/2\rfloor}=2^{\Omega(n)}$, with arbitrary table coefficients and arbitrary real top weights. A paired-literal restriction proof replaces the longer separated-mask dual; LOW2 independently checked it. For the fixed-table half-parity subproblem a finite-difference construction matches this exponential rate up to a polynomial factor and was exactly checked.

[PROVED] Additional obstructions: polynomial-size table-measurement rank is $\Omega(N/\log N)$ (§1); two shared address statistics per block still require $\widetilde\Omega(n^2)$ gates by the inherited runs lemma (§2); exchangeable random unequal-magnitude pools have exponentially small normalized exact margin even with adaptive thresholds (§4.4). The last statement does not rule out arbitrary-weight exact feasibility.

[UNRESOLVED] No unrestricted exponent improvement. Full proofs, checks, source/priority limits and board exchanges follow; no rediscovery is asserted as a new literature result.

## Scope and inherited constraints

[KNOWN, COMMON.md and review_coherence/report.md] Ordinary Andreev has independent table bits $x_c$, $N=2^k$, parity-address blocks of length $m$, $km=\Theta(N)$, and unrestricted real bottom/top weights with direct raw top inputs. Exact unrestricted bounds remain $\widetilde\Omega(n^{3/2})$ and $O(n^2)$. This report seeks a different architecture or a precise family obstruction, not a constant improvement.

[KNOWN, corrected review_coherence §§1–2] The drift conclusion applies ONLY to eligible blocks whose EVERY coefficient is globally comparable to the maximum address coefficient; a gate can have no eligible block. It does not reduce the problem to zero-sum gates. The sign-coherent lower bound is paper Section 6, Theorem 12. All block-count-only constructions are sign coherent and therefore cannot improve the exponent.

[KNOWN, COMMON.md] One-table-bit bounds and average-case exponent $3/2$ are existing results, not targets to rediscover. Lex-packing additive staircases, character sharing, and simple table chunks have already failed.

## Research queue

1. Dense alternative table transforms: exact sign recovery, entrywise dominance and unavoidable implementation costs.
2. Geometric/lexicographic architectures whose address normals vary within blocks, including decision lists and coded arrangements.
3. Matrix/self-reduction and nonlinear feature lifting with no hidden extra depth.
4. LP existence and quantitative exact-margin obstructions; check promising survivors exactly on small raw instances.

Every substantive claim below will be labelled [PROVED], [VERIFIED], [CONJECTURE], [REFUTED], or [KNOWN, source]. Board communication is append-only.

## 1. Low-dimensional real table registers: a geometric obstruction

### 1.1 Exact model and theorem [PROVED]

Write a general top score as

$$F(x,a)=\beta\cdot x+\delta\cdot a+\beta_0+\sum_{j=1}^S v_j[\alpha_j\cdot x+\gamma_j\cdot a\ge\theta_j].$$

Suppose the span of the table normals $\{\alpha_j\}$ has dimension $r$. Choose a basis and let $T:\mathbb R^N\to\mathbb R^r$ be the resulting table-feature map. For each parity label $b$ choose one raw address representative $a_b$. Each of the $NS$ restricted bottom tests is a halfspace in $T(x)$.

All relevant sets are finite. Replace every bottom threshold by a sufficiently small downward perturbation to preserve all Boolean gate outputs while putting no Boolean input on its boundary. The $NS$ affine hyperplanes consequently assign each $T(x)$ to an open cell. An arrangement of $H$ hyperplanes in $\mathbb R^r$ has at most $\sum_{i=0}^r\binom Hi$ open cells (induct on $H$, charging new cells to the induced arrangement on the new hyperplane). Dependencies or coincident hyperplanes can only decrease this bound.

Within one cell, the bottom outputs at each of the $N$ representatives are fixed. Hence the output table has the form

$$x_b=[\beta\cdot x+c_b\ge0]\qquad(b\in\{0,1\}^k),$$

with $c_b$ fixed on that cell. As the single scalar $\beta\cdot x$ varies, these $N$ threshold tests produce at most $N+1$ distinct binary vectors. Exact computation makes that vector equal to the table $x$ itself; there cannot be more than $N+1$ tables in one cell. Therefore

$$\boxed{2^N\le(N+1)\sum_{i=0}^r\binom{NS}{i}.}$$

This includes arbitrary real address weights, arbitrary top signs, all free raw top inputs, and any block lengths. It does not assume coherence, zero drift, bounded weights, or uniform table distribution. No novelty priority is claimed for the elementary arrangement argument.

### 1.2 Consequences [PROVED]

For $r=1$,

$$S\ge\frac{2^N/(N+1)-1}{N}.$$

Thus a single exponentially weighted binary or mixed-radix encoding of the table cannot support a polynomial-size circuit even if every gate uses a different raw-address normal and threshold. The obstruction is the order/partition complexity of reading all coordinates, not the precision of the real register. If there is no direct table input at the top, replace $N+1$ by one.

For $1\le r\le NS$, the standard arrangement estimate gives

$$N-\log_2(N+1)\le r\log_2(eNS/r).$$

If $S\le N^C$ for fixed $C$, then $r=\Omega(N/\log N)$. In particular any proposed $N^{2-\varepsilon}$ architecture based on $N^{1-\eta}$ linear table measurements, for fixed $\eta>0$, is impossible. For fixed $r$ the gate cost is exponential in $N/r$, not a subquadratic exponent. Full-rank Fourier, wavelet, random-projection and coding transforms survive this obstruction and still need an implementation argument.

### 1.3 Exact dense pair-sharing identity [PROVED]

For $\eta\in\{\pm1\}^N$, $W>0$ and any address form $t(a)$, set $g=[t(a)+W\sum_c\eta_c x_c\ge0]$. On singleton tables,

$$g(e_c,a)=[t(a)\ge W]+\frac{1+\eta_c}{2}[-W\le t(a)<W].$$

The difference of two singleton restrictions is $(\eta_c-\eta_d)/2$ times the same slab. Thus one dense-table gate simultaneously contributes to all table pairs separated by a code word. This is an explicit obstruction to independent per-pair charging with no table-support factor, not a computing circuit. Sent to LOW1 for its cancellation search.

## 2. Geometry through a small number of raw linear statistics

### 2.1 The inherited common-runs theorem [KNOWN, mixed_sign/report.md §2]

Fix a common order of coordinates in each block. Let $\rho_{j,i}$ count the nonzero sign runs in the weights of gate $j$ in block $i$ (use one for an identically zero block). The existing Runs Lemma gives at most

$$m^k-\prod_i(m-\rho_{j,i})\le m^{k-1}\sum_i\rho_{j,i}$$

split cubes for every table. For completeness, partition each prefix-count axis into its monotone step runs. On each resulting box the coherent diagonal argument applies. Summing its product-of-side-lengths bound across the boxes gives the displayed result. Cube entropy (paper Theorem 12 proof) demands expected splitting $D_0$ on every cube, where

$$D_0=\frac{\max\{0,N-k-1-\log_2(S+1)\}}{k+\log_2(S+1)}.$$

Consequently, if all $\rho_{j,i}\le R$,

$$S\ge\frac{mD_0}{kR}.$$

For $S<N^2$, this is $S\ge m(N-3k-1)/(3k^2R)$ and hence $\widetilde\Omega(n^2/R)$ at balance. This theorem is inherited, not newly discovered.

### 2.2 Rank-two address geometry [PROVED corollary]

Assume for each block $i$ there is a fixed real vector space $V_i\subseteq\mathbb R^m$ of dimension at most two containing the restriction of EVERY gate's address normal to that block. Table weights, top weights and all magnitudes remain arbitrary. Write

$$\gamma_{j,i,l}=u_{j,i}p_{i,l}+v_{j,i}q_{i,l}.$$

Order the nonzero coordinate vectors $(p_{i,l},q_{i,l})$ around the plane by polar angle and put zero vectors anywhere. A nonzero linear functional is positive on one open half-circle and negative on the opposite half-circle; along the linearized circular order, deleting zero evaluations, it changes sign at most twice. Thus every gate has at most three runs in every block in ONE common order. This also covers collinear vectors, repeated angles, zero coefficients and zero linear functionals.

The preceding inherited lemma with $R=3$ proves

$$\boxed{S\ge\min\{N^2,\ m(N-3k-1)/(9k^2)\}=\widetilde\Omega(n^2).}$$

Interpretation: allowing two arbitrary real weighted address statistics per block, followed by arbitrary combinations in every bottom threshold, does not change the quadratic exponent. The normals can have many mixed sign patterns and arbitrarily bad global comparability. The result therefore does not follow by treating the corrected drift theorem as an unrestricted zero-sum theorem. It is an elementary application of the prior runs theorem; no independent novelty claim is made for low-crossing geometric arguments.

### 2.3 Polynomial/moment-curve normal families [PROVED corollary]

More generally suppose there are fixed parameters $t_{i,l}\in\mathbb R$ and fixed nonzero weights $w_{i,l}$ such that every gate has

$$\gamma_{j,i,l}=w_{i,l}p_{j,i}(t_{i,l}),\qquad \deg p_{j,i}\le d.$$

A common raw bit flip changes the signs of $w$ to positive; this permutes the parity labels and hence relabels the independent table coordinates, preserving ordinary Andreev and gate count. Sort coordinates by $t$. A nonzero real polynomial of degree $d$ changes sign at most $d$ times, and repeated roots/parameters/zero evaluations cannot increase the number of nonzero sign runs. Thus $R\le d+1$ (or use the trivial cap $m$), giving

$$S\ge\min\{N^2,\ m(N-3k-1)/(3k^2(d+1))\}=\widetilde\Omega(n^2/(d+1)).$$

For fixed or polylogarithmic degree, this family cannot have exponent below two. Degree $d=n^\delta$ permits only the lower exponent $2-\delta$ by this argument, not an upper construction. The same reasoning works for piecewise polynomial rows with $P$ shared pieces, giving $R\le P(d+1)$; it must not be asserted for arbitrary high-dimensional random or code normals. This excludes a concrete broad family of lattice/moment-curve-style universal arrangements but not unrestricted geometry.

### 1.4 Middle-layer strengthening [PROVED; checked after board feedback]

Within a fixed cell the possible exact tables are a coordinatewise chain, not merely $N+1$ arbitrary patterns. Two distinct tables of the same Hamming weight are incomparable, so at most one middle-layer table belongs to any cell. The stronger inequality is

$$\boxed{\binom{N}{\lfloor N/2\rfloor}\le\sum_{i=0}^r\binom{NS}{i}.}$$

For one table direction this gives $S\ge(\binom{N}{\lfloor N/2\rfloor}-1)/N$. No appeal to Sperner's theorem is needed beyond counting the middle layer; this is an explicit antichain. It changes only polynomial factors in the exponential obstruction. LOW2 independently checked the original arrangement/tie/raw-top argument and the rank-two polar-order argument on the board.

## 3. Transform and tensor candidates killed by their exact conditions

### 3.1 Separable address dictionaries require full dimension [PROVED elementary condition; related rank bounds are KNOWN]

Suppose the proposed score after parity-fiber averaging is

$$P_x(b)=\sum_{j=1}^q h_j(L_j(x))g_j(b)+c(x),$$

where the fixed $g_j$ are arbitrary real address functions, $L_j$ are linear table forms, and $h_j$ may be completely arbitrary nonlinear functions. Exactness is the pointwise strict sign condition $(2x_b-1)P_x(b)>0$, after harmless top strictification. Let $V=\operatorname{span}(1,g_1,\ldots,g_q)\subseteq\mathbb R^N$. If $V$ were proper, choose a nonzero $w\in V^\perp$ and a table with $2x_b-1=\operatorname{sgn}w_b$ on its nonzero coordinates. Then $w\cdot P_x>0$, contradicting orthogonality. Hence $V=\mathbb R^N$, so $q+1\ge N$.

This gives the exact sign-realizability condition at the address-dictionary level: every table orthant must intersect the set of actually attainable coefficient vectors, and full span is necessary, not sufficient. Arbitrary nonlinear table quantizers do not evade the full-dimension necessity. Raw affine address terms disappear into $c(x)$ under uniform averaging over each parity fiber when $m\ge2$, since each raw bit then has conditional mean $1/2$; strict sign correctness survives averaging. The theorem assumes the displayed separated form; it is not a rank bound for arbitrary joint halfspace features.

[KNOWN, corrected review_coherence §6] If the $g_j$ are characters and each is implemented by its own one-dimensional parity ladder, all $N$ characters are necessary and the disjoint implementation costs $\Omega(\sum_T|T|m)=\Omega(kNm)=\Omega(n^2)$. The valid lower count uses monotone chains of attainable values, not numerical range, and survives arbitrary odd weight magnitudes. This is an existing dedicated-ladder obstruction; replacing Fourier coefficient amplitudes by wavelets, saturation, or random projections does not by itself remove it.

### 3.2 Matrix recursion and tensor rank [PROVED obstruction to the stated algebraic scheme]

Split a parity label into two halves of sizes $q_1,q_2$ with $q_1q_2=N$, view the table as $M\in\mathbb R^{q_1\times q_2}$, and write lookup $u^TMv$ for one-hot selectors. An exact trilinear identity

$$u^TMv=\sum_{r=1}^R L_r(M)P_r(u)Q_r(v)$$

with all three factors linear requires $R\ge N$: flatten the coefficient tensor along the $M$ coordinate. Its $N$ matrix-entry slices are the $N$ independent coordinate functions $u_iv_j$, whereas a sum of $R$ simple tensors has flattening rank at most $R$. The bound is attained by the obvious $N$ entries. Therefore fast matrix-multiplication tensor decompositions cannot reduce the number of scalar products for this lookup tensor. This is ordinary flattening rank, not a new tensor-rank theorem.

A sign-only replacement is not killed by equality-rank alone; the preceding full-address-dimension condition still rules out fewer than $N-1$ fixed separated address features, but gates mixing table and address need not be separated. More importantly, implementing $P_r(u)$ or $Q_r(v)$ by their own circuits and feeding them to lookup gates adds depth. A valid subquadratic self-reduction still needs an explicit raw-input flattening identity with per-feature cost $o(N)$ and no independent full-parity ladders. No such identity was obtained.

### 3.3 Nonnegative group tests [KNOWN from current LOW2 board result; reviewed here]

LOW2's private-kernel reduction covers circuits syntactically monotone in table bits after normalizing top gate coefficients positive: all table coefficients and all direct top table coefficients must then be nonnegative. It converts such circuits to private dominating slabs and imports the inherited $\widetilde\Omega(n^{32/19})$ one-table-bit lower bound, or $\widetilde\Omega(n^2)$ with bounded integer address normals. I checked the owner/nonowner inequalities including endpoints. This is LOW2's restricted-model extension; it is not mine and does not exclude signed table-code decoding.

## 4. Nonconstructive dense random pools: an exponential margin obstruction

### 4.1 Candidate pool and exact condition [PROVED]

A natural geometry-first pool uses arbitrary table normals and random full-support signed address normals, all of one magnitude within each gate:

$$g_j(x,a)=[\alpha_j\cdot x+G_j\sum_{l=1}^{M}\sigma_{j,l}a_l\ge\theta_j],\quad \sigma_j\in\{\pm1\}^M,\quad M=km.$$

Allow arbitrary thresholds, arbitrary top weights, arbitrary free affine terms, arbitrary $G_j>0$, and also pure-table gates. This library has high splitting probability and includes the simultaneous-survival counterfamilies. An LP for fixed bottoms asks for $(2A-1)F\ge1$ on every Boolean input. Feasibility alone is not ruled out below; what fails is a polynomial ratio between top coefficient variation and exact margin.

### 4.2 Exponential normalized-margin theorem [PROVED]

Choose nonempty $T\subseteq[k]$ with $d=|T|m\ge2$, and restrict the table affinely to two complementary character tables:

$$x_c=\frac{1+y\chi_T(c)}2,\quad y\in\{\pm1\}.$$

The target output sign is $f(y,a)=y\chi_T(b(a))$, a Walsh monomial in $y$ and the $d$ raw address coordinates in the selected blocks. Give $y$ and all raw address bits their independent uniform distributions.

For fixed $y$, complement the raw address coordinates with negative $\sigma_{j,l}$. The restricted bottom is now a symmetric Boolean function of all $M$ raw address bits. All its degree-$d$ Walsh coefficients have the same magnitude before undoing those flips. Parseval and $\operatorname{Var}(g_j)\le1/4$ give

$$|\widehat g_{j,y}(B_T)|\le\frac1{2\sqrt{\binom Md}}.$$

This holds for every threshold and every table normal, including constant restrictions. Therefore

$$|\mathbb E[f g_j]|=\left|\frac{\widehat g_{j,+}(B_T)-\widehat g_{j,-}(B_T)}2\right|\le\frac1{2\sqrt{\binom Md}}.$$

Every affine raw top term has zero correlation with $f$: table terms become affine in $y$, address terms depend on at most one address bit, and $d\ge2$. Pure-table bottoms also have zero correlation. If an exact score $F$ has minimum signed margin $\mu>0$ on this restricted finite domain, then

$$\mu\le\mathbb E[fF]\le\frac{\sum_j|v_j|}{2\sqrt{\binom Md}}.$$

Hence

$$\boxed{\frac{\mu}{\sum_j|v_j|}\le\frac1{2\sqrt{\binom Md}}.}$$

Taking $|T|=\lfloor k/2\rfloor$ in the balanced growing-$k$ regime makes $d/M$ bounded away from zero and one, so the normalized exact margin is $\exp(-\Omega(M))=\exp(-\Omega(n))$.

### 4.3 Scope, failure mode and escape routes

[PROVED] This kills an exact construction justified by polynomial normalized margin and sampling/boosting from this dense equal-magnitude pool. Its difficulty is stronger than the usual $1/N$ Fourier reconstruction margin: high-degree information in a selected half of the blocks is exponentially diluted by dependence on the other raw coordinates. Large table coefficients do not repair the bound because it holds for every threshold after each fixed table substitution.

[NOT A GATE LOWER BOUND] Arbitrarily large top coefficients and cancellations can have exponentially poor normalized margin while computing exactly. The task explicitly permits those coefficients. Therefore the theorem does NOT exclude a subquadratic circuit from the entire pool, and does not contradict any known upper bound or the survival barrier. A standard sampling bound using normalized margin would require exponentially many samples; this is failure of that proof route, not a lower bound on every deterministic subset.

[CONJECTURE/OPEN] Unequal address magnitudes, character-dependent supports, or a genuinely cancellation-based exact LP solution might avoid this obstruction. The known Fourier construction does use character-dependent supports; full-support random-mask sampling should not be mistaken for it. This theorem was posted early to LOW1/LOW2 as a correctness-dependent constraint beyond marginal split counts.

### 4.4 Random continuous directions: thresholds may be adaptive [PROVED]

The equal-magnitude assumption can be removed for a distributional architecture obstruction. For a fixed real direction $w\in\mathbb R^M$, define

$$C_w(B)=\sup_{\theta\in\mathbb R}|\widehat{[w\cdot a\ge\theta]}(B)|.$$

**Maximal Fourier lemma.** For every $w$,

$$\sum_{B\subseteq[M]}C_w(B)^2\le(M+1)^2.$$

**Proof.** Order all $2^M$ Boolean vertices by decreasing $w\cdot a$, breaking ties arbitrarily. Every threshold set is a prefix in this order. Fix the complete binary interval tree on its $2^M$ positions, including leaves and root. Every prefix is a disjoint union of at most $M+1$ tree intervals. If $I$ denotes the indicator of the corresponding set of Boolean vertices, Cauchy gives, for every $B$ and every prefix $P$,

$$|\widehat{1_P}(B)|^2\le(M+1)\sum_{I\text{ in its decomposition}}|\widehat{1_I}(B)|^2\le(M+1)\sum_{I\text{ in the tree}}|\widehat{1_I}(B)|^2.$$

The last expression is independent of the prefix, so it bounds the supremum over thresholds. Summing over $B$ and applying Parseval to each $1_I$, each dyadic level contributes exactly $\sum_I\Pr(a\in I)=1$. There are $M+1$ levels, proving the bound. Ties cause no issue because actual threshold sets are a subset of the considered prefixes. This elementary dyadic maximal estimate is supplied in full; no novelty priority for maximal-inequality techniques is claimed.

Now let the distribution of $w$ be invariant under permutations of the $M$ raw coordinates. Every $C_w(B)$ with $|B|=d$ then has the same distribution, so

$$\mathbb E C_w(B)^2\le\frac{(M+1)^2}{\binom Md}.$$

For a pool of $S$ directions whose marginals are exchangeable (independence is unnecessary), Markov and a union bound give, with probability at least $1-\delta$,

$$\max_{j\le S}C_{w_j}(B)\le(M+1)\sqrt{\frac{S}{\delta\binom Md}}.$$

Choose $B=B_T$ from the complementary-character restriction in §4.2. The two fixed-table restrictions of each bottom have the SAME direction and potentially completely different thresholds. The supremum in $C_w$ already permits both, even when the table coefficients and thresholds were chosen after seeing the pool. Thus any exact top score supported on this pool satisfies, with the same probability,

$$\boxed{\frac{\mu}{\sum_j|v_j|}\le(M+1)\sqrt{\frac{S}{\delta\binom Md}}.}$$

For polynomial $S$, $d/M$ bounded away from zero and one, and fixed $\delta$ (or suitable exponentially small $\delta$), the right side is exponentially small. Hence merely replacing random $\pm1$ normals by independent Gaussian, continuous heavy-tailed, or other exchangeable full-address directions does not supply a polynomial normalized exact margin. This remains a restriction on margin-based existence/sparsification arguments; arbitrary exponentially ill-conditioned exact circuits are not ruled out. Selecting directions adaptively from a larger pool requires charging the size of the original pool or separately verifying exchangeability.

## 5. Exact obstruction for separated full-sign directions: arbitrary top weights

### 5.1 Statement [PROVED; posted for independent board review]

This strengthens §4 for a natural random-direction family and removes its top-weight restriction. Let $M\ge32$ be even and $d=M/2$. Let $\sigma_1,\ldots,\sigma_R\in\{\pm1\}^M$ satisfy

$$M/4\le\operatorname{dist}(\sigma_i,\sigma_j)\le3M/4\quad(i\ne j),\qquad R\,3^{-M/16}\le1/8.$$

Allow an arbitrary finite number of bottom gates whose address normals are positive scalar multiples of one of these sign directions; arbitrary thresholds, arbitrary table normals and all free raw top inputs are allowed. Then no such circuit computes ordinary Andreev when $k$ is even, $M=km$, and $m\ge1$ (with the displayed large-$M$ conditions). In fact, after fixing the table, it cannot sign-compute ANY prescribed parity of exactly $M/2$ raw address bits.

Equivalently, even granting every possible univariate function of the Hamming distance to each center $\sigma_j$, their real linear span plus all affine raw features cannot sign-compute that half-coordinate parity. The theorem is not a bound on arbitrary full-sign direction families: the separation hypothesis is essential to this proof. It is not a lower bound for unrestricted Andreev.

### 5.2 The middle-degree kernel [PROVED]

Use raw signs $z\in\{\pm1\}^M$ and characters $\chi_U(z)=\prod_{l\in U}z_l$. Put $q=\binom M{M/2}$ and

$$\kappa_\sigma(z)=\frac1q\sum_{|U|=d}\chi_U(\sigma)\chi_U(z)=\kappa(\operatorname{dist}(z,\sigma)).$$

The standard binomial counting identity, also obtained by exchanging the two subsets in the sum, gives

$$\kappa(t)=\frac{[u^t](1-u)^{M/2}(1+u)^{M/2}}{\binom Mt}
=\begin{cases}0,&t\text{ odd},\\(-1)^{t/2}\binom{M/2}{t/2}/\binom Mt,&t\text{ even}.\end{cases}$$

Thus $\kappa(0)=1$, $\kappa(M)=(-1)^d$, and for every $1\le t\le M-1$,

$$|\kappa(t)|\le\frac1{M-1}.$$

To verify the last bound, the ratio of consecutive nonzero absolute values at $t$ and $t+2$ is $(t+1)/(M-t-1)$. Absolute values decrease to the middle and then increase symmetrically; the largest interior ones occur at $t=2,M-2$ and equal $1/(M-1)$.

Moreover, writing $\eta=3^{-M/16}$,

$$|\kappa(t)|\le\eta\quad\text{for }M/8\le t\le7M/8.$$

For an explicit proof, let $t_0$ be the smallest even integer at least $M/8$. The product formula for $|\kappa(t_0)|$ has $t_0/2\ge M/16$ factors $(2j+1)/(M-2j-1)$. Each is at most $(M/8+1)/(7M/8-1)\le1/3$ for $M\ge16$. Monotonicity and reflection cover the entire interval. Odd $t$ has value zero.

### 5.3 Interpolation with a bounded pointwise correction [PROVED]

Fix $B\subseteq[M]$ of size $d$ and target $f(z)=\chi_B(z)$. Define the $R\times R$ matrix

$$K_{ij}=\kappa(\operatorname{dist}(\sigma_i,\sigma_j)),\qquad v_i=f(\sigma_i).$$

Its diagonal is one and every off-diagonal entry has absolute value at most $\eta$. Hence $\|K-I\|_\infty\le(R-1)\eta<1/8$, so the geometric inverse series is valid. The solution $c=K^{-1}v$ satisfies $\|c\|_\infty\le8/7<2$. Set

$$P(z)=\sum_{j=1}^R c_j\kappa_{\sigma_j}(z).$$

By construction $P(\sigma_i)=f(\sigma_i)$. Since $P$ and $f$ are homogeneous Walsh degree $d$, also $P(-\sigma_i)=f(-\sigma_i)$.

For any other vertex $z$, it is within projective distance less than $M/8$ of at most one center: otherwise the triangle inequality would contradict the pairwise projective distance at least $M/4$. Every other center has ordinary distance in $[M/8,7M/8]$ from $z$. The possible near-center contribution is at most $2/(M-1)$ because $z$ is not a center or antipode. Consequently

$$|P(z)|\le\frac2{M-1}+2R\eta<1.$$

If there is no near center the first term is simply unnecessary. This pointwise inequality, not just a small Fourier correlation, is what permits an exact dual with arbitrary top weights.

### 5.4 A nonnegative exact dual [PROVED]

Define the unnormalized nonnegative mass

$$\mu(z)=2^{-M}(1-f(z)P(z)).$$

It is zero at the centers and antipodes and strictly positive elsewhere. There are other vertices: $2R<2^M$ follows from the assumed bound on $R$. Thus its total mass is positive and it can be normalized if desired.

Let $h(z)$ be ANY real function depending only on $\operatorname{dist}(z,\sigma_i)$. Its degree-$d$ Fourier coefficients have the form $\widehat h(U)=a_d\chi_U(\sigma_i)$ for $|U|=d$. Therefore

$$\mathbb E[f h]=a_d f(\sigma_i),\qquad
\mathbb E[P h]=a_d\sum_j c_jK_{ij}=a_d f(\sigma_i).$$

Since $f^2=1$,

$$\sum_z\mu(z)f(z)h(z)=\mathbb E[(f-P)h]=0.$$

The same annihilation holds for all constants and all raw affine address functions because both $f$ and $P$ have degree $d\ge2$. Every bottom gate with address normal proportional to $\sigma_i$, after fixing its table, is such a radial function. The raw table contribution at the top is then constant. Thus the signed measure annihilates EVERY allowed score $F$, regardless of its coefficients. A strictly sign-correct score would instead make every nonzero term $\mu(z)f(z)F(z)$ positive, a contradiction. Any exact threshold circuit can be strictly separated on its finite domain by shifting its top threshold slightly, so weak-positive tie conventions do not evade the contradiction.

For Andreev choose a block subset $T$ of size $k/2$ and fix table bits to $x_c=(1+\chi_T(c))/2$. The required sign becomes $f(z)=\prod_{i\in T,l}z_{i,l}$, which uses exactly $M/2$ raw bits. This proves the statement.

### 5.5 Random-pool consequence and precise limitation [PROVED]

For independent uniform sign centers, each pair distance is binomial $(M,1/2)$. The elementary exponential-moment tail estimate gives probability at most $2e^{-M/8}$ of falling outside $[M/4,3M/4]$. A union bound gives failure probability at most $R^2e^{-M/8}$. Any polynomial $R$ also satisfies $R3^{-M/16}\le1/8$ for all sufficiently large $M$.

Therefore polynomially many independent full-support equal-magnitude random address directions fail to support an exact Andreev circuit with high probability, EVEN allowing unlimited thresholds per chosen direction, adaptively chosen table normals, and arbitrary real top weights. This is an actual infeasibility theorem for that pool, stronger than the exponential-margin result. It coexists with LOW1's $\widetilde O(n^{3/2})$ pool passing every ordinary table-pair edge test: high simultaneous splitting/coverage is not shared top-score realizability.

The deterministic theorem is stated with $k$ even. The RANDOM-pool consequence extends to every $k\ge2$: when $k$ is odd, fix one entire address block to zero and keep $k'=2\lfloor k/2\rfloor$ live blocks, of total length $M'=k'm$. Restricted independent full-sign directions are still independent uniform signs, so their separation holds with the same probability estimate in $M'$. Choose the fixed character table on half the live blocks. Since $M'=\Theta(n)$ at balance, the conclusion is unchanged. A deterministic odd-$k$ family must satisfy the separation hypothesis on those live coordinates; separation on the original coordinates alone is not being silently substituted. Highly clustered masks, unequal address magnitudes, or character-dependent supports are not excluded by this exact dual. Those remain possible escape routes, not constructions. The kernel/projection method is classical Fourier algebra; this run makes no priority claim beyond giving a complete architecture-specific argument.

## 6. Strongest architecture obstruction: paired cancellation gives an exponential bound

### 6.1 Theorem [PROVED; independent board review requested]

There is a much simpler argument than §5, and it applies to ALL full-support equal-magnitude sign directions, not only separated ones. Suppose each table-reading or address-reading bottom gate has address coefficients

$$\gamma_j=G_j\sigma_j,\qquad G_j>0,\quad\sigma_j\in\{\pm1\}^{km},$$

or is pure-table. Table coefficients, thresholds, top coefficients and all direct raw top coefficients are unrestricted real numbers. For $k\ge2$ and $d=m\lfloor k/2\rfloor\ge2$, every exact circuit in this class satisfies

$$\boxed{S\ge2^d=2^{m\lfloor k/2\rfloor}.}$$

At balance, $d=\Theta(n)$, so the cost is exponential rather than $n^{2-\varepsilon}$. This is a restricted architecture lower bound, not an unrestricted Andreev exponent improvement. The proof is elementary variable identification and parity orthogonality; no novelty priority for that technique or this corollary is claimed.

### 6.2 Complete proof [PROVED]

If $k$ is odd, first fix one entire address block, leaving $k'=2\lfloor k/2\rfloor$ live blocks. Fix the table to a character on half those live blocks. In raw sign coordinates the required output sign is then the parity of exactly $d=k'm/2$ selected bits,

$$f(z,w)=\prod_{i=1}^d z_i,$$

with $d$ other live raw bits $w_1,\ldots,w_d$ ignored by this fixed target. Pair them arbitrarily with the selected bits. Removed coordinates and table inputs contribute only constants to all remaining forms.

For EVERY $t\in\{\pm1\}^d$, impose the literal restrictions

$$w_i=t_i z_i\qquad(1\le i\le d).$$

Each restriction is a legal substitution of raw bits by literals of $d$ independent live bits, so it preserves depth-two threshold form and exact correctness. The target remains $\prod_i z_i$, independent of $t$.

Write one gate's two paired address signs as $\sigma_i,\tau_i\in\{\pm1\}$. After substitution its live coefficient on $z_i$ is proportional to

$$\sigma_i+t_i\tau_i.$$

This is nonzero exactly when $t_i=\sigma_i\tau_i$. Consequently the gate reads ALL $d$ live variables only on the SINGLE restriction $t=(\sigma_i\tau_i)_i$. On every other restriction it is independent of at least one live variable. Its unique multilinear representation on the Boolean cube then has degree at most $d-1$, or, equivalently, has zero correlation with full live parity.

For a fixed $t$, if no bottom reads all $d$ variables, every bottom has zero correlation with parity. Every direct affine top term also has zero correlation because $d\ge2$. Their real linear combination therefore has zero correlation. This is impossible for a strictly sign-correct parity score, whose correlation with parity is the strictly positive average of its absolute value. Strictification of a finite correct top threshold is harmless. Thus each of the $2^d$ restrictions requires at least one bottom that reads all live variables. Each bottom can serve at most one restriction, proving $S\ge2^d$.

This conclusion is stronger than a random-pool statement: randomization, optimized deterministic sign masks, arbitrary top-weight cancellation, complete ladders and arbitrary affine table shifts all fail with fewer than exponentially many full equal-magnitude directions/gates. It explains exactly why a full random signed pool can pass LOW1's ordinary-edge tests while still being unsuitable for exact computation. The decisive restrictions identify pairs of raw variables and preserve a half-address parity target; they are not ordinary one-live-bit-per-block cube restrictions, so the known survival barrier does not apply.

### 6.3 General paired-cancellation inequality [PROVED]

For the same fixed character-table restriction and same pairing, allow arbitrary real address coefficients $u_{j,i},v_{j,i}$ on the paired selected/ignored bits. Define

$$p_j=\prod_{i=1}^d\frac{\#\{t_i\in\{\pm1\}:u_{j,i}+t_i v_{j,i}\ne0\}}2.$$

The identical parity argument says the restrictions on which some gate reads all variables must cover the full $t$-cube. Hence

$$\boxed{\sum_j p_j\ge1.}$$

If some pair has both coefficients zero, $p_j=0$. Otherwise, if $q_j$ pairs have equal nonzero absolute magnitudes, then $p_j=2^{-q_j}$; pairs with unequal magnitudes (including one zero) never cancel and contribute factor one. This is an exact necessary condition, not an unrestricted gate bound: generic unequal magnitudes can have $p_j=1$. The full-sign theorem is precisely the case $q_j=d$ for every useful gate.

The equality condition is substantive. Known character-specific supports include zero coefficients and can avoid this obstruction; unequal block scales and generic real directions can too. An arbitrarily small perturbation that preserves a gate's Boolean truth table does not change its computation and hence cannot rescue a forbidden full-sign circuit, but it can destroy the syntactic cancellation count. Any extension beyond truth-table-equivalent perturbations requires a different argument, such as the still-limited margin result in §4.4.

### 6.4 Relation to the longer exact dual

[PROVED comparison] Section 5 gives a concrete nonnegative annihilator for a separated subset of this class, and its rational small certificate remains valid. Section 6 supplies the stronger and simpler universal size lower bound for the entire equal-magnitude full-support architecture. The final result should therefore lead with §6, rather than suggesting that separation or a random-pool conditioning estimate is necessary for this class. The unequal-magnitude exchangeable-pool result in §4.4 is separate and still only a normalized-margin statement.

### 6.5 Matching exponential scale for the fixed-table subproblem [PROVED]

The paired restriction is not merely a loose exponential estimate. For partial parity $f(z,w)=\prod_{i=1}^d z_i$ on $M=2d$ raw signs, there is a full-sign circuit using at most $M2^d$ bottoms, so the architecture's exponential rate is pinned down up to a polynomial factor for this natural subproblem.

For $\sigma\in\{\pm1\}^d$ define $L_\sigma(z,w)=\sum_i\sigma_i z_i+\sum_i w_i$. Expanding the degree-$d$ power and summing with signs gives the finite-difference identity

$$\sum_{\sigma\in\{\pm1\}^d}\left(\prod_i\sigma_i\right)L_\sigma(z,w)^d=2^d d!\prod_i z_i.$$

Indeed the sign sum annihilates every monomial except those using each of the $d$ selected variables an odd positive number of times. Total degree $d$ forces each once and leaves no ignored-variable factor; the multinomial coefficient is $d!$. Each $L_\sigma$ takes the $M+1$ levels $-M,-M+2,\ldots,M$. The exact univariate function $L_\sigma^d$ telescopes into $M$ raw threshold gates on this FULL sign direction. Summing their real scores yields the displayed equality and sign-computes the target with no extra layer. The weights may be exponentially large, as the task allows.

Thus this fixed-table half-parity family has gate complexity between $2^d$ and $M2^d$ in the full-sign bottom class. This is an upper bound for the subproblem only; it is not a construction for arbitrary tables or an improvement over ordinary parity's linear circuit when zero weights are permitted. It also explains why exponentially large top weights do not rescue the requested polynomial-size architecture.

## 7. Verification and scope audit

[VERIFIED] All own computations completed successfully using only the Python standard library; no processes remain running. Run:

```
python3 -I /tmp/andreev_gap/swarm/up2/checks.py
python3 -I /tmp/andreev_gap/swarm/up2/separated_dual_checks.py
```

`checks.json` records 2,880 exact angular-order rows; 1,200 maximum split sweeps; 1,400 polynomial rows; 2,081 scalar-register cells; 29,680 dense pair-sharing identities; 2,448 symmetric Fourier coefficient checks; 260 exhaustive raw character restrictions; 128 maximal-Fourier order checks; 5,456 full-sign cancellation rows; 1,000 general paired-weight counts; and 3,049 missing-variable parity correlations. The surviving partial-parity construction of §6.5 was checked on all 1,360 raw inputs for $d=2,3,4,5$, expanding 363,776 individual raw bottom evaluations.

`separated_dual_checks.json` records 1,088 exact Krawtchouk identities and interior bounds, all 256 addresses of a rational four-direction certificate, and a 64-coordinate instance satisfying the theorem's sufficient hypotheses. The 256-address certificate has 248 positive masses, with all 36 radial-shell equations, 40 threshold equations and nine affine equations zero exactly. `separated_dual_certificate.json` contains the complete rational masses. These are checks of written universal proofs, not inference of asymptotics from finite cases.

[PROVED/KNOWN compatibility audit]

- The full-sign exponential lower bound permits arbitrary table support and arbitrary real top weights. It does not subsume the unrestricted model because zero and unequal address coefficients are essential exclusions. The known quadratic construction uses character-dependent zero supports, so there is no conflict.
- The one-table-bit $32/19$ bound remains inherited. Full-sign gates are a different, narrower address class, so an exponential bound there is consistent with all quoted bounds.
- The rank-two and polynomial-normal bounds are corollaries of the inherited common-runs lemma, not new unrestricted exponents or a reproof advertised as novel.
- Character tables are exponentially rare under the uniform independent-table distribution. Their exact obstruction is fully consistent with the known optimal average-case exponent $3/2$.
- None of these arguments infers that an arbitrary small circuit consists of zero-sum gates. The corrected global eligibility qualification is maintained throughout. Random full-sign gates may have excellent survival and near-zero drift yet still fail exact score feasibility.
- The unequal-magnitude random-pool theorem is ONLY a normalized-margin obstruction. The exact paired-cancellation theorem must not be extrapolated through small coefficient perturbations that alter Boolean gate truth tables.

[KNOWN methodological ancestry / priority unresolved] Parity orthogonality, literal restrictions, hyperplane-arrangement cell counts, finite differences and Krawtchouk projection identities are classical. A limited web search for binary-weight/partial-parity circuit lower bounds did not locate the precise pairing statement. The inspected [Baldi chapter on shallow networks](https://www.igb.uci.edu/~pfbaldi/book-deep-learning-in-science/Ch3-ShallowNetworks.pdf), §3.2.4 and Exercise 3.15, concerns single-gate binary-weight capacity and does not establish priority for the present architecture corollary. This is not an exhaustive novelty search; no new-literature-priority claim is made.

## 8. Shared-board exchange and dead ends

[KNOWN from concurrent agents; checked where stated] I posted low-rank table registers, rank-two address geometry, dense pair-sharing gates, the maximal-Fourier margin theorem, the separated-direction exact dual and the final pairing bound as candidates/results. LOW1 and LOW2 checked the arrangement argument; LOW2 checked the polar-order and maximal-Fourier arguments; UP1, LOW1 and LOW2 independently checked the radial dual; LOW2 checked the pairing proof. Exact small artifacts were exposed on the board before handoff.

I checked LOW2's owner-slab extraction and supplied explicit dense signed table rows explaining why it does not extend unrestrictedly. I checked UP1's integer-level guard identity and gave a one-gate implementation for guarded raw bits. LOW1's cheap pairwise-feasible ladders and four-point collision certificate, then its random all-pair coverage family, supplied concrete demonstrations that local geometry is insufficient. LOW2's rational positive dependence among oriented rectangles provided a common-top obstruction beyond those tests. These contributions are credited to their agents in the board and their own reports.

[DEAD-END conclusions, with exact scope]

- One huge table register, or $N^{1-\eta}$ shared real table measurements: arrangement cells are too few; polynomial gates need $\Omega(N/\log N)$ measurement rank.
- Two shared raw address statistics per block, or fixed-degree moment-curve normals: common sign runs force exponent two, even with mixed signs and huge magnitudes.
- Full-support equal-magnitude signed address normals: paired literal restrictions force $2^{\Omega(n)}$ gates. Random masks, complete ladders and huge top weights cannot rescue this class.
- Exchangeable unequal-magnitude random directions plus polynomial-margin sampling: the maximal-Fourier bound forces exponentially small normalized exact margin. Exact feasibility with huge cancellations remains open here.
- Separable transformed-table dictionaries with dedicated character ladders: full address dimension plus the inherited ladder obstruction restores quadratic cost.
- Fast matrix/tensor multiplication for a linearly separated lookup identity: the lookup tensor already has flattening rank $N$; recursive computed selectors add depth unless explicitly flattened.
- Sparse-table repair and guarded decision lists: UP1 obtained valid subquadratic promised/hybrid gadgets, but the remaining concentration-tail tables are not sparse perturbations, so this does not compute ordinary Andreev exactly.

## 9. Final status and single next step

[PROVED restricted architecture result] The strongest obstruction is §6: full-support equal-magnitude address normals require $2^{m\lfloor k/2\rfloor}$ bottom gates with unrestricted table/top coefficients. The natural fixed-table half-parity subproblem has complexity between $2^d$ and $2d\,2^d$ in this class. This is stronger than the earlier separated/random-pool impossibility and should be the lead result of this report.

[UNRESOLVED unrestricted objective] No $n^{2-\varepsilon}$ exact circuit and no improved unrestricted lower exponent were obtained. The main exact gap remains unchanged. No shared paper was edited and no additional agents were started.

[CONJECTURE / most promising next step] Seek a nonnegative exact dual for jointly chosen character-table and paired-address restrictions of **support-dependent, unequal-magnitude** gate pools. The goal is to retain shared-top feasibility constraints after exact coefficient cancellation fails. The concrete starting objects are the general paired-cover inequality in §6.3 and LOW2's oriented-rectangle positive-dependence certificates; one must obtain an exact annihilator, not merely small correlations or more un-oriented edge coverage. This directly targets the escape routes left by the strongest proved obstruction.
