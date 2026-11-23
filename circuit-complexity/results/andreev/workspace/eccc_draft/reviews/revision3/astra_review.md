# Third review and substantive revision proposal

Authors: Christian Reitwiessner

Date: 2026-11-11. Reviewed source: `eccc_draft/paper.tex` and `paper.pdf`, copied to `reviewed_source.tex` and `reviewed_source.pdf` in this directory. I assessed the arguments independently before reading the two previous reports. No shared source, PDF, or checking-script output was modified. No subagents were used.

## Recommendation

**Make a substantive revision, not another round of local copy edits.** I found no fatal mathematical defect in the four original theorem arguments. However, the approximation proof can be made **explicit and deterministic without random masks**, and its circuits can be made **sign-coherent**. This is a mathematical strengthening, not just a shorter presentation. It also removes the mask-selection open question and gives the paper a more coherent main result: exact versus average-case complexity in the same gate class.

A complete proposed replacement is in [paper.tex](/tmp/andreev_gap/eccc_revision3/paper.tex), with a compiled [paper.pdf](/tmp/andreev_gap/eccc_revision3/paper.pdf). It is **10 US-letter pages, 11pt, with one-inch margins**, including both appendices and references. It retains all four original conclusions and all proofs. The refined exact constant moves to Appendix A; the incidental full-support result moves to Appendix B. There are no overfull boxes or unresolved-reference warnings in the build log.

The most important independently usable replacement is [unmasked_approximation.tex](/tmp/andreev_gap/eccc_revision3/unmasked_approximation.tex). Integrate that argument even if rejecting the larger rewrite.

## 1. Strongest finding: the random masks are unnecessary

This applies to the original Section 4, beginning at line 310 of the snapshot. The original mask proof is valid, but it proves a weaker existence statement than the score construction actually provides.

### The reusable symmetry lemma

Let $v_c=(-1)^{x_c}$ be independent uniform signs and

$$X_S=\sum_{c\in\{0,1\}^k}(-1)^{S\cdot c}v_c.$$

For distinct characters $S,T$, an odd function $g$, and any function $h$,

$$\mathbb E_x[g(X_S)h(X_T)]=0.$$

**Complete proof.** Choose $u$ such that $(S\triangle T)\cdot u$ is odd. The signed permutation

$$v'_c=(-1)^{T\cdot u}v_{c\oplus u}$$

preserves the product-uniform law. For every character $U$ it gives

$$X'_U=(-1)^{(T\triangle U)\cdot u}X_U.$$

In particular $X'_S=-X_S$ and $X'_T=X_T$. The expectation is its own negative. This also covers the empty character, although the approximation leaves that character exact.

Do not substitute the false claim that Walsh coefficients are independent. Ordinary covariance orthogonality would also be insufficient for nonlinear truncation errors. The signed-permutation symmetry is the actual reason the stronger conclusion holds. The lemma is elementary; I would not advertise the symmetry itself as a novel result without further literature evidence.

### Exact substitution in the approximation construction

Keep $q=2^r$, the partial vote $P_*$, the symmetric truncation $f_R$, the thresholds, and every numerical constant. Replace the random-mask definitions by

$$D_S=t_S-\lfloor m|S|/2\rfloor,
\qquad\eta_S=(-1)^{\lfloor m|S|/2\rfloor}.$$

Use the explicit score

$$P_R=2X_\varnothing+
\sum_{\varnothing\ne S\subseteq[r]}
\eta_S\bigl(f_R(X_S+D_S)+f_R(X_S-D_S)\bigr).$$

As before, $f_R(u)=(-1)^u u[|u|\le R]$, and replacing $f_R$ by $\varphi(u)=(-1)^u u$ gives exactly

$$P_*=2\sum_{S\subseteq[r]}X_S(-1)^{t_S}.$$

Fix an arbitrary raw address input $a$. Both $f_R$ and $\varphi$ are odd; consequently

$$e_S=\eta_S\bigl(f_R(X_S+D_S)+f_R(X_S-D_S)\bigr)
-2X_S(-1)^{t_S}$$

is an odd function of $X_S$ alone. The symmetry lemma, **conditional on this fixed $a$**, implies

$$\mathbb E_x\left[\left(\sum_S e_S\right)^2\middle|a\right]
=\sum_S\mathbb E_x[e_S^2\mid a].$$

Under uniform address inputs, each $D_S$ has exactly the same shifted binomial marginal used in the original argument, independent of $X_S$. Thus its existing tail calculation gives, with $v=N+rm/4$,

$$\mathbb E_{x,a}(P_R-P_*)^2
\le64(q-1)v\exp(-R^2/(16v)).$$

