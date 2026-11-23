<!-- Copyright (c) 2026 Christian Reitwiessner. All rights reserved. -->
Authors: Christian Reitwiessner

# One-table-bit threshold circuits for ordinary Andreev

Research continuation, 2026-11-09. Work directory: `/tmp/andreev_gap/one_table_bit/`.
This report is saved incrementally. Labels distinguish **PROVED** (a hand proof supplied here), **COMPUTATION**, **REFUTED**, and **OPEN**. No independent referee review or Lean formalization is claimed. Existing mathematical attribution is retained below. No shared paper is edited.

**Current baseline and progress beyond it.** Exact one-table-bit circuits require $\Omega(n^{32/19}/\log^{45/19}n)$ bottoms at balance. The reduction $S_{\rm table}\ge(N/4)\operatorname{Slice}(m)$ is independently present in the completed referee report, Section 8; the geometric slicing bound is due to Sauermann–Xu, with Klein's older theorem already giving exponent $5/3$. An exact $n^{3/2+o(1)}$ construction in this subclass is therefore ruled out. Beyond this updated baseline, this report proves an explicit valid upper bound $O(n^{1+\log_2 3})$, a near-quadratic lower bound for bounded integer address normals despite arbitrary top weights, and a coefficient-size tradeoff. The unrestricted quadratic circuit does not currently close this restricted-model gap.

## 1. Model and source audit

Put $N=2^k$, $D=km$, and $n=N+D$. There are independent table bits $x_c$, $c\in\{0,1\}^k$, and address bits $a\in\{0,1\}^D$. The label $b(a)$ consists of the $k$ block parities, and the target is $x_{b(a)}$. A bottom gate reads at most one table bit:

$$g_j(x,a)=[L_j(a)+\beta_jx_{c_j}\ge\theta_j].$$

Address weights and all top coefficients are arbitrary reals. Address-only bottoms and raw address/table inputs at the top are allowed. $S$ counts bottoms; add one for the output gate. Balanced means $D=N$ (on the integral subsequence where this is possible), or $D\asymp N$ for asymptotic comparisons.

Read: the supplied `RESEARCH_STATE.md`, `threshold_paper/paper.tex`, and the reports in `coherence_fable`, `push_lower`, `review_lower`, `upper_astra`, and `push_upper`. `review_coherence/report.md` was absent on initial inspection, appeared later, and was read first through Section 7, then through the completed Sections 8–11 following the user's update. Its Section 8 independently supplies the same single-one-table direct sum and bounded-table-fan-in extension as Section 3 below. Those are now the baseline, not an unresolved target or a novelty claim of this continuation. The completed review also confirms the essential intercept qualification and the restricted scope of the additive barrier. It does not review this report's later upper construction.

The review's other corrections are respected: drift controls only blocks comparable to the **global** address-weight scale; zeros or local-only comparability do not qualify. The source's Proposition 5.1 numerical-range argument is false because attainable values can have gaps. No bound below charges the numerical range of an arbitrary real-weight form. The explicit upper staircase uses every integer in $[0,|T|m]$, which really is attained; its exact count is justified on that attained set.

The unrestricted $5n^2/16+o(n^2)$ construction does not automatically give an upper bound in this subclass: its main ridges read many independent table bits. Its transfer must be proved, rather than inferred from its final score being affine in the table.

## 2. Exact correctness condition [PROVED]

For a fixed address, write the actual top score in bit coordinates as

$$F(x,a)=C(a)+\sum_c w_c(a)x_c.$$

This is always possible, since a function of the single bit $x_c$ is affine. More explicitly, let $h_{j,t}(a)=[L_j(a)+\beta_jt\ge\theta_j]$, $t\in\{0,1\}$. Then

$$w_c(a)=u_c+\sum_{j:c_j=c}v_j(h_{j,1}(a)-h_{j,0}(a)),$$

and $C$ includes the top constant, raw address term, address-only gates, and $\sum_jv_jh_{j,0}$. The difference $h_{j,1}-h_{j,0}$ is a signed indicator of a slab between parallel halfspaces. In terms of $q=\theta_j-L_j(a)$ it is active precisely when

$$\min(0,\beta_j)<q\le\max(0,\beta_j).$$

For the convention $[F\ge0]$, exact correctness at $a$, with $b=b(a)$, is equivalent to

$$C+\sum_{c\ne b}w_c^+<0\le C+w_b+\sum_{c\ne b}w_c^-,$$

where $w^+=\max(w,0)$ and $w^-=\min(w,0)$. These are the maximum negative-class score and minimum positive-class score, respectively. Thus the permitted intercept interval is

$$-w_b-\sum_{c\ne b}w_c^-\ \le C\ <\ -\sum_{c\ne b}w_c^+.$$

