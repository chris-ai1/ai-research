# Round 3 UP1: exact coupled cancellation research

Authors: Christian Reitwiessner

Status: COMPLETED round-three UP1 research. No unrestricted exponent improvement.

## Outcome

**No exact $n^{2-\varepsilon}$ ordinary-Andreev circuit was obtained.** The supplied unrestricted gap remains unchanged.

[PROVED, strongest own local characterization] On the punctured integer square of radius $R$, the entire class $f(u+v)+g(u-v)+h(u)+j(v)$ has optimal sign-product amplitude distortion exactly $r=\lfloor(R+1)/2\rfloor$ and optimal uniform additive error exactly $(r-1)/(r+1)$. A $4r$-raw-threshold witness attains both. The complete proof is §4; LOW2 independently checked the cocycle and witness. This is an exact local approximation theorem, not a lower bound against arbitrary Andreev circuits.

[PROVED, substantive joint exponent result] The exact shuffled-bridge occupation formula in §5 supplies a missing lemma for LOW2's address-profile isolation theorem. Combined with the inherited common-mask signing lemma, it improves that theorem's mask loss from $2^R$ to $R$, giving $\widetilde\Omega(n^2/R)$ for its explicitly defined two-block-magnitude class with arbitrary dense table normals and real scale ratios, when $R^2\le(m-O(k\log G))/2$. For $R=n^{o(1)}$ this excludes a fixed-power upper improvement. LOW2 originated the profile graph and drift-prefix application; UP2 and LOW2 independently derived the bridge formula, and the contributions are credited below.

[PROVED, further mechanism audits] Exact multiplication of a whole score by a $q$-monomial raw-table polynomial costs at most $q(J+n+1)$ bottoms (§2), preserving a common multiplier without norm sampling. Universal exact real-valued product identities fail on the continuous punctured square for $R>3$ (§3). On the finite integer grid, arbitrary mixed integer ridge directions of total primitive-coordinate budget $D$ cannot give exact product amplitude when $R\ge2D+1$ (§6). Large or irrational slopes remain outside that last theorem.

[VERIFIED] All standard-library exact checks passed; no asymptotic claim relies on finite extrapolation. No paper edits, package installs, online posts, or additional agents.

## Model and mission

Ordinary exact $\mathrm{THR}\circ\mathrm{THR}$ for unrestricted Andreev: $N=2^k$ independent table bits, $k$ parity blocks of length $m$, $n=N+km$, and $km=\Theta(N)$. Arbitrary real weights, mixed signs, and raw top wires are allowed. Every threshold gate must be charged, and all bottom gates see only raw inputs. Target is an exponent improvement, not a constant or logarithmic improvement.

Investigate exact common-amplitude identities, coupled corrections, and nonseparable ridge/finite-difference identities. Read all earlier reports before proposing candidates. Exact character-table and rare-input constraints will be imposed before accepting constructions. Prior proved obstructions are not open candidates.

## Progress

- Initialized report before research. Read COMMON.md, all eight completed round-one/two reports, the round-two board, research state, and the paper sections supplying the exact/approximate constructions and model.
- No paper edits, package installs, or additional agents.

## 1. Exact constraints imposed before construction

[KNOWN, round-one UP1 §3 and round-two UP2 §1] For complementary character tables $x_T^\pm(c)=(1\pm\chi_T(c))/2$, the actual common-top difference must have strict sign $\chi_T(b(a))$ on every raw address. All raw-address terms cancel; raw-table terms leave a constant. Central-window libraries with saturated table offsets fail this condition under every top refit. Characters with $|T|\asymp k$ impose parity on $\Theta(n)$ raw bits.

[KNOWN, round-two UP1 §4] Any repair of a saturated character pair using a threshold bank with top variation $B$ and protected margin $\mu$ needs $B/\mu\ge2\sqrt{m|T|}$. The norm-sampling route is closed here. No low-variation target is left open in this report.

[KNOWN, round-two UP2 §§1,3] Bounded semantic Walsh coupling and bounded integer address ratios force exponent two; fixed-mask real two-scale channels retain exponent two even with polynomial dense-table equal-magnitude helpers. Full support, a finite palette, or numerical near equality alone are not obstructions. New candidates must leave the actual semantic classes, rather than merely perturb written coefficients.

