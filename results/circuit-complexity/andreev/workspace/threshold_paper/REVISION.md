<!-- Copyright (c) 2026 Christian Reitwiessner. -->
Authors: Christian Reitwiessner

# Upper-bound revision

The paper now includes the strongest general exact construction from the research thread and the improved average-case upper bounds, with self-contained proofs and raw-gate accounting.

- Exact: $(5/16+o(1))n^2$ total gates at balance. The finite bottom-gate formula is stated explicitly; exact balance also gives the negative $n\log n/4$ correction up to $O(n)$.
- Approximation: $O(n^{3/2}\sqrt{\log(1/\delta)})$ gates for agreement $1-\delta$, and $O(\varepsilon^2 n^{3/2}\sqrt{\log(1/\varepsilon)})$ gates over the stated small-advantage regime. The proof fixes masks nonuniformly; it makes no efficient uniform mask-selection claim.
- Formalization: distinguishes the two new hand proofs from merged Lean proofs of the earlier bounds. PRs 2377, 2813 and 2814 are merged; 2816 is open as checked on 7 November 2026.

The earlier simpler quadratic construction remains as an introduction. The unrelated moduli proof sketch was removed to keep the revision focused. Finite SMT records, experimental coefficient languages, failed approaches, and the unreviewed lower-bound-range extension remain in the research archive rather than the paper. A small positive-part correction makes the sign-coherent appendix's entropy bound valid in trivial parameter regimes.

Validation:

```sh
python3 verify_upper_updates.py
tectonic paper.tex
```

`upper_update_checks.json` records 58,264 exhaustive table/block-count cases for the new raw gate construction, larger spot checks, and independent exact cross-moment checks. Block-count enumeration is complete here because every exact-construction gate and direct coefficient is uniform inside its block. The mathematical proofs establish the all-size statements; finite checks are guardrails.

The revised PDF is 19 pages (previously 18). All labels resolve, no overfull boxes or undefined references were reported, and the new result pages were visually inspected. The source and PDF are preserved together in the private continuation archive.

## 11 November 2026: sign-coherent lower bound promoted to a main result

The $\Omega(n^2/\log^3 n)$ lower bound for circuits with sign-coherent bottom gates was an appendix note marked preliminary. It is now Section 6 (Theorem 12, Lemmas 13 and 14, Proposition 15), listed in the abstract, the results table, the technique table and the formalization table. The mathematics is unchanged. The section uses its own notation ($G$ bottom gates, cubes $q$) so that no symbol of earlier sections is reused. The explainer cites the new numbers.

PR #2816 was merged on 9 November 2026; the formalization section now says so. The PDF is 20 pages; all labels resolve and there are no overfull boxes or undefined references. Pages 1, 2 and 13 were inspected visually.

## Full-support equal-magnitude address lower bound

Added a main section with the exponential bottom-gate lower bound, its complete literal-pairing/parity proof, and the general paired-cancellation covering inequality. Both full support and equal absolute magnitudes within each gate are explicit hypotheses. Table coefficients and raw top weights remain unrestricted. The abstract, result overview, technique table and formalization status include the result. This is a hand proof checked by research agents; no Lean formalization or novelty priority is claimed. The unrestricted exponent gap is unchanged.
