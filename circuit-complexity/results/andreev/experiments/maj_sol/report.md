# PATH1: ordinary Andreev, majority models, exact sums, and multiplicity

Copyright (c) 2026 Christian Reitwiessner

Authors: Christian Reitwiessner

Research completed independently; no subagents, no online posts, no changes outside this directory. Read the lower-bound report, independent review, mixed-sign extensions, upper report and actual construction code, and the newer mixed-upper periodic/subcube families. Labels below distinguish proofs here, finite checks, sourced results, and unresolved questions.

## Findings

* **[PROVED HERE]** In the exact-sum model with address coefficients in $\{0,\pm\lambda_j\}$ at gate $j$, including fully mixed signs and arbitrary table coefficients, one has
  $$S\ge \max_{1\le r\le k}\binom kr=\binom{k}{\lfloor k/2\rfloor}=\Omega(N/\sqrt k).$$
  This uses one global Fourier rank argument, not per-cube survival. It has a quantitative approximation version and a weaker bounded-integer-weight version below. It is an intermediate theorem, **not** an improvement on the balanced unrestricted-real lower bound.
* **[PROVED HERE]** For arbitrary bottom LTFs, sign correctness with margin $\gamma$ forces gate-output top norm at least $\gamma/q_{km+1}$, where $q_M=2^{-M}\binom{M-1}{\lfloor(M-1)/2\rfloor}$. Thus $\sum_j|v_j|=\Omega(\gamma\sqrt{km})$, even with affine direct inputs. Exact sums have the same bound with $\gamma=|c|$.
* **[REFUTED IN ITS POINTWISE FORM]** Uniform $O(V/m)$ within-block smoothness of a symmetrized bounded-weight gate is false already for balanced $\pm1$ coefficients. This invalidates one natural justification of the earlier exact-sum sketch. The proposed $\Omega(Nm/V)$ **gate** bound itself remains neither proved nor refuted here.
* **[VERIFIED]** The actual merged $d''$ construction has coefficient total $\Theta(N^3)$, not $O(N^2)$, in the balanced regime. Its conversion into majority gates with repeated literal wires also has $\Theta(N^3)$ wires including threshold padding. Converting its top to a gate with no repeated gate-output wires by cloning the bottom gates has $\Theta(N^3)$ bottom gates and $\Theta(N^4)$ literal wires.
* **[KNOWN SOURCE + TRANSFER]** Paturi–Saks plus the parity-table restriction gives $S=\Omega(m/\log^2m)$ at fixed $k$ for polynomially bounded bottom and top integer weights, stronger there than the unrestricted parity bound.
* **[KNOWN SOURCE]** Kane–Williams already give a superquadratic unrestricted wire lower bound for ordinary Andreev, hence also for multiplicity wire counts. No additional asymptotic multiplicity lower bound beating that result was established here.

## 1. Models and exact transfer costs

Use Boolean inputs $z=(x,a)\in\{0,1\}^{N+km}$, $N=2^k$, $A(x,a)=x_b$, and $f=(-1)^A$. Count $S$ bottom gates, with a top gate allowed to read raw inputs unless stated otherwise. Gate counts below exclude that one top gate. This direct-input convention matters.

**Integer thresholds.** A bottom gate is $g_j=[w_j\cdot z\ge t_j]$ with integer coefficients and threshold. Distinguish an **address bound** $|w_{j,a}|\le V$ from an **all-input bound** $|w_{j,i}|\le V$. Neither bounds $t_j$ or the top weights. A threshold outside the attainable range is a constant gate and can be removed. Divide a gate's coefficient vector by its positive gcd $h$, replacing $t$ by $\lceil t/h\rceil$, before charging multiplicity if desired.

