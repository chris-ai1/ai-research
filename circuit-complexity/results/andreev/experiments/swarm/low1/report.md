# LOW1: table differences beyond one table bit

Authors: Christian Reitwiessner

Date: 2026-11-11. Research agent LOW1, OpenAI Astra. Saved immediately on restart and updated after each major idea. No subagents; no shared-paper edits.

## Outcome

**No unrestricted lower-bound exponent improvement was obtained.** The strongest result of this run is a proved limitation of the proposed slicing extension: a family of $O(n^{3/2})$ dense signed-majority gates passes every table-pair/ordinary-address-edge nonconstancy test simultaneously, and has full joint table-transcript entropy on every address subcube. With $\widetilde O(n^{3/2})$ gates the same holds for the usual repeated-coordinate parity cubes. These libraries are not claimed to compute Andreev. The complete proofs are in §3, with independent checks from UP1 (ordinary-edge probability) and LOW2 (multi-coordinate extension).

A separate $\widetilde O(N)$ ladder library even sign-represents each two-bit-swap parity problem independently, for every background, yet fails a four-point joint-score certificate (§2). Standard higher derivatives have no forced sign, and almost-all-edge slicing has an elementary square-root upper bound (§1). Thus shared top-score orientation, rather than independent pair feasibility or transcript entropy, is the most promising remaining target. LOW2 supplied an exact finite positive-dependence certificate. In a late advance, UP2 proved an asymptotic radial dual for separated full-sign dictionaries; combining it with our coverage theorem gives pools that pass all these relaxations yet provably have no correct top weights (§6). The unrestricted extension remains open.

## Mission and baseline

Seek an exponent above $3/2$ for unrestricted exact depth-two threshold circuits for ordinary Andreev, using table differences and hypercube slicing. All raw inputs may enter the top gate. At balance, $N=2^k$, $km=\Theta(N)$, and $n=\Theta(N)$.

**[KNOWN, supplied reports]** One-table-bit circuits satisfy $S\ge (N/4)\operatorname{slice}(m)=\widetilde\Omega(n^{32/19})$. A gate reading $t$ table bits gives the immediate factor-$t$ loss; this is not a new result. Exact unrestricted bounds remain $\widetilde\Omega(n^{3/2})$ and $O(n^2)$, while constant-error upper bounds have exponent $3/2$.

**[KNOWN, corrected review]** Drift conclusions require a full eligible block with all magnitudes comparable to the gate's global maximum address weight. Non-drifting can be vacuous. No argument below assumes unrestricted gates are zero-sum or eligible.

## Reading and protocol

Read `swarm/COMMON.md`, the corrected `review_coherence/report.md`, the relevant complete proofs in `one_table_bit/report.md`, the exact/truncated staircase sections of the shared paper, and primary slicing sources. Read and appended to the board throughout. Candidates were posted before their final proof status; superseded entries were corrected by append-only replies. All authored artifacts credit Christian Reitwiessner and retain mathematical source attribution.

## Required adversarial checks

Each proposed capacity estimate must be tested against: (i) random signed address weights with one table bit; (ii) random signed address weights with dense table weights; (iii) Fourier/staircase gates from the exact quadratic construction; (iv) truncated staircase gates of the exponent-$3/2$ average-case construction. Any successful unrestricted argument must explain where it needs correctness on rare inputs.

## 1. Higher-order differences and almost-all slicing

### 1.1 Standard higher derivatives do not inherit a forced sign [PROVED / REFUTED route]

Let $F_0(x,a)=2x_{b(a)}-1$. This is an exact signed score for Andreev. For each fixed address it is affine in the table variables; hence every order-$d\ge2$ mixed discrete derivative in distinct table coordinates is zero. Such a score is realizable by a finite depth-two threshold circuit: for every full Boolean input with output one, use a bottom gate isolating that point, then take twice their sum minus one. Efficiency is irrelevant to a counterexample to a consequence of exactness alone.

More generally, for a fixed address and a finite signed combination $L(F)=\sum_x\lambda_xF(x,a)$, exact correctness by itself forces $L(F)>0$ for all strict correct scores precisely when every nonzero $\lambda_x$ has the same sign as $2x_{b(a)}-1$ (with at least one nonzero coefficient). If a coefficient has the wrong sign, increase the magnitude of the score at that single input to dominate the finite sum. Arbitrary positive margins at the finitely many inputs are implementable by weighted point-indicator bottoms. Standard higher alternating derivatives do not satisfy this condition: after fixing the selected table bit, their signs still alternate along another differentiated bit.

