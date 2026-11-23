# Second independent review of the compact ECCC draft

Authors: Christian Reitwiessner

Review date: 2026-11-11. Draft: `eccc_draft/paper.tex` and `paper.pdf`.

## Review protocol and status

Review completed. The initial mathematical and presentation assessment was made from the compact draft alone, before reading `reviews/round1.md`, `reviews/related_work.md`, the longer draft, or previous checking scripts. No draft files were edited. Prior findings, attribution, and reproducibility artifacts were audited subsequently.

## Independent assessment (before previous reviews)

The source specifies 11pt and one-inch margins. The four theorem statements and their proofs were checked separately, including finite parameter cases, direct raw-input terms at the top, and the assumptions needed for each restricted lower bound.

### Initial mathematical conclusions (recorded before prior reviews)

I found no substantive flaw in any of the four all-size arguments on the independent first pass.

- **Theorem 3.1:** the three quadratic/character identities and the three coefficient-shift identities have the right coefficients. At $b=e_i$, the largest possible odd count is exactly $2\alpha+1$, giving the stated margin. The last correction is an identity of raw-input staircases, not a hidden parity layer. The known overlap is precisely the even-level $\sigma$ gates. At exact balance, substituting $\alpha=m/2-1$ into (2) gives the explicit upper bound $5N^2/4-kN/2+6N-2k-2$ bottoms; adding the output gate agrees with the displayed asymptotic expansion. Floor balance changes the leading comparison by $O(Nk)$.
- **Theorem 4.1:** mask independence is used conditionally on the entire input, while address-character orthogonality kills the conditional mean cross terms afterward; independence of Walsh coefficients is not needed. The centered variance proxy and the constants $16$, $64$, and $16v/q$ check out. The offset $2q$ handles ties when $q<N$, and the case $q=N$ has score margin $2N$. The stated $\delta$ range and the small-advantage range are valid, including the rounding of $q$ and the direct raw top wires.
- **Theorem 5.1:** the description of a cube function remains valid with arbitrary raw table and address inputs at the top. The top threshold rank is counted after fixing the splitting gates and their functions. The half-open crossing intervals are disjoint even at equality and with zero block weights. The implicit finite bound and its floor-balanced asymptotic consequence follow.
- **Theorem 6.1:** strictification works before orientation reversal. Each paired literal restriction cancels at least one coefficient for all but one sign pattern per bottom gate; a functionally constant gate only weakens its usefulness. The parity correlation argument includes raw top terms exactly when $d\ge2$. Pure-table gates contribute nothing. The full-support unequal-magnitude counterconstruction is also valid.

### Initial presentation observations

The PDF has ten US-letter pages and the source uses 11pt with one-inch margins. All ten pages have been read as a standalone document. Sections 4–6 are reasonably local; the exact construction on page 4 is the densest part. Its large algebra display would benefit from one short explanation of the purpose of the coefficient shifts, not more variables or another lemma. The simple raw-affine expansion is unnecessarily repeated immediately after equation (1) (lines 171–173); that space can fund a local explanation elsewhere.

A small notation-scope inconsistency remains: lines 120–124 say that $X_S,t_S$ are used only in Sections 2–4, but Section 6 reuses them (and $\varphi$) in the unequal-magnitude counterconstruction. Reintroduce them there by a short reference to Section 2 and soften “Only in” to “In.” This is a readability correction, not a mathematical defect.

Independent finite checks, attribution verification, and the comparison with earlier reviews follow below; those have not yet informed these conclusions.

## Check against the first review and related-work audit

The earlier reports were read only after the independent assessment above was recorded. The substantive round-one objections are now fixed in the compact source, not merely acknowledged in a status file:

| Previous issue | Revised location | Assessment |
|---|---|---|
| Abstract's missing advantage range and fixed-error endpoint | lines 29–34 | Fixed: the $\varepsilon$ interval is explicit and the comparison uses $0<\delta<1/2$. |
| Confusion between gate-to-wire upper bounds and lower bounds | lines 613–616 | Fixed: $O(n^3)$ wires follows from the gate upper bound; support information is needed for the lower-bound direction. |
| Missing coefficient-shift sums and quadratic counting guidance | lines 232–251 | Fixed: both shift sums and the diagonal/off-diagonal character counts are displayed. I checked their algebra independently. |
| Unexplained tail constant | lines 393–399 | Fixed: the centered-variable argument, integrated tail, and final absorption are explicit. The constants work. |
| Pairing checker missing from the submission bundle; Lean reference unspecified | lines 626–635 | Fixed: both named scripts exist in `eccc_draft/`, and the exact-construction PR is linked. Rerun/provenance details below. |
| Dangling “earlier circuit” comparison | lines 324–339 | Removed. |
| $L=1$ exception, evenness of $L$, and sign-coordinate convention | lines 332–339, 549–560 | Fixed, including the separate vote threshold and strictification order. |
| Kabanets's initial | line 652 | Fixed to V. |
| Raw top edges omitted from wire explanation | lines 428–430 | Fixed: $nG+G+n$ explicitly includes both kinds of top edges. |
| $\varphi(u)$ defined “for integers $\theta$” | line 137 | Fixed to $u$. |
| Excess or ambiguous notation | lines 198, 205, 339, 373, 474, 536 | The extra $Y_S$ is gone, $x_0$ is explained, the vote is explicit, $g_S$ has a domain, the reduced sum is identified as over $I$, and the full-support scale is $\rho_j$. |

