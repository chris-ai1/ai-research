# Review of "Depth-Two Threshold Circuits for Andreev's Function: Sharper Bounds"

Reviewer: independent sub-agent. Sources consulted: `paper.tex`, `paper.pdf` (13 pages, rendered page by page), the Kane–Williams source (arXiv:1511.07860v1, theorem numbers checked against its `\newtheorem` setup: theorems, lemmas, corollaries and definitions are numbered by section, propositions globally), and the full texts of Kabanets–Kane–Lu (ECCC TR17-026), Chen–Santhanam–Srinivasan (ToC 14(9)) and Chen–Tal–Wang (ECCC TR26-039), plus web lookups for the remaining references and the Complexitylib issue/PR numbers.

## Overall verdict

**Mathematically sound in every part I could check; revise before circulation.** No blocker.

- I re-derived every formalized proof (Lemmas 1–7, Theorems 1–3, Corollary 1, Appendix A) and every constant (36, 144, 576, $2^{-(k+6)}$, the gate counts $2N^2+kmN$ and $\tfrac34n^2+1$, the Hoeffding windows, the exponent bookkeeping in Lemma 6). All are correct.
- The Theorem 4 outline is plausible and the parameter arithmetic is right, but it has three gaps that must be stated (top-gate tie convention, union over all middle subcircuits, range of $s$ in Part 2).
- The main non-mathematical problem is one provenance overclaim: Part 2 of Theorem 4 ("a first average-case bound" for $B_n$) follows almost verbatim from Kane–Williams' own Corollary 6.2 proof plus Markov; only the logarithmic factor is new.
- Readability is good overall (boxes, plans, local variables) but several symbols are reused with different meanings, one hypothesis is literally "always true", and there are two layout defects.

Counts: 0 blocker, 5 major (findings 1–4, 24), 22 minor, 7 nit (three of the nits record verified attributions and need no change).

All KW citations by number are correct: Thm 1.2 (upper bounds, incl. $O(n^3/\log n)$ and $\mathsf{MOD}_3\circ\mathsf{MOD}_2$ of size $O(n^2)$), Thm 1.4 (parity windows), Cor 1.1 (approximate majority), Lemma 1.1 and Lemma 3.1 (restriction lemmas), Thm 2.3 (RSO counting), Lemma 6.1 (Gram-matrix lemma), Cor 6.2 (bad seed), Section 3 (tightness for majority), Section 6 ($B_n$, the "cannot prove correlation" remark). CSS Thm 9.3 and Lemma 9.1, CTW Appendix A.3, KKL Thm 1.2 also exist and say what the paper says, with the caveats in findings 24–26.

---

## A. Correctness findings

**1. (major) Theorem 4, proof outline, Step 4 (p. 10): the top majority gate's tie convention is not fixed, and the argument silently needs a strict majority.**
"Strictly more than half of the at most $s$ middle subcircuits are correct on every $u$" only holds if the top gate is a strict majority. With the usual $\mathsf{MAJ}$ convention (output $1$ iff at least half the inputs are $1$), an even fan-in $t$ with exactly $t/2$ ones gives output $1$ with only half the subcircuits correct, and the averaging argument then yields correlation $\ge 0$, not $\ge 1/s$. Kane–Williams have the same gap; Chen–Santhanam–Srinivasan close it in their Proposition 9.5 by also requiring $\mathrm{Corr}(f,\mathbf 1)$ to be small and tracking the threshold. *Fix:* state the convention in the theorem (e.g. "majority gate with an arbitrary fixed tie rule"), and in Step 4 either (a) add the constant function to the bad-seed family (it is already in $\mathcal H_0$ and has correlation $\le\eta$ with every $v_y$, $y\neq0$) and argue as in CSS Prop. 9.5, or (b) restrict to odd fan-in / strict majority and say so.

**2. (major) Theorem 4, Step 1 (p. 10): the family of functions is defined for "the restricted circuits", singular, but Step 4 needs it for every middle subcircuit.**
A $\mathsf{MAJ}\circ\THR\circ\THR$ circuit has up to $s$ middle gates, each the top of its own depth-two subcircuit (sharing bottom gates). The bad-seed family must be the union over all these subcircuits, which multiplies the count by at most $s<d^3$ (harmless, but it has to be said). Also, Lemma 5 as stated counts functions of one circuit $C$; Step 1 applies it to each subcircuit. *Fix:* one sentence: "For each of the at most $s$ middle gates, let $\mathcal H_Q^{(j)}$ be the family of Lemma 5 for its depth-two subcircuit; take the union over $j$, $\sigma$ and the shift $c$."