**Majority of literals with multiplicity.** A gate is an ordinary majority of a multiset of literals, optionally including constants; every occurrence is a wire. Canceling opposite occurrences gives an integer threshold. Conversely put $B=\sum_i|w_i|$ and $r=t+\sum_{w_i<0}|w_i|$. Replace positive coefficients by repeated positive literals and negative coefficients by repeated negative literals. This gives a threshold $[\sum_{\ell\text{ occurrences}}\ell\ge r]$ with $B$ variable wires. A strict majority gate with odd fan-in implements it using exactly
$$p=|B-2r+1|$$
constant wires: add $B-2r+1$ ones if nonnegative, or its negation zeros otherwise. Then the threshold is exactly $r$. For a nonconstant gate $1\le r\le B$, $p\le B-1$. This is an explicit conversion cost, not a claim of minimal majority realization. Constants are essential to this particular same-depth conversion; specify if the model forbids them.

Define coefficient weight
$$W_{\rm coef}=\sum_j\|w_j\|_1+\sum_j|v_j|+\|u\|_1$$
for integer top score $F=\sum_jv_jg_j+u\cdot z+K$. Biases are excluded in this convention; an alternative including thresholds must be named. The conversion above includes explicit bias-padding wires, and costs at most twice the nonconstant-gate coefficient weight. Negative top coefficients are handled by complemented bottom outputs, replacing $g$ by $1-g$ and adjusting the bias. This needs no extra threshold depth. Negative raw coefficients use negative literals.

**Unit top weights, no repeated gate-output wire.** Each physical bottom gate may feed the top at most once, with coefficient $+1$ on a selected output literal. Equivalently allow signed unit coefficients and complement outputs for free. Direct inputs need a separate convention: if also unrepeated, their coefficients are in $\{0,\pm1\}$. Constants may pad the majority threshold.

An integer top coefficient $v_j$ is replaced by $|v_j|$ physically distinct copies of gate $j$. This changes the bottom-gate count from $S$ to $S'=\sum_j|v_j|$ and changes the bottom literal cost to
$$\sum_j|v_j|\bigl(\|w_j\|_1+p_j\bigr).$$
It does not preserve the original bottom-gate count. Unrestricted integer direct weights can likewise be implemented by repeated raw literals; if the top forbids those repetitions too, use copies of one-literal identity bottom gates, adding $\|u\|_1$ gates and bottom wires. Real weights first require an integer representation; no uniform coefficient bound follows from their gate count alone. Large integer top weights therefore cannot silently be replaced by unit weights without charging these costs.

Finally, a literal majority **without repeated variable wires at the bottom** has coefficients $0,\pm1$, whereas the multiset model may have arbitrary integer coefficients. Splitting a weight-$V$ raw input into $V$ occurrences is forbidden in the former model and cannot be claimed as a free same-depth conversion. These are genuinely different gate-count questions.

## 2. Exact-sum theorem via Fourier rank

An exact sum means
$$F(x,a)=\sum_{j=1}^S v_jg_j(x,a)+u\cdot(x,a)+K=c f(x,a)+d,\qquad c\ne0,$$
on **all bit inputs**. The coefficients $v_j,u,K$ may be real. Bounding them is an additional restriction. Exact equality to $A$ instead of $f$ is equivalent after affine rescaling.

Write $X_c=(-1)^{x_c}$ and $\chi_T(a)=(-1)^{\sum_{i\in T}a_i}$. For a set $R$ of blocks let $T_R$ be all $m|R|$ bit positions in those blocks. The Walsh expansion is
$$f(x,a)=\frac1N\sum_{R\subseteq[k]}\left(\sum_{c\in\{0,1\}^k}(-1)^{R\cdot c}X_c\right)\chi_{T_R}(a).$$
All Fourier conventions are expectations under independent uniform bit inputs.

**Theorem 1 [PROVED].** Suppose at each bottom gate all nonzero address weights have the same absolute value $\lambda_j>0$; signs, zero positions, table weights and thresholds are arbitrary. For each $1\le r\le k$, $S\ge\binom kr$.

*Proof.* Fix $r$ and put $d_0=rm$. Form the $N$ by $\binom kr$ matrix of joint Fourier coefficients at table characters $X_c$ and address characters $\chi_{T_R}$, $|R|=r$. The target matrix is $c/N$ times the corresponding columns of the $N$ by $N$ Walsh matrix. Its columns are orthogonal, so its rank is $\binom kr$ and every singular value is $|c|/\sqrt N$.