The existing $2q$ margin then gives disagreement with the partial vote at most

$$\frac{16v}{q}\exp(-R^2/(16v)).$$

Therefore the original choice

$$R=\left\lceil4\sqrt{v\log\frac{16v}{q\delta}}\right\rceil$$

proves exactly the same two approximation rates for a specified deterministic circuit. The gate count remains $4(q-1)(R+1)$ bottoms. Radius may be capped at $N+km$, where the approximation is exact on every attainable affine-form value.

In fact **every fixed collection of the original masks** satisfies the same mean-square bound: after fixing masks and $a$, the error is still odd in $X_S$, and each masked count has the same marginal law under uniform $a$. Choosing all masks zero is simply the cleanest construction.

### Consequences that must be propagated through the paper

1. Replace “masked staircases” with “symmetric truncation” or “orthogonal odd errors.” Remove mask independence, conditional mask means, and averaging over circuits.
2. Replace the nonuniform mask-existence qualification in the theorem with the explicit construction above. No random seed needs to be found.
3. Delete the mask-selection open question. It is resolved by this argument.
4. State that the approximate circuits are sign-coherent: $X_S+D_S$ has address weights $+1$ on active blocks, and $X_S-D_S$ has weights $-1$; inactive blocks have weight zero. All table weights remain unrestricted in the model.
5. Highlight the new structural comparison: within sign-coherent circuits, the exact exponent is $2$ and the fixed-error exponent is $3/2$, both up to logarithms. The lower bound is exact because count-grid cubes do not sample uniform raw addresses.

This strengthening is specific to the independent uniform input table. An encoded/generalized Andreev table need not have the signed-permutation symmetry used above.

## 2. What should be in the main paper

The original layout treats a constant refinement, an approximation theorem, and two rather different restricted lower bounds as roughly equal headline contributions. It also asks the reader to absorb the most complicated algebra before reaching the more reusable approximation insight. Passing two correctness reviews is not a reason to retain this organization.

The replacement has the following spine:

- **Affine-form compilation.** A numerical score that is a sum of univariate functions of raw integer affine forms compiles directly into bottom thresholds, at a cost equal to its nonzero jumps. This says exactly why no additional circuit layer is hidden. The telescoping proof is included.
- **Grouped Fourier lookup.** Fourier inversion plus $X(-1)^t=\varphi(X+t)-\varphi(t)$ gives quadratic size immediately. The empty character is affine, so the simple finite count improves harmlessly to $2N(N-1)+kmN$ bottoms. Full derivation appears in Theorem 2.2 of the proposal.
- **Odd-error orthogonality.** The new standalone symmetry lemma explains the mean-square estimate. Symmetrization, rather than masking, is the essential design choice.
- **Restriction demand versus capacity.** Separate the information needed after a restriction from the fraction of restrictions a single gate can cross. This makes the coherent proof reusable without suggesting that an arbitrary restricted threshold has the same normal at different cubes.

The refined $5/16$ construction belongs in **Appendix A**, with its full all-size score, cancellations, exceptional-address margins, and raw-gate count. I retained that proof and added a short explanation of its purpose: replace two staircases by one, aggregate the resulting quadratic corrections, and repair a few addresses using sign margins. The leading constant remains visible in the abstract; its optimization no longer blocks the main argument.

The full-support equal-magnitude result belongs in **Appendix B as a proposition**. Its proof has a worthwhile short lesson, but the class is too fragile to carry the paper's main narrative. Both zero supports and a change from magnitude one to magnitude two defeat the exponential conclusion. The proposal gives a separate missing-variable parity lemma with its classical attribution, then the pairing count. This separates the old dual obstruction from the particular application.

The proposed source retains complete proofs and real-weight qualifications; it does not obtain 10 pages by shrinking the font or sending essential arguments to an unprovided supplement. I removed the unrelated polynomial-containment “Andreev's Problem” discussion and the nonessential KKL background sentence. The parent's broader literature audit can restore a targeted KKL comparison if useful. The two function definitions in CSS differ from this paper in both the table encoding and the address extractor; the proposal says both.

## 3. The restriction abstraction, precisely

The original entropy proof is correct, but its central economy deserves emphasis: **the circuit is fixed, so table changes move thresholds, not the live-variable normals or top weights.** Counting all possible threshold functions would discard this information.

The replacement lemma considers a fixed circuit with an $N$-bit table $x$ and $h\ge1$ other live bits $z$, where the resulting function of $z$ determines $x$ injectively. If $D(x)$ bottoms are nonconstant in $z$, then