[CONJECTURE / posted early] The concrete local question is exact constant-amplitude multiplication of two raw affine signs on the punctured integer grid $1\le|u|,|v|\le R$, using fewer than $R$ halfplanes. The known dyadic kernel only computes the correct sign. I am testing exact finite quadratures, mixed finite differences, and a common positive amplitude across multiple channels. Even a positive local compiler would still need an all-input Andreev score and a full raw-gate count.

## 2. Exact common-amplitude modulation by a raw table polynomial

### 2.1 A positive compiler [PROVED; elementary distributive construction]

Let $C(x)$ be a conjunction of $r$ literals of raw TABLE bits, and let $L(x,a)$ be any raw affine form. Put $U_C(x)$ equal to the number of satisfied literals. For any $B>\max_{x,a}|L(x,a)|$,

$$C(x)[L(x,a)\ge0]=[L(x,a)+B(U_C(x)-r)\ge0].$$

If all literals hold, the new gate is the old one. If a literal fails, its score is at most $\max L-B<0$. Thus each product is ONE raw bottom threshold, with exactly the original address normal. Ties on the accepted conjunction are preserved. This does not multiply computed gates.

Let

$$H(x,a)=h_0+\sum_c u_cx_c+\sum_l w_la_l+\sum_{j=1}^{J}v_jg_j(x,a),$$

and let a raw-table polynomial have a specified literal-monomial expansion

$$P(x)=\sum_{\nu=1}^q p_\nu C_\nu(x).$$

Then $P(x)H(x,a)$ has an exact depth-two REAL-SCORE implementation with at most $q(J+n+1)$ bottoms, before merging. Products of $C_\nu$ with a raw input bit are conjunctions and therefore one threshold; products with $g_j$ use the formula above. Constants and empty conjunctions may be put directly at the top. This is a finite unrestricted-real coefficient compiler. It has no norm/margin or numeric-range dependence; its cost is the actual number $q$ of monomials, not the degree of $P$ or the number of its integer values.

In particular, for a nonvanishing raw TABLE affine form $U(x)=u_0+\sum_{c\in I}u_cx_c$, the product $UH$ uses at most $(|I|+1)(J+n+1)$ bottoms and, when $H$ is strict, has sign

$$\operatorname{sgn}(UH)=\operatorname{sgn}(U)\operatorname{sgn}(H).$$

Any correct finite weak-threshold score $H$ is first made strict by shifting its intercept within the least negative gap. This is an EXACT sign-switch compiler with the same common amplitude $|U|$ multiplying the entire original score. It avoids termwise normalization entirely. It is distinct from a constant-amplitude product or a general two-branch zero-extension. If $U$ contains only $n^{o(1)}$ raw table terms, its overhead is subpolynomial, regardless of coefficient sizes. A dense affine $U$ generally costs $N$ times the bank and does not yield the desired exponent.

No literature priority is asserted for conjunction gating or distributivity. The point is to identify and cost a genuinely exact common-amplitude mechanism in the stated raw depth-two model.

### 2.2 Why this does not give arbitrary branch selection [PROVED scope]

Multiplying a score by $U$ flips its sign on the negative guard region; it does not replace that score by an unrelated branch. In particular $UH$ is not $[U\ge0]H$. Multiplying different channel scores by different $U$ values generally destroys their common amplitude. A successful use must exhibit ONE common factor for the entire assembled score, or prove an actual dominance inequality for the differing amplitudes. The already-refuted sign-only substitution is not being reinstated.

Moreover table-polynomial modulation preserves every original address direction exactly in its table-reading gate products. It can create genuinely dense semantic table dependence, but does not create any new mixed-address geometry. Gated raw-address affine terms restrict to affine functions at every fixed table. This closure will matter for LOW2's new profile-isolation candidate.

## 3. A continuous exact-amplitude obstruction

### 3.1 Finite universal halfplane identities fail above dynamic range three [PROVED]

Let $R>3$ and $D_R=([-R,-1]\cup[1,R])^2$. There is NO finite expression

$$a_0+a_1u+a_2v+\sum_{j=1}^s c_j[\alpha_ju+\beta_jv\ge\theta_j]
=\operatorname{sgn}(u)\operatorname{sgn}(v)$$

on every $(u,v)\in D_R$, with arbitrary real parameters. Thus an exact universal common-amplitude multiplier for real affine values cannot have finite size depending only on the ratio of maximum to minimum nonzero magnitude. This is an auxiliary continuous-domain theorem, NOT a gate lower bound for the finite raw Boolean model or the integer grid.