This does not refute clever higher-order certificates using other information about the circuit. It refutes obtaining their forced parity sign from exactness alone, as in the first-order pair proof. It survives all four adversarial families because it is a logical obstruction before any gate capacity estimate; in particular the exact affine lookup score already kills the inference.

### 1.2 Almost-all-edge slicing cannot improve the exponent [KNOWN, Klein; elementary proof supplied]

An edge of $\{0,1\}^m$ can be sampled by choosing its direction uniformly and the other $m-1$ bits uniformly. Its lower endpoint has Hamming weight $R\sim\operatorname{Bin}(m-1,1/2)$. The plane $\sum_i z_i=r+1/2$ slices every edge of layer $r$. Taking all integer layers within $t$ of $(m-1)/2$ therefore uses at most $2t+2$ hyperplanes and leaves at most $2\exp(-2t^2/(m-1))$ of all edges unsliced. Thus

$$O\!\left(\sqrt{m\log(2/\delta)}+1\right)$$

planes slice a $1-\delta$ fraction. For $\delta=m^{-C}$ this is $\widetilde O(\sqrt m)$, so no robust all-but-inverse-polynomial-edge theorem can require $m^{1/2+\varepsilon}$. Even $\delta=\exp(-m^\eta)$ only forces the construction's exponent to $(1+\eta)/2$.

The middle-layer example is explicitly in Klein's proof overview: [*Slicing all Edges of an n-cube Requires n^(2/3) Hyperplanes*](https://arxiv.org/abs/2212.03328). The stronger exact slicing theorem of [Sauermann–Xu](https://arxiv.org/html/2510.16592v1) was checked at its primary statement. A targeted literature search found no almost-all variant that evades this elementary obstruction; no exhaustive novelty claim is made.

**Family checks.** Random signed address normals just complement coordinates in the layer example; it remains valid. Adding one or many table coefficients only shifts the selected layers after fixing a table. The exact staircase construction pays for all attained layers, whereas truncated staircases omit the extreme layers. Therefore the rare-input issue is essential and explicit, not an artifact of a weak proof. A density-only approximate-cancellation argument is insufficient.

## 2. A cheap library meeting all two-bit-swap parity demands [PROVED]

This is a barrier to a specified relaxation, not to all table-difference arguments. It appears stronger than the supplied marginal-survival barrier: the library passes exact parity realizability for every individual two-bit swap and background. No literature priority is claimed.

Choose arbitrary signs $\sigma_{ij}\in\{\pm1\}$, including independent random signs. Define

$$Q_i(x)=\sum_{c:c_i=1}x_c,\qquad L_i(a_i)=\sum_{j=1}^m\sigma_{ij}a_{ij}.$$

Write $p_i$ and $q_i$ for the positive and negative sign counts, so the attained values of $L_i$ are every integer from $-q_i$ to $p_i$. Include the gates

$$g_{i,r}(x,a)=[Q_i(x)+L_i(a_i)\ge r],\qquad -q_i+1\le r\le N/2+p_i.$$

There are exactly $N/2+m$ gates per block, thus

$$S=k(N/2+m)=\widetilde O(N)\quad\text{at balance}.$$

### 2.1 Every required local parity problem is feasible

Fix $c_i=0$, $d=c\oplus e_i$, and any assignment $y$ to all other table bits. Let $x^0$ have $(x_c,x_d)=(1,0)$ and $x^1$ have $(0,1)$, with common background $y$. Put $h=\sum_{e\notin\{c,d\}:e_i=1}y_e$, so $0\le h\le N/2-1$. For every integer cut $r$,

$$g_{i,r}(x^1,a)-g_{i,r}(x^0,a)
=[h+1+L_i(a_i)\ge r]-[h+L_i(a_i)\ge r]
=[L_i(a_i)=r-h-1].$$

All attained levels occur: for $\ell\in[-q_i,p_i]$, the cut $r=h+\ell+1$ lies in the specified ladder. Consequently

$$\sum_r(-1)^{r-h-1}\bigl(g_{i,r}(x^1,a)-g_{i,r}(x^0,a)\bigr)
=(-1)^{L_i(a_i)}=(-1)^{|a_i|}.$$

