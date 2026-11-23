# Novelty search: depth-two threshold circuits for Andreev's function

Date of search: 2026-11-06. Baseline: Kane–Williams (KW), arXiv:1511.07860v1 (= ECCC TR15-188), STOC 2016.

**Method.** I ran web searches (standard and extended) over arXiv, ECCC, DBLP, Semantic Scholar, Dagstuhl/LIPIcs, ToC, authors' pages and GitHub. I downloaded and text-searched the full texts of KW, KKL (ECCC TR17-026), CSS (arXiv:1806.06290, ToC version), Kabanets–Lu (ECCC TR18-115), L. Chen (arXiv:1805.10698), Hansen–Podolskii (ECCC TR13-021), Chen–Tal–Wang (ECCC TR26-039) and Nag (ECCC TR26-167, v1 and v2). For the other works I read only the abstracts or the search-result summaries; these are marked "abstract only" below.

**Caveat.** "Nothing found" means only that these searches turned up nothing. It is not evidence of novelty. Google Scholar's "cited by" lists for KW could not be browsed directly; I covered them through the citing papers I found.

**Public disclosure by the project itself.** The core claims are already public on GitHub, so they are not third-party prior art:
- [complexitylib issue #2347](https://github.com/cslib-community/complexitylib/issues/2347), opened 2026-11-02 by `chris-ai1` and closed 2026-11-03, states:
  - the exact construction, with an earlier count of $4N^2+kmN=\tfrac54n^2$ gates;
  - the windowed average-case circuits;
  - an $\varepsilon^2$ lower bound, still with $\log^3$ and $\log^{7/2}$ factors.
- PRs [#2364](https://github.com/cslib-community/complexitylib/pull/2364) and [#2366](https://github.com/cslib-community/complexitylib/pull/2366), merged 2026-11-03, formalize the exact and windowed circuits.
- Issue #2812, opened 2026-11-06, covers the $\tfrac34n^2$ circuit, top fan-in and $B_n$. I saw only its title, through cross-references.

The paper should cite or acknowledge these. Their statements differ from the paper's ($\tfrac54$ vs $\tfrac34$; $\log^3$ vs $\log^2$), so the paper should also say which version is current.

---

## 1. Claimed results

| # | Claim | Status | Closest prior work (exact location) | Confidence |
|---|---|---|---|---|
| 1 | Exact $\mathsf{THR}\circ\mathsf{THR}$ circuit for Andreev with $2N^2+kmN=\tfrac34n^2$ bottom gates and small integer weights | **Not found.** The best published depth-2 bound is KW's $O(n^3/\log n)$. Generic conversions give about $n^3$, not $n^2$. | KW Thm 1.2 and §5.2 sketch, item 2: $n^2/\log n$ parities, each in $O(n)$ gates. KW Thm 1.2 also gives depth-3 $O(n)$, a parity decision tree of depth $\log_2 n$, and **$\mathsf{MOD}_3\circ\mathsf{MOD}_2$ of size $O(n^2)$**. That last one is a different basis and does not give $\mathsf{THR}\circ\mathsf{THR}$. Hansen–Podolskii (TR13-021) Thm 5: $\mathsf{PTF}_{\{1,2\}}(\mathrm{poly})=\mathsf{THR}\circ\mathsf{MAJ}$, where a PTF of length $L$ and degree $D$ becomes $L(D+1)$ gates. This is a general "function of a bounded linear form → staircase" conversion; it does not supply a short representation for Andreev. See the discussion below. | Medium-high |
| 2a | Average-case **upper** bound $O(\varepsilon^2n^{3/2}\sqrt{\log n})$ gates; $1-\delta$ agreement with $O(n^{3/2}\sqrt{\log(n/\delta)})$ gates | **Not found.** | KW only remark (§6) that Andreev has correlation $\Omega(1/\sqrt n)$ with the majority of the table bits, i.e. $O(1)$ gates suffice for advantage $1/\sqrt n$. KW Thm 1.4 gives the analogous windowed upper bound for PARITY ($O(\sqrt n)$ gates, 99%). | Medium-high |
| 2b | Average-case **lower** bounds $\Omega(\varepsilon^2n^{3/2}/\log^2n)$ gates and $\Omega(\varepsilon^2n^{5/2}/\log^{5/2}n)$ wires | **Not found.** No improvement of KW's $\varepsilon^3$ dependence or of their $\log^3$, $\log^{7/2}$ factors for Andreev was found. | KW Thm 1.1 ($\varepsilon^3$, $\log^3$, $\log^{7/2}$). KKL Thm 6.3 is worst case only, with $(\log n)^{O(d^2)}$ unspecified; they write that "a correlation bound as in [KW16] can also be proved in a similar way", without the details. CSS give correlation bounds for the *generalized* Andreev function, but only against $n^{1+\varepsilon_d}$ wires. Nag TR26-167 Table 1 still lists KW's $\varepsilon^3n^{5/2}/\log^{7/2}n$ as the explicit-function average-case wire bound. | Medium-high |
| 3 | Worst-case $\Omega(n^{3/2}/\log^2n)$ gates for Andreev | **Not found as stated.** It would be a log-factor improvement. No gate lower bound above $n^{3/2}\cdot\mathrm{polylog}$ for any function in $\mathsf P$, $\mathsf{NP}$ or $\mathsf E$ was found. | KW Thm 1.1 with $\varepsilon=\Theta(1)$: $\Omega(n^{3/2}/\log^3n)$. KKL Thm 1.1/6.3 with $d=1$: $n^{3/2}(\log n)^{-O(1)}$ gates and $n^{5/2}(\log n)^{-O(1)}$ wires, worst case, a function in $\mathsf P$ (Andreev). CSS Thm 9.3 re-derives KW's depth-3 bound with $n^{o(1)}$ loss. Above $n^{3/2}$, every bound is for $\mathsf{E}^{\mathsf{NP}}$: Tamaki TR16-100 and ACW FOCS'16 at $n^{2-\varepsilon}$; CTW Thm 1.1 at $n^{2.5-\varepsilon}$. CTW's own introduction says: "Kane and Williams proved that there is a function in P that requires THR∘THR circuits with $n^{1.5-\varepsilon}$ size; this was later improved by [Tam16] and [ACW16] … at the cost of having the hard function in $\mathsf E^{\mathsf{NP}}$". | Medium-high that $n^{3/2}/\mathrm{polylog}$ is the state of the art for $\mathsf P$. Medium that no explicit $\log^2$ exists anywhere (KKL's exponent is unspecified). |
| 4 | Top fan-in $t\ge\tilde\Omega(n^{3/4}/\sqrt s)$ for a MAJ of $t$ size-$s$ $\mathsf{THR}\circ\mathsf{THR}$ circuits computing Andreev | **Not found.** It follows immediately from 2b via KW's own averaging (KW Cor. 1.1 and §5.1). It is new only because 2b is. | KW Cor. 1.1 and §5.1 example: "no $\mathsf{TC}^0_3$ circuit of $O(n^{1.1})$ gates where the output gate has fan-in $o(n^{2/15})$". KKL Thm 1.2/6.8 allow top fan-in up to $2^{n^\epsilon}$, but for a *different* function $B_{n,\epsilon}$ (built from list-decodable codes), not for Andreev. | High that it is not stated for Andreev. Note that, per the review, the claim needs $s\gtrsim\sqrt n$, or a $\min$ with $\sqrt n$. |
| 5 | $B_n$: MAJ∘THR∘THR $\Omega(n^{3/2}/\log^2n)$ gates and $\Omega(n^{5/2}/\log^{5/2}n)$ wires; average-case bound $\tfrac12+O(s\log^2n/n^{3/2})$ | **Partially known (follow-ups exist).** No explicit $\log^2$ / $\log^{5/2}$ bound and no average-case bound for $B_n$ was found. | **CSS (ToC 2018) §9, Thm 9.3** re-proves KW Thm 1.3 for the same $B_n$ ("the same as that defined by Kane and Williams [27, Section 6]") with $n^{1.5-o(1)}$ gates and $n^{2.5-o(1)}$ wires, via their Lemma 9.1, and states Lemma 9.7 ("implicit in Corollary 6.2 from [27]"). **KKL (STOC'17) Thm 1.2 = Thm 6.8**: MAJ of at most $2^{n^\epsilon}$ depth-2 degree-$d$ PTF circuits, wires $\le n^{3/2+1/d}(n^\epsilon\log n)^{-cd^2}$, cannot compute $B_{n,\epsilon}$, a list-decodable-code variant. This is a different function, a wire bound, and the polylog is unspecified. **KW §6, last paragraph** says explicitly that they "are unable to prove" a correlation bound for $B_n$, and that their approach cannot go below $1/\sqrt n$. KW §7, open question 1 asks for asymptotically tight results for $A_n$ and $B_n$. | Medium-high |
| 6a | Restriction + counting cannot exceed about $n^{3/2}/\log n$ for Andreev | **Partially known (implicit).** The ingredients are in KW: Lemma 1.1 is "essentially tight for MAJORITY" (KW §3), and the restricted function is a $k$-bit lookup. No explicit statement of this barrier for Andreev was found. | KW §3 tightness remark; KW §5.2 ("We cannot expect to prove much stronger lower bounds for $A_n$"); KW §6, last paragraph (a $1/\sqrt n$ limit for correlation). Nag TR26-167 §1.2 and §9 discuss looseness of the fan-in-blind $O(k/\sqrt n)$ survival bound in another setting. | Medium |
| 6b | Andreev has deterministic CC at most $2k+2$ under every input partition, so discrepancy and sign-rank cannot give $n^{2-o(1)}$ | **Not found for Andreev specifically.** The general principle is standard: discrepancy is $\ge 2^{-O(D)}$, and sign rank is $\le 2^{D}$. Sign-rank methods are already known to be insufficient for $\mathsf{THR}\circ\mathsf{THR}$. | Chattopadhyay–Mande, "Weights at the bottom matter when the top is heavy" (ECCC TR17-083; arXiv:1705.02397): a function with linear-size $\mathsf{THR}\circ\mathsf{THR}$ circuits but sign rank $2^{\Omega(n^{1/4})}$, so the sign-rank method alone cannot give strong $\mathsf{THR}\circ\mathsf{THR}$ bounds. Hansen–Podolskii TR13-021: 3-party NOF unbounded-error CC bounds would give $\mathsf{THR}\circ\mathsf{THR}$ bounds. Forster et al. 2001 and Nisan 1994 for the $\mathsf{THR}\circ\mathsf{MAJ}$ / $\mathsf{MAJ}\circ\mathsf{THR}$ CC routes. | Medium (an elementary observation; I would present it as a remark, not a contribution) |
| 7 | Mod-$p$ generalization: $O(pN^2+(p-1)^2kmN)$ gates | **Not found.** | No mod-$p$ variant of Andreev's function was found in the threshold-circuit literature. Known "generalized Andreev" functions (Komargodski–Raz; Chen–Kabanets–Kolokolova–Shaltiel–Zuckerman; CSS §2.4) replace the *table* with a code, not the parity with a mod-$p$ residue. Two searches on this topic were blocked by the search tool (see the query log). | Medium-low (thin search coverage) |

### Notes on claim 1 (generic conversions)

- **Fourier/sparsity route.** As a $\pm1$ function of all $n$ inputs,
  $$(-1)^{A}=2^{-k}\sum_{S,c}(-1)^{x_c}\chi_S(c)\chi_S(b),$$
  i.e. $N^2$ parities of length up to $|S|m+1$, with spectral norm $\|\hat f\|_1=N$.
  - Converting each parity separately into a depth-2 symmetric-function staircase (Hajnal et al. 1993, Prop. 1) costs $\sum_{S,c}O(|S|m)=\Theta(N^3)=\Theta(n^3)$. This is KW's route (KW §5.2 item 2, $O(n^3/\log n)$ after their accounting).
  - Bruck–Smolensky-type sparsification (spectral norm $L$ gives a sign of $O(nL^2)$ parities) gives no saving here.
- **Parity decision trees.** Andreev has a parity decision tree of depth $k+1$ (KW Thm 1.2). A depth-$d$ PDT expands into at most $4^d$ parities, which is again $N^2$ parities of length $\Theta(n)$, so about $n^3$.
- **$\mathsf{THR}\circ\mathsf{MAJ}$ = poly-length PTFs over $\{1,2\}^n$** (Hansen–Podolskii Thm 5). Each function $g(L)$ of a bounded integer linear form $L$ is a PTF over $\{1,2\}^n$ of length (range of $L$). The paper's circuit is therefore equivalent to a length-$\Theta(n^2)$ PTF over $\{1,2\}^n$. HP supply the *equivalence*, not this specific representation.
- **What is missing in the literature** is exactly the paper's decomposition (T1 grouping + T2) of the lookup into $O(N)$ functions of single linear forms, each of range $O(N)$.
- **The circuit is effectively $\mathsf{THR}\circ\mathsf{MAJ}$.** Bottom weights are in $\{-2,\dots,2\}$ and top weights are below $2n$, so the circuit is in $\mathsf{THR}\circ\mathsf{MAJ}$ with $\tfrac34n^2$ gates. It is also in $\mathsf{MAJ}\circ\mathsf{MAJ}$ after duplicating wires polynomially (KW's circuit is likewise in $\mathsf{THR}\circ\mathsf{MAJ}$). This is worth stating: the upper bound holds in the weaker class.
- No $O(n^2)$ or $n^{2-\delta}$ $\mathsf{THR}\circ\mathsf{THR}$ or $\mathsf{MAJ}\circ\mathsf{MAJ}$ bound for Andreev or for multiplexer-of-parities was found anywhere, including the Mahajan survey (abstract only), CSS, KKL, CTW and Nag.

---

## 2. Techniques

| Tech. | Description | Status | Reference(s) |
|---|---|---|---|
| T1 | Fourier expansion of the multiplexer grouped by character: $\sum_S X_S(-1)^{t_S}=N(-1)^{x_b}$ | **Known (standard).** Lemma 1 is Fourier inversion of the table $T:\{0,1\}^k\to\{\pm1\}$ evaluated at $b$: $X_S=N\hat T(S)$ and $(-1)^{t_S}=\chi_S(b)$. Writing it this way is presentation, not a new idea. | O'Donnell, *Analysis of Boolean Functions* (2014), Ch. 1 (Fourier expansion and inversion). KW §5.2 item 2 uses the Fourier expansion of the AND inside the multiplexer (ungrouped). |
| T2 | Parity removal: for even $X$, $X(-1)^t=\varphi(X+t)-\varphi(t)$ with $\varphi(u)=(-1)^uu$; equivalently $\varphi(X+t)+\varphi(X-t)=2X(-1)^t$ | **Not found.** It is closest in spirit to the polarization identity $xy=\tfrac14((x+y)^2-(x-y)^2)$, which turns products into functions of sums. I found no use of this parity version in threshold-circuit constructions, including symmetric-function, IP2, multiplication and PTF-over-$\{1,2\}$ constructions. | Nearest related: Hansen–Podolskii Thm 5 ("exponential form": any function of a bounded linear form is an interpolated sum, and conversely). |
| T3 | Staircase / telescoping $g(L)=g(\ell)+\sum_\theta(g(\theta)-g(\theta-1))[L\ge\theta]$ | **Known.** | Hajnal–Maass–Pudlák–Szegedy–Turán 1993, Prop. 1 (symmetric functions in $\mathsf{THR}\circ\mathsf{MAJ}$ with top sum $\pm1$; cited by KW §5.2 for exactly this). Muroga, *Threshold Logic and its Applications* (1971). Siu–Roychowdhury–Kailath 1991 (the "telescoping" technique for symmetric functions; abstract only). Hansen–Podolskii Thm 5 (EMAJ gate per value of a linear form). |
| T4 | Windowed staircases via Hoeffding concentration | **Known.** | KW Thm 1.4, upper bound proof (§4: $L_k=[\sum x_i\ge k]$ only for $k$ in an $O(\sqrt n)$ window, 99% agreement). The paper's version applies a union bound over $2^r$ linear forms, which is a routine extension. |
| T5 | Random restrictions with Littlewood–Offord; counting threshold functions over fixed features | **Known.** | KW Lemma 1.1 and Lemma 3.1 (block restrictions, one star per block); Littlewood–Offord 1943; Erdős 1945. Alternative proofs: CTW (TR26-039) Lemma 4.1 and App. A.3, Lemma A.3/A.3.1 (uniform $k$-star restriction, generalized to unate functions, via chains in the cube); KKL Lemma 6.1 (degree-$d$ PTFs, polylog loss). Counting: Winder 1960 ($2^{O(n^2)}$ LTFs); Chow 1961; **Roychowdhury–Siu–Orlitsky 1994 (KW Thm 2.3)**: at most $(2^n+1)^{s+1}$ threshold functions of $s$ fixed functions on $n$ variables. The paper's top-gate count $(2^k+1)^{q+k+1}$ is exactly this theorem. It should be cited as RSO/KW Thm 2.3 rather than only "Chow's theorem". |
| T6 | Fixed-weight counting: survivors keep their live weights, only thresholds vary, giving $O(k+\log s)$ bits per survivor | **Structural fact known; this counting use not found.** The fact that a restricted LTF is $[A(y)+B(z)\ge\theta]$, with weights on live variables fixed and a column-dependent scalar shift, is ubiquitous in algorithmic-method papers (e.g. CTW Thm 4.4 proof; Williams STOC'14; IPS FOCS'13). KW (Cor. 2.2 in the proof of Thm 1.1), KKL (Cor. 6.5: $O(s^dn+sn^{d+1})$ bits) and CSS (Lemma 9.6, Cor. 2.10: $2^{O(m^2)}$ per gate) all count *all* LTFs on the live bits, about $k^2$ bits per gate. **Nag's "one scalar offset per column"** (TR26-167 v2, §1.2 table and App. A.2 "Exact residualization") is a *different* device: constant bottom gates are removed exactly and their contribution is folded into one scalar offset of the **top** gate per column. It does not count bottom-gate thresholds. | The key enabler is that the counting family depends on the *fixed circuit* and $\sigma$, not on the random table. This is impossible in the Kolmogorov-style arguments of KKL and CSS, where the decoder cannot be given the circuit, and is not done in KW, who fix a circuit-independent hard table. The paper should state this point explicitly. |
| T7 | Correlation bound uniform over all survivor counts $q$ (deviation $\alpha\sqrt q+\beta$), then $\mathbb E\sqrt U\le\sqrt{\mathbb EU}$ instead of Markov | **Not found in this context.** Each component (union bound with $q$-dependent deviation, Jensen/Cauchy–Schwarz) is textbook. KW Thm 1.1 proof, KKL Thm 6.3 proof and CSS all use Markov on the survivor count. I found no prior KW-style argument that removes the Markov loss this way. | Standard tools only, e.g. Boucheron–Lugosi–Massart, *Concentration Inequalities* (2013). |
| T8 | Nearly-orthogonal-vectors bound: if $\lvert\langle v_i,v_j\rangle\rvert\le\delta M$ and $\lvert\langle T,v_i\rangle\rvert\ge\gamma M$ for all $i$, then $t(\gamma^2-\delta)\le1$ | **Known.** KW Lemma 6.1 proves a version via PSD Gram matrices. The sharp form $t\le(1-\delta)/(\gamma^2-\delta)$ is the Johnson bound in correlation form; it is also the standard SQ-dimension / Bessel-type inequality. The paper's own proof gives $t(\gamma^2-\delta)\le1$ because it bounds $t(t-1)\delta$ by $t^2\delta$. | KW Lemma 6.1; S. M. Johnson 1962 (Johnson bound); Guruswami, *List Decoding of Error-Correcting Codes*, LNCS 3282 (2004), Ch. 3 (Johnson bounds); Blum–Furst–Jackson–Kearns–Mansour–Rudich STOC 1994 (orthogonal case, $\le1/\gamma^2$); Szörényi ALT 2009 and Feldman (arXiv:1002.3183) for the almost-orthogonal SQ versions. I did not check exact theorem numbers in Johnson, Guruswami or Szörényi; cite them by chapter or section. |
| T9 | Fixing the circuit before the hard input (quantifier swap) for $B_n$ | **Not found for $B_n$.** It is a standard probabilistic-method move. KW (Cor. 6.2, proof of Thm 1.3), CSS (Lemma 9.7) and KKL (Thm 6.8, a Kolmogorov-random seed) all fix one seed that is bad for *all* small circuits. | No prior use for $B_n$ found. |

**Errata and known issues with KW's restriction lemmas.**
- No public erratum or correction was found. arXiv has only v1, ECCC TR15-188 has no listed revision, and searches for erratum, error and correction found nothing.
- Independent re-proofs exist that a paper can cite next to its own repairs:
  - **CTW App. A.3** (Lemma A.3/A.3.1) for the uniform-$k$-star version of KW Lemma 1.1;
  - **KKL Lemma 6.1**, eq. (44)–(45), for gate and wire survival under block restrictions (polylog loss, PTFs);
  - **CSS Lemma 9.1**, a different structural lemma recovering KW's depth-3 bounds up to $n^{o(1)}$.
- I found no published discussion of KW's $\varepsilon$-range issue (Cor. 2.2 needing $\varepsilon^2 2^n\gg n^2$). Nag (TR26-167 §1.2) quotes KW's range "$\varepsilon\gg\sqrt{\log n/n}$" without comment.

---

## 3. Queries run

Web searches (mode in brackets):
1. `Andreev's function depth-two threshold circuit upper bound` [extended]
2. `Kane Williams depth-two threshold circuits Andreev lower bound improved follow-up` [extended]
3. `"THR∘THR" OR "THR o THR" lower bound gates explicit function polynomial time 2017..2026` [standard]
4. `eccc.weizmann.ac.il depth-2 threshold circuits lower bound 2025 2026` [extended]
5. `Lijie Chen "Toward Super-Polynomial Size Lower Bounds for Depth-Two Threshold Circuits" abstract` [standard]
6. `Hansen Podolskii "Polynomial threshold functions and Boolean threshold circuits" depth 2 THR MAJ` [standard]
7. `parity decision tree depth-two threshold circuit simulation size sparse polynomial over parities MAJ∘MAJ` [extended]
8. `Kabanets Kane Lu "A polynomial restriction lemma with applications" abstract wire lower bound n^{3/2+1/d}` [standard]
9. `Kabanets Lu "Satisfiability and derandomization for small polynomial threshold circuits" gate lower bound` [standard]
10. `Chen Santhanam Srinivasan "Average-case lower bounds and satisfiability algorithms for small threshold circuits" Andreev correlation n^{1.5}` [standard]
11. `multiplexer addressing function threshold circuit depth 2 size O(n^2) OR quadratic "addressing function" OR "multiplexer" majority circuits` [extended]
12. `"Andreev" function "LTF∘LTF" OR "depth-two threshold" OR "THR∘THR" upper bound quadratic 2020..2026` [extended]
13. `"approximate majority" depth-three threshold circuits top fan-in lower bound Andreev TC0_3` [standard]
14. `Zhenjian Lu PhD thesis Simon Fraser threshold circuits polynomial threshold functions lower bounds Andreev` [standard]
15. `depth-2 threshold circuit gate lower bound explicit function in P better than n^{1.5} "Kane and Williams" improved` [extended]
16. `Andreev function communication complexity every partition discrepancy sign rank threshold circuit lower bound barrier` [standard]
17. `threshold circuit construction product of linear form and parity "(-1)^" identity depth-two symmetric function weighted sum times parity` [extended]
18. `statistical query dimension almost orthogonal functions bound number correlated "1/(γ^2" Szörényi Yang lemma` [standard]
19. `Amano Maruoka "On the complexity of depth-2 circuits with threshold gates" MFCS 2005 results` [standard]
20. `Szörényi "Characterizing statistical query learning: simplified notions and proofs" ALT 2009` [standard]
21. `"Andreev" function mod 3 OR "mod p" variant parities replaced by MOD_p threshold circuits generalization` [standard] — **failed (search-tool error), no results**
22. `Kane Williams random restriction lemma linear threshold functions erratum OR error OR correction Littlewood-Offord block restriction` [standard]
23. `Chen Ren "Strong average-case lower bounds from non-trivial derandomization" THR∘THR average-case lower bound E^NP` [standard]
24. `Mahajan "Depth-2 threshold circuits: provable limitations" Resonance 2019 Andreev` [standard]
25. `Andreev function variant block sums modulo p multiplexer threshold circuit` [standard] — **failed (search-tool error), no results**
26. `"Andreev's function" generalization Z_p residues address circuit complexity` [standard]
27. `Siu Roychowdhury Kailath "Depth-size tradeoffs for neural computation" telescoping symmetric functions threshold circuits` [standard]
28. `sum of functions of linear forms threshold circuit "THR∘MAJ" exact computation Fourier coefficients times character polarization trick multiplication depth-2` [standard]

Full texts downloaded and searched (keywords: Andreev, Kane, explicit, restriction, Markov, Jensen, Cauchy, Chow, offset, residual, survivor, upper bound, communication):
- KW arXiv:1511.07860v1
- KKL ECCC TR17-026
- CSS arXiv:1806.06290 (ToC 14(9))
- Kabanets–Lu ECCC TR18-115
- L. Chen arXiv:1805.10698
- Hansen–Podolskii ECCC TR13-021
- CTW ECCC TR26-039
- Nag ECCC TR26-167 (v1, Aug 17 2026; v2, Sep 15 2026)

Pages read:
- ECCC abstract pages for TR26-039 and TR26-167, including the ECCC comments on TR26-167;
- GitHub complexitylib issue #2347 and PRs #2364 and #2366;
- the GitHub repo MacchaCat/depth2-threshold-barriers (README only). It does not mention Andreev or Kane–Williams.

Not reached or not done:
- Google Scholar "cited by" pages for KW;
- the full text of Mahajan's Resonance survey (abstract only);
- Amano–Maruoka MFCS 2005 (bibliographic record only);
- Siu–Roychowdhury–Kailath 1991 (abstract only);
- Tamaki TR16-100 and ACW FOCS'16 (only as cited by CTW and KKL);
- Zhenjian Lu's thesis (abstract only);
- the mod-$p$ searches (tool errors).

---

## 4. Recommended references (full entries)

1. **[KW]** Daniel M. Kane and Ryan Williams. *Super-Linear Gate and Super-Quadratic Wire Lower Bounds for Depth-Two and Depth-Three Threshold Circuits.* STOC 2016, pp. 633–643. arXiv:1511.07860 (v1, 24 Nov 2015); ECCC TR15-188. https://arxiv.org/abs/1511.07860. Cite Thm 1.1, Thm 1.2 (incl. $\mathsf{MOD}_3\circ\mathsf{MOD}_2$ $O(n^2)$), Cor. 1.1, Thm 1.3, Thm 1.4, Lemma 1.1, Lemma 3.1, Thm 2.3, Cor. 2.2, Lemma 6.1, Cor. 6.2, §6 last paragraph, §7 open question 1.
2. **[KKL]** Valentine Kabanets, Daniel M. Kane, and Zhenjian Lu. *A Polynomial Restriction Lemma with Applications.* STOC 2017, pp. 615–628. ECCC TR17-026. https://eccc.weizmann.ac.il/report/2017/026/. Cite Thm 1.1 / Thm 6.3 ($d=1$: $n^{3/2}(\log n)^{-O(1)}$ gates and $n^{5/2}(\log n)^{-O(1)}$ wires, worst case, Andreev); Thm 1.2 / Thm 6.8 ($B_{n,\epsilon}$, MAJ of depth-2); Lemma 6.1; Cor. 6.5.
3. **[CSS]** Ruiwen Chen, Rahul Santhanam, and Srikanth Srinivasan. *Average-Case Lower Bounds and Satisfiability Algorithms for Small Threshold Circuits.* CCC 2016, LIPIcs 50, 1:1–1:35; journal version Theory of Computing 14(9):1–55, 2018. ECCC TR15-191; arXiv:1806.06290. https://theoryofcomputing.org/articles/v014a009/. Cite §9, Lemma 9.1, Thm 9.3, Lemma 9.6, Lemma 9.7.
4. **[CTW]** Lijie Chen, Avishay Tal, and Yichuan Wang. *Super-quadratic Lower Bounds for Depth-2 Linear Threshold Circuits.* STOC 2026. ECCC TR26-039. https://eccc.weizmann.ac.il/report/2026/039/. Cite Thm 1.1, §1 (state of the art for $\mathsf P$ vs $\mathsf E^{\mathsf{NP}}$), Lemma 4.1 and App. A.3 (alternative proof of the KW restriction lemma).
5. **[Nag]** Dev Nag. *Almost-Everywhere Near-Cubic Wire Lower Bounds for $\mathsf{SYM}\circ\mathsf{THR}$ and $\mathsf{THR}\circ\mathsf{THR}$.* ECCC TR26-167, 2026 (v1 17 Aug 2026, v2 15 Sep 2026). https://eccc.weizmann.ac.il/report/2026/167/. Unrefereed. The ECCC page carries a critical comment by O. Goldreich and an author reply.
6. **[Tam16]** Suguru Tamaki. *A Satisfiability Algorithm for Depth Two Circuits with a Sub-Quadratic Number of Symmetric and Threshold Gates.* ECCC TR16-100, 2016. https://eccc.weizmann.ac.il/report/2016/100/
7. **[ACW16]** Josh Alman, Timothy M. Chan, and R. Ryan Williams. *Polynomial Representations of Threshold Functions and Algorithmic Applications.* FOCS 2016, pp. 467–476. doi:10.1109/FOCS.2016.57.
8. **[HP13]** Kristoffer Arnsfelt Hansen and Vladimir V. Podolskii. *Polynomial Threshold Functions and Boolean Threshold Circuits.* MFCS 2013, LNCS 8087, doi:10.1007/978-3-642-40313-2_46 (page range not verified); Information and Computation 240:56–73, 2015. ECCC TR13-021. https://eccc.weizmann.ac.il/report/2013/021/. Cite Thm 5 ($\mathsf{PTF}_{\{1,2\}}(\mathrm{poly})=\mathsf{THR}\circ\mathsf{MAJ}$).
9. **[HMPST93]** András Hajnal, Wolfgang Maass, Pavel Pudlák, Mario Szegedy, and György Turán. *Threshold Circuits of Bounded Depth.* J. Comput. Syst. Sci. 46(2):129–154, 1993. Cite Prop. 1 (staircase for symmetric functions).
10. **[ROS94]** Vwani P. Roychowdhury, Kai-Yeung Siu, and Alon Orlitsky. *Neural Models and Spectral Methods.* In: Theoretical Advances in Neural Computation and Learning, Kluwer, 1994. This is KW's [ROS94b], the source of KW Thm 2.3 (counting threshold functions of fixed features).
11. **[Chow61]** Chao-Kong Chow. *On the Characterization of Threshold Functions.* Proc. 2nd Annual Symp. on Switching Circuit Theory and Logical Design (FOCS), pp. 34–38, 1961.
12. **[Win60]** Robert O. Winder. *Single Stage Threshold Logic.* Proc. 1st Annual Symp. on Switching Circuit Theory and Logical Design (FOCS), 1960.
13. **[Erd45]** Paul Erdős. *On a Lemma of Littlewood and Offord.* Bull. Amer. Math. Soc. 51:898–902, 1945.
14. **[CM17]** Arkadev Chattopadhyay and Nikhil S. Mande. *Weights at the Bottom Matter When the Top is Heavy.* ECCC TR17-083; arXiv:1705.02397, 2017. (Linear-size $\mathsf{THR}\circ\mathsf{THR}$ function with exponential sign rank.)
15. **[FKL+01]** Jürgen Forster, Matthias Krause, Satyanarayana V. Lokam, Rustam Mubarakzjanov, Niels Schmitt, and Hans Ulrich Simon. *Relations Between Communication Complexity, Linear Arrangements, and Computational Complexity.* FSTTCS 2001, LNCS 2245, pp. 171–182.
16. **[Johnson / Guruswami]** Venkatesan Guruswami. *List Decoding of Error-Correcting Codes.* LNCS 3282, Springer, 2004, Ch. 3 (Johnson bounds). Optionally also S. M. Johnson, *A New Upper Bound for Error-Correcting Codes*, IRE Trans. Inform. Theory 8(3):203–207, 1962.
17. **[Szö09]** Balázs Szörényi. *Characterizing Statistical Query Learning: Simplified Notions and Proofs.* ALT 2009, LNCS 5809, pp. 186–200. doi:10.1007/978-3-642-04414-4_18. (Optional, for the almost-orthogonal SQ form of T8.)
18. **[O'D14]** Ryan O'Donnell. *Analysis of Boolean Functions.* Cambridge University Press, 2014. (Fourier inversion, T1.)
19. **[Chen18]** Lijie Chen. *Toward Super-Polynomial Size Lower Bounds for Depth-Two Threshold Circuits.* arXiv:1805.10698, 2018. (Context only.)
20. **[Formalization]** cslib-community/complexitylib, issue #2347 (2026-11-02) and PRs #2364 and #2366 (merged 2026-11-03): https://github.com/cslib-community/complexitylib/issues/2347. Cite this as the public record of the formalization.

Optional context: Impagliazzo–Paturi–Saks, *Size–Depth Tradeoffs for Threshold Circuits*, SIAM J. Comput. 26(3):693–707, 1997 (parity wire bound $n^{3/2}$); Goldmann–Håstad–Razborov, *Majority Gates vs. General Weighted Threshold Gates*, Comput. Complexity 2:277–300, 1992.