**3. (major) Theorem 4, Part 2 (p. 10): the size bound $2^k|\mathcal H_Q| = 2^{O(Q\log d+\log^2 d)}$ assumes $\log s = O(\log d)$, but Part 2 is stated for every $s$.**
From Lemma 5, $\log|\mathcal H_Q| = O(Q(k+\log s)+k^2)$. For $s$ super-polynomial in $d$ the exponent is not $O(Q\log d)$. The claim is trivial for $s\ge d^{3/2}$, so this is only a missing sentence. *Fix:* "We may assume $s<d^{3/2}$, since otherwise the bound exceeds $1$."

**4. (major, self-containedness) Lemma 4, second bound (p. 7): $\mathbb E[\#\text{gates on}\ge2\text{ live bits}]\le 4w/m^{3/2}$ is not proved in the paper and cannot be read off Kane–Williams' Lemma 3.1, which only gives $O(\cdot)$.**
The paper says "for the second, see [KW] and the formal proof". Everything about wires (Thm 3, Cor 1, Thm 4) rests on this bound with its explicit constant. My own attempt to extract the constant $4$ from the KW proof pattern (per gate with $w_g$ address wires, $\sum_i p_i\min\{1/m, w_g/m^2\}$ with $\sum_i p_i\le k+2\sqrt{w_g}$) gives $4w_g/m^{3/2}$ only when $w_g\ge k^2/4$; the small-fan-in case needs a separate argument. The paper's standard for Lemma 4's first bound is a half-page appendix; the second deserves the same. *Fix:* add the proof to Appendix A (it should be about ten lines in the style of the first), or at minimum state the per-gate inequality that the Lean proof establishes and where the case split is.

**5. (minor) Theorem 2, Part 2 (p. 6): wrong "so".**
"Also $V>1/(64\varepsilon^2)$, so the vote has advantage $1/(2\sqrt{2V})\ge2\varepsilon$." The advantage bound follows from the *upper* bound $V\le1/(32\varepsilon^2)$; the lower bound $V>1/(64\varepsilon^2)$ is what gives $N/V<64\varepsilon^2N$ in the gate count two lines later. *Fix:* swap the two uses.

**6. (minor) Theorem 2, "Windows" (p. 6): Lemma 3 is applied outside its hypothesis.**
Lemma 3 requires $L\in\{\ell,\dots,h\}$ always. The windowed staircase is applied to a window $L$ may leave; the text says "give exactly the same score" and later "wrong only outside the windows", which is correct, but the reader has to supply the fact that the windowed sum equals $g(\ell)$ or $g(h)$ outside. Also $\lambda$ is not an integer, so the windows need rounding, which is where the "$+2$" in $2^r(6\lambda+2)+1$ comes from; that is not said. *Fix:* add a one-line corollary to Lemma 3: "If $L$ is only known to lie in $[\ell,h]$ on some event $E$, the right-hand side equals $g(L)$ on $E$." Then: "Rounding the window ends to integers, the two staircases for $S$ need at most $4\lambda+1$ and $2\lambda+1$ gates."

**7. (minor) Theorem 2, "Windows" (p. 6): the Hoeffding form used is not stated.**
The reader must check that for $X_S$ (sum of $N$ signs) the tail is $2e^{-\lambda^2/(2N)}\le2e^{-\lambda^2/(2n)}$, and for $t_S$ (sum of $\le n$ bits) it is $2e^{-2\lambda^2/n}\le 2e^{-\lambda^2/(2n)}$. Both are true; neither is written. *Fix:* give the two tails explicitly before the union bound.

**8. (minor) Appendix A (p. 12): $\min\{1,(\rho-k)^{-1/2}\}$ is undefined for $\rho\le k$.**
The sum $\sum_{\rho=1}^{km}\min\{1,(\rho-k)^{-1/2}\}$ needs the convention that the term is $1$ for $\rho\le k$ (which the bound $k+2\sqrt n$ uses). *Fix:* define $p(\rho)=1$ for $\rho\le k+1$ and $(\rho-k)^{-1/2}$ otherwise.

**9. (minor) Proposition 1 (p. 5): two small inaccuracies in the count.**
(a) "The term $S=0$ is $\sum_c x_c$ ($N$ gates)": by the paper's own definition the top gate reads input bits, so this term costs $0$ gates. Harmless for an upper bound but confusing. (b) "$pZ_{S,r}+t_S$ ranges over at most $N+(p-1)m\cdot\#\{i:S_i\ne0\}$ values": that quantity is the *length* of the range; the number of values is one more, and the number of staircase gates equals the length. *Fix:* say "ranges over an interval of length at most …, so needs at most … gates" and drop or justify the $N$ for $S=0$.

**10. (minor) Theorem 1 (p. 5): "Bottom weights lie in $\{-2,-1,0,1,2\}$."**
From (1) the weights are $\mp2$ on table bits and $1$ on address bits; $-1$ never occurs. True as stated, but it suggests a case that does not exist. *Fix:* "$\{-2,0,1,2\}$" or "in $\{\pm2\}$ on table bits and $1$ on address bits".

**11. (minor) Lemma 6, proof (p. 8): the exponent bookkeeping is compressed into one line.**
The step from $(2q+k+1)(k+1)+q\ln(s+1)-2q(k+2+\ln(s+1))-2(k+2)^2$ to $-2q-(k^2+6k+7)$ is correct (I expanded it), but it is the one place a reader is likely to stall. *Fix:* insert the intermediate line "$=-2q-q\ln(s+1)+(k+1)^2-2(k+2)^2$".

**12. (nit) Remark "Limits of the method" (p. 9): the $2k+2$-bit protocol needs one more bit for the second player to indicate which case occurred**, or a fixed rule; also the first player's "partial block parities" are $k$ bits only if the player holds bits in every block. Informal, so fine, but "at most $2k+3$" or "$O(k)$" is safer.

---

## B. Readability / presentation findings

**13. (minor) Theorem 2 (p. 5): "Assume $km\le n$ (always true)."**
A hypothesis that is always true is not a hypothesis; it is clearly a Lean artifact. *Fix:* delete it, or move to Section 7 as "the Lean statement carries the redundant hypothesis $km\le n$".

**14. (minor) Variable reuse across sections (requirement 2).** The paper promises each lemma uses only local variables plus boxed notation, but the following symbols change meaning, sometimes within a page:
- $c$: address in $\{0,1\}^k$ (Sections 3–4 box) and parity vector of the fixed bits (Sections 5–6 box). Both are "addresses", which makes the clash worse, not better.
- $r$: fan-in of a gate (Section 1 definition), number of retained address bits (Thm 2), residue mod $p$ (Prop 1), list entries $r_z$ (Section 6).
- $\lambda$: window half-width (Thm 2) and weight lower bound (Fact 2).
- $D$: sum of signs (Thm 2) and dimension (Lemma 7).
- $h$: upper end of a range (Lemma 3) and a function (Lemma 6).
- $v$: weight vector (Lemma 5) and vectors $v_i$, $v_y$ (Lemma 7 and after).
- $\mathcal Q$ (Thm 2) vs $Q$ (Thm 4) — different objects with the same letter.
- $t$: $t_S$ (Section 3) and fan-in $t$ (Cor 1).
- $P$: a statement (bracket definition) and a number of points (Fact 1).
- $F$: contribution of fixed bits (App. A) and "some $F$" in the table.
*Fix:* rename at least $c$ (Section 5), $r$ (Thm 2, e.g. $\rho$ is taken too — use $j$ or $r_0$), $\lambda$ in Fact 2, and $D$ in Lemma 7.

**15. (minor) Lemma 5, proof (p. 7): "With one extra choice (a constant gate) for padding" is too terse.**
The reader has to reconstruct: "pad the list of survivors to length exactly $q$ with constant gates, so that 'at most $q$ survivors' is covered by lists of length $q$ over an alphabet of size $(2^k+1)(s+1)$". *Fix:* say that.

**16. (minor) Section 2 table and text refer to Lemmas 5–7 and Theorem 4 by number three pages before they exist.** The table gives names for some ("Fixed-weight counting (Lemma 5)") but the text says "Lemma 2" bare. Acceptable in an overview, but requirement 3 (low working memory) is better served by always pairing number and name in Section 2. *Fix:* "removing the parity factor (Lemma 2)" etc.

**17. (minor) Layout, p. 11: an orphaned QED box.** The proof outline of Theorem 4 ends on p. 10 and its $\square$ sits alone at the top of p. 11. *Fix:* `\qedhere` on the last `enumerate` item, or tighten spacing.

**18. (minor) Layout, p. 13: a single bibliography entry on its own page.** *Fix:* tighten `\itemsep`, or shorten two entries (e.g. drop the conference/journal double listing for HP and CSS), so references end on p. 12.

**19. (minor) Section 7 vs Section 4 wording on constants.** Section 7 says "The formal versions use the same constants as this paper" and then "Theorem 2 is formalized with the older identity … which only changes constant factors". Theorem 2 has no explicit constants in the paper, so "same constants" is vacuous for it, and the Lean constant is never given. *Fix:* either state the explicit gate bound the Lean theorem proves for Theorem 2, or restrict the "same constants" sentence to Theorems 1, 3 and Corollary 1.

**20. (minor) Summary box: "Everything else is proved in Lean"** while the status table says Theorem 1 and Corollary 1 are in open PRs (PR #2813 has changes requested as of 6 Nov 2026). *Fix:* "Everything else is formalized in Lean (two results in open pull requests)".

**21. (minor) Table in Section 1, "top fan-in" row omits the cap $t\le\sqrt N/(6(k+2))$.** The entry $\tilde\Omega(n^{3/4}/s^{1/2})$ exceeds the cap for $s<n^{1/2}$; the note "see Corollary 1 for the range" is there but easy to miss. *Fix:* write $\min\{\tilde\Omega(n^{1/2}),\tilde\Omega(n^{3/4}/s^{1/2})\}$ in the cell.

**22. (nit) Theorem 3's "size $s$" and Lemma 5's $(s+1)$.** For the wire version the proof says "$s$ replaced by $w$"; the reason this is legitimate (survivors have $\ge2$ wires, so there are at most $w/2$ candidate gates) is not stated. One clause fixes it.

**23. (nit) The bracket $\ind{P}$ is defined with "statement $P$" and Fact 1 uses $P$ for the number of points on the same page spread.** Use $M$ or $|X|$ in Fact 1.

---

## C. Provenance findings

**24. (major) Summary and Section 6: "a first average-case bound" for $B_n$ (Theorem 4, Part 2) overstates novelty.**
Kane–Williams' proof of Corollary 6.2 already shows that at most $m\cdot2^{o(n)}$ seeds, i.e. a $2^{-\Omega(n)}$ fraction, are approximated by *any* small circuit. Combining that with Markov on $U$ (exactly the paper's Step 3) gives $\tfrac12+n^{-3}+\tilde O(s/n^{3/2})+2^{-\Omega(n)}$ with KW's own parameters and their $\log^3$ losses. KW's remark in Section 6 ("we are unable to prove this") refers to correlation $\varepsilon = n^{-\omega(1)}$, not to a polynomially small bound; the paper's paraphrase "cannot prove a correlation bound for $B_n$" drops that qualifier. What is new in Part 2 is the $\log^2$ instead of $\log^3$, obtained by fixing the circuit first. *Fix:* in the summary write "an average-case bound for $B_n$ of the form $\tfrac12+\tilde O(s/n^{3/2})$, which Kane and Williams do not state but which follows from their argument; our version saves a logarithm". In the table's "Best previously known" cell write "implicit in [KW]" rather than "none stated". Rephrase the sentence after the proof outline to quote KW's actual claim (no correlation bound below $1/\sqrt n$ for circuits of about $n$ gates, and no $n^{-\omega(1)}$ bound at all).

**25. (minor) Lemma 4 attribution (p. 7): "Independent proofs of the first lemma appear in [CTW, App. A.3], [KKL, Lemma 6.1] and [CSS, Lemma 9.1]."**
CTW App. A.3 is indeed an alternative proof of KW Lemma 1.1 (via unate functions and hypercube paths, with $O(k/\sqrt n)$). KKL Lemma 6.1 is a degree-$d$ PTF restriction lemma whose $d=1$ case loses polylog factors, and CSS Lemma 9.1 is a $(t,k)$-imbalance lemma with probability $p^{1/2-o(1)}$; CSS Remark 9.2 says explicitly it is "incomparable" to the constant-forcing form. Neither is a proof of Lemma 4 with explicit constants. *Fix:* "An alternative proof of the $O(\cdot)$ form is in [CTW, App. A.3]; [KKL, Lemma 6.1] and [CSS, Lemma 9.1] prove analogues with polylogarithmic and $n^{o(1)}$ losses."

**26. (minor) Table rows "Andreev, exact … $n^{3/2}/(\log n)^{O(1)}$ [KKL]" and "wires … $n^{5/2}/(\log n)^{O(1)}$ [KKL]".**
KKL Theorem 1.1 is for a function $F_n\in\mathsf P$; the proof (Thm 6.3) uses $A_n(\vec a,y)$ with a $4n$-bit table and $n$ address bits, i.e. an unbalanced variant of Andreev's function, and is incompressibility-based. The attribution is fair but should be footnoted: "for a variant of Andreev's function with a table four times the address length".

**27. (minor) "Fixed-weight counting … structural fact standard [CTW]" (Section 2 table and text).**
The fact that a restricted LTF keeps its weights and only its threshold moves is used explicitly in KW's proof of Lemma 1.1 and is written as equation (9.1) in CSS ($\theta'=\theta-\langle w'',y\rangle$). CTW use it implicitly (Theorem 4.4) but never state it. Citing CTW for it is odd. *Fix:* cite [KW, proof of Lemma 1.1] and [CSS, eq. (9.1)]; keep [CTW] if you want a satisfiability-algorithm example.