For gate $j$, let $J_j$ be its nonzero address support and let $\epsilon_{j,i}$ be its signs. Flip its negative address inputs. For each fixed table $x$, the gate is now a symmetric threshold of the $|J_j|$ live address inputs. Consequently at a fixed degree $d_0$ its address Fourier coefficient at $T$ equals
$$h_{j,d_0}(x)\,\mathbf1[T\subseteq J_j]\prod_{i\in T}\epsilon_{j,i}.$$
The sign product and support indicator are independent of $x$. Taking the table Fourier coefficient at $X_c$ therefore gives an outer product: this gate's matrix has rank at most one. Affine direct inputs and constants have zero joint coefficient at every pair $(X_c,\chi_{T_R})$ with $R\ne\emptyset$, including when $rm=1$. The sum of $S$ such matrices has rank at most $S$. Compare ranks. $\square$

This proof permits a different magnitude $\lambda_j$ at every gate, so it is stronger than merely the integer $V=1$ hypothesis. It places no coherence condition on the signs. It combines all tables and many address characters in one rank calculation.

**Bounded integer extension [PROVED].** If address magnitudes are in $\{1,\dots,V\}$, partition a gate's support into magnitude classes $J_{j,h}$. For degree $d_0$ the coefficient depends, after sign flips, only on the profile $(|T\cap J_{j,1}|,\dots,|T\cap J_{j,V}|)$. Thus its matrix rank is at most the number $P_j(d_0)$ of feasible profiles, with
$$P_j(d_0)\le\binom{d_0+V-1}{V-1},\qquad
\binom kr\le\sum_jP_j(rm)\le S\binom{rm+V-1}{V-1}.$$
This quickly weakens for $V\ge2$; it must not be advertised as an $Nm/V$ bound.

**Approximation extension [PROVED].** If instead $\mathbb E(F-cf-d)^2\le\eta^2$, the same rank argument plus Parseval and the best low-rank approximation inequality gives
$$S\ge\binom kr-\frac{N\eta^2}{c^2}.$$
For completeness, a rank-$S$ matrix misses at least $\binom kr-S$ of the target's equal singular values; its squared Frobenius error is at least $(\binom kr-S)c^2/N$. This matrix error is bounded by the full Fourier squared error $\eta^2$.

A sign-correct score with two-sided amplitude control $\gamma\le fF\le B$ has $|F-cf|\le(B-\gamma)/2$, with $c=(B+\gamma)/2$. Hence
$$S\ge\binom kr-N\left(\frac{B-\gamma}{B+\gamma}\right)^2.$$
At $r\simeq k/2$, retaining a constant fraction of the rank bound requires amplitude distortion $O(k^{-1/4})$. Merely bounding the top coefficient norm by a polynomial does **not** give this near-constant output amplitude. Thus this is a real robustness statement, but not a transfer to ordinary sign correctness with a loose norm bound.

## 3. What fails in the proposed smoothness route

Take even $m$, half the block weights $+1$ and half $-1$, and
$$g(a)=[\sum_{i\le m/2}a_i-\sum_{i>m/2}a_i\ge0].$$
After averaging over all within-block permutations, let $q(s)$ be its value at block weight $s$. Then $q(0)=1$ and $q(1)=1/2$, for every even $m$. Thus neither a pointwise adjacent-layer bound $|q(s+1)-q(s)|=O(V/m)$ nor the claimed uniformly smooth picture is valid at $V=1$. At $m=2$, $q=(1,1/2,1)$ even has nonzero discrete second difference. Averaging preserves equality, but does not eliminate parity information gate by gate.

This refutes a possible lemma, not the desired total bound. A proof of $S=\Omega(Nm/V)$ would need a global cancellation argument or a suitably weighted smoothness inequality that survives boundary layers. I found no such proof and no finite counterexample to the gate bound. The Fourier-profile extension above identifies a precise bottleneck rather than assuming smoothness.

