Authors: Christian Reitwiessner

# Generic exact wire upper bounds for ordinary Andreev

Status: completed research handoff, 2026-11-11. No generic $o(n^3)$ exact wire upper was established. The new results are complete paid flattenings, exact cost obstructions for specified upper architectures, and a sparse noncharacter decoder with an explicit unresolved compiler target. The earlier wires_astra report is preserved. All five groups of exact checks passed.

## Objective and conventions

For $N=2^k$, $M=km=\Theta(N)$ and $n=N+M$, compute ordinary Andreev $A(x,a)=x_{b(a)}$ exactly on every independent table $x\in\{0,1\}^N$ and raw address $a\in\{0,1\}^{km}$, where $b_i(a)=\sum_l a_{il}\pmod2$. Seek $O(n^{3-\delta})$ or a meaningful $o(n^3)$ generic exact support-wire upper bound.

A raw depth-two circuit has score $\beta+u\cdot(x,a)+\sum_jv_j[w_j\cdot(x,a)\ge\theta_j]$. Count all aggregated nonzero input-to-bottom, bottom-to-top, and raw-to-top edges. Coefficient magnitude is free; intermediate nonlinear or aggregate features are not free inputs. Approximation is not exact computation.

## Initial constraints

[VERIFIED inherited] Exact generic $O(n^3)$ wires follow from the quadratic gate construction. Fixed-error exponent 2.5 is already matched and is not this objective. The parent completed the sharper construction's leading wire recount, giving $9n^3/64+o(n^3)$; that recount is secondary here and is credited to the parent.

[PROVED inherited architectural restriction, hand proof] The previous report's semantic pruning/profile argument gives wire exponent three up to polylogarithms when address magnitudes are bounded integers and constant within each original block. This does not exclude logarithmic savings, but it excludes a fixed power saving within that class. Potential escape routes include heterogeneous within-block magnitudes and genuinely sparse interactions between table and address inputs.

## Research log

- Created this report before exploration, as requested.
- Completed: reconsulted all round-three barriers, derived and costed exact prefix and Haar flattenings, proved an arbitrary-real blockwise monochromatic-guard obstruction, checked a sparse affine-plane decoder, and ran exact finite checks. The parent owns the improved cubic leading coefficient.

## Increment 1: triage and a sharper architectural distinction

[VERIFIED parent artifact] The parent reports an explicit finite recount at `/tmp/andreev_gap/wire_recount/recount.py` and `checks.json`: 48 gate-count identity cases and balanced $k=1,2,4,8,16,32$. The resulting generic exact upper is $W\le(9/64+o(1))n^3$. This is the benchmark, not this investigation's asymptotic improvement.

[VERIFIED inherited barriers] Round-three UP1 rules out constant-amplitude four-ridge sign multiplication and supplies a primitive-integer-direction budget obstruction; it does not rule out arbitrary finite-grid real slopes. UP2 excludes small lexicographically separated address groups even with dense table normals and arbitrary pure-address helpers. LOW1 supplies the bounded-integer blockwise profile theorem and costed helper extension. LOW2 supplies arbitrary-real two-scale profile isolation with a mask resource, and explicitly refutes a magnitude-free replacement of integer levels by real bands. The completed reports were read in the preceding wire investigation and reconsulted here.

[PROVED inherited consequence, important for design] The sparse-semantic-character wire inequality in the earlier wire report is stronger than a blockwise warning: for integer address coefficients individually rescalable into $[-C,C]$, and at most $Q$ active complementary-character table pairs per mixed gate,
$$W_{\rm address}\ge\frac{N\bigl(m^2k(k+1)-2mk\bigr)}{64CQ}.$$
Thus **heterogeneous within-block coefficients alone are insufficient** if the construction retains bounded $C$ and sparse character activity. In particular, replacing each old carrier by odd weights on selected bits and even weights elsewhere remains blocked for fixed $C,Q$. Genuine mixing of table characters, a growing arithmetic resource, or a different architecture is needed for a power saving.

[REFUTED implementation shortcut] Writing a block-parity selector as a top threshold over $O(pm)$ block-count cuts does not make it an input to another bottom gate. Gating a sublookup by that selector would add a third nonlinear layer unless explicitly flattened. Pure-address cuts may be shared at the one output, but their outputs cannot be fed into mixed bottoms in this model.

