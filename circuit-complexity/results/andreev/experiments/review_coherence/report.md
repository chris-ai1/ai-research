# Independent adversarial review of coherence_fable

Authors: Christian Reitwiessner

Date: 2026-11-09. Reviewer: Astra; independent work, without subagents.

Scope: ordinary $A_{k,m}$, $N=2^k$ independent table bits, $k$ parity-address blocks of $m$ raw bits, arbitrary real threshold weights, direct raw top inputs allowed. $S$ counts bottom gates. The asymptotic balanced regime means $km=\Theta(N)$; literal $km=N$ with integral equal blocks exists only on a subsequence (e.g. $k$ a power of two). No claim below needs equality beyond constant factors. No shared paper was edited and nothing was posted online.

Sources read: `/tmp/andreev_gap/coherence_fable/report.md` and its scripts/logs; `mixed_sign/report.md`, `review_lower/report.md`, and the requested `research_backup/docs/RESEARCH_STATE.md` and `threshold_paper/paper.tex`. Original source labels such as PROVED are not evidence of correctness. This report was saved incrementally and the requested review is complete. **PROOF** denotes an argument checked here; **COMPUTATION** denotes a finite check, not an asymptotic proof; **REFUTATION** is an explicit contradiction; **CONJECTURE/UNRESOLVED** is not a theorem.

## Review outcome

The drift estimate survives independent scrutiny under its exact global-comparability hypothesis. The structural theorem is repairable but does not reduce arbitrary-weight circuits to genuine zero-sum gates, supersede the earlier unrestricted mixed-sign hybrid, or imply a coherent lower bound. The marginal-entropy barrier survives; its claimed universal limitation on methods does not.

The most consequential additional correction is that modern hypercube slicing already implies $\widetilde\Omega(M^{13/19})$ for exact parity, including direct top inputs. Comparing two single-one table scores then proves $\mathrm{size}_{\mathcal T_1}(A)\ge (N/4)\operatorname{slice}(m)=\widetilde\Omega(n^{32/19})$ for the report's one-table-bit class. Its proposed restricted exponent-$3/2$ target is therefore already reachable from known literature. This is not an unrestricted Andreev improvement. See §8 for the complete model-preserving proof and §9 for primary attribution.

| Source claim | Verdict | Essential qualification/correction |
|---|---|---|
| Lemma 4.1, drift split bound | **Correct asymptotically** | Full nonzero block globally comparable to the largest address weight; random arrangements essential. |
| Theorem 4.2, many low-drift gates | **Fixable gap** | Repair entropy-to-split demand; conclusion concerns only eligible blocks and can be vacuous elsewhere. |
| “Nearly zero-sum supersedes all previous mixed-sign structure” | **Wrong** | No control on arbitrary-weight/sparse blocks; no coherent conversion. |
| Theorem 2.1, main entropy inequality | **Correct** | Inactive constants may be merged into the top threshold. |
| Theorem 2.1 auxiliary activity bounds | **Fixable gap** | Reverse the half-open endpoint convention; repair the image-cardinality inequality. |
| Lemma 3.0 and Theorem 3.1, simultaneous random feature family | **Correct at balance** | Union bound works; does not produce a computing circuit. |
| Universal barrier for every bounded per-gate charge | **Wrong** | Only the stated marginal-entropy/split relaxation is met; correctness-dependent demands can reject it. |
| $\mathrm{size}(A_{1,m})=\mathrm{par}(m+1)$ | **Correct** | Uses raw top inputs and arbitrary real weights. |
| Fixed-$k\ge2$ equivalence / balanced parity nonimplication | **Unproved as stated** | Only one direction is supplied; include $k=1$ and the normal-form implication changes. |
| “Best exact parity lower bound is $\Omega(\sqrt M)$” | **Wrong/outdated** | Known slicing yields $\widetilde\Omega(M^{13/19})$ in this model. |
| Proposition 5.1, numerical-range staircase count | **Wrong** | Attainable values can have gaps; corrected dedicated-ladder bound is $\Omega(M)$. |
| Proposition 6.1, affine/dominance characterization | **Correct with offset constraint** | Actual $c(a)$ must be in its interval; free centering costs at most a constant factor. |
| §6.2, beating $n^{3/2}$ for one-table-bit gates is open | **Wrong as a claimed frontier** | The score-difference matching argument gives $\widetilde\Omega(n^{32/19})$. |
| §5.4, same gates useful under every arrangement | **Not proved** | Interchanges population and arrangement quantifiers. |

## 1. Drift Lemma 4.1 — correct asymptotically under its actual hypotheses

**Verdict: CORRECT for the stated global-comparability hypothesis and random restriction; FIXABLE presentation issues in exact constants and interpretations.** Independent adversarial computations are recorded in §10.

Write $G=\max_{i,l}|\gamma_{i,l}|>0$. The required block $i$ satisfies

$$G/W\le |\gamma_{i,l}|\le G\quad\text{for EVERY }l,\qquad \delta=|\sum_l\gamma_{i,l}|/(mG)\ge2/m.$$

This excludes zeros in that block, not just small nonzero coefficients. $G$ is the maximum across **all address blocks**. A block with local max/min ratio $W$ whose whole scale is much smaller than another block is not covered. For the structural conclusion $W$ must be fixed (or explicitly at most $n^{o(1)}$); its polynomial growth cannot be suppressed in $n^{-\varepsilon+o(1)}$. There is no restriction on table coefficients because the result is uniform in the fixed table and hence in the resulting threshold.

**PROOF (independent reconstruction).** Choose independent uniform permutations in the blocks and a uniform cube $c\in\{0,\ldots,m-1\}^k$. Conditional on live coordinate $\ell$ in block $i$, $c_i$ remains uniform and its preceding set $F$ is uniform among sets of that size. For every particular $T\subseteq[m]\setminus\{\ell\}$,

$$\Pr(F=T\mid\ell)=\frac1{m\binom{m-1}{|T|}}=\int_0^1q^{|T|}(1-q)^{m-1-|T|}\,dq.$$

Thus the beta-mixture representation is exact: draw $q\sim U[0,1]$, then include each nonlive bit independently with probability $q$. It is not a uniform raw-address restriction and is not valid for a fixed adversarial arrangement.