**Small-data guardrails.** The supplied $k=1$ exact minimum $2\lceil m/2\rceil$ and $k=2$ values $4,5,\ge6$ were established in the **block-symmetric** model, as the independent review explicitly says. They cannot be quoted as full mixed-sign exact optima. The sign-model minima $3,3,\ge4$ for $k=2,m=1,2,3$, and the $V=1$ versus $V=2$ distinction at $(2,2)$, do not conflict with Theorem 1, which gives only 2 at $k=2$. No claim here excludes those witnesses. The newer subcube-dominance family has unit bottom weights but nonconstant, table-dependent output amplitudes, so Theorem 1's exact-sum hypothesis generally fails for it.

## 4. Margin versus top norm, with arbitrary LTF bottom gates

**Lemma 2 [PROVED].** For every Boolean threshold gate $g$ on $M$ inputs,
$$|\mathbb E\,g(z)(-1)^{|z|}|\le q_M:=2^{-M}\binom{M-1}{\lfloor(M-1)/2\rfloor}.$$

*Proof.* Flip negative-weight inputs, which affects only the sign of the full parity coefficient. The gate is monotone. Symmetrize over all coordinate permutations; its average layer values $p_0\le\cdots\le p_M$ are monotone. Write the averaged function as a nonnegative mixture of constant functions and thresholds $[|z|\ge t]$, with total threshold-mixture mass at most one. Each threshold has full parity coefficient
$$2^{-M}\sum_{s=t}^M(-1)^s\binom Ms=2^{-M}(-1)^t\binom{M-1}{t-1}.$$
The maximum magnitude is $q_M$. $\square$

**Corollary [PROVED].** For $M=km+1\ge2$, if $fF\ge\gamma>0$ on all inputs, then
$$\sum_j|v_j|\ge\gamma/q_M=\Theta(\gamma\sqrt M).$$
Restrict the tables to $x_c=y\oplus(|c|\bmod2)$. The target becomes parity on $(y,a)$, every bottom gate remains an LTF, and direct inputs become affine. All affine terms have zero correlation with full parity. Therefore $\gamma\le\mathbb E[fF]\le q_M\sum_j|v_j|$. Exact sums $F=cf+d$ give the same inequality with $\gamma=|c|$, by taking the full parity coefficient (changing the output orientation if needed).

In particular, $|v_j|\le U$ implies $S\ge\gamma/(Uq_M)$, and unit top weights imply $S\ge\gamma/q_M$. This is a normalization-sensitive norm lower bound, not a new balanced gate exponent. Without fixed margin, scaling all top weights makes a coefficient-norm lower bound meaningless. Bottom weight restrictions were not needed for this lemma.

## 5. Concrete upper totals, not just maximum coefficients

`experiments.py` imports `build_dpp` and measures its **finalized merged gate list**. It sums integer coefficients with Python integers and separately counts majority padding. No formulas from the report are used to infer the totals. Gcd-normalizing the bottom gates makes no difference for these cases.

| $(k,m)$ | merged $S$ | bottom $\ell_1$ | gate-output top $\ell_1$ | direct $\ell_1$ | coefficient total | majority wires incl. constants |
|---|---:|---:|---:|---:|---:|---:|
| $(2,2)$ | 31 | 268 | 712 | 88 | 1,068 | 1,230 |
| $(3,2)$ | 87 | 1,290 | 5,240 | 368 | 6,898 | 7,682 |
| $(4,4)$ | 370 | 13,100 | 75,312 | 2,144 | 90,556 | 98,195 |
| $(5,6)$ | 1,323 | 89,386 | 624,416 | 11,840 | 725,642 | 777,206 |
| $(6,10)$ | 5,072 | 680,516 | 5,363,168 | 72,064 | 6,115,748 | 6,504,289 |
| $(7,18)$ | 20,583 | 5,651,274 | 47,361,024 | 495,872 | 53,508,170 | 56,727,810 |

Here the top majority padding is one constant wire in every listed case. Bottom padding is substantial and is included only in the last column. The bias $K$ itself is excluded from coefficient weight. These are $d''$ costs, not claims of optimal majority realizations. For example at $(2,2)$ a 3-gate unrestricted sign circuit is much smaller than $d''$.

