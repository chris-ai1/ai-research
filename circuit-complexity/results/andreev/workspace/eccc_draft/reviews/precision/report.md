Authors: Christian Reitwiessner

# Whole-paper precision review and proposed revision

The proposal is complete: [paper.tex](/tmp/andreev_gap/precision_revision/paper.tex), [paper.pdf](/tmp/andreev_gap/precision_revision/paper.pdf), and [paper.diff](/tmp/andreev_gap/precision_revision/paper.diff). I found no mathematical defect requiring a change to the stated numerical bounds. The changes make types, quantifier order, domains, function arguments, parameter dependencies, and asymptotic scope explicit. All nine result statements and their nine proofs remain.

The proposal is **12 pages**, exceeding the original 8–10-page target. It keeps the original 11pt article class and one-inch margins. Repeated road-map prose was removed, but no proof was omitted and no font or margin was compressed. Integration and any further length decision remain with the parent.

I read the canonical source standalone before making changes. No previous reports or new literature searches were needed. All work and generated check outputs are confined to this directory. The canonical source, canonical PDF, and canonical check outputs were not edited.

## Statement-by-statement findings

| Location in proposed source | Finding and revision | Mathematical scope checked |
|---|---|---|
| Introduction and definitions | Explicit positive integer parameters $k,m$, $N=2^k$, $n=N+km$; table space $\mathcal X$, address space $\mathcal A$, typed map $b$, and typed $A_{k,m}$. Circuit $C$ is an object whose evaluated output is denoted $C(u)$. Sign coherence is defined for gates and circuits. | Arbitrary real weights, arbitrary real thresholds, raw input wires to the top gate, and combined-edge wire counts are retained. Balance is an asymptotic regime in $k$, not an extra finite-parameter assumption on other results. |
| [Lemma 2.1](/tmp/andreev_gap/precision_revision/paper.tex:156) | Preserves the parent's corrected affine identity, including $d\ge1$, an integer-valued affine map, fixed integer endpoints bounding **every** input, a typed function $g$, and a proof fixing $u$. Replaces the informal consequence about a “score” by a quantified statement for $J\ge0$ maps on the same input cube and an affine top term. | Gate cost counts nonzero numerical finite differences. Constants are absorbed by the output threshold; affine input terms use direct wires. The case $J=0$ is allowed. |
| Lookup definitions and [Theorem 2.2](/tmp/andreev_gap/precision_revision/paper.tex:216) | $X_S:\mathcal X\to\{-N,-N+2,\ldots,N\}$ and $t_S:\mathcal A\to\{0,\ldots,m|S|\}$ are maps; all lookup identities use $X_S(x)$, $t_S(a)$, and $b(a)$. The matrix $H$ is fixed, while $v(x)$ and $X(x)$ are evaluated vectors. The scalar function $\varphi$ is defined outside the proof because later sections reuse it. | Exact finite bottom-gate count $2N(N-1)+kmN$ and one output gate are unchanged. The scalar identity is quantified for every even integer and every integer. Integer weight bounds have absolute polynomial degree and constant. |
| [Theorem 3.1](/tmp/andreev_gap/precision_revision/paper.tex:242) and its proof | The theorem now begins with one absolute constant $K$ before quantification over $k,\delta,\varepsilon$. Both circuits are explicitly deterministic. $P_*$, $P_R$, $e_S$, $D_S$, $f_R$, the vote $V_r$, and the compiled circuit $C_{r,R}$ have declared domains or formulas with arguments. | Error range $0<\delta\le1/2$, advantage range $N^{-1/2}\le\varepsilon\le1/8$, the larger-advantage conversion, and both resource bounds are unchanged. No masks are introduced. |
| [Lemma 3.2](/tmp/andreev_gap/precision_revision/paper.tex:260) | $g,h:\mathbb Z\to\mathbb R$ are fixed functions with a universally quantified oddness condition. The expectation evaluates them at random coefficient values. The proof uses a defined table bijection; a fixed address can index the functions, but is not being averaged within this lemma. | No independence of different Walsh coefficients is asserted. Conditional orthogonality for every fixed address is what justifies averaging later. |
| [Lemma 4.1](/tmp/andreev_gap/precision_revision/paper.tex:415) | The circuit $C$ is fixed; its bottom output maps $\gamma_j$ are typed. The induced map $x\mapsto(z\mapsto C(x,z))$ into the space of Boolean functions is explicitly injective. $D:\{0,1\}^N\to\{0,\ldots,G\}$ is a counting function, and $D(\boldsymbol x)$ is a random variable. Entropy $\mathsf H$ is distinct from the Walsh matrix $H$. | Arbitrary positive integers $N,h$ and nonnegative integer $G$ are allowed; this lemma does not assume $N$ is a power of two. The proof first bounds each fiber $\{x:D(x)=d\}$ for $0\le d\le G$, then applies entropy. Direct table wires only shift the output threshold once gate functions are specified. |
| [Theorem 4.2](/tmp/andreev_gap/precision_revision/paper.tex:455) | $D_0$ is explicitly a nonnegative scalar depending on $k,G$. A separate map $\iota$ sends prefix-count vectors to address inputs, avoiding reuse of the input symbol $a$ as a map. For a fixed gate and table, $F_{j,x}$ is its weighted input-sum function on the count grid. | $F_{j,x}$ is only asserted to be coordinatewise monotone in chosen directions, **not affine in the block counts**; unequal weights make that distinction necessary. Both finite inequalities and the balanced $\Omega(n^2/\log^3n)$ bound are unchanged. The consequence for $O(n^{2-\eta})$ families is quantified for fixed real $\eta>0$ and sufficiently large admissible $k$. |
| [Theorem A.1](/tmp/andreev_gap/precision_revision/paper.tex:559) | Every auxiliary map, integer constant, and dependency is identified. The main formula is the integer-valued map $P(x,a)$. The old scalar correction constant $C$ becomes $C_0$ so it is not confused with circuit notation. Dense algebra uses explicitly fixed inputs and different scalar names, as detailed below. | The exact gate bound, gate-sharing subtraction, strict margin $N$, integer weights, $5/16$ leading coefficient, and negative $n\log n/4$ term are unchanged. The asymptotic expressions are described as **upper bounds**, not forced equalities for the size of a circuit after optional gate removal. |
| [Lemma B.1](/tmp/andreev_gap/precision_revision/paper.tex:711) | Predicates $p_j$, real coefficients $\lambda_j$, affine map $B$, output expression $F$, and parity $f$ are typed. The hypothesis is $f(z)F(z)>0$ for every input. Functional dependence means that for each coordinate there exists an input pair differing only there on which the predicate changes. | The conclusion explicitly gives a predicate with $\lambda_j\ne0$. This is the consequence of the same correlation proof; it does not change the ensuing bound. The conditions $d\ge2$ and $J\ge0$ are retained explicitly. |
| [Proposition B.2](/tmp/andreev_gap/precision_revision/paper.tex:736) | The quantifier is **for each gate $j$**, its address vector is zero or $v_j=\rho_j\sigma_j$ for its own real $\rho_j>0$ and its own sign vector $\sigma_j$. The fixed table, remaining live variables, strict perturbation, and each restriction are specified. | The perturbation constant works simultaneously on the finite remaining input domain. Twice the target bit minus one is $(-1)^{d+1}f(z)$, fixing the sign convention. Restricted coefficients are $(\rho_j/2)(s_{j,i}+t_i u_{j,i})$. Nonzero coefficients are used only as a **necessary** condition for dependence, not a sufficient one. The $2^d$ bound and the general bounded-magnitude full-support counterexample remain unchanged. |