It is nonempty if and only if $w_b>\sum_{c\ne b}|w_c|$. This verifies the algebra in `coherence_fable`, Proposition 6.1, but makes its qualification “together with the matching value of $c(a)$” essential. Dominance alone is not sufficient for a given circuit: $F=2x_b+1$ satisfies dominance but outputs the constant one.

Equivalently, put $\xi_c=2x_c-1$, $K_c=w_c/2$, and $R=C+\frac12\sum_cw_c$. Then

$$F=R+\sum_c\xi_cK_c.$$

Let $A=K_b-\sum_{c\ne b}|K_c|$. The exact condition is

$$A>0,\qquad -A\le R<A.$$

If a strict margin is desired, lower the top threshold by a sufficiently small positive amount, equivalently add a small positive constant to its score. This makes every correct finite circuit strict: all negative scores were already strictly negative, and all positive scores were nonnegative. After such a shift the condition is $A>|R|$. The odd-in-table dictionary model from `upper_astra`, Section 4, has $R=0$, and its stated strict dominance condition is exactly necessary and sufficient.

### Constant-factor equivalence with pure selector kernels [PROVED]

Given any correct one-table-bit circuit, replace its score by

$$F(x,a)-F(\mathbf1-x,a)=\sum_c w_c(a)(2x_c-1).$$

Both evaluations have opposite target labels, so their difference has the correct strict sign. Each complemented bottom still reads just one table bit. Address-only gates and raw address terms cancel; at most twice as many table-reading bottoms remain. Thus intercept repair costs at most a factor two, and the pure dominance formulation loses no gate exponent.

Conversely, a kernel expressed as a constant plus signed slabs can be multiplied by its own table sign with at most four ordinary one-table-bit bottom gates per slab: expand the slab as two halfspaces, and for each halfspace $E$ use $\xi_cE=2x_cE-E$. The conjunction $x_cE$ is an actual raw-input LTF by a sufficiently large table coefficient. Address-only $E$ gates can be shared. This establishes equivalence up to constant factors with the minimum total number of slab terms in a dominating family; it does not bound coefficient magnitudes.

## 3. Direct-sum lower bound beyond exponent $3/2$ [PROVED using a cited theorem]

Let $\operatorname{Slice}(r)$ denote the minimum number of real affine hyperplanes strictly slicing every edge of $\{0,1\}^r$. A slice means opposite, nonzero signs at the two endpoints. This is equivalent under affine rescaling to the standard definition on $\{\pm1\}^r$.

**Theorem 3.1 (one-table-bit direct sum).** Every exact circuit in the model above satisfies

$$\boxed{S_{\rm table}\ \ge\ \frac N4\operatorname{Slice}(m).}$$

Here $S_{\rm table}$ is the number of table-reading bottoms; any number of address-only bottoms and all raw top wires are allowed.

**Proof.** Let $s_c$ count bottoms assigned to table bit $c$. Fix an address block $i$. Pair labels into the $N/2$ disjoint pairs $\{c,d\}$ with $d=c\oplus e_i$. For each pair, fix every block other than $i$ to an arbitrary raw string of its prescribed parity. Leave all $m$ coordinates $z$ of block $i$ free. The selected label is then $c$ or $d$, alternating according to the parity of $z$.

At a point with label $c$, dominance gives $K_c>|K_d|$, hence $K_c-K_d>0$. At a point with label $d$, it gives $K_d>|K_c|$, hence $K_c-K_d<0$. Consequently $K_c-K_d$, restricted to this $m$-cube, has strictly alternating parity sign on every edge.

The difference has the exact form

$$K_c(z)-K_d(z)=\frac{u_c-u_d}{2}
+\frac12\sum_{j:c_j=c}v_j(h_{j,1}(z)-h_{j,0}(z))
-\frac12\sum_{j:c_j=d}v_j(h_{j,1}(z)-h_{j,0}(z)).$$

It is a constant plus a linear combination of at most $2(s_c+s_d)$ halfspace indicators on $z$. There is **no raw-address affine term**: raw address inputs and address-only gates contribute only to the table-independent intercept, which disappeared when taking table coefficients. If every such indicator were unchanged across an edge, the difference would be unchanged too, contradicting its opposite strict signs. Thus these halfspaces collectively separate the endpoints of every edge.

Ties in a bottom halfspace do not cause a gap. For a nonconstant indicator $[L\ge t]$ on the finite cube, choose $t'$ strictly between $\max\{L(z):L(z)<t\}$ and $\min\{L(z):L(z)\ge t\}$. Its truth table is unchanged, and its boundary now passes through no vertex. Constants can be omitted. Each separated edge is strictly sliced by one of the resulting hyperplanes. Therefore $2(s_c+s_d)\ge\operatorname{Slice}(m)$.

Sum over the disjoint matching of labels. Every table-reading bottom is counted exactly once, so $2S_{\rm table}\ge(N/2)\operatorname{Slice}(m)$. No bound on a top coefficient or on a classification margin was used. $\square$

### Imported slicing results and the balanced exponent