**Balanced asymptotics [PROVED from the builder].** Take $km=\Theta(N)$, $m\asymp N/k$, with integer rounding where necessary. Main ridges have $\Theta(N^2)$ gates with $O(N)$ bottom coefficient sum and $O(N)$ top coefficient. There are only $O(N)$ global quadratic/gated-product gates; these have $O(N)$ bottom sum and at most $O(N^2)$ top coefficient. Thus both bottom and gate-output top $\ell_1$ totals are $O(N^3)$. They are also $\Omega(N^3)$: a constant fraction of the ridge families have $\Theta(N)$ range and $\Theta(N)$ coefficient sum, while the $km$ gates for $x_0\sigma$ have top coefficient $\mathrm{Cov}=\Theta(N^2)$ (merging with the full-set override changes it by only $O(N)$). Direct terms and padding fit the same upper bound. Hence coefficient and multiplicity totals are $\Theta(N^3)=\Theta(n^3)$.

Cloning to remove repeated gate-output wires gives $\Theta(N^3)$ physical bottom gates. Its bottom wires are $\Theta(N^4)$: already the $\Theta(N)$ global $x_0\sigma$ gates have $\Theta(N)$ bottom wires each and $\Theta(N^2)$ clones each. The matching upper bound follows by multiplying the ridge and global-family costs separately. `results.json` includes exact unpadded cloned-bottom totals; at $(7,18)$ it is 17,306,858,640, before padding clones or fixing repeated direct inputs.

The newer subcube family in `mixed_upper/report_body.md` offers better fixed-$k$ slopes and $0/1$ bottom coefficients, but its recursive dominance weights are not automatically polynomial in $N$ uniformly in $k$. It cannot replace an actual top-norm computation. No optimality claim about any of these upper totals is made.

## 6. Primary-source check and limits of communication arguments