**Proof.** Work first on the four open rectangles $Q_{\epsilon\delta}=\epsilon(1,R)\times\delta(1,R)$. On a small open cell avoiding the finitely many boundary lines, the threshold sum is constant; equality with a constant target forces $a_1=a_2=0$.

Group all nonconstant halfplanes by their exact boundary line. If a boundary line intersects one open rectangle, choose a point of intersection avoiding all other distinct lines and points immediately on either side. In suitable orientation, its entire group's contribution is $A[t\ge0]+B[t\le0]$, plus constants from other features. The target is constant on all three points. The two side values force $A=B$, and the boundary value then forces $A+B=A$, hence $A=B=0$. Thus the whole group contributes zero everywhere. This step handles weak-threshold ties and antiparallel boundaries; ignoring the boundary point would incorrectly retain an equality spike.

After removing those groups, every remaining halfplane is constant on each of the four open rectangles. It cannot separate a diagonal pair from the other pair, since the convex hulls already intersect at the center using one representative from each rectangle. Nor can it separate just one rectangle from the other three: for $R>3$, the convex hull of the other three OPEN rectangles intersects that rectangle's interior. For the positive-positive rectangle, take $1<t<(R-1)/2$ and choose $r\in(2t+1,R)$, $q=r-2t\in(1,R)$. The points $(r,-q)$ and $(-q,r)$ lie in two other rectangles and have midpoint $(t,t)$ in the first. Sign changes give the other cases. The same reasoning excludes a three-versus-one partition.

Therefore each remaining feature is constant, or selects two adjacent rectangles. Its four values have zero alternating rectangle difference, as does the constant term. The desired sign product has alternating difference four. Contradiction. $\square$

For $1\le R<3$ an exact four-halfplane representation DOES exist: choose $R-1<t\le2$ and use the round-two kernel $K_{1,t}$. For all $1\le A,B\le R$, $|A-B|<t\le A+B$, so its amplitude is exactly one. The borderline $R=3$ is deliberately not classified here.

### 3.2 Scope for the current task

[REFUTED specified route] A finite exact cubature of the logarithmic kernel that is valid for ALL real affine values with bounded ratio cannot supply a universal constant-amplitude compiler once $R>3$. Arbitrarily accurate approximation remains possible and is consistent with round two. The integer-grid question is NOT settled: the proof uses open neighborhoods and therefore cannot be transferred to finitely many raw input values. A valid discrete identity must exploit attainable-value structure, rather than be called a universal real-score identity.

[PROVED interpretation] The common-amplitude polynomial compiler in §2 avoids this obstruction because its gates may use the original raw table bits and its multiplier is $|U|$, not a constant-amplitude identity depending only on $(u,v)$. Neither statement implies an unrestricted Andreev size bound.

## 4. One-scale ridges have a linear amplitude-distortion obstruction

### 4.1 Exact cocycle [PROVED]

Consider the unusually generous local bank

$$H(u,v)=f(u+v)+g(u-v)+h(u)+j(v),$$

where $f,g,h,j$ are ARBITRARY real functions on the attained finite sets. Thus every number of thresholds, every top refit, and every pure-$u$ or pure-$v$ correction is permitted along these four directions. Define its odd-in-both-coordinates projection

$$\mathcal O H(A,B)=\tfrac14\bigl(H(A,B)-H(A,-B)-H(-A,B)+H(-A,-B)\bigr).$$

Writing

$$F(t)=\tfrac14(f(t)+f(-t)-g(t)-g(-t)),$$

one gets exactly

$$\mathcal O H(A,B)=F(A+B)-F(A-B),$$

and $F$ is even. Consequently, for every integer $r\ge1$ whose points occur in the domain,

$$\boxed{\sum_{i=1}^{r}\mathcal O H(2i-1,1)=\mathcal O H(r,r).}$$

The equality telescopes from $F(0)$ to $F(2r)$. It needs no coefficient bounds, positivity of individual terms, smoothness, or staircase assumption.

### 4.2 Uniform approximation and amplitude consequences [PROVED]

On the punctured integer square $1\le|u|,|v|\le R$, choose $r=\lfloor(R+1)/2\rfloor$. If $H$ approximates $\operatorname{sgn}(uv)$ uniformly within $\epsilon$, then its odd projection lies in $[1-\epsilon,1+\epsilon]$ on every positive pair. The cocycle forces

$$r(1-\epsilon)\le1+\epsilon,\qquad
\boxed{\epsilon\ge\frac{r-1}{r+1}.}$$