[INITIAL CONJECTURE, resolved in §§2–3] Partitioning the table into prefix chunks reduces the support of each table aggregate. Its selector expansion can, however, replicate every suffix channel over all prefix characters. The completed raw compilation below establishes a cubic obstruction for that route. Sparse noncharacter table bases are also examined with paid carrier compilers; a mere character-wise sign certificate does not imply all-table lookup.

## 2. Exact prefix chunking: full flattening and a cubic cost obstruction

[PROVED construction; no asymptotic improvement] Split the address label into a prefix of $p$ bits and suffix of $r=k-p$ bits. Put $B=2^p$, $K=2^r$, so $BK=N$, and write table signs $y_c=1-2x_c$. For prefix $u$ and suffix character $S$ define
$$X_{u,S}=\sum_{v\in\{0,1\}^r}(-1)^{S\cdot v}y_{u,v}.$$
For a prefix character $U$, put $T=U\cup S$ and $d_T=m|T|$. Walsh inversion on the suffix and the exact prefix indicator give
$$N y_b=\sum_{u,S,U}(-1)^{U\cdot u}X_{u,S}(-1)^{t_T}.$$
Every $X_{u,S}$ has parity $K$, so with $\varphi(z)=(-1)^z z$,
$$X_{u,S}(-1)^{t_T}=(-1)^K\varphi(X_{u,S}+t_T)-\varphi(t_T).$$
These are raw affine forms; no selector output is fed into another gate. For $T\ne\varnothing$, each main ladder has $2K+d_T$ cuts, each reading exactly $K+d_T$ inputs. The $T=\varnothing$ contribution is the raw top affine form $\sum_c y_c$.

There is genuine sharing: $\sum_u(-1)^{U\cdot u}=0$ unless $U=\varnothing$. Thus only the suffix pure-address ladders remain, with coefficient $-B$. Summing gives the explicit input-to-bottom count
$$\begin{aligned}
W_{\rm main}&=2NK(N-1)+\frac32MN^2+\frac{m^2k(k+1)N^2}{4K},\\
W_{\rm correction}&=\frac{m^2r(r+1)K}{4}.
\end{aligned}$$
The bottom count is
$$S=2N(N-1)+\frac{BMN}{2}+\frac{mrK}{2},$$
and the full support count is $W=W_{\rm main}+W_{\rm correction}+S+N$. All quantities are integers; the formulas cover $r=0$ and $p=0$.

[PROVED obstruction for this compiler] For $m\ge2$, all coordinates counted in each main cut are semantically essential. After complementing its negatively weighted table variables, the cut is a threshold of $2\sum_{j=1}^K x_j+\sum_{l=1}^{d_T}a_l$. Because $d_T\ge2$, every level from $0$ to $2K+d_T$ is attained; fixing one address coordinate leaves every level up to $2K+d_T-1$ attainable. Every address coordinate therefore has a witness at every nonconstant cut. A table coordinate also has a witness across its weight-two jump. Distinct cuts have different truth tables, and distinct channels/chunks have different essential supports. Thus this is not a count inflated by irrelevant numerical coefficients or mergeable duplicates.

In particular $W\ge\tfrac32MN^2=\Theta(n^3)$ for **every** chunk size in this fully flattened family. At balance, letting $B=N/K$ and omitting lower-order terms, its main coefficient is
$$W_{\rm main}/N^3=\frac2B+\frac32+\frac B4(1+1/k)+o(1).$$
Growing the number of chunks actually increases the address contribution. The constant-size optimum remains cubic and is worse than the parent's sharper $9/64$ benchmark. This is a rigorous compiler-specific obstruction, not a lower bound against every use of table chunking.

## 3. Sparse Haar rows: the decoder is exact but the obvious carrier expansion is expensive

[PROVED exact noncharacter identity] For a prefix $u$ of length $p<k$, put
$$H_u=\sum_v(y_{u0v}-y_{u1v}),\qquad
\psi_u(b)=\mathbf1[b_{1:p}=u](-1)^{b_{p+1}}.$$
The table row has support $K_p=N/2^p$. The Haar reconstruction is
$$y_b=\frac1N\sum_cy_c+\sum_{p=0}^{k-1}\sum_{u\in\{0,1\}^p}\frac{H_u}{K_p}\psi_u(b).$$
This follows by telescoping the averages of the nested prefix subcubes containing $b$. Its written table support is only $N(k+1)$, including the constant row.

