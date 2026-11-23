# Independent adversarial first review

Authors: Christian Reitwiessner

Scope: standalone-first review of `eccc_draft/paper.tex`; no changes to the shared draft. This report was written incrementally. The initial proof assessment and independent checks preceded inspection of the longer paper or existing checkers.

**Verdict: REVISE (limited repairs).** No fatal defect found in the four main theorems. Prioritized objections, independently verified proof details, and proposed repairs follow.

## Initial standalone findings

- The definition immediately before Lemma 2.2 says “for integers $\theta$” although the argument of $\varphi$ is $u$. Replace it with “for integers $u$.”
- The completed audit below checks the exact score, its compilation, the masked error estimate, and both lower-bound proofs independently.

## Standalone algebra audit

The refined score identities also require two short sums that are currently left implicit at lines 239–244:

$$
\sum_{S\ne\varnothing}\kappa_SW_S
=2N(2\alpha+1)(1+\alpha)E,
\qquad
\frac12\sum_{S\ne\varnothing}\kappa_St_S
=N(2\alpha+1)\sigma.
$$

Both follow directly by writing $k-2|S|=\sum_i(-1)^{[i\in S]}$ and using character orthogonality. These are not counterexamples: they check the missing intermediate cancellation and would make the claimed “substitution” appreciably easier to verify. The maximum odd block count is $2\alpha+1$ for both odd and even $m$, including $m=1$.

The entropy encoding handles raw top inputs correctly: their live coefficients are fixed, while all fixed input contributions and nonsplitting gate values become the one top threshold. Diagonal cube intervals are half-open and genuinely disjoint even when adjacent cubes share a vertex or have zero weights. The equal-magnitude proof's strictification is valid before reversing orientation and remains valid on every literal restriction.

## First prioritized objections

1. **Medium — abstract omits the parameter range of the advantage bound (lines 29–32).** The theorem only asserts the $\varepsilon^2$ bound for $N^{-1/2}\le\varepsilon\le1/8$, and the proof does not establish that expression uniformly as $\varepsilon\uparrow1/2$. As written, the abstract sounds unrestricted. State the range in the abstract; also restrict the fixed-error comparison to $0<\delta<1/2$. This is a statement-scope repair, not a failure of Theorem 4.1.
2. **Medium — wire sentence needs an upper/lower distinction (lines 596–599).** An upper bound $G$ on bottom gates always gives at most $nG+G+n$ wires in this model, without essential-dependence assumptions. The existing sentence is only sensible for a *lower* bound or a claim of a matching wire count. Suggested replacement: “The gate upper bound gives $O(n^3)$ wires; obtaining wire lower bounds from gate lower bounds requires additional support information.”
3. **Proof exposition — exact cancellation is too compressed for the requested easy complete proof (lines 219–244).** The identities are correct, but add the two coefficient-shift sums recorded above. Also give a one-line orthogonality identity for the quadratic sum, rather than asking the reader to expand all cross terms from scratch. No extra gate or circuit layer is missing.
4. **Proof exposition — prove the tail estimate with its stated constant (lines 377–388).** The claimed bound is true for all integer $R\ge1$, but the instruction to integrate from $R/2$ and absorb a polynomial is not a complete derivation of the displayed constant. A short valid derivation is recorded below.

## First independent calculations

`independent_checks.py` was written anew from the compact source. It checked all tables and all count vectors for $k=1,2$, $1\le m\le8$, and $k=3$, $1\le m\le5$, plus larger seeded cases, totaling **119,110** cases. All three displayed score identities, both implicit coefficient-shift sums, the closed form, and the signed margin passed. A separate explicit list of raw affine threshold gates, including their top coefficients, matched the score in **2,800** evaluations and reproduced the finite gate bound after the stated duplicate saving. Exact binomial-distribution summation tested **7,800** tail inequalities, including $R=1$ and radii beyond the support. Exhaustive table-majority checks included $L=1,2,4,8,16$. Results are in `independent_checks.json`.

## Complete repair for the tail step

Let $V=U-\mathbb EU$, $v=v_S$, and $h=R/2$. Since $|\mathbb EU|\le1/2$ and $R\ge1$, the event $|U|>R$ implies $|V|>h$, while $U^2\le2V^2+1/2$. The stated Hoeffding bound implies