## Dependencies and quantifiers requiring particular care

**Approximation.** Bold $\boldsymbol x,\boldsymbol a$ denote independent uniform random inputs; ordinary $x,a$ denote fixed inputs. The partial vote fixes integer $r\in\{0,\ldots,k\}$ and sets $q=2^r$, $L=N/q$. The function $P_*$ therefore depends on $k,m,r$; $P_R$ also depends on the fixed integer radius $R$. Each $e_S$ depends on $k,m,S,R$. For fixed $a$, the explicitly displayed map

$$u\mapsto\eta_S\big((f_R-\varphi)(u+D_S(a))+(f_R-\varphi)(u-D_S(a))\big)$$

is odd on all of $\mathbb Z$, and its value at the even integer $X_S(x)$ is $e_S(x,a)$. This avoids the ill-defined phrase “the function $e_S$ is odd in the function $X_S$,” while also avoiding a false claim about the exact reflected identity at odd coefficient values.

The proof separately names the random variables $U,V$ and the numerical variance proxies $v_S,v$. The radius depends only on $k,m,r,\delta$, never on the input. At balance $v\le5N/4$, so the constants are uniform even when $\delta$ or $\varepsilon$ varies with $k$. In Part 2, the stated range is nonempty only for $N\ge64$, and the chosen least power of two actually satisfies $q\le N/2$. The revised proof uses that stronger elementary observation to remove an unreachable branch, without altering the algorithm or its applicability range. For tiny $\delta$, capping $R$ at $N+km$ makes truncation exact and preserves the upper bound.

