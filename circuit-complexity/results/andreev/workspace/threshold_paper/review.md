# Review: "Depth-Two Threshold Circuits for Andreev's Function: Sharper Bounds"

Reviewed from `paper.tex` / `paper.pdf` (8 pages) only. Citation checks against the Kane–Williams source (arXiv:1511.07860v1).

## Overall verdict

**Major revision required.** The core mathematics that can be checked from the text is correct: Lemmas 1–3, 5, 6, 7, the gate count $2N^2+kmN=\tfrac34n^2$, the top-weight bound, the Hoeffding/union-bound choice of $\alpha,\beta$, and the derivation of the constant $36=9\cdot4$ all verify (I re-derived them and checked the gate count and the vote advantage numerically). However:

- Two theorem statements claim more than their proofs give: Theorem 2 has no upper limit on $\varepsilon$ (false near $\varepsilon=\tfrac12$), and Corollary 1's fan-in bound is only proved for $s\gtrsim\sqrt n$.
- The scope claims are inconsistent: page 2 and Section 6 say everything except Proposition 1 is formalized, while Theorem 4 is marked "formalization in progress" and only has a proof outline.
- Lemma 4, which supplies the constant $4$ inside the headline constant $36$, is neither proved nor precisely cited: the text defers to "our erratum", which does not exist in the paper or the bibliography.
- The variable hygiene the paper promises ("each lemma uses only its own local variables plus the boxed globals") is not met: $C$, $\beta$, $L$, $Q$, $M$, $t$, $r$, $c$, $u$, $\delta$, $n$, $k$, $\ell$ are each reused with different meanings, several times within adjacent lemmas, and $a_{i,j}$ is never defined.

Counts: blocker 1, major 8, minor 17, nit 12 (38 findings).

---

## A. Correctness findings

### A1. Theorem 2 (Sec. 3, lines 227–233) — **major** — missing upper bound on $\varepsilon$
**What is wrong.** The statement says "for every $\varepsilon\ge C/\sqrt n$ there is a circuit with $O(\varepsilon^2n^{3/2}\sqrt{\log n})$ gates that $\varepsilon$-agrees". At $\varepsilon=\tfrac12$ this would be an exact circuit with $O(n^{3/2}\sqrt{\log n})$ gates, which the paper itself lists as open (page 2: worst-case gap between $n^{3/2}/\log^2n$ and $\tfrac34n^2$). The proof needs $L=1/(32\varepsilon^2)\ge2$, i.e. $\varepsilon\le 1/8$; and the $L=1$ branch gives agreement $1-\delta$ with $O(n^{3/2}\sqrt{\log(n/\delta)})$ gates, which is $O(\varepsilon^2n^{3/2}\sqrt{\log n})$ only when $\tfrac12-\varepsilon\ge n^{-O(1)}$.
**Fix.** State the range explicitly, e.g. "for $C/\sqrt n\le\varepsilon\le\tfrac12-\tfrac1n$", and handle the two regimes ($L\ge2$ via the vote; $L=1$ via $\delta=\tfrac12-\varepsilon$) in the proof. Also fix the summary ("$\tilde\Theta(\varepsilon^2n^{3/2})$") and table accordingly.

### A2. Theorem 2 proof, "Counting" (lines 257–261) — **minor** — constants do not close after rounding
**What is wrong.** $L$ must be a power of two, so "$L\approx1/(32\varepsilon^2)$" means $L\in[1/(32\varepsilon^2),1/(16\varepsilon^2)]$, and the vote advantage $1/(2\sqrt{2L})$ is then only guaranteed to be $\ge\sqrt2\,\varepsilon$, not $2\varepsilon$. With $\delta=\varepsilon$ the final agreement is $\tfrac12+(\sqrt2-1)\varepsilon<\tfrac12+\varepsilon$.
**Fix.** Take $\delta=\varepsilon/4$ (or $L\le1/(64\varepsilon^2)$) and write the inequality chain out: advantage $-\,\delta\ge\varepsilon$.