This is an exact parity score, with no raw live-address term, for every background $y$ and every fixing of the other blocks. Therefore every swap difference separately has both (a) edge coverage and (b) a feasible top parity representation using this library. The top coefficients in this display depend on $h$; the assertion does not give one simultaneous top gate. Taking the negatives if required matches either orientation of the actual target pair.

The same construction also handles an arbitrary distinct label pair under the repeated-coordinate restriction from one_table_bit §3: choose a block $i$ where the labels differ, substitute the same live $m$ bits in all differing blocks with the prescribed complements, and use ladder $i$ alone.

### 2.2 The library cannot compute Andreev, even with arbitrary free raw top wires

For $k\ge2$, use the four labels $00,01,10,11$ in two coordinates, with the remaining coordinates zero. Let $x$ have ones at $00,11$ and let $x'$ have ones at $01,10$. Then $Q_i(x)=Q_i(x')$ for every $i$. Every bottom gate therefore agrees on $x,x'$ at every address. Their top-score difference is the constant raw-table contribution $u\cdot(x-x')$.

At an address with label $00$, correctness would force that constant strictly positive; at label $01$ it would force it strictly negative. Contradiction. Equivalently, place weight $1/4$ on the four inputs $(x,a),(x',a),(x,a'),(x',a')$ for parity labels $00,01$: their output signs are $+,-,-,+$. This signed distribution annihilates every bottom feature, every raw input, and the constant, giving an exact four-point separation certificate.

Thus a successful unrestricted argument must enforce simultaneous top coefficients, or employ table differences beyond isolated swaps. Merely imposing all two-bit-swap parity lower bounds separately cannot yield even the already known unrestricted $n^{3/2}$ bound.

### 2.3 Stress tests and exactness

* Random signed address weights with one table bit: the known one-table-bit direct sum still holds; the counterlibrary is outside that model, and its density is precisely what allows sharing.
* Random signed address weights with dense table weights: the counterlibrary has dense $0,1$ table normals and arbitrary/random $\pm1$ address normals. A version using sufficiently many random sign table rows and full ladders also supplies geometric coverage, but is not needed for this theorem.
* Exact quadratic Fourier/staircase gates: these also use dense table forms and full ladders. Their actual common top score supplies the consistency absent from this counterlibrary.
* Truncated exponent-$3/2$ gates: truncating the ladders loses the exact identity at extreme attained levels. The counterlibrary deliberately pays for those rare levels, yet still costs only $\widetilde O(N)$ because it has just $k$ directions. Passing local exact demands is therefore substantially weaker than global correctness.

## 3. An exponent-$3/2$ barrier for simultaneous table-pair edge coverage [PROVED]

### 3.1 Statement and scope

Let there be $N$ table bits and $D\ge2$ address bits, $n=N+D$. There exists a family of $R=O(n^{3/2})$ threshold gates with **dense $\pm1$ table and address normals** such that for every two distinct tables $x,x'$ and every ordinary edge $(a,a')$ of the full $D$-dimensional address cube, at least one gate satisfies

$$g_j(x,a)-g_j(x',a)\ne g_j(x,a')-g_j(x',a'). \tag{3.1}$$

In particular, every adaptive table pair, every fixing of other address blocks, and every surviving ordinary address subcube passes the necessary edge-slicing test. This includes all rare tables and extreme addresses. It is a simultaneous existence theorem for a feature library, **not** a circuit computing Andreev, and it does not assert parity sign-realizability with fixed or even independently chosen top weights. It does not cover arbitrary affine substitutions whose edges flip many raw address coordinates; see §3.5.

Consequently, no lower bound above $n^{3/2}$ follows from the relaxation consisting solely of all conditions (3.1). This is narrower than a barrier to the entire table-difference method: common oriented top weights are discarded by this relaxation, and may still provide a stronger argument.

### 3.2 One random gate distinguishes a rectangle with probability $\Omega(n^{-1/2})$

Use signed input coordinates and choose all coefficients $\epsilon_c,\eta_l$ independently and uniformly in $\{\pm1\}$:

$$g(x,a)=\left[\sum_c\epsilon_c(2x_c-1)+\sum_l\eta_l(2a_l-1)\ge0\right].$$

In ordinary bit coordinates, divide the inequality by two: all input coefficients are still $\pm1$, and the threshold is an allowed real number. Fix distinct $x,x'$ at table Hamming distance $h$, $1\le h\le N$, and an address edge in coordinate $l$. Absorb the fixed input signs into the random coefficients. Let $M=n-1$, let $S$ be the sum of the $M$ random signs other than the edge coefficient, and let $B$ be the sum of the $h$ signs corresponding to the changed table coordinates. At the second table the sum excluding the edge coordinate is $S'=S-2B$.

