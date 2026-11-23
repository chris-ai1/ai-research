# LOW2 round two: paired cancellation audit and signed-path duals

Authors: Christian Reitwiessner

Date: 2026-11-11. Status: completed round-two handoff; no unrestricted exponent improvement obtained.

## Outcome

[PROVED CHECK] UP2's paired-cancellation exponential theorem has no identified gap under its stated hypotheses (§1).

[PROVED] Mere near equality cannot preserve that exponential conclusion: an exact compiler gives $(M+1)$ overhead with arbitrarily close positive coefficients, and UP2's two-scale mechanism gives exponent two for every fixed positive tolerance (§3). Truth-table-equivalent perturbations remain covered.

[VERIFIED EXACT FINITE] A 49-row positive oriented-rectangle dependence refutes a 48-gate library with pairwise-distinct address magnitudes, all geometric pair tests passing, and no semantic full-sign representation (§4). No unrestricted asymptotic inference is made.

Peer results audited: LOW1's $\exp(\Omega(n/q))/n^2$ spectrum/support-overlap theorem and UP2's exponent-two bounded-Walsh/bounded-scale class (§5). The unrestricted $3/2$ versus $2$ gap remains open.

## Initial scope and queue

1. Independently audit UP2 round-one Section 6, including degeneracies, strictification, raw top inputs, and the claimed gate count.
2. Extend exact cancellation to coefficient spectra and support overlap; distinguish semantic stability from numerical closeness.
3. Investigate exact positive duals for mixed signed table paths, without top coefficient bounds.

[KNOWN, task brief] The unrestricted exact ordinary Andreev gap remains $\widetilde\Omega(n^{3/2})$ to $O(n^2)$. Every result below will retain its model hypotheses. New files are credited as requested; no shared-paper edits or external posts.

## 1. Independent audit of UP2 round-one Section 6

[PROVED CHECK; theorem attributed to UP2] The exponential theorem is correct as stated. Fix one block if $k$ is odd, put $d=m\lfloor k/2\rfloor\ge2$, and fix the table to the character on half the remaining blocks. In raw signs the target is $f(z,w)=\prod_{i=1}^dz_i$. For each $t\in\{\pm1\}^d$, substitute $w_i=t_iz_i$. A full same-magnitude gate has restricted coefficients $G(\sigma_i+t_i\tau_i)$ and hence can have all of them nonzero for exactly one $t$. Every other restriction omits a variable, so its full parity Fourier coefficient is zero. Constants, pure-table gates, and affine raw top inputs have zero full-parity coefficient because $d\ge2$.

For a correct top score with positive labels using a weak threshold and negatives using a strict threshold, the maximum negative score is strictly less than zero, while the minimum positive score is nonnegative. Shift the intercept by a strictly positive amount smaller than the negative gap. Every signed score is now strictly positive; averaging against full parity is strictly positive. Hence every $t$ requires a gate with all coefficients nonzero, and $S\ge2^d$. Possible semantic loss of dependence when all coefficients are nonzero only makes this counting condition weaker, never invalid. There is no top-norm assumption. Pure-table gates and zero top weights may be discarded. The proof does not cover unequal magnitudes or $d=1$ with free raw top wires.

[PROVED CHECK] The general inequality $\sum_jp_j\ge1$, with $p_j=\prod_i\#\{t_i:u_{ji}+t_iv_{ji}\ne0\}/2$, is equally valid. A doubly-zero pair gives zero; an equal nonzero magnitude pair gives $1/2$; every other pair gives one. This exact syntactic count is not stable under generic coefficient perturbations.

## 2. A limitation of survivor amplification

[PROVED / REFUTED universal demand; sent to LOW1] On $d$ bits,

$$\prod_{i=1}^d(1-2z_i)=\sum_{U\subseteq[d]}(-2)^{|U|}\Bigl[\sum_{i\in U}z_i\ge|U|\Bigr].$$

There is exactly one fully dependent bottom in this representation; every other bottom omits at least one variable. The empty-set term is the free constant. Thus after granting arbitrary missing-variable features there is no lower demand of two or more fully dependent survivors. This does not rule out a tradeoff counting the discarded features: this particular representation has $2^d-1$ bottoms. It does rule out applying a parity slicing lower bound directly to the surviving subset. The quotient by all degree-$<d$ functions is one-dimensional, explaining the limitation.

## 3. Almost equal coefficients: semantic stability versus a polynomial compiler

