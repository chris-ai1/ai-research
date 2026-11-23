# Review 3 (independent): "Depth-Two Threshold Circuits for Andreev's Function: Sharper Bounds"

Statement numbers are as rendered in `paper.pdf`: Lemma 1, 2, 3, Thm 4, Prop 5, Thm 6, Thm 7,
Lemma 8, Fact 9, Lemma 10, Lemma 11, Cor 12, Lemma 13, Thm 14, Fact 15, Lemma 16.
Line numbers refer to `paper.tex`.

Sources checked:
- the Kane–Williams source `/tmp/kwsrc/thr-thr-arxiv.tex`;
- PR #2816 at head `7b4652b` (`KaneWilliamsB.lean`, `NearlyOrthogonal.lean`);
- PR #2813 at head `b8b0c45` (`Andreev.lean`);
- merged commit `242879e`, which is identical to `main` (`AndreevLowerBound.lean`,
  `AndreevAverage.lean`, `RandomRestriction.lean`, `ThresholdCounting.lean`, `SmallBias.lean`);
- the PDFs of KKL (ECCC TR17-026) and CSS (ToC 14(9)), for the cited theorem numbers.

## Overall verdict

**Minor revision. There are no blockers.**

- **Correctness.** I re-derived every complete proof in the paper and found no mathematical
  error.
- **Theorem 14 constants.** The constants follow from the outline once the missing parameter
  choices are supplied (finding 1). I checked that they then match the Lean statements.
- **Theorem 14 versus Lean.** Every Theorem 14 statement is implied by the corresponding Lean
  theorem in PR #2816. The paper's versions are slightly weaker or differently phrased.
  Section 7's claim that the constants are "the same" is therefore inaccurate.
- **Main weakness.** The Theorem 14 outline cannot be checked by a reader. It leaves $q_0$
  unspecified, never derives the constants, and its Part 2 accounting does not produce the
  stated $2^{-3p}$ term.
- **Smaller issues.** "Correlation" is never defined, several symbols are reused with
  different meanings, one table cell cites CSS for a bound CSS does not state, and the
  discriminator step is uncited.

Severity counts: **0 blocker, 1 major, 14 minor, 10 nit** (25 findings).

---

## A. Correctness findings

**1. [major] Theorem 14 proof outline (l. 720–757): the constants cannot be reconstructed,
and step 3's accounting does not give the stated bound.**

*What is wrong.*
- Step 3 bounds the agreement by $\tfrac12+\gamma+\Pr[\text{bad seed}]+\Pr[U>q_0]$. Part 2
  states $\tfrac12+2^{-3p}+\dots$ with $\gamma=2^{-3p}$. These are consistent only if
  $\Pr[\text{bad seed}]$ contributes nothing, and it does not.
- The correct accounting, and the one in Lean, is
  $(1+\gamma)/2+\Pr[\text{bad}]+\mathbb E[U]/(q_0+1)$ with $\Pr[\text{bad}]\le\gamma/2$.
- $q_0$ is only "of order $d/\log d$" and "suitable". The constants $R$, $2432$, $4864$ and
  $19456$ appear without derivation; "The formal proof makes these steps exact" sends the
  reader to Lean.
- The outline never explains why Part 2 needs $d>R$ while Part 1 does not.

*Fix.* Add the explicit chain below. I checked that it reproduces exactly the Lean constants.
1. Fix the parameters. Take $s<2^{4p}$, so $\log_2(s+1)\le4p$, and $m=d/(16p)$. Let
   $q_0=\max\{Q:(36p+2)Q+R\le d\}$.
2. Count bad seeds. Combine Lemma 10 ($\log_2|\cH_q|\le q(36p+2)+(16p+1)^2$), the $m^k\le2^{16p^2}$
   choices of $\sigma$, the $2^k$ shifts, and the $2^{6p+1}$ seeds per family member:
   $$\Pr[\text{bad seed}]\le2^{(36p+2)q_0+272p^2+54p+2-d}.$$
3. Choose $R$. $R=272p^2+54p+3$ makes this at most $\tfrac12$, which suffices for Part 1.
   $R=272p^2+57p+3$ makes it at most $2^{-3p-1}=\gamma/2$, which Part 2 needs.
4. Bound the survivors. $\mathbb E[U]\le4s\sqrt{2d}/m=64p\,s\sqrt{2d}/d$, so by Markov
   $\Pr[U>q_0]\le64p(36p+2)\,s\sqrt{2d}/(d(d-R))$.
