<!-- Copyright (c) 2026 Christian Reitwiessner. -->
<!-- Authors: Christian Reitwiessner -->
# Independent assessment, recorded before reading round 1

Reviewed source SHA-256: `7ab9074fb3c1ad41016f22cff83790cca50a489362d7294ff458a120b24c3415`.
Reviewed PDF SHA-256: `081628cf4a1db5bf70fb978b7fdbdd3ec65c9c07ce38cbe0bba02ff5e9eb9a8b`.

The whole source, extracted text of all ten pages, ten-page rendered contact sheet, and full-sized pages 1 and 8 have been assessed independently. The current rewrite is substantially clear and does not need another wholesale rewrite. The PDF is ten letter-size pages, with 11pt article class and one-inch geometry margins. The requested abstract TODO is visibly present. No overfull/underfull or warning entries were found in its build log.

Two actual precision fixes:

1. Section 5, lines 445–446, says that gates imply wires with a factor of “at most n.” With direct input wires and all gates counted, the earlier correct bound is $nG+G+n=(n+1)(G+1)-1$, which can exceed $n(G+1)$. Say “a factor of $O(n)$” or use the exact $n+1$ bound.
2. Appendix B, lines 651–654, says “scores producing zero were strictly negative.” This means inputs producing output bit zero, but reads as a contradiction about zero-valued scores. Say explicitly that $F<0$ on inputs whose output bit is zero. This is a wording correction, not a change to the valid perturbation argument.

Helpful targeted clarifications:

- Lemma 4.1: explain that direct live-input weights and the coefficients of the specified nonconstant predicates are fixed, so only the scalar output threshold varies. This makes the $2^h+1$ count robust for readers checking arbitrary real top weights and raw direct top wires.
- Appendix A: motivate $W_S$ using $X_S=4\sum_{S\cdot c\text{ odd}}x_c-2\sum_cx_c$ for nonempty $S$, or at least say that $W_S$ augments the half-table sum with singleton corrections. Explain that the ceiling staircase changes at alternate integer levels. A second page of unmotivated definitions would be worse than adding a couple of sentences here.
- State sign coherence in Theorem A.1 itself, since the proof supplies the stronger property and the introduction relies on it.
- Make the summation range in equation (2) explicit to survive a page boundary.

Layout priorities, pending any proposed build: page 4 ends in the middle of the opening odd-error paragraph; page 7 ends after the first dense Appendix A definition display, with the rest on page 8; page 8 ends with the closed score but its sign check is on page 9. The latter two are the clearest opportunities to lower short-context reading burden. The lemma/proof divisions on pages 2/3, 5/6, and 9/10 are tolerable and need not all be eliminated.

Mathematical audit: no failed main argument found. Independently followed lookup compilation, odd-error symmetry, the tail-to-error bound and partial-vote advantage, the arbitrary-real-weight entropy count, sign-coherent cube incidences, and the full-support parity obstruction. Checked Appendix A's six expansion/shift identities, closed score, sign margin, and zero-address correction on 30,264 cases with $1\le k\le6$, $1\le m\le5$: exhaustive for $k\le2$ and for $k=3,m\le3$, and 200 seeded cases per remaining parameter pair. All passed. This finite check supports but does not replace the algebraic review.

Do not alter abstract text just to improve style; it is explicitly provisional. Preserve its TODO. No new mathematical claims or additional literature research are needed for this editorial round.
