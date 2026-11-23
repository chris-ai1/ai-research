Authors: Christian Reitwiessner

# Independent second editorial review

**Verdict: approve after two small precision corrections. No substantive mathematical blocker was found.** The first rewrite is coherent across the whole paper and does not warrant another wholesale rewrite. I recommend integrating the supplied small revision and finalizing the current editorial task. The intentionally provisional abstract is not a newly discovered blocker; its visible TODO must remain.

The reviewed canonical source was `/home/user/agents/andreev-research/workspace/eccc_draft/paper.tex`, SHA-256 **`7ab9074fb3c1ad41016f22cff83790cca50a489362d7294ff458a120b24c3415`**. The reviewed PDF was SHA-256 **`081628cf4a1db5bf70fb978b7fdbdd3ec65c9c07ce38cbe0bba02ff5e9eb9a8b`**. Both are preserved here as `original.tex` and `original.pdf`.

I read the entire current source and extracted PDF, inspected the rendered ten-page layout, checked the main arguments, and recorded `independent-assessment.md` **before** opening `reviews/editorial_round1/report.md`. That later report confirmed the input hashes and explained the prior editorial choices; it did not supply this round's findings. I did not delegate, edit canonical files, run scripts that overwrite their outputs, or undertake a new literature search.

## Corrections to make before finalizing

1. **Section 5, original lines 445–446, PDF page 7: the claimed wire factor is too sharp.** “Gate upper bounds imply wire upper bounds with a factor of at most $n$” does not follow under the paper's explicit counting convention. With $G$ bottom gates, one output gate, and direct input wires, the paper correctly gives $nG+G+n=(n+1)(G+1)-1$ wires. This can exceed $n$ times the total gate count. Replace **“a factor of at most $n$”** with **“a factor of $O(n)$.”** This fixes a literal quantitative assertion without changing any asymptotic result. The replacement is included.

2. **Appendix B, original lines 651–654, PDF page 10: distinguish output bit zero from a zero score.** “Scores producing zero were strictly negative” is an unfortunate ambiguity at the exact point where strict sign agreement is required. The argument is valid, but its statement should be unambiguous. The supplied replacement is:

   > Write the circuit's output as $[F\ge0]$. On inputs with output bit zero, $F<0$. Since the domain is finite, adding a sufficiently small positive constant makes the score nonzero everywhere without changing the output. Orient this strict score to match $f$.

These are small finalization fixes, not failures of the circuit constructions or lower-bound proofs. Neither requires a new result or a new review round.

## Targeted improvements included in the proposal

- **Equation (2), original line 289, PDF page 5:** write the full range $\varnothing\ne S\subseteq[r]$. It is already the intended range, but the equation follows a page break, where an unqualified sum over $S$ is easier to misread as the full $[k]$ sum.
- **Lemma 4.1 proof, original lines 361–367, PDF page 6:** make explicit that the weights from the chosen bottom gates to the output, and the weights on direct live-input wires, remain fixed. Only a scalar output threshold varies after their functions are specified. This explains the $2^h+1$ count while preserving arbitrary real weights and direct input wires. No weight-discretization assumption is introduced.
- **Theorem A.1, original lines 477–478:** state “sign-coherent” in the theorem itself. The existing gate lists already prove the stronger property—all their address weights are nonnegative—and the introduction already relies on it. This makes the statement match the established construction rather than extending it.
- **Appendix A setup, original lines 501–513:** explain that $W_S$ augments a sum over half the table with a singleton-address correction, give the integer domain of the displayed staircase identity, and explain that the ceiling restricts changes to odd integer levels. These are brief explanations of the existing formulas, not added constructions.
- **Appendix A shifts, original lines 544–554:** put the character-sum explanation before the shift identities. In the proposed pagination, their explanation and formulas are all on page 8, rather than leaving the explanation on the next page.
- **Appendix A layout:** one deliberate page break before its proof keeps all local definitions and the staircase motivation together on page 8. The closed score and its sign verification now share page 9. This uses modest blank space after Theorem A.1 on page 7, rather than compressing fonts, margins, or mathematical explanations. The resulting reflow also keeps Proposition B.2 and its proof together on page 10.

The last items are recommended editorial improvements, not acceptance blockers. A parent choosing a minimal integration can apply only the two corrections above. The complete proposal is small enough that integrating it as a whole is reasonable.

## Whole-paper assessment and mathematical scope

**Abstract and introduction.** The balance condition and the distinction between exact computation and uniform-input approximation are explicit. The sign-coherent class permits different orientations between blocks and gates and does not constrain table or output weights. The motivation correctly distinguishes reproducing a Fourier score, preserving its sign, and truncating it. The abstract remains crowded, but the user has expressly deferred it: its source is byte-identical in the proposal, including **“TODO: The abstract still needs considerable work.”** The note is visible and unclipped in the PDF. I would not change its emphasis again in this round.

**Section 2.** The compilation lemma says what is implemented by bottom thresholds and what reaches the output directly. The Fourier explanation is especially useful: $X=Hv$, $H^{\mathsf T}H=NI$, and $v=N^{-1}H^{\mathsf T}X$ all remain. The lookup sign convention, evenness of $X_S$, affine empty character, gate count, and polynomial integer-weight claim are consistent. The section is clear enough to stand without Appendix A.