**28. (minor) Section 1, table notes: "Because of the $\tfrac34n^2$ upper bound, no gate lower bound above $n^2$ holds for Andreev's function, so the $\mathsf E^{\mathsf{NP}}$ bounds cannot hold for it."**
Only the $n^{5/2-\delta}$ bound of [CTW] is excluded. The $n^{2-\delta}$ bounds of [Tam, ACW] are below $\tfrac34n^2$ and could in principle hold for Andreev's function. *Fix:* "so the $n^{5/2-\delta}$ bound cannot hold for it".

**29. (minor) Fact 1 heading vs bibliography: author order and chapter title for [RSO].**
Fact 1 says "Roychowdhury, Siu, Orlitsky"; the bib entry says "Roychowdhury, Orlitsky, Siu". KW have the same inconsistency (text vs bib), and KW's bib gives the title as "Neural models and spectral *models*" while the paper has "spectral *methods*"; the Springer listing for pp. 3–36 of that volume could not be verified. *Fix:* check the chapter in the Kluwer volume and make text and bib agree.

**30. (minor) Table "Andreev, depth 3, top fan-in: $\tilde\Omega(n^{1/2}/s^{1/3})$ [KW]" and the sentence after Corollary 1.**
KW state only the instance ($n^{1.1}$ gates $\Rightarrow$ fan-in $n^{2/15}$); the general formula is the paper's derivation from Cor. 1.1. *Fix:* "implicit in [KW, Cor. 1.1]".