Condition on the other blocks and $\ell$. Splitting is the event $\Phi_q\in J$ for a half-open interval $J$ of length $R\le kG$, with $\Phi_q=\sum_{l\ne\ell}\gamma_{i,l}\xi_l$. Its drift $D'=\sum_{l\ne\ell}\gamma_{i,l}$ has $|D'|\ge\delta mG-G\ge\delta mG/2$; reflect signs if needed. Kolmogorov–Rogozin at scale $G/(2W)$, followed by a cover of $J$, gives

$$\Pr(\Phi_q\in J)\le\frac{C(2kW+1)}{\sqrt{(m-1)\min(q,1-q)}}.$$

Bernstein's inequality gives probability at most $2/m$ whenever $\operatorname{dist}(qD',J)\ge u(q)$, with

$$u(q)=2G\sqrt{(m-1)q(1-q)\ln m}+2G\ln m.$$

The remaining set $Q$ is contained in

$$|q-q_0|<a+b\sqrt{q(1-q)},\qquad a\le\frac{2(k+2\ln m)}{\delta m},\quad b\le\frac{4\sqrt{\ln m}}{\delta\sqrt m}.$$

Here is a simpler endpoint-safe justification of the integration step. On $q\le1/2$, put $r=\sqrt q$. All admissible $r$ satisfy $|r^2-q_0|<a+br$. For any two such points $r>s$, subtraction implies

$$(r-s-b)(r+s)<2a.$$

Since $r+s\ge r-s$, their diameter is at most $b+\sqrt{2a}$. Consequently $\int_{Q\cap[0,1/2]}q^{-1/2}\,dq\le2b+2\sqrt{2a}$. Use $r=\sqrt{1-q}$ for the other half. This also handles $q_0$ outside $[0,1]$; no invalid square root of a negative quadratic discriminant is needed. Integrating yields

$$p(g)\le O\!\left(\frac{kW}{m}\left[\frac{\sqrt{\ln m}}{\delta}+\sqrt{\frac{k+\ln m}{\delta}}\right]\right)+\frac2m.$$

This is the claimed asymptotic drift bound. The displayed numerical coefficient $8C_{KR}$ in the source is not derived literally by its stated substitutions (an additional $\sqrt2$ is then said to be absorbed into a supposedly fixed constant); use an unspecified absolute constant. This is irrelevant to the requested exponent question.

**Interpretation limits.** In the balanced regime $k=\Theta(\log n)$ this is $\widetilde O(k/(\delta m))$ for bounded $W$. With unrestricted growing $k$, the explicit $\sqrt{k/\delta}$ term must not be hidden in polylogarithmic notation. The bound is an upper bound, not a universal asymptotic equality: thresholds far outside the attainable range yield zero splitting, and zero drift does not force random-walk-like behavior. The source's $\Theta(\sqrt{k/m})$ statements describe particular signed-weight examples, not all gates. The drift lemma says nothing nontrivial when its upper bound exceeds one and says nothing at $\delta=0$.

**REFUTATION of replacing global comparability by local comparability.** Take two blocks: all $+1$ in the first, exactly half $+M$ and half $-M$ in the second, with $M>m+1$, and threshold $m+1/2$. The first block has local ratio one and local relative drift one. Nevertheless a random edge in the second block crosses between levels $0$ and $M$ with probability $\Theta(m^{-1/2})$ (the expected local time of a uniform balanced bridge); whenever it does, the whole cube splits regardless of the first prefix count. Thus local drift in the first block does not imply $\widetilde O(1/m)$ splitting. The stated lemma avoids this counterexample precisely because the first block does not have scale comparable to the global maximum.

## 2. Theorem 4.2 — a valid restricted hybrid consequence, not a universal zero-sum theorem

**Verdict: FIXABLE GAP in the derivation; CORRECT with the precise eligible-block quantifier below. The unrestricted zero-sum interpretation is WRONG.**

A block is **eligible at $W$** precisely when all its $m$ coefficients have magnitudes in $[G/W,G]$, with $G$ the gate's global address maximum. Non-drifting means

$$\forall i\text{ eligible at }W:\quad |\sum_l\gamma_{i,l}|<\delta_0mG.$$

It does NOT mean every block with bounded *local* max/min ratio. It does NOT imply that every block is eligible, or even that any block is eligible. A gate with a zero in every block, or with one very large and many much smaller coefficients in each block, can be non-drifting vacuously even when its signed sums are large relative to its local $\ell_1$ masses. The all-zero address case is inert and should be removed. Being outside the drifting class is not equivalent to being a random-walk gate.

**PROOF (repaired demand and table-reading conclusion).** Let $J$ index table-reading gates and $T_c=\sum_{j\in J}p_j^c$, where $p_j^c$ is actual nonconstancy probability over the uniform table on cube $c$. The corrected entropy theorem (reviewed in §3 below) and concavity of binary entropy imply

$$N-\log_2(N+1)\le\sum_{j\in J}[h(p_j^c)+kp_j^c]
\le S h(T_c/S)+kT_c
\le T_c\log_2(eS/T_c)+kT_c.$$

For $S\le N^2$ and sufficiently large $N=2^k$, this forces $T_c\ge N/(4k)$: when $T_c\le1$ the right side is only $O(k)$; when $T_c>1$ it is at most $(3k+\log_2 e)T_c$. Thus averaging over independent uniform arrangements and cubes gives

$$\sum_{j\in J}p_j\ge N/(4k).$$

This is the missing step. Entropy is not bounded pointwise by $k$ times the probability of splitting: the activity indicator itself can carry $h(p)$ bits. Nor does entropy directly prove the source's literal $N/(3k)$ bound without lower-order corrections. Pure-address gates contribute zero entropy even if they split, so doing the averaging over $J$ is essential to the claimed **table-reading** conclusion.

In the balanced regime Lemma 4.1 gives a uniform bound

$$p_j\le \frac{C k^{3/2}W\sqrt{\ln m}}{\delta_0m}+2/m$$

for drifting gates; coherent gates have $p_j\le k/m$. Choose a sufficiently large absolute $K$ and