The gate changes along the edge at table $x$ precisely when

$$S=t,\qquad t=\begin{cases}0,&M\text{ even},\\-1,&M\text{ odd}.\end{cases}$$

The same gate changes in the same edge orientation at table $x'$ precisely when $S'=t$. Thus (3.1) holds whenever $S=t$ and $B\ne0$. In fact its exact probability is

$$2\Pr(S=t)\bigl(1-\Pr(B=0\mid S=t)\bigr). \tag{3.2}$$

This follows because the two single-crossing events are disjoint and have equal probabilities by swapping the tables.

### 3.3 Elementary conditional anti-concentration

Here $h\le N\le M-1$, since $D\ge2$. If $h$ is odd, $B$ cannot vanish. If $h$ is even, direct counting gives

$$p_{M,h}:=\Pr(B=0\mid S=t)
=\frac{\binom h{h/2}\binom{M-h}{(M-h+t)/2}}
{\binom M{(M+t)/2}}\le\frac23. \tag{3.3}$$

For completeness, the uniform bound follows without a limit theorem. With $q=M-h$, the ratio of successive even-$h$ terms is

$$\frac{p_{M,h+2}}{p_{M,h}}=
\begin{cases}
\dfrac{(h+1)q}{(h+2)(q-1)},&M\text{ even},\\[4pt]
\dfrac{(h+1)(q+1)}{(h+2)q},&M\text{ odd}.
\end{cases}$$

In each case the ratio is at most one up to the center and at least one afterwards; hence the maximum occurs at an endpoint of the allowed even-$h$ interval. For even $M\ge4$, both endpoints $h=2,M-2$ give $M/[2(M-1)]\le2/3$. For odd $M\ge3$, endpoints $h=2,M-1$ give $(M+1)/(2M)\le2/3$. The case $M=2$ has only odd $h$ and probability zero.

Finally $\Pr(S=t)=2^{-M}\binom M{(M+t)/2}=\Theta(M^{-1/2})$ by the central-binomial estimate. Equations (3.2)–(3.3) prove a uniform lower bound $c/\sqrt n$ for an absolute $c>0$.

The hypothesis $D\ge2$ matters. If all other coordinates are flipped table coordinates, the centered odd-majority symmetry can make the rectangle difference vanish identically; that degenerate case was not silently included.

### 3.4 Union bound and stress tests

There are fewer than

$$D\,2^{2N+D-1}$$

choices of ordered distinct table pair and address edge. For $R$ independent gates, the chance a fixed rectangle has no witness is at most $\exp(-cR/\sqrt n)$. With $R=\lceil Cn^{3/2}\rceil$ and sufficiently large absolute $C$, a union bound makes the probability of any failure less than one. Duplicated gates, if any, may be removed without harming coverage. This proves the theorem.

**Required stress tests.**

1. One-table-bit signed random gates: the proof fails exactly where it should. If the table pair avoids a gate's table bit, $B=0$ deterministically. The known one-table-bit direct sum is not contradicted.
2. Dense random table and signed address gates: these are the actual counterfamily. All weights have the same magnitude, so there is no hidden large-weight or ineligible-block loophole.
3. The exact quadratic construction: its actual top coefficients imply the requisite oriented inequalities where correctness forces opposite signs. Our cheaper library only satisfies the un-oriented nonzero condition and need not share any of those top coefficients.
4. Truncated exponent-$3/2$ gates: the theorem is stronger than average-case edge coverage—its union bound covers **all** inputs and ordinary edges. Thus simply asking an edge-coverage relaxation to include rare inputs still does not force an improved exponent. Exactness must be used in a stronger way, such as one common orientation of all rectangle inequalities.

This is distinct from the inherited random-restriction survival barrier: the relaxation here explicitly quantifies over every table pair and every address edge at once. It still does not bar all cross-cube arguments or all correctness-dependent per-gate measures.

### 3.5 Remaining gap and strongest next target

For a four-input rectangle on which the target signs are $+,-,-,+$, exactness implies the **oriented** inequality

$$\sum_j v_j\bigl(g_j(x,a)-g_j(x',a)-g_j(x,a')+g_j(x',a')\bigr)>0.$$