### 3.1 Exact stability statement

[PROVED elementary] If every bottom's Boolean truth table on the entire input domain admits a representation with zero address normal or full-support equal-magnitude address normal, then UP2's exponential theorem applies even if the supplied numerical representation has unequal coefficients. Replace each bottom independently by its equal-magnitude representation; every bottom output and hence the complete circuit remain unchanged. The equal representation may use a different threshold and table coefficients.

One sufficient perturbation condition is explicit. In raw signs, start with a strict equal-magnitude gate score $L_0(x,z)$ having finite-domain gap $\eta=\min_{x,z}|L_0(x,z)|>0$. Perturb the address coefficient vector by $e$ and the threshold by $\delta$ while fixing table coefficients. If $\|e\|_1+|\delta|<\eta$, the Boolean gate is unchanged. Starting from an ordinary weak threshold, first move its threshold slightly downward to eliminate all ties without changing outputs. This is a semantic stability statement, not an extension to all numerically close coefficient vectors.

### 3.2 A depth-preserving near-equality compiler

[PROVED; derived in this round, no priority claim] Let $M$ be the number of raw address bits, $U(a)=\sum_{l=1}^M a_l$, and let $g(x,a)=[L(x,a)\ge0]$, where $L=\alpha\cdot x+\gamma\cdot a-\theta$ is any real affine form. For every $B>\max_{x,a}|L(x,a)|$,

$$\boxed{g(x,a)=\sum_{r=0}^{M}[B(U(a)-r)+L(x,a)\ge0]-U(a).}$$

To prove it, fix an input and write $t=U(a)$. For $r<t$ the threshold score is strictly positive, for $r>t$ it is strictly negative, and for $r=t$ the indicator equals $g$. There are exactly $t$ earlier terms. This also handles threshold ties at $L=0$ exactly.

Every compiled bottom has address coefficients $B+\gamma_l$. Given any $\varepsilon>0$, choose $B$ additionally so large that these are positive and

$$\frac{B+\max_l\gamma_l}{B+\min_l\gamma_l}\le1+\varepsilon.$$

Such a finite $B$ exists; arbitrary real weights are allowed. No extra depth, intermediate computed feature, or bounded top norm is used. For a score $F=q(x,a)+\sum_jv_jg_j$, replace each bottom by this identity and absorb $-\sum_jv_jU$ in the free affine top part. Gate count grows by at most $M+1$. Different gates may use different $B_j$.

[PROVED consequence / REFUTED extension] Full-support address normals with arbitrary prescribed positive ratio tolerance $1+\varepsilon$ admit exact ordinary Andreev circuits of size $O(n^3)$, by applying the compiler to the inherited $O(n^2)$ construction. Here $\varepsilon$ may tend to zero arbitrarily rapidly with $n$. Half-coordinate parity, formerly requiring $2^{M/2}$ equal-magnitude gates, has $O(M^2)$ compiled gates. Consequently no exponential theorem survives **mere numerical near equality**, even with all address coefficients positive. The compiler does not give an exponent improvement; its purpose is to refute an attractive but false robustness hypothesis. Positivity is compatible with the inherited sign-coherent $\widetilde\Omega(n^2)$ bound for full Andreev.

[PROVED mechanism] As $B\to\infty$, normalized compiled scores approach total-address-count thresholds. At the integer layer $U=r$, the lower-order original form decides the gate output. Thus these gates split a large tied level of the limiting equal-weight form. They need not be truth-table-equivalent to their equal-weight limit, regardless of how small the normalized perturbation is. Section 3.1's positive-gap premise is precisely what fails.

### 3.3 Stronger near-equality consequence of UP2's two-scale construction

[PROVED CONSEQUENCE; construction mechanism attributed to UP2] For any even integer $B\ge2$, replace UP2's magnitudes $1,2$ by $B-1,B$: use $B-1$ on the selected character blocks and $B$ on the complement, with arbitrary signs. Let $M=km$ and write this address form as $L_T$. Its parity remains $\chi_T(b)$; its coefficient ratio is $B/(B-1)$, and its attained integer range has length $BM-m|T|$.

For $X_T=\sum_c\chi_T(c)(1-2x_c)$, which is even when $k\ge1$, and $\varphi(u)=(-1)^u u$,

$$\varphi(X_T+L_T)-\varphi(L_T)=X_T\chi_T(b).$$