$$\mathbb E D(x)\ge
\frac{\max\{0,N-h-1-\log_2(G+1)\}}
{h+\log_2(G+1)}.$$

**Complete proof.** A fixed normal has at most $2^h-1$ nonconstant threshold cuts on $2^h$ points. Specify the $D$ active gates, one cut for each, and the top threshold rank. After constant gates and direct table inputs are absorbed into that threshold, its coefficients are fixed; it has at most $2^h+1$ cuts. The description determines the function and therefore $x$. Hence

$$
N\le H(D)+\mathbb E\log_2
\left[\binom GD(2^h-1)^D(2^h+1)\right]
\le\log_2(G+1)+\mathbb ED\bigl(\log_2(G+1)+h\bigr)+h+1.
$$

Rearrange, using $D\ge0$. The hypothesis $h\ge1$ avoids a degenerate zero denominator in a purported general statement.

Apply this with $h=k$ at each count-grid cube. For the capacity side, a block-coherent gate is monotone on each oriented diagonal chain of cubes. Consecutive half-open crossing intervals are disjoint, including at threshold equality. The number of chains is $m^k-(m-1)^k$. Thus

$$D=D_0,\qquad p=1-(1-1/m)^k,\qquad Gp\ge D.$$

For the full-support appendix, the same counting template has $D=1$ by the parity dual and $p=2^{-d}$ by literal cancellation. I recommend the simple counting template in prose, not a heavyweight new definition system.

## 4. All-size audit of the original four claims

These are checks of the supplied mathematical arguments, not a claim of formal certification.

**Refined exact upper bound.** The diagonal/off-diagonal character counts correctly handle $c=d$ separately; when $k=1$ there are no distinct nonzero addresses, so the $N/4$ count creates no exceptional case. The two coefficient-shift sums have the stated values. At $b=e_i$, the largest possible odd block count is exactly $2\lfloor(m-1)/2\rfloor+1$, including $m=1$. At $b=0$, $C=N(R+4)$ gives the required strict sign margin. In the raw implementation $B=n+2>km$ correctly gates the products with a table bit, the even-level overlap is a genuine shared threshold, and $N/2$ and $4C/N$ are integers. Polynomial weight bounds survive the correction. Exact balance forces even $m$, and floor balance only changes the leading comparison by $O(Nk)$. I did not change the refined all-size bound.

**Approximation.** The original masked argument is sound; the issue is unnecessary randomization. For the replacement, the signed-permutation proof is all-size, works for the empty character too, and only uses table-uniformity. Centering has mean at most $1/2$ for odd block sizes. The variance proxy $N+m|S|/4$ and tail constants are unchanged. The case $q=N$ has score margin $2N$, while $q<N$ has an even cell size and score lattice $4q\mathbb Z$; the offset $2q$ handles ties. The $L=1$ vote is treated separately. The chosen least power of two exists in the stated advantage range, and direct top wires are included in the wire upper bound. No extension to encoded tables is asserted.

**Coherent lower bound.** Arbitrary real weights only affect the order of the finitely many live-cube values, not their number. Constant gates and all direct table/top inputs are correctly absorbed or retained. Zero address weights may be assigned either orientation. The chain count remains valid for $m=1$, with $(m-1)^k=0$. If $G<N^2$, integrality gives $G+1\le N^2$, justifying the logarithmic simplification. The bound is on bottom gates, and it is exact-computation only.

**Full-support lower bound.** Strictification must precede reversing the score orientation, as in the original proof. A nonzero paired coefficient does not guarantee functional dependence, but only the necessary direction is used: a zero coefficient forces a missing variable. Thus “can serve at most one restriction” is valid even for constant or saturated gates. The hypothesis $d\ge2$ is essential to remove raw affine top terms by orthogonality. Pure-table gates become constants. Both the support and magnitude qualifications are necessary, with actual quadratic counterconstructions already supplied.

**Classification of findings.** I found no counterexample or broken all-size implication in the four original statements. The new deterministic/coherent approximation is a strengthening. Moving proofs to appendices, changing the title, removing irrelevant references, and adding the reusable lemmas are exposition and scope recommendations. They should not be presented as repairs to false theorems.

## 5. Targeted primary-literature check

The parent is doing the broad audit. I independently checked the following sources for the claims relevant to this rewrite; this is not an exhaustive priority search.

