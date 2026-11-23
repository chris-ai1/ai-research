Authors: Christian Reitwiessner

# LOW1 round 2: common-top geometry beyond coverage

Status: completed second-round research handoff. No unrestricted exponent improvement.

**Strongest result [PROVED, restricted intermediate class]:** if each bottom has identical absolute-coefficient histograms across address blocks, with at most $q$ magnitude values including zero, then
$$S\ge e^{-2}d^{-2}\exp(d/(2q)),\qquad d=m\lfloor k/2\rfloor\ge2.$$
At balance this is $\exp(\Omega(n/q))/n^2$: exponential for fixed $q$, allowing arbitrary mixed signs, unequal magnitudes, gate-dependent supports, dense signed table weights, and unrestricted top weights. The complete proof is §3. It combines UP2's round-one parity pairing with an averaged permanent estimate derived using the classical Brégman inequality. LOW2 independently checked the permanent argument. No novelty priority is claimed.

**Other outcomes [PROVED]:** a one-survivor parity score with only $d(d-1)$ missing-variable helpers refutes stronger survivor-only amplification (§2); a semantic character-slab incidence refinement makes UP2's round-two charge invariant robust under truth-table-preserving perturbations (§4.1). A 1,024-input exact common-top dual for genuinely unequal, varying-support directions is saved (§3.6).

Mission: retain forced signs and one common top coefficient vector while allowing unequal address magnitudes and gate-dependent supports. Read and adversarially test all round-1 barriers; do not repeat pair-coverage or transcript-only arguments.

## Research log

- [KNOWN] Starting unrestricted exact gap is $\widetilde\Omega(n^{3/2})$ to $(5/16+o(1))n^2$. Fixed-error exponent is $3/2$.
- [CONJECTURE] A useful separation may reside in the compatibility of oriented table-derivative slabs under one global top coefficient vector, rather than in their coverage.

Proofs, exact checks, scope qualifications, and peer exchanges are recorded below.

## 1. Survivor amplification is false without charging discarded gates

[REFUTED, substantive peer exchange with LOW2] I proposed combining selected/ignored pairing with the hypercube slicing lower bound on gates retaining all live variables. LOW2 supplied the exact counterexample
$$\prod_{i=1}^d(1-2z_i)=\sum_{U\subseteq[d]}(-2)^{|U|}[z_i=1\text{ for all }i\in U].$$
Every summand is a threshold indicator, and only $U=[d]$ uses all variables. Therefore no universal lower demand above ONE fully dependent gate is valid after discarding arbitrary missing-variable thresholds. Such discarded thresholds can slice edges and supply the entire low-degree correction. The vector-space quotient by missing-variable functions has dimension one, spanned by full parity.

This counterexample costs exponentially many discarded gates. A quantitative tradeoff charging their cost could still be useful; it is not established. I acknowledged the objection on the board and redirected the research. Attribution: LOW2's round-two board response; the elementary multilinear expansion is classical.

[KNOWN/guardrail from UP2 round-two board] Full-support two-scale rows can simulate sparse character gates exactly when the total contribution of small coefficients is below an existing threshold gap. Finite magnitude alphabets alone do not give an exponential lower bound. Any overlap/spread hypothesis must be stated, and a syntax-based collision estimate is not robust under generic perturbations unless truth-table equivalence is retained.

## 2. Polynomial helpers strengthen the survivor-count barrier