### A3. Theorem 2 proof, "Fewer terms" (lines 244–248) — **minor** — explanation of the vote advantage is wrong although the number is right
**What is wrong.** For $L=2^{k-r}$ even, the other $L-1$ entries can never be "balanced". The correct statement is: with $D$ the $\pm1$ sum of the other $L-1$ entries, the rule "output 1 iff score $<0$" is correct whenever $D\le-1$, correct with probability $\tfrac12$ when $D\ge1$, so $\Pr[\text{correct}]=\tfrac12+\tfrac12\Pr[D=-1]=\tfrac12+\tfrac12\binom{L-1}{L/2}2^{1-L}$. (Verified exhaustively for $L=2,4,6,8$.) The inequality $\binom{L-1}{L/2}2^{1-L}\ge1/\sqrt{2L}$ is also asserted without proof.
**Fix.** Replace "balanced" by the $D=-1$ case analysis; add one line for the binomial bound (e.g. $\binom{L}{L/2}2^{-L}\ge1/\sqrt{2L}$ for $L\ge1$), and note $L$ is even because $r<k$.

### A4. Corollary 1 (lines 393–411) — **major** — fan-in bound not proved for small $s$
**What is wrong.** The proof applies Theorem 3 only "as long as $1/(2t)\ge3(k+2)/\sqrt N$", i.e. $t\le\sqrt N/(6(k+2))$. If $t$ is larger we only learn $t=\tilde\Omega(\sqrt n)$, which implies the displayed $t\ge\tilde\Omega(n^{3/4}/\sqrt s)$ only when $s\ge\tilde\Omega(\sqrt n)$. For $s=O(1)$ the statement claims $t\ge\tilde\Omega(n^{3/4})$, which is not established (and is not expected to follow from this method, since $\varepsilon=1/(2t)$ is then below the $\log n/\sqrt n$ threshold where $O(1)$-gate circuits already achieve $\tfrac12+\Omega(1/\sqrt n)$). The first sentence of the corollary also silently inherits Theorem 3's hypothesis $\varepsilon\ge3(k+2)/\sqrt N$.
**Fix.** State $t\ge\tilde\Omega\bigl(\min\{n^{3/4}/\sqrt s,\ \sqrt n\}\bigr)$, or add the hypothesis $s\ge\sqrt n$; add the $\varepsilon$ hypothesis to the first sentence.

### A5. Lemma 4 (lines 304–311) — **major** — unproved, constant $4$ unverifiable, "erratum" not available
**What is wrong.** The lemma is stated with the explicit constant $4$, which feeds directly into the $36$ of Theorem 3. The text says the KW proofs "need small repairs (our erratum lists them)" and that the formalization proves the repaired statements, but no erratum is cited or included, and no derivation of $4$ is given. KW themselves only state $O(|\mathcal P|/\sqrt n)$. From KW's proof one can reconstruct $4$ (Erdős's Littlewood–Offord constant $1$, a factor $2$ from the two-case rank argument, and $\sum_{\ell\le km}\ell^{-1/2}\le2\sqrt{km}$), but a reader cannot verify this from the paper. Note also that KW's restriction lemma is stated for a partition of *all* variables with one star per part, while here the table bits are fully fixed; the adaptation is routine but not stated.
**Fix.** Either (a) include a one-page proof of Lemma 4 with explicit constants (it is short), or (b) state Lemma 4 with an unspecified constant $c_0$, carry $9c_0$ through Theorem 3, and cite the erratum/formalization as a proper reference with a URL. Also say explicitly that the table bits are among the fixed bits and why that does not hurt.