In particular exact equality is impossible already for $R\ge3$, and even a fixed useful additive error bound is impossible as $R\to\infty$. This applies to the ENTIRE four-direction ridge span, not just to positive coefficients or the round-two kernel weights.

If instead $H$ merely has the correct strict sign everywhere and its signed values satisfy $0<\mu\le\operatorname{sgn}(uv)H(u,v)\le B$, the same projection lies in $[\mu,B]$ on positive pairs. Therefore

$$\boxed{B/\mu\ge\lfloor(R+1)/2\rfloor.}$$

Thus a one-scale two-ridge sign product necessarily has linear amplitude distortion, regardless of how many thresholds it uses. Taking the sign of this score is possible; using it as a constant-amplitude factor inside a sum is not. Common input rescaling gives the same statement for $u\pm\lambda v$ whenever the corresponding scaled integer test grid is attained.

The $r=2$ identity is an explicit 12-point equality obstruction: the alternating rectangle at $(1,1)$ plus the one at $(3,1)$ minus the one at $(2,2)$ annihilates every allowed ridge, while its value on the exact product is one after division by four. This signed functional is NOT a positive sign-computation dual, and is not claimed to be one.

### 4.3 Scope and asymptotics

[REFUTED specified route] Fixed-scale finite differences or threshold refitting on $u\pm v$, even with arbitrary separate corrections, cannot normalize the product to a constant or a fixed relative amplitude interval. An actual multiscale scheme must introduce genuinely different slope ratios; merely adding more thresholds on the same directions does not help.

[UNRESOLVED] The analogous exact-product complexity with arbitrarily many unequal slopes on the FINITE integer grid remains open in this run. The continuous theorem of §3 must not be used as a discrete lower bound. Neither result changes either unrestricted Andreev exponent.

### 4.4 The distortion and approximation bounds are EXACTLY sharp [PROVED]

Put $r=\lfloor(R+1)/2\rfloor$ and

$$F(t)=\min\{\lfloor |t|/2\rfloor,r\},\qquad
H_*(u,v)=F(u+v)-F(u-v).$$

For positive integers $A,B\le R$, let $s=A+B$, $d=|A-B|$. These have the same parity, $s-d=2\min(A,B)\ge2$, and $d\le R-1$. Therefore $\lfloor d/2\rfloor\le r-1$ and

$$1\le F(s)-F(d)\le r.$$

Oddness in each coordinate gives $1\le\operatorname{sgn}(uv)H_*(u,v)\le r$ on the whole punctured square. Both extremes are attained: $(1,1)$ gives one and $(r,r)$ gives $r$. Thus the optimal maximum/minimum signed amplitude ratio among ALL sign-correct four-direction ridge scores is EXACTLY

$$\boxed{\lfloor(R+1)/2\rfloor.}$$

Scaling $H_*$ by $2/(r+1)$ achieves uniform product approximation error exactly $(r-1)/(r+1)$, matching §4.2. Hence this is also the exact optimum additive error for that entire linear function class.

The witness has an honest $4r$-gate raw realization:

$$F(t)=\sum_{q=1}^r\bigl([t\ge2q]+[-t\ge2q]\bigr),\qquad
H_*=\sum_{q=1}^r K_{1,2q}(u,v).$$

Substituting raw affine $u,v$ gives four raw bottoms per $q$ and one common top. This is NOT an unrestricted product optimum or an Andreev upper bound. It is a tight all-size characterization of a natural finite-difference normalization class, including arbitrary univariate corrections and arbitrary top cancellations.

## 5. Substantive cross-agent advance: exact bridge occupation bound

LOW2 requested a random-prefix replacement for the exponential $2^R$ mask-class loss in its new profile-isolation theorem. The following exact calculation supplies that missing ingredient. This is a standard walk-generating-function argument developed here for the requested application, not a claim of literature priority.

### 5.1 Exact local-time formula [PROVED]

Let a path be a uniformly random permutation of $p$ steps $+1$ and $q$ steps $-1$, with $p\ge q$, $h=p+q$, and $\Delta=p-q$. Include its initial and final positions among its $h+1$ visits. For an integer level $\ell$, write $d=\operatorname{dist}(\ell,[0,\Delta])$. Then

$$\boxed{\mathbb E V_\ell=\frac{\sum_{i=0}^{q-d}\binom{h+1}{i}}{\binom hq},}$$

where the numerator is zero if $q-d<0$. Thus the expected occupation is constant for every level between the two endpoints and is smaller outside that interval.

