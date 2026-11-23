# UP1: exact unrestricted upper-bound research

Authors: Christian Reitwiessner

Restart date: 2026-11-11. Requested model: OpenAI Astra. No subagents.

## Outcome

**No exact $n^{2-\varepsilon}$ circuit for unrestricted Andreev was obtained.** The supplied unrestricted exponent gap is unchanged.

[PROVED positive building block] Tables with at most $h$ ones admit an exact promise circuit of size $O((km+h)\min\{2^k,h^2k\})$. An exact integer-level guard compiler keeps depth two and repairs all such tables in the supplied average-case circuit at balanced cost $\widetilde O(N^{3/2}h+Nh^3)$. For $h=N^\beta$, $\beta<1/3$, the hybrid remains subquadratic but is **not exact on all other inputs**. Full construction and finite gate bounds are in Section 5.

[PROVED obstruction] Complementary character tables give a four-input exact dual refuting **every** top-weight refit of the central-window Fourier bottom pool, not merely its prescribed score (Section 3.1). The mask-cover attempt also costs quadratic size in the per-character covering architecture. The strongest cover bound follows immediately from a known skew-cover theorem, while Section 2 gives an additional self-contained common-outlier lemma; neither is an unrestricted Andreev lower bound.

All work stayed in this folder apart from append-only board exchanges. No subagents, repository changes, or online posts were made. New files credit Christian Reitwiessner.

## Scope and correction

[KNOWN, COMMON.md and corrected review_coherence] The target is an exact depth-two threshold circuit for Andreev lookup with $N=2^k$ table bits and $k$ blocks of $m$ address bits, beating exponent $2$ when $km=N$. Gates and top affine input terms have arbitrary real weights. The best supplied unrestricted bounds are $\widetilde\Omega(n^{3/2})$ and $O(n^2)$.

The near-zero-sum conclusion is conditional on globally comparable eligible blocks, and may be vacuous. It is **not** a necessary zero-sum normal form for unrestricted circuits. Sign-coherence itself remains a genuine restricted-model obstruction (paper Section 6, Theorem 12).

## Initial research agenda

[CONJECTURE / CANDIDATE, not a construction] Explore parity-preserving signed address masks combined with table translations or masks: a uniform collection of transforms might make a truncated Fourier score pointwise reliable. The exact question is whether transformations can simultaneously keep every input inside enough windows and preserve a usable top-score margin, without multiplying the $n^{3/2}$ cost by $n^{1/2}$ or more. First tasks: derive the exact transformed score and its failure/margin bound; test pairwise-independent sign families and discrepancy-based designs; check all claims against the corrected coherence theorem and known dead ends.

No exponent improvement is established at initialization. This report will be updated after each major idea.

## 1. Literal mask-score candidate and first obstruction

[CANDIDATE, not established] For each nonempty $S$ and replica $r$, let $M_S=|S|m$, $D_{r,S}=|a_S\oplus z_{r,S}|-\lfloor M_S/2\rfloor$ and $\eta_{r,S}=(-1)^{|z_{r,S}|+\lfloor M_S/2\rfloor}$. Let $f_W(u)=(-1)^u u\mathbf1_{|u|\le W}$. The literal averaged score is

$$P=2RX_\varnothing+\sum_{r=1}^R\sum_{S\ne\varnothing}\eta_{r,S}\bigl(f_W(X_S+D_{r,S})+f_W(X_S-D_{r,S})\bigr).$$

Every summand is a staircase of an affine raw-input form, hence costs at most $4R(N-1)(W+1)$ bottom gates overall, plus the top. It uses dense table normals and mixed address signs and therefore is not excluded merely by coherent or one-table-bit lower bounds. Its untruncated version is $2RN(-1)^{x_b}$.

[KNOWN, paper Section 4] Independent masks yield a uniform-average input guarantee. That guarantee does not become worst-case by simply fixing several mask choices. The top gate can aggregate these real scores but cannot take a majority of their signs without an additional layer.

[KNOWN, RESEARCH_STATE Section 13 and asymptotic_creative_astra_pass2/report.md] Separable hard clipping at $o(N)$, fixed sublinear power shrinkers and fixed logarithmic shrinkers already have explicit scalable counterexamples, even with affine top repairs. These are not new research results here. Arbitrary table-sign masks need an address-dependent output correction; Walsh-character masks only permute the coefficient spectrum.