Including the free affine $X_\varnothing$, the sum is $N(1-2x_b)$. Every term is a raw affine staircase. Summing the lengths of the two ranges over $T\ne\varnothing$ gives at most

$$2N(N-1)+(2B-1)MN-2BM$$

bottoms. No intermediate parity or Fourier gates are assumed; all affine forms are substituted into the raw thresholds. Choosing an even $B\ge1+1/\varepsilon$ proves $O_\varepsilon(n^2)$ exact circuits with full-support ratio at most $1+\varepsilon$ for every **fixed** $\varepsilon>0$. This already rules out a uniform exponential lower bound at any fixed positive tolerance. Arbitrary signs may be imposed, so positivity of the original count-layer compiler is not essential to this counterexample.

Combining the two constructions gives, for $0<\varepsilon\le1$ at balance,

$$S=O\!\left(\min\{\varepsilon^{-1}n^2,n^3\}\right).$$

For a shrinking tolerance the first route pays for its integer scale, whereas the second route has coefficient magnitudes depending on the tolerance but a gate count independent of it. These are architecture counterexamples, not an improvement of the unrestricted quadratic upper bound. For fixed $B$ and one Walsh table statistic per gate, UP2's slab-charge theorem supplies the matching exponent two; I do not claim an independently new matched-class theorem.

## 4. Mixed signed table paths: exact dual outside the full-sign class

### 4.1 What survives of private-owner extraction

[KNOWN, round-one LOW2 §4] The private-owner reduction requires every table-to-output path and every raw top table coefficient to be nonnegative after orienting bottom outputs. Dense signed table normals do not satisfy it. In complementary-singleton differences a balanced signed row already contributes positively to many labels. Merely asserting that a small negative mass or few negative entries is harmless is not justified: the owner slab's inclusion in every nonowner negative slab depends on exact sums of all other table coefficients. A negative coefficient can invalidate that containment at the slab's extreme tails, even when its numerical size is arbitrarily small. Since top coefficients are unbounded, small tail width cannot be discarded.

[REFUTED local extension, explicit example] Take $\alpha=(2,-\varepsilon,0,0)$ with $0<\varepsilon<1$ and complementary-singleton residual threshold $T=-\varepsilon/2$. The sum is $A=2-\varepsilon$, and coordinate 1 has the positive owner slab $A-\alpha_1=-\varepsilon<T\le2$. Its difference is $+1$. At coordinates 3 and 4, however, both threshold evaluations are one, so the difference is 0, not $-1$. Thus the round-one pointwise private-dominance inequality fails despite an arbitrarily small negative table coefficient. This does not refute all possible generalized private-kernel reductions; it pinpoints the failed inequality.

### 4.2 A genuinely unequal-magnitude oriented dual

[VERIFIED EXACT FINITE; method inherited from round-one LOW2, instance and semantic audit new] `unequal_certificate.json` contains 48 raw threshold gates for $A_{2,2}$. Every table row has mixed signs. Every address row has mixed signs and its four absolute magnitudes are exactly $1,2,3,4$ in some order. All thresholds and coefficients are integers in signed raw-input coordinates.

The pool has these exactly verified properties:

- All 3,840 distinct-table-pair / ordinary-address-edge rectangle rows are nonzero; each has at least four witnesses.
- All 1,536 forced-sign oriented rectangle rows are nonzero.
- A positive rational combination of 49 of those oriented rows is exactly zero in every one of the 48 bottom coordinates.
- Every raw affine feature cancels in every rectangle individually; the independent verifier additionally checks all 57 signed-feature equations (48 bottoms, eight raw inputs, and the constant).

For a rectangle $(x,x';a,a')$ with target signs $+,-,-,+$, strict exactness forces

$$\sum_jv_j\bigl(g_j(x,a)-g_j(x',a)-g_j(x,a')+g_j(x',a')\bigr)>0.$$

A positive combination of such inequalities would still be strictly positive, whereas the certificate makes its left side zero. Thus **no real top coefficients**, including arbitrary raw top coefficients, compute Andreev with this pool. Dividing the rectangle weights by four yields an ordinary nonnegative input measure of total mass one annihilating every label-signed feature.

This is genuinely beyond the round-one paired class. Every selected/ignored coefficient pair has unequal absolute magnitudes, so the syntactic pairing coverage value is $p_j=1$. Moreover every gate is excluded from the **semantic** full-sign class: each address coordinate is essential somewhere over all table/address inputs. Its sign in any threshold representation is therefore fixed by unateness. For each gate the certificate records one table and two addresses having equal Hamming count after those forced sign flips, but different gate outputs. A full equal-magnitude address normal would have equal outputs there, whatever its table coefficients and threshold. Thus a gatewise semantic replacement cannot apply UP2's theorem to this pool.