$$\delta_0=Kk^{5/2}W\sqrt{\ln m}\,\frac{S}{Nm}.$$

Use the known unrestricted $\widetilde\Omega(N^{3/2})$ size lower bound to ensure $\delta_0\ge2/m$, or simply replace $\delta_0$ by its maximum with $2/m$ and handle that case explicitly. For $S\le N^{2-\varepsilon}$ and fixed $W$, $\delta_0=o(1)$ and the aggregate split mass of drifting table-reading gates is at most $N/(16k)+2S/m$ after increasing $K$. The coherent mass is at most $Sk/m=o(N/k)$. Hence a constant fraction of the required $N/k$ mass comes from gates in $J$ that are BOTH noncoherent and non-drifting. The independent arbitrary-weight survival bound from `mixed_sign` Lemma 3.1 is $p_j\le k/m+O(k^{3/2}/\sqrt m)$. Therefore there are

$$\Omega(N\sqrt m/k^{5/2})=\widetilde\Omega(n^{3/2})$$

such table-reading gates. Using the upper bound on $S$ gives $\delta_0\le N^{-\varepsilon}\operatorname{polylog}(N)W$, and for $S=\widetilde O(N^{3/2})$ it gives $\delta_0mG=\widetilde O(\sqrt m)G$. These are valid only on eligible blocks. The input research state records a separate improved $O(k/\sqrt m)$ survival proof; importing it could improve logs, not the exponent, and is unnecessary here.

**Does this supersede the previous mixed-sign hybrid? No, not as an unrestricted structural theorem.** `mixed_sign` Theorem 3.2 applies to arbitrary magnitudes, controls minority count, and forces a large noncoherent population. The new drift estimate distinguishes many gates that that run-count estimate treats poorly (e.g. fixed signed bias with a linear minority count). On an eligible block, near-zero signed sum is genuinely stronger: if $\mu$ is its minority count, then

$$\mu\ge m\frac{1-W\delta_0}{W+1},$$

by lower-bounding majority mass by $(m-\mu)G/W$ and upper-bounding minority mass by $\mu G$. This yields $\Omega(m)$ minority bits for fixed $W$ and small $\delta_0$. But on noneligible blocks there is no conclusion. The arbitrary-weight minority/run/sign-pattern statements therefore remain necessary. One can combine both charging bounds to force many gates outside the union of the small-minority and drifting classes; that is an additional hybrid argument, not supplied by the source's zero-sum slogan.

**Does it imply the coherent lower bound for unrestricted circuits? No.** It identifies exceptional gates with a permissible $\widetilde O(m^{-1/2})$ split rate and demands only $\widetilde\Omega(n^{3/2})$ of them. It neither converts them to coherent gates nor supplies a $\widetilde O(1/m)$ usefulness bound. It proves a near-quadratic result for a restricted class in which every gate is coherent or has an eligible block of definite drift. The general near-quadratic lower bound remains open. No asymptotic exponent improvement for unrestricted ordinary Andreev follows.

**Further quantifier error in source §5.4.** An aggregate demand for each arrangement, $\forall\sigma\,\sum_j p_j(\sigma)\ge D$, does not give a fixed set of gates each useful under EVERY arrangement. The gates supplying the demand can vary with $\sigma$. Similarly, Littlewood–Offord's upper bound on activity of table-heavy gates does not by itself force the same $\widetilde\Omega(n^{3/2})$ gates to have a specified small number of large table coefficients. A threshold on useful activity and another hybrid/counting step would be needed. Statements (3) and (4) of that four-property list are not established as stated.

## 3. Theorem 2.1 — entropy proof correct, activity convention needs repair

**Verdict: CORRECT main entropy inequality; FIXABLE errors in the auxiliary statements.**

**PROOF.** Fix the arrangement and cube. Let $r_j$ be the number of distinct breakpoint values. The actual restricted truth vector of a bottom gate has $r_j+1$ possible values as its table scalar varies; merge its two constant vectors into one symbol. There remain at most $r_j\le N$ symbols (one symbol if the gate is constant in the address). The joint symbols specify every nonconstant restricted gate. Any unknown constant values and the top's direct table-input contribution can be absorbed into one top threshold. Conditional on the joint symbols, the fixed score on the $N$ live-address inputs admits at most $N+1$ threshold patterns. The resulting output truth table is exactly a permutation of all $N$ independent table bits. Thus

$$N\le\sum_jH(Z_j^c)+\log_2(N+1).$$

The top reading raw addresses causes no issue: its live linear form is fixed independently of $x$. Pure-address gates have deterministic symbols and contribute zero entropy. Merging constant-zero and constant-one is legitimate because the additional threshold-position variable absorbs their difference. Independence among the $Z_j$ is neither claimed nor needed; subadditivity is an upper bound and may be very loose.

**Activity endpoints.** For the source convention $g=[Y+F\ge\theta]$, actual nonconstancy is

$$Y\in[\min B,\max B),$$

not $(\min B,\max B]$. With atoms, these are not interchangeable. Example: $g=[x+z\ge1]$ has breakpoints $0,1$ and is active at $x=0$, whereas the source's interval selects $x=1$. For a quantitative failure of the auxiliary entropy bound use $k=2$ and $g=[x_1+x_2+x_3+z_1\ge3]$, ignoring the fourth table bit and $z_2$. Its symbol has entropy $h(3/8)$, since activity occurs at table sum two; the source assigns $p=1/8$, and $h(3/8)>h(1/8)+2/8$. The error disappears by changing the activity interval to $[\min B,\max B)$ everywhere (and the corresponding concentration-function convention). No asymptotic theorem is lost.

With corrected $p$, the sound estimates are

$$H(Z_j^c)\le h(p)+p\log_2(N-1)\le h(p)+kp,$$

$$H(Z_j^c)\le\min\{k,\log_2|\operatorname{im}Y_j|,|\operatorname{supp}\alpha_j|\}.$$

The source's displayed chain $\log_2(1+\#\operatorname{im}Y_j)\le\min(k,|\operatorname{supp}\alpha_j|)$ is false (already two values and one support bit); the last entropy conclusion itself is correct by the deterministic-map argument above. The redundant entropy upper bound in item (1) can simply be replaced by $h(p)\le p\log_2(e/p)$.