5. Read off the constants. Since $64p(36p+2)\le2432p^2$, this gives Part 2. Part 1 needs
   this probability to be at least $\tfrac12$, which gives the factor $4864=2\cdot2432$.
   For wires, $\mathbb E[U]\le4w/m^{3/2}=256p^{3/2}w/d^{3/2}$ and
   $256p^{3/2}(36p+2)\le9728p^{5/2}$, which gives $19456=2\cdot9728$.

This is about ten lines and turns the outline into a checkable proof, apart from the
discriminator lemma (finding 7).

**2. [minor] Theorem 14 statement (l. 696–719) versus the Lean theorems in PR #2816.**

Checked against `size_ge_/wireCount_ge_of_threshold_eval_eq_kaneWilliamsB_balanced` and
`card_eval_eq_kaneWilliamsB_le_balanced_size/_wireCount`.

*Mismatches.* In every case the paper's statement is implied by the Lean theorem, so nothing
claimed is false.
- (a) **Part 1, $R$.** Lean's worst-case theorems use $R=272p^2+\mathbf{54}p+3$. The paper
  uses $57p$ in both parts. The paper's own outline (a union over $t\le2^{3p}$ subcircuits)
  would need the extra $3p$, but Lean avoids that union.
- (b) **Part 2, wires.** "similarly for wires" hides the formal constant. Lean proves
  agreement at most $\tfrac12+2^{-3p}+9728\,p^{5/2}w/(d^{3/2}(d-R))$, with
  $R=272p^2+57p+3$.
- (c) **What is counted.** Lean bounds `c.size` and `c.wireCount` of the depth-$\le2$
  multi-output circuit, excluding the top gate and its $t$ wires. The paper's "$s$ gates and
  $w$ wires in total" is a weaker reading of this.
- (d) **Top gate.** In Lean the top gate is `threshold t θ` over the outputs. Outputs may be
  input bits and may repeat, and $t$ counts multiplicity ($4t\le d^3$). The paper's "$t$
  depth-two threshold circuits" does not say that repeats are allowed and counted.
- (e) **Notation.** Lean's `n` is the paper's $d$ (message or seed length), Lean's `ℓ` is
  $m$, and Lean's message `x` is the seed $y$.

*Fix.*
- Either state Part 1 with $54p$ (and say that Part 2 needs $57p$, see finding 1), or keep
  $57p$ and drop "same constants" in Section 7.
- Give the Part 2 wire constant.
- Say "$s$ and $w$ need not count the top gate or its wires".
- Say "the $t$ inputs of the top gate may repeat".
- Put the dictionary in (e) into Section 7.

**3. [minor] Theorem 14 Part 1: the hypothesis $t\le d^3/4$ and the comparison with KW
Thm 1.3 (table l. 130–131).**

*What is wrong.* KW Thm 1.3 has no fan-in hypothesis. The table compares the two results
without comment.

*Fix.* Add one sentence: "If the subcircuits are distinct, then $t\le s$ (and $t\le w+2$).
When $t>d^3/4$ both bounds of Part 1 hold trivially, so the hypothesis costs nothing for
$\mathsf{MAJ}\circ\THR\circ\THR$ in the sense of KW." I checked both inequalities. CSS
(Lemma 9.8) uses the same kind of restriction, a class $\mathsf{MAJ}\circ\THR\circ\THR[\dots,n^3]$.
Cite it.

**4. [minor] Theorem 14 is about a parameterized version of $B_n$, but the summary (l. 70)
and table (l. 130–132) say "$B_n$ of Kane and Williams".**

*What is wrong.*
- The theorem requires exactly $k=16p$, $d=km\le2^p$ and bias at most $2^{-7p}$.
- KW take $k=16\log_2d$ and an AGHP list of bias $O(d^{-7})$ with an unspecified constant (KW
  Prop. 2, Cor. 6.1). Their list is an instance of Theorem 14 only if that constant works
  out.
- The formalization proves existence via the AGHP powering construction over
  $\mathrm{GF}(2^{8p})$. PR #2816 says that polynomial-time computability is not certified.

*Fix.*
- Write "$B_n$ (with the parameters of Theorem 14)" in the summary, the table and l. 657.
- Note that the AGHP powering list has bias at most $(d-1)2^{-8p}\le2^{-7p}$, so explicit
  lists satisfy the hypothesis and the function is in $\mathsf P$. That fact is used on l. 111.