Every raw affine top feature cancels. The same vector $v$ must satisfy this for all such rectangles. Condition (3.1) merely says each row of this system is nonzero. The natural next step is an exact positive dependence among these oriented rows for the random dense dictionary, then a theorem extending that obstruction to every smaller dictionary. This dovetails with LOW2's common-top cone certificate; no such general theorem is claimed here.

One could also use nonstandard address cubes obtained by repeated/complemented raw coordinates. Their edges may flip several raw coordinates at once; the statement proved here is explicitly for ordinary edges. Whether those enlarged tests add anything above the same exponent is investigated separately rather than assumed.

### 3.6 Extension to bounded multi-coordinate address changes [PROVED]

The ordinary-edge theorem extends to all address pairs at Hamming distance $1\le\ell\le L<D$ with

$$R=O(n^{3/2}\sqrt L).$$

For each gate independently choose a bias type $\delta\in\{0,1\}$ with equal probability. With $\delta=0$, use no bias; with $\delta=1$, add one independent random sign to the signed majority score. All raw input normals remain dense $\pm1$. Fix a rectangle whose table distance is $h\ge1$ and whose address distance is $\ell<D$. The bias type making $M=n-\ell+\delta$ even has probability $1/2$.

Let $C$ be the sum of the $\ell$ flipped-address coefficient signs, after absorbing the original inputs; let $S$ be the sum on all remaining inputs plus the possible bias; and let $B$ be the sum of the $h$ flipped-table signs included in $S$. The four scores before thresholding are

$$S+C,\quad S-2B+C,\quad S-C,\quad S-2B-C.$$

The random variables $C$ and $(S,B)$ are independent. Choose $c=1$ if $\ell$ is odd and $c=2$ if $\ell$ is even. Then $\Pr(C=c)=\Omega(\ell^{-1/2})$. Also $\Pr(S=0)=\Omega(n^{-1/2})$. Conditional on $S=0$, the law of $B$ is symmetric, and §3.3 gives $\Pr(B=0\mid S=0)\le2/3$, because $h\le N\le M-1$ (at least one unchanged address coordinate remains).

On $S=0,C=1,B\ne0$, the gate changes between the two addresses at the first table and not at the second. On $S=0,C=2,B<0$, the first-table gate values are $1,0$, whereas both second-table values are $1$ (including the possible zero endpoint, since the convention is $[\cdot\ge0]$). Thus in both parity cases a sufficient event has probability at least

$$\frac12\Pr(C=c)\Pr(S=0)\frac{1-\Pr(B=0\mid S=0)}2
=\Omega((n\ell)^{-1/2}).$$

There are fewer than $2^{2n}$ possible rectangles even without using the distance bound. A union bound with $R=Cn^{3/2}\sqrt L$ therefore proves simultaneous coverage.

At $L=k=\Theta(\log n)$ this gives $\widetilde O(n^{3/2})$ gates. It covers the usual repeated/complemented-coordinate $m$-cubes for arbitrary label pairs: each such cube edge changes at most one coordinate per address block, hence at most $k$ raw address coordinates. The threshold convention and bias parity are essential details, not informal continuous approximations. Exact binomial enumeration checked 364 $(n,h,\ell)$ instances through $n=14$ against the displayed sufficient-event probability.

Thus the exponent-$3/2$ barrier also applies to the relaxation obtained by imposing all those standard multi-block table-pair slicing tests. It still does not impose a common oriented top score. Arbitrary substitutions with a cube edge changing a polynomial number of raw coordinates are outside this $L=O(\log n)$ consequence.

### 3.7 Joint transcript entropy is already maximal [PROVED]

The simultaneous coverage theorem also blocks a simple attempt to combine slicing with stronger information accounting. Fix any address subcube containing an edge. For each gate and table $x$, record its truth vector on that cube, merging the two constant truth vectors into one symbol $Z_j(x)$, exactly as in the corrected coherence review.

The map $x\mapsto(Z_1(x),\ldots,Z_R(x))$ is injective. Indeed, if two distinct tables had the same joint symbols, then for every gate either their nonconstant truth vectors would be identical, or both vectors would be constant. In either case the difference of gate values between the two tables would be constant across the cube. This contradicts (3.1) on any cube edge.

Thus, under a uniform independent table,

$$H(Z_1,\ldots,Z_R)=N,\qquad\sum_jH(Z_j)\ge N.$$