This is a finite guardrail for the desired positive-dual mechanism, not asymptotic evidence and not a lower bound of 49 gates for $A_{2,2}$. The target has a much smaller circuit using different bottoms. No claim is made that every random unequal-magnitude pool fails.

### 4.3 Discovery, checks, and negative result

[VERIFIED] `unequal_dual.py` uses the already installed SciPy LP only to discover a support. It then reconstructs strictly positive rational weights by exact elimination and checks every equation. `verify_certificate.py` independently uses only the Python standard library to reevaluate all gates, all rectangle coverage demands, all semantic witnesses, all certificate signs, and all rational annihilation equations from the saved JSON. The verifier passes.

[VERIFIED numerical diagnostic only] An initial 72-gate prefix of the same deterministic random sequence had an infeasible rectangle-dual LP, so no certificate was obtained for that pool. The 48-gate prefix above has a verified exact certificate. No conclusion of actual computability, or even exact oriented feasibility, is inferred solely from the floating-point failure at 72. This dependence on the chosen pool is a useful warning against extrapolating the successful finite dual to an asymptotic theorem.

## 5. Substantive peer exchanges and checked intermediate theorems

### 5.1 LOW1's spectrum/support-overlap extension

[PROVED CHECK, theorem and full proof belong to LOW1 round-two §3] Averaging UP2's paired restrictions over perfect matchings gives

$$1\le\sum_j\frac{\operatorname{per}C^{(j)}}{d!},$$

where $C_{il}$ is $0$ for two zero coefficients, $1/2$ for equal nonzero absolute values, and $1$ otherwise. LOW1 proves the soft permanent estimate

$$\frac{\operatorname{per}C}{d!}\le\min\{1,e^2d^2\exp(-D(C)/d)\},\qquad D(C)=\sum_{i,l}(1-C_{il}),$$

using the classical Brégman inequality on an independent Bernoulli matrix of mean $C$. I checked the probabilistic factorization, the bound $(r!)^{1/r}\le(r+2\log d+2)/e$, the $d!$ denominator, and the zero-coefficient treatment on the board. This is an audit conditional on the classical Brégman theorem; LOW1 supplies the inspected primary citation and full proof.

Consequently, if every gate has identical absolute-coefficient histograms across its address blocks, with at most $q$ distinct values including zero, then

$$S\ge e^{-2}d^{-2}\exp(d/(2q)),\qquad d=m\lfloor k/2\rfloor.$$

This is a genuine restricted-class extension to unequal magnitudes and gate-dependent supports. At balance it is $\exp(\Omega(n/q))/n^2$, exponential for fixed $q$. It allows arbitrary table/top signs and real magnitudes but still requires exact multiplicities and cross-block spread. Character-specific supports, character-specific two-scale rows, and generic unequal magnitudes escape. I do not count this peer result as a LOW2 theorem.

### 5.2 LOW1's stronger survivor counterexample

[PROVED CHECK, attributed to LOW1 round-two §2] My one-survivor witness in §2 costs exponentially many missing-variable helpers. LOW1 strengthened it to one survivor plus $d(d-1)$ helpers. For $s=\sum_i z_i$, define

$$f(r)=\frac{(-1)^r}{d\binom{d-1}{r}}\sum_{u=0}^{r}\binom du,\quad 0\le r\le d-1.$$

Then

$$(-1)^s=\sum_i f(s-z_i)+(-1)^d2^d[s=d].$$

For $s<d$, the first sum is $(d-s)f(s)+sf(s-1)=(-1)^s$ by cancellation of consecutive cumulative binomial sums. At $s=d$, the remaining correction is exactly $(-1)^d2^d$. Each helper function telescopes into $d-1$ thresholds omitting one variable. This demonstrates that one surviving gate can suffice even with only quadratically many helpers. It strengthens, rather than retracts, the objection I sent to LOW1.

### 5.3 UP2's character-table slab charge

[PROVED CHECK, attributed to UP2 round-two report] Let $r_j$ count nonzero nonconstant Walsh coefficients of gate $j$'s table-normal vector. Comparing the two complementary $T$-character tables cancels every gate with zero $T$ coefficient. Raw address top terms cancel; raw table terms become a constant. The actual score difference must sign-compute parity on $m|T|$ raw bits. Each remaining bottom difference has two boundary halfspaces, which together must slice every parity edge. Hence