**Littlewood–Offord clause.** For $R>0$, at least $r$ table coefficients of magnitude at least $R$ imply $p\le C/\sqrt r$ for a half-open length-$R$ interval. Complement negative-weight table bits and condition on other coordinates; the subsets giving a sum in that interval form an antichain, so Sperner/Erdős applies. When $R=0$, the gate never splits and $p=0$ directly; do not invoke an antichain argument with zero coefficients. This clause is classical anti-concentration, not a new structural theorem about every gate in a correct circuit.

## 4. Lemma 3.0 and Theorem 3.1 — simultaneous barrier valid; universal method barrier overstated

**Verdict: CORRECT probabilistic construction at balance, with FIXABLE parameter/constant details. WRONG as a theorem excluding every bounded per-gate potential or all other methods.**

**PROOF (one gate).** Fix any arrangement and cube. Its $K=\sum_i c_i$ fixed signs and $k$ live signs are disjoint independent coordinates in a random gate. Let $F$ be the fixed sum, $P$ the number of positive live signs and $Q=k-P$. For $g=[F+\lambda\cdot z+x_d\ge1/2]$, changing $x_d$ changes a vertex value iff $F\in[-P,Q]$. The live sum attains every integer between $-Q$ and $P$. Moreover the two restricted vectors give distinct *merged* symbols: if they differed but both were constant, all vertex sums would have to be zero, impossible for $k\ge1$ and live coefficients $\pm1$. Consequently $H_x(Z)=1$ on that event, zero otherwise. This checks the step not automatically justified by mere dependence on $x_d$ for arbitrary gates.

The interval $[-P,Q]$ contains zero and at least one of $-1,+1$. Therefore, conditional on the live signs,

$$\Pr(F\in[-P,Q])\ge2^{-K}\binom K{\lfloor K/2\rfloor}\ge(2K+2)^{-1/2}.$$

The latter inequality has an elementary proof, independent of the source's finite verification: for even $K=2r$, $\binom{2r}{r}/4^r\ge1/(2\sqrt r)$ follows by induction using ratio $(2r+1)/(2r+2)$; for odd $K=2r+1$ multiply by that ratio and compare with $1/(2\sqrt{r+1})$. Handle $K=0,1$ directly. In particular the weaker $p_*=(2\sqrt{2km})^{-1}$ used by the source is safe.

**PROOF (simultaneity).** With $S$ independent gates, $I_j=H(Z_j^c)$ are independent Bernoulli variables over the gate draw for each fixed arrangement and cube. Their expectation is at least $p_*$. Chernoff gives

$$\Pr\left(\sum_j I_j<Sp_*/2\right)\le e^{-Sp_*/8}.$$

There are at most $(m!)^k m^k$ arrangement/cube pairs, with log at most $2km\ln m$ for $m\ge2$. Hence failure probability is at most

$$\exp(2km\ln m-Sp_*/8).$$

Take a sufficiently large absolute $C$ and $S\ge C(km)^{3/2}\ln(km)$. At balance this is $O(n^{3/2}\log n)$, and $Sp_*/2\ge N$. The displayed numerical sufficient constant in the source's intermediate algebra is too small by a constant factor; choosing $C$ large repairs it. Outside the balanced regime the final inequality $Sp_*/2\ge2^k$ requires a separate $S\ge4\sqrt{2km}\,2^k$ term. The theorem should explicitly restrict its final demand statement to balance (as the introduction intends).

Uniformly random $d_j$ are unnecessary for the **marginal entropy sum**: every gate reads a fair table bit regardless of $d$. One could take all $d_j=d_0$ and still pass these inequalities, although then the entire joint symbol vector depends on just one table bit. Thus the construction meets the stated necessary numerical demand, not the actual ability to reconstruct arbitrary tables or compute Andreev. It supplies a feature family, not a correct threshold circuit. Calling it a set can be replaced by indexed family/multiset; at large balanced parameters duplicate random gates are negligible.

**Scope of the barrier.** It genuinely refutes a route consisting solely of this marginal-entropy (or raw split-count) demand and supply bounds valid for ALL gate families, even if a single arrangement or distribution of arrangements is chosen after the family is known. Since every arrangement works pointwise, averaging or choosing several arrangements does not help that particular demand.

It does **not** follow that every per-gate charge $\phi_j\le O(k)\mathbf1_{\mathrm{split}}$ is large on the example: an upper bound supplies no lower bound. For example charges can vanish on one-table-bit gates; whether such charges admit a valid demand for correct circuits is a new question, not excluded by this construction. Likewise the barrier family need not satisfy a new correctness-dependent structural hypothesis. The construction does not rule out stronger demands using joint/conditional information, top-sign compatibility, per-table-label coverage, restricted families, or relations across cubes. The source's assertions that all per-gate arguments fail, that only a particular top-weight/cross-cube route remains, or that “most gates can be made coherent” is categorically excluded are not proved. The report should claim a barrier for the precisely demonstrated relaxation, not an impossibility theorem about future proofs.

**COMPUTATION.** `independent_checks.py` exhaustively evaluates actual truth vectors and their merged symbols, rather than reusing the window formula, for $k=1,\ldots,4$, $K=0,\ldots,6$. Every tested dependence event, entropy event and $F\in[-P,Q]$ event agrees. This independently checks endpoint cases and the constant-merging issue; the universal result rests on the proof above, not this finite check.

## 5. Parity reductions and normal-form claims

### 5.1 Proposition 1.1: $\mathrm{size}(A_{1,m})=\mathrm{par}(m+1)$

**Verdict: CORRECT, exactly in the specified model.**

**PROOF.** For the lower bound substitute $x_1=1-x_0$; every bottom and direct top form remains affine in independent inputs $(a,x_0)$ and the output becomes their parity. For the upper bound start with a parity circuit score $T(a,y)$. On its finite domain shift its final threshold slightly so all true/false scores are strictly separated, rescale to margin one, and choose $B\ge\max|T|$. Substituting $y=x_0$ and using score

$$T(a,x_0)+2B(x_0+x_1-1)$$