The related-work repairs are also visible: HMPST is cited as Proposition 2.1, the exponential argument now credits Minsky–Papert, the basis and function distinctions remain explicit, and there is no claim of exhaustive priority. The optional suggestions to remove unused source macros and to add a Hansen–Podolskii theorem locator were not implemented; neither is a correctness or release blocker. The optional recommendation to illustrate omitted-support necessity using the whole lookup construction is still useful (see the final local edits).

## Reproducibility audit

To respect the instruction against shared edits, I copied the two **unmodified** bundled scripts into `round2_artifacts/` beside this report and ran those copies. This matters because `verify_results.py` writes a JSON file next to itself.

Both scripts completed successfully with exit status zero using Python 3.13, with no installations:

- `verify_results.py`: the raw threshold compiler passed **58,264 exhaustive table/count inputs**, plus **80 larger sampled inputs**. Its four exact masked-moment tests also passed. For these gates, dependence within a block is only through its count, so exhaustive count inputs cover every raw address arrangement. The enumerated comparisons use the actual $\ge$ convention, and score margins are checked.
- `restriction_checks.py`: **354,304** mask-identity cases; exact cross-character sums zero in every tested pair; **7,430** coherent cube/threshold tests, including equalities and zero weights; **112,320** pairing/missing-coordinate correlation tests. This now substantively supports the paragraph's promised pairing artifact.

I additionally wrote `round2_checks.py` from the revised identities, without importing either existing checker. It passed **27,734** exact identity/score inputs (exhaustive small inputs and seeded larger cases), **396** finite gate-count parameter pairs, **4,020** binomial tail-bound cases, and **5,760** complete joint-mask cases. The last test sums over the full independent mask collections and compares the squared total error with the sum of diagonal squared errors; it does not just re-use the proof's product-of-conditional-means calculation. It also checks majority agreement, threshold ties, and the $2q$ error margin for both $q<N$ and $q=N$.

All algebra and joint-mask calculations use integers or exact fractions. The tail checks sum the binomial law with exact integer multiplicities and compare in floating point. They support the audit but are not substitutes for the all-size arguments.

Artifacts produced by this review:

- `round2_checks.py` and `round2_checks.json`.
- `round2_artifacts/verify_results.log` and `round2_artifacts/upper_update_checks.json`.
- `round2_artifacts/restriction_checks.json`.

The source under review has SHA-256 `0e460a861950e0c9d55fdbf162caefaef482a01ad24085b1bc845b280757a2ac`; the PDF has SHA-256 `ec691446f3eaa34c603230b243d42cf659c369b4733ba7886450eec23c5cb12e`. The source matches the recorded revision in `review_status.json`.

## Attribution and formalization verification

The revised attribution is defensible, with no unsupported priority assertion found.