**Proof.** Let $W_s(z)$ count unrestricted nearest-neighbor walks from zero to the integer $s$, by length. As a formal power series,

$$W_s(z)=\frac{r(z)^{|s|}}{\sqrt{1-4z^2}},\qquad
r(z)=\frac{1-\sqrt{1-4z^2}}{2z}.$$

For completeness, $W_0=\sum_{t\ge0}\binom{2t}{t}z^{2t}=1/\sqrt{1-4z^2}$. For $s\ge1$, the walk recurrence $W_s=z(W_{s-1}+W_{s+1})$ and symmetry select the formal root $r=z+O(z^3)$ of $r=z(1+r^2)$, yielding the displayed expression. Equivalently one can verify its coefficient recurrence directly. These identities are formal power series, so no analytic convergence is needed.

Counting a walk to $\Delta$ with a marked visit to $\ell$ gives the product $W_\ell W_{\Delta-\ell}$. Put $D=|\ell|+|\Delta-\ell|=\Delta+2d$ and

$$C_D(h)=[z^h]\frac{r^D}{1-4z^2}.$$

The identity $1-r^2=r\sqrt{1-4z^2}/z$ implies

$$C_D(h)-C_{D+2}(h)
=[z^{h+1}]\frac{r^{D+1}}{\sqrt{1-4z^2}}
=\binom{h+1}{(h-D)/2}.$$

Telescope until $D>h$, when the coefficient is zero. The numerator becomes $\sum_{i=0}^{(h-D)/2}\binom{h+1}{i}=\sum_{i=0}^{q-d}\binom{h+1}{i}$. There are $\binom hq$ paths with endpoint $\Delta$. Dividing proves the formula. $\square$

### 5.2 Uniform bound and its random-prefix consequence [PROVED]

For $0\le i\le q$, consecutive descending binomial terms satisfy

$$\frac{\binom{h+1}{i-1}}{\binom{h+1}{i}}
=\frac{i}{h+2-i}\le\frac q{p+2}<1.$$

Hence the maximum local time is at most

$$\frac{\binom{h+1}q}{\binom hq}\frac1{1-q/(p+2)}
=\frac{(h+1)(p+2)}{(p+1)(\Delta+2)}
\le\boxed{\frac{h+1}{\Delta+1}}.$$

The last inequality is equivalent to $\Delta\le p$. For a prefix time chosen uniformly from $0,\ldots,h$, independently of the shuffle, the probability of hitting ANY prescribed set of $w$ integer levels is therefore at most

$$\boxed{w/(\Delta+1).}$$

The same bound holds for negative endpoint drift after reflection. This is exactly the estimate LOW2 needs; it includes both endpoints, permits a gate-dependent target interval, and requires no independent signs within the shuffled path.

### 5.3 Application to LOW2's two-profile obstruction [PROVED consequence, tree mechanism attributed to LOW2]

The model is LOW2 round-three report §2: arbitrary dense table/top normals; two address magnitudes constant by block; arbitrary real ratios and one zero magnitude allowed; at most $R$ masks per unordered nontrivial block profile; full-sign uniform-magnitude gates and arbitrary pure-address helpers permitted. Set $r=\max\{2,\lceil\log_2(G+1)\rceil\}$, $L=(k-1)r$, and $h=m-(k-1)r>0$.

LOW2's connected-tree restriction reserves $L$ selected/ignored pairs and isolates the exceptional profile $P=\{T,T^c\}$. All other profiles can later be annihilated by random literal identifications, because some tree edge has equal magnitudes. The remaining task is to make the $E_P$ exceptional gates individually constant at BOTH character tables.

In one unused selected block and one unused ignored block, retain $h$ coordinates each. UP1 round-one §2.1 supplies, for each block, a common sign vector making every one of the profile's at most $R$ masks have absolute signed sum at least

$$\delta=h/R-R.$$

Use that vector as the common raw-bit complement convention. Choose a uniform random coordinate permutation in each block, and independently a uniform prefix time in $0,\ldots,h$. Set exactly that prefix to one in the complemented convention; this is a distribution of legitimate baseline assignments. Each mask sees a shuffled $\pm1$ bridge with absolute drift at least $\delta$.

For a fixed exceptional gate choose the baseline block on which its magnitude is maximal, say $W>0$, and condition on the other block's entire baseline. Its pre-identification live range has width at most $2LW$. Nonconstancy occurs when the normalized shuffled prefix sum falls in an interval of length at most $2L$, containing at most $2L+1$ integer levels. By §5.2, when $\delta\ge0$ its probability is at most $(2L+1)/(\delta+1)$. This holds uniformly for either fixed table and irrespective of the other baseline.