However
$$\psi_u(b)=2^{-p}\sum_{U\subseteq[p]}(-1)^{U\cdot u}(-1)^{(U\cup\{p+1\})\cdot b}.$$
After multiplying the score by $N$, every resulting term has coefficient $\pm1$. Direct parity-carrier flattening at the finest level has $N^2/4$ terms, each using two table inputs and typically $\Theta(M)$ raw address inputs. Their ladder lengths are $\Theta(M)$, so this implementation already costs $\Omega(N^2M^2)=\Omega(n^4)$ wires. Cancellation of pure-address corrections does not remove its mixed gates. Sparse written table rows alone therefore do not establish a sparse raw circuit. A better direct compiler for localized parity wavelets would be a substantive new ingredient.

Explicitly, the finest-level address-square contribution alone is
$$2^{k-1}\sum_{U\subseteq[k-1]}m^2(|U|+1)^2
=\frac{N^2m^2k(k+3)}{16}.$$
For $m\ge2$ these main cuts have the essential-support property proved in §2; different prefixes or characters cannot merge them.

## 4. Raw affine equality guards: an exact paid compiler

[PROVED elementary compiler; earlier paired one-table-bit guard constructions are credited] Let $L(a)$ be a nonzero raw affine form and $g(z)=[Q(z)\ge0]$ a raw threshold. On the finite Boolean domain let $\Delta>0$ be the least nonzero absolute value of $L$, and choose $D>\max|Q|/\Delta$. Then
$$\mathbf1[L=0]g=[DL+Q\ge0]-[L>0].$$
At $L=0$ this is $g$; at positive or negative $L$ the two terms agree. The strict comparison $[L>0]$ is itself an LTF because the attainable values have gap $\Delta$.

Consequently an entire score $F=\beta+\sum_{i=1}^p u_i z_i+\sum_{j=1}^S v_jg_j$ can be gated by $L=0$ using at most $S+p+2$ bottoms: one guarded bottom for each $g_j$, one for each raw affine term, and two shared guard boundaries for the constants. Different large coefficients $D$ are allowed; magnitudes are not wires. If $\ell=|\operatorname{supp}L|$, a safe full support bound is
$$W(\mathbf1[L=0]F)\le W_{\rm bot}(F)+(S+p+2)(\ell+1)+p.$$
This includes the new gate-to-top edges. The union of raw supports is what is charged. There is no intermediate feature layer.

For a single table sign $y_c$, the familiar sharper paired construction is
$$\mathbf1[L(a)=0]y_c=[DL(a)+y_c\ge0]-[DL(a)-y_c\ge0],$$
with $D\Delta>1$. It uses two bottoms and at most $2\ell+4$ total support edges. The earlier monochromatic-plane experiments already used this special case.

If guards cover every address and each guard's local score has the correct strict sign everywhere on that guard, any positive sum of the guarded scores is correct on all independent tables. Overlap causes no difficulty. This is a genuine flattening rule, but the number and support of the guards still have to be paid.

### 4.1 A sharp geometric obstruction for blockwise monochromatic guards

[PROVED new deduction in this investigation; no literature-priority claim] Suppose each guard is a raw affine hyperplane whose absolute address coefficient is constant within each original block; magnitudes may be arbitrary real numbers, unbounded and different between blocks, and sign masks may vary by guard. Require that every address on a nonempty guard has one fixed parity label $c$. Such a guard contains at most
$$\binom m{\lfloor m/2\rfloor}^{k}$$
raw addresses. Therefore any covering family has at least
$$R\ge\left(\frac{2^m}{\binom m{\lfloor m/2\rfloor}}\right)^k=m^{k/2}\exp(O(k))$$
guards. At balance this is $\exp(\Theta((\log n)^2))$, so the paired one-table-bit compiler is superpolynomial in this class.