- **Kane–Williams:** verified Theorems 1.1–1.2 and Sections 4, 5.2, and 6. The proposed comparisons and ingredient attributions use those precise locations. In particular, do not advertise central-window parity approximation or the table-majority endpoint as new. Say “improves the upper bound stated by Kane and Williams,” not “first quadratic” or an exhaustive “previously best known.” [Primary paper](https://arxiv.org/pdf/1511.07860).
- **Hajnal–Maass–Pudlák–Szegedy–Turán:** Proposition 2.1 is the correct symmetric-function construction. The general real-valued finite-difference compilation rule is proved in our text rather than attributed verbatim to that proposition. [Author-hosted primary PDF](https://igi-web.tugraz.at/people/maass/psfiles/47.pdf).
- **Hansen–Podolskii:** Theorem 5 of the ECCC version uses level tests of bounded integer forms; Lemma 6 supplies polynomial-overhead monotone-bottom simulation. This is relevant context for coherence, but does not imply a size-preserving simulation or an unrestricted near-quadratic lower bound. The proposal identifies which version its locators refer to. [ECCC TR13-021](https://eccc.weizmann.ac.il/report/2013/021/download/).
- **Impagliazzo–Paturi–Saks:** Lemma 2.1 gives the oriented monotonicity ingredient. The fixed-normal table-information count and the count-grid capacity application need their own proofs; the proposal supplies both. [Primary paper](https://cseweb.ucsd.edu/~paturi/myPapers/pubs/ImpagliazzoPaturiSaks_1997_siamjc.pdf).
- **Minsky–Papert:** I inspected the cached primary scan, printed pages 56–58, Theorem 3.1.1 and Corollary 1. They explicitly give the full-support-predicate necessity for parity. The new standalone missing-variable lemma is a short orthogonality proof of that classical fact, not a claimed new obstruction. The literal-pairing application must be distinguished from it. [Primary scan source](https://media.githubusercontent.com/media/dimitarpg13/deep_learning_and_neural_networks/main/literature/books/Minsky-and-Papert-Perceptrons-1969.pdf); the web fetch failed in this pass, so I used the already cached PDF from the earlier review.
- **Chen–Santhanam–Srinivasan:** Section 2.4, equation (2.1), uses $\operatorname{Enc}(x_1)_{E(x_2)}$. Both the independent table and the simple parity address have changed. Its exponentially small-correlation results must not be read as statements about the ordinary function here. [Primary journal paper](https://arxiv.org/pdf/1806.06290).

Targeted searches did not identify a primary source establishing the precise proposed deterministic approximation construction or the specialized coherent bound. That negative result is not evidence of novelty. The earlier review's conclusion that no proof blocker remained is compatible with my audit, but its recommendation to retain the mask-existence qualification is superseded by Section 1 above.

## 6. Validation and integration notes

The new independent [check_unmasked.py](/tmp/andreev_gap/eccc_revision3/check_unmasked.py) passed:

- 7,268 exact signed-permutation checks and 140 nonlinear pair-moment checks, including an even/non-odd second test function;
- 14,820 conditional cross-moment/mean-square checks;
- 514,200 full score/table/count inputs, including partial-vote identities, full lookup, and threshold ties;
- 671 finite-difference compilation values;
- 135 exact majority-agreement checks and 135 mean-square tail-bound checks.

Table sums, moments, majority probabilities, and threshold calculations use exact integer arithmetic. Only the comparison with the exponential tail bound uses floating point. Address count inputs are weighted by their binomial multiplicities when uniform-address probabilities are evaluated. These tests are finite falsification attempts; the symmetry proof is the all-size justification.

The proposed PDF was compiled locally with `/tmp/andreev-pdf-tools/tectonic --keep-logs paper.tex` in this separate directory. The Fontconfig environment message did not stop the build; the TeX log contains no overfull-box or unresolved-reference warning. Both the original and proposed PDF were inspected; selected dense and boundary pages were rendered for visual review. The proposed paper fits the original format without negative spacing hacks.

For minimal integration, replace only the original approximation mask definitions and cross-term subsection using `unmasked_approximation.tex`, propagate the explicitness and coherence conclusions, and remove the obsolete open question. For the stronger editorial improvement, use the complete proposed source as a starting point and merge the parent's literature findings. Its numerical refined bound is unchanged. The earlier simple-construction Lean claim was omitted from the rewrite to keep proof-status metadata separate; this review did not rerun Lean or certify that formalization. If restored, its stated count must remain the earlier formalized one, not the slightly trimmed empty-character count or the new approximation theorem.

**Final assessment:** the original claims survived this audit, but the paper can be materially stronger and clearer. The highest-value change is the deterministic, sign-coherent approximation proof; the highest-value structural change is to let the short compilation and restriction principles carry the main paper, with constant optimization and the fragile full-support class in fully proved appendices.