$$
\mathbb E[V^2[|V|>h]]
\le(2h^2+4v)e^{-h^2/(2v)}.
$$

Consequently

$$
\mathbb E[U^2[|U|>R]]
\le(R^2+8v+1)e^{-R^2/(8v)}
\le(R^2+16v)e^{-R^2/(8v)}
\le16v e^{-R^2/(16v)}.
$$

Here $v\ge N\ge2$ and $1+t\le e^t$ justify the last two inequalities. Thus no change to the constants $16$, $64$, or the chosen radius is necessary.

## Additional actionable issues

5. **Medium — reproducibility paragraph is broader than the compact bundle (lines 609–616).** After completing the standalone audit and independent computations, I inspected `eccc_draft/verify_results.py`. It checks the raw exact construction and masked moments, but contains no literal-pairing check. The compact directory contains no second checking script. Either include and name the pairing checker in the submission artifacts, give a precise external path/link, or remove “and the pairing identities” from the description. Likewise give a repository/commit link for the earlier Lean results. This is an artifact/provenance gap, not a mathematical gap.
6. **Low — undefined historical reference (line 331).** “The earlier circuit” has no identifiable antecedent in this standalone paper. Delete that sentence or replace it with a precise citation. The majority calculation is proved locally and needs no historical reference.
7. **Low — quantifier and convention cleanup.** At line 329, start “For $L\ge2$, conditioning …”; the sum-of-$L-1$-signs explanation is not valid for $L=1$, although the separately stated $p(1)=1$ is correct. Explicitly say $L\ge2$ is even because $L$ is a power of two. At line 533 define sign coordinates, e.g. $z_i=2a_i-1$ and $w_i=2a'_i-1$, so the common *positive* scale in line 555 and the orientation reversal have a stated convention. The proof works with this convention.
8. **Low — bibliography typo.** `K. Kabanets` at line 630 should be `V. Kabanets` (Valentine Kabanets). The authors' [paper page](https://www.cs.sfu.ca/~kabanets/Research/PTF-restriction.html) confirms the name.
9. **Low — support-wire conclusion omits the top's edges in its explanatory sentence (line 417).** The asymptotic result is correct, but say “There are at most $nG+G+n$ wires for $G$ bottoms” rather than accounting only for inputs to bottoms. The parameter regime absorbs the additive terms.

## Proof-by-proof assessment

### Section 2: Fourier inversion and staircases

All three lemmas are correct. In particular $N=2^k$ is even since $k\ge1$, so every $X_S$ is even; the shift identity is valid also for negative arguments. The staircase lemma counts interval *length*, not the number of integer points, so $2N+m|S|$ and $m|S|$ are right. The resulting $2N^2+kmN$ bottom-gate bound includes redundant gates for $S=\varnothing$, which is harmless. The only error is the $u/\theta$ typo noted above. The displayed affine raw form rules out an extra layer.

### Section 3: refined exact construction

No false identity or missing layer found. A useful way to verify the largest quadratic identity is to define, **only for this verification**, $\beta_c=x_c(1+\alpha[c\text{ is a unit address}])$ for $c\ne0$ and $T=\sum_{c\ne0}\beta_c=z+\alpha E$. For distinct nonzero $c,d$,

$$
\sum_S[S\cdot c\text{ odd}]=N/2,
\qquad
\sum_S[S\cdot c\text{ odd}][S\cdot d\text{ odd}]=N/4.
$$

The diagonal sum is $N/2$. Thus

$$
8\sum_S(W_S^2+W_St_S)
=2N\left(T^2+T\sigma+z+(2\alpha+\alpha^2)E
 +(1+\alpha)\sum_i x_{e_i}s_i\right),
$$

which is exactly the displayed identity since $w=2T+\sigma$. This derivation is a suggested optional replacement for the vague instruction to expand squares; the extra variables need not enter the final paper's permanent notation.

The sign margins check separately:

- If $b=0$, $x_0=0$ gives $P\ge2N$; $x_0=1$ gives $P\le-2N$.
- If $b=e_i$, odd $s_i$ lies in $[1,2\alpha+1]$. For $x_{e_i}=0$, $P/N=2(1+\alpha)-s_i\ge1$; for $x_{e_i}=1$, $P/N=-s_i\le-1$.
- All other addresses give $P=\pm N$.