gives the correct lookup when $x_0\ne x_1$, forces positive when both are one, and negative when both are zero. Only direct top coefficients and the top threshold change. Arbitrary real weights and direct raw top inputs are essential to the no-added-gates formulation. This establishes an equality of minima, not an exact formula for $\mathrm{par}(M)$.

For any $k$, the affine table substitution $x_c=y\oplus(|c|\bmod2)$ likewise proves $\mathrm{size}(A_{k,m})\ge\mathrm{par}(km+1)$. Fixing the table to a constant parity table instead gives parity on $km$ bits, not $km+1$; the latter requires retaining the independent bit $y$ through that substitution. Source §5.2 conflates these two operations.

### 5.2 What follows, and what does not

**Verdict: MIXED; several asserted equivalences/nonimplications are WRONG or UNPROVED.**

* At $k=1$ the equivalence with parity is exact. For a specified fixed $k\ge2$, the supplied proof gives only the necessary implication $o(m)$ Andreev circuits $\Rightarrow o(M)$ parity circuits. It supplies no reverse simulation from arbitrary sign-correct parity circuits to arbitrary-table $A_{k,m}$. Combining parity **scores** as if they were exact $\pm1$ parity values would add an unjustified assumption/layer. If the quantifier is “some fixed $k$, allowing $k=1$”, equivalence follows from the $k=1$ identity. These are different statements. Also $o(M)$ does not mean a fixed-power improvement $M^{1-\eta}$; logarithmic savings are sublinear too.
* A function-dependent coherence normal form asserted for **all** $A_{k,m}$ includes $k=1$, so it DOES imply a near-linear parity bound via Proposition 1.1 and the coherent $\Omega(m)$ bound. The source's categorical “function-dependent implies nothing about parity” is false with that quantifier. If the claim is restricted to balanced growing-$k$ Andreev, the given restrictions do not imply such a parity lower bound. That is a limitation of these reductions, not a proof of logical independence or impossibility of all other reductions.
* A syntactic transformation of every depth-two circuit into circuits whose bottom gates are all monotone/antimonotone after a **common** reorientation, with $S\operatorname{polylog}$ gates, would imply $\mathrm{par}(M)\ge M/\operatorname{polylog}M$. Do not call this merely “unate gates”: every individual threshold function is already unate after its own input flips. The same reorientation must work across the gates (or all coefficients of each gate must have one sign in the original coordinates).
* A balanced Andreev coherence conversion with loss $S^c$ yields a lower bound of exponent $2/c$, up to logs. It exceeds $3/2$ when $c<4/3$; it is not equivalent to exponent two for fixed $c>1$. A near-quadratic lower bound plus an explicit coherent $O(n^2)$ construction gives a nonconstructive near-size-preserving replacement, but $n^{2-o(1)}$ corresponds to subpolynomial overhead, not necessarily polylogarithmic overhead.
* The conjectured direct sum $\mathrm{size}(A)\gtrsim N\,\mathrm{par}(m)/\operatorname{polylog}n$ would transfer a near-linear **lower bound** for parity to a near-quadratic lower bound for balanced Andreev. On its own it would not make the two lower-bound questions equivalent. An upper bound in terms of $N\,\mathrm{par}(m)$, or another reverse reduction, is missing.

The supplied small-size parity experiments are finite solver evidence, not a proof of an all-size parity formula. This review does not rerun that unrelated solver campaign. Primary-source checks of the asymptotic lower-bound status appear in §9.

## 6. Proposition 5.1 — false range argument; a weaker framework obstruction is repairable

**Verdict: WRONG under the relevant interpretation “values attained by $L$”; CORRECT but unnecessarily weak if one literally requires alternation at every integer in the full numerical interval.**

The algebraic first clause is correct: all $c_l$ are odd (set one bit at a time), and $L_{\max}-L_{\min}=\sum_l|c_l|\ge M$. The attainable values need NOT be consecutive integers.

**REFUTATION.** Let $M=2$ and $L=3y_1+3y_2$. Its attainable set is $\{0,3,6\}$, width six. The score

$$-1+2[L\ge3]-2[L\ge6]$$

has the correct parity sign at every attainable value, with TWO gates, violating the claimed minimum $\lceil6/2\rceil=3$. This was also checked on all four raw inputs. More generally scaling every odd coefficient by an arbitrarily large odd number changes the numerical range without changing the number of threshold gates needed. Any gate lower bound proportional to that unnormalized range is therefore impossible on the attained input set. If alternation were required on all integers between the extremes, including unattainable values, each adjacent pair would require a distinct jump, giving at least the full range number of gates for a pure step sum. That stronger hypothesis is not furnished by correctness on Boolean inputs.

**PROOF (corrected architecture-specific statement).** Reorient negative coefficients by complementing their bits. Then $L=L_{\min}+\sum_l|c_l|z_l$, with every $|c_l|$ positive odd. Along any maximal Boolean chain of length $M$, $L$ strictly increases and its parity alternates at each step. A pure threshold-step sum in $L$ must therefore have at least $M$ gate transitions to sign-represent parity on all attained inputs. If arbitrary direct raw affine terms are allowed, choose the chain order adversarially according to their signs, as in the coherent parity proof: at least $\lfloor M/2\rfloor$ steps require bottom changes, and each monotone bottom changes at most once. Thus $\Omega(M)$ remains true, independent of coefficient magnitudes and signs.

For architectures that explicitly allocate a disjoint parity staircase to each character $T$, this gives cost $\Omega(\sum_T |T|m)=\Omega(kNm)$, hence a quadratic exponent at balance. It does not prove such allocation necessary, prohibit shared gates/cancellations between characters, or prove a direct-sum theorem for arbitrary threshold circuits. The source's “only known mechanism” is a description of searched constructions, not an exhaustive mathematical classification of possible constructions. The corrected statement supports the narrow signed-ladder obstruction, not the general conjecture.

## 7. Proposition 6.1 — correct affine reformulation with an essential offset constraint

**Verdict: CORRECT proposition if “matching $c(a)$” means the actual interval below. FIXABLE overstatement when dominance alone is presented as an exact fixed-budget reformulation.**

A gate $[\alpha x_d+L(a)\ge\theta]$ is constant, $x_d$, or $1-x_d$ as a function of the table. Its coefficient on $x_d$ is nonzero exactly for