### A6. Proof of Theorem 3, wire bound (lines 370–372) — **minor** — missing step
**What is wrong.** The wire part of Lemma 4 counts gates depending on $\ge2$ live bits, but Lemmas 5 and 6 are stated for survivors in the sense of "depends on $\ge1$ live bit". The proof says "the same computation", omitting that gates depending on exactly one live bit are literals of a live bit and are absorbed into the top gate (which reads the $k$ live bits), so the count of Lemma 5 still applies with $q$ = number of $\ge2$-live-bit gates.
**Fix.** Add that sentence; ideally state Lemma 5 for "$q$ gates not absorbed into the top gate".

### A7. Lemma 5 (lines 326–329) — **minor** — black-box misattributed
**What is wrong.** "By Chow's theorem there are at most $(2^k+1)^{q+k+1}$ such functions" is not Chow's theorem; it is the Roychowdhury–Siu–Orlitsky bound (KW Theorem 2.4, proved there via Knuth's proof of Chow). Since this is the one genuinely black-box step of the lower bound, it should be cited exactly.
**Fix.** "by [KW, Theorem 2.4] (Roychowdhury–Siu–Orlitsky)".

### A8. Lemma 6 proof (lines 347–351) — **minor** — the key calculation is omitted
**What is wrong.** "Summing over $h$ and $q$ gives total probability at most $2^{-(k+6)}$ (a geometric series; this is where $\alpha$ and $\beta$ are chosen)". The reader must do the computation. It works: $\ln|\mathcal H_q|\le(2q+k+1)\ln(2^k+1)+q\ln M$, the exponent is $\ge 2q(k+2+\ln M)+2(k+2)^2$, and the difference is $\ge4q+k^2+7k+8$ for $k\ge2$ (and still fine for $k=1$); the sum is $\le1.02\,e^{-(k^2+7k+8)}\ll2^{-(k+6)}$. But this is exactly the kind of step a self-contained paper must display.
**Fix.** Display the two-line inequality. Optionally note that $2^{-(k+6)}$ is very loose.

### A9. Theorem 1 proof (lines 199–201) — **nit** — justification of the top-weight bound
"$|\theta|\le n$" gives $|2\theta-1|\le2n+1$, not "below $2n$". The claim is true because $-N<\theta\le n$. Say so.

### A10. Theorem 3 statement, "Taking $\varepsilon=\tfrac12$ gives the worst-case bounds" — **nit**
Requires $\tfrac12\ge3(k+2)/\sqrt N$, i.e. $N\ge36(k+2)^2$. Add "for $N\ge36(k+2)^2$".

### A11. Proof of Theorem 3 (line 365) — **nit**
"$\beta/N$ and $2^{-(k+6)}$ add up to at most $2\varepsilon/3$": the first is $\le\varepsilon/3$ by hypothesis; for the second one needs $2^{-(k+6)}\le(k+2)2^{-k/2}$. One clause suffices.

### A12. Proposition 1 (lines 211–222) — **minor** — sketch too terse to check the gate count
$S$ now ranges over $\mathbb Z_p^k$, $t_S$ is implicitly redefined (as $\sum_iS_is_i$?), $Z_{S,r}$ is not defined ("integer counts"), and whether the top test is on $N(-1)^{x_b}$ or $Nx_b$ changes the range of $Z_{S,r}$ and hence whether the first term is $pN^2$ or $2pN^2$. With $Z_{S,r}=\#\{c:S\cdot c\equiv r,\ x_c=1\}$ and the crude range $(p-1)m$ per block in the support of $S$, I get $pN^2+(p-1)^2kmN$, matching the claim, but the reader cannot reconstruct this from the text. Also the top weights are real (cosines), unlike Theorem 1's integers; say so.
**Fix.** Write the character identity, define $Z_{S,r}$ and $t_S$, and give the two-line count.

### A13. "Comparison" paragraph (lines 204–208) — **nit**
"about $N^2$ parities" times $O(n)$ gates per parity gives $O(n^3)$, not the cited $O(n^3/\log n)$; KW say $O(n^2/\log n)$ parities. Align.