**5. [minor] "With $p=\lceil\log_2d\rceil$" (l. 715) is circular, since $d=16pm$ depends on $p$.**

*Fix.* "Take $m=\lfloor2^p/(16p)\rfloor$. For $p\ge9$, $2^{p-1}<d\le2^p$, so
$p=\lceil\log_2 d\rceil$." This is what the Lean docstring states.

Also calibrate "nontrivial for $p\ge17$", which I verified ($R>2^p$ for $p\le16$). At
$p=17$ we have $d=130832$, and Part 1 certifies only about 10 gates. Saying so prevents
over-reading the explicit constants.

**6. [minor] Table row "$B_n$, $\varepsilon$-agree" (l. 132) and its notes give no range of
validity.**

*What is wrong.* Part 2 yields $s=\Omega(\varepsilon n^{3/2}/\log^2n)$ only when
$\varepsilon\ge2\cdot2^{-3p}$ (about $n^{-3}$) and $d>R$.

*Fix.* Add this range to the table notes, as is already done for Andreev's function.

**7. [minor] Theorem 14, outline step 4 (l. 745–754): the "averaging (discriminator)
argument" is neither stated nor cited.**

*What is wrong.* This is the one ingredient of Part 1 that is not in the paper. "Correlation
at least about $1/t$" is vague. The precise condition used in Lean is
$t\gamma+(t+1)\eta<1$.

*Fix.* State the lemma in one line: if $[\sum_{i\le t}h_i\ge\theta]$ equals a target with
bias at most $\eta$, then some $h_i$ has correlation at least $(1-(t+1)\eta)/t$.

Cite it as follows:
- Hajnal et al. [HMPST], the discriminator lemma;
- CSS Prop. 9.5, which proves it for unweighted majority and says a weaker version is
  implicit in KW (see also provenance finding 20).

**8. [nit] Outline preamble (l. 724–725): "We may assume $s<2^{4p}$" does not cover the
wire bounds.**

*What is wrong.* The wire bounds count candidate gates by $w$, so they need $w<2^{4p}$.

*Fix.* "assume $s<2^{4p}$ (respectively $w<2^{4p}$)".

**9. [nit] Theorem 4 (l. 305–307): the description of the weights is inaccurate and not
what is formalized.**

*What is wrong.*
- The $t_S$ gates have weight $0$ on table bits, so table weights lie in $\{0,\pm2\}$, not
  "$\pm2$".
- PR #2813 (`andreevStairWeightInt_mem`) certifies only bottom weights in $\{-2,\dots,2\}$.
  The finer shape ("$0$ or $1$ on address bits") is not formalized.

*Fix.* Write "in $\{0,\pm2\}$ on table bits and $\{0,1\}$ on address bits". In Section 7, say
that the formal statement bounds them by $2$ in absolute value. The statements about
odd top weights and $|{\cdot}|\le2n-1$ do match the formalization.

**10. [nit] Theorem 4 (optional improvement).**

The $S=\emptyset$ term is $X_\emptyset$, which is linear in the table, so the top gate can
read it directly. Its staircase of $2N$ gates is unnecessary, giving $\tfrac34n^2-n+1$. If
the authors prefer the uniform construction, a remark is enough.

### What I verified as correct

- **Lemmas 1–3.**
- **Theorem 4:** the gate count $2N^2+kmN$; the top weights
  $\pm(-1)^\theta(2\theta-1)$, odd with absolute value at most $2n-1$.
- **Proposition 5:** the character identity; $\sum_\nu\psi_\nu(t_S)=0$; the count
  $p(N-1)N+(p-1)^2kmN$.
- **Theorem 6:**
  - $\Pr[\text{correct}]=\tfrac12+\tfrac12\binom{V}{V/2}2^{-V}$;
  - the Hoeffding tails;
  - the union bound giving exactly $\delta$;
  - window sizes $4\lambda+2$ and $2\lambda+2$;
  - the Part 2 choice of $V$, with advantage at least $2\varepsilon$.
- **Lemma 10.**
- **Lemma 11:** the exponent $-2q-q\ln(s+1)-(k^2+6k+7)$; the bound
  $1.2e^{-(k^2+6k+7)}\le2^{-(k+6)}$; the case $U\ge N$.