If $2E_P(2L+1)<\delta+1$, a union bound finds one pair of baselines making all exceptional gates constant at both tables. LOW2's subsequent literal-identification union bound then kills every other profile, producing its exact nonnegative character-parity dual. Thus

$$\boxed{2E_P(2L+1)\ge h/R-R+1}\qquad(h/R-R\ge0).$$

Summing the $N/2-1$ unordered profiles gives the strengthened restricted bound

$$\boxed{G\ge\left(N/2-1\right)
\frac{h/R-R+1}{2(2L+1)}.}$$

For $R^2\le h/2$, balanced parameters and polynomial $G$, this is $\widetilde\Omega(n^2/R)$, replacing the signature-class loss $2^R$ by $R$. In particular $R=n^{o(1)}$ with $R^2\le h/2$ still forbids a fixed-power subquadratic improvement. For fixed $R$ the matching exponent remains two. This is a joint application of LOW2's new profile graph, the inherited UP1 common-correlation lemma, and the bridge calculation above. It is NOT an unrestricted exponent change, and it does not assert that arbitrary address normals have two blockwise levels.

The raw-address affine terms produced by the compiler of §2 become affine after either table is fixed. They vanish under the retained parity of degree $L\ge2$, so adding these helper terms does not affect the dual. Table-only gating of the STRUCTURED profile-normal bank therefore cannot evade the new obstruction merely by acquiring dense semantic Walsh coupling. This closure applies to those structured bottoms and to affine-after-table-fixing helpers only. Arbitrary pure-address threshold helpers must remain ungated unless their normals independently satisfy the profile condition: multiplying one by a nonconstant table conjunction makes it a mixed gate that no longer cancels between character tables. LOW2 identified this essential scope qualification on the board; it is incorporated here.

## 6. A multiscale integer-direction finite-difference obstruction

### 6.1 Direction-budget theorem [PROVED]

Let $w_i=(\alpha_i,\beta_i)\in\mathbb Z^2\setminus\{0\}$, $1\le i\le t$, be the DISTINCT primitive integer directions of a proposed finite ridge representation. Arbitrary real rescaling of a direction and arbitrary offsets are harmless; the function along each direction is unrestricted. Put

$$D=\max\left\{\sum_i|\alpha_i|,\sum_i|\beta_i|\right\}.$$

If $R\ge2D+1$, no score of the form

$$H(u,v)=h(u)+j(v)+\sum_{i=1}^t f_i(\alpha_i u+\beta_i v)$$

can equal $\operatorname{sgn}(uv)$ on every nonzero integer $|u|,|v|\le R$. All $f_i,h,j$ may be arbitrary functions, so this includes unlimited threshold cuts, signed coefficients, and free raw affine terms. Directions along an axis can instead be put into $h$ or $j$; they need not count in $D$.

Thus an exact product identity with primitive direction entries bounded by $C$ requires $t>(R-1)/(2C)$, hence at least that many bottom gates. This is a local two-input integer-direction resource bound, not an unrestricted Andreev lower bound. Large primitive slopes or irrational directions escape; arbitrary real weights cannot silently be normalized to bounded integers.

**Proof.** Use only odd grid points, writing $(u,v)=2z+(1,1)$ with $z\in\mathbb Z^2$. Let $F(z)=\operatorname{sgn}(2z_1+1)\operatorname{sgn}(2z_2+1)$, and let $\Delta_v H(z)=H(z+v)-H(z)$. For each direction set its nonzero integer tangent $v_i=(\beta_i,-\alpha_i)$. Its own ridge is annihilated by $\Delta_{v_i}$. Hence

$$Q=\Delta_{e_1}\Delta_{e_2}\prod_{i=1}^t\Delta_{v_i}$$

annihilates EVERY term of $H$: a corresponding tangent difference kills each mixed ridge, and an axis difference kills each separate $h,j$ term. All differences commute.

On the target, however, $\Delta_{e_1}\Delta_{e_2}F=4\mathbf1_{\{(-1,-1)\}}$. Choose a real linear functional $\ell$ with $\ell(v_i)\ne0$ for every $i$. Let $A_*=\{i:\ell(v_i)>0\}$ and $s_*=\sum_{i\in A_*}v_i$. Among all subset sums, $s_*$ uniquely maximizes $\ell$, so its coefficient in the expansion of $\prod_i\Delta_{v_i}$ is exactly $(-1)^{t-|A_*|}$, even if other subset sums coincide. At $z_*=(-1,-1)-s_*$,