**31. (nit) "Cutting staircases to a window via concentration [KW, Thm 1.4], for parity."** Correct; KW's parity upper bound (proof of Thm 1.4) is exactly this. Fine as is.

**32. (nit) "Grouping by character and removing the parity factor … new, to our knowledge".** I found no prior statement of Lemma 2 or of the $\tfrac34n^2$ circuit. Hansen–Podolskii's results on PTFs and $\THR\circ\mathsf{MAJ}$ do not contain it. The hedge is appropriate; no change needed, but a sentence saying that the general $\THR\circ\mathsf{MOD}_2\to\THR\circ\THR$ simulation only gives $O(n^3/\log n)$ (and why Lemma 2 beats it) would make the novelty claim easier to assess.

**33. (nit) Lemma 7: "a version of [KW, Lemma 6.1]".** KW's Lemma 6.1 is stated with $O(\varepsilon^{-1})$ and $\Omega(\varepsilon^{1/2})$ and proved via a Gram matrix; the paper's clean $J(\gamma^2-\eta)\le1$ is a genuine tidy-up. Correct attribution.

**34. (nit) Section 2 table, "Uniform-in-$q$ union bound … [KW, KKL, CSS] use Markov".** Verified: KW (proof of Thm 1.1, "by Markov's inequality, with probability at least $1-\epsilon/3$"), CSS (Thm 9.3 proof, event $E_2$), KKL (Thm 6.3 proof). Also verified that all three count $2^{O(k^2)}$ per surviving gate (KW Thm 2.3 consequence, CSS Lemma 9.6 via Cor. 2.10, KKL Cor. 6.5). The paper's description of prior work is accurate here.