**Section 3.** The reflected forms make each truncation error odd in its own coefficient for every fixed address input. The signed table permutation flips one coefficient and fixes another; it does not assert that Walsh coefficients are independent. Conditioning first on the address therefore justifies cancellation of the cross terms. The staircase realizes the truncated score deterministically with coherent address signs. The tail integration, threshold distances, majority tie convention, and choice of $q$ give the stated error and advantage ranges. No random masks, probabilistic selection of a circuit, or intermediate parity gates are needed or introduced. The balanced qualification, $0<\delta\le1/2$, $N^{-1/2}\le\varepsilon\le1/8$, and the reduction for larger advantage remain unchanged.

**Section 4.** The entropy argument only varies thresholds of fixed forms; it remains valid with arbitrary real table and output weights and raw direct output wires. On each chain cube, the score need not be affine in the block-count vector. The proof correctly uses its monotonicity, endpoint extrema, and disjoint crossing intervals. The count $m^k-(m-1)^k$, the finite inequality involving $D_0$, and the balanced $\Omega(n^2/\log^3 n)$ consequence are consistent. The explanation that these restrictions do not preserve uniform address error is important and should remain.

**Section 5 and source attribution.** The questions retain the distinction between unrestricted exact bounds and the restricted exact lower bound. The comparison of advantage powers is properly qualified by the lower bound's range. Apart from the wire-factor correction, this section needs no rewrite. The AI-assistance disclosure, finite-check descriptions, cslib-frontier URL, and limited claim about the earlier Lean formalization are all retained. All bibliography keys, authors, version locators, and URLs are unchanged; this editorial review is not a new priority audit.

**Appendix A.** It remains the hardest part of the paper, but its density now reflects actual algebra rather than unexplained new terminology. The three expansion identities, shift identities, closed score, exceptional-address margins, product implementations, shared gates, and final count fit together. In particular, the shifts change coefficients without adding levels; the zero-address correction is compiled into raw-input thresholds; and the gate sharing yields the displayed count. The exact-balance evenness of $m$, $\alpha=m/2-1$, the $5/16$ refinement including the logarithmic term, and the floor-balance qualification remain intact. The added sentences and revised pagination are sufficient; I do not recommend replacing the proof by a high-level sketch or moving it out of the document.

**Appendix B.** The parity obstruction applies to strict scores, the small threshold perturbation is valid, and direct output terms remain affine after the pair identifications. A nonzero full-support equal-magnitude gate can retain every live coordinate for at most one sign pattern; it need not actually depend on every coordinate at that pattern, which is why “at most” is essential. The conditions $k\ge2$, $m\ge1$, and $d=m\lfloor k/2\rfloor\ge2$, as well as the allowance of address-zero gates, are preserved. Both examples explaining why support and equal magnitude are necessary remain. No unrestricted exponential lower bound is suggested.

## Validation and residual preferences

The proposed `paper.tex` builds successfully with `/tmp/andreev-pdf-tools/tectonic --keep-logs paper.tex`. Its PDF is **10 US-letter pages**, including all nine proof environments, both appendices, and references. The **11pt class, one-inch geometry margins, preamble, abstract, labels, bibliography keys, and external links are preserved**. There are no overfull/underfull boxes, undefined references, or citation warnings. Tectonic still prints the existing environment diagnostic `Fontconfig error: Cannot load default config file: No such file: (null)` but exits successfully; the resulting PDF was rendered and inspected.

An independent finite check passed **30,264** table/block-count cases for Appendix A: exhaustive for $k\le2$, $1\le m\le5$, and $k=3$, $1\le m\le3$; plus 200 seeded cases for every remaining pair with $1\le k\le6$, $1\le m\le5$. It checked all six expansion/shift identities, the closed score, sign margin, and zero-address correction. This supports, but does not replace, the algebraic assessment. I did not rerun the already reviewed historical-mask scripts.

Some natural page breaks remain: Lemma 2.1 is separated from its short proof across pages 2–3; the opening mean-square paragraph crosses pages 4–5; and Lemma 4.1's statement and proof straddle pages 5–6. These are **optional layout preferences**, not remaining logical gaps. A trial that forced the entire odd-error opening and information-lemma statement together produced 11 pages and a worse later break, so it was discarded. The delivered proposal prioritizes the more demanding Appendix A while retaining the requested length. Further pagination work is not a reason to hold finalization.

The canonical source and PDF remain byte-identical to the reviewed originals. Canonical scripts and their artifacts were not modified. `verification.json` records preservation checks and hashes. The handoff files are:

| File | Purpose / SHA-256 |
|---|---|
| `paper.tex` | Complete proposed revision; `84995c9e9338ad635f51d9ded3b5d23fe88a3323d1f8525066cb610114dcbfa9` |
| `paper.pdf` | Built, inspected 10-page proposal; `381c085e90c8aac28e0796882a9aee46ba859b32019e7c6b2f1e740eda840e13` |
| `editorial.patch` | Source-only diff against the exact reviewed source |
| `original.tex`, `original.pdf` | Unchanged reviewed baseline |
| `independent-assessment.md` | Findings recorded before consulting round 1 |
| `verification.json` | Build, scope-preservation, and finite-check record |

After the two precision fixes, **no actual blocker remains for this requested editorial round**. Further abstract development remains explicitly deferred by the user.