$$QF(z_*)=4(-1)^{t-|A_*|}\ne0.$$

Every stencil point at which $Q$ evaluates a score is

$$z_*+\sum_{i\in A}v_i+\epsilon e_1+\eta e_2,
\qquad \epsilon,\eta\in\{0,1\}.$$

Its original odd coordinates have absolute value at most $2D+1$; more precisely each coordinate of $\sum_{i\in A}v_i-s_*$ is bounded in absolute value by the sum of that coordinate's absolute tangent entries. They are odd and therefore nonzero. Thus all stencil points are in the assumed finite punctured grid. Exact equality there would imply $QH(z_*)=QF(z_*)$, contradicting $QH=0$. $\square$

### 6.2 Quantitative and design consequences [PROVED]

The unmerged stencil has total absolute coefficient mass at most $2^{t+2}$. Consequently, under the same range condition, every uniform additive approximation has error at least $2^{-t}$. This is usually much weaker than §4's sharp one-scale error but works for arbitrary finite integer direction sets.

[REFUTED specified route] Any bounded-integer multiscale exact quadrature with $tC=o(R)$ fails even with arbitrarily many thresholds and top refitting along its chosen directions. This attacks actual shared ridge identities; it does not infer an obstruction from sign-only witnesses. Dyadic slopes reaching scale $R$, incommensurate real slopes, or a raw-coordinate compiler exploiting more information than $(u,v)$ are not excluded. No proposed all-real-weight construction is claimed to be closed by this arithmetic budget alone.

## 7. Verification, exchanges, dead ends, and handoff

### 7.1 Exact artifacts [VERIFIED]

Run:

```bash
python3 -I /tmp/andreev_gap/swarm_round3/up1/checks.py
```

The script uses only the Python standard library and exact integers/rationals. `checks.json` records:

- 3,920 conjunction-gated threshold identities, including ties and off-conjunction inputs;
- 3,920 exact products of whole raw depth-two scores by literal-monomial table polynomials;
- 420 telescoping cocycles for arbitrary random univariate tables;
- 88,560 input evaluations of the explicit $4r$-bottom witness;
- 40 exact optimal-error/distortion checks for radii $1,\ldots,40$;
- five rational convex-hull witnesses for the continuous obstruction;
- 1,368 exact bridge occupation formulas and bounds, by full path enumeration through length 14;
- 120 exact finite-difference annihilator stencils for genuinely mixed primitive integer direction sets.

`stencil_certificate.json` stores one explicit equality-obstruction stencil and its target evaluation. For every permitted ridge direction, the coefficients at every attained linear-form value sum to zero. Its weights are NOT all label-oriented; it certifies failure of exact amplitude representation, not failure of sign computation. All files include Christian Reitwiessner's author credit. These finite checks are guardrails for the written universal arguments, not extrapolations to asymptotic exponents.

### 7.2 Substantive cross-agent exchange [PROVED CHECKS / attributed peer work]

I posted the constant-amplitude target before developing its proofs and requested character/finite-difference attacks. UP2 emphasized that even a cheap product compiler must pay for its whole unsampled bank, and supplied the correct diagonal-dominance condition for a table-linear final score. LOW1 correctly warned that a staircase in a computed logarithmic ratio is not a raw affine gate; none is used here.

I attacked LOW1's corner-specific helper burden by observing that a central-majority survivor has full parity coefficient of order $d^{-1/2}$, whereas the AND's is $2^{-d}$. No subquadratic helper construction was inferred. I checked UP2's all-complemented-bases face-coefficient lemma and credited the stronger conjunction theorem to the source UP2 found; I did not independently inspect that external source and do not claim its theorem as my own.

I checked LOW2's tree isolation, disjoint coordinate allocation, two-table cancellation, and simultaneous exceptional-gate constancy. In particular the random literal cancellation is independent of table offsets, so it needs a union bound over gate directions rather than twice that count; the baseline sweep still pays for both fixed-table versions. The tree idea and dense-table theorem belong to LOW2. Its independent two-baseline refinement was also supplied by UP2.

