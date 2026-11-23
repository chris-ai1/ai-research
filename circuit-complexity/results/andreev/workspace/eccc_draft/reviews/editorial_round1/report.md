Authors: Christian Reitwiessner

First substantive editorial round — 2026-11-11.

The complete proposed revision is `paper.tex`, with its successfully built `paper.pdf`, in `/tmp/andreev_gap/editorial_round1/`. The PDF is **10 pages**, including both appendices and references, at **11pt with one-inch margins**. The canonical source, canonical PDF, scripts, and existing script outputs under `/home/user/agents/andreev-research/workspace/eccc_draft/` were not changed. All files recorded in the input manifest remained byte-identical at the final check. `editorial.patch` provides a source-only integration diff; `original.tex` and `original.pdf` preserve the reviewed baseline.

I assessed the complete canonical source and extracted PDF before reading `reviews/revision3/literature_audit.md`. I also inspected page renderings of the original and proposed PDFs. I did not consult earlier editorial review reports, delegate work, or repeat the literature search. This is the first editorial rewrite and scope review, not an independent priority certification.

The initial assessment was that the argument had a coherent structure, but several passages assumed too much recent context. The abstract omitted the balance hypothesis, the approximation proof compressed the reasons for reflected forms and its voting threshold, and Appendix A introduced its score before explaining the staircase identity behind it. The restriction proof also used a raw-score description that could be mistaken for an affine function of block counts when weights within a block are unequal.

The revision addresses the entire document:

- **Abstract:** Leads with the balanced family and the refined exact bound, states deterministic uniform-input approximation, and connects odd errors to the table symmetry. It retains the restricted exact lower bound and mentions the two secondary results. The margin note is unchanged, including the exact text **“TODO: The abstract still needs considerable work.”** It remains visible in the PDF.
- **Introduction:** Makes the threshold convention and counting conventions explicit; distinguishes floor and exact balance; explains staircases before using the term; and organizes the comparison around exact, approximate, and sign-coherent complexity. The historical comparison retains Kane–Williams's precise advantage range and both their gate and wire bounds. It preserves all source credit and the distinction between ordinary lookup, generalized Andreev functions, and newer hard functions in $E^{\mathsf{NP}}$.
- **Affine-form compilation:** Explains separately how constants and direct input terms reach the output. Defines $S\cdot c$, retains the full matrix interpretation $X=Hv$, $H^{\mathsf T}H=NI$, $v=N^{-1}H^{\mathsf T}X$, and calls the transformed object the *signed* truth table. The transition now distinguishes exact score reproduction, sign preservation, and truncation.
- **Approximation:** Motivates partial table votes and reflected forms before their formulas; clarifies the majority calculation and the passage from advantage $2\varepsilon$ to $\varepsilon$; and makes the fixed-address scope of the odd-error argument explicit. It describes the tail calculation directly, without introducing “variance proxy” terminology. The threshold-distance paragraph now refers to $-P_*$, the score actually being thresholded. The construction remains deterministic throughout.
- **Sign-coherent lower bound:** Replaces the abstract “demand/capacity” introduction with a description of the actual restrictions. Defines a gate that “splits” a cube. Defines $F(s)$ as the score on $a(s)$, so it does not imply linearity in the count vector $s$. The incidence argument explicitly takes expectations over tables after the fixed-table crossing count. The explanation of why exactness matters remains.
- **Further questions and verification:** Keeps the exact gate, wire, error-dependence, and biased-table questions, and qualifies the comparison of $\varepsilon$ powers by the range of the known lower bound. It distinguishes finite script checks from proofs and preserves the cslib-frontier link and the limited Lean-formalization claim.
- **Appendix A:** Explains the odd-level staircase before displaying the score and moves the existing parity-product identity forward. Recalls $t_S$ locally, distinguishes the quadratic corrections from the exceptional-address corrections, and reorganizes gate accounting by actual gate families. Explicit level ranges, nonnegative address weights, and the divisibility explaining integer output coefficients make existing claims easier to check. All displayed construction identities and the exact count are retained. The theorem now uses the fully specified name $A_{k,m}$ instead of $A$.
- **Appendix B and bibliography:** Clarifies the table restriction, sign-coordinate pairing, strict-score perturbation, and the “at most one restriction per gate” quantifier. Makes explicit that the common magnitude may vary between gates. Retains both counterexamples to dropping the weight restrictions. The bibliography retains all authors, entries, links, and version-specific locators, with clearer prose and consistent journal presentation.

The mathematical scope was checked against the baseline, not broadened. In particular:

- The exact counts remain $2N(N-1)+kmN$ and the full expression in Theorem A.1, each for bottom gates with one additional output gate. The $(3/4+o(1))n^2$, $(5/16+o(1))n^2$, and exact-balance $\frac5{16}n^2-\frac n4\log_2(n/2)+O(n)$ bounds remain unchanged.
- The approximation bounds and domains remain $0<\delta\le1/2$, $N^{-1/2}\le\varepsilon\le1/8$, and the stated reduction for $1/8<\varepsilon<1/2$. Gate and wire bounds, the chosen radius, and the $nG+G+n$ wire count are unchanged. No random-mask selection or nonuniformity qualification was reintroduced.
- The information lemma, exact finite-parameter sign-coherent inequality, and $\Omega(n^2/\log^3 n)$ consequence retain arbitrary real weights and raw input wires to the output. Orientations may vary by block and gate; unequal magnitudes and zeros remain allowed.
- The exponential lower bound still requires every nonzero address-weight vector to have full support and equal magnitudes within that gate. Its conditions $k\ge2$, $m\ge1$, $d=m\lfloor k/2\rfloor\ge2$, and its $2^d$ count are unchanged. No unrestricted lower-bound improvement is claimed.

I compared the mathematical expressions, theorem statements, hypotheses, and proof uses across the two sources. All theorem/equation labels, bibliography keys, and external URLs are preserved. The changed mathematical phrasing supplies definitions, equivalent score conventions, or explicit consequences of the existing gate lists; it does not assert a stronger theorem.

Validation used unchanged local copies of the existing scripts in `checks/`, with outputs confined to that directory:

| Check | Result |
|---|---|
| `verify_results.exact_checks()` | Passed 58,264 exhaustive table/block-count cases for $1\le k\le3$, $1\le m\le4$, plus 80 sampled cases at four larger parameter pairs. |
| `approximation_checks.py` | Passed 514,200 full-score inputs, 2,976 raw-gate score inputs, 14,820 conditional-error moment checks, 7,268 table involutions, 140 odd-pair moments, 671 compiled values, 135 tail-bound cases, and 135 majority-agreement cases. |
| `restriction_checks.py` | Passed 7,430 coherent-cube threshold tests and 112,320 pairing/missing-coordinate correlation checks. Its historical mask section also ran; that section is not evidence needed for the current deterministic approximation proof. |
| Tectonic | `/tmp/andreev-pdf-tools/tectonic --keep-logs paper.tex` completed successfully. No overfull/underfull boxes or undefined references/citations were reported. |
| PDF and layout | Ten US-letter pages; source retains the original 11pt class, one-inch geometry, and spacing settings. Page renderings checked for clipping; abstract note, long displays, and references checked at readable scale. |

Exact caveats for integration and the next reviewer:

1. **The abstract is still provisional.** Its scope is clearer, but it still compresses several results and mechanisms into one paragraph. The required note is deliberately retained. The next reviewer should independently assess emphasis rather than infer that the note can now be removed.
2. **Appendix A remains the densest part.** The revised ordering explains why the staircase is used, but the three character-sum identities still require the reader to perform expansions from the supplied counts. I found no scope-changing error in this round. An independent mathematical and readability check of those identities and the final gate accounting is still worthwhile; the finite tests do not prove them for all parameters.
3. **There is limited layout headroom.** Natural breaks separate some statements from proofs: Lemma 2.1 across pages 2–3, Lemma 4.1 across pages 5–6, and Proposition B.2 across pages 9–10. The mean-square paragraph crosses pages 4–5, and Appendix A's local definitions cross pages 7–8. These are readable but not ideal for a very small context window. Additional explanatory text may require compensating cuts to remain within ten pages. No font, margin, or spacing compression was used to reach the target.
4. **Build environment diagnostic:** Tectonic emits `Fontconfig error: Cannot load default config file: No such file: (null)` on stderr. It exits successfully and produces the inspected PDF using the existing font setup. This is recorded rather than hidden; there were no corresponding TeX box or missing-reference warnings.
5. **Literature and formalization limits remain.** I relied on the supplied latest audit for the cited-source scope and did not independently re-audit the literature. The failed identification of a prior matching result is not a priority proof. Only the earlier quadratic construction is described as formalized in Lean. The local `exact_checks()` run excluded `verify_results.py`'s historical mask routine; the canonical scripts and their historical content were deliberately left unchanged.

SHA-256 values identify the precise reviewed baseline and proposed handoff:

| Artifact | SHA-256 |
|---|---|
| Canonical input `paper.tex` / local `original.tex` | `3625d03443417304e080043655e46b76e098fda2bda0e0cb2aab53b81971f61e` |
| Canonical input `paper.pdf` / local `original.pdf` | `a34d434b7d4182a9350147f22c9fd10597db1cea54b6cc1ef60c380598b1937c` |
| Proposed `paper.tex` | `7ab9074fb3c1ad41016f22cff83790cca50a489362d7294ff458a120b24c3415` |
| Proposed `paper.pdf` | `081628cf4a1db5bf70fb978b7fdbdd3ec65c9c07ce38cbe0bba02ff5e9eb9a8b` |
| Literature audit read | `eaff8c7a8eef46bf2da7191a78b33eb5ea938f9c02b81ff544f02708d4e1d229` |

`verification.json` records these hashes, layout checks, and preservation checks; `input_manifest.json` records hashes of all canonical draft files at the start. Build output is in `build.stdout.txt`, `build.stderr.txt`, and `paper.log`. The complete source and PDF are ready for the parent to integrate and send to a **new** second reviewer.