- **Theorem 7:** the constants $36$ and $144$; the reduction for $m\le N$; the condition
  $\varepsilon=\tfrac12$ when $N\ge36(k+2)^2$; the balanced asymptotics. These match
  `size_ge_of_card_eval_eq_andreev_ge_of_le_eps` and `..._of_le_two_pow` at `242879e`. The
  Lean `_of_le_two_pow` versions also assume $\varepsilon\le1$, which holds automatically.
- **Corollary 12:** both parts; the exponents $n^{2/15}$ versus $n^{1/5}$.
- **Lemma 13:** both the stated form and the sharper form. The Lean
  `card_mul_sq_le_of_abs_inner_ge` proves the sharper form.
- **Fact 15:** it holds for half-open intervals (by the Sperner argument).
- **Lemma 16:** including the ties case.
- **Lemma 8:** both bounds.
- **The bias definition:** it matches Lean's `IsSmallBias`, which uses the expectation of
  the character.
- **The appendix theorem names:** all exist in the merged files.

---

## B. Readability and understandability findings

Checked against requirements 1–4 and 7 of the brief.

**11. [minor] (self-contained) "Correlation" is used but never defined.**

*Where.* Lemma 11's title, the paragraph after Lemma 13, the Theorem 14 outline (steps 1, 3
and 4), and the paragraph after it (l. 759–766). In Lemma 13 itself the quantity is
$|\langle\xi,v_i\rangle|/D$. In the outline the objects are $\{0,1\}$-valued functions
of $u$ or $z$.

*Fix.* In the Section 6 box, define
$\mathrm{corr}(f,v)=2^{-k}\bigl|\sum_z(-1)^{f(z)}v(z)\bigr|$ for $f:\bits^k\to\bits$ and
$v\in\{\pm1\}^{2^k}$. Note that agreement equals $\tfrac12(1+\text{signed correlation})$.

**12. [minor] (few variables) Symbols are reused with different meanings, which the brief
asks to flag.**

| Symbol | Meanings |
|---|---|
| $S$ | a set of blocks, Sections 3–4; a set of address positions, Appendix A |
| $t$ | an integer, Lemma 2; $t_S$; the number of subcircuits, Theorem 14; a rank index, proof of Lemma 8 |
| $R$ | a number of variables, Fact 15; $R_j$, Lemma 16; $272p^2+57p+3$, Theorem 14 |
| $p$ | a prime, Proposition 5; the size parameter, Theorem 14 |
| $\theta$ | the staircase index, Lemma 3; the top-gate count threshold, Theorem 14 |
| $z$ | gate inputs, Section 1; bits, Fact 15; the parity vector and list index, Section 6 |
| $C$ | a depth-two circuit, per the Section 5 box that "applies to Section 6"; a depth-three circuit, Theorem 14 Part 1 |
| $s$ | the size of $C$, per the box; the size of each subcircuit, Corollary 12 |
| $n$ | $N+km$; $d+km$ in Section 6 |

*Fix.* Rename locally:
- $\Lambda$ for the Appendix A position set;
- $T$ or $M$ for the number of subcircuits, as Corollary 12 already uses $M$;
- $R_0$ for the Theorem 14 constant;
- $q$ for the prime in Proposition 5, or another letter;
- $\kappa$ for the top threshold.

Also say in the Section 5 box that Corollary 12 and Theorem 14 override $C$ and $s$.

**13. [minor] (consistency) Section 2 uses $r$ where Section 4 uses $k_0$.**

*Where.* Section 2 says "characters of the first $r$ address bits" (l. 215), and its table
row says "sum over $S\subseteq\{1..r\}$" (l. 193). Section 4 uses $k_0$ for the same
quantity, and $r$ is never defined.

*Fix.* Use $k_0$ throughout.

**14. [minor] (low working memory) Section 2 depends on concepts defined only later.**

*Where.* It relies on "character", "staircase", "survivor", "fixed-weight counting", "costs
a factor $\varepsilon$" and "seed". The reader must hold these terms for 3–8 pages before
they are defined.

*Fix.* Either move Section 2 after Section 5 as a "Discussion of techniques", or give each
term a one-line definition where it first appears.

**15. [nit] Section 6 box (l. 662–668): two names for one object.**

*What is wrong.* $z$ serves both as the running index of the list and as "the vector of
block parities". In Section 5 the same parity vector is called $b=u\oplus o$.