[CANDIDATE] An elementary central-window covering obstruction is posted on the board: $R$ sign masks on $M$ coordinates admit a common vertex whose absolute correlations are at least $M/R-R$. Full proof and checks follow below. This would rule out a direct $R=o(\sqrt M)$ mask-cover upgrade at central-limit-scale window width, without claiming any unrestricted circuit lower bound.

## 2. Mask covering has a quadratic replication barrier

### 2.1 A simultaneous large-correlation vertex

[PROVED] Let $p_1,\ldots,p_R\in\{\pm1\}^M$, $R\ge1$. There exists $z\in\{\pm1\}^M$ such that

$$|\langle p_r,z\rangle|\ge M/R-R\qquad(1\le r\le R).$$

**Proof.** Choose $\epsilon\in\{\pm1\}^R$ maximizing $\|v\|_2^2$ for $v=\sum_r\epsilon_rp_r$. Flipping the $r$th sign gives

$$0\le\|v\|_2^2-\|v-2\epsilon_rp_r\|_2^2
=4\epsilon_r\langle p_r,v\rangle-4M.$$

Thus $\epsilon_r\langle p_r,v\rangle\ge M$ for every $r$. The point $u=v/R$ lies in $[-1,1]^M$ and has these oriented projections at least $M/R$.

Write $P$ for the matrix with rows $p_r$. Choose an extreme point $u'$ of the nonempty compact polytope

$$\{w\in[-1,1]^M:Pw=Pu\}.$$

At most $\operatorname{rank}P\le R$ coordinates of $u'$ are strictly between $-1$ and $1$: otherwise a nonzero nullvector supported on its fractional coordinates would allow a small feasible move in both directions, contradicting extremality. Round each fractional coordinate to its nearest sign (break zero arbitrarily). Each changes by at most one; hence every row projection changes by at most $R$. Consequently

$$\epsilon_r\langle p_r,z\rangle\ge M/R-R,$$

which proves the assertion. When the right side is nonpositive the statement is trivial but still valid. No probabilistic or comparability assumption is used. This is a self-contained max-norm signing and cube-rounding argument, not a claimed new general discrepancy theorem.

### 2.2 Heterogeneous windows

[PROVED] If central slabs $|\langle p_r,z\rangle|\le T_r$, with $T_r\ge0$, cover every Boolean sign vector, then

$$\boxed{\sum_{r=1}^R T_r+R^2\ge M.}$$

**Proof.** Suppose $L=\sum_r(T_r+R)<M$ and set $c_r=T_r+R>0$. Maximize $\|\sum_r c_r\epsilon_rp_r\|_2^2$. The same flip calculation gives $\epsilon_r\langle p_r,v\rangle\ge c_rM$. Now $u=v/L$ belongs to the cube and its $r$th oriented projection is at least $(M/L)(T_r+R)>T_r+R$. Preserve all projections while moving to an extreme point and round at most $R$ fractional coordinates as above. The resulting vertex satisfies $|\langle p_r,z\rangle|>T_r$ for every $r$, contradicting coverage.

[PROVED] For masked centered counts $D_r=|a\oplus z_r|-\lfloor M/2\rfloor$, covering every $a$ by a window $|D_r|\le W_r$ requires

$$\sum_r(2W_r+1)+R^2\ge M.$$

Indeed, with sign vectors $p_r=(-1)^{z_r}$ and $z=(-1)^a$, $D_r=((M\bmod2)-\langle p_r,z\rangle)/2$. Thus being in the count window implies being in the central slab of radius $2W_r+1$. For even $M$ the $+1$ can be omitted.

### 2.3 Consequence and exact scope

[PROVED] Suppose each replica uses a central-limit-scale or wider window, $W_r\ge c\sqrt M$ for a fixed $c>0$. Every covering family has total width $\sum_rW_r=\Omega_c(M)$. To see this, if $R\ge\sqrt M/2$, the width lower bound alone gives $\sum_r W_r\ge cM/2$. Otherwise $R^2<M/4$, and the preceding inequality forces $2\sum_rW_r\ge3M/4-R=\Omega(M)$.