**Proof.** Every block magnitude must be nonzero, since otherwise flipping a raw bit in that block preserves the guard and changes its label. Complement negative coordinates and let $s_i\in\{0,\ldots,m\}$ be the resulting block counts. The guard equation is $\sum_i a_i s_i=\theta$, and its prescribed parity vector is shifted by fixed mask parities. Suppose two distinct count vectors $s,t$ on it have that prescribed parity. Every coordinate of $t-s$ is even. Let $2^v$, $v\ge1$, be the largest common power of two dividing all nonzero coordinates of $t-s$. Then
$$s+(t-s)/2^v$$
is an integer point in the same box, on the same hyperplane, and has a different parity vector because some coordinate of $(t-s)/2^v$ is odd. This contradicts monochromaticity. Thus the guard contains exactly one count tuple, contributing at most the product of the central binomial coefficients. Covering all $2^{km}$ raw addresses proves the count. Stirling's estimate gives the asymptotics.

This explains the old random-mask cover's cost, rather than merely observing that its upper estimate is large. Its leading exponential scale is unavoidable for this architecture. It also permits arbitrary real inter-block scales, so large coefficients do not repair it. The midpoint proof fails for genuinely unequal magnitudes inside a block: then a block's value is no longer determined by its Hamming count.

This obstruction also survives aggregated-edge accounting for the paired compiler. Remove duplicate guards with the same label and vertex set, merging their positive coefficients. Each of the two mixed threshold functions has table derivative $\pm\mathbf1_H$, so different nonempty guard sets cannot yield identical or complementary Boolean functions. Different labels read different essential table bits. Moreover every address coordinate is essential: at an address on $H$, flip that coordinate and choose the table bit so the mixed gate changes. Thus the emitted gates have actual fan-in $M+1$, not padded coefficients. The number of distinct emitted gates is at least the number of distinct guards even if one permits complement reuse, which already suffices for the superpolynomial conclusion.

This does not lower-bound arbitrary signed one-table-bit circuits or a different resynthesis of the summed score. It rules out obtaining a polynomial construction by this positive monochromatic-guard cover and its stated two-gate compiler.

### 4.2 Heterogeneous guard probe

[VERIFIED finite only] `probe.py` exhaustively examines specified positive-integer coefficient profiles up to permutations within blocks, block permutations, and sign complementation. Its seven cases examine 5,777 profile orbits and every attainable level. None beats the product-central-binomial section bound. This is not an asymptotic theorem for heterogeneous coefficients, and is not evidence that irrational or large-integer constructions are impossible. The largest witnesses found in these small boxes are blockwise uniform. Exact profiles, levels and coverage counts are in `probe.json`.

## 5. A sparse affine-plane decoder: exact identity and the missing compiler

[PROVED exact decoder; standard finite-geometry incidence ingredient] First take $k=2r$, $q=2^r$, and index the $N=q^2$ labels by points of $\mathbb F_q^2$. Use all $q^2+q$ affine lines, including the vertical lines. For a line $\ell$, define the raw table form
$$D_\ell(x)=\sum_{c\in\ell}y_c,$$
which reads only $q=\sqrt N$ table inputs. Any point lies on $q+1$ lines, and two distinct points lie on exactly one common line. Consequently, for **every independent table** and every label $b$,
$$\boxed{\sum_{\ell\ni b}D_\ell(x)-\sum_c y_c=q y_b.}$$
This is an exact common-amplitude identity, not independent character correctness or a sign-only product claim. Its proof is coefficient-wise: $y_b$ appears $q+1$ times in the first sum and every other table sign appears once.

For odd $k$, embed the labels into $\mathbb F_q^2$ with $q=2^{\lceil k/2\rceil}$ and pad the other point values by the real constant zero. There are at most $2N$ points; the same identity holds at every genuine address, with table forms reading at most $q$ genuine bits. The additional address coordinate in the embedding is the constant zero, not a computed feature. Thus the decoder itself applies generically, not only on an even-$k$ subsequence.

[CONJECTURE / precise next candidate] The required module for each line is
$$G_\ell(x,a)=D_\ell(x)\mathbf1[H_\ell b(a)=\beta_\ell],$$
where $H_\ell$ is the rank-$r$ binary matrix describing its field-linear equation. This is an equality of real scores; merely obtaining its sign is insufficient. A direct raw-threshold implementation with $B(N)=O(N^{1-\delta})$ bottoms per line, reading at most $M+q$ inputs each, would give a generic exact
$$W=O(N^2B(N))=O(n^{3-\delta})$$
construction after summing the line modules and the raw affine correction. A bound $B(N)=o(N)$ would already give $o(n^3)$. All bottom-to-top edges and the $N$ raw top edges fit in this count. This is a sufficient construction target, **not an established module bound**.