**Refined appendix.** Globally within Appendix A, $s_i,\sigma,t_S$ are maps of address inputs; $Z,E,W_S$ are maps of table inputs; $w$ and $P$ are maps of both. Constants $\alpha,R,C_0$ depend only on $k,m$; $\kappa_S,r_S$ additionally depend on $S$. Only after fixing $x,a$ does the proof introduce scalar abbreviations

$$u_i=s_i(a),\quad u=\sigma(a),\quad z=Z(x),\quad e=E(x),\quad\omega=w(x,a),\quad\omega_S=W_S(x),\quad\tau_S=t_S(a),\quad\beta=b(a).$$

These are different symbols from the maps. The subset and coordinate summation ranges are stated. The closed form restores $P(x,a)$ and function arguments, and the gate implementation explicitly leaves the pointwise convention. No map is silently equated with a numerical value.

**Asymptotic interpretation.** Floor and exact balance are specified as sequences with $k\to\infty$ through admissible integers. Unqualified implicit constants are absolute and uniform in admissible parameters. Statements about fixed-error exponents explicitly fix a real error in $(0,1/2)$. The exact-balance gate-bound expression, including the top gate, expands to

$$\frac5{16}n^2-\frac n4\log_2(n/2)+3n-2\log_2(n/2)-1,$$

which confirms the retained $O(n)$ remainder. This is an expansion of the offered **bound**, not a lower bound on the gates actually retained after sharing.

## Preserved material and checks

Automated source comparisons confirm that the entire abstract, its visible margin TODO, the complete epsilon comparison table and caption (including both applicability ranges), the literature-comparison prose, and the bibliography are byte-identical to the frozen source. The cslib-frontier link is unchanged. All mathematical result and proof environments are retained. The visible author and copyright headers remain Christian Reitwiessner; the new PDF also has Christian Reitwiessner in its author metadata.

The three existing scripts were copied byte-for-byte into `validation/` before execution, so their file writes cannot overwrite canonical outputs:

- `verify_results.py`: passed 58,264 exhaustive small table/block-count cases and 80 sampled larger cases; gate construction, closed form, strict margins, and counts agree.
- `approximation_checks.py`: passed 140 odd pair moments, 7,268 table involution cases, 14,820 conditional error moments, 514,200 complete-expression inputs, 671 compiled staircase values, 135 tail-bound cases, 135 majority-agreement cases, and 2,976 raw-gate expression inputs. This is the relevant **unmasked** approximation suite.
- `restriction_checks.py`: passed 7,430 coherent-cube threshold tests and 112,320 pairing/missing-coordinate checks. Its legacy mask tests also pass; those tests do not introduce masks into the paper and are not being offered as evidence for the new unmasked argument.
- New `validation/precision_audit.py`: passed all six transcribed intermediate appendix identities, the closed form, and the signed margin on **25,844** inputs covering $k,m\in\{1,2,3\}$. It also checks the exact-balance size expansion at $k=1,2,4,8,16$ and the preservation assertions above.

Outputs are in `validation/`; [precision_audit.json](/tmp/andreev_gap/precision_revision/validation/precision_audit.json) records the additional audit. These finite checks supplement the universal proofs; they are not a formal proof of the theorem statements.

## Build and layout

Build command, run in this proposal directory:

```text
/tmp/andreev-pdf-tools/tectonic --keep-logs paper.tex
```

The final build succeeds. The final log has zero overfull boxes, zero underfull boxes, and no unresolved references or citations. Tectonic emits a nonfatal system Fontconfig configuration message. An earlier first-time font download failed transiently with “No space left on device”; retry succeeded without deleting other files or changing the typography.

The PDF has 12 US-letter pages, with unchanged 11pt body text and one-inch margins. I inspected the all-page contact sheet and full-page renderings of the abstract, approximation formulas, entropy proof, and refined algebra. The margin TODO is visible; displayed formulas fit without clipping. The affine lemma begins on page 2 and continues on page 3. The bibliography starts on page 11 and continues on page 12. These are ordinary page breaks, but the final bibliography-only continuation and the two-page overrun are editorial tradeoffs for the parent to consider. The proposal does **not** claim to meet the original page limit.

[Layout status](/tmp/andreev_gap/precision_revision/layout/status.json) records the final checks. Rendered pages and the contact sheet are in `layout/`.

## Remaining scope and ambiguities

No remaining substantive mathematical typing or dependency ambiguity was identified in the revised result statements and proofs. The following limitations are intentional:

- The existing table notation $\varepsilon\gg\sqrt{\log n/n}$ is retained verbatim. Its earlier-literature range has not been sharpened or reinterpreted. Literature accuracy was not re-researched in this precision pass.
- The abstract TODO remains deliberately unresolved, as requested.
- “Explicit” asserts the displayed deterministic construction and parameter choices; no new construction-time or real-parameter encoding complexity claim is made.
- The 8–10-page target is unmet. Recovering it requires a separate substantive shortening decision; this proposal does not silently trade away proofs or typing.
- The canonical PDF was already older than the parent's just-corrected affine source. It remains untouched; this proposal's PDF is built from the complete proposed source.

## SHA-256 provenance

| Artifact | SHA-256 |
|---|---|
| Frozen canonical source (`baseline.tex`) | `0002fdab65e487bfdc9d945767e12d9becd5af8a93995d0f7b3fd3ed597e32f3` |
| Canonical source at completion, unchanged | `0002fdab65e487bfdc9d945767e12d9becd5af8a93995d0f7b3fd3ed597e32f3` |
| Canonical PDF, unchanged | `1f8c2520670f892a53a8e33a4d2193cf73d72f1740085d7dd519f682f0cac2ee` |
| Proposed `paper.tex` | `2d52ccd838d73227dcd1be86c6b00a52f9bbe374e8193ec27f8efe8667344966` |
| Proposed `paper.pdf` | `d59d55d6c7e00f8c2c7762d25afd40833e6d0ecf904c11a1fbefcd6826323378` |

[manifest.json](/tmp/andreev_gap/precision_revision/manifest.json) also records copied-script identity and the final source label locations. `revise.py` reproduces the proposal from `baseline.tex`; `paper.diff` is the unified integration diff. No canonical files have been integrated or replaced.