For independently implemented character channels, take $M_S=|S|m$ and apply this to every nonempty $S$. A design requiring at least one valid window per character and every raw address, and charging $\Theta(W_{r,S}+1)$ gates per replica, must pay

$$\Omega\!\left(\sum_S M_S\right)=\Omega(km2^k).$$

At balance $km=\Theta(N)$ this is exponent $2$. In the common uniform-width regime $W=\widetilde\Theta(\sqrt{km})$, any polynomial reduction below quadratic in the *replication budget* is therefore impossible. This remains true if only the $\Omega(N)$ characters with $|S|\ge k/3$ are considered.

**Limits.** This is a geometric covering/architecture obstruction, **not** a lower bound for arbitrary depth-two circuits, arbitrary score aggregates, or all mask strategies. It does not exclude compensating errors across characters, variable-width designs with many very narrow windows, nonlinear coupled table codes, or shared gates implementing something other than these dedicated channels. It also does not claim coverage suffices for correctness. The literal score in Section 1 fails for a separate stronger table-tail reason even when coverage is perfect.

### 2.4 A known theorem gives the stronger all-width conclusion

[KNOWN THEOREM; PROVED immediate application] Sauermann–Xu, *Nondegenerate hyperplane covers of the hypercube*, Theorem 1.1, says that a nondegenerate cover has at least $M/2$ hyperplanes. A cover whose every normal has all coordinates nonzero is a special case. I inspected the [primary theorem statement](https://arxiv.org/html/2507.00773v2) during this run; the source also attributes the earlier skew-cover result to previous work.

Every masked count window $|D_r|\le W_r$ is a union of at most $2\lfloor W_r\rfloor+1$ integer-level hyperplanes, each with nonzero $\pm1$ normal on all $M$ active coordinates. A family of such windows covering all raw inputs therefore yields a skew hyperplane cover and must satisfy

$$\boxed{\sum_r(2\lfloor W_r\rfloor+1)\ge M/2.}$$

Thus $\sum_r(W_r+1)=\Omega(M)$ for **arbitrary** nonnegative widths, including many width-zero or very narrow windows. Applied separately to character channels, the covering approach has cost $\Omega(km2^k)$ at all widths. This supersedes the narrower asymptotic covering consequence of Section 2.3. It is an elementary consequence of an inherited literature theorem, **not a newly discovered lower-bound exponent**. Section 2.1 still supplies an explicit simultaneous large-correlation vertex and a self-contained proof, but it is not the strongest known mask-cover size obstruction.

## 3. Literal score refutation, including free affine repairs

[PROVED, independently confirmed by LOW2 on the board] Fix a nonempty character $T$, and use the table signs $\xi_c=\chi_T(c)$ or their complements. Then $X_T=\pm N$, all other Walsh coefficients vanish, and $X_\varnothing=0$. If

$$W<N-\lceil |T|m/2\rceil,$$

then $f_W(\pm N+D)+f_W(\pm N-D)=0$ for every mask and address. For the other characters, oddness of $f_W$ gives $f_W(D)+f_W(-D)=0$. Hence the entire candidate score vanishes on both complementary character tables at all raw addresses, for **any** number or choice of masks and even arbitrary fixed aggregation coefficients. Taking $T=\{i\}$ already forces $W\ge N-\lceil m/2\rceil$ if this literal family is to have any chance of exactness.

[PROVED] Adding arbitrary affine raw-input terms cannot repair this zero-score pair. The difference between the two resulting top scores is a constant depending only on their table bits; raw address terms and the threshold cancel. At an address where $\chi_T(b)=1$, exactness forces this difference to have one strict sign; where $\chi_T(b)=-1$, it forces the opposite strict sign. Both raw addresses exist for every $m\ge1$, a contradiction. This argument also permits arbitrary shared pure-address gates in the repair.

[REFUTED] Thus address masking alone cannot upgrade the literal truncated score to an exact subquadratic circuit. This does not depend on any disputed zero-sum normal-form claim and does not presume bounded top weights.

### 3.1 Strengthening: the whole truncated bottom library is infeasible

[PROVED] The preceding table-tail obstruction survives **arbitrary individual top weights on every bottom gate**, not merely different weights on the $f_W$ summands. Consider the actual bottom library

$$g_{r,S,\pm,\theta}=[X_S\pm D_{r,S}\ge\theta],\qquad -W\le\theta\le W+1.$$

On complementary character tables $\xi=\pm\chi_T$ satisfying $W<N-\lceil |T|m/2\rceil$, the $T$-channel forms on the positive table are integers at least $W+1$, and those on the negative table are integers at most $-W-1$. Thus every $T$-channel bottom is identically one on the first table and zero on the second. Every other channel has the same table statistic zero on both tables, so its gate values agree at every fixed address. Each bottom's table-pair difference is therefore constant in the address. Arbitrary pure-address gates and all direct address terms cancel; direct table terms contribute another constant. The top-score difference cannot change sign, whereas the selected character bit does.

Equivalently, choose two raw addresses with opposite $T$-parities and put equal weight on the four combinations of these addresses and the complementary character tables. The alternating target signs annihilate every bottom feature and every free affine feature. This is an exact finite-support dual certificate for **all top-weight refits of this entire central-window pool**. The obstruction does not apply after adding new table directions or appropriate tail-level gates. It is stronger than a failure of the prescribed numerical staircase reconstruction.

## 4. Responses to the lower-bound agents

[PROVED, response to LOW1] For integer $L,q,r$,

$$[q+1+L\ge r]-[q+L\ge r]=[L=r-q-1].$$

This confirms LOW1's all-background two-table-swap ladder identity. Its $k(N/2+m)$-gate library can separately represent every required parity difference with pair/background-dependent top weights. Such separate feasibility cannot establish a common top threshold.

[PROVED, explicit collision witness] For $k\ge2$, take tables supported on labels $\{00,11\}$ and $\{01,10\}$, with all other label coordinates zero. They have equal $Q_i=\sum_{c:c_i=1}x_c$ for every $i$. Therefore every gate in LOW1's library, and every extra pure-address gate, agrees between the two tables at each fixed address. The top-score difference can only be a constant direct-table term. The desired tables are incomparable: one is larger at label $00$, the other at $01$. Exactness would force both signs for that constant, impossible. This is a common-top obstruction, not an additional gate lower bound.

[PROVED, stress family sent to LOW1] Dense table normals $\alpha_c=\chi_S(c)$ produce only two responses on singleton tables, so one slab can serve many table pairs. Replacing $\alpha_c$ by $\chi_S(c)+\epsilon2^{-\operatorname{index}(c)}$ makes all coefficients distinct while preserving any fixed gate truth table on the finite cube if the threshold is first strictified and $\epsilon$ is sufficiently small. Thus arguments based on exact equality of table coefficients are not robust. The threshold strictification is essential if an original gate has input ties. This is an explicit example family; it is not a computing circuit.

## 5. A positive exact building block for genuinely sparse table tails

### 5.1 Sparse-table lookup

[PROVED; promise result, not ordinary Andreev] For every integer $1\le h\le N$, the restriction of $A_{k,m}$ to tables with at most $h$ ones has an exact depth-two circuit with

$$S\le q(4h+2km),\qquad q\le\min\{N,\lceil18h^2\ln(4N)\rceil\}.$$

One top gate is additional. No claim of priority is made for the elementary sampling idea; the role here is a quantitatively explicit correction gadget.

**Character set and existence.** Choose a multiset $Q$ of $q$ Walsh characters such that

$$\left|\sum_{S\in Q}\chi_S(d)\right|\le q/(3h)\qquad\text{for every }d\ne0.$$

If $q=N$, take every character once and the left side is zero. Otherwise take $q=\lceil18h^2\ln(4N)\rceil$ independent uniform characters. For each fixed nonzero $d$, their evaluations are independent unbiased signs. The elementary exponential-moment bound gives failure probability at most $2\exp(-q/(18h^2))$. A union bound over $N-1$ differences is less than $1/2$, proving existence. A circuit fixes this multiset once; it does not choose characters per input.

Put $L_S(x)=\sum_c\chi_S(c)x_c$, and define

$$F(x,a)=\sum_{S\in Q}\chi_S(b)L_S(x)
=\sum_{c:x_c=1}\sum_{S\in Q}\chi_S(b+c).$$

If $x_b=0$ and $|x|\le h$, then $F\le q/3$. If $x_b=1$, then $F\ge q-(h-1)q/(3h)\ge2q/3$. Thus the threshold $F\ge q/2$ computes $x_b$ exactly on the promise, with strict margin at least $q/6$ in the real score.

**Raw gates.** On the promise, $L_S\in[-h,h]$. Put $t_S=\sum_{i\in S,j}a_{ij}\in[0,|S|m]$ and $\varphi(u)=(-1)^u u$. Then

$$\varphi(2L_S+t_S)-\varphi(t_S)=2L_S\chi_S(b).$$

The first staircase on $[-2h,2h+|S|m]$ uses $4h+|S|m$ gates, and the second on $[0,|S|m]$ uses $|S|m$ gates. Its forms are affine in the original raw inputs, so depth remains two. Test the resulting doubled score against $q$. If $S=\varnothing$, its affine contribution can instead be read freely at the top. Repeated characters can be merged, so the displayed count is an upper bound, not an optimal size claim.

At balance this is $\widetilde O(Nh^2)$ for $h<\sqrt N$, hence exponent $1+2\beta$ on the promise $h=N^\beta$. These gates are coherent; there is no contradiction with Theorem 12 because correctness is required only on sparse tables here. The polynomial-exponent conclusion is a **promise** upper bound and is not the task's unrestricted upper-bound objective.

### 5.2 Exact guarded composition at depth two

[PROVED] Let $U$ be an integer-valued affine raw-input form, $I$ a finite set of $q_I$ integers, and $g=[L\ge\theta]$ a raw threshold gate. Choose $B>\max|L-\theta|$ on the finite input cube. For every input,

$$\boxed{[U=r]g=[B(U-r)+L-\theta\ge0]-[U\ge r+1].}$$

If $U\le r-1$, both terms are zero; if $U\ge r+1$, both are one; if $U=r$, the first equals $g$ and the second is zero. The strict choice of $B$ handles the off-level cases, while the original weak inequality at $L=\theta$ is preserved exactly. In particular, no multiplication of computed gate outputs is used.

For a real depth-two score

$$H=c+\sum_{j=1}^S v_jg_j+\sum_{\ell=1}^d u_\ell z_\ell,$$

apply this identity to every gate and to each raw bit regarded as $[z_\ell\ge1]$, and use $[U=r]=[U\ge r]-[U\ge r+1]$ for the constant. Summing over $r\in I$ represents $[U\in I]H$ exactly as a top linear combination of at most

$$q_I(S+d+2)$$

raw threshold gates. The two pure-$U$ gates per level can be shared across every term. All new coefficients may be large, as permitted. This construction is stronger than merely detecting the exceptional set, and more expensive than a free detector: its cost is proportional to the number of admitted integer levels.

### 5.3 Repairing all sparse tables of an approximate circuit

[PROVED hybrid guarantee, not exact ordinary Andreev] Let $H_0$ be any original depth-two real score, oriented so output one means score nonnegative, and let $H_1$ be the sparse-table score above with its threshold subtracted. Define

$$H=H_0+[|x|\le h](H_1-H_0).$$

The guard has $h+1$ levels because $|x|$ is a nonnegative integer. The identity in Section 5.2 implements this at depth two. On every sparse table the score is exactly $H_1$; on every other table it is exactly $H_0$. Thus correctness on sparse tables is exact, and **no previously correct input outside the repair set is changed**. Existing correctness inside the set is also preserved because the replacement is exact there.

If $H_0$ is the supplied fixed-error $S_0=O(n^{3/2})$ construction and $S_1=O((km+h)\min\{N,h^2k\})$, a safe finite gate bound is

$$S_0+(h+1)(S_0+S_1+n+2).$$

At balance and $h=N^\beta$, $0\le\beta<1/3$, this is

$$\widetilde O(N^{3/2+\beta}+N^{1+3\beta}),$$

whose exponent is strictly below two. This is a deterministic circuit correct on **all** such sparse tables and at least as accurate as $H_0$ on all other inputs. The same construction on $N-|x|$ repairs co-sparse tables too at another constant factor. Fixed known character tables can likewise be used as centers by replacing $|x|$ with affine Hamming distance to that table, but repairing all $N$ character centers independently incurs a prohibitive factor $N$.

The bottom gates of the hybrid inherit mixed signs from $H_0$ and can acquire other weight scales through guarding. They are therefore not being claimed to evade the coherent theorem while remaining coherent. The construction also respects the corrected eligibility qualification: no general zero-sum conclusion is assumed.

### 5.4 Why this does not finish detect-and-correct

[PROVED asymptotic counting observation] For $W=N^{1/2+\delta}$ with fixed $0<\delta<1/2$, the layer of tables at Hamming distance $N/2-\Theta(W)$ from a fixed character has logarithmic cardinality

$$N-\Theta(W^2/N)-O(\log N)=N-\Theta(N^{2\delta})-O(\log N).$$

This follows by the binary-entropy expansion of the binomial coefficient (round the distance to an integer). Thus ordinary concentration-window failures still contain $2^{N-o(N)}$ tables. They are rare under the uniform distribution but not sparse perturbations with $h=o(\sqrt N)$. Enumeration or the sparse-table gadget cannot cover them economically. A guard for their entire range also contains $\Theta(N)$ integer levels, so the lemma above gives a factor-$N$ cost rather than a free decision-list handoff.

[CONJECTURE / unresolved direction] A successful extension must share the corrections across many table directions or find a substantially cheaper guarded score whose correctness is conditional on a wide tail interval. Neither a small detector nor low uniform probability supplies that composition for free.

## 6. Verification and reproducibility

[VERIFIED] Both standalone scripts use the Python standard library and exact integer or rational arithmetic. Run:

```bash
python3 -I /tmp/andreev_gap/swarm/up1/checks.py
python3 -I /tmp/andreev_gap/swarm/up1/checks_positive.py
```

`checks.json` records 6,294 exhaustively enumerated small mask families, 20 constructive exact-rational rounding cases through $M=256$, 35,824 character-tail summands, 18,512 bottom-feature four-point dual equalities for the entire window pool, 287 staircase identities, and four collision-table checks. All passed. The first version of the tail-check harness accidentally included an equality case outside the theorem's strict window hypothesis; it failed as it should. The corrected harness tests only the explicitly stated hypothesis and additionally tests the stronger singleton-character window range. No mathematical claim was weakened to fit a failing in-hypothesis example.

`checks_positive.json` records 1,655 exhaustive sparse-table raw-gate cases, 20,460 exact guard identities (including ties and off-level inputs), and all 256 raw inputs of a compiled $A_{2,2}$ hybrid. The hybrid check verifies exact replacement on the sparse region and exact preservation of the original score off that region, even though the original test score is deliberately arbitrary and incorrect. All passed. It also records exact bias certificates for sampled character multisets at $(k,h,q)=(8,1,125),(10,2,599),(12,3,1573)$; their maximum nonzero-difference character sums were $35,81,161$, respectively, each meeting $3h\max|K|\le q$. These finite checks supplement the all-size proofs rather than infer exponents from small sizes.

## 7. Board exchanges and lessons from peers

[PROVED CHECKS / attributed results] LOW1 and LOW2 independently checked the max-norm rounding argument. LOW2 independently refuted the literal masked score on character tables. I strengthened that attack to arbitrary top weights on the full central-window bottom pool and to free affine repairs. LOW1 and UP2 independently checked the exact level-guard identity; LOW1 also derived it while responding to the sparse-table candidate. UP2 observed that, for the specific guard $|x|\le h$, a raw input bit $z$ can be gated with the single threshold $[Bz-|x|\ge B-h]$ when $B>N+h$. This removes an unnecessary $h$ factor on raw top terms, but does not change the displayed dominant hybrid exponent.

[PROVED CHECKS, LOW1 result] I checked LOW1's dense-table two-bit-swap library and supplied the same four-point collision witness independently. I also supplied the endpoint-ratio proof of its conditional hypergeometric bound $\Pr(B=0\mid S=t)\le2/3$, including the necessary exclusion of the one-total-address-bit degeneracy. LOW1's report Section 3 proves that $O(n^{3/2})$ random dense signed gates pass every ordinary table-pair/address-edge nonconstancy test simultaneously; its joint transcript is injective on every address cube. These are exact geometric/information properties, not a computing circuit. This prevents me from treating strong survival or transcript tests as evidence of an upper construction.

[PROVED CHECK, UP2 result] I read and checked UP2 report Section 5's exact dual for polynomially many well-separated full-support equal-magnitude sign directions. It allows **all** thresholds and arbitrary top weights and still cannot compute a parity on exactly half the raw coordinates. The radial middle-degree kernel interpolates the target at all centers and antipodes, stays strictly below one in magnitude elsewhere, and produces a nonnegative annihilating measure. I checked the Krawtchouk identity, the radial Fourier cancellation, the unique-near-center bound, and the treatment of threshold ties. This is a restricted-library obstruction on the even-$k$ Andreev subsequence, not an unrestricted circuit lower bound. It strengthens the earlier margin-only warnings about random dense pools: merely adding tail thresholds to independent full-support masks does not save that architecture.

[VERIFIED finite evidence, attributed to LOW2] LOW2's report Sections 5.1 and 7 records exact rational common-top infeasibility certificates for small dense libraries that pass individual rectangle tests, including a positive combination of 56 oriented rectangles. I read the certificate description and criterion, but did not independently rerun LOW2's scripts. These results reinforce the need to test one common top score, not independent per-pair fits. LOW2's separate table-monotone owner-slab theorem is a restricted extension of inherited one-table-bit slicing bounds; my signed table code does not satisfy its monotonicity assumption.

## 8. Final status and one next step

[REFUTED routes] Central-window Fourier masks fail even with unrestricted top-weight refitting. All-input mask covering cannot lower the per-character exponent, including by many narrow windows, by the known skew-cover consequence. Raw sparsity and rare uniform-measure tails are different: the latter still contain exponentially many central-weight tables. Guard compilation is real but currently pays once per integer level. Full-support independent equal-magnitude random directions are additionally excluded by UP2's exact dual; a high-entropy feature transcript is insufficient by LOW1's result.

[PROVED strongest positive result of UP1] The sparse-table exact promise circuit and the depth-preserving guard compiler yield the balanced hybrid size

$$\widetilde O(N^{3/2+\beta}+N^{1+3\beta}),\qquad h=N^\beta,\quad 0\le\beta<1/3.$$

The hybrid is correct on every table of weight at most $h$ (and, with a second repair, at least $N-h$), and preserves all original correctness elsewhere. It is **not** the requested exact ordinary-Andreev circuit. No unrestricted exponent change, no optimality, and no exhaustive novelty claim are asserted.

[CONJECTURE / single most promising next step] Seek a **shared tail-correction score** that couples multiple signed table statistics and uses deliberately structured address directions with unequal magnitudes or character-dependent supports. The concrete criterion is to replace the level-by-level guard's $hS$ cost by a joint representation of the needed correction on a wide tail interval, with one feasible top vector. Include complementary character-table rectangles as exact constraints from the start; they expose the missing information in a central-window library immediately. The guard compiler supplies a correct fallback for a thin collection of exceptional layers, while the known cover theorem and UP2's dual eliminate the naive random-mask alternatives. No construction meeting this criterion is currently known from this run.

### Final board addendum

[PROVED CHECK, attributed to UP2 and LOW1] UP2 subsequently extended its random-pool consequence to odd $k$ by fixing one entire block: the remaining even number of blocks still has independent uniform restricted sign directions and contains a target parity on exactly half its raw coordinates. This extension is sound and removes the even-$k$ qualification for the asymptotic **random-pool** obstruction; the deterministic separation theorem is applied on the remaining coordinates. LOW1 and UP2 also combined their high-probability events to obtain libraries of $\widetilde O(n^{3/2})$ gates that pass all the stated slicing/transcript tests yet provably admit no common top decoder. This is a stronger justification for requiring a common-top feasibility test in the next upper-bound attempt, not a circuit construction or unrestricted lower-bound improvement.