---

## What I verified line by line (for the record)

- Lemma 1: exchange of sums and $\prod_i(1+(-1)^{c_i+b_i})=N[c=b]$. Correct.
- Lemma 2: $\varphi(X+t)-\varphi(t)=(-1)^t X$ for even $X$. Correct. Older identity $\varphi(X+t)+\varphi(X-t)=2X(-1)^t$ also correct.
- Theorem 1: per-$S$ gates $2N+2|S|m$; $\sum_S|S|=kN/2$; total $2N^2+kmN$; balanced $3N^2=\tfrac34n^2$; top weights $(-1)^\theta(2\theta-1)$ with $-N<\theta\le n$, so $|{\cdot}|\le2n-1$. Correct.
- Proposition 1: character identity, periodicity trick $\psi_r(pZ+t)-\psi_r(t)=pZg_r(t)$, $\sum_r\psi_r=0$, $Z_{S,r}\le N/p$ for prime $p$ and $S\ne0$, $\sum_S\#\{i:S_i\ne0\}=k(p-1)N/p$, total $N+pN^2+(p-1)^2kmN$. Correct; specializes to Theorem 1 at $p=2$.
- Theorem 2: subcube identity; $\Pr[\text{correct}]=\tfrac12+\tfrac12\binom{V}{V/2}2^{-V}\ge\tfrac12+1/(2\sqrt{2V})$; $\lambda=\sqrt{2n\ln(4\cdot2^r/\delta)}$ makes the union bound exactly $\delta$; $V\in[1/(64\varepsilon^2),1/(32\varepsilon^2)]$ gives advantage $\ge2\varepsilon$ and $N/V<64\varepsilon^2N$; $\log(N/\varepsilon)=O(\log n)$ since $\varepsilon\ge1/\sqrt N$. Correct.
- Lemma 5: nested thresholds give $2^k+1$ functions per weight vector; Fact 1 with $P=2^k$ and $q+k$ inputs. Correct.
- Lemma 6: $\ln(2^k+1)\le k+1$; exponent $-2q-q\ln(s+1)-(k^2+6k+7)$; $\sum_q e^{-2q}=1.157\le1.2$; $1.2e^{-(k^2+6k+7)}\le2^{-(k+6)}$ for all $k\ge1$; $U\ge N$ case via $\alpha\sqrt U\ge\sqrt3N>N/2$. Correct.
- Theorem 3: $\varepsilon\ge3(k+2)/\sqrt N$ gives $\beta/N\le\varepsilon/3$ and $2^{-(k+6)}\le\varepsilon/192$ (since $(k+2)2^{k/2}\ge1$); $9\cdot4=36$; $m\le N$ case: $e^{3(k+2)}-1>N^{5/2}\ge mN, m^{3/2}N$. Balanced exponents $n^{3/2}/\log^2n$ and $n^{5/2}/\log^{5/2}n$. Correct.
- Corollary 1: $\varepsilon=1/(2t)$, $144\cdot4=576$, cap $t\le\sqrt N/(6(k+2))$; $n^{1.1}\Rightarrow n^{1/5}$ vs KW $n^{2/15}$. Correct.
- Lemma 7 and the sharper form. Correct. Application with $D=2^k$ and the $\eta$-biased list. Correct.
- Theorem 4 arithmetic: $\gamma^2-\eta\ge d^{-6}/2$, bad fraction $2^{O(Q\log d+\log^2d)-d}\cdot2d^6$, $\mathbb E[U]=O(s\log d/\sqrt d)$, $\Pr[U>Q]=O(s\log^2d/d^{3/2})$, $s=\Omega(d^{3/2}/\log^2d)$, $w=\Omega(d^{5/2}/\log^{5/2}d)$. Correct modulo findings 1–3.
- Appendix A: half-open interval of length $\sum|\omega^{(i)}|$; rank argument gives $\ge\rho(i)-k$ heavy fixed positions; Erdős/Sperner bound $\binom{R}{\lfloor R/2\rfloor}2^{-R}\le1/\sqrt R$ (checked for $R=1,2,3$ and asymptotically); $\sum_{j\le M}j^{-1/2}\le2\sqrt M$; $k\le2\sqrt n$ from $2^k\ge k^2/4$. Correct.
- Complexitylib: issue #2347 (closed 3 Nov 2026), issue #2812 (open), PR #2813 (open, changes requested), PR #2814 (open, approved by an agent review), commit 242879e all exist. File names could not be verified from the web.