$$\sum_jr_j\ge\tfrac12\sum_{T\ne\varnothing}\operatorname{slice}(m|T|).$$

I checked this charge and all free-top terms on the board. For $r_j\le r$, it imports the inherited $\widetilde\Omega(n^{32/19}/r)$ bound; individually rescalable integer address normals in $[-C,C]$ give $S\ge kmN/(16Cr)$. LOW1's semantic strengthening counts only character differences that are nonconstant on the address cube, and survives truth-table-preserving perturbations. Generic mixed table directions can serve many characters, so no unrestricted exponent follows.

[PROVED peer construction, checked algebraically] UP2's full-support two-scale row has odd coefficients $\pm1$ on selected character blocks and even coefficients $\pm2$ elsewhere. Its parity is the chosen character. Substituting it in the original Walsh staircase identity gives a common exact top score of size $O(n^2)$. Thus that sparse-Walsh bounded-scale class has exponent exactly two, despite full support and arbitrary within-block signs. This also supplies a simple escape from the equal-magnitude exponential theorem. It is not a new unrestricted upper benchmark.

### 5.4 UP1's coupled corrections and approximate product

[PROVED CHECK, attributed to UP1] On complementary character tables that saturate every retained central-window bottom, their difference is address-constant. Adding a correction of address degree $r<m|T|$ cannot supply a strict parity score; orthogonality still refutes it. Thus the proposed shared quadratic cancellations do not repair those tails merely by being globally coupled.

[PROVED CHECK of integral, utility unresolved] UP1 proposed a four-halfspace kernel for multiplying signs of nonzero affine scores. It equals $\operatorname{sgn}(uv)$ precisely on $||u|-\lambda|v||<t\le|u|+\lambda|v|$. Its double integral against $dt\,d\lambda/(t\lambda)$ is $(\pi^2/2)\operatorname{sgn}(uv)$: after integrating $t$ and rescaling, the scalar integral is $4\sum_{q\ge0}(2q+1)^{-2}$. I checked and posted this identity. Bounded nonzero integer score ranges permit finite-grid approximate sampling; unrestricted real scores require an explicit minimum gap. In either case, preserving a weighted aggregate needs error below its actual margin divided by coefficient variation. No gate lower bound may be inferred from that norm ratio, and no exact Andreev improvement is claimed.

## 6. Verification, final status, and next step

[VERIFIED] All owned computations finished. No packages were installed. Reproduction commands:

```bash
python3 -I /tmp/andreev_gap/swarm_round2/low2/checks.py
python3 -I /tmp/andreev_gap/swarm_round2/low2/verify_certificate.py
```

`checks.json` records 2,400 paired-cancellation rows, 6,200 compiler input identities, 125 coefficient-ratio checks, 1,550 semantic-stability inputs, 124 monomial parity identities, 336 compiled partial-parity inputs, and 768 complete near-equal Walsh-circuit inputs expanding 165,888 raw bottom evaluations. These check explicit identities; they are not evidence for an unproved asymptotic claim. `certificate_verification.json` records 57 exact rational annihilation equations, 49 positive rectangle weights, 1,536 oriented and 3,840 ordinary coverage tests, and 48 semantic full-sign exclusions.

[PROVED / main audit outcome] No actual gap was found in UP2 round-one §6 or in the corresponding paired-cancellation proof now visible in `threshold_paper/paper.tex`. Its exact $2^{m\lfloor k/2\rfloor}$ bound retains all stated hypotheses. I posted that audit early so the parent need not infer a problem from ongoing extension research.

[PROVED / strongest own new conclusion] Numerical near equality is an invalid exponential-hardness hypothesis. An arbitrary circuit has the exact $(M+1)$-overhead compiler of §3.2, with arbitrarily small coefficient-ratio tolerance. Combined with UP2's parity-scale mechanism, §3.3 gives exact near-equal full-support Andreev circuits of size $O(\min\{\varepsilon^{-1}n^2,n^3\})$ for $0<\varepsilon\le1$, and thus exponent **two** for every fixed positive tolerance. This is a robustness counterexample, not an improved unrestricted upper exponent. Truth-table-equivalent perturbations still obey the original exponential theorem.

