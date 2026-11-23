Authors: Christian Reitwiessner

# Round 3 LOW1: charging full-dependence gates and helpers together

Status: completed round-three research report. No unrestricted exponent improvement.

**Strongest result [PROVED, restricted class]:** exact Andreev needs $\widetilde\Omega(n^2)$ structured gates when each gate has an individually bounded integer address normal whose absolute magnitude is constant within each block. Signs/masks, dense signed table normals, real top weights and raw top wires are unrestricted. The bound survives arbitrary pure-address helpers and polynomially many additional superincreasing address gates. Complete theorem and proof: §§3 and 4.6. The exact quadratic Fourier family gives the matching exponent. This combines LOW2's new profile isolation with LOW1's skew-baseline and magnitude-class incidence arguments, using the known Sauermann–Xu cover theorem.

**Additional result [PROVED]:** a costed monomial-support inequality charges both full-dependence gates and missing-variable helpers. Superincreasing rows plus identical-block-histogram helpers obey an exponential mixed-class tradeoff (§4). It explicitly accommodates the prior one-survivor/quadratic-helper counterexample.

All proof statuses, models, source attribution, exact guardrails and exchanges are recorded below. Early candidate entries are retained as provenance and explicitly superseded by the completed sections.

## Model and early exact constraints

The model is exact ordinary depth-two THR of THR for Andreev, with arbitrary real bottom and top weights and raw input wires at the top; $N=2^k$, $k$ blocks of $m$ bits, $km=\Theta(N)$.

**[KNOWN, preceding rounds]** Exactness includes all rare addresses and all character tables $x_c=y\oplus\langle S,c\rangle$. On these tables the output is parity of $y$ and all bits in selected blocks $S$. Full-dependence survivor counts alone cannot give amplification: one surviving full-dependence gate and quadratically many missing-variable helpers already compute exact selected parity. The helper cost and common top coefficients must therefore enter any valid argument.

**[CONJECTURE / research direction]** Seek a signed higher-difference or polynomial-annihilator constraint which charges both the full-dependence component and the lower-order correcting component, summed over table characters. A claim based only on pair coverage, transcript information, finite weight palettes, or near-equality will not be treated as a candidate.

## Work log

Initial report created before investigation; reading all required previous reports and the paper.

## 1. A candidate costed hybrid (proof being audited)

**[PROVED lemma, attribution UP2 round-three board]** A real score strictly sign-computing full $d$-bit parity has every one of its $2^d$ multilinear monomial coefficients nonzero in every complemented $0/1$ coordinate basis. The coefficient on a set $U$ is an alternating sum over its face from the chosen origin; the parity signs make every summand have the same strict sign.

**[CONJECTURE / proof under audit]** This lemma can count helpers rather than discarding them. A function depending on $s$ live variables contributes at most $2^s$ coefficients. A superincreasing threshold has, on average over complemented bases, at most $3(3/2)^d$ coefficients, by its lexicographic prefix-conjunction decomposition. Superincreasing normals appear to remain superincreasing under disjoint literal identifications.

Consequently a mixture of $F$ superincreasing raw address gates and $H$ full-support equal-magnitude gates should obey
$$H+3F\ge (4/3)^d\left(1-\frac{d+1}{2^d}\right),\qquad d=m\lfloor k/2\rfloor.$$
Both classes allow arbitrary signed dense table coefficients, thresholds, top weights and raw top wires. Unlike applying their separate lower bounds, this charges their interaction in one actual score. Complete proof, constants and a histogram extension are the next task. This is a restricted heterogeneous class, not an unrestricted exponent improvement. The face-coefficient idea and superincreasing single-class direction belong to UP2; the proposed helper accounting and hybrid are LOW1's.

## 2. New candidate exponent-two class: arbitrary masks and dense table normals