This includes $m=1$ with $\alpha=0$, both parities of $m$, and $k=1$ where the third case is empty.

The staircase jump at odd $\theta$ is exactly $-8\theta+\kappa_S$; the jump at even $\theta$ is zero. The argument range is $[0,N+2\alpha|S|+m|S|]$. The squares need $R+km$ thresholds, and $B=n+2>km$ makes every gated product vanish when its table selector is zero. The zero-address correction follows from

$$
\sum_{S\ne\varnothing}\lfloor t_S/2\rfloor
=\frac N4\bigl(\sigma-[b\ne0]\bigr).
$$

The duplicate even-level gates with $S=[k]$ really have identical raw affine forms and thresholds. Their weights can be added without changing the circuit. Combining the ridge/floor counts and adding $R+3km-\lfloor km/2\rfloor$ gives precisely (2), the claimed finite bound. Every address weight in this construction is nonnegative, so the coherent-class membership is also correct.

At exact balance, $k\mid2^k$ forces $k$ to be a power of two and $m=2^k/k$ is even, including the smallest cases. Substitution gives the **displayed upper-count expression**, with the top added,

$$
\frac54N^2-\frac12kN+6N-2k-1
=\frac5{16}n^2-\frac n4\log_2(n/2)+3n-2k-1.
$$

Hence the claimed second-order term is right. Floor balance introduces only $O(Nk)$ change. All weights remain integers: in particular $4C/N=4(R+4)$ is integral. Bottom coefficients and thresholds are $O(n)$; the coefficient totals can be bounded by $O(n^3)$. No finite gate-count defect was found.

### Section 4: approximation and endpoints

The majority formula and all threshold conventions check out. For even $L$, the pivotal probability is $2^{-L}\binom{L}{L/2}$. The lower bound is a standard central-binomial estimate, not a new proof claim. If complete elementary details are desired, put $c_h=4^{-h}\binom{2h}{h}$: $c_1=1/2$ and

$$
\frac{c_{h+1}}{c_h}=\frac{2h+1}{2h+2}\ge\sqrt{\frac h{h+1}},
$$

which proves $c_h\ge1/(2\sqrt h)$ by induction.

For $q<N$, $L$ is even and $P_*$ lies in $4q\mathbb Z$. The vote is $[-P_*\ge2q]$, so a zero score outputs zero as promised. Every score is distance at least $2q$ from this threshold. For $q=N$, $L=1$, $P_*=\pm2N$, and the threshold must change to zero, as the paper correctly does. Equality in the error event is harmless: disagreement implies $|P_z-P_*|\ge2q$ in both cases.

For Part 2, the allowed interval is nonempty only when $N\ge64$. Its smallest endpoint gives $q=32$. Since $32\varepsilon^2N\le N/2$, the least allowed power of two actually satisfies $q\le N/2$, a stronger fact than $q\le N$. Thus Part 2 never silently uses the wrong tie convention at $q=N$. The generic argument and Part 1 nevertheless cover $q=N$ correctly. Radius rounding contributes only $O(q)$ gates. At very small $\delta$, radii can exceed the full support; the construction then becomes exact, so there is no endpoint obstruction.

The independence argument is sound and does **not** require independent Walsh coefficients. Given $x,a$, separate masks are independent even when their address supports overlap. Their marginal shifted-binomial laws do not depend on $a$. The conditional mean error is a table-dependent factor times $(-1)^{t_S}$, and a block in $S\triangle T$ has unbiased parity because $m\ge1$. This proves the vanishing cross moments. The diagonal estimate uses only $(u+v)^2\le2u^2+2v^2$ and the tail lemma, giving the stated $64(q-1)v$ factor. Markov's inequality gives the $16v/q$ factor, and averaging fixes a *single* mask collection for the complete uniform input distribution. No hidden input-dependent advice occurs.

### Section 5: coherent lower bound