$$\theta-L(a)\in(\min(0,\alpha),\max(0,\alpha)],$$

which is correct including both tie cases (unlike the differently oriented interval in Theorem 2.1). Hence the full score has the form $w(a)\cdot x+c(a)$ with $w_d$ as stated. For a fixed address with output label $b$, exact correctness is equivalent to

$$-w_b-\sum_{d\ne b}\min(w_d,0)\ \le c(a)\ <\ -\sum_{d\ne b}\max(w_d,0).$$

This interval is nonempty iff

$$w_b>\sum_{d\ne b}|w_d|.$$

**PROOF.** Maximize the score over the false face $x_b=0$ and minimize it over the true face $x_b=1$. The false maximum must be strictly negative, the true minimum nonnegative. These are exactly the two inequalities above. The script independently checks this equivalence for all 1,625 choices of three integer coefficients in $[-2,2]$ and integer offset in $[-6,6]$.

In a given circuit $c(a)$ is generated by the same bottom gates and direct top weights; it is not an independently selectable function of $a$. Example: $w=(2,0)$ satisfies dominance for label zero, but $c=100$ outputs constant one. Thus dominance alone is necessary and does not certify an existing circuit.

**PROOF (useful asymptotic repair).** If a proposed one-table-bit gate family has dominance everywhere, it can be centered with at most two extra pure-address gates per original gate. Write $g_j^0(a)=g_j(0,a)$ and $g_j^1(a)=g_j(1,a)$, each a raw address threshold. Replace $v_jg_j(x_d,a)$ in the top score by

$$v_j\left(g_j(x_d,a)-\frac{g_j^0(a)+g_j^1(a)}2\right).$$

Also center the direct table term to $\sum_d u_d(x_d-1/2)$ and remove direct address terms. The resulting score is exactly $\sum_d w_d(a)(x_d-1/2)$, whose sign is the designated dictator whenever dominance holds. So a dominance-only design does yield a correct circuit with at most a factor-three bottom overhead. This does not justify ignoring the offset in an exact-size proposition, but it makes the dominance formulation appropriate when only asymptotic exponents matter.

The claimed “equivalently each family weakly computes its own parity-class indicator” requires a definition and is not an ordinary threshold-separation statement. For two labels, the weight vector $(1,0)$ on class zero and $(100,101)$ on class one satisfies both dominance conditions; family zero is numerically larger OFF its own class. Dominance compares coordinates at the same address, not a family's values across addresses.

The final claim that a result for one-table-bit gates would “almost certainly extend” is speculation. Multi-table-bit gates are nonlinear in $x$ and no same-size reduction to this class is proved. The new target is legitimate; its transfer to unrestricted circuits is not established.

## 8. Additional exponent-level correction: the proposed one-table-bit target follows from slicing

**PROOF / REFUTATION of source §6.2's “smallest open target” claim.** The statement that beating exponent $3/2$ for one-table-bit circuits is still open is not supported: an elementary direct-sum reduction, combined with a known slicing theorem, already gives exponent $32/19>3/2$. This does NOT improve the unrestricted ordinary-Andreev bound.

### 8.1 Modern slicing bounds apply even with raw top inputs

Let $\operatorname{slice}(r)$ be the minimum number of hyperplanes slicing every edge of the $r$-cube. Sauermann–Xu, Theorem 1.1, prove

$$\operatorname{slice}(r)=\Omega(r^{13/19}/\log^{32/19}r).$$