**[SOURCE VERIFIED]** [Kane–Williams, Theorem 1.1](https://cseweb.ucsd.edu/~dakane/depth2LTF.pdf) proves gate and wire lower bounds for ordinary Andreev against arbitrary real-weight depth-two LTF circuits. At constant advantage their published bounds are $n^{3/2}/\log^3 n$ gates and $n^{5/2}/\log^{7/2}n$ wires, up to the theorem's asymptotic exclusion formulation. The paper explicitly permits direct input wires at the output. This is the source version checked, not a claim that its gate logarithm is the latest improvement; the task's $\log^2 n$ baseline may refer to later work. Ordinary support wires are no more numerous than integer literal occurrences, so the published wire lower bound transfers immediately to integer coefficient totals and majority multiplicity wires after removal of redundant zero connections. It does **not** imply a new lower bound beyond unrestricted-real circuits.

The same paper's historical discussion distinguishes a nearly linear parity gate lower bound for MAJ-of-MAJ (Paturi–Saks) from the $\Omega(\sqrt n)$ arbitrary-LTF parity gate bound. Thus one must not transfer the latter's apparent barrier to every small-weight majority model. Under the table-to-parity restriction above, however, a table weight becomes the sum of up to $N$ coefficients on $y$, and bounded bottom weights do not remain bounded by the same parameter. Precise polynomial-weight conventions and size dependence must be tracked before invoking the stronger majority parity result.

**[KNOWN SOURCE + TRANSFER]** The original [Paturi–Saks, *Approximating Threshold Circuits by Rational Functions*](https://cseweb.ucsd.edu/~paturi/myPapers/pubs/PaturiSaks_1994_ic.pdf) proves $\Omega(M^2/\log^2 M)$ edges for depth-two parity circuits with polynomially bounded weights. This gives a useful stronger **fixed-$k$ majority consequence** omitted from the earlier mixed-sign report. Put $M=km+1$, assume $N\le M^C$ and all original bottom/top integer coefficients are at most $M^C$ for a fixed $C$. Under the parity-table substitution, a bottom or direct coefficient on $y$ is at most $NM^C$, still polynomial in $M$; thresholds can be clipped to polynomial attainable ranges. The restricted circuit has at most $(M+1)S+M$ ordinary support wires. Consequently
$$S=\Omega(M/\log^2 M).$$
In particular for fixed $k$, polynomial-weight depth-two circuits for ordinary Andreev need $\Omega(m/\log^2 m)$ gates. This beats the unrestricted parity-based $\Omega(\sqrt m)$ bound in that parameter regime. It is inherited from a known theorem, not a new asymptotic parity result; it does not beat the balanced Andreev bound. It applies to polynomial-size literal-multiset majority circuits whose coefficients/multiplicities are polynomial in $M$, and to unit unrepeated top gates with the same bottom restriction. A bottom-only coefficient bound with arbitrary real top weights does not satisfy this theorem's assumptions. The transfer carefully charges the single substituted variable $y$, rather than pretending its weight stayed at $V$.

**[SOURCE VERIFIED]** [Chattopadhyay–Mande, *Weights at the Bottom Matter When the Top is Heavy*](https://arxiv.org/abs/1705.02397) separates THR-of-MAJ from THR-of-THR using a large-sign-rank function with a small unrestricted threshold circuit. This supports the relevance of bounded bottom weights and warns against treating MAJ-of-THR, THR-of-MAJ, and THR-of-THR interchangeably. Their function is not ordinary Andreev, so their exponential separation does not give an Andreev lower bound.

**[PROVED HERE: polynomial communication ceiling, not impossibility]** For *any* two-party partition of ordinary Andreev's raw inputs, Alice sends her partial parity in each address block ($k$ bits); Bob computes $b$ and sends it back ($k$ bits); the owner of $x_b$ supplies its bit, with at most one more bit to distribute the answer. Thus deterministic communication is at most $2k+2$, even when table and address bits are interleaved. In the natural table-versus-address partition it is only $k+1$. This gives polynomial upper bounds on partition-matrix rank/sign rank via protocol rectangles. It rules out exponential-in-$n$ sign-rank lower bounds for ordinary Andreev through those partitions, **not polynomial circuit lower bounds**. Indeed the natural sign matrix, with all table sign vectors as rows and the $N$ addresses as columns, has sign rank exactly $N$: any proper subspace of $\mathbb R^N$ misses a strict orthant (take a nonzero orthogonal vector and its coordinate signs). All orthants occur as rows. Its ordinary rank is also $N$.

A bottom gate's natural-partition matrix has at most $1+\sum_a|w_a|$ distinct columns when address weights are integral: columns are determined by their address weighted sum. Therefore its ordinary rank is at most that quantity. Taking ranks of a sign-correct top score gives only a weak bound of the form $N\le O(1)+\sum_j(1+\sum_a|w_{j,a}|)$; it does not furnish $Nm/V$. This explicitly explains what this elementary communication/rank route can and cannot show, without saying that low communication precludes all polynomial lower bounds.

## 7. Experiments and open end

Run `python3 /tmp/andreev_gap/maj_sol/experiments.py`. `results.json` stores all integer totals and checks. The script exhausts all full-support $\pm1$ gates and thresholds for $M=2,\dots,7$ and matches the exact $q_M$ bound. It checks 20 seeded random signed-support unit-address gates at each of $(k,m)=(2,2),(2,3),(3,2)$, verifying rank at most one for every positive address degree at least two. These checks are sanity tests; the proofs cover all degrees and real table weights.

`tiny_exact.py` is a separate 15-second-per-instance z3 search for exact sums with arbitrary real table coefficients, address coefficients in $\{-1,0,1\}$, arbitrary real top coefficients and affine direct inputs. It checks $(k,m,S)=(1,3,3)$ and $(2,1,3)$. SAT witnesses are rechecked with exact rational arithmetic; UNKNOWN is not a lower bound. Its output is `tiny_results.json`. The completed outcomes were **UNSAT** at $(1,3,3)$ and **UNKNOWN** at $(2,1,3)$. The former establishes a new full mixed-sign, unit-address-weight exact lower bound of 4 at $(k,m)=(1,3)$; together with the supplied block-symmetric unit-weight upper construction, its exact minimum in this address-bounded model is 4. It does not establish that minimum when address magnitudes are unrestricted. The second run yields no conclusion. No solver jobs remain running.

The strongest unresolved task remains the proposed global $\Omega(Nm/V)$ exact-sum theorem. This report establishes a non-survival intermediate theorem and its precise robustness range, but does not close the balanced majority gate gap or establish a new superquadratic multiplicity lower bound beyond Kane–Williams.
