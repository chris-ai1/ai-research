# Literature audit for the structural revision

Authors: Christian Reitwiessner

Audit date: 2026-11-11. Scope: ordinary independent-table, parity-address Andreev lookup in depth-two real-weight threshold circuits. This supplements the earlier targeted audit and Astra's third review. Sources were inspected for specific statements and model compatibility; this is not an exhaustive priority certification or a verification of every cited proof.

## Search procedure

Searched combinations of “Andreev function”, “depth two threshold”, “quadratic upper bound”, “Fourier lookup”, “sign-coherent”, “unate”, “monotone bottom”, and “upper bounds 2024 2025 2026”. Searched separately for random Boolean Walsh spectra, joint coefficient distributions, and odd-function orthogonality. Followed primary-source references for symmetric-function compilation, monotone restrictions, and generalized Andreev constructions. Checked current ECCC and author-hosted papers to distinguish historical bounds from newer results for different hard functions. Search hits and abstracts alone were not treated as proofs of a matching result.

## Closest sources and decisions

1. **Kane–Williams, STOC 2016.** [Primary PDF](https://cseweb.ucsd.edu/~dakane/depth2LTF.pdf), Theorems 1.1–1.2 and Sections 4, 5.2, 6. The direct predecessor for this function and model. Preserve credit for Fourier-based lookup, concentration-window parity approximation, and the table-majority endpoint. The paper compares its bounds with specified statements, rather than claiming the first quadratic construction after an exhaustive search.

2. **Hajnal–Maass–Pudlák–Szegedy–Turán, JCSS 1993.** [Primary PDF](https://igi-web.tugraz.at/people/maass/psfiles/47.pdf), Proposition 2.1 and Lemma 2.4. Classical symmetric-function threshold simulation. The finite-difference compilation lemma in our paper is proved locally as a real-valued score identity; its elementary mechanism is not advertised as new.

3. **Hansen–Podolskii, Information and Computation 2015.** [ECCC version](https://eccc.weizmann.ac.il/report/2013/021/download/), Theorem 5 and Lemma 6. Relevant bounded-integer level-test representation and polynomial-overhead monotone-bottom simulation. Neither establishes a size-preserving replacement of arbitrary threshold bottoms or our numerical coherent lower bound. Version-specific theorem locators are identified in the bibliography.

4. **Impagliazzo–Paturi–Saks, SIAM J. Comput. 1997.** [Primary PDF](https://cseweb.ucsd.edu/~paturi/myPapers/pubs/ImpagliazzoPaturiSaks_1997_siamjc.pdf), Section 2, Lemma 2.1 and Section 3. Oriented monotonicity and restriction simplification are predecessor tools. Our proof separately states the fixed-normal information count and the count-grid crossing calculation; these specialized statements are not attributed verbatim to IPS.

5. **Minsky–Papert, Perceptrons.** Section 3.1, Theorem 3.1.1 and its corollary, inspected by Astra in the cached primary book scan. The necessity of a full-dependent predicate for parity is classical. Our appendix isolates this fact before its literal-pairing application. The application is qualified by exact equal magnitudes and full support.

6. **O'Donnell, Analysis of Boolean Functions, 2014.** [Author-hosted edition](https://www.cs.cmu.edu/~odonnell/papers/Analysis-of-Boolean-Functions-by-Ryan-ODonnell.pdf), Chapter 1, Sections 1.2–1.4. Standard parity basis, Fourier inversion, and orthogonality. The online table of contents was retrieved; a fresh full-PDF fetch timed out. The paper includes its own inversion proof and does not depend on an unverified specialized theorem from this book.

7. **Chen–Santhanam–Srinivasan, Theory of Computing 2018.** [Primary journal paper](https://arxiv.org/pdf/1806.06290), Section 2.4, equation (2.1). Its generalized Andreev function uses an encoded table and an extractor address. Both differences matter: our random-table symmetry and its consequences cannot simply be transferred to that function. This distinction is now explicit in the introduction.

8. **Chen–Tal–Wang, 2026.** [ECCC TR26-039](https://eccc.weizmann.ac.il/report/2026/039/download/), Theorem 1.1. Gives superquadratic depth-two gate lower bounds for a function in $E^{\mathrm{NP}}$. Added to the main bibliography so the Andreev-specific gap cannot be read as the current global frontier for every explicit function. This audit checked the theorem statement and scope, not the complete algorithmic proof.

## Broader context checked but kept outside the short bibliography

9. **Ivchenko–Medvedev, 2011.** [Primary PDF](https://www.mathnet.ru/php/getFT.phtml?jrnid=mvk&paperid=30&what=fullt), Sections 1–3 and Theorems 1–2. Studies the joint generating function and moments of random Boolean Walsh spectra. Its displayed spectrum uses a different truth-table normalization. This is relevant probability background, not an identified predecessor of our threshold approximation theorem. Our odd-function lemma is proved by an elementary signed permutation; no priority claim is made for that symmetry.

10. **Kabanets–Kane–Lu, STOC 2017.** [Author-hosted paper](https://www2.cs.sfu.ca/~kabanets/papers/PTF.pdf). Extends restriction methods to polynomial threshold gates. Useful context, but the revised proof needs neither a polynomial threshold restriction theorem nor its stronger hypotheses. Omitted from the compact core bibliography.

11. **Chen–Jin–Williams, STOC 2020.** [ECCC TR20-065](https://eccc.weizmann.ac.il/report/2020/065/download/), Theorems 3.2 and 1.15. Short-seed shrinkage and explicit-obstruction thresholds concern formula models and specified computational problems. They supply no immediate Andreev threshold-circuit barrier. A certificate against a fixed bottom library also has different quantifiers from their universal efficiently generated obstruction.

12. **Potukuchi, FSTTCS 2019.** [Primary paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol150-fsttcs2019/LIPIcs.FSTTCS.2019.25/LIPIcs.FSTTCS.2019.25.pdf), abstract and problem definition. Its “Andreev's Problem” is polynomial containment in a finite-field point set, not table lookup. Retained here as an exclusion rather than consuming space in the short introduction.

13. **Sauermann–Xu, 2025.** [Primary record](https://arxiv.org/abs/2510.16592), “Improved lower bound for hypercube edge slicing.” Geometric slicing bounds matter to our broader parity and one-table-bit investigations. The record's scope was checked; the revised compact paper's proofs do not invoke this theorem, and its exponent must not be presented as an unrestricted Andreev lower bound.

## Outcome and remaining limits

The search supports more precise attribution and a stronger separation of functions and models. It did not identify a source proving the particular deterministic truncation circuit or the specialized coherent count-grid lower bound. That unsuccessful identification is not evidence of novelty. Standard Fourier inversion, threshold staircases, random-spectrum symmetries, and the parity-order obstruction remain credited as elementary or classical ingredients. The paper's concrete constructions and complete specialized arguments carry its claims.

The principal mathematical change came from checking the proof, rather than from importing a new theorem: symmetric truncation makes errors odd, so a table symmetry cancels cross moments without masks. The old mask-selection question is consequently removed. The resulting explicit circuits are sign-coherent, making the exact-versus-average comparison concern the same restricted gate class.