*Related slip.* Outline step 4 says "$C$ computes $z\mapsto v_y(z\oplus o)$", but the
restricted circuit is a function of the live bits. It should read $u\mapsto v_y(u\oplus o)$.

*Fix.* Use $b$ for the parity vector, as in Section 5, keep $z$ as a dummy index, and
correct step 4.

**16. [nit] (clear statements) Theorem 14 Part 1 leaves unclear what is counted.**

*What is wrong.* Part 1 says "$C$ … has $s$ gates and $w$ wires in total", without saying
whether the top gate and its wires are included (see finding 2(c)).

*Fix.* Say explicitly that $s$ and $w$ may exclude the top gate and its wires.

**17. [nit] Proposition 5 proof sketch (l. 343–345): the stated reason is not the operative
fact.**

*What is wrong.* "$pZ_{S,\nu}$ is a multiple of $p$" is trivially true and is not the fact
that matters. The fact that matters is that $g_\nu$ has period $p$, so
$g_\nu(pZ+t)=g_\nu(t)$.

*Fix.* Rephrase the sentence around that fact.

**18. [nit] (presentation) Layout: two statements are split across pages.**

*Where.* I rendered all 14 pages.
- The statement of Theorem 14 starts at the foot of p. 10 and its two inequalities are on
  p. 11. This is the statement whose hypotheses matter most.
- The Proposition 5 box breaks across pp. 5–6.

No other layout problems were visible: no overfull boxes, and the tables fit the width.

*Fix.* Keep Theorem 14 on one page (`\needspace` or a `\clearpage` before the subsection).
Make the Proposition 5 box unbreakable.

**19. [nit] Corollary 12, Part 2 (l. 628–634): the role of $M\le\sqrt N/(6(k+2))$ is
unclear.**

*What is wrong.* The hypothesis reads like a restriction, but the balanced-case sentence
converts it into a $\min$.

*Fix.* State the dichotomy directly: either $M>\sqrt N/(6(k+2))$, or
$mN\le576(k+2)M^2s\sqrt n$.

---

## C. Provenance and honest-scope findings

Checked against requirements 5 and 6 of the brief.

### Citation checks

These citations are correct:
- KW Thm 1.1, 1.2 (all three constructions), 1.3 and 1.4 (window via concentration for parity);
- KW Lemma 1.1, Lemma 3.1, Thm 2.3 (RSO), Cor 1.1 and the "$n^{1.1}$ / $n^{2/15}$" example;
- KW Lemma 6.1 (the Gram-matrix lemma), Cor 6.2 (a seed fixed first, bad for all small
  circuits) and Def 6.1 (with $k=16\log_2n$ and $m\approx n^{16}$, so $\eta\approx n^{-7}$);
- KW §3 (tightness for majority), §6 (no $n^{-\omega(1)}$ correlation bound; the approach
  cannot go below $1/\sqrt n$);
- HMPST Prop. 1, as KW cite it;
- KKL Thm 1.1 (gate and wire bounds of order $n^{3/2}$ and $n^{5/2}$, up to
  $(\log n)^{O(1)}$, for an Andreev variant with a $4n$-bit table), Thm 1.2 = Thm 6.8 (a wire
  bound for a MAJ of depth-two PTF circuits, for a generalized $B_n$) and Lemma 6.1 (a PTF
  restriction lemma with polylog losses). KKL's §6 arguments are Kolmogorov-style, use
  Markov, and fix the hard string first;