[PROVED cost of the available compiler] Expanding the syndrome indicator over its $q$ binary characters gives
$$\mathbf1[H_\ell b=\beta_\ell]=\frac1q\sum_{v\in\mathbb F_2^r}(-1)^{v\cdot\beta_\ell}(-1)^{(H_\ell^{\mathsf T}v)\cdot b}.$$
The nonzero character carriers involve up to $M$ raw address bits. Applying the paid parity ladder to each product with $D_\ell$ costs $O(q(M+q))$ bottoms and $O(q(M+q)^2)$ input edges per line. The total is therefore only $O(N^{7/2})$ at balance, worse than the existing benchmark. Pure-address corrections can cancel across parallel lines; their removal does not change this dominant mixed-gate count. At even $k$, the nonzero binary character spaces of the line directions partition all nonzero characters, and this expansion splits each resulting full character into $q$ table chunks. It therefore reproduces the same address-support problem diagnosed in §2.

The module target must directly couple the syndrome coordinates rather than expand all their characters. For a power saving its gates must also escape the bounded-integer blockwise semantic class; changing the table basis alone does not evade that theorem. Unlike a vague request for a better product gadget, the displayed module specifies its domain, exact amplitude, raw inputs, gate target and resulting full wire bound. No implementation meeting that target was found here.

## 6. Verification, attribution, and final assessment

[VERIFIED] Reproduction commands:

```bash
python3 -I /tmp/andreev_gap/wires_upper_astra/checks.py
python3 -I /tmp/andreev_gap/wires_upper_astra/probe.py
```

The first checks complete emitted prefix circuits on all independent raw inputs for seventeen small parameter/chunk choices: 12,272 input evaluations and 1,650 essential-coordinate witnesses. It also checks 5,460 Haar coefficients and 2,120 explicit table/address cases; 25,394 threshold-guard identities, 50,788 paired table-sign guards and 25,394 gated entire scores, including threshold ties; 1,960 blockwise affine forms and 17,976 monochromatic levels for the midpoint lemma; an explicit heterogeneous counterexample to extending its proof; and 4,368 affine-plane coefficients for $q=2,4,8$. Coefficient-wise identities certify every independent table, not just character tables. `checks.json` records exact counts. The probe is separately labelled finite search, never an asymptotic conclusion. No solver or dependency was installed.

Sources and inherited work: the [earlier wire report](/tmp/andreev_gap/wires_astra/report.md) supplies the semantic architecture restrictions; the [current paper](/home/user/.t3/scratch/2026-11-02-improve-upper-bound-of-andreevs-93c6aee6/threshold_paper/paper.tex) supplies the parity-carrier construction and sharper exact score; the parent owns the [cubic support recount](/tmp/andreev_gap/wire_recount/recount.py). All four round-three reports were reconsulted: [UP1](/tmp/andreev_gap/swarm_round3/up1/report.md), [UP2](/tmp/andreev_gap/swarm_round3/up2/report.md), [LOW1](/tmp/andreev_gap/swarm_round3/low1/report.md), [LOW2](/tmp/andreev_gap/swarm_round3/low2/report.md). The earlier monochromatic-plane/rank constructions in the research state and upper reports are predecessors of the guard discussion, not rediscovered upper benchmarks. The guard/compiler observations and standard affine-plane counting carry no novelty-priority claim. A targeted primary-source search rechecked [Kane–Williams §5.2](https://cseweb.ucsd.edu/~dakane/depth2LTF.pdf); no literature claim of a new generic subcubic construction is made.

The strongest completed new obstruction is §4.1: even unlimited real inter-block scales cannot rescue blockwise monochromatic affine covers, and the compiler's support is genuinely essential. The strongest concrete next construction target is §5's exact syndrome-gated sparse table sum. Its decoder is already valid on every table and address; its missing raw-threshold module is identified and fully costed. The simpler prefix/Haar flattenings do not give $o(n^3)$, and the heterogeneous small guard probe found no asymptotic lead. The current generic exact benchmark remains the parent's $W\le(9/64+o(1))n^3$.

Artifacts are confined to this new directory. The previous report was preserved; no shared paper, dependency, additional agent, or online post was created or changed by this upper investigation.