This is a primary-literature result, not a new theorem of this review. [Sauermann–Xu, *Improved lower bound for hypercube edge slicing*, 2025](https://arxiv.org/abs/2510.16592).

**PROOF (transfer, including direct inputs).** Given a parity circuit on even $r$ with score $u\cdot x+\sum_{j=1}^s v_jg_j(x)-\tau$, complement coordinates with negative $u_i$. The resulting function is parity or its complement, and all direct coefficients are nonnegative. Every upward edge on which the output decreases must be cut by a bottom gate; otherwise the score cannot decrease. These are exactly one of the two classes distinguished by the parity of the lower endpoint's Hamming weight. The map $x\mapsto1-x$ interchanges those two edge classes when $r$ is even. The bottom hyperplanes together with their reflected copies therefore slice all edges. Shift each bottom threshold infinitesimally if needed to avoid all vertices while preserving its Boolean values. Hence $2s\ge\operatorname{slice}(r)$. For odd input count, fix one input and apply the even case. Thus in the model of the question,

$$\mathrm{par}(M)=\Omega(M^{13/19}/\log^{32/19}M).$$

The source's claim that $\Omega(\sqrt M)$ remains the best exact parity gate lower bound is therefore WRONG. It is a valid older bound, and the square-root scale remains relevant for average-case parity; that is a different statement.

### 8.2 Direct sum for gates reading at most one table bit

Fix any block index $i$. Partition the $N$ table labels into $N/2$ pairs $\{d,e\}$ with $e=d\oplus e_i$ and $d_i=0$. Let $s_d$ count bottom gates reading table bit $x_d$ (pure-address gates are excluded).

For one pair fix all address blocks except $i$ to any strings having the common prescribed parities $d_{-i}$. Let $X^d$ be the table having its sole one at $d$, and $X^e$ the table having its sole one at $e$. For the actual real top score $\Phi$, define

$$D_{d,e}(a_i)=\Phi(X^d,a)-\Phi(X^e,a).$$

When block $i$ has even parity, the first score is nonnegative and the second strictly negative, so $D_{d,e}>0$. When block $i$ has odd parity, the signs reverse and $D_{d,e}<0$. Thus $D_{d,e}$ sign-represents parity or its complement on ALL $m$ raw bits.

All pure-address gates, direct address inputs, and gates reading a table bit outside $\{d,e\}$ cancel in this difference. A remaining bottom gate contributes a difference of two raw-address threshold gates (the two fixed values of its table bit); direct table terms contribute only a constant. Therefore $D_{d,e}$ is a depth-two threshold score with NO direct live inputs and at most $2(s_d+s_e)$ bottom gates. Every address edge changes its output, so those hyperplanes slice every edge:

$$2(s_d+s_e)\ge\operatorname{slice}(m).$$

Summing over the disjoint matching gives the explicit bound

$$S\ge\sum_d s_d\ge\frac N4\operatorname{slice}(m)
=\Omega\!\left(\frac{Nm^{13/19}}{\log^{32/19}m}\right).$$

At balance $m=\Theta(N/k)$ this is

$$\boxed{\mathrm{size}_{\mathcal T_1}(A_{k,m})\ge\widetilde\Omega(n^{32/19}).}$$

This proof does not assume a common bottom sign pattern, bounded weights, an exact top sum, or a free address-dependent offset. It directly uses the signs of two actual circuit scores, so strict/weak threshold ties are handled correctly. It also proves $S\ge N\,\mathrm{par}(m)/4$, since the same difference is a permissible parity circuit; the slicing formulation is slightly more direct.

There is no contradiction with the valid part of Theorem 3.1: its random feature family passes marginal-entropy demands but does not compute Andreev, so need not satisfy these pairwise score-difference requirements. This is a concrete reason the broad “no per-gate argument” wording is untenable. The method uses correctness to isolate disjoint table-label families before applying a known multi-hyperplane theorem.

**Limit of transfer.** If every bottom reads at most $t$ table bits, each gate participates in at most $t$ matching pairs, and the same proof gives $S\ge N\operatorname{slice}(m)/(4t)$ (or the corresponding lower bound on total bottom table-support wires). For unrestricted $t$ this gives no improvement over the known general Andreev exponent. A generalization from one-table-bit gates without paying for table support is precisely what is missing, contrary to the source's suggestion of an almost automatic extension.

## 9. Primary literature and novelty assessment

**Drift bound.** Its anti-concentration input is exactly a standard Kolmogorov–Rogozin concentration-function bound applied to independent two-point variables. Rogozin's original theorem already supplies the interval-length factor used here. [B. A. Rogozin, *On Evaluating the Concentration Functions*, 1961](https://www.mathnet.ru/php/archive.phtml?jrnid=tvp&option_lang=eng&paperid=4753&wshow=paper). A modern sharp version is due to [Tomas Juškevičius, 2022](https://arxiv.org/abs/2201.09861). The additional steps are the elementary beta-mixture identity, Bernstein concentration around $qD'$, and integration over the interval of plausible $q$ values. **Assessment:** a useful application of standard concentration plus anti-concentration, not a new anti-concentration theorem. The precise bounded-range Andreev drift corollary was not located in this targeted search; that is not a certification of novelty or an exhaustive literature review. Its exponent-level contribution is a restricted structural refinement, not a stronger unrestricted lower bound.

**Table anti-concentration.** Theorem 2.1(3) is the classical antichain/Littlewood–Offord phenomenon. The primary source is [Paul Erdős, *On a lemma of Littlewood and Offord*, 1945](https://users.renyi.hu/~p_erdos/1945-04.pdf). Preserve that attribution. The entropy-symbol packaging in Theorem 2.1 is a straightforward sharpening of the existing fixed-direction count; it can remove pure-address gates from the account but does not alone improve the unrestricted exponent.

**Historical baseline.** [Impagliazzo–Paturi–Saks, *Size–Depth Tradeoffs for Threshold Circuits*, 1997](https://cseweb.ucsd.edu/~paturi/myPapers/pubs/ImpagliazzoPaturiSaks_1997_siamjc.pdf) proves the older square-root gate bound for exact depth-two parity and contains the classical orientation/chain argument. [Kane–Williams, *Super-Linear Gate and Super-Quadratic Wire Lower Bounds for Depth-Two and Depth-Three Threshold Circuits*, 2016](https://arxiv.org/abs/1511.07860) supplies the classical ordinary-Andreev $\widetilde\Omega(n^{3/2})$ gate bound and shows the square-root parity gate scale is tight for high constant average-case agreement. Those statements do not establish that the exact parity bound is still square-root today.

**Current exact-parity correction.** The connection of slicing to threshold-circuit lower bounds is already established in [Yehuda–Yehudayoff, *Slicing the hypercube is not easy*, 2021](https://arxiv.org/abs/2102.05536). [Sauermann–Xu's 2025 slicing theorem](https://arxiv.org/abs/2510.16592) provides the $13/19$ exponent used in §8. The raw-top-input transfer and the table-pair direct-sum proof are written out independently here so the exact model is explicit. They should be described as consequences of known geometric lower bounds, not as a new unrestricted parity breakthrough. The review does not assert that $13/19$ is an exhaustively verified optimal current literature exponent; it is a verified available exponent already sufficient to refute the source's square-root-best claim and solve its stated restricted target.

**Other scope corrections.** [O'Neil, *Hyperplane cuts of an n-cube*, 1971](https://doi.org/10.1016/0012-365X(71)90025-2) gives the classical maximum-edge-cut bound. It does not alone justify the source's extra assertion that cuts cannot concentrate on one parity class by more than a constant factor: a threshold isolating the all-one vertex cuts only edges incident to that single parity class, with an unbounded relative concentration factor as $N$ grows. The source's $\Omega(N\sqrt{km})$ one-table-bit discussion needs additional reasoning; §8 supplies a stronger asymptotic result directly.

The older slicing upper-bound citation in the background is also out of date: [Soiffer et al., *Improved Upper Bounds for Slicing the Hypercube*, 2026](https://arxiv.org/abs/2602.16807) improves it. That changes only a constant and is immaterial to the present task. No improvement of slicing should be confused with an exact parity circuit construction: covering edges is a necessary condition, not sufficient to find fixed top weights.

**Novelty conclusion.** The simultaneous marginal-entropy barrier is a valid elementary probabilistic-method refinement of the earlier fixed-distribution barrier. The drift theorem is a standard-tools application with a useful but conditional hybrid corollary. Neither establishes a coherent normal form or the desired unrestricted quadratic exponent. The one-table-bit lower bound in §8 is an elementary reduction to known literature, and its priority as a separately stated corollary has not been exhaustively investigated.

## 10. Independent computations and source-script audit

**COMPUTATION, reproducible:**

```
python3 -I /tmp/andreev_gap/review_coherence/independent_checks.py
python3 -I /tmp/andreev_gap/review_coherence/transfer_checks.py
```

The first script imports only the supplied NumPy installation, not source-author mathematical code. Exact small-case probabilities use `Fraction` and enumerate every nonlive subset, weighting each by $1/(m^2\binom{m-1}{r})$ for the live-coordinate/subset law. It convolves block endpoint distributions and sweeps all distinct fixed-threshold split events. Eight two-block, eight-bit profiles include coherent, biased, exactly zero drift, minimal drift, unequal bounded magnitudes, drift carried by a few heavier bits, heavy tails, and mismatched block scales. All probabilities and vectors are saved in `checks.json`; this is exact verification of those instances, not a proof for arbitrary real weights.

The larger fixed-seed experiment tests seven profiles at each of $m=64,256,1024$, with 60,000 independently sampled restrictions per profile (1,260,000 total). It samples the exact beta-mixture restriction law. The threshold $\theta=\tfrac12\sum\gamma+\tfrac12$ is fixed before drawing restrictions; an additional fixed threshold $1/2$ is also measured. It includes:

* constant drift with $W=1$;
* exactly zero drift and the minimal admissible drift $2/m$;
* net drift carried by $\sqrt m$ coefficients, with all others cancelling, both at $W=4$ and at $W=m$;
* sparse profiles with zeros, explicitly OUTSIDE the lemma;
* an all-positive small-scale block together with a globally much larger balanced block, explicitly OUTSIDE any local-to-global simplification.

No fixed-threshold observation contradicts the proved bounded-range asymptotic estimate. The zero/minimal-drift profiles retain the square-root survival scale; heavy-tailed or sparse profiles need not split frequently merely because the lemma is inapplicable. Exact probabilities, Monte Carlo standard errors, actual relative drifts and global scale ratios are retained, so numerical evidence is not mislabeled as a uniform theorem. The original source's unspecified absolute constants are not “verified” by fitting numerical constants.

The script also exhaustively checks 3,810 actual barrier truth-vector cases and 1,625 dictator/offset cases, and records exact counterexamples to the activity endpoint and attained-range claims. `transfer_checks.py` verifies complement reflection on all edges in even dimensions through eight, the score-difference construction on explicit correct one-table-bit $A_{1,m}$ circuits for $m\le10$, and cancellation identities for random one-table-bit scores. These guard against sign, endpoint and raw-input accounting mistakes; the all-size results are the written proofs.

**Source-script caveat.** `drift_split.py` calls `defect_split.split_fraction` without a threshold. That function selects `np.median(F)+0.5` AFTER seeing the arrangement. Thus the advertised source checks estimate an arrangement-dependent-threshold quantity, whereas Lemma 4.1 concerns a fixed gate and threshold averaged over arrangements. They are useful exploratory diagnostics, not direct verification of the lemma's exact quantifiers. The new computations avoid this issue. Their finite data also cannot establish the source's assertions of a precise limiting constant or “true” $\Theta$ behavior. `adaptive_arr.py` is a local-search heuristic; its best found total is an upper bound on the optimum, not a certificate of an every-arrangement minimum. `barrier_const.py` does use exact rational probabilities for its finite checks.

**PROOF: fixed-arrangement drift is false.** For $m$ divisible by four and $k=1$, order $(+1,-1)$ repeated $m/4$ times, followed by $m/2$ positive weights. The signed sum is $m/2$, so $\delta=1/2$ and $W=1$. At threshold $1/2$, at least the first $m/2$ edges split. Thus a fixed arrangement can have constant split fraction despite constant drift. Uniform random arrangement is indispensable. The transfer script checks the arithmetic on several sizes; the construction proves it for all such $m$.

**PROOF detail for the block-scale counterexample in §1.** For $m=2h$ with exactly $h$ signs of each kind, the probability that the random bridge crosses $0\to1$ at step $2r+1$ is

$$\frac{\binom{2r}{r}\binom{2h-2r-1}{h-r-1}}{\binom{2h}{h}}.$$

For $r$ in a fixed central fraction of $[0,h]$, central-binomial estimates make this $\Theta(m^{-1/2})$. Summing over $\Theta(m)$ such steps gives $\Theta(\sqrt m)$ expected crossings; division by $m$ gives the claimed $\Omega(m^{-1/2})$ split probability. This supplies the lower bound needed to refute a $\widetilde O(1/m)$ local-comparability extension.

**Optional union-bound sharpening, no exponent change.** A cube/arrangement pair determines only a live coordinate and a fixed subset in each block. There are $(m2^{m-1})^k=\exp(O(km))$ distinct restrictions, rather than $(m!)^km^k$. Union-bound over these restrictions instead: $S=C(km)^{3/2}$ already meets the marginal demand simultaneously at balance for sufficiently large $C$. The extra logarithm in Theorem 3.1 is unnecessary, but this does not improve or worsen the exponent-level barrier and does not address the score-difference constraints of §8.


## 11. Artifacts and final assessment

All review-created source files carry Christian Reitwiessner authorship credit. Original mathematical results retain their literature attribution. No source-author report, shared paper, or repository file was modified. The assigned review directory was empty apart from an empty logs directory when this review began; no prior report was overwritten.

* `report.md`: claim-by-claim audit, corrected proofs, counterexamples, and primary-source assessment.
* `independent_checks.py`, `checks.json`, `logs/independent_checks.log`: exact split distributions, entropy/barrier/offset checks and fixed-threshold Monte Carlo.
* `transfer_checks.py`, `transfer_checks.json`, `logs/transfer_checks.log`: exact checks supporting the slicing and table-pair transfers.

**Explicit answers.** The near-zero-sum result does **not** supersede the previous arbitrary-weight mixed-sign hybrid; it adds a stronger conclusion only on globally comparable blocks. It does **not** imply the coherent near-quadratic lower bound for unrestricted circuits. The drift bound uses standard anti-concentration rather than a new probabilistic principle. The source has no proved unrestricted exponent improvement. Its one-table-bit proposed target, however, is surpassed by the literature-based $\widetilde\Omega(n^{32/19})$ consequence proved in §8; arbitrary table support remains the obstruction to transferring that consequence to the full model.