The entropy encoding is injective: knowing $I$, its restricted Boolean gates, and the top threshold rank determines the entire restricted truth table, hence $x$. Normal vectors and live raw top coefficients are fixed after choosing the circuit and cube. Constant bottom values, raw table terms, and fixed address terms all alter only the top threshold. The counts $2^k-1$ and $2^k+1$ correctly include ties and constants. The use of $\log_2(G+1)$ rather than $\log_2G$ avoids a $G=0$ exceptional definition. No precision assumption on real weights is needed.

The diagonal lines partition *cubes*, not vertices; vertex overlap causes no double counting. For adjacent cubes, $q^+=(q+\varepsilon)^-$ exactly, and the half-open score intervals are disjoint. Zero weights give empty intervals or shared endpoints, not duplicate crossings. There are exactly $m^k-(m-1)^k$ line starts, also at $m=1$. The final asymptotic split at $G\ge N^2$ is valid; in the other case the integrality of $G$ gives $G+1\le N^2$ and hence $\log_2(G+1)\le2k$. No unmentioned large-$m$ assumption is needed for the finite self-consistent bound.

### Section 6: full-support equal-magnitude lower bound

The table restriction produces parity on $d=m\lfloor k/2\rfloor$ selected bits. If $k$ is odd there is indeed an ignored block available to fix, leaving equal numbers of selected and ignored bits. A single positive score shift smaller than the least magnitude of a negative-class score makes the original top gate strictly correct on the finite domain; subsequent global orientation reversal and every literal restriction preserve strictness. Raw top terms stay affine and have zero full-parity correlation because $d\ge2$.

Each nonzero normal has all restricted coefficients nonzero only at the unique pairing pattern $t_i=\sigma_i\tau_i$. Nonzero coefficients are merely a *necessary* condition for dependence; the proof correctly uses “at most one,” so gates rendered constant by large thresholds do not cause trouble. With no full-dependent bottom, every top summand has zero full-parity correlation, contradicting strict sign correctness. The pigeonhole conclusion $2^d$ is valid. The all-zero normal exception and the unequal-magnitude counterconstruction are handled correctly. For a stronger local explanation of why omitted coordinates matter, cite the Section 2 circuit for the *whole* lookup function, rather than just the selected-bit parity example at lines 577–578.

## Known standard ingredients and citations, separate from new-proof issues