- I independently checked KW's model definition, Theorems 1.1–1.2, and Section 5.2. Their model allows raw top inputs; the named upper bound is indeed $O(n^3/\log n)$, and the separate quadratic bound has the modular basis stated in this draft. The fixed-error exponent comparison is supported. Credit for concentration-window parity approximation also belongs there. [Kane–Williams primary paper](https://arxiv.org/pdf/1511.07860).
- HMPST's Proposition 2.1 is the correct symmetric-function citation. The more general finite-difference identity is proved locally in the draft rather than falsely attributed verbatim to that proposition. Hansen–Podolskii's Theorem 5 in the ECCC version does use level tests for bounded integer forms and is accurately described as related representation background. [HMPST](https://igi-web.tugraz.at/people/maass/psfiles/47.pdf), [Hansen–Podolskii](https://eccc.weizmann.ac.il/report/2013/021/download/).
- IPS's Lemma 2.1 supplies the oriented-chain ingredient. The draft appropriately presents its cube/table-entropy combination as the argument for the specific coherent bound rather than claiming IPS already proved that bound. [IPS primary paper](https://cseweb.ucsd.edu/~paturi/myPapers/pubs/ImpagliazzoPaturiSaks_1997_siamjc.pdf).
- I visually inspected the cached primary book scan at PDF pages 71–73 (printed pp. 56–58): Minsky–Papert, Theorem 3.1.1 and Corollary 1, do state the full-support-predicate obstruction for parity. Section 6 now credits exactly that ingredient and gives its own short proof. Calling the final restricted corollary a theorem is not itself a novelty claim; it need not be demoted if the present qualifications remain. [Primary book scan](https://media.githubusercontent.com/media/dimitarpg13/deep_learning_and_neural_networks/main/literature/books/Minsky-and-Papert-Perceptrons-1969.pdf).
- The remaining background is appropriately scoped: the KKL record confirms the corrected author initial and polynomial-threshold restriction topic, while CSS Section 2.4 actually uses both an encoded table and an extractor. The draft's stated encoded-table distinction is true, though it could additionally mention the extractor if desired. [KKL record](https://eccc.weizmann.ac.il/report/2017/026/), [CSS primary paper](https://arxiv.org/pdf/1806.06290).

The formalization claim is now supported by a live reference. PR 2813 is marked merged on 7 November 2026, with merge commit `a62a692`. The old `complexitylib` URL redirects successfully to `cslib-frontier`. The merged `Andreev.lean` source contains the count $2\cdot4^b+bm2^b$ for bottoms and the circuit correctness/size statements for the earlier construction. This matches Section 2's $3n^2/4$ specialization. The paper carefully excludes the refined exact construction, masked mean-square bound, and restricted lower bounds from that formalization claim. [Merged PR](https://github.com/cslib-community/cslib-frontier/pull/2813), [merge-pinned Lean source](https://raw.githubusercontent.com/cslib-community/cslib-frontier/a62a692/Complexity/Computability/Circuit/Boolean/WeightedThreshold/Andreev.lean).

This was a source/provenance check, not a fresh Lean build or a transitive axiom/kernel audit. No claim of formal certification by this review is intended. Likewise, verification of these named classical sources does not certify exhaustive priority for the specialized constructions or the literal-pairing corollary.

## Remaining local edits, in priority order

There are **no mathematical or reproducibility blockers**. The following are small copy or explanation improvements, not reasons to change any bound or add pages.

1. **Repair the notation-scope promise (lines 120 and 594–602).** Replace “Only in Sections …, use” with “In Sections …, use.” In the last paragraph of Section 6 say “Using $X_S,t_S,\varphi$ from Section 2, …” before the unequal-magnitude construction. This is the only definite remaining internal copy inconsistency I found.
2. **Use the whole-function counterexample for omitted supports (lines 594–595).** Replace the selected-bit parity example with: “The full-support assumption cannot be dropped: the Section 2 construction already gives $O(n^2)$ gates for $A$ with address coefficients in $\{0,1\}$.” It directly substantiates the theorem's qualification and adds no notation.
3. **Explain why the coefficient shifts are cheap (near line 242).** One useful sentence is: “The shifts $\kappa_S$ change only coefficients of existing odd thresholds, so the singleton-address correction adds no staircase gates.” This connects the page-4 algebra with the gate count and makes the choice less mysterious. The present identities already prove it correctly.
4. **Optionally justify the binomial estimate locally (after line 334).** For an entirely elementary presentation, add: “For even $L$, the binomial expression satisfies $p(L+2)/p(L)=(L+1)/(L+2)\ge\sqrt{L/(L+2)}$; together with $p(2)=1/2$, induction proves the inequality.” No extra symbols are necessary. The standard estimate is currently correct, so this is a completeness/readability preference rather than a hole.
5. **Minor prose/space cleanup.** At line 305 use “under the uniform distribution on all input bits.” Delete the duplicated raw-affine expansion at lines 171–173, since equation (1) already states it. That frees space for the short explanations above without reducing font size or widening margins.

Avoid adding a global notation table or further permanent abbreviations. The existing section resets make $q,z,R$ reuse understandable; renaming them all would not improve the proof. For the entropy display, a two-line alignment is optional if needed for comfortable reading, but the current equation is inside the text area. The PDF has no unresolved `??` references; the log has no overfull-box warning. The single underfull bibliography warning is cosmetic. I read the PDF text and inspected renders of all ten pages; no layout defect blocks release.

## Final verdict

**READY — mathematically sound on this review, with minor local copy edits recommended.**

All four main claims survived a fresh all-size audit and independent finite checks. The previous substantive review findings are repaired. The named reproducibility artifacts exist and run successfully, and the Lean statement is narrowly and verifiably attributed to the earlier construction. The remaining changes above improve local comprehension and remove one notation-scope inconsistency; they do not require new lemmas, extra variables, altered parameter ranges, or a longer paper.

No shared draft edits, subagents, posts, or installations were used. All new review files are under `/tmp/andreev_gap/eccc_reviews/`.