This holds simultaneously for every ordinary address subcube. The bounded-multi-coordinate extension proves the same conclusion for all standard repeated-coordinate cubes whose edges change at most $k$ raw bits, with $R=\widetilde O(n^{3/2})$.

A preliminary board entry derived only marginal entropy using binomial point masses and a separate union bound. The injectivity proof above supersedes it and is strictly stronger. No claim is made that such transcripts admit a common linear-threshold decoder. Their information content and their decodability by the circuit's one actual top gate are different requirements.

## 4. Other candidate routes: precise limits and exchanges

### 4.1 Reachable-cut pigeonhole counting [REFUTED as a standalone inference]

If a gate has at most $q$ possible restricted truth patterns as its table input varies, the naive joint-pattern upper bound is $q^S$. Comparing this with $2^N$ forces a collision only when $S\log_2q<N$. This condition is already false far below $S=n^{3/2}$. Restriction to a chain, with $q\le m+2$, does not rescue that arithmetic. A small per-gate range does not force useful simultaneous collisions at the target circuit sizes.

Even $N$ dense-weight gates can have an injective joint table-response map. Fix a live raw bit $z$ and $0<\epsilon<1/(4N)$, and use

$$g_c(x,z)=[2x_c+z+\epsilon\sum_{d\ne c}x_d\ge1/2].$$

For $x_c=0$, its response is $z$; for $x_c=1$, it is the constant one. The joint restricted response identifies every table. The small dense coefficients are semantically redundant, which is exactly why a useful definition must use reachable-cut patterns, not equality of written coefficients. UP1 independently emphasized that arbitrary tiny distinct perturbations preserve a preselected finite gate truth table while destroying exact coefficient equalities.

The random dense library of §3 goes further: no choice of two distinct tables can cancel every relevant gate on even one address edge, while still passing the strongest transcript entropy equality. Any adaptive-pair argument must use additional structure of a *correct common top score*, not pigeonhole counting alone.

### 4.2 LOW2's dense monotone-table reduction [CHECKED, attributed to LOW2]

LOW2 proposed and proved a restricted extension that does retain the $32/19$ exponent with arbitrarily dense table normals. After orienting all nonzero top coefficients positive, assume all table coefficients and raw top table coefficients are nonnegative. If a bottom row has table mass $A$, it has at most one coordinate $d$ with $\alpha_d>A/2$. Its positive complementary-singleton difference is a slab private to $d$; when that slab fires, all other complementary-singleton differences are $-1$. With nonnegative top coefficients and direct table terms, these private slabs produce nonnegative dominating selector kernels. The inherited one-table-bit slicing reduction then applies, giving $\widetilde\Omega(n^{32/19})$, or $\widetilde\Omega(n^2)$ for bounded integer address normals.

I checked the endpoint inequalities and posted the check: for any nonowner $c$, firing of the owner slab implies

$$\alpha_c\le A-\alpha_d<T\le\alpha_d\le A-\alpha_c.$$

This is a valid restricted-model extension, not an unrestricted result or my independent theorem. Details are in `/tmp/andreev_gap/swarm/low2/report.md` §4. The sign restrictions cannot be silently removed: arbitrary dense signed table rows can contribute positively to many labels, and the truncated Fourier construction violates the required path signs after orienting its top coefficients.

### 4.3 Checks of upper-agent candidates [PROVED CHECKS, not LOW1 constructions]

* UP1's Bang-type mask rounding: maximizing a signed combination of masks gives a suitable fractional cube point; a vertex of the affine slice preserving $R$ forms has at most $R$ fractional coordinates. Nearest-endpoint rounding changes each sign-mask form by at most $R$. I confirmed this step on the board. The resulting $M/R-R$ lower correlation is an obstruction to guaranteed mask coverage, not to arbitrary score compensation.
* UP2's low-dimensional table feature count: after simultaneously strictifying bottoms on the finite input set, the table feature space has a bounded number of arrangement cells. Within one cell the free raw table contribution is a single common scalar, so output vectors form a chain as that scalar varies. I confirmed that raw top wires do not invalidate the count. Its refined middle-layer antichain bound is in UP2's report.
* UP1's sparse-table score has the claimed promise margin: empirical Walsh bias at most $1/(3h)$ gives at most $q/3$ score on a zero selected bit and at least $2q/3$ on a one selected bit, when $|x|\le h$. Its raw-product identity is valid. It remains a promise construction, and dense central table layers are not handled by this observation.

### 4.4 Exact-layer guarding is possible without adding depth [PROVED elementary compiler]