- CSS Thm 9.3 ($n^{1.5-o(1)}$ gates and $n^{2.5-o(1)}$ wires for KW's $B_n$), Lemma 9.1
  (an $n^{o(1)}$-loss restriction lemma) and eq. (9.1) (the threshold shift
  $\theta'=\theta-\langle w'',y\rangle$). CSS fix the seed first (Lemmas 9.7–9.8).

I could not check: Guruswami Ch. 3; the CTW remark "as also noted"; Nag; Tamaki; ACW.

**20. [minor] Table cells for $B_n$ (l. 130–131) cite [KW, CSS] for
$\Omega(n^{3/2}/\log^3n)$ and $\Omega(n^{5/2}/\log^{7/2}n)$.**

*What is wrong.* CSS Thm 9.3 states only $n^{1.5-o(1)}$ and $n^{2.5-o(1)}$, as the paper's
own table note says. So the cell attributes to CSS a bound they do not prove.

*Fix.* Cite only [KW] in the cell, and keep CSS in the note.

**21. [minor] Discriminator step and fan-in restriction: prior work is not credited.**

*What is wrong.*
- CSS Prop. 9.5 ("a weaker version of which is implicit in [KW]") is the
  unweighted-majority discriminator used in step 4.
- CSS Lemma 9.8 restricts to at most $n^3$ middle gates, which parallels $t\le d^3/4$.

Neither is cited where it is used.

*Fix.* Cite both in the Theorem 14 outline (see also finding 7).

**22. [nit] Section 2, l. 230–231: "incompressibility-style arguments, as in [KKL, CSS]"
mischaracterizes CSS.**

*What is wrong.* KKL do use Kolmogorov complexity (§6.1–6.2). CSS (Lemmas 9.7–9.8, and their
Andreev arguments) use a counting argument with the hard input fixed first, not
incompressibility. The real point is the order of quantifiers, which l. 238–239 states
correctly for $B_n$.

*Fix.* "arguments that fix the hard input before the circuit, by counting [KW, CSS] or by
incompressibility [KKL], cannot do this."

### Status labels

I checked the summary, both tables, the theorems and Section 7.

**23. [minor] Summary (l. 72–74): the formalization claim is too coarse.**

*What is wrong.* "All results are formalized in Lean, several in open pull requests" hides
three facts:
- The headline result (Theorem 4, $\tfrac34n^2+1$), Corollary 12, Lemma 13 and Theorem 14
  are only in **open, unmerged** PRs.
- Those PRs describe their own results as "not yet independently reviewed".
- Proposition 5 also has a proof sketch, not just a numerical check.

*Fix.* "Theorems 6 and 7 and Lemmas 8, 10 and 11 are formalized in merged code. Theorem 4,
Corollary 12, Lemma 13 and Theorem 14 are formalized in open pull requests that are
not yet reviewed. Proposition 5 has a proof sketch checked numerically on small cases."

**24. [minor] Section 7 (l. 793–798): "the formal versions use the same constants" is
inaccurate for Theorem 14, and the "two details" omit the model differences that matter.**

*What is wrong.*
- The constants differ: see finding 2(a)–(b).
- The model differences are missing: the top gate is unweighted with fan-in counted with
  multiplicity; `c.size` and `c.wireCount` exclude the top gate; and Lean's `n` is the
  paper's $d$.
- For Theorems 6 and 7, Lean proves explicit finite inequalities. For Theorem 6 this is the
  windowed circuit with free parameters $r$, $B$, $t$, of size $4\cdot2^rB+1$
  (`card_eval_andreevWindowedCircuit_eq_andreev_ge(_sqrt)`). The $O(\cdot)$ forms, the
  Part 2 choices ($V$, $\delta=\varepsilon$) and the balanced-case asymptotics are derived on
  paper. The text calls these theorems simply "formalized (merged)".

*Fix.*
- Add a third "detail" with the Theorem 14 dictionary and model.
- Add a sentence: "Lean states explicit finite inequalities; the asymptotic corollaries are
  derived in the text."
- Change "same constants" to "the same or slightly better constants".

**25. [nit] Proposition 5 status (l. 328, 353–355, 783) is stated loosely.**

*What is wrong.*
- The proposition is stated for prime $p$, and its sketch uses $Z_{S,\nu}\le N/p$, which
  needs primality. Yet the numerical check lists $p=4$, a non-prime run with a different
  bound.
- "Tables of up to 27 entries" means $k\le3$ for $p=3$ and $k\le2$ for $p=4,5$, which is
  very small.
- Also, l. 775 says "All formal proofs use only the standard axioms and contain no
  `sorry`". I found no `sorry` in `KaneWilliamsB.lean`, but a reader cannot check the claim
  from the paper.

*Fix.*
- Status: "proof sketch; numerically checked for $p=3,5$ with $k\le2$ or $3$ (and for
  $p=4$, outside the proposition, with the bound $Z\le N$)".
- For the axioms claim, point to the CI job or the `#print axioms` output.

### Novelty claims

The "new, to our knowledge" labels in the Section 2 table are suitably hedged, and the text
separates the standard structural fact (threshold shift) from its new use (counting).
Section 6's statement that Part 2 "is not essentially new" is honest and matches what I
found in KW's proof of Cor. 6.2. I did not find an overclaim apart from findings 4 and 20.