- The cited baseline is real: [Kane–Williams, Theorem 1.2 and Section 5.2](https://arxiv.org/pdf/1511.07860) state the $O(n^3/\log n)$ threshold upper bound and the separate quadratic modular-basis bound. Their definition permits raw inputs at the top, so the circuit-model comparison is fair. Their Theorem 1.1 gives the quoted fixed-advantage gate/wire exponents; their Section 4 gives the concentration-window parity construction. These checks support the scoped comparison, not an exhaustive “best known” or priority claim.
- Fourier orthogonality and threshold telescoping are standard and are nevertheless proved here. [Hansen–Podolskii, proof of Theorem 5](https://eccc.weizmann.ac.il/report/2013/021/download/) explicitly uses exact level tests for bounded integer forms and converts them to thresholds. A pinpoint citation there, and to HMPST's symmetric-function proposition, would be better than unqualified whole-paper citations. No external standard theorem is doing unacknowledged work in the refined score.
- The subgaussian/Hoeffding estimate and central-binomial bound are standard facts. The new part needing scrutiny is their use in the masked lookup argument; that use checks out. The complete constant derivation and optional binomial induction above remove any need for readers to look these two facts up.
- [Chen–Santhanam–Srinivasan, Section 2.4](https://theoryofcomputing.org/articles/v014a009/v014a009.pdf) defines a generalized Andreev function; the paper is right to distinguish it from independent-table lookup. [Potukuchi's paper](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.FSTTCS.2019.25) concerns finite-field polynomial-graph containment, so the stated distinction is also right. KKL and IPS serve as background attribution, not black-box lemmas in the new lower bounds.
- The restrained novelty wording at lines 108–109 should be retained. This audit does not establish exhaustive priority. It establishes that the claimed comparison with the named KW construction is accurate and that the restricted lower bounds are not presented as unrestricted improvements.
- The formalization disclaimer at lines 613–616 is properly scoped: it does **not** claim the refined constant, the masked mean-square result, or either restricted lower bound is Lean-verified. Only after the standalone audit did I inspect the longer source's formalization section, which identifies the earlier `Andreev.lean`, `AndreevWindowed.lean`, and `AndreevAverage.lean` work. The [earlier exact-construction PR](https://github.com/cslib-community/complexitylib/pull/2813) describes the $3n^2/4$ construction and distinguishes the old windowed construction. I did not rebuild or kernel-audit those external Lean files, and no stronger formalization assertion should be inferred from this review.

## Final computation record and limits

In addition to the first checker, `restriction_checks.py` independently tested **354,304** mask identities on actual raw-bit/mask assignments. Exact integer summation of conditional mask errors gave zero for every cross-character pair at $k=2$, $m=1,2,3$, and radii $1,2,3,5$. It also checked **7,430** threshold/cube cases with unequal coherent weights and zero weights, including the actual partition into diagonal lines, and **112,320** literal-pairing/correlation cases for $2\le d\le5$. All passed. Results are in `restriction_checks.json`.

These are finite falsification attempts, not universal proofs. The all-size justifications are given in the mathematical audit above. The exact score and raw gate computations use integer arithmetic; the tail experiment evaluates exact binomial probability formulas in floating point, with ample slack. The mask cross-term computations use exact integer sums. The existing checker was read only after these independent checks were written and completed; it was not used to generate them.

Afterward, a search of the wider repository did locate older pairing checks, e.g. `research_backup/experiments/swarm/up2/checks.py`. This narrows objection 5 to **submission discoverability and packaging**, rather than absence of any such computation. Include a named artifact or link if keeping the present reproducibility sentence.

## Notation, locality, and length

The present PDF has **10 pages**, confirmed with `pypdf`; its existing build log likewise reports 10 pages. Thus the delivered PDF is currently within the requested 8–10-page limit, although the task called the initial version nine pages. The log contains no overfull-box warning. I did not rebuild or change the shared draft.

Section-local reuse is mostly well signposted. Keep $N,k,m,n$ global, but avoid adding permanent symbols to repair the two compressed arguments. Specific simplifications:

- Remove $Y_S$ and define $W_S=\sum_{c:S\cdot c\text{ odd}}x_c+\alpha\sum_{i\in S}x_{e_i}$ directly; $Y_S$ is used only in its definition and the ensuing prose.
- Drop the unused macro `\THR` and unused theorem environments if convenient; this is source cleanup only.
- Define the top vote directly as $[-P_*\ge2q]$ for $q<N$ and $[-P_*\ge0]$ for $q=N$, alongside the majority discussion. This avoids an implicit sign-to-bit conversion and keeps ties local.
- Replace “a function $g_S$ of the table alone” with “a function $g_S:\mathbb Z\to\mathbb R$ independent of $a$.” Its argument is already $X_S$; the current prose is valid but less precise.
- In the entropy proof, write the reduced top sum as $\sum_{j\in I}v_jg_j$ immediately after absorbing constant gates. The current unrestricted $\sum_j$ is intelligible but leaves a needless indexing question.
- Prefer $\rho_j$ to $G_j$ for the scale of the full-support normal; this avoids visually reusing the preceding section's gate-count symbol $G$. Cross-section reuse of $q,z,R$ is otherwise explicitly local and not a correctness issue.
- State $x_0=x_{(0,\ldots,0)}$ at the first exceptional-address correction if targeting readers new to this notation.

To add the two coefficient-shift sums and the tail derivation without exceeding 10 pages, cut the repeated explanation of the raw affine form at lines 170–172, the dangling historical sentence at line 331, and some of the unrelated-model discussion in the introduction. Do not save space by deleting the raw-gate compilation, the mask conditional-expectation argument, or the raw-top terms in the lower bounds: those are essential to reviewability.

## Final verdict

**REVISE — limited statement, provenance, and exposition repairs; no fatal mathematical defect found.**

All four main theorem arguments survived the independent all-size audit and finite attempts to falsify them. The abstract's missing accuracy range and the ambiguous wire sentence should be fixed before release. Add the short exact-cancellation and tail-constant derivations to meet the user's requirement of easy, complete proofs; repair the small notation errors and artifact references. These changes do not require changing the $5/16$ constant, finite gate bound, approximation rates, or either restricted lower bound. No shared draft edits, posts, installations, or subagents were used.