LOW2 then asked for the drifted shuffled-prefix local-time bound. I derived and posted the exact marked-walk formula and the sharp $(h+1)/(\Delta+1)$ upper estimate (§5), including a telescoping proof of the coefficient identity. LOW2 and UP2 independently obtained the same numerator, and UP2 independently obtained the same sharp upper estimate. LOW2 checked the bound and incorporated the improved mask inequality. The independent derivations are an audit, not three separate discoveries or an unrestricted result.

LOW2 independently checked §4's one-scale cocycle, the exact saturating witness, and the $4r$ raw threshold expansion. LOW2 also identified the overly broad possible reading of the table-gating closure: arbitrary pure-address thresholds cease to cancel when multiplied by a table predicate. I accepted this correction; §5.3 now requires those gated helpers to satisfy the structured normal hypothesis, or to remain affine after fixing the table. The compiler algebra itself never depended on that lower-bound scope.

All exchanges are append-only in `../board.md`. No new agents or threads were started.

### 7.3 Dead ends with precise reasons

[REFUTED specified routes]

1. **Universal finite exact real-amplitude quadrature.** For $R>3$, the continuous four-rectangle theorem excludes every finite halfplane representation. This does not exclude an attainable-value-dependent finite-grid identity.
2. **Fixed-scale normalization with arbitrary thresholds/refits.** The exact minimax error tends to one and the exact optimal amplitude distortion grows as $R/2$. Unlimited cuts and separate univariate corrections do not fix it.
3. **Bounded arithmetic-budget multiscale normalization.** If the mixed primitive integer direction budget is $D\le(R-1)/2$, the odd-grid finite-difference stencil excludes exact amplitude. Huge or irrational slopes are outside this result.
4. **Treating common multiplication as free branch selection.** $UH$ gives a common multiplier and a sign switch, not unrelated conditional branches. The literal-monomial count, not polynomial degree or coefficient size, is the compiler cost.
5. **Table-only enrichment of a structured address bank.** It preserves its address directions. LOW2's new profile obstruction, including the drift improvement, survives arbitrary dense table coupling in the stated mask regime. Gating arbitrary unstructured pure-address helpers is explicitly NOT covered.

[KNOWN closed before this round] Norm-based sampling on saturated character tails, low-degree repairs, sparse-Walsh bounded-ratio guards, equal-magnitude full-support pools, and survivor-only amplification were not revived as open candidates.

### 7.4 Single best next step and final status

[CONJECTURE / concrete next step] Seek a DISCRETE exact common-amplitude bank whose mixed guard/feature directions have sufficiently large or incommensurate primitive slopes and whose resulting raw address magnitudes vary within blocks. Impose the complementary-character parity constraints before optimizing, and require one shared top score on all independent tables. The remaining local question is the finite integer-grid product with unrestricted slopes; the remaining global requirement is a correction bank of subquadratic size before any per-product overhead. A solution of the local question alone would not establish Andreev's upper bound.

This step deliberately leaves the now-closed table-only/profile-preserving route. Actual coupling of different address normals is necessary to escape those restricted classes; semantic density only in table coordinates is not enough. It remains a research target, not a construction or existence assertion.

[FINAL STATUS] No exact unrestricted upper exponent below two and no unrestricted lower exponent above $3/2$ were obtained. The strongest own local result is the exact fixed-scale amplitude characterization (§4), supplemented by the integer-direction annihilator (§6). The strongest exponent consequence of the cross-agent work recorded here is LOW2's $\widetilde\Omega(n^2/R)$ profile-class bound, whose improved mask loss uses the bridge calculation (§5). Full proofs, source attribution and scope are retained. No shared-paper edit, package install, online post, or additional agent was made; all owned computations finished.

### Late peer-audit addendum

[PROVED CHECK, attributed to LOW1] Before final handoff, LOW1 independently checked §3's elimination of opposite-orientation line groups, including equality spikes, and its convex-hull midpoint argument. LOW1 also checked §4's sharp cocycle and matching clipped witness. These audits agree with the stated scopes: the continuous result is not a finite-grid lower bound, and the amplitude result is not a generic sign-computation dual.

[KNOWN from LOW2's completed board example] LOW2 made UP2's character-only warning concrete: $F(\xi,a)=\xi_{b(a)}+\sum_c\xi_c$ is strictly correct on every signed character table but fails at the selected negative entry of a table with one negative sign when $N\ge4$. Its quadratic raw implementation follows by adding a free table-affine term to the inherited exact score. This reinforces the report's requirement to test ALL mixed tables after character constraints; it is not a subquadratic character-promise construction.