[VERIFIED EXACT FINITE / mixed signed paths] The 49-rectangle certificate rejects a genuinely unequal-magnitude 48-bottom pool with all pair-coverage demands satisfied. It is outside both syntactic cancellation and semantic full-sign replacement. It supplies a valid positive dual with arbitrary real top weights, but no scalable forced-dependence theorem. The attempted simple owner-slab extension already fails with one arbitrarily small negative table coefficient (§4.1).

[PROVED CHECK / peer intermediate results] LOW1's identical-block magnitude-histogram class has lower bound $e^{-2}d^{-2}\exp(d/(2q))$, allowing unequal values and support variation; I audited its permanent argument. UP2's bounded-Walsh-support/bounded-address-scale class has exponent two, including its exact full-support two-scale upper family; I audited the charge. Both are substantial stated-hypothesis intermediate results, attributed to their authors, and neither proves an unrestricted exponent change.

[REFUTED / dead ends] Demanding multiple fully dependent survivors after freely discarding missing-variable gates is false; LOW1 strengthened my witness to quadratic helper count. Almost equal coefficients need not preserve Boolean functions at tied levels. Tiny negative table paths need not preserve private owner containment. Nonzero rectangle rows and complete pair coverage still fail to enforce one common top. Small correlations or thin exceptional slabs cannot be dropped when top weights are unbounded.

[CONJECTURE / single next step] Seek an analytic **positive dependence of oriented rectangle rows** for structured two-scale address directions whose magnitude profiles vary by character/block and whose table normals have large semantic Walsh support. This class evades both LOW1's cross-block histogram hypothesis and UP2's small-Walsh-support charge, yet has a known exact quadratic benchmark. The finite unequal-magnitude certificate supplies a concrete algebraic target; the needed theorem must force such a dependence for every library below an improved size threshold, not just random libraries or one favorable finite pool. This remains open.

[UNRESOLVED unrestricted objective] Neither an exact $n^{2-\delta}$ construction nor a lower bound $n^{3/2+\delta}$ for fixed $\delta>0$ was obtained. The unrestricted gap remains unchanged. All new files credit Christian Reitwiessner, source attribution is retained, and all work is confined to the assigned folder plus append-only board exchanges. No shared-paper edit, external post, or additional subagent was made.

### 5.5 Late audit: UP2's costed hybrid obstruction

[PROVED CHECK; attributed to UP2 round-two §3] After my initial handoff, UP2 posted a stronger hybrid theorem. It allows $H$ dense-table full-sign equal-magnitude address helpers, plus $E_T$ gates per character whose table rows lie in $\operatorname{span}(1,\chi_T)$ and whose address rows are multiples of one fixed signed two-scale $1/2$ direction for that character. Pure-address features and arbitrary top weights are permitted.

I checked the embedding and posted the audit. On complementary $T$ tables every other character channel cancels. Write the own direction, after bit flips and an additive shift, as $L_T=p+2q$, with $d=m|T|$ selected and $e=M-d$ ignored bits, and $K=d+2e$. The own gates at both tables make at most $2E_T$ cuts of the integer levels $0..K$, leaving an interval of at least $\lceil(K+1)/(2E_T+1)\rceil$ levels where all are constant.

Choose $r=\max\{2,\lfloor\log_2(2H+1)\rfloor+1\}$, so $2^r>2H$. Provided $d\ge r+1$ and $e\ge r$, retaining $r$ selected and $r$ ignored bits gives a range $0..3r$. Fixed remaining coordinates can supply every baseline from $0$ to $K-3r$: the selected interval $0..d-r$ has length at least one and fills the gaps between the even ignored contributions. A constant interval with at least $3r+1$ levels therefore makes the entire own channel constant on such a retained cube. The difference score would then compute selected $r$-bit parity using at most $2H$ full-sign helpers plus a constant, contradicting the audited pairing theorem. Consequently

$$E_T>\frac12\left(\frac K{3r}-1\right).$$

Summing middle characters proves $\Omega(MN/\log(H+2))$ dedicated gates for polynomially many helpers, hence exponent two at balance. Sparse $1/0$ own directions have the same proof with live range $r$ instead of $3r$. The one-direction-per-character assumption is essential to this interval proof; arbitrary support/magnitude-dependent helpers remain outside it. This is a valid costed hybrid obstruction, unlike discarding every missing-variable gate for free and applying slicing to the remainder. It is UP2's theorem, not an additional LOW2 claim.