**Cited theorem, not proved anew here.** Lisa Sauermann and Zixuan Xu, *Improved lower bound for hypercube edge slicing*, arXiv:2510.16592v1, Theorem 1.1, prove

$$\operatorname{Slice}(m)=\Omega\!\left(\frac{m^{13/19}}{(\log m)^{32/19}}\right).$$

Their theorem allows arbitrary real normals and offsets. The primary theorem statement was inspected directly: [paper, Theorem 1.1](https://arxiv.org/html/2510.16592v1). The reduction above therefore yields

$$S=\Omega\!\left(\frac{N m^{13/19}}{(\log m)^{32/19}}\right).$$

At balance $m=N/k$, $k=\log_2N$, this becomes

$$\boxed{S=\Omega\!\left(\frac{n^{32/19}}{(\log n)^{45/19}}\right)=n^{1.6842105\ldots-o(1)}.}$$

The older theorem of Ohad Klein, *Slicing all Edges of an $n$-cube Requires $n^{2/3}$ Hyperplanes* ([arXiv:2212.03328v2](https://arxiv.org/abs/2212.03328), FOCS 2023), already gives $\Omega(Nm^{2/3}/\log^{4/3}m)$, or $\Omega(n^{5/3}/\log^2n)$ at balance. Thus the exponent improvement does not depend exclusively on the newer $13/19$ result. These are applications of the cited geometric results; no novelty claim is made for those results or their proofs.

**Consequence.** An exact $n^{3/2+o(1)}$ construction in the one-table-bit model is impossible. The restriction is essential: a gate that reads many table bits can contribute to many label pairs, and the matching sum no longer charges each gate once.

### Alternative proof and a precise limited-read extension [PROVED]

There is a useful proof that avoids even the affine reformulation. Let $F$ be the actual top score, and let $e_c,e_d$ be tables with their unique one in positions $c,d$. On the same single-block restriction, $F(e_c,a)-F(e_d,a)$ is strictly positive when the selected label is $c$ and strictly negative when it is $d$. Every bottom not reading either $x_c$ or $x_d$ cancels. Each remaining bottom contributes the difference of two raw-address halfspaces, and the raw address top term cancels. This again gives a slicing family.

For a general circuit let $T$ be the sum of bottom-gate table fan-ins, counting nonzero aggregated table coefficients. Sum this argument over a disjoint label matching. A gate reading $t_j$ table bits occurs in at most $t_j$ pairs. Therefore

$$T\ge\frac N4\operatorname{Slice}(m).$$

In particular, if every bottom reads at most $t\ge1$ table bits,

$$S\ge\frac{N}{4t}\operatorname{Slice}(m).$$

Thus the exponent $32/19$ survives $t=n^{o(1)}$, and remains above $3/2$ for $t\le n^{\eta}$ with fixed $\eta<7/38$. This does not improve the known unrestricted total-wire lower bound: $T$ counts only table wires, and allowing $t=N$ destroys the useful gate direct sum. This exact proof uses sparse tables $e_c,e_d$ and supplies no uniform-average-case lower bound.

### Why this does not contradict the cube-accounting barrier

The proof is not demand per count-cube divided by one-gate survival. It uses a *whole* $m$-dimensional cube separately for each disjoint label pair, and a collective geometric theorem asserting that too few hyperplanes cannot slice all of its edges. The theorem is stronger than a uniform one-hyperplane edge-density bound. The literal assertion in `coherence_fable`, Section 6.2, that no one-table-bit argument can exceed exponent $3/2$ is therefore too broad if read outside its expressly additive survival template.

### Strengthened per-family statement [PROVED]

In fact $2(s_c+s_d)\ge\operatorname{Slice}(m)$ for **every** distinct pair of labels, not just adjacent ones. In each block where $c_i\ne d_i$, substitute the same $m$ free bits $z$, complementing its first bit when $c_i=1$. Fix each remaining block to parity $c_i$. Then the selected label is $c$ for even $z$ and $d$ for odd $z$. This is an affine substitution of raw bits (coordinate repetitions and complements), so all restricted gates are still halfspaces. The same proof applies. Thus at most one table family can have fewer than $\operatorname{Slice}(m)/4$ gates. A zero-gate family is possible, as Section 4 demonstrates; it forces every other family to be larger.

### Bounded address coefficients, while retaining arbitrary top weights

For fixed integer $C\ge1$, suppose each gate can be rescaled so that its address coefficients lie in $\{-C,\ldots,C\}$. Sauermann–Xu, *Nondegenerate hyperplane covers of the hypercube*, [arXiv:2507.00773v2, Corollary 1.2](https://arxiv.org/html/2507.00773v2), prove that such an $m$-cube edge-slicing family has at least $m/(4C)$ hyperplanes; offsets are unrestricted. Apply the **single-block**, disjoint-pair restriction, which preserves this coefficient bound, to obtain

$$S_{\rm table}\ge\frac{Nm}{16C}.$$

At balance and fixed $C$ this is $\Omega(n^2/\log n)$. This applies even to mixed $0,\pm1$ address coefficients, with arbitrary table coefficient and arbitrary real top weights. It is a useful sharper restricted result, not a quadratic lower bound for arbitrary real address coefficients. Merely integerizing arbitrary normals does not keep $C$ bounded.

In particular, the random one-table-bit $\pm1$ barrier family from `coherence_fable`, Section 3, of size $\widetilde O(n^{3/2})$ cannot be turned into a correct circuit by choosing clever real top coefficients, even with arbitrarily many address-only auxiliary gates. Its successful marginal-entropy accounting genuinely misses a collective obstruction. Gates having one common nonzero address-weight magnitude per gate are also covered, by rescaling each normal to $0,\pm1$.

### An address-coefficient tradeoff and coherent special case [PROVED]

The bounded-integer theorem also yields a useful tradeoff when the integer bound grows. Let each table-reading gate's address normal, after an individual rescaling, be an integer vector of maximum absolute entry $C_j\ge1$ (ignore address-constant gates). Then

$$\boxed{\sum_j C_j\ge Nm/16.}$$

Here is the weighted version of the reduction in Sauermann–Xu's Corollary 1.2. A slicing hyperplane with integer normal bounded by $C_j$ can be replaced by at most $2C_j$ parallel hyperplanes through integer levels, so that every vertex incident to an edge it slices lies on a replacement plane whose normal is nonzero in that edge direction. The nondegenerate-cover lower bound is $m/2$ (their Theorem 1.1). A label pair has at most two original planes per gate, hence $4\sum_{j\text{ in pair}}C_j\ge m/2$. Summing disjoint pairs proves the display. No top weight appears. This uses the same cited nondegenerate-cover theorem, not a new proof of that geometric result.

In particular, if $\max_j C_j\le n^\gamma$, then the balanced lower bound is $\Omega(n^{2-\gamma}/\log n)$. This is stronger than the arbitrary-real slicing exponent for fixed $\gamma<6/19$. Conversely a proposed $n^{2-\varepsilon}$ circuit must have average normalized integer coefficient scale at least $n^{\varepsilon}/O(\log n)$. This is a representation-sensitive coefficient lower bound, not a claim that arbitrary real weights have a canonical integer scale. Merely scaling an integer representation upward is harmless to the inequality; obtaining a small $C_j$ realization is the substantive hypothesis.

If the table-reading bottoms are sign-coherent in even **one common address block**, the pair restrictions for that block have unate halfspaces all oriented along the same increasing chain, up to negating their defining equations. Each slices at most one of the $m$ consecutive chain edges. Thus $2(s_c+s_d)\ge m$ and $S_{\rm table}\ge Nm/4$. This applies to arbitrary coherent magnitudes, with no integer or drift-comparability assumption. It improves logarithms in this restricted setting, not the exponent of the already near-quadratic coherent bound.

## 4. An exact one-table-bit upper bound [PROVED]

The general quadratic construction is not a valid bound for this subclass. Here is a standalone construction with

$$\boxed{S\le km\bigl(3^{k-1}+2^{k-1}\bigr).}$$

At balance it is $O(n^{1+\log_2 3})=O(n^{2.584963\ldots})$. This improves the straightforward one-table-bit Fourier expansion's cubic exponent, but leaves a substantial gap to Theorem 3.1. It is the best balanced upper bound established in this report, not a claim of optimality or exhaustive literature priority.

### 4.1 Dominance from subsets, instead of exact selectors

Identify a label with the subset of blocks where it is one. Let $\lambda=2k$ and define

$$K_c(a)=\lambda^{|c|}[c\subseteq b(a)].$$

All kernels are nonnegative. If $r=|b(a)|$, the selected coefficient is $\lambda^r$ while the sum of all other coefficients is $(1+\lambda)^r-\lambda^r$. Thus the strict margin is

$$K_b-\sum_{c\ne b}|K_c|=2\lambda^r-(1+\lambda)^r>0,$$

because $(1+1/(2k))^r\le e^{1/2}<2$. For $r=0$ the margin is exactly one. The score $\sum_c(2x_c-1)K_c$ therefore computes the target for every independent table. The large weights are allowed by the model. They grow at most $k^{O(k)}$, and are not being mistaken for gate multiplicities.

### 4.2 Raw-input threshold implementation and exact count

Write $\chi_T(b)=(-1)^{\sum_{i\in T}b_i}$ and $t_T(a)=\sum_{i\in T,j}a_{i,j}$, with $T_T=|T|m$. For nonempty $c$,

$$K_c=(\lambda/2)^{|c|}\sum_{T\subseteq c}(-1)^{|T|}\chi_T(b).$$

On integer $0\le t\le T_T$,

$$(-1)^t=1+2\sum_{r=1}^{T_T}(-1)^r[t\ge r].$$

The constants in the Fourier sum cancel when $c\ne\varnothing$, giving

$$K_c=2k^{|c|}\sum_{\varnothing\ne T\subseteq c}\sum_{r=1}^{T_T}(-1)^{|T|+r}E_{T,r}(a),\qquad E_{T,r}=[t_T\ge r].$$

Also $K_\varnothing=1$, which uses only a raw top table input and a constant. For every $c\supseteq T\ne\varnothing$ and $1\le r\le T_T$, instantiate the one-table-bit gate

$$g_{c,T,r}=[t_T+(T_T+1)x_c\ge r+T_T+1]=x_cE_{T,r}.$$

In the top score replace $(2x_c-1)E_{T,r}$ by $2g_{c,T,r}-E_{T,r}$. The address-only $E_{T,r}$ gates are shared. All thresholds act directly on raw inputs; no computed parity is supplied to another bottom gate.

The number of gated terms is

$$\sum_c\sum_{\varnothing\ne T\subseteq c}m|T|=mk3^{k-1},$$

since a distinguished block belongs to $T$ in $3^{k-1}$ pairs $(T,c)$ with $T\subseteq c$. The number of address-only terms is $\sum_Tm|T|=mk2^{k-1}$. This proves the bound. All weights and scores can be taken integer, and the signed score has margin at least one.

### 4.3 What transfers from the unrestricted quadratic circuit

If a full circuit's final score is affine in $x$, its coefficient $w_c$ can be recovered by evaluating that score at $x=e_c$ and $x=0$. Each original bottom then contributes the difference of two address halfspaces. Multiplying those terms by $(2x_c-1)$ yields a one-table-bit realization with $O(NS)$ bottoms. Thus affine-score quadratic constructions have a generic **cubic**, not quadratic, transfer. Applying this to the final affine score in `push_upper`, Section 1, is valid but inferior to the subset construction above. A gate-by-gate claim that the original ridges already read one table bit is false: $W_T$ and $w$ in that report contain many independent table inputs.

No same-size or constant-factor conversion of the $5n^2/16$ circuit is proved here. Its existence is also not refuted by the current lower bound.

### 4.4 Small block lengths are different: the inherited $m\le2$ upper bound

For completeness, the research state's Section 11 already gives a one-table-bit construction with $N$ bottoms at $m=2$ (attributed there to `exact_creative_astra`). Here is its direct proof. Write the two address columns as binary integers $U,V\in\{0,\ldots,N-1\}$, so $b=U\mathbin{\mathrm{xor}}V$. For each label $c$, use

$$g_c=[U-(V\mathbin{\mathrm{xor}}c)+x_c\ge1].$$

For a fixed $c$, $V\mathbin{\mathrm{xor}}c=\sum_i2^i(c_i+(1-2c_i)v_i)$ is affine in the raw second-column bits. Thus this is an actual allowed bottom gate, with mixed within-block signs in general. As $c$ varies, the comparison targets permute all integers $0,\ldots,N-1$. Exactly $U$ are smaller than $U$, and equality occurs for the selected label only. Therefore $\sum_cg_c=U+x_b$, and the raw affine top correction $-U$ extracts the output. Fixing the second column to zero also proves the $N$-gate bound for $m=1$.

This does not improve the growing-$m$, balanced exponent, but it refutes any literal assertion that *every* known ordinary-Andreev construction must read many table bits per gate. The bound in Section 4 is the balanced general upper bound established here, not the best formula for every parameter pair.

## 5. Localization, Fourier mass, and noise: exact conclusions and limits

### 5.1 Dominance is not per-column localization [REFUTED claim]

The subset construction has $K_\varnothing\equiv1$ even though its own parity fiber has measure $1/N$. More generally $K_c$ is supported on all labels containing $c$, a fraction $2^{-|c|}$ of the cube, not just its own fiber. Its own-fiber fraction of its $L_1$ mass is $2^{|c|-k}$. Thus dominance does **not** imply that each family is numerically larger on its own fiber, or has a constant fraction of its mass there. The independent review's two-label example $(K_0,K_1)=(1,0)$ on label zero and $(100,101)$ on label one makes the same point even more directly. A localization lemma must allow scaling across columns or use pairwise differences; the direct-sum theorem uses the latter.

### 5.2 What the halfspace Fourier-tail theorem actually implies

Let $P$ average a raw-address function over its parity fibers. Under the uniform raw-address measure, $P$ is the orthogonal projection onto the characters indexed by unions $U_T$ of whole address blocks. For $T\ne\varnothing$, $|U_T|\ge m$.

Yuval Peres' [*Noise Stability of Weighted Majority*](https://arxiv.org/abs/math/0412377) proves $\operatorname{NS}_\epsilon(h)=O(\sqrt\epsilon)$ for Boolean halfspaces. The Fourier identity for noise sensitivity, with $\epsilon=1/m$, consequently implies

$$\sum_{|U|\ge m}\widehat h(U)^2=O(m^{-1/2})\quad(m\ge2).$$

Indeed the noise factor $1-(1-2/m)^{|U|}$ is bounded below by an absolute positive constant there (handle $m=2$ directly). For a slab $q=h_1-h_0$, the squared tail is at most twice the sum of the two halfspace tails. Hence for $K_c=d_c+\sum_j\alpha_{cj}q_{cj}$,

$$\|PK_c-\mathbb EK_c\|_2\le O(m^{-1/4})\sum_j|\alpha_{cj}|.$$

This is a coefficient-norm estimate, **not** a gate-count estimate. No hypothesis bounds the sum on the right. Normalizing the minimum dominance margin to one merely allows coefficients to become larger. Nor can a small absolute Fourier tail for every feature be replaced by a small tail for their linear span: one rare-vertex halfspace $h=\mathbf1_{a=0}$ has $\|h\|_2=2^{-D/2}$, but multiplying it by $2^{D/2}$ gives a unit vector whose Fourier mass is spread uniformly over all degrees. For $D$ large, a constant fraction lies above degree $D/2$. A span argument needs a conditioning/leverage bound, or another correctness-dependent restriction on cancellation.

### 5.3 An elementary weight bound, explicitly not a gate lower bound [PROVED]

Suppose the pure dominance margin is at least $\delta>0$ everywhere, and use the original top coefficients $v_j$ in $K_c=u_c/2+\sum_{j:c_j=c}v_j(h_{j,1}-h_{j,0})/2$. Then

$$\sum_{j\text{ table-reading}}|v_j|\ge N\delta\sqrt m.$$

To prove this, first note that for a $\{0,1\}$ halfspace $h$ on $m$ bits,

$$|\widehat h([m])|\le\frac1{2\sqrt m}.$$

Complement coordinates to make $h$ monotone. Its total influence satisfies $I(h)=2\sum_i\widehat h(\{i\})\le2\sqrt{m\operatorname{Var}h}\le\sqrt m$, with character orientation chosen toward increasing bits. Taking the full-parity coefficient through any coordinate difference gives $|\widehat h([m])|\le I_i(h)/2$. Sum over coordinates. For each pair in Theorem 3.1, the parity correlation of $K_c-K_d$ has magnitude at least $\delta$. Each slab has full-parity coefficient of magnitude at most $1/\sqrt m$. Thus $\sum_{j:c_j\in\{c,d\}}|v_j|\ge2\delta\sqrt m$; sum the disjoint pairs. Unbounded $v_j$ prevent converting this to a count. This proof is included to expose precisely where a tempting Fourier argument stops.

### 5.4 Noise sensitivity reproduces only the square-root direct sum

On the $m$-cube for a label pair, a noise step flipping each bit with probability $\epsilon$ changes parity with probability $[1-(1-2\epsilon)^m]/2$. Whenever parity changes, at least one of its at most $2(s_c+s_d)$ halfspace features changes. Peres' bound and a union bound therefore give $s_c+s_d=\Omega(\sqrt m)$ at $\epsilon=1/m$. Summing pairs gives $\Omega(N\sqrt m)$, or exponent $3/2$ at balance. This argument is safe for unbounded top weights because it charges changes of the feature vector, not the size of a weighted score change. The stronger slicing theorem in Section 3 is exactly what improves the exponent beyond this noise/sensitivity calculation.

## 6. Rank and LP duality

### 6.1 Rank is necessary, but does not provide the missing exponent [PROVED]

Choose one address $a_b$ of each parity label, and form $M_{bc}=K_c(a_b)$. It is strictly row-diagonally dominant with positive diagonal. It is nonsingular: if $Mv=0$, choose $b$ with $|v_b|$ maximal; the diagonal term strictly exceeds the sum of magnitudes of all other terms in row $b$, a contradiction. The same conclusion holds for the fiber-averaged matrix, because $\mathbb E K_b>\mathbb E\sum_{c\ne b}|K_c|\ge\sum_{c\ne b}|\mathbb EK_c|$.

For a shared feature dictionary $K_c=d_c+\sum_{j=1}^H\beta_{cj}E_j$, rank is at most $H+1$, so $H\ge N-1$. For the original one-table-bit circuit, two gate-free columns would both be constant vectors and violate full rank, so at most one table family is gate-free. Neither statement controls $\operatorname{nnz}(\beta)$ beyond exponent one. Sign rank of the small equality sign matrix alone is not the right condition: strict $\ell_1$ dominance is much stronger than positive diagonal and negative off-diagonal signs.

### 6.2 Exact finite feasibility and its dual [PROVED]

Fix any finite slab dictionary $q_{cj}(a)$, with variables $d_c,\alpha_{cj}$. A strict dominating family exists if and only if the following finite system is feasible, after rescaling its minimum margin to one:

$$K_{b(a)}(a)+\sum_{c\ne b(a)}\sigma_cK_c(a)\ge1
\quad\text{for every }a\text{ and every }\sigma\in\{\pm1\}^{N-1}.$$

Write $z_b=1,z_c=\sigma_c$ otherwise, and let $A$ be the matrix whose corresponding row has entries $z_c$ for $d_c$ and $z_cq_{cj}(a)$ for $\alpha_{cj}$. Then the system is $A\theta\ge\mathbf1$. By the finite-dimensional alternative theorem, it is infeasible exactly when there is $y\ge0$ with $\mathbf1^Ty=1$ and $A^Ty=0$. Equivalently a dual distribution on $(a,z)$ satisfies

$$\mathbb E z_c=0,\qquad \mathbb E[z_cq_{cj}(a)]=0\quad\text{for all dictionary terms}.$$

Necessity of the obstruction follows immediately by multiplying all primal inequalities by $y$. Sufficiency is Farkas' lemma (or separation of the finite cone). This incorporates arbitrary real top coefficients correctly: approximate small correlations give only a bounded-norm/margin statement, whereas an unbounded-weight infeasibility certificate needs exact annihilation. One cannot refute all possible small circuits with an LP over an arbitrarily chosen restricted direction pool without proving that the pool is universal.

Slicing every edge is necessary but not sufficient for a parity top gate: the coordinate thresholds $[z_i=1]$ slice every edge of an $m$-cube, yet no affine combination sign-computes parity for $m\ge2$. The uniform parity-signed distribution annihilates their constant and coordinate features. This is a small exact dual obstruction to interpreting geometric coverage as an upper construction.

## 7. Exact computations [COMPUTATION, all passed]

`verify.py` is a Python-standard-library-only checker, independent of the source reports' scripts. It uses integer arithmetic throughout. Results are in `verification.json`, with authorship metadata.

1. It enumerates 4,875 choices of three integer table coefficients, intercept, and selected coordinate. Direct enumeration of all eight tables agrees exactly with both the bit-coordinate intercept interval and the signed-coordinate dominance/intercept condition, including equality cases.
2. It builds the actual raw-input gates from Section 4 for 24 instances: $k=1,m=1,\ldots,8$; $k=2,m=1,\ldots,5$; $k=3,m=1,\ldots,4$; $k=4,m=1,\ldots,4$; and $k=5,m=1,\ldots,3$. It checks all raw addresses when $km\le12$, and every block-count orbit for the larger block-symmetric instances. For every tested address/orbit, it extracts the actual affine table score from the gates, matches every coefficient and intercept to the closed form, and computes exact extremal scores over **all independent tables**. Every instance has minimum signed margin one. This is stronger than checking a sample of tables.
3. It checks the strengthened pair-extraction restriction for every distinct label pair at $(k,m)=(2,3),(3,3),(4,2)$: 6, 28, and 120 pairs, respectively. On all their embedded $m$-cube edges (72, 336, and 480 edges in total per instance), the coefficient difference has opposite strict signs and at least one of the halfspace features belonging to those two families changes.
4. It verifies the exact uniform parity dual against the constant and coordinate-feature dictionary for dimensions $2,\ldots,8$.
5. It checks the inherited two-column comparison construction for $k=1,\ldots,6$ on all $N^2$ address pairs in each instance, symbolically over all tables. The resulting score is exactly $x_b$.

Run `python3 /tmp/andreev_gap/one_table_bit/verify.py` to reproduce. These finite checks validate formulas and guardrails; the asymptotic geometric theorem is cited, not inferred from computations. No process remains running from these checks.

## 8. Continuing past the referee baseline: the upper gap

### 8.1 Two rigorous obstructions to sparse parity-label designs [PROVED]

Suppose the kernels depend only on the parity label, and write $M_{bc}=K_c(b)$. Then **at least one column has every one of its $N$ Walsh coefficients nonzero**. If each column $c$ had a missing coefficient $T_c$, the identity

$$0=\sum_b\chi_{T_c}(b)M_{bc}$$

would imply $M_{cc}\le\sum_{b\ne c}|M_{bc}|$. Summing over columns contradicts the strict row-diagonal dominance of $M$. This is a gate-independent statement about any parity-label-only dominating kernel family; it does not assume coefficient bounds or nonnegative off-diagonal entries. In particular a design with $o(N)$ Fourier channels in **every** column cannot work. The subset construction attains a much smaller *total* than $N^2$ by allowing highly unequal column complexities, including one full column.

The same conclusion applies to the fiber-averaged matrix of an arbitrary raw-address family. Thus some kernel has all $N$ block-parity Fourier coefficients nonzero even without parity-label-only dependence. This is a support statement, not a quantitative mass bound; these coefficients may be arbitrarily small relative to the gate coefficients.

For the more restrictive translation-equivariant design $K_c(b)=q(b\oplus c)$, dominance is $q(0)>\sum_{d\ne0}|q(d)|$. Consequently every Walsh coefficient of $q$ is strictly positive, since

$$N\widehat q(T)=q(0)+\sum_{d\ne0}\chi_T(d)q(d)>0.$$

Thus **all $N$ columns require all $N$ Fourier channels**. Translating and averaging an asymmetric circuit is not a cost-free symmetry reduction. With the independent full parity ladders used in Section 4, one dense column already costs order $m\sum_T|T|=kmN/2$; all dense columns restore the cubic balanced count. These statements concern the independent-character implementation only. A raw-address halfspace can contribute to many Fourier coefficients at once, so Fourier support is not itself a lower bound on arbitrary one-table-bit gates.

### 8.2 Why a fixed small kernel certificate cannot simply be tensored

For a nonnegative local kernel matrix, put $\alpha_b=M_{bb}/\sum_c M_{bc}$. A tensor product of $q$ such matrices has selected-coordinate fraction $\prod_{i=1}^q\alpha_{b_i}$. Local dominance only gives $\alpha_b>1/2$; the product can fall below $1/2$ as $q$ grows. The same calculation uses absolute row sums for signed matrices. A scalable tensor construction must make leakage $O(1/q)$ per factor with the **same support pattern**, or supply a different global combination. The subset construction does this by increasing $\lambda$ with $k$. A one-off LP certificate with fixed slack does not establish a new asymptotic exponent.

### 8.3 Bounded support search [COMPUTATION / inconclusive]

`fourier_probe.py` explores parity-label-only kernels $K_c(b)=\sum_T\beta_{cT}\chi_T(b)$, with the strong linearized condition $0.3M_{bb}-\sum_{c\ne b}|M_{bc}|\ge1$. It greedily attempts to delete coefficients, resolving a feasibility LP after each deletion. Coefficients are unbounded; each solve has a one-second time limit. This is a heuristic over Fourier supports, not a search over arbitrary halfspace directions and not an exact optimizer.

Eight seeded $k=3$ runs retained 27, 27, 28, 27, 27, 27, 27, 27 coefficients; three $k=4$ runs retained 87, 83, 81. The analytic subset baseline is $3^k$, namely 27 and 81. No smaller support was found. All completed LP calls reported feasible or infeasible; residuals on feasible solutions were within approximately $3\times10^{-7}$ of the unit constraint. These floating-point results are **not** infeasibility certificates and do not prove that $3^k$ is optimal. No new upper theorem is based on them. The exact integer construction in Section 4 is separately verified.

Results and the tested support patterns are saved in `fourier_probe.json`, with authorship metadata. Reproduce with `python3 -I /tmp/andreev_gap/one_table_bit/fourier_probe.py`; it uses the already available NumPy/SciPy installation under `coherence_fable/pydeps_local`. The process finished normally. The upper gap therefore remains after both the asymmetric analytic construction and this bounded search. Repeated searches merely optimizing finite constants were not pursued.

## 9. Final status and remaining questions

The rigorous balanced bounds established here for the requested arbitrary-real one-table-bit model are

$$\Omega\!\left(n^{32/19}/\log^{45/19}n\right)
\ \le\ S_{\mathcal T_1}(A)\ \le\ O\!\left(n^{1+\log_2 3}\right).$$

The lower target beyond $3/2$ is already covered by the completed referee report's Section 8 and the independently reproduced reduction here. Even Klein's older slicing bound gives exponent $5/3$. The progress beyond that updated baseline is the explicit asymmetric upper construction, the stronger bounded-normal and coefficient-tradeoff consequences, and the localization/Fourier/tensor obstructions. These additional results are hand proofs with exact finite checks where applicable, pending independent review. The current construction is valid in the restricted model without assuming that a many-table-bit gate transfers at constant cost. It does not settle the optimal exponent. For bounded integer address normals, the stronger lower bound is $\Omega(n^2/\log n)$.

**OPEN:** whether $O(n^{2+o(1)})$ one-table-bit constructions exist; whether the arbitrary-real lower exponent can reach two; whether a correct family of localized/dominating slabs permits a substantially stronger geometric bound than generic edge slicing; and whether any multi-table-bit generalization avoids the fan-in loss in the exact limited-read extension. Proving the conjectured $\operatorname{Slice}(m)=\Omega(m)$ would yield $\Omega(n^2/\log n)$ here, but it is not assumed. Fourier tail and noise estimates alone stop at norms or square-root slicing; neither justifies a stronger gate bound with unbounded real top weights.

The per-cube entropy construction from `coherence_fable` remains a barrier to its specified additive accounting method, not to this pairwise collective argument. Correctness does not require each individual coefficient to concentrate on its own parity fiber. Both qualifications are essential to an accurate research state.

All newly authored artifacts in this directory credit Christian Reitwiessner. Mathematical attribution to Klein, Sauermann–Xu, Peres, and the supplied local reports is retained. No shared paper was edited, no subagents were started, and nothing was posted online.