**[CONJECTURE / proof under audit; extends LOW2's round-three profile-isolation candidate]** Suppose each gate's address normal can be rescaled to integer entries in $[-C,C]$, and its absolute magnitude is constant within each address block. Signs may be arbitrary inside every block, table normals may be fully dense and signed, and top weights/raw top wires are unrestricted. For fixed $C$, the proposed lower bound is $\widetilde\Omega(n^2)$, with matching exponent from the inherited two-scale construction. There is no restriction on the number of masks.

The new ingredient is to pair two unused baseline blocks of distinct magnitude. Every baseline coefficient becomes a nonzero integer $\pm a\pm b$, regardless of the masks. If too few exceptional gates are nonconstant on a small live tree/graph cube for every baseline, their narrow integer bands would give too few hyperplanes in a skew cover. The inherited Sauermann–Xu skew-cover theorem forces a baseline making all exceptional gates constant. LOW2's random literal identifications then annihilate every other gate's full parity coefficient. Across characters, a gate can be exceptional only for unions of its block magnitude classes, yielding a bounded incidence direct sum.

Complete proof is being written. Attribution: LOW2 supplies graph-based profile isolation and the order of restrictions; LOW1 supplies skew baseline coverage (removing the mask cap at bounded integer scales) and the multi-class incidence count. The cover lower bound is known: Sauermann–Xu, *Nondegenerate hyperplane covers of the hypercube*, Theorem 1.1, https://arxiv.org/html/2507.00773v2 (primary statement inspected in this run). No unrestricted exponent or novelty priority is claimed.

## 3. Main theorem: a semantic magnitude-profile direct sum [PROVED]

This section supersedes §2's candidate status. It is an application/extension developed through the round-three exchange, not a claimed literature-priority theorem. LOW2 supplied profile isolation by selected/ignored graph restrictions; the skew-cover step and multi-class charge below are LOW1's additions. The geometric lower bound is inherited from Sauermann–Xu.

### 3.1 Model and finite statement

Let $S$ count the **structured** bottom gates. In a chosen threshold representation, each structured gate's address normal can be rescaled by a positive scalar so that
$$\gamma_{j,i,l}=\sigma_{j,i,l}a_{j,i},\qquad
 \sigma_{j,i,l}\in\{-1,1\},\qquad a_{j,i}\in\{0,\ldots,C\}.$$
Here $C\ge1$ is an integer; $a_{j,i}$ may vary arbitrarily between blocks and gates. All signs inside a block are unrestricted, with no bound on the number of masks. Every table coefficient, threshold and top coefficient is arbitrary real. Let $q_j$ be the number of distinct values among $a_{j,1},\ldots,a_{j,k}$, including zero if present.

We additionally allow arbitrary pure-address gates, arbitrary pure-table gates, raw top wires, and arbitrary extra bottom features whose restriction at each fixed table is affine in the address. Their number and weights need not be bounded. More generally, the last class can have address degree less than the retained parity dimension used below. These allowances do not create extra layers; they describe functions of the original inputs in the existing top score.

Set
$$r=\max\{2,\lceil\log_2(S+1)\rceil\},\quad
D=m-(k-1)r,\quad L_* =r\lfloor k^2/4\rfloor.$$
Assume $k\ge2$ and $D>0$. Choose one representative $T$ from each unordered nontrivial cut $\{T,T^c\}$ of the block set. There are $N/2-1$ representatives.

Define the two actual Boolean tables
$$x_{T,c}^{\pm}=\frac{1\pm\chi_T(c)}2,\qquad
\chi_T(c)=(-1)^{\sum_{i\in T}c_i}.$$
A gate is **active** for $T$ when
$$a\longmapsto g_j(x_T^+,a)-g_j(x_T^-,a)$$
is nonconstant. Write $\mathcal A_j$ for this semantic activity set. It depends only on the Boolean gate, not the chosen numerical representation.

A structured gate is **separated by $T$** when
$$\{a_{j,i}:i\in T\}\cap\{a_{j,i}:i\notin T\}=\varnothing.$$
Let $E_T$ count the structured gates both separated by $T$ and active for $T$. Exact computation implies
$$\boxed{E_T\ge\frac{D}{4(2Cr|T|(k-|T|)+1)}.} \tag{3.1}$$
Consequently
$$\boxed{
\sum_{j=1}^{S}|\{T\in\mathcal A_j:T\text{ separates }j\}|
\ge \left(\frac N2-1\right)\frac{D}{4(2CL_*+1)}.
} \tag{3.2}$$
The left side is at most $\sum_j(2^{q_j-1}-1)$, giving the explicit heterogeneous-profile charge
$$\boxed{
\sum_{j=1}^{S}(2^{q_j-1}-1)
\ge \left(\frac N2-1\right)
\frac{m-(k-1)r}{4(2Cr\lfloor k^2/4\rfloor+1)}.
} \tag{3.3}$$
No table-Walsh sparsity condition occurs. Written dense perturbations which preserve the Boolean gates cannot change the activity sets. It suffices that every structured Boolean gate admits a representation with the stated block magnitudes; fix one such representation per gate before the proof.

### 3.2 Proof: exact character difference and disjoint live coordinates

Let $F$ be the actual top score, outputting one iff $F\ge0$. On the complementary tables, exactness forces
$$\chi_T(b(a))\bigl(F(x_T^+,a)-F(x_T^-,a)\bigr)>0
\quad\text{for every raw address }a. \tag{3.4}$$
The difference is strict even if the positive-class score is zero, because the negative-class score is strictly negative. Pure-address features and raw address terms cancel. Pure-table features contribute constants. Features affine in the address after fixing the table give an affine difference. Inactive structured gates give constants and may be ignored. These conclusions hold for the one actual top coefficient vector.

Take the complete bipartite graph with vertex classes $T,T^c$. For each edge $(i,h)$ reserve $r$ distinct raw coordinates in block $i$ and $r$ in block $h$, paired across that edge. All reservations are disjoint, even for edges sharing a block. Every block needs at most $(k-1)r$ coordinates, leaving at least $D$ unused. Put
$$L=r|T|(k-|T|).$$
There are $L$ selected live coordinates and $L$ ignored live coordinates. They are kept independent for now. Their selected parity, after all other coordinates are fixed, is parity on the $L$ selected variables up to one constant sign.

For a gate which is **not** separated, some graph edge joins blocks of equal magnitude. Later, identify each ignored live bit with either its paired selected bit or its complement, independently and uniformly. In sign coordinates each paired coefficient becomes $u+tv$, $t\in\{-1,1\}$. Along the $r$ pairs of that equal-magnitude edge, a nonzero common magnitude cancels for one of the two literal choices, independently for all pairs. A zero common magnitude cancels for both choices. Therefore the probability that this gate retains all $L$ live coefficients is at most $2^{-r}$. This is independent of the table offsets and of the baseline fixing chosen next.

### 3.3 Proof: a skew cover charges exceptional gates with arbitrary masks

Choose any block $u\in T$ and any block $v\notin T$. Reserve $D$ additional unused coordinates in each as baseline coordinates. Pair these baseline coordinates with each other and set both bits in baseline pair $h$ equal to a variable $z_h\in\{0,1\}$. These variables parameterize a choice of **fixed** baseline; they are not part of the eventual parity cube. Set every other unreserved raw address bit to zero.

For any separated gate, $a_{j,u}\ne a_{j,v}$. Its coefficient on baseline variable $z_h$, after that gate's positive rescaling, is
$$c_{j,h}=\sigma_{j,u,h}a_{j,u}+\sigma_{j,v,h}a_{j,v}\in\mathbb Z\setminus\{0\}. \tag{3.5}$$
Thus its baseline form has full support for every choice of its signs, without a common-mask hypothesis. The distinct **absolute** magnitudes rule out cancellation, including when one is zero.

At either fixed table, the gate has form
$$[c_j\cdot z+R_j(y,w)\ge\theta_j^{\pm}],$$
where $R_j$ is the contribution of the $2L$ independent live coordinates. Its live range width is
$$W_j=\max R_j-\min R_j
       =\sum_{\text{live coordinates}}|\gamma_{j,i,l}|
       \le2CL.$$
For a baseline $z$, this gate can be nonconstant on the live cube only if
$$\theta_j^{\pm}-\max R_j\le c_j\cdot z
 <\theta_j^{\pm}-\min R_j. \tag{3.6}$$
The interval has length $W_j\le2CL$. Since $c_j\cdot z$ is integer, this bad set is contained in at most $2CL+1$ level hyperplanes $c_j\cdot z=h$. Every such hyperplane has a nonzero coefficient on every one of the $D$ baseline coordinates.

If every baseline left some active separated gate nonconstant at one of the two tables, these at most $2E_T(2CL+1)$ hyperplanes would cover the whole $D$-cube. They would form a **skew cover**. The known skew-cover bound, a special case of Sauermann–Xu Theorem 1.1, requires at least $D/2$ hyperplanes. Hence
$$2E_T(2CL+1)\ge D/2,$$
which is exactly (3.1).

For completeness, why a cover must exist in a correct circuit: if it did not, choose an uncovered baseline. Every active separated gate is now constant on the entire live cube at both tables. Independently choose the live literal-identification signs. The probability that any of the at most $S$ remaining structured gates retains all live coordinates is at most
$$S2^{-r}<1.$$
Thus some simultaneous choice makes every nonseparated gate miss a live variable, at both table offsets. Inactive differences and separated differences are constants. Extra affine-after-table features have address degree at most one after substitution. Since $L\ge2$, every term of the actual difference score has zero uniform correlation with full live parity. Equation (3.4) requires this correlation to have a strict nonzero sign. Contradiction.

This is why the discarded helpers are not assumed costless: their entire number determines $r$, and a single restriction annihilates all of them only **after** the skew-cover charge has made every exceptional gate individually constant. No slicing lower bound is applied solely to fully dependent survivors.

### 3.4 Proof: direct sum over magnitude classes

For a fixed gate, partition the $k$ blocks by their equal absolute magnitudes. A cut separates its magnitude sets exactly when each of its $q_j$ classes lies entirely on one side. There are $2^{q_j}-2$ nontrivial oriented choices, hence $2^{q_j-1}-1$ unordered cuts. Semantic activity can only reduce that count. Sum (3.1) over the $N/2-1$ representatives and use $L\le L_*$. This proves (3.2)–(3.3).

This is an aggregate constraint on one exact circuit, with heterogeneous profiles and dense signed table paths. It is not a claim that independent pair coverage or independent top decoders suffice for computation.

### 3.5 Exponents and two-level sharpening

**[PROVED]** Suppose $q_j\le q$ and $S<N^2$. Then $r\le2k+1$. For sufficiently large balanced instances, $D\ge m/2$ and the preceding theorem gives
$$\boxed{S=\Omega\!\left(\frac{n^2}{C(2^{q-1}-1)\log^4 n}\right),\qquad q\ge2.} \tag{3.7}$$
If $S\ge N^2$, the same lower conclusion is automatic in its relevant parameter range. Fixed $C$ implies $q\le C+1$, so the exponent is **two**, with arbitrary signs and unlimited masks. More generally, if $q$ is fixed and $C=n^\delta$, this proves exponent $2-\delta$ up to logarithms; it exceeds $3/2$ for every fixed $\delta<1/2$. This is a restricted coefficient/profile class, not an unrestricted improvement.

For at most two distinct block magnitudes, replace the complete bipartite graph by a connected bipartite spanning tree. Any nonseparated two-color profile has an equal-magnitude edge: otherwise it is a proper two-coloring of a connected tree and equals $T$ or $T^c$. Now $L=(k-1)r$ and a two-level gate is separated by at most one unordered cut. Thus
$$\boxed{S\ge\left(\frac N2-1\right)
\frac{m-(k-1)r}{4(2C(k-1)r+1)},} \tag{3.8}$$
which yields
$$S=\Omega(n^2/(C\log^3n)).$$
One-level rows are nonseparated for every nontrivial cut and contribute zero to the incidence charge. Zero is a legitimate second level. Pure-table rows never contribute.

The supplied exact Walsh construction with blockwise magnitudes $0,1$, or UP2's round-two full-support magnitudes $1,2$, belongs to these classes and has $O(n^2)$ gates. Their masks may be arbitrary. Hence the fixed-$C$ class has matching **exponent two**; the statement is not literal $\Theta(n^2)$ without logarithms.

### 3.6 Limits, exact dual, and attribution

**[PROVED scope]** The theorem permits genuinely dense semantic Walsh activity and unrestricted real top cancellation. It removes the round-two Walsh-support bound and LOW2's round-three mask cap, at the price of commensurable bounded integer address magnitudes. It does not cover arbitrary magnitudes within a block or arbitrary large/incommensurable relative scales. Those are substantive restrictions. Numerical near equality alone still gives no cancellation or short integer-level cover.

If the bound fails for a fixed circuit, the construction gives a concrete nonnegative exact dual: take uniform mass on the two complementary character tables and on the retained live cube, with the baseline and literals fixed as above. The output signs are opposite between the tables and alternate with live parity. Every labelled bottom, raw input and constant has zero expectation, whereas a strict correct score would have positive expectation. Pairing any positive-parity live vertex with a negative-parity one expresses this dual as a positive mixture of oriented four-input rectangles. Thus the proof supplies a common-top certificate, not transcript entropy or coverage alone.

**[KNOWN source]** The only imported geometric theorem is the lower bound $D/2$ for a skew hyperplane cover of the Boolean $D$-cube, from [Sauermann–Xu, *Nondegenerate hyperplane covers of the hypercube*, Theorem 1.1](https://arxiv.org/html/2507.00773v2). Its primary statement was read. Its proof is not claimed here. LOW2's round-three graph profile isolation is essential ancestry. The new contribution in this report is pairing the unused baseline coordinates to create a skew cover independent of mask count, then summing over a gate's magnitude classes.

## 4. A costed survivor/helper inequality and an exponential mixed class [PROVED]

This section supersedes §1's candidate status. It answers the charging part of the mission for a rigorously specified heterogeneous class. It does not supply a general quadratic-helper lower bound.

### 4.1 Exact monomial budget, including missing-variable gates

**[KNOWN elementary parity sparsity; rederived and introduced in this round by UP2]** Let a real score $P$ have strict sign $\varepsilon(-1)^{|z|}$ on the $d$-cube, $\varepsilon\in\{-1,1\}$. In the coordinate basis $u_i=z_i\oplus b_i$, its unique multilinear polynomial has coefficient
$$c_{b,U}=\sum_{V\subseteq U}(-1)^{|U|-|V|}P(b\oplus1_V).$$
Every summand has sign $\varepsilon(-1)^{|b|+|U|}$. Hence every one of the $2^d$ coefficients is nonzero, for **every** complemented basis $b$. This is a face-difference consequence of exact signs, not a lower bound on a normalized margin. Classical parity sparsity is discussed and reproved in Basu–Bhatnagar–Gopalan–Lipton, [*Polynomials that Sign Represent Parity and Descartes' Rule of Signs*](https://arxiv.org/html/math/0702773); that primary paper was inspected. No novelty is claimed for this ingredient.

For a bottom function $h$ on the live cube, define its semantic budget
$$\mathcal M(h)=2^{-d}\,\mathbb E_b\bigl[\#\{U:c_{b,U}(h)\ne0\}\bigr].$$
If $P$ is an affine raw score plus a weighted sum of bottoms $h_j$, then the support of its polynomial is contained in the union of those supports and the at most $d+1$ affine positions. Therefore
$$\boxed{1-\frac{d+1}{2^d}\le\sum_j\mathcal M(h_j).} \tag{4.1}$$
This remains true after averaging any family of legal literal restrictions which preserve full live parity. Crucially, a bottom missing variables contributes to the right side. If it semantically depends on at most $s$ live coordinates,
$$\mathcal M(h)\le2^{s-d}. \tag{4.2}$$
For a missing-one helper this is $1/2$, not zero. Arbitrarily large top weights cannot create new monomial positions. The exact coefficient-sign system is stronger than the support-count consequence (4.1), but (4.1) is already useful in the mixed class below.

### 4.2 Superincreasing gates survive identifications but have small budget

A nonzero address normal is superincreasing if its nonzero absolute coefficients, in decreasing order $w_1,\ldots,w_p$, satisfy
$$w_i>\sum_{h>i}w_h\quad\text{for every }i.$$
Orders, supports and signs may vary by gate. Magnitudes may be arbitrary real, including irrational. All table coefficients and thresholds are unrestricted.

**[PROVED, independently checked by UP2 and LOW2]** This property survives arbitrary disjoint signed literal identifications and fixing of coordinates. For a merged group whose largest original coefficient is $w_i$, its new absolute coefficient is at least $w_i$ minus the other magnitudes in its group. Superincrease makes this strictly larger than the sum of all original magnitudes in later merged groups, hence than the sum of their new absolute coefficients. Order merged groups by their earliest original nonzero position. Zero groups may be discarded. This proves superincrease of the remaining normal, without comparing table thresholds.

After complementing input signs, a threshold on such a normal is a lexicographic comparison. Its accepted set has a disjoint prefix-conjunction expansion with at most one conjunction of each width $1,\ldots,p$, plus a possible constant. To see the precise count, choose its least accepted binary word in lex order. If it has trailing zeroes, truncate at its last one. Accepted words either first exceed it at a zero position before that last one, or have its complete truncated prefix. These are disjoint and have different widths. Constant gates require no such expansion.

A conjunction of $t$ literals expands into $2^v$ monomials in a complemented basis, where $v$ of its literals are negative in that basis. Under uniform basis complementation $v\sim\operatorname{Bin}(t,1/2)$, so its expected support is $(3/2)^t$. Hence every superincreasing threshold on at most $d$ live variables has
$$\mathcal M(h)\le3(3/4)^d. \tag{4.3}$$
The deliberately loose constant also covers constant gates. This step uses the **exact** prefix expansion before the common top combination, not replacement by a merely sign-equivalent feature. UP2 supplied the lexicographic direction and the complemented-basis calculation; the restriction-stable helper application is the present report's use of them.

### 4.3 Averaged helper budget is a soft permanent

Fix a middle character selecting $\lfloor k/2\rfloor$ blocks. If $k$ is odd, fix one other block to zero. There remain $d=m\lfloor k/2\rfloor$ selected signs $z$ and $d$ ignored signs $w$. Take a uniform perfect matching $\pi$ between the halves, followed by independent literal signs $t_i$, and identify $w_{\pi(i)}=t_i z_i$.

For an arbitrary helper $j$ with selected coefficients $u_{j,i}$ and ignored coefficients $v_{j,l}$, define
$$B^{(j)}_{il}=\mathbb E_{t\in\{-1,1\}}
  2^{-\mathbf1\{u_{j,i}+tv_{j,l}=0\}}.
$$
Thus its entries are $1/2$ for two zeros, $3/4$ for equal nonzero magnitudes, and $1$ otherwise. If $s_j(\pi,t)$ is the number of nonzero merged coefficients, then
$$\mathbb E_{\pi,t}2^{s_j-d}=\frac{\operatorname{per}B^{(j)}}{d!}. \tag{4.4}$$
Indeed $2^{s_j-d}$ is the product of a factor $1/2$ for every missing merged variable and a factor one for every nonzero one. Average the independent literal signs and then the permutation. Actual semantic support may be smaller, making (4.4) an upper bound on its semantic budget. This addresses threshold-induced inactivity as well as syntactic coefficient cancellation.

Let $a_{j,\lambda}$ and $b_{j,\lambda}$ count occurrences of magnitude $\lambda$ in the two halves, and put
$$E_j=2a_{j,0}b_{j,0}+\sum_{\lambda>0}a_{j,\lambda}b_{j,\lambda}.$$
Then $\sum_{i,l}(1-B^{(j)}_{il})=E_j/4$. The round-two soft-permanent estimate gives
$$\frac{\operatorname{per}B^{(j)}}{d!}
\le\min\{1,e^2d^2\exp(-E_j/(4d))\}. \tag{4.5}$$
**[KNOWN ingredient / attribution]** That estimate is proved in LOW1 round-two §3.2 using Brégman's permanent inequality. For a matrix $B\in[0,1]^{d\times d}$, randomize independent Bernoulli entries with means $B$, apply Brégman, use independent row sums and $(r!)^{1/r}\le(r+2\log d+2)/e$, then divide by $d!\ge(d/e)^d$. It yields $\operatorname{per}B/d!\le e^2d^2\exp[-\sum(1-B_{il})/d]$. The current change is the helper-budget matrix, not a new permanent theorem.

### 4.4 The mixed-class tradeoff

Suppose $F$ bottom gates have superincreasing address normals, while $H$ other bottoms are arbitrary helpers. All bottom gates, including pure-address ones, must be included in these groups; arbitrary pure-table gates contribute only a constant after fixing the character table. For $d\ge2$, (4.1)–(4.4) prove
$$\boxed{
1-\frac{d+1}{2^d}\le
3F(3/4)^d+
\sum_{j\in H}\frac{\operatorname{per}B^{(j)}}{d!}.
} \tag{4.6}$$
One may replace each permanent by the expected **semantic** budget of the actual restricted helper for a sharper truth-table-invariant version. This is a charge on fully dependent lexicographic gates and partially dependent helpers together.

If every helper is full-support equal-magnitude, its number of nonzero merged coefficients is binomial $(d,1/2)$, so its budget upper bound is exactly $(3/4)^d$. Consequently
$$\boxed{H+3F\ge(4/3)^d\left(1-\frac{d+1}{2^d}\right).} \tag{4.7}$$
The union of the two classes therefore has an exponential lower bound at balance. The individual exponential theorems did not imply this union statement: generic superincreasing rows have no equal-magnitude cancellation and make the old full-survivor covering bound vacuous. Missing-variable helpers could in principle correct their scores; (4.6) explicitly charges those corrections.

More generally, if each helper has identical absolute-coefficient histograms in every block, with at most $q$ levels including zero, then $E_j\ge d^2/q$. Hence
$$\boxed{
H\ge e^{-2}d^{-2}e^{d/(4q)}
\left(1-\frac{d+1}{2^d}-3F(3/4)^d\right)_+.
} \tag{4.8}$$
For polynomially many superincreasing gates and fixed $q$, exponentially many histogram helpers are necessary. This is a heterogeneous extension beyond round two's requirement that **every** gate have overlapping histograms. For unrestricted all-distinct helper magnitudes, $E_j=0$ may hold and the charge becomes vacuous; no unrestricted exponent follows.

A complementary-table variant allows arbitrary pure-address gates for free: they cancel in the actual score difference. A superincreasing gate contributes a difference of two lexicographic thresholds, doubling the factor 3 to 6; an arbitrary helper difference still depends on at most $s_j$ merged variables and keeps the same $2^{s_j-d}$ bound. The same conclusions follow with $6F$ instead of $3F$, while arbitrary table-only and affine-after-table terms occupy at most the same $d+1$ positions.

### 4.5 Mandatory counterexample audit and limits

**[KNOWN, LOW1 round two, originating with LOW2's monomial witness]** For $s=\sum_i z_i$,
$$(-1)^s=\sum_{i=1}^d f(s-z_i)+(-1)^d2^d[s=d],$$
where
$$f(r)=\frac{(-1)^r}{d\binom{d-1}{r}}\sum_{u=0}^{r}\binom du.$$
Every $f(s-z_i)$ uses $d-1$ threshold cuts omitting variable $i$. The last AND is the sole fully dependent gate. The total helper count is $d(d-1)$.

This identity is fully compatible with (4.6): each helper can contribute $1/2$ of the normalized monomial budget, giving a total upper budget $d(d-1)/2$, not zero. The theorem does not assert that this example is optimal. It does not establish a universal $\Omega(d^2)$ helper requirement, and does not reduce a general fully dependent threshold to a corner gate.

**[PROVED guardrail, supplied by UP2]** If the sole full-dependent gate is an AND of one literal per variable, at least $d$ helpers omitting exactly one variable are needed for $d\ge3$, with every omission represented. Choose the basis making the AND the monomial $z_1\cdots z_d$. Each degree-$(d-1)$ coefficient of the strict parity score is nonzero; neither the full AND nor a helper missing two variables nor raw affine terms contribute there. The coefficient on $[d]\setminus\{i\}$ therefore requires a helper omitting exactly $i$. This is only linear, and its attribution is UP2.

**[REFUTED as a general inference; UP1 stress test]** The exponentially large normalization of the full AND coefficient is not universal. A central majority has full parity correlation of order $d^{-1/2}$ in the appropriate parity dimension, and a quadratic missing-coordinate correction can be built for that survivor as well. Thus the initial corner-amplitude thought cannot imply a general helper-size bound. Top variation and gate count remain distinct resources.

### 4.6 Combined theorem: superincreasing helpers do not lower the profile exponent [PROVED]

The preceding two mechanisms combine into a stronger costed hybrid. Let $S$ structured gates satisfy §3's bounded integer, blockwise constant-magnitude hypothesis. Permit $F$ additional gates with arbitrary superincreasing address normals, arbitrary signs/supports, and unrestricted dense table normals. Also permit the free pure-address, pure-table and affine-after-table features of §3. Set
$$r=\left\lceil\log_{4/3}\bigl(16(S+6F+1)\bigr)\right\rceil,
\qquad D=m-(k-1)r>0.$$
The same inequalities (3.1)–(3.3) hold, counting only the $S$ structured gates, with this new value of $r$. For two-level structured gates the tree version (3.8) holds.

**Proof.** Fix a cut and its complete bipartite graph as in §3, with $L=r|T|(k-|T|)\ge r$. If (3.1) failed, the same skew-cover argument would supply a baseline making every semantically active separated structured gate constant at both tables. Every other structured gate either has a constant table difference, or has $r$ equal-magnitude live pairs on some graph edge.

Average the subsequent literal signs and complemented live-coordinate bases. For each such nonseparated structured gate, its difference depends on at most the number $s$ of nonzero merged coefficients, and
$$\mathbb E\mathcal M(g_j^+-g_j^-)
 \le\mathbb E2^{s-L}\le(3/4)^r.$$
Each equal nonzero pair contributes $3/4$, each zero-zero pair contributes $1/2$, and every other pair contributes at most one. The pairs are disjoint, so their literal choices are independent. This is a cost on missing-variable helpers, not their removal.

Every superincreasing gate remains superincreasing after the restriction. Its two fixed-table versions contribute expected normalized monomial support at most $6(3/4)^L$, by (4.3) and a union bound on their supports. Pure-address features cancel; the remaining free affine features occupy at most $L+1$ monomial positions. Exact sign correctness of the actual common difference score therefore requires
$$1-\frac{L+1}{2^L}
\le S(3/4)^r+6F(3/4)^L
\le(S+6F)(3/4)^r<\frac1{16}.$$
But $r\ge10$ and $L\ge r$, so the left side exceeds $1/2$. Contradiction. The class-incidence direct sum is unchanged. $\square$

In particular, for fixed $C$ and polynomial $S+F$, the structured gates still require exponent **two**, despite polynomially many arbitrary irrational-scale superincreasing helpers. For fixed $q$ and $C=n^\delta$, the same $2-\delta$ restricted exponent follows. The conclusion is about the union class and cannot be obtained by quoting the two separate class lower bounds.

There is also an explicit positive-dual interpretation. If the expected union of all feature supports plus affine positions is smaller than $2^L$, some literal restriction and basis have a missing monomial $U$ of degree at least two. Its alternating coefficient is an exact zero for every table-difference feature. Uniform mass on that origin face and the two complementary character tables, with their actual target signs, annihilates every allowed bottom and raw feature. Exactness would make the average signed score positive. This is a polynomial/helper cancellation certificate on a face, and can again be expressed as a positive mixture of oriented rectangles.

## 5. Verification and substantive exchanges

### 5.1 Exact guardrails [VERIFIED]

Run

```bash
python3 -I /tmp/andreev_gap/swarm_round3/low1/verify.py
```

The standard-library script uses integers and rational arithmetic and writes `verification.json`. It passed:

- 109,200 strict-parity face-coefficient checks in complemented bases;
- 4,340 superincreasing disjoint-pair identifications;
- 536 complete threshold-offset averaged monomial-support checks;
- 59,920 exact helper restriction cases checking the soft-permanent identity;
- 164,682 magnitude-class/cut incidence cases;
- 750 complete-graph cancellation-product cases;
- 8,712 integer bad-baseline band cases, with endpoint ties;
- 525 prior quadratic-helper layer identities and compatibility checks.

These validate algebra and edge cases. The asymptotic conclusions rest on the written proofs and the cited cover theorem, not extrapolation. No packages were installed and no shared-paper files were edited.

### 5.2 Exchanges and attribution [PROVED CHECKS where specified]

I posted the helper-charging target before proposing a theorem. UP1 supplied the central-majority warning: an AND's tiny full Fourier coefficient cannot be treated as universal. UP2 supplied the compulsory omission-type observation and introduced the complemented-basis face-coefficient route; its source search identified classical parity sparsity and the stronger known threshold-of-conjunctions bound. My exponential hybrid uses the weaker support calculation deliberately because it permits a quantitative missing-variable helper budget. UP2 and LOW2 independently checked its superincreasing-identification step and the soft matrix entries $1/2,3/4,1$.

LOW2 proposed graph-based address-profile isolation with dense table normals. I checked the connected-tree coloring step, disjoint allocation, literal-sign survival bound, and its two-baseline extension to arbitrary real scale ratios and one zero scale. I then supplied the paired-baseline skew-cover replacement, removing the mask cap at bounded integer scales, and the complete-bipartite multi-class incidence extension. The final proof includes the factor-two cost for complementary table comparisons, allowing arbitrary pure-address helpers. The semantic activity refinement counts only actual nonconstant differences.

I also independently checked UP1's continuous-domain constant-amplitude obstruction: grouped opposite orientations on a common boundary line have contributions $A[t\ge0]+B[t\le0]$; equal target values on both sides and on the boundary force $A=B=0$. Its convex-hull midpoint argument is valid for $R>3$. This is explicitly not a finite-integer-grid lower bound. I checked UP1's exact four-direction telescoping constraint and matching clipped-ramp witness, establishing optimal amplitude distortion $\lfloor(R+1)/2\rfloor$ in that specified ridge class. Neither result is asserted as an Andreev exponent change.

LOW2/UP1 separately develop a real-two-level bound with a sign-mask resource. Their two-baseline/random-prefix approach trades dependence on that resource against arbitrary real magnitudes. The bounded-integer/unlimited-mask theorem here is complementary, with different hypotheses; it does not silently import a general real-scale estimate.

## 6. Dead ends, final status, and next step

**[REFUTED specified routes]** A survivor-only demand greater than one remains false. The exact quadratic-helper identity is rechecked and explicitly charged here. An AND's corner-amplitude burden is not a universal threshold-gate burden. Near-equality and a finite palette without a spread/profile condition do not imply exponential hardness. Pair coverage and transcript entropy alone do not enforce a shared top. Integer narrow-band hyperplane counts cannot be extended to irrational scales merely by numerical approximation: attainable values and threshold ties may change, and rescaling may make $C$ enormous.

**[PROVED strongest result]** Dense semantic table coupling and unlimited address sign masks still require exponent two when every structured address row has a bounded integer magnitude constant within each block. The finite semantic charge is (3.1)–(3.3); two levels give (3.8). Polynomially many arbitrary superincreasing helpers do not remove this bound (§4.6). Full table and top weights remain unrestricted real, and the proof gives a positive common-score certificate. This is a new restricted-class application within the investigation, with LOW2's profile isolation and the inherited skew-cover theorem explicitly credited.

**[PROVED additional costed class]** A mixture of superincreasing rows and identical-block-histogram helpers has the explicit tradeoff (4.8), exponential for fixed helper palette and polynomially many superincreasing rows. Unlike the preceding permanent covering inequality, it counts the partially dependent helpers' polynomial contribution as well.

**[UNRESOLVED]** No unrestricted $n^{3/2+\varepsilon}$ lower bound, no unrestricted $n^{2-\varepsilon}$ upper bound, and no universal quadratic-helper lower bound was proved. Arbitrary within-block heterogeneous real magnitudes still evade the decisive profile/collision charge. The unrestricted exponent gap is unchanged.

**[CONJECTURE / best next step]** Extend the profile-isolation/skew-baseline mechanism to rows with genuinely heterogeneous magnitude distributions **within** each block. The concrete missing statement is a common disjoint pairing, or a positive face-dual replacement, that charges rows with cross-cut magnitude overlap without assigning one coordinate per gate. It must simultaneously handle exceptional separated rows and retain a quantitative helper budget. The proved bounded-integer block-uniform class supplies a matched quadratic benchmark; the new superincreasing hybrid supplies a stress test against simply adding collision-free arithmetic helpers. Removing only a constant or logarithmic loss is not the objective.

All new files credit Christian Reitwiessner. No additional agents, shared-paper edits, online posts or package installations were made. All owned computations completed.

### Final independent-audit update

**[PROVED CHECKS, attributed to peers]** LOW2 read §3's complete proof and independently inspected the primary cover theorem. It checked the nonzero paired baseline coefficients, real table-offset treatment, two-table hyperplane count, disjoint coordinate reservations, exact class-union count, and semantic-activity restriction; it found no gap. UP2 independently checked the same bounded-palette mechanism and explicitly flagged the factor-two/free-pure-address scope distinction, which is incorporated in (3.1). Both peers also checked the helper soft matrix and superincreasing-identification lemma. These are substantive peer audits, not formal verification or exhaustive novelty certification.

**[PROVED CHECK, final hybrid audit attributed to LOW2]** LOW2 additionally checked §4.6: each superincreasing mixed gate contributes two lex expansions (factor six), while a nonseparated table difference is a function on one common surviving support and therefore needs no extra factor two in its $2^s$ support bound. Raw-address and arbitrary pure-address terms cancel; the affine budget is safe. Replacing $\log S$ by $\log(S+F)$ preserves the exponent for polynomial $F$. The final exact dual uses a missing face coefficient, not an assertion that all helpers have zero full-cube Fourier coefficient before that face is chosen.