### A14. Sentence after Theorem 2 (line 263) — **nit**
"both bounds are tight up to polylogarithmic factors" fails for the second bound when $\delta$ is tiny (e.g. $\delta=2^{-n}$ gives $\sqrt{\log(n/\delta)}=\sqrt n$). Add "for $\delta\ge n^{-O(1)}$".

### A15. Theorem 4 outline, step 2 (line 476) — **nit**
Lemma 4 is stated in Andreev's notation ($n$, $m$, table). Applying it to $B$ with block length $\ell=n/k$ and total input $2n$ gives $4\sqrt{2n}\,k/n=O(\log n/\sqrt n)$ per gate; say this translation, and note Lemma 4 holds for every fixed seed because the Littlewood–Offord step only uses the randomness of the fixed address bits.

---

## B. Readability / understandability findings

### B1. Scope claims are inconsistent (page 2 "How to read", Thm. 4 statement, Sec. 6) — **blocker** (requirement 5)
Page 2: "All results except Proposition 1 are formalized in Lean." Section 6: "All theorems except Proposition 1 are proved in Lean 4." Theorem 4: "(formalization in progress, issue #2812)" and only a "Proof outline". Section 6's file list says "depth three: see issue #2812", which also leaves Corollary 1's status unclear. The summary box presents the depth-three results as shown, with no caveat.
**Fix.** One consistent sentence everywhere: Theorems 1–3 formalized; Proposition 1 numerically checked only; Corollary 1 (state whether formalized); Theorem 4 outlined, formalization in progress. Put the caveat in the summary and in the table (e.g. mark the $B_n$ row "outline"). Move "issue #2812" out of the theorem statement into Section 6 and name the repository.

### B2. No pointer to the formalization or the erratum (Sec. 6, Lemma 4) — **major** (requirements 1, 5)
"Complexitylib" has no URL, version or commit; "our erratum" is not in the bibliography. The bibliography has a single entry. Claims that rest on these cannot be checked.
**Fix.** Add references with URLs and a commit hash; cite Alon–Goldreich–Håstad–Peralta (or whatever KW use) for the existence of explicit $\delta$-biased lists in the $B_n$ definition, and [KW, Thm 1.2] for "Andreev's function has depth-three majority circuits of size $O(n)$" (line 418).

### B3. $a_{i,j}$ and $a$ never defined (Sec. 1, eq. (1)) — **major** (requirement 1)
The address bits are introduced only as "$k$ address blocks of $m$ bits"; $A(x,a)$ uses $a$ and eq. (1) uses $a_{i,j}$ without definition. Also $x$ as "the table" vector is only implicit.
**Fix.** In the definition: "block $i$ consists of bits $a_{i,1},\dots,a_{i,m}$; write $a$ for all address bits and $x$ for the table."

### B4. $L$ reused within Section 3 — **major** (requirement 2)
Lemma 3 uses $L$ for the linear form; three paragraphs later "$Q$ is the set of $L=N/2^r$ addresses", and then "computes $g(L)$ whenever $L$ lies in the window" (line 255) uses the Lemma-3 meaning again. Direct clash in one page.
**Fix.** Rename the address count (e.g. $\ell_r$ or $|Q|$), or rename the linear form in Lemma 3.

### B5. $\beta$ reused in adjacent lemmas (Lemma 5 proof, Lemma 6 statement) — **major** (requirement 2)
Weight vector $\beta$ on page 5, then the constant $\beta=(k+2)\sqrt N$ ten lines below.
**Fix.** Call the weight vector $\omega$ or $v$.

### B6. $C$ reused — **minor**
Unspecified constant $C$ (page 2 and Theorem 2), the circuit $C$ (Theorem 3), circuits $C_i$ (Corollary 1). Give the constant a value or a different letter.