In response to UP1's composition question, let $U$ be a raw affine form and choose $B>\max_{x,a}|U(x,a)-\theta|$. For any integer table Hamming layer $t$,

$$[|x|=t]\,[U\ge\theta]
=[U+B(|x|-t)\ge\theta]-[|x|\ge t+1].$$

For $|x|<t$ both terms on the right are zero; for $|x|>t$ both are one; at layer $t$ the first is the original gate and the second zero. The second gate is shared by every term in a given guarded score. Raw affine terms can be guarded by treating each raw bit as a threshold, costing $O(n)$ additional gates; constants use a difference of the two adjacent table-layer cuts. Therefore a score valid on one exact layer, with $S$ bottoms, has a zero-extension with $S+O(n)$ bottoms at the same depth.

This compiler does **not** make a whole interval guard cheap: using it on every layer $0\le t\le h$ costs $O(h(S+n))$. Nor does it supply useful central-layer scores. It resolves a narrow composition issue and gives no unrestricted exponent gain. It works for all four gate stress families because it is an exact raw-affine identity with a finite-domain choice of $B$, not a statistical approximation. Exactness outside the layer comes from literal cancellation of the two thresholds.

### 4.5 Concrete responses from the other agents

**[VERIFIED EXACT FINITE, LOW2]** In response to the request following §3, LOW2 found an exact positive dependence among 56 oriented rectangle rows in a 64-gate dense signed $A_{2,2}$ pool. Every individual forced-sign rectangle row is nonzero, yet their positive rational combination is the zero vector. This rules out all common top coefficients for that pool. The certificate is in `/tmp/andreev_gap/swarm/low2/oriented_certificate.json`; its proof and exact verification are in LOW2's report §5.1. It demonstrates that the proposed next invariant is strictly stronger than coverage. It is not an asymptotic lower bound.

**[PROVED architecture obstruction, UP1]** UP1 strengthened the character-table attack to the entire central-window bottom library with arbitrary free top coefficients. On complementary character tables $\xi=\pm\chi_T$, the $T$-channel table form is $\pm N$ and all other Walsh forms are zero. If $W<N-\lceil |T|m/2\rceil$, all $T$-channel window gates are constants on each table and every other gate agrees between tables. Therefore the complete top-score difference is address-independent, contradicting the forced parity sign. This is exactly the kind of rare-table collision that a specific proposed upper library can fail, despite the existence of the unrelated random library in §3. More address masks alone cannot repair that central-window library.

## 5. Reproducibility, final status, and next step

**[VERIFIED]** Run `python3 -I /tmp/andreev_gap/swarm/low1/verify.py`. The standard-library-only checker verifies:

* 7,140 exact hypergeometric inequalities through $M=120$;
* the exact single-edge rectangle probability by full random-normal enumeration through $n=12$;
* 364 multi-coordinate rectangle cases through $n=14$ by exact binomial enumeration;
* 9,548 exact ladder identities;
* all 3,840 distinct-table-pair/address-edge rectangles for a fixed 128-gate $A_{2,2}$ feature pool, with at least 20 witnesses per rectangle;
* the four-point dual against the ladder gates and every raw affine feature.

The results are saved in `verification.json`. These are sanity checks of the formulas and finite examples, not substitutes for the asymptotic hand proofs. All task-owned commands have finished; no external posting, shared-paper edit, or additional subagent was used.

**Strongest own result [PROVED]:** $O(n^{3/2})$ gates suffice for the simultaneous all-table-pair ordinary-edge slicing relaxation; $\widetilde O(n^{3/2})$ suffice for the standard repeated-coordinate version. Both also satisfy full joint table-transcript distinguishability. This is a method limitation, not an Andreev circuit and not an improvement of the known unrestricted lower bound.

**Restricted-model progress learned from the board [PROVED by LOW2, checked here]:** the $\widetilde\Omega(n^{32/19})$ lower bound extends to dense table-monotone circuits with the explicitly stated nonnegative paths; the slicing exponent itself is inherited. No unrestricted monotonicity normalization is valid.

**Dead ends:** scalar-equality pigeonholes become vacuous at the target size; higher standard derivatives need not have any sign; density-only robust slicing stops at the square-root scale; separate pairwise parity feasibility and even joint transcript entropy do not enforce one common top score. The random-library theorem covers rare inputs exactly, so omitting rare inputs is not its loophole.

