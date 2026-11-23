<!-- Copyright (c) 2026 Christian Reitwiessner. All rights reserved. -->
Authors: Christian Reitwiessner

# Extractors and depth-two threshold complexity of ordinary Andreev

Research cutoff: 2026-11-09. Work performed independently, without subagents, and saved incrementally. The source workspace was read-only during research; the completed report was subsequently prepared for the user's requested private-repository archive. No shared paper was edited. Mathematical results retain their original attribution.

**Result:** no new fixed-power upper or lower bound for unrestricted ordinary Andreev was obtained. Constant-error complexity already has matching $3/2$ exponents. This report supplies source-specific proofs and obstructions and verifies relevant extractor results through the cutoff. Its elementary exact $\Omega(n^{3/2}/\log n)$ lower bound for the restricted one-table-bit model is valid but **superseded** by the repository's completed $\Omega(n^{32/19}/\log^{45/19}n)$ slicing consequence. See Sections 4–8 for the arguments, the archive synchronization note in Section 7, and Section 9 for the bounds and unresolved targets.

## 1. Scope and verified starting point

Write $N=2^k$, $b_i=\bigoplus_{j=1}^m a_{i,j}$, and $A(x,a)=x_b$, on $n=N+km$ bits. Exact balance means $km=N$; the integer constraint $k\mid 2^k$ matters, and other sizes use floor balance/padding. The circuit is $\mathrm{THR}\circ\mathrm{THR}$ with arbitrary real weights and direct raw-input wires into the top gate. Size below counts bottom gates, up to an additive one for the top. Uniform average case means uniform independent **table and raw address** bits. Advantage $\varepsilon$ means agreement $1/2+\varepsilon$; error $\delta$ means agreement $1-\delta$.

Read first: the requested `research_backup/docs/RESEARCH_STATE.md`, `threshold_paper/novelty_search.md`, `andreev_depth_two_bounds.md`, `kw_applications.md`, `kane_williams_erratum.md`, and relevant portions of `threshold_paper/paper.tex` in the source workspace. Earlier reports are historical, not necessarily current theorem statements.

**Baseline correction discovered on reading the current manuscript.** The latest `paper.tex`, theorem `thm:avgupper` and its proof (lines 486–610), already removes the union-bound $\sqrt{\log n}$ loss for fixed error:

$$
S_{1-\delta}=O\!\left(n^{3/2}\sqrt{\log(1/\delta)}\right),\qquad 0<\delta\le 1/2.
$$

It also proves

$$
S_{1/2+\varepsilon}=O\!\left(\varepsilon^2 n^{3/2}\sqrt{\log(1/\varepsilon)}\right),\qquad N^{-1/2}\le\varepsilon\le1/8.
$$

These are inherited results, not findings of this investigation. The proof uses independent address masks and a second-moment error estimate; the masks are fixed nonuniformly by averaging. Exact computation has the inherited $5n^2/16+o(n^2)$ upper bound. The inherited unrestricted lower bounds are $\Omega(\varepsilon^2n^{3/2}/\log^2n)$ gates and $\Omega(\varepsilon^2n^{5/2}/\log^{5/2}n)$ support wires, in the proved common range $\varepsilon\ge3(k+2)/\sqrt N$. Pending hand proofs extending the gate advantage range must not be confused with formalized results. The coherent $\Omega(n^2/\log^3n)$ bound restricts within-block signs and is not an unrestricted bound.

## 2. Evidence and status discipline