### B7. Section 5 silently redefines global symbols — **major** (requirement 2)
In the $B_n$ box, $n$ becomes the seed length (total input $2n$), $k=16\log_2n$, $\ell$ is the block length, $\delta$ the bias, $x$ the seed, $r_z$ a list. Globally $n=N+km$, $k=\log_2N$, $\delta$ was Theorem 2's failure probability, $x$ the table, $\ell$ Lemma 3's lower end, $r$ Theorem 2's count of kept coordinates and Proposition 1's residue. Theorem 4 then invokes Lemmas 4 and 5, stated in the old symbols, in the new ones.
**Fix.** Either use fresh letters for $B_n$ ($n_B$, $k_B$, $\ell_B$, bias $\eta$) or a sentence "In this subsection $n,k$ denote ... and the lemmas of Section 4 apply with $m:=\ell$, $N:=2^k$".

### B8. Further reuse — **minor**
$M$: $s+1$ (Lemma 5) vs. vector dimension (Lemma 7; equals $2^k$ in the application but never said). $t$: integer (Lemma 2), $t_S$, fan-in (Cor. 1), vector count (Lemma 7). $Q$: set of addresses (Thm 2) vs. survivor cap (Thm 4). $c$: generic address, the shift vector in the Sec. 4 box, and the constant in "$Q=cn/\log n$". $u$: integer argument of $\varphi$ (line 156), live bits (Sec. 4), real argument of $g_r,\psi$ (Prop. 1). $w$ wires vs. $w_j$ gate weights; $s$ gates vs. $s_i$ block weights (Theorem 3's statement sits next to both). $y$: nonzero test vector in the $B_n$ box and a second seed on line 449.

### B9. Lemmas 4, 5, 6 refer to "the circuit" with no local hypothesis — **minor** (requirement 2)
Lemma 4 uses $s$ and $w$ without introducing a circuit; Lemma 5 says "Fix the circuit"; Lemma 6 says "the circuit's agreement". Each should begin "Let $C$ be a depth-two threshold circuit with $s$ bottom gates and $w$ wires." Also say whether $s$ counts the top gate (Theorem 1 does; Lemmas 4–5 implicitly do not).

### B10. Theorem 2's proof is not labelled and never states the circuit — **minor** (requirements 3, 5)
The text between Theorem 2 and the \qed is three paragraphs headed "Fewer terms / Shorter staircases / Counting" with no "Proof". The reader must assemble the circuit (windowed staircases for $\varphi(X_S+t_S)$ and $\varphi(t_S)$, $S\subseteq\{1..r\}$, top gate tests the sign) themselves. Say in one sentence what the circuit is before the two ideas, and label the proof. State that the Lean proof uses a different identity *here*, not only in Section 6.

### B11. "Fixing" undefined (Lemma 6 proof) — **minor**
"Call a fixing bad" — a fixing (assignment to the fixed bits for a given $\sigma$) is never defined; define it in the notation box, and define $c$ there precisely ($c_i$ = parity of the $m-1$ fixed bits of block $i$, so that $b=u\oplus c$).

### B12. Lemma 5 statement is hard to parse — **minor**
"Every restricted circuit with $q$ survivors belongs to a set of at most ... functions of $u$". Better: "Let $\mathcal H_q$ be the set of functions $u\mapsto C|_\rho(u)$ over all fixings $\rho$ (for this $\sigma$) with exactly $q$ survivors. Then $|\mathcal H_q|\le\ldots$" and then use $\mathcal H_q$ by name in Lemma 6.

### B13. Working memory in Lemma 6 and Theorem 3 — **minor** (requirement 3)
Lemma 6's statement uses $U$, $s$, $N$, $k$ from three different places (notation box, Lemma 4, Section 1) with no reminder. Theorem 3's proof uses $\alpha,\beta$ from Lemma 6 and $\mathbb E[U]$ from Lemma 4 across a page break; the final insertion "Insert $\alpha^2=\ldots$ and Lemma 4" leaves the reader to multiply out $9\cdot4$. Display the one line $\varepsilon^2N\le 9(k+2+\ln(s+1))\cdot 4s\sqrt n/m$.

### B14. After-Lemma-7 paragraph (lines 449–452) — **minor**
"the vectors $u\mapsto(-1)^B$" should be $z\mapsto(-1)^{r_z\cdot x}$ (indexed by $z$, not $u$; $u$ only appears after restriction). State $M=2^k$, $v_x=((-1)^{r_z\cdot x})_z$, and that Lemma 7 needs $\gamma^2>\delta$.

### B15. Theorem 4 part 2 constants — **minor** (requirement 4)
"$O(s\log^2n/n^{3/2})+n^{-\Omega(1)}$" has no explicit constants or exponent and the proof outline uses $\gamma$, $Q=cn/\log n$ without fixing them. Fix $\gamma=n^{-3}$ (say), $c$, and give the resulting exponent.

### B16. "Chow's theorem", "Littlewood–Offord", "Hoeffding" as black boxes — **minor** (requirement 1)
The undergraduate reader is told to know Hoeffding, Cauchy–Schwarz, Markov. Littlewood–Offord (Lemma 4) and the RSO counting bound (Lemma 5) are additional black boxes; state them as numbered Facts with precise citations.

### B17. Proposition 1 placed inside a `keybox` — **nit** (requirement 6)
The boxes are otherwise reserved for notation/definitions; a proposition with a proof sketch in the same style blurs that convention.

### B18. Layout — **minor** (requirement 6)
Page 1 is roughly a quarter empty (the `\needspace{12\baselineskip}` pushes "Results" to page 2); page 3 has a quarter-page gap after Proposition 1; page 4 has a quarter-page gap before the unbreakable notation box. Reduce the needspace, allow the tcolorboxes to break (`breakable`), or move the "Plan" paragraph after the box.

### B19. PDF bookmarks — **nit**
`\sect{\color{ink}...}` leaks into the bookmarks: they read "inkSetting and results", "inkLower bounds", etc. (hyperref warnings in the log). Use `\texorpdfstring{\color{ink}#1}{#1}` in `\sect`/`\subsect`.

### B20. `\MAJ` defined but unused; $\THR\circ\THR$ used in the summary without definition — **nit**
Either define $\THR\circ\THR$ in "Threshold circuits" or drop the symbol from the summary.

### B21. Table row "depth 3, top fan-in $t$" — **nit** (requirement 4)
The $s$ in this row is never defined in the table; add "each subcircuit $\le s$ gates" to the row label or a footnote. Also mark which rows are exact statements and which are asymptotic (the first row is exact, the rest asymptotic in the balanced case).

### B22. "Limits of the method" (lines 375–382) — **nit**
This is informal discussion; it reads like claims ("no argument of this form can give more than ..."). Label it "Remark (informal)". The claim that the restricted function has an $N$-gate circuit should say "OR of at most $N$ ANDs, each a threshold gate".

### B23. Forward reference — **nit** (requirement 6)
Page 2 states "The lower bounds hold for $\varepsilon\ge C\log n/\sqrt n$" before $k$'s relation to $n$ is tied to Theorem 3's $3(k+2)/\sqrt N$; give the explicit value ($3\sqrt2(\log_2n+1)/\sqrt n$) so the reader need not convert.

---

## Summary of findings by severity

| Severity | Correctness (A) | Readability (B) | Total |
|---|---|---|---|
| blocker | – | B1 | 1 |
| major | A1, A4, A5 | B2, B3, B4, B5, B7 | 8 |
| minor | A2, A3, A6, A7, A8, A12 | B6, B8, B9, B10, B11, B12, B13, B14, B15, B16, B18 | 17 |
| nit | A9, A10, A11, A13, A14, A15 | B17, B19, B20, B21, B22, B23 | 12 |

The three most important fixes are B1 (scope consistency), A1 (range of $\varepsilon$ in Theorem 2) and A5 (Lemma 4 / the constant 4 behind 36).