**Single most promising next step:** prove a scalable exact positive dependence among the forced-sign rectangle rows for every sufficiently small valid bottom library, or first for a broad dense mixed-sign class. This retains one common top vector and annihilates all raw affine features. LOW2's finite certificate proves the mechanism can reject pools that pass every individual coverage test; the missing ingredient is an asymptotic theorem handling arbitrary normals, thresholds, and ill-conditioning. No such theorem is asserted here.

## 6. Late board advance: asymptotically infeasible pools passing all our tests

### 6.1 UP2's exact radial-kernel dual [PROVED by UP2; independently checked here]

After the initial handoff, UP2 completed a stronger exact obstruction in `up2/report.md` §5. I read and checked that proof, including its pointwise bound, all-threshold annihilation, antipodal signs, and threshold ties. Let $D$ be even, $d=D/2$, and let $R$ sign address directions have pairwise Hamming distance in $[D/4,3D/4]$, with $R3^{-D/16}\le1/8$. Then no score in the span of arbitrary radial functions about those directions and affine raw inputs can sign-compute a prescribed degree-$d$ parity.

The proof uses

$$\kappa_\sigma(a)=\binom Dd^{-1}\sum_{|U|=d}\chi_U(\sigma)\chi_U(a).$$

Its value at distance $t$ is zero for odd $t$, and $(-1)^{t/2}\binom{D/2}{t/2}/\binom Dt$ for even $t$. It has magnitude at most $1/(D-1)$ away from the two endpoints, and exponentially small magnitude at fractional distances. The matrix $K_{ij}=\kappa_{\sigma_j}(\sigma_i)$ is exponentially close to the identity. Solve $Kc=(f(\sigma_i))_i$ for the target parity $f$, and put $P=\sum_jc_j\kappa_{\sigma_j}$. Projective separation implies $P=f$ at centers and antipodes, while $|P|<1$ everywhere else.

The nonnegative nonzero measure $\mu(a)=2^{-D}(1-f(a)P(a))$ then annihilates every label-signed radial function: if $h$ is radial about $\sigma_i$, its degree-$d$ Fourier coefficients are a common scalar times $\chi_U(\sigma_i)$, and therefore $\langle f,h\rangle=\langle P,h\rangle$. Affine terms vanish as $d\ge2$. A strict correct score would have positive integral against $\mu f$, contradicting annihilation. Strictification handles the ordinary threshold convention. The measure is initially unnormalized; I flagged this detail and UP2's written proof now states it explicitly.

The theorem allows unlimited thresholds per direction, arbitrary table coefficients chosen after the directions, and arbitrary real top coefficients. For Andreev with even $k$, fix a character table on $k/2$ blocks. It is a restricted-library obstruction, not an unrestricted lower bound. Extreme thresholds do not evade it, but deliberate geometric clustering, unequal magnitudes, or missing address coordinates are not excluded.

### 6.2 Combined separation theorem [PROVED consequence of §3 and UP2]

On the balanced even-$k$ subsequence, there exist $\widetilde O(n^{3/2})$ dense signed threshold libraries which simultaneously:

1. pass all table-pair slicing conditions on ordinary and standard repeated-coordinate address cubes;
2. have joint merged-constant transcript entropy exactly $N$ on every such cube;
3. admit **no** common top weights computing Andreev.

Indeed, draw the library from §3.6 with a sufficiently large constant. The rectangle union bound succeeds with probability $1-\exp(-\Omega(n))$. Independently of whether the two events are correlated, a union bound for the random address directions gives projective separation with probability at least $1-R^2e^{-D/8}$. Polynomial $R$ satisfies UP2's deterministic size condition. Therefore both events occur in the same draw for sufficiently large parameters. The exact dual rejects this pool despite its geometric and information properties. The same separation applies at $O(n^{3/2})$ when only ordinary address edges are required.

This is the strongest combined conclusion available at the end of the run. It makes the role of the common top gate explicit at asymptotic scale, extending LOW2's finite cone examples. The nonfeasibility theorem and radial construction belong to UP2; the all-pair coverage and transcript conclusions are LOW1's. No claim of a new unrestricted circuit exponent follows.

**Updated next-step assessment.** Exact oriented-score certificates are now more than a finite proof of principle: UP2's certificate works for polynomial separated full-sign dictionaries. Extending such a positive dual to arbitrary magnitudes and deliberately clustered directions, while retaining table-dependent structure, is the most promising next step. It remains open in this run.