The requested primary source is Kane–Williams, [arXiv:1511.07860v1](https://arxiv.org/pdf/1511.07860), dated 24 November 2015. Its ordinary function, its code-based $B_n$, and later extractor-based generalized functions will be kept distinct. Local errata describe proof repairs and an advantage-range gap; quoting the original abstract alone is insufficient.

Subsequent sections distinguish **proved deductions in this report**, **verified external theorem statements**, **conditional implications**, **refutations of specified routes**, and **unresolved possibilities**. No assertion that a literature search proves novelty or exhaustively establishes the latest result is intended. Exact source URLs, inspected theorem numbers, dates, and available PDF hashes are saved in [evidence.json](evidence.json).

## 3. The surviving sources: exact calculation

**Proposition 3.1 (proved here; elementary source audit).** Let a coordinate restriction leave $t_i$ live raw variables in block $i$. Put $t=\sum_i t_i$ and $d=|\{i:t_i>0\}|$. Uniform live inputs form an oblivious bit-fixing (OBF) source of entropy exactly $t$ in the $M=km$ raw coordinates. Their parity address is uniform on a coordinate affine subcube of dimension exactly $d$, with fibers of size $2^{t-d}$. With one live bit in every block, $t=d=k$ and $b=u\oplus o$ is a bijection. With the table fixed, the restricted target contains exactly $2^d$ independent labels when the table is drawn uniformly, regardless of $t$.

*Proof.* Each nonempty block parity is balanced and different blocks use disjoint live bits. The linear parity map has rank $d$, so each image has $2^{t-d}$ preimages. Distinct address values use distinct independent table coordinates. $\square$

Consequences:

- On the actual one-per-block source family, the ordinary parity map is already a **zero-error, seedless extractor of all $k$ surviving bits**. Generic OBF extractors solve a harder problem (arbitrary free positions), not an entropy defect in this restricted map.
- Keeping more variables in a block increases raw entropy but does not increase independent labels. If the $2^t$ restricted inputs are treated as independent random labels in a counting argument, that argument is incorrect.
- Leaving fewer than $k$ blocks active reduces the table-label budget from $N$ to $2^d$. A map applied after restriction cannot manufacture new independent table bits.

**Proposition 3.2 (proved here; affine-source obstruction).** For any $c\in\{0,1\}^k$, the source uniform on

$$
V_c=\{a:b(a)=c\}
$$

is affine of dimension $M-k$, but $b(V_c)$ is constant. Its statistical distance from $U_k$ is $1-2^{-k}$. Thus ordinary parity addressing is not an affine extractor even at entropy $M-k$, very close to full entropy. A fixed table makes $A$ constant on this source. These sources are not the transversal coordinate restrictions of Proposition 3.1. $\square$

**Threshold conditioning is a third source model.** Fixing a threshold's output gives a Boolean cube intersected with a real halfspace; fixing many outputs gives an intersection of halfspaces. Such sets need not be affine or OBF. For example, $\{00,01,10\}$ is a halfspace cell of size three, hence is not an affine subspace. Conditioning independent blocks on their joint sum can also destroy independence: conditioning two fair bits on their sum being one leaves $\{01,10\}$. A lower bound that invokes affine or two-source extraction after such conditioning needs an additional structural theorem.

If a transcript $T$ has at most $2^L$ possible values and the original input $X$ is uniform on $\{0,1\}^r$, then, outside transcript values of total probability at most $\tau$,

$$
H_\infty(X\mid T=t)\ge r-L-\log_2(1/\tau).
$$

Indeed, there are at most $2^L$ cells, and cells smaller than $\tau2^{r-L}$ have total size at most $\tau2^r$. This is an entropy statement only; it does not make the cells affine, independent-source, or efficiently samplable without rejection. Conditioning on the current live input can also invalidate the independence of any proposed seed.

## 4. A direct extractor/information proof of the existing lower-bound scale

This section gives a self-contained reformulation, not a claim of a new exponent or priority. It explains exactly why ordinary lookup, unlike a purpose-built extractor, has a square-root leakage tradeoff.

**Lemma 4.1 (proved here: random access under leakage).** Let $X$ be a uniform $N$-bit table, $T$ any information about $X$, and $J$ uniform on $[N]$, independent of $(X,T)$. If a predictor $g(T,J)$ makes error at most $\delta\le1/2$, then

$$
I(X;T)\ge N\bigl(1-h_2(\delta)\bigr).\tag{4.1}
$$

Here entropies and mutual information use base two. In particular, advantage $\varepsilon$ requires

$$
I(X;T)\ge \frac{2}{\ln2}\,N\varepsilon^2.\tag{4.2}
$$

*Proof.* For each coordinate use its Bayes-optimal predictor from $T$, with error $p_i\le1/2$. Their average error is at most $\delta$. Binary conditional entropy satisfies $H(X_i\mid T)\le h_2(p_i)$. Subadditivity and concavity give $H(X\mid T)\le\sum_iH(X_i\mid T)\le Nh_2(\delta)$. Subtract from $H(X)=N$. Finally $1-h_2(1/2-\varepsilon)\ge2\varepsilon^2/\ln2$. $\square$

**Equivalent high-entropy extractor fact.** For an arbitrary distribution $Y$ on $N$ bits with $H_\infty(Y)\ge N-a$, coordinate sampling $\mathrm{Index}(Y,J)=Y_J$ satisfies

$$
\operatorname{TV}\bigl((J,Y_J),(J,U_1)\bigr)
\le \sqrt{\frac{(\ln2)a}{2N}}.\tag{4.3}
$$

To prove this, put $p_i=\Pr[Y_i=1]$. Entropy subadditivity gives $\sum_i(1-h_2(p_i))\le a$, while $1-h_2(p_i)\ge2(p_i-1/2)^2/\ln2$. Average $|p_i-1/2|$ and apply Cauchy–Schwarz. This extractor has seed length $k=\log_2N$ and output length one, but its error is determined by entropy **deficiency** $a$, not just the existence of high entropy. For advantage $\varepsilon$, it needs $a=O(\varepsilon^2N)$ to be useful. It is the prescribed ordinary lookup map, so replacing it by an extractor with a better deficiency/error tradeoff would change the target.

**Proposition 4.2 (proved here: finite restriction/leakage inequality).** Fix a circuit with $S\ge1$ bottom gates, their weights, and their top coefficients. Apply a uniformly random one-live-variable-per-block restriction to addresses. Let $Q$ be its number of nonconstant bottom gates after also fixing a uniform table, and write $B=\mathbb E Q$. If the original circuit has uniform-input error $\delta\le1/2$, then

$$
N\bigl(1-h_2(\delta)\bigr)
\le \log_2(S+1)+B\log_2 S+(B+1)\log_2(N+1).\tag{4.4}
$$

*Proof.* Condition first on the free positions and all fixed address bits; call these data $R$, independent of the random table. Encode the whole restricted Boolean function by: the number $q$ of survivors; their identities (at most $\binom Sq$ choices); each surviving gate's threshold position in its fixed list of at most $N+1$ functions; and the top threshold position. The original live bottom weights, original top coefficients, and original direct-live-input coefficients remain fixed. Once the bottom functions are specified, varying the scalar offset of the top produces at most $N+1$ functions. Thus the number of descriptions with $q$ survivors is at most

$$
\binom Sq(N+1)^{q+1}.
$$

Let $T$ be a deterministic such description. Entropy coding gives

$$
H(T\mid R)\le\log_2(S+1)+\mathbb E[Q]\log_2S+(\mathbb E[Q]+1)\log_2(N+1).
$$

For each fixed $R$, the live address $J=u\oplus o(R)$ is uniform and independent of $(X,T)$. Apply Lemma 4.1 to the conditional Bayes predictor (whose error is at most $1/2$ and at most the circuit's conditional error); average and use concavity of $h_2$ to obtain (4.4). The reconstructed full input is uniform, so the circuit's mean conditional error is its original error. $\square$

Using the repaired threshold restriction estimate $B\le4S\sqrt n/m$, (4.4) implies

$$
S=\Omega\!\left(\frac{\varepsilon^2mN}{\sqrt n\log n}\right)
=\Omega\!\left(\frac{\varepsilon^2n^{3/2}}{\log^2n}\right)\tag{4.5}
$$

at balance, when $S\le n^2$ and $\varepsilon\ge C\sqrt{\log n/N}$ for a sufficiently large constant. Larger $S$ makes the desired bound trivial. The additive $\log n$ term in (4.4) must be retained at smaller advantages. This recovers the fixed-top-weight hand refinement recorded in the source workspace; it does not supersede the separate, pending VC proof with endpoint $C/\sqrt N$. For wires, absorbing single-variable gates changes the top's live coefficients, so this particular fixed-top count cannot simply be reused.

**Why improved extraction alone cannot improve this exponent.** The one-per-block restriction has $N$ independent labels and per-gate survival of order $k/\sqrt N$ for majority gates. Even replacing the residual counting bound by the strongest possible unrestricted Boolean-function bound on $k$ variables cannot demand more than $N$ bottom gates: minterm lookup uses at most $N$. This limits the specified argument template—one restriction, survivor count, and unrestricted residual hardness—to at most order $N^{3/2}/k$. It is not a universal barrier to methods using dependence across restrictions, gate directions, or table-dependent threshold shifts.

**Proposition 4.3 (proved here: the leakage exponent is tight for relevant geometric cells).** For $1\le r\ll N$, there are sources of min-entropy $N-r$, obtained by conditioning $r$ disjoint majority halfspaces, on which the left side of (4.3) is $\Theta(\sqrt{r/N})$.

*Proof.* Partition almost all coordinates into $r$ odd-sized buckets of sizes $\Theta(N/r)$, leaving any parity adjustment coordinates unused. Condition the majority in each bucket to be $+1$. Each condition has probability $1/2$, independently, so the conditioned source is flat with entropy exactly $N-r$. If a bucket has odd size $\ell$, symmetry gives

$$
\mathbb E[\xi_i\mid\operatorname{sgn}(\sum_{j=1}^{\ell}\xi_j)=+1]
=\frac{\mathbb E|\sum_{j=1}^{\ell}\xi_j|}{\ell}=\Theta(\ell^{-1/2}).
$$

Averaging the coordinate biases gives the claim. The central-binomial estimate establishes the displayed asymptotic. Equivalently, leaking all $r$ bucket-majority bits permits prediction of a random table bit with advantage $\Theta(\sqrt{r/N})$. For $r=1$, use $N-1$ coordinates if $N$ is even. $\square$

This does **not** show that every such transcript is generated cheaply by the original circuit after restriction. It does rule out a better black-box error bound for **Index itself** on arbitrary high-entropy sources, or even on intersections of disjoint halfspaces. Exploiting how the transcript is generated is essential for a stronger circuit bound.

## 5. Upper bounds: what extraction can and cannot replace

### 5.1 Address compression, with an optimal information bound

**Proposition 5.1 (proved here).** Let $Z=E(a)$ be any deterministic address-only feature with at most $L$ possible values. Allow an arbitrarily powerful decoder $D(x,Z)$, but no further access to $a$. Under uniform table and address inputs, its advantage in predicting ordinary Andreev is at most

$$
\varepsilon\le\frac12\sqrt{\frac{\min\{L,N\}}{N}}.\tag{5.1}
$$

Thus $L\ge4\varepsilon^2N$ is necessary. For exact correctness on every table and address, $b(a)$ must be determined by $Z$, and in particular $L\ge N$.

*Proof.* Conditional on $Z=z$, let $p_{z,c}=\Pr[b=c\mid Z=z]$. For uniform independent table signs $\xi_c$, the best decoder's conditional advantage is

$$
\frac12\mathbb E_x\left|\sum_c p_{z,c}\xi_c\right|
\le\frac12\sqrt{\sum_c p_{z,c}^2}.
$$

Writing $r_{zc}=\Pr[Z=z,b=c]$, we have $r_{zc}\le1/N$. Therefore

$$
\sum_z\Pr[Z=z]\sum_c p_{z,c}^2
=\sum_{z:\Pr[Z=z]>0}\frac{\sum_c r_{zc}^2}{\Pr[Z=z]}
\le L/N.
$$

Jensen gives (5.1); the trivial bound is $1/2$. If two addresses in one feature fiber have different parity addresses $c,c'$, choose a table with $x_c\ne x_{c'}$. The decoder cannot be exact on both. $\square$

Balanced buckets of parity addresses attain $\Theta(\sqrt{L/N})$ advantage by taking the majority of their table bits. The inherited subcube-majority upper construction already implements this scaling with $L=\Theta(\varepsilon^2N)$ relevant characters. An extractor's almost-uniform output does not mean it identifies the correct bucket or computes the bucket majority.

The hypothesis that **all address access passes through $Z$** is essential: this is an obstruction to a particular compression route, not a lower bound on unrestricted circuits with mixed table/address gates and raw top inputs. If a feature is independent of $b$, even perfectly uniform output only permits the table-majority advantage $\Theta(N^{-1/2})$. Independence is stronger than merely having uniform marginals.

### 5.2 Table compression and the role of real coefficients

By Lemma 4.1, a table-only $r$-bit summary used with an independent full address needs

$$
r\ge N(1-h_2(\delta))=\Omega(\varepsilon^2N).
$$

Exact lookup needs $r\ge N$. This is a constraint on finite summaries. It does not limit the information encodable in arbitrary real weights or a real-valued affine feature; nor does it say that $r$ Boolean features suffice to implement the decoder in one threshold layer. A lossless condenser preserves source entropy statistically; it is not an encoding of arbitrary tables supporting all exact coordinate queries with fewer than $N$ bits.

### 5.3 Layer, seed, and correctness accounting

The admissible form of a circuit is

$$
\mathbf1\!\left[\lambda\cdot(x,a)+\sum_{j=1}^S\alpha_j
\mathbf1[w_j\cdot(x,a)\ge\theta_j]\ge\Theta\right].\tag{5.2}
$$

Every proposed construction must produce this form directly. A polynomial-time extractor, an $\mathrm{NC}^1$ extractor, or even a constant-depth $\mathrm{AC}^0$ extractor is not automatically a depth-one threshold feature. Computing extractor outputs, then feeding them into a depth-two lookup circuit, generally adds layers. Even if extractor bits were individual threshold gates, substituting them into the lookup's bottom thresholds creates three layers. Only an explicit identity that flattens the **composed score** avoids this problem. The inherited parity/staircase identity is such an identity, rather than an appeal to closure under composition.

For a fixed seed, an extractor linear over $\mathbb F_2$ outputs **parities**, not real affine forms. Substituting one XOR into a threshold gate can already yield XOR, which is not a threshold function. Thus “linear extractor” does not license free substitution into (5.2). Even when a parity has an $O(M)$-gate staircase representation, a further threshold applied to an arbitrary combination of these parities need not flatten through the eventual top gate.

A seed of $d$ bits means $2^d$ evaluations if all seeds are enumerated. At $d=C\log_2(M/\eta)$ this is $(M/\eta)^C$, with a theorem-dependent constant $C$; $O(\log M)$ seed length is not negligible when seeking a fixed improvement in the gate exponent. Even summing the resulting **Boolean circuit outputs** adds a threshold layer. Merging real scores at a common top is possible only with a sign/margin argument proving that this merged score solves the target.

A strong seeded extractor guarantees statistical closeness averaged over an **independent uniform seed**. It does not give one seed that works for every source, one seed that computes $x_b$ on every input, or a bound on the gate count of that seed's lookup. For any fixed seed $s$ and one-bit map $E_s$, a largest fiber has size at least $2^{M-1}$ and makes $E_s$ constant; this refutes universal fixed-seed extraction for all sources at entropy $M-1$. Nonuniform averaging may legitimately choose a seed/mask for one prescribed input distribution. The inherited average-case circuit already does this, without evaluating the mask generator inside the circuit.

### 5.4 A pointwise randomization route and its precise missing lemma

For a fixed address input, a uniform XOR mask makes each masked address count binomial; this is genuine pointwise randomization of the address part. It does **not** make arbitrary table Walsh coefficients small. For the character table $\xi_c=\chi_T(c)$, one has $X_T=N$ and $X_S=0$ for $S\ne T$. This refutes replacing the uniform-table tail estimate by an all-tables tail estimate for the same truncated arguments.

**Conditional construction target, not a theorem of existence.** Suppose there were $K$-bottom raw-input scores $P_s(x,a)$ with an exactly sign-correct common expectation and a uniform, normalized margin/concentration bound guaranteeing that the sum of $O(n)$ independent scores has the correct sign at every one of the $2^n$ inputs with positive probability. Then fixing those scores nonuniformly and combining their bottom gates at one top would give $O(nK)$ exact size. To obtain $n^{2-\gamma}$ by this generic all-input union bound needs $K=O(n^{1-\gamma})$. Taking existing $K=\widetilde O(n^{3/2})$ distributional approximators neither supplies the pointwise hypothesis nor yields the desired size. A Boolean majority of whole approximating circuits is instead depth three. The unresolved alternative is a much cheaper, shareable correction for exceptional table/address inputs.

## 6. Verified extractor results and explicit parameter instantiations

Here $M$ is an extractor's source length, $h$ its min-entropy, $\ell$ its output length, $d$ its seed length, and $\eta$ its statistical error. These letters are deliberately distinct from the Andreev address length $k=\log_2N$, block length $m$, and circuit advantage $\varepsilon$. All statements below were checked in primary-source theorem text, except the explicitly marked announcement. Their full construction proofs are not independently certified here.

### 6.1 Strong seeded extraction and low-depth implementation

**Doron–Ribeiro, Theorem 1.** [arXiv:2411.07473v2](https://arxiv.org/pdf/2411.07473v2), initially 12 November 2024, revised 9 February 2026: for fixed $\gamma>0$ and $h\ge C\log(M/\eta)$, a strong extractor has $d\le C\log(M/\eta)$ and $\ell\ge(1-\gamma)h$. The near-linear runtime has preprocessing qualifications: no preprocessing in the stated regime $h\ge2^{C\log^*M}\log^2(M/\eta)$ and $\eta\ge2^{-CM^{0.1}}$; other regimes require primes and sometimes primitive elements. This is a runtime theorem, not a two-layer threshold construction.

**Instantiation.** At $h=M^\alpha$ and $\eta=M^{-b}$ for fixed $\alpha,b>0$, the favorable asymptotic regime applies, but seed enumeration is still $M^{C(1+b)}$. At $h=k\sim\log M$, the required constant $C$ is not automatically satisfied; even a suitable constant-factor increase in live bits would only provide randomness, not new table labels.

**Cheng–Wu, Theorems 1.1–1.3.** [ECCC TR24-040, revision 2, 11 May 2026](https://eccc.weizmann.ac.il/report/2024/040/revision/2/download/): strong extractors in logspace-uniform $\mathrm{AC}^0$ for $h\ge M/\log^aM$, $\eta\ge2^{-\log^cM}$, fixed $a,c$, with $d=O(\log(M/\eta))$ and $\ell\ge(1-\gamma)h$; an $\mathrm{NC}^1$ construction for $h\ge\Omega(\log(M/\eta))$, $\eta\ge2^{-h^\alpha}$, fixed $\alpha,\gamma\in(0,1)$, with the same seed/output order. Their negative theorem concerns $\mathrm{AC}^0$ strong dispersers, not $\mathrm{THR}\circ\mathrm{THR}$.

**Instantiation and scope.** The address source with $h=k=\Theta(\log M)$ is far below the $\mathrm{AC}^0$ construction's entropy regime. A nearly full-entropy table source does meet it. Neither result flattens extractor-plus-lookup to (5.2). No inference from an $\mathrm{AC}^0$ lower bound to an arbitrary-weight threshold lower bound is valid.

**Cheng–Wu, Theorems 1.7–1.8.** [arXiv:2610.37122v2](https://arxiv.org/pdf/2610.37122v2), first submitted 27 October 2026, revised 6 November: a strong quantum-proof extractor for entropy $M-a$ has

$$
d\le(1+\alpha)\log a+(2+\alpha)\log(1/\eta)+O_\alpha(1),\quad
\ell\ge M-O_\alpha(a+\log(1/\eta)),
$$

for fixed $\alpha>0$ (take $a\ge1$ here). A separate theorem handles every constant entropy rate with $d=O(\log(M/\eta))$, $\ell=\Omega(M)$, down to $\eta=2^{-cM}$ for a rate-dependent constant. Computation is polynomial time. The v2 date matters; some indexed abstracts retain an outdated sampler comparison.

**Concrete test.** With table length $M=N$, deficiency $a=N^{1/2}$, error $\eta=N^{-1/10}$, and $\alpha=1/10$, the seed bound is $0.76\log_2N+O(1)$, and output length is $N-O(\sqrt N)$. Thus excellent seeded extraction can fit into the available address-bit budget on a *suitable independent-seed experiment*. Yet its output is not $X_J$: (4.3) and Proposition 4.3 show why the prescribed coordinate function has a worse error guarantee. Replacing it makes a new function. Also, at $S=n^{3/2+\gamma}$ the bound $B=O(Sk/\sqrt N)$ already exceeds the table length up to logs, so the restriction transcript provides no positive high-entropy guarantee in that regime.

### 6.2 Oblivious bit-fixing extraction and linear condensers

**Doron–Fridman, Theorem 1.3 / conference Theorem 3.** [ECCC TR25-012](https://eccc.weizmann.ac.il/report/2025/012/download/), submitted 17 February 2025; [RANDOM 2025](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.APPROX/RANDOM.2025.33), published 15 September 2025. There are constants $c>1$, $\beta\in(0,1)$ giving explicit seedless OBF extraction for

$$
h\ge\log M(\log\log M)^c,\quad
\ell=(1-o(1))h,\quad
\eta=2^{-(h/\log M)^\beta}.\tag{6.1}
$$

Their source is exactly uniform on a coordinate subcube. They also discuss low-weight affine extensions and linear condensing; neither is a threshold-circuit flattening theorem.

**Parameter consequences.** The one-per-block source has $h=k\sim\log M$ and fails (6.1). At $h=\log M(\log\log M)^c$, the guaranteed error is only $2^{-(\log\log M)^{c\beta}}$, not inverse-polynomial in $M$. To ensure $\eta\le M^{-b}$ from this formula requires

$$
h\ge (b\log_2 M)^{1/\beta}\log_2 M,
$$

as well as its entropy threshold. For $h=M^\alpha$, it gives $\eta=2^{-M^{\alpha\beta}/(\log M)^\beta}$, genuinely very small. This is useful when **defining a new extractor-based address**, but extra live variables in ordinary blocks still leave at most $N$ independent labels.

**Chen–Cheraghchi–Shagrithaya, Corollary 2 (full Corollary 30).** [Optimal Erasure Codes and Codes on Graphs, arXiv:2504.03090v1](https://arxiv.org/pdf/2504.03090v1), 3 April 2025. For fixed finite field and entropy rate $\rho$, slack $\tau>0$, sufficiently large $M$, there are strong seeded symbol-fixing extractors, linear for each seed, with $\ell=(\rho-\tau)M$ symbols and $d=O(\log(1/(\eta\tau)))$; companion lossless condensers output $(\rho+\tau)M$ symbols for entropy at most $\rho M$.

**Why this does not supply a constant-seed shortcut here.** The constant-seed interpretation holds for fixed slack and error. For $h\sim\log M$, positive output would require $\tau<\rho=h/M$, outside a fixed-rate/slack reading and making $\log(1/\tau)=\Theta(\log M)$. No uniform low-rate instantiation is asserted here without its large-$M$ conditions. Over $\mathbb F_2$, the outputs are parities. Their exact distributional correctness on good seeds does not make them LTFs or implement ordinary lookup.

### 6.3 Affine, two-source, and non-malleable extraction

**Xin Li, Theorems 1.6–1.7.** [arXiv:2303.06802v2](https://arxiv.org/pdf/2303.06802v2), initial 13 March 2023, revised 30 May 2023: for every **fixed** error $\eta>0$, there is $C_\eta>1$ and an explicit one-bit extractor for two independent $M$-bit sources each of entropy $C_\eta\log M$, including unknown interleavings; another one-bit extractor works for affine sources or sums of two independent such sources. Theorems with fixed error do not authorize setting $\eta=M^{-b}$ while keeping $C_\eta$ constant. No low threshold depth is claimed.

**Li–Zhong, Theorems 1.1–1.4.** [arXiv:2404.17013v1](https://arxiv.org/pdf/2404.17013v1), submitted 25 April 2024; cover dated 29 April. For $h\ge\log^C M$, two-source non-malleable extraction gives $\ell=\Omega(h)$, and affine non-malleable extraction gives $\ell=h^{\Omega(1)}$, both with error $M^{-\Omega(1)}$. At $h\ge c\log M$, the stated versions output one bit with constant error. Two-source inputs must be independent; affine tamperings must satisfy the specified no-fixed-point condition. A generic inverse-polynomial error is not automatically below every target $M^{-b}$.

**Li–Zhong, Theorems 1.2–1.3 and 3.15.** [arXiv:2610.02407](https://arxiv.org/pdf/2610.02407), publicly submitted 1 October 2026, manuscript cover 21 September. For fixed positive entropy rate and a fixed number of fixed-point-free affine tamperings, they obtain linear output and $2^{-\Omega(M)}$ error. For fixed $0<\zeta<1$ and tampering count $t$, the sublinear theorem requires $h\ge C_{\zeta,t}M/\log M$, outputs at least $\lfloor M^{1-\zeta}\rfloor$ bits, and has error $2^{-M^{1-\zeta}}$. Their lower-bound applications concern linear branching programs, low-degree/local decision trees, and proof complexity, not unrestricted depth-two threshold computation of ordinary Andreev.

**Source match.** The new sublinear threshold is enormously larger than $k=\Theta(\log M)$ in the standard restriction. At $h=M/\log M$ a suitable constant factor does meet it, but retaining that many raw bits does not increase parity-address rank beyond $k$. Non-malleability protects specified affine transformations, not arbitrary threshold-output leakage. Independent raw blocks exist *before* circuit conditioning; after conditioning their independence requires a proof. Applying two-source extraction to two disjoint uniform groups before conditioning is possible but unnecessary—the parities are already independent and uniform—and changes the address if substituted for them.

### 6.4 Quadratic and computationally specified sources

**Chandrasekaran–Goodman–Zuckerman, Theorem 1.3 / Theorem 9.4.** [Quadratic Extractors, arXiv:2611.07266v1](https://arxiv.org/pdf/2611.07266v1), 5 November 2026, also [ECCC TR26-303](https://eccc.weizmann.ac.il/report/2026/303/): an explicit extractor for $X=p(U)$, a quadratic **image** over $\mathbb F_2$, at $h\ge\log^C M$, with output $h^{\Omega(1)}$ and error $M^{-\Omega(1)}$. Corollary 1.4 includes 2-local samplers; Corollary 1.5 handles $\mathrm{AC}^0$-samplable sources at entropy $M^{1/3+\alpha}$, fixed $\alpha>0$.

**Mismatch.** A source uniform on the solutions of quadratic equations is a **variety source**, not automatically a quadratic image. A threshold-defined cell is neither automatically such an image nor an $\mathrm{AC}^0$-samplable source. Computing a membership predicate and efficiently sampling its preimage are different tasks. This recent theorem cannot be applied to the residual table cells on the basis of entropy alone.

**Fu Li–Zuckerman, Theorems 7–8.** [RANDOM 2019](https://drops.dagstuhl.de/storage/00lipics/lipics-vol145-approx-random2019/LIPIcs.APPROX-RANDOM.2019.72/LIPIcs.APPROX-RANDOM.2019.72.pdf): explicit seedless extraction from a **single halfspace** source at entropy $(1-c_1)M$, with linear output and exponentially small error. A separate reduction converts an appropriate seed-extending PRG with error $\nu$ into a recognizable-source extractor of error $2^a\nu$ at entropy deficiency $a$. The factor $2^a$ cannot be omitted.

**Match and limit.** A single conditioned bottom-gate output matches the halfspace model, but a transcript or intersection of several halfspaces does not automatically do so. Even for one halfspace the theorem's extractor is a different Boolean map from Index. Proposition 4.3 shows concretely why Index cannot inherit its exponentially small error. A PRG-based route must fool the relevant recognizers to error at most $\eta2^{-a}$, not just $\eta$.

**Ball–Chattopadhyay–Gurumukhani–Shaltiel–Zhao, Theorems 1–3.** [arXiv:2611.07829v1](https://arxiv.org/pdf/2611.07829v1), 5 November 2026: under exponential hardness of $\mathsf E$ for nondeterministic circuits, one-bit constant-error extraction for $h=O(\log M)$, and nearly all entropy with inverse-polynomial error for $h=M^\alpha$; under the corresponding $\Sigma_2$-circuit hardness assumption, nearly all entropy for $h=\log^aM$ and inverse-polynomial error. The full versions allow specified postselection models. These are **conditional**, not unconditional extractor or threshold lower-bound theorems. Their source-size and runtime exponents depend on the fixed parameters.

Any lower bound using those hardness assumptions would remain conditional; treating it as unconditional would be invalid. Even a conditional application would need to show the actual cell lies in the stated sampling/postselection model and would produce pseudorandom bits of the extractor, not the selected ordinary table coordinate.

### 6.5 Important announcement and search limitations

A [UC Davis seminar announcement dated 5 November 2026](https://www.math.ucdavis.edu/research/seminars?talk_id=7770) reports forthcoming work of Dean Doron and Jesse Goodman on low-error two-source extraction at entropy $o(M)$, using rapid mixing and approximate duality. A September 2026 Simons workshop schedule also lists the talk. Searches of the authors' available pages, ECCC, and arXiv did not locate a full theorem with quantitative entropy/error/output parameters. **Announcement only:** it is not used as a verified theorem. Thus this report does not claim that previously published low-error two-source entropy thresholds are still the absolute latest announced frontier.

The superficially similar [Ben-Aroya–Doron–Ta-Shma 2016 low-error paper](https://eccc.weizmann.ac.il/report/2016/106/) was explicitly retracted on 21 July 2016. It cannot be used to fill this gap.

## 7. The one-table-bit route: an elementary bound superseded by slicing

The initial read-only snapshot of `research_backup/experiments/one_table_bit/report.md` established the model and selector-dominance equivalence while its later sections were unfinished. Proposition 7.1 below was derived from that snapshot. No literature-priority or independent-review claim is made for this derivation.

**Archive synchronization, 2026-11-09.** Before archiving this report, the repository had advanced to `c2944fb`. The completed [coherence referee report, Section 8](https://github.com/chris-ai1/andreev-research/blob/c2944fb/experiments/review_coherence/report.md) and [one-table-bit report](https://github.com/chris-ai1/andreev-research/blob/c2944fb/experiments/one_table_bit/report.md) establish the stronger restricted baseline

$$
S\ge\frac N4\operatorname{slice}(m)
=\Omega\!\left(\frac{Nm^{13/19}}{\log^{32/19}m}\right)
=\Omega\!\left(\frac{n^{32/19}}{\log^{45/19}n}\right)
$$

at balance, using Sauermann–Xu's [hypercube edge-slicing theorem](https://arxiv.org/abs/2510.16592). Comparing the top scores on two single-one tables whose labels differ in one address bit makes gates reading neither table bit and direct raw-address terms cancel. The remaining score sign-represents parity on that block; summing the slicing requirement over disjoint table-label pairs gives the reduction. Proposition 7.1 is retained as a simpler, weaker proof, **not the current restricted frontier**.

The completed one-table-bit report also supplies a restricted exact upper bound $O(n^{1+\log_2 3})$, and $S\ge Nm/(16C)$ when each address normal can separately be rescaled to integer entries in $[-C,C]$. For fixed $C$, the latter is $\Omega(n^2/\log n)$, using Sauermann–Xu's [bounded-normal slicing corollary](https://arxiv.org/html/2507.00773v2). These are inherited archive results, not extractor results from this investigation. The additional one-table-bit constructions and coefficient bounds retain their source report's pending independent-review status. None is an unrestricted ordinary-Andreev exponent improvement.

A gate in this subclass has the form $[L_j(a)+\beta_jx_{c_j}\ge\theta_j]$. For fixed address $a$, the top score is

$$
F(x,a)=C(a)+\sum_c w_c(a)x_c.
$$

Comparing the largest score with $x_b=0$ to the smallest score with $x_b=1$ shows that exact ordinary-Andreev correctness forces

$$
w_{b(a)}(a)>\sum_{c\ne b(a)}|w_c(a)|.\tag{7.1}
$$

There is also an intercept condition; dominance alone is not sufficient for an arbitrary fixed $C(a)$. In the odd-in-table score obtained by subtracting $F(\mathbf1-x,a)$ from $F(x,a)$, dominance is sufficient. Symmetrization at most doubles bottom count. The original one-table-bit report proves these points with ties handled explicitly.

**Proposition 7.1 (proved here; valid but superseded by the stronger bound above).** Every exact one-table-bit circuit for $A_{k,m}$ has

$$
S\ge c\frac{(N-1)m}{\sqrt{km}}
=\Omega\!\left(\frac{n^{3/2}}{\log n}\right)\quad\text{at balance},\tag{7.2}
$$

for an absolute $c>0$. Address-only bottoms and direct raw top inputs are allowed.

*Proof.* Restrict only the raw addresses to one live variable in every block, keeping **all** table variables unfixed. For each table-reading gate define two address halfspaces

$$
h_{j,0}(a)=[L_j(a)\ge\theta_j],\qquad
h_{j,1}(a)=[L_j(a)+\beta_j\ge\theta_j].
$$

Call the gate active if either halfspace remains nonconstant on the live cube. The probability is at most twice the standard one-per-block survival bound, hence at most $C\sqrt{km}/m$. If no active gate reads $x_c$, then its coefficient $w_c$ is constant over the entire live cube; raw top table weights are also constant. There cannot be two distinct coordinates $c,d$ whose coefficients are both constant: the live cube contains an address for every table position, so (7.1) at addresses $c$ and $d$ would give simultaneously

$$
w_c>|w_d|\quad\text{and}\quad w_d>|w_c|,
$$

an impossibility. Thus at least $N-1$ different table coordinates have an active gate, and at least $N-1$ gates are active on **every** such restriction. Taking expectations gives $(N-1)\le CS\sqrt{km}/m$. $\square$

This proof uses the table-local structure to replace truth-table counting by a direct requirement of $N-1$ active table groups. It does not apply to gates reading several table bits, and it proves no average-case counterpart: exact correctness on all tables was used in (7.1). It remains a useful elementary structural argument, but improves neither the completed restricted baseline nor the unrestricted exponent.

**Why extractor/sampler kernels have not supplied an upper bound.** In the address-halfspace dictionary from the archived `upper_astra/report.md`, write

$$
K_c(a)=d_c+\sum_{j=1}^H\beta_{cj}h_j(a).
$$

The pointwise requirement is

$$
K_{b(a)}(a)>\sum_{c\ne b(a)}|K_c(a)|\quad\text{for every }a.\tag{7.3}
$$

The circuit cost is at most $H+\operatorname{nnz}(\beta)$ after forming $\xi_ch_j=2x_ch_j-h_j$ with $\xi_c=2x_c-1$; $x_ch_j$ is one raw-input LTF by adding a sufficiently large coefficient on $x_c$. Terms $d_c\xi_c$ go directly to the top. This construction is genuinely two layers. An extractor or disperser gives a distributional guarantee over each permitted source, not (7.3). Signed coefficients can cancel, and their magnitudes are unrestricted, so correlation bounds on individual halfspaces alone do not control the final margin. A sampler also needs to approximate all relevant signed scores with their normalization/margins accounted for; estimating a global table average cannot identify an arbitrary requested table entry.

An explicit dictionary satisfying (7.3) with $H+\operatorname{nnz}(\beta)=O(n^{2-\gamma})$ would be a valid exact improvement in this subclass. None of the verified extractor theorems supplies it.

**A different “one table bit” operation must not be confused with this model.** Fixing all table entries except $x_c$ to zero leaves $x_c\land[b(a)=c]$. This function has an exact $O(km)$-bottom circuit: express every block-parity equality as an affine sum of the $m$ thresholds $[\sum_j a_{ij}\ge r]$, and threshold the sum of these $k$ Boolean equality values plus the raw bit $x_c$ at $k+1$. On this slice the constant-zero function already has error $1/(2N)$ under uniform remaining inputs. Hence an isolated one-coordinate slice cannot prove a superlinear exact lower bound or a constant-advantage uniform average-case lower bound. Multiplying its complexity by $N$ would require a direct-sum theorem, not merely an extractor.

## 8. Ordinary versus modified Andreev, and conditional lower-bound targets

### 8.1 What the classical and modern lower bounds actually concern

Kane–Williams [Theorems 1.1–1.3](https://arxiv.org/pdf/1511.07860) give the classical ordinary-Andreev gate/wire lower scales $\varepsilon^3n^{3/2}/\log^3n$ and $\varepsilon^3n^{5/2}/\log^{7/2}n$, an $O(n^3/\log n)$ exact depth-two upper bound, and a depth-three lower bound for a **different code-based function** $B_n$. Their restriction lemmas are the starting point here; the local errata repair rank/tie/zero-weight details and narrow the proof's small-advantage range. The inherited project improvements in Section 1 are stronger than those original numerical statements.

Chen–Santhanam–Srinivasan [Section 2.4, Theorems 2.17–2.18, Lemma 2.19, and Corollary 4.3](https://arxiv.org/pdf/1806.06290) use

$$
F(z,y)=\operatorname{Enc}(z)_{E(y)},
$$

where $|z|=4r$, $|y|=r$, $E$ is an OBF extractor with surviving entropy $r^\gamma$, output $0.9r^\gamma$, and error $2^{-r^{\Omega(\gamma)}}$. The codeword has length $2^{0.9r^\gamma}$ and is locally evaluable. Their exponentially small correlation conclusion for slightly superlinear-wire bounded-depth circuits concerns this generalized function, not the independent raw-table function in this report. Improving its extractor can modify that construction's parameters; it does not automatically improve ordinary Andreev.

The public 2026 theorem of Chen–Tal–Wang [Theorem 1.1, ECCC TR26-039](https://eccc.weizmann.ac.il/report/2026/039/download) gives $n^{2.5-\gamma}$ gates for a function in $\mathsf E^{\mathsf{NP}}$, for each fixed $\gamma>0$. It is neither an ordinary-Andreev bound nor compatible with transferring that gate exponent to an explicit function already having a quadratic construction. The [Nag TR26-167 revision](https://eccc.weizmann.ac.il/report/2026/167/) similarly concerns a language in $\mathsf E^{\mathsf{NP}}$; its later comment announces a further extension. Neither claim is used as a proved ordinary-Andreev bound here. A 2026 spiky-rank search hit concerns ReLU circuits, not a new theorem for this target.

### 8.2 The missing reductions

An arbitrary code or extractor is not a free restriction. Coordinate substitutions, constants, and complements preserve each raw-input LTF. A substitution $x_c=y_1\oplus y_2$ does not: even a gate that simply outputs $x_c$ becomes XOR, which is not an LTF. General binary-linear codes use precisely such parity substitutions. Adding circuits for code symbols or extractor outputs changes depth and size; a separate flattening proof would be required.

One can view the generalized codeword as an ordinary table only by supplying all its entries. For the CSS parameters, that is $2^{\Theta(r^\gamma)}$ raw table bits rather than $\Theta(r)$ input bits. Rewriting a lower bound in the former input length destroys its original exponent. Similar parameter accounting is required for KW's polynomial-length code variant. A lower bound on a specially encoded lookup does not transfer just because both formulas contain a table subscript.

### 8.3 A precise generic extractor-assisted restriction implication

**Conditional template (proved implication, hypotheses not established for an improved ordinary restriction).** Suppose restrictions on $M$ raw addresses:

1. reconstruct uniform original inputs when live inputs are filled uniformly;
2. leave $t$ live bits and an address map $E_R:\{0,1\}^t\to[L]$ with distribution within $\eta$ of uniform;
3. have an independent uniform $L$-bit table;
4. leave a mean $B\le Sp$ bottom survivors, and a table-independent class of at most $K_q$ restricted predictors for $q$ survivors.

For a fixed predictor $h$, average its sign within each address fiber to obtain coefficients $\mu_c\in[-1,1]$. With fiber masses $p_c$, its correlation with the random table is $\sum_c p_c\mu_c\xi_c$. Replace $p_c$ by $1/L$: this changes correlation by at most $2\eta$. Hoeffding on the independent $\xi_c$ and a union bound over predictors now apply. Choosing a survivor-dependent deviation and averaging its square root gives a bound of the form

$$
\varepsilon\le \eta+	au+
O\!\left(\sqrt{\frac{B\Lambda+\Lambda_0+\log(1/\tau)}{L}}\right),\tag{8.1}
$$

provided $\log K_q\le q\Lambda+\Lambda_0$ and the union over $q$ is included in $\Lambda,\Lambda_0$. In particular, usefulness at advantage $\varepsilon$ needs $\eta+\tau<\varepsilon$ by a fixed margin; “small error” without this comparison is insufficient. A single union over $K$ sources/branches can also cost $K\eta$ when the guarantee is per-branch failure rather than uniform statistical error; the quantifiers must be specified.

For fixed directions and fixed top coefficients on a $t$-bit live domain,

$$
K_q\le\binom Sq(2^t+1)^{q+1},
$$

so one can take $\Lambda=O(t+\log(S+1))$ and $\Lambda_0=O(t+\log(S+1))$. The count depends on the **live domain** $2^t$, not only on the extractor output length. With $L=N$, $t=k$, $\eta=0$, $p=O(k/\sqrt N)$ this reproduces the known exponent. Enlarging $t$ to meet a generic extractor threshold gives no larger $L$ for the ordinary parity address and worsens this count. Under a restriction estimate $p=O(t/\sqrt M)$ it gives only the scale

$$
S\gtrsim\frac{(\varepsilon-\eta-\tau)^2N\sqrt M}
{t\,(t+\log S)}
$$

when additive terms are dominated. The formula is a parameter audit, not a new restriction theorem.

A fixed-power improvement from the same approach would require, for example, a source-preserving simplification with $p\le n^{-1/2-\gamma}\operatorname{polylog}n$ and $t=O(\operatorname{polylog}n)$, or a fundamentally stronger constraint on the **joint family of residual functions across restrictions**. The first uniform survival improvement is false for the usual restriction: at balance, a majority on the raw addresses survives when the fixed sum lies in a central interval of width $k$, with probability $\Theta(k/\sqrt M)$. This gives a concrete obstruction, not merely absence of a suitable extractor theorem.

The coherent lower bound uses a different restriction measure and a single-crossing property. Count-space cubes are not uniformly distributed raw addresses; that exact theorem cannot be promoted to a uniform average-case statement by invoking an extractor without controlling the induced measure. Mixed signs invalidate the coherent crossing count. No extractor theorem checked here repairs either issue.

## 9. Conclusions at the exponent level

**No new fixed-power improvement for unrestricted ordinary Andreev was obtained.** The verified extractor theorems do not currently close the exact $3/2$ versus $2$ gate-exponent gap. The substantive deductions here are the source-rank calculation, the information/extraction formulation with a tight square-root leakage obstruction, the address-compression bound, and the elementary one-table-bit active-group argument, whose numerical lower bound is superseded by the completed slicing result. They are hand proofs, not Lean formalizations or independent referee certifications.

For balanced inputs, the resulting status is:

| Task and model | Lower bound | Upper bound | Interpretation |
|---|---|---|---|
| Exact, unrestricted | $\Omega(n^{3/2}/\log^2 n)$ | $5n^2/16+o(n^2)$ | Inherited gap remains. |
| Fixed uniform error $0<\delta<1/2$, unrestricted | $\Omega(n^{3/2}/\log^2 n)$ | $O(n^{3/2})$ | Gate exponent already matches. |
| Advantage $C\log n/\sqrt n\le\varepsilon\le1/8$, unrestricted | $\Omega(\varepsilon^2n^{3/2}/\log^2n)$ | $O(\varepsilon^2n^{3/2}\sqrt{\log(1/\varepsilon)})$ | Matching powers of $n$ and $\varepsilon$ up to logs; inherited. |
| Error $\delta=2^{-\Theta(n^\beta)}$, fixed $0<\beta<1$ | $\Omega(n^{3/2}/\log^2 n)$ | $O(n^{(3+\beta)/2})$ | No matching dependence on very small error proved. |
| Exact, one-table-bit bottoms | $\Omega(n^{32/19}/\log^{45/19}n)$ | $O(n^{1+\log_2 3})$ | Inherited completed archive results; supersede Proposition 7.1. Upper construction awaits independent review. |
| Exact, sign-coherent bottoms | $\Omega(n^2/\log^3n)$ | $O(n^2)$ | Restricted exact exponent already matches. |

For support wires the inherited uniform-average-case tradeoff remains $\widetilde\Theta(\varepsilon^2n^{5/2})$ in the documented common range. Proposition 7.1 is a gate argument, not a better unrestricted wire theorem. The stronger inherited one-table-bit bounds and their coefficient-restricted refinement also do not apply to dense table-dependent bottoms.

For $\varepsilon=n^{-\alpha}$ with fixed $0<\alpha<1/2$, the matched unrestricted gate exponent is $3/2-2\alpha$; logarithmic factors and the endpoint must not be suppressed when $\alpha$ approaches $1/2$ with $n$. The raw top table-majority gate already supplies advantage $\Theta(N^{-1/2})$ with no bottoms. For exactness, error strictly below $2^{-n}$ under the uniform distribution forces zero errors; inserting that accuracy into the available upper construction restores quadratic size.

### Concrete remaining targets, rather than a generic call for better extractors

1. **Exact upper bound:** give a sparse halfspace/slab selector family satisfying (7.3), or a different raw-LTF score identity that shares the exceptional-tail corrections across characters. Charge all feature-table products. Generic extraction of address randomness is not the missing property.
2. **Exact lower bound above $3/2$:** use coupling across many restrictions, table-dependent threshold-shift geometry, or another structural resource that survives after the per-restriction label entropy has been exhausted. A uniformly better single-gate survival probability for the existing restriction is impossible.
3. **Average case:** the constant-advantage exponent and polynomially small-advantage powers are already matched. A substantive remaining improvement would be a nontrivial lower-bound interpolation for exponentially small error, or a corresponding improved upper construction. Ordinary fixed-error extraction does not address this.
4. **Conditional new-function work:** modern low-error OBF/affine extractors can be inserted when one is allowed to redefine a generalized Andreev function. Any resulting result must name the new function, normalize its actual input size, and prove its own circuit-depth/size or restriction theorem. It is not an ordinary-Andreev result.

## 10. Verification, evidence, and limits

[verify_claims.py](verify_claims.py) is a standard-library-only collection of finite guardrail computations. [verification.json](verification.json) records:

- 136 coordinate-restriction cases verifying the exact rank and fiber-size formulas;
- all 255 nonempty flat sources on three table bits verifying the Index entropy-deficiency inequality numerically;
- all 625 realizable parity-fiber count patterns for a binary address feature at $k=m=2$, with exact rational Bayes-advantage evaluation over all 16 tables;
- all 256 binary transcripts on the eight three-bit tables verifying the entropy/prediction inequality numerically;
- 1,184 exhaustive table-slice/input cases verifying the explicit one-coordinate $km$-gate staircase score.

All checks passed. In the compressed-address experiment, the largest observed advantage is exactly $5/16$; this is a finite computation, not an asymptotic optimum claim. Entropy checks use floating-point logarithms with a $10^{-12}$ tolerance; the address-feature and staircase checks use exact arithmetic. The universal results rest on their displayed proofs, not these experiments.

Primary-source searches covered arXiv, ECCC's 2026 listings and author pages, author-hosted papers, and primary conference full texts. Searches specifically included 2025–2026 seeded, affine, OBF, two-source, low-error, low-depth, quadratic, and recognizable-source extraction, plus Andreev/threshold follow-ups. The report distinguishes submission, revision, cover, and conference-publication dates. A search engine's “published” age or a bibliography aggregator's later ingestion date was not used as a theorem date. The November two-source announcement is explicitly unresolved at the theorem level.

The linked source corpus includes the full KW paper and theorem statements of the extractor papers. I checked hypotheses, parameter substitution, and whether the source model matches; I did not independently reprove every external extractor construction. Access failures for some trailing-slash ECCC PDF URLs were resolved through their direct download links or the arXiv/conference version where available. Source PDFs retain their original authorship; the new report, verification script/results, and evidence records credit Christian Reitwiessner.

The final archive synchronization preserves the initial source hashes in [evidence.json](evidence.json) and separately records the completed one-table-bit and coherence-review snapshots from repository commit `c2944fb`. Their stronger bounds are attributed to those reports and their cited geometric theorems; this synchronization is not a new independent review of them.

The companion [bounds.html](bounds.html) displays only the exponent comparison. Its inline rendering succeeded; automated screenshot preview was unavailable because the host lacks browser shared libraries. This does not affect the mathematical checks.