[PROVED; extends LOW2's monomial witness] Full parity on $d\ge2$ bits has an exact depth-two real score with **one** fully dependent bottom and $d(d-1)$ bottoms each omitting one variable. Thus one cannot claim that a single survivor requires exponentially many helpers.

Let $s=\sum_i z_i$, $z_i\in\{0,1\}$, and for $0\le r\le d-1$ define
$$f(r)=\frac{(-1)^r}{d\binom{d-1}{r}}\sum_{u=0}^{r}\binom du.$$
Then
$$(-1)^s=\sum_{i=1}^d f(s-z_i)+(-1)^d2^d[s=d]. \tag{2.1}$$
For $s<d$, the sum on the right before its last term is $(d-s)f(s)+sf(s-1)$, taking $f(-1)=0$. The binomial identities $(d-s)\binom ds=d\binom{d-1}s$ and $s\binom ds=d\binom{d-1}{s-1}$ reduce this to the difference of successive cumulative binomial sums, which is $(-1)^s$. At $s=d$, that sum is $df(d-1)=(-1)^{d-1}(2^d-1)$, and the last term makes it $(-1)^d$.

Each $f(s-z_i)$ telescopes into $d-1$ thresholds $[\sum_{j\ne i}z_j\ge r]$, $1\le r\le d-1$, plus a free constant. The final AND $[s=d]$ is the sole bottom depending on all $d$ variables. Coefficients may be exponentially large, as the model permits. All normals use only zeros and ones, and the same common top vector implements the entire identity. This is a parity subproblem construction, not an Andreev circuit.

The full equal-magnitude/full-support theorem does not apply because every helper has a zero coefficient. Exactness on all parity inputs holds. No approximation or independent top fitting is used. A tradeoff with a quadratic cost scale remains conceivable, but is not proved here.

## 3. A permanent bound for unequal magnitudes and gate-dependent supports

### 3.1 Exact averaged cancellation matrix [PROVED]

Fix $k\ge2$ and $d=m\lfloor k/2\rfloor\ge2$. Choose a character table selecting $\lfloor k/2\rfloor$ blocks; if $k$ is odd fix one other block to zero. The target becomes $f(z,w)=\prod_{i=1}^d z_i$ on $d$ selected signs $z$ and $d$ ignored signs $w$.

For gate $j$, let $u_{j,i}$ and $v_{j,l}$ be its coefficients on these halves. Define the $d\times d$ matrix
$$C^{(j)}_{il}=\frac{\#\{t\in\{-1,1\}:u_{j,i}+tv_{j,l}\ne0\}}2.$$
Its entries are $0$ for a zero-zero pair, $1/2$ for equal nonzero absolute coefficients, and $1$ otherwise. These values make no assumption on signs, thresholds, table normals, or coefficient size.

Choose a uniform perfect matching $\pi$ between the halves and independent uniform signs $t_i$. Restrict $w_{\pi(i)}=t_i z_i$. The probability that gate $j$ has all $d$ nonzero live coefficients is exactly
$$p_j=\frac{\operatorname{per}C^{(j)}}{d!}. \tag{3.1}$$
For every $(\pi,t)$, a correct strict top score has positive full-parity correlation. Affine raw top terms have zero correlation, and every bottom with a zero live coefficient has zero correlation. Thus at least one bottom must retain all coefficients, regardless of its actual dependence after thresholding. Averaging gives
$$\boxed{\sum_{j=1}^S\frac{\operatorname{per}C^{(j)}}{d!}\ge1.} \tag{3.2}$$
This uses the same actual top score before and after restriction, not independently chosen local decoders. However it is a necessary covering consequence, not the whole common-top feasibility condition. The parity/cancellation step is due to UP2's round-one theorem; the matching average is the current extension. Pure-table gates have zero permanent and contribute nothing.

### 3.2 A general soft-permanent estimate [PROVED using a KNOWN theorem]

For any $d\times d$ matrix $C$ with entries in $[0,1]$, put
$$D(C)=\sum_{i,l}(1-C_{il}).$$
Then
$$\boxed{\frac{\operatorname{per}C}{d!}\le\min\{1,e^2d^2\exp(-D(C)/d)\}.} \tag{3.3}$$
All logarithms in this section are natural.

**Proof.** Let $H$ have independent Bernoulli entries with means $C_{il}$. Multilinearity of the permanent yields $\mathbb E\operatorname{per}H=\operatorname{per}C$. Write $R_i$ for its row sums and $\phi(r)=(r!)^{1/r}$ for $r\ge1$, with $\phi(0)=0$. The classical Brégman permanent inequality gives $\operatorname{per}H\le\prod_i\phi(R_i)$. Since the rows are independent,
$$\operatorname{per}C\le\prod_i\mathbb E\phi(R_i).$$
For integer $1\le r\le d$, monotonicity of $\log x$ gives
$$\log(r!)\le\int_1^r\log x\,dx+\log r=r\log r-r+1+\log r.$$
As $t=(1+\log r)/r\le1$ and $e^t\le1+2t$ for $0\le t\le1$,
$$\phi(r)\le e^{-1}(r+2\log r+2)\le e^{-1}(r+2\log d+2).$$
The last bound also holds for $r=0$. Put $\delta_i=\sum_l(1-C_{il})$, so $\mathbb ER_i=d-\delta_i$. Therefore
$$\operatorname{per}C\le e^{-d}\prod_i(d-\delta_i+2\log d+2).$$
The integral lower bound $\log(d!)\ge d\log d-d$ gives $d!\ge(d/e)^d$. Dividing and applying $1+x\le e^x$ to each positive factor proves
$$\frac{\operatorname{per}C}{d!}\le\exp\left(2\log d+2-\frac1d\sum_i\delta_i\right).$$
The other bound $\operatorname{per}C\le d!$ follows directly from its definition. This proves (3.3).

**Attribution and inspected source.** The nontrivial inherited ingredient is Brégman's theorem, not a newly proved permanent theorem. The exact statement and its Radhakrishnan entropy proof are given in Theorem 1 and Section 2 of Cutler–Radcliffe, [*An entropy proof of the Kahn–Lovász theorem*](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v18i1p10/pdf/), Electronic Journal of Combinatorics 18 (2011), P10. That primary research paper was opened and its theorem inspected. Radhakrishnan's original 1997 article was located, but direct publisher access returned 403; no claim of having read that inaccessible full text is made. The Bernoulli smoothing and coarse explicit estimate above are supplied in full here; no literature-priority claim is made for them.

### 3.3 Collision energy and the resulting lower bound [PROVED]

For a fixed gate, let $a_{j,\lambda}$ and $b_{j,\lambda}$ count occurrences of absolute coefficient $\lambda\ge0$ on the selected and ignored halves, respectively. Define
$$E_j=2a_{j,0}b_{j,0}+\sum_{\lambda>0}a_{j,\lambda}b_{j,\lambda}.$$
The exact cancellation matrix has $D(C^{(j)})=E_j/2$. Consequently every exact circuit obeys
$$\boxed{1\le\sum_j\min\{1,e^2d^2e^{-E_j/(2d)}\}.} \tag{3.4}$$
In particular, if $E_j\ge E$ for every gate with a nonzero contribution, then
$$\boxed{S\ge e^{-2}d^{-2}\exp(E/(2d)).} \tag{3.5}$$
Equivalently, every polynomial-size exact circuit must contain, for each chosen middle character and fixed removed block, a gate with
$$E_j\le2d(\log S+2\log d+2).$$
This is a precise structural alternative: substantial overlap of magnitude multiplicities on the two halves is incompatible with small exact circuits. It is not a statement about drift, signs, or globally comparable weights. Generic distinct magnitudes may give $E_j=0$, so the unrestricted obstruction remains absent.

### 3.4 A new intermediate class: identical block magnitude histograms [PROVED]

Suppose each bottom gate has the same multiset of absolute address coefficients in every block. The multiset may differ from gate to gate; its order within every block and every coefficient sign are arbitrary. Zeros are allowed, so supports may vary between blocks and gates. Let $q$ bound the number of distinct values in each gate's multiset, counting zero if present. Pure-table gates may also occur.

The selected and ignored halves have identical magnitude histograms, so $a_{j,\lambda}=b_{j,\lambda}$ and $\sum_\lambda a_{j,\lambda}=d$. Cauchy's inequality gives
$$E_j\ge\sum_\lambda a_{j,\lambda}^2\ge d^2/q.$$
Using (3.5),
$$\boxed{S\ge\frac{\exp(d/(2q))}{e^2d^2},\qquad d=m\lfloor k/2\rfloor.} \tag{3.6}$$
At balance this is $\exp(\Omega(n/q))/n^2$. For every fixed $q$ the bound is exponential, and for $q=n^\eta$ with fixed $\eta<1$ it is stretched exponential (when that many levels are available). If $q\le d/(10\log d)$, it already gives the polynomial bound $S\ge e^{-2}d^3=\Omega(n^3)$. These are **restricted-class** exponents, not claims for unrestricted Andreev. The full equal-magnitude theorem has the sharper exact bound $2^d$ for $q=1$; (3.6) is intended to extend its scope, not improve its constant.

The same conclusion holds under the weaker hypothesis of equal histograms only across one chosen selected/ignored division. More generally, if at most $q$ distinct magnitudes occur across those halves and
$$\sum_\lambda(a_{j,\lambda}-b_{j,\lambda})^2\le d^2/q,$$
then $\sum_\lambda a_{j,\lambda}b_{j,\lambda}\ge d^2/(2q)$ by polarization and Cauchy. The lower bound becomes $e^{-2}d^{-2}\exp(d/(4q))$. This permits imperfect spread; it still requires actual equal magnitude classes, not approximate numerical equality.

### 3.5 Scope, architecture checks, and limits [PROVED or KNOWN as specified]

- The class permits arbitrary mixed signs, arbitrary dense signed table coefficients, arbitrary real top weights, arbitrary unequal real magnitudes, and coordinate-dependent zero supports. It is not covered just by table monotonicity, one-table-bit restrictions, or a bounded common sign-run hypothesis.
- Known exact and approximate Fourier circuits violate the histogram condition: a character channel has nonzero address weights on selected blocks and zeros on ignored blocks. For the matching character $T$, the positive-magnitude and zero classes occupy opposite halves, giving $E_j=0$. Their existence is compatible with (3.4).
- UP2's two-scale character row assigns one magnitude to selected blocks and another to ignored blocks. It too has $E_j=0$ on its matching character. Finite alphabet and full support alone therefore do not imply (3.6).
- LOW2's round-two compiler makes all coefficients arbitrarily near equal by adding a large common count. It changes their exact magnitude multiplicities according to their original supports; it need not equalize block histograms. Near equality alone is refuted as an exponential lower-bound hypothesis by that compiler.
- The single-largest-class hypergeometric argument supplied by UP2 gives the weaker but elementary $\exp(d/(2q^2))$ bound. LOW2 checked the zero-class case. The permanent estimate exploits all classes simultaneously and improves the dependence to $q$ at a polynomial loss. Both share UP2's original parity restriction mechanism.
- No new unrestricted lower exponent or exhaustive novelty assertion follows. The genuinely new content in this round is a proved magnitude-multiplicity/support-overlap extension, and an explicit obstruction to the attempted survivor amplification.

### 3.6 The obstruction is an exact common-top dual [PROVED / VERIFIED]

If the right side of (3.4) is strictly below one for a proposed library, the union bound yields a single matching and sign choice for which every bottom loses a live variable. Uniform mass on that literal-restriction cube, with the fixed character table, is then a nonnegative exact dual annihilating every labelled bottom and every labelled raw affine feature. Thus the theorem supplies an exact dual with unrestricted top coefficients; it is not a normalized-margin argument.

[VERIFIED EXACT] `dual_check.py` constructs such a certificate for 32 gates on $A_{2,10}$. Every gate has magnitude histogram $(0,0,1,1,1,1,3,3,3,3)$ in each block, independently permuted and signed, with dense mixed table weights. One matching and identification-sign vector simultaneously cancel at least one live coefficient in every row. All 1,024 resulting labelled inputs have mass $1/1024$. Direct integer evaluation checks the 57 annihilation equations (32 bottoms, 24 raw inputs, and the constant). The compact certificate is `paired_dual_certificate.json`; each row's missing live coordinates make it valid for all thresholds/table normals on that direction pool, not just the displayed sample choices. This finite example illustrates the mechanism; its small parameters do not satisfy or establish the asymptotic sufficient bound.

The intermediate class is nonvacuous and not merely a renamed semantic full-sign class. For example, take two blocks each with positive coefficients $(1,1,3)$ and threshold three. Every variable is essential, yet singleton addresses of equal Hamming count receive different outputs depending on the coefficient selected. Essential positive unateness forces any equivalent full-sign threshold to use all positive signs, which would make equal-Hamming-count outputs identical. So this gate is genuinely outside the semantic full-sign class, while its block histograms agree. Conversely, full-sign point indicators already show that exponential-size circuits in the permitted class can compute arbitrary Boolean functions; the lower bound is not caused by global inexpressibility.

## 4. Peer results audited and strengthened

### 4.1 Semantic character-slab incidence [PROVED consequence; UP2 reduction]

UP2's round-two result charges the nonconstant Walsh support of each TABLE normal. For $T\ne\varnothing$, let $x_c^\pm=(1\pm\chi_T(c))/2$. Their actual top-score difference must have strict signs $\chi_T(b)$, and raw address terms cancel. If $\sum_c\alpha_{jc}\chi_T(c)=0$, bottom $j$ cancels. Each other bottom difference is a signed slab with two threshold boundaries. Fixing the address blocks outside $T$ leaves parity on $m|T|$ bits, so these boundaries must slice every cube edge. Summing over $T$ gives
$$\sum_j r_j\ge\frac12\sum_{T\ne\varnothing}\operatorname{slice}(m|T|),$$
where $r_j$ is the table normal's nonconstant Walsh support size. The slicing lower bounds and their exponents are inherited, not proved in this run. This reduction is UP2's, independently checked here and by LOW2.

[PROVED semantic refinement supplied by LOW1] Replace $r_j$ by the number $r_j^{\rm sem}$ of characters $T$ for which
$$a\longmapsto g_j(x^+,a)-g_j(x^-,a)$$
is nonconstant on the full address cube. Every constant difference can be absorbed into the difference score's constant before applying the edge test. A nonconstant difference still uses at most two boundaries. Thus the same incidence inequality holds with $r_j^{\rm sem}\le r_j$. This formulation is stable under arbitrary coefficient perturbations preserving each gate's Boolean truth table. It includes written table normals of full Walsh support when most associated slabs never change on attainable addresses. No unrestricted bound on this semantic incidence is asserted.

The bounded integer address case of the inherited slicing theorem gives $\sum_jr_j^{\rm sem}\ge kmN/(16C)$, with per-gate integer entries in $[-C,C]$. Thus bounded semantic incidence gives exponent two in a restricted class. This is an attributed refinement of UP2's new reduction, not an independent improvement to the unrestricted exponent or a new geometric slicing theorem.

### 4.2 Magnitude closeness is insufficient [PROVED check, LOW2 construction]

LOW2's compiler is correct: for any bottom $g=[L(x,a)\ge0]$, $U(a)=\sum_l a_l$, and $B>\max|L|$,
$$g=\sum_{r=0}^{M}[B(U-r)+L\ge0]-U,\qquad M=km.$$
At $U=t$, the $r<t$ summands are one, $r=t$ is $g$, and all later summands vanish. By taking $B$ additionally larger than every address coefficient's magnitude, and arbitrarily large thereafter, all new address coefficients are positive with ratio arbitrarily close to one. A known quadratic exact circuit becomes cubic, and the fixed-character parity subproblem becomes quadratic. This refutes an exponential near-equality extension. It does not force equal block histograms: the exact level distinctions still encode original supports. I checked this on the board and kept its attribution to LOW2.

### 4.3 Coupled polynomial repair still misses character tails [PROVED check, UP1 result]

UP1's edge-coupled masks make some global quadratic cross terms collapse. They do not evade the complementary-character obstruction after central truncation: if each original bottom's table-pair difference is address-constant, adding a correction of address degree $r<|T|m$ leaves a polynomial of degree less than the required parity degree. Its correlation with that parity is zero, whereas a strictly sign-correct difference has positive correlation. Thus such a correction cannot repair the channel even when granted for free. Nonlinear coupled corrections remain open; a large Walsh coefficient alone says nothing sufficient about their cost.

### 4.4 UP1's logarithmic sign-product integral [PROVED check; auxiliary observation]

For nonzero $u,v$ and positive $\lambda,t$, UP1 defines
$$K_{\lambda,t}=[u+\lambda v\ge t]+[-u-\lambda v\ge t]-[u-\lambda v\ge t]-[-u+\lambda v\ge t].$$
This is $[|u+\lambda v|\ge t]-[|u-\lambda v|\ge t]$, always zero or $\operatorname{sgn}(uv)$. The $dt/t$ integral is the log ratio of the larger and smaller magnitudes. Substituting $x=\lambda|v|/|u|$ gives
$$\int_0^\infty\!\int_0^\infty K_{\lambda,t}\frac{dt\,d\lambda}{t\lambda}=\frac{\pi^2}{2}\operatorname{sgn}(uv).$$
The identity follows by splitting at one, inverting the upper half, and integrating the positive odd-power expansion of $\log((1+x)/(1-x))$. This verifies UP1's integral, not an Andreev construction.

[PROVED auxiliary observation supplied by LOW1] If $1\le|u|,|v|\le R$, choose dyadic $\lambda$ such that $1\le\lambda|v|/|u|\le2$. The larger-to-smaller magnitude ratio is at least three, so some dyadic $t\in[1,4R]$ lies strictly above the smaller and at most the larger. A fixed $O(\log^2R)$ grid of $(\lambda,t)$ therefore has at least one nonzero $K$ for every pair, while all its nonzero terms have the correct sign. Summing gives an exact **sign-only** product score using $O(\log^2R)$ raw halfspaces. Its amplitude is not constant, so it cannot replace an arbitrary weighted product inside a shared top score. This highlights why UP1's normalized amplitude/margin issue, not isolated sign-product computability, is decisive.

## 5. Verification and peer exchange

[VERIFIED EXACT] `python3 -I verify.py` passed: 5,148 rational layer identities through $d=100$; 1,020 exhaustive compiled parity scores; 42,800 literal restrictions in 40 unequal/zero coefficient examples with exact permanent-survival counts; 6,172 zero parity correlations; 10,411 exact hypergeometric-moment bounds; all 66,064 binary Brégman instances in dimensions two through four; 60 Bernoulli-permanent averaging identities; and 653 balanced-histogram collision inequalities. Results: `verification.json`. Tests of analytic estimates are finite guardrails; the exponent follows from the written proof and the attributed Brégman theorem.

[VERIFIED EXACT] `python3 -I dual_check.py` additionally checks the 1,024-input, 32-bottom dual described in §3.6. No package installs, floating-point LP conclusions, or asymptotic extrapolation from these sizes are used.

[PROVED CHECKS / attribution] LOW2 refuted my first survivor-amplification candidate; I accepted the objection and strengthened its witness to polynomial helper cost in §2. UP2 supplied the single-class hypergeometric estimate and coordinated scope; LOW2 checked both the zero-class issue and the improved Bernoulli/Brégman proof. I checked UP2's character-slab reduction, supplied its semantic incidence refinement, checked LOW2's near-equal compiler, and checked UP1's polynomial-tail obstruction and logarithmic integral. These substantive exchanges are recorded append-only in `/tmp/andreev_gap/swarm_round2/board.md`.

## 6. Final assessment and single next step

[PROVED restricted result] The collision-energy/permanent theorem is a meaningful extension beyond round one's equal-magnitude/full-support class. It permits multiple arbitrary real magnitudes and varying zeros, provided the exact magnitude multiplicities overlap across a selected/ignored division. Equal block histograms are a clean sufficient condition, not an unstated assumption on unrestricted circuits. For $q\le d/(10\log d)$ the result gives $\Omega(n^3)$ at balance; for fixed $q$ it is exponential. This does not contradict the quadratic general upper bound, whose character channels deliberately violate the overlap condition.

[UNRESOLVED] No unrestricted exponent above $3/2$ and no exact ordinary-Andreev upper exponent below two was obtained. The supplied unrestricted gap is unchanged. Generic all-distinct address magnitudes make every cancellation matrix entry one and defeat this proof. Two-scale character-specific rows and the known exact/approximate Fourier constructions provide explicit non-generic escapes too. The semantic character-slab incidence refinement likewise needs a substantive incidence cap; dense genuine Walsh coupling is uncontrolled.

[REFUTED routes] Independent edge coverage, full transcript entropy, and separate parity feasibility remain inadequate by round one. The new survivor-amplification attempt fails even with only quadratic missing-variable helpers. Approximate magnitude equality is not exact cancellation and admits LOW2's cubic compiler. Polynomial corrections to saturated character channels cannot supply the missing parity degree. Dyadic/logarithmic sign-product witnesses do not normalize amplitudes inside a common score.

[CONJECTURE / single most promising next step] Extend the collision-energy restriction dual to a **costed tradeoff for fully dependent versus missing-variable gates** when the magnitudes are all distinct. It must retain the common top score, charge the missing-variable helpers, and permit the exact quadratic helper construction in §2. A bound using only full-survivor counts is false. LOW2's genuinely unequal oriented-rectangle certificate gives a finite exact target for such a collective dual; no scalable theorem is currently proved. This is preferable to another coverage/information relaxation or a near-equality perturbation argument.

All work stayed in LOW1's assigned round-two folder except append-only board entries. No shared paper edits, online posts, package installs, or additional subagents were used. All task-owned computations finished. New files credit Christian Reitwiessner; UP2, LOW2, UP1, Brégman, Radhakrishnan, Cutler–Radcliffe, and inherited slicing sources retain their respective mathematical attribution.

### Late peer audit: UP2's dense-helper hybrid theorem [PROVED CHECK, attributed to UP2]

UP2 subsequently proved an exponent-two obstruction for a hybrid of arbitrary dense-table full-sign equal-magnitude helpers and character-specific two-scale ladders, with ONE common signed address form per character. I audited its missing-interval embedding on the board. For a character with $d$ selected and $e$ ignored raw bits, flip its common mask so its statistic is $p+2q$ with range $0..K$, $K=d+2e$. The own-channel gates on complementary tables have at most $2E_T$ cuts. A constant interval of $3r+1$ levels contains a complete $r$-selected/$r$-ignored subcube, because the other coordinates' fixed sums fill every integer $0..K-3r$ when $d-r\ge1$ and $e-r\ge0$.

On that subcube every own-channel difference is constant, every other Walsh channel cancels, and the common top-score difference sign-computes selected parity using at most $2H$ full-sign helper restrictions. Choosing $r\ge2$ with $2^r>2H$ contradicts UP2's round-one theorem. Hence $K+1\le3r(2E_T+1)$. Summing middle characters gives $E=\Omega(MN/\log(H+2))$ for polynomial helpers, with $M=km$, thus exponent two. Arbitrary independent masks within a character would invalidate the common scalar interval; that hypothesis must be retained. This theorem belongs to UP2 and does not change LOW1's unrestricted status.
