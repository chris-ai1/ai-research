<!-- Copyright (c) 2026 Christian Reitwiessner. -->
Authors: Christian Reitwiessner

# Upper-bound research: truncated mixed ridges, quantized reconstruction, and selector kernels

## Result and status

**No exact $o(n^2)$ construction is established.** The exact growing-$k$ benchmark remains the inherited research bound $5n^2/16+o(n^2)$, not yet Lean-formalized. This run gives four concrete pieces of progress:

1. **A proved distributional upper bound:** genuinely mixed-sign truncated ridges give agreement at least $1-\delta$ using $O(N\sqrt{(N+km)\log(N/\delta)})$ bottom gates. At balance this is $O(n^{3/2}\sqrt{\log(n/\delta)})$. This does not solve the exact problem; no literature-priority claim is made.
2. **A new exact finite $k=4$ amplitude certificate:** two odd Walsh-amplitude channels give an integer score with margin $43$ on every independent table and parity address. This repairs the inherited sign-only failure, but its independent-ladder implementation does not improve the asymptotic bound or the best balanced constant.
3. **A proved strengthening of a narrow obstruction:** fixed unequal character weights cannot repair the inherited odd sign-only Walsh rule, even with an arbitrary table-dependent intercept. The reason is symmetrization, not a larger solver search.
4. **Two precisely specified exact targets:** a margin-sensitive mixed-window synthesis problem and a direct table-bit-gated selector dictionary. The latter abandons per-character products entirely and turns exact correctness into a necessary-and-sufficient diagonal-dominance inequality.

All new work is in `/tmp/andreev_gap/upper_astra`. No archive files, old processes, commits, or PRs were changed. Both bounded jobs finished successfully. Sources consulted were the local curated state/continuation and the reports in `push_upper`, `coarse_mixed_general`, and `mixed_upper_sol`; the user's supplied summary supplies the latest generator certificate. The arguments below are self-contained derivations, not claims about current external literature.

## 1. Model and inherited bottlenecks

Write $N=2^k$, $n=N+km$, $b_i=\bigoplus_j a_{i,j}$, and $\xi_c=2x_c-1$. The target sign is $\xi_b$. Define

$$\chi_S(c)=(-1)^{|S\cap c|},\qquad X_S=\sum_c\chi_S(c)\xi_c.$$

For $k\ge1$, every $X_S$ is even, and

$$\sum_S X_S\chi_S(b)=N\xi_b,\qquad \sum_S X_S^2=N^2.$$

A bottom is one LTF of the original table and address bits. The top may read original bits. Throughout, $S$ counts bottoms; total gates are $S+1$. All coefficients may be real. The approximation claim uses uniform independent **raw** table and address bits, not uniform count vectors or a generator-restricted table family.

Inherited facts that govern this search:

- A separate full ladder for each nonempty character incurs $\Theta(m\sum_S|S|)=\Theta(kmN)$ even with a constant number of amplitude channels. At $km\sim N$ this is quadratic.
- Merely reorienting address coordinates leaves the full range intact. Mixed signs help only with localization or sharing.
- Exact constant coverage by translates of one middle-layer kernel has an exponential mask-support obstruction in the archived restricted architecture. Varying widths can cancel fluctuations, but the existing witnesses are expensive.
- The $k=3$ joint top-score refit gives a fixed-$k$ additive saving. It suggests optimizing the whole score, not reconstructing every product independently.
- The sign-coherent and unrestricted lower bounds do not prohibit a logarithmically subquadratic mixed construction. A failed window cover is not an unrestricted lower bound.

For balance use $m=\lfloor N/k\rfloor$, so $n=2N-O(k)$, or take $k$ along powers of two with exact $km=N$.

## 2. Mechanism I: central mixed ridges, with exact tail repair as the missing step

### 2.1 Actual hyperplanes and score

For every nonempty $S$, let $M_S=|S|m$. Choose a mask $z_S$ on its active raw coordinates and put

$$L_S(a)=|a_S\oplus z_S|=|z_S|+\sum_{i\in S,j}(1-2z_{S,i,j})a_{i,j}.$$

Choose an even integer $e_S$ nearest $M_S/2$, so $|e_S-M_S/2|\le1$, and set $d_S=L_S-e_S$. Choose masks nonconstant inside every active block, with different choices across characters. For example, when $m\ge3$, use one flipped coordinate per active block and vary that coordinate with $S$. This produces genuinely different mixed views, not merely different block signs or one common reorientation.

Let $\phi(u)=(-1)^u u$. Since $X_S$ is even,

$$\phi(X_S+d_S)+\phi(X_S-d_S)=2X_S(-1)^{d_S}.$$

Therefore, with $\eta_S=(-1)^{|z_S|+e_S}$,

$$2X_\varnothing+\sum_{S\ne\varnothing}\eta_S\bigl(\phi(X_S+d_S)+\phi(X_S-d_S)\bigr)=2N\xi_b.$$

For integer $R\ge1$, replace $\phi$ by the clipped staircase

$$\psi_R(u)=\phi(-R)+\sum_{\ell=-R+1}^{R}\bigl(\phi(\ell)-\phi(\ell-1)\bigr)[u\ge\ell].$$

It equals $\phi$ on $[-R,R]$ and is constant outside. The proposed actual top score is

$$P_R=2X_\varnothing+\sum_{S\ne\varnothing}\eta_S\bigl(\psi_R(X_S+d_S)+\psi_R(X_S-d_S)\bigr).$$

Each indicator is the bottom hyperplane

$$[X_S\pm L_S\ge\ell\pm e_S].$$

After substituting $X_S=2\sum_c\chi_S(c)x_c-\sum_c\chi_S(c)$ and $L_S$, these are LTFs of raw inputs, with table weights $\pm2$ and address weights $\pm1$. There are at most

$$S_R=4(N-1)R$$

bottoms and one top. Constants and $2X_\varnothing$ are free affine top terms. There is no hidden extra layer.

### 2.2 Uniform-input theorem [proved]

On the event that all $2(N-1)$ arguments have magnitude at most $R$, the score is exactly $2N\xi_b$. For a fixed argument, the independent table terms have interval length two and the active raw address terms have interval length one. Its mean has magnitude at most one. Hoeffding's inequality gives, for $R>1$,

$$\Pr(|X_S\pm d_S|>R)\le2\exp\left(-\frac{2(R-1)^2}{4N+M_S}\right).$$

A union bound, using $M_S\le km$, proves that

$$R=\left\lceil1+\sqrt{\frac{4N+km}{2}\log\frac{4N}{\delta}}\right\rceil$$

suffices for agreement at least $1-\delta$. Thus

$$S=O\!\left(N\sqrt{(N+km)\log(N/\delta)}\right).$$

At balance this is $O(n^{3/2}\sqrt{\log(n/\delta)})$. In advantage notation this gives $\varepsilon\ge1/2-\delta$, for $0<\delta<1/2$. It is compatible with the inherited unrestricted lower bound; it does not claim optimal logarithms. The probability argument works for any fixed masks, so using genuinely different mixed masks incurs no probability or gate-count penalty.

### 2.3 Why this does not yet give exact subquadratic size

Demanding the union-bound failure probability be less than one atom of the full input space requires $\delta<2^{-n}$, which restores $R=\Theta(N)$ at balance and hence quadratic size. Concentration cannot be silently upgraded to exactness.

Define the explicit residual

$$E_R(x,a)=2N\xi_b-P_R(x,a).$$

A sufficient exact-repair lemma is: there is a sum $Q$ of $o(N^2)$ actual bottom LTFs and an affine term such that

$$|Q-E_R|<2N\quad\text{on every input},$$

while $R=O(\sqrt{N\log N})$. Then $P_R+Q$ has the correct sign. Exact equality $Q=E_R$ is stronger than necessary. The missing lemma is **shared tail repair**: the tail pieces for different Walsh forms and mixed views must be implemented jointly. Paying for every tail separately simply restores the old ladders.

Useful correlation: Parseval bounds the number of large table coefficients by

$$\#\{S:|X_S|>H\}\le N^2/H^2.$$

This is an input-dependent sparsity statement, not a circuit-size bound. A fixed circuit cannot instantiate only the active characters for free. Nor does this bound control address tails. It identifies the intended sharing resource but does not supply the missing construction.

**Bounded exact check.** `verify.py` checks all $131072$ raw inputs for $k=3,m=3$, using masks that vary inside blocks. It verifies the full identity on every input and verifies zero errors on the central event for radii $2,4,6,8,10,13$. Radius $13$ is exact on the whole domain. Clipping errors are not monotone in radius: radius six gives 4000 errors and radius eight gives 6286. This is a concrete warning against treating a larger clipped window as a pointwise improvement. The theorem only uses a monotone sufficient event, not monotonicity of the clipped score.

## 3. Mechanism II: controlled-margin quantization plus joint mixed windows

This route stays in Fourier coordinates but changes the reconstruction problem from exact coefficient recovery to a single robust sign score.

### 3.1 New $k=4$ certificate [exact finite theorem]

For $r>0$ put

$$q_r(t)=[t\ge r]-[t\le-r].$$

For $N=16$, the score

$$\boxed{F(x,b)=4X_\varnothing+\sum_{S\ne\varnothing}\chi_S(b)\bigl(11q_2(X_S)+32q_4(X_S)\bigr)}$$

satisfies

$$\xi_b F(x,b)\ge43$$

for every table and every parity address. Thus the amplitude is $0$ at zero, $11\operatorname{sgn}(t)$ at $|t|=2$, and $43\operatorname{sgn}(t)$ at $|t|\ge4$.

**Certificate and independent verification.** Translation of the address labels maps any $b$ to zero and multiplies $X_S$ by $\chi_S(b)$. Since $q_r$ is odd, checking every one of the $65536$ tables at $b=0$ proves all $1048576$ table/address cases. `probe.py` compresses these to 42 distinct integer constraint rows, uses a small LP only for discovery, and reconstructs rational coefficients. The separate standard-library `verify.py` enumerates every table, evaluates the displayed integer formula, and obtains minimum margin exactly 43. A second certificate, also checked rationally in discovery, is

$$5X_\varnothing+\sum_{S\ne\varnothing}\chi_S(b)(16q_2(X_S)+36q_6(X_S)),$$

with margin at least 52. The first certificate is the main reported one.

This is a new abstract ordinary-table certificate relative to the read archive. It is not an optimum for unrestricted circuits, nor an improved growing-$k$ upper bound.

### 3.2 Actual mixed-sign all-$m$ realization and its cost

For an integer table form $X$, write

$$q_r(X)=\tfrac12\bigl((2[X\ge r]-1)+(2[X\ge1-r]-1)\bigr).$$

For either cutoff $v$, choose integer $B>N+|v|$, any mixed mask on the active coordinates, and let $L=|a\oplus z|$, $H=[X\ge v]$. Then

$$C=\sum_{j=0}^{\lfloor M/2\rfloor}[BL+X\ge2Bj+v]$$

obeys

$$4C-2L-1-2H=(-1)^L(2H-1).$$

Multiplying by $(-1)^{|z|}$ realizes $\chi_S(b)(2H-1)$. Substitute these actual raw-input LTFs into the boxed certificate. Masks can differ between channels and characters and be mixed inside each active block. There are four $H$-channels for each of the fifteen nonempty characters. Consequently a straightforward realization has at most

$$S=4\sum_{S\ne\varnothing}\left(\lfloor |S|m/2\rfloor+2\right)=64m-16[m\text{ odd}]+120$$

bottoms, plus one top. Degenerate constants or coincident gates can only reduce this bound. For $m\ge2$ mixed masks exist; $m=1$ still has the same algebraic construction but cannot have mixed signs within a one-bit block.

This count is **not competitive with the strongest inherited construction**. The significance is the certified two-level nonlinear amplitude and its known margin, which make a mixed-window replacement falsifiable instead of speculative.

### 3.3 A stronger failure theorem for sign-only reconstruction [proved]

There are no fixed real $w_S$ and no arbitrary table-dependent intercept $D(x)$ such that

$$D(x)+\sum_{S\ne\varnothing}w_S\operatorname{sgn}(X_S)\chi_S(b)$$

strictly represents every $k=4$ table, with $\operatorname{sgn}(0)=0$.

**Proof.** Suppose such weights existed. Average valid scores over the action of $\mathrm{GL}(4,2)$ on table labels and addresses. Validity and positive margins are preserved under averaging. This group acts transitively on nonzero characters, so all averaged character weights equal one common $w$, while the intercept remains some function of the table. Take the table whose ones are at $0,1,2,4,8$. Its equal-weight sign reconstruction takes the same value 5 at addresses 0 and 15, although their desired outputs differ. Multiplication by any common $w$ and addition of an address-independent intercept cannot separate them, contradiction.

Even a freely supplied address-only term can be eliminated first by averaging translations; it becomes a constant absorbed into $D$. This theorem is about odd sign-only amplitudes with fixed top coefficients. It does **not** exclude asymmetric tie handling, multiple amplitude thresholds, nonlinear table-dependent character weights, or nonseparable mixed gates.

For a common single odd threshold $q_r$, all $r>2$ also fail: a table with exactly one one has every nonconstant $|X_S|=2$, so all channels vanish and no intercept separates its addresses. Together these facts show that two odd threshold channels are necessary and sufficient in the common-quantizer family considered here. The necessity is analytic, not a floating-point infeasibility claim.

### 3.4 A scalable quantization lemma, but not a cheap circuit [proved]

There is an odd staircase $f$ on the even integers in $[-N,N]$, with $O(\sqrt N)$ positive steps, such that

$$|f(t)-t|\le t^2/(4N).$$

One explicit construction starts at positive grid point $r=2$, uses the next grid point

$$r'=r+2\max\{1,\lfloor r^2/(8N)\rfloor\},$$

and sets $f(t)=r$ for even $r\le t<r'$, extending oddly and setting $f(0)=0$. If the step is two there is no intermediate even integer and no rounding error. Otherwise the error is below $r^2/(4N)\le t^2/(4N)$. Up to $O(\sqrt N)$ the grid may retain every even value. `quantizer_check.py` independently verifies the rounding-error inequality on every positive even input for $N=2,4,…,65536$. Above that scale, each dyadic interval $[u,2u]$ contains $O(N/u+1)$ grid points; summing gives $O(\sqrt N)$ steps.

Parseval then gives, for every table and address,

$$\left|\sum_{S\ne\varnothing}(f(X_S)-X_S)\chi_S(b)\right|\le N/4.$$

Thus $X_\varnothing+\sum_{S\ne\varnothing}f(X_S)\chi_S(b)$ has margin at least $3N/4$. This supplies a controlled-margin all-$k$ quantizer with substantially fewer amplitude thresholds than exact coefficient recovery. However, independent coarse ladders cost $O(\sqrt N\,kmN)$, or $O(N^{5/2})$ at balance. It is a reconstruction lemma, **not** a gate improvement. It also does not prove that constant-many channels are impossible for growing $k$.

### 3.5 Exact mixed-window target and its obstruction

For each $H=[h(x)\ge v]$, the inherited localized identity realizes

$$\chi_S(b)(2H-1)[p\le L_z(a)\le u]$$

using the actual data gates $[BL_z+h\ge B\ell+v]$, $p\le\ell\le u$, and the two endpoint gates $[L_z\ge p]$, $[L_z\ge u+1]$. Cost is $u-p+3$. An odd $q_r$ window uses its two $H$ channels with the same mask/window and shares the two endpoints, costing at most $2(u-p+1)+2$ bottoms. All masks here should be mixed inside every relevant block and genuinely different across windows.

Instead of requiring each channel's window weight $W_{S,r}(a)$ to be identically one, ask directly for

$$\xi_b\left(D(x)+\sum_{S,r}\alpha_{S,r}\chi_S(b)q_r(X_S)W_{S,r}(a)\right)>0$$

on all raw inputs, with total localized bottom cost $o(N^2)$. This is the exact missing lemma for the second mechanism. The $k=4$ certificate supplies explicit $D,\alpha$ and a margin to start from. A uniform perturbation condition $|W-1|<1/15$ suffices for that certificate, because its total amplitude weight is $15(11+32)=645$ and its margin is 43. Joint synthesis can be less restrictive than this sufficient bound.

Cautions: (i) uniform approximate coverage is different from the archived exact single-kernel cover, but naive sampling can be expensive; (ii) setting any character's windows identically zero at an address fails on its parity table unless some other part of the score handles that table; (iii) simply implementing all $O(\sqrt N)$ quantizer channels independently is worse than the baseline. The objective must price shared endpoints and data gates globally, and optimize the full score rather than a list of independent products.

## 4. Mechanism III: table-bit-gated address dictionaries, with no character products

This is the cleanest distinct exact architecture to test next.

Choose arbitrary mixed address halfspaces

$$E_j(a)=[w_j\cdot a\ge t_j],\qquad j=1,\ldots,H,$$

and coefficient vectors $\beta_{cj}$, with constants $d_c$. Define address kernels

$$K_c(a)=d_c+\sum_j\beta_{cj}E_j(a).$$

The target top score is linear in the independent table signs:

$$F(x,a)=\sum_c\xi_c K_c(a).$$

**Exact characterization.** This score is correct for every table at an address $a$ if and only if

$$\boxed{K_{b(a)}(a)>\sum_{c\ne b(a)}|K_c(a)|.}$$

Sufficiency is the triangle inequality. Necessity follows by choosing every other independent table sign adversarially. A zero score cannot be allowed in this odd-in-table-signs model, since complementing the table would create the opposite target with the same zero score. This proves the strict condition regardless of which output gets a threshold tie.

**Actual bottom gates.** For every nonzero $\beta_{cj}$, choose $B_j>\max_a(w_j\cdot a-t_j)$ and use

$$g_{cj}(x,a)=[w_j\cdot a+B_jx_c\ge t_j+B_j]=x_cE_j(a).$$

The top score is

$$\sum_c d_c(2x_c-1)+\sum_{cj}\beta_{cj}(2g_{cj}-E_j).$$

Thus the construction has at most

$$S=H+\operatorname{nnz}(\beta)$$

bottoms and one top. If $\sum_c\beta_{cj}=0$, the address-only gate $E_j$ disappears from the top and need not be instantiated. Each $E_j$ is shared by all table columns. No table/parity intermediates are assumed available.

**Precise proposed lemma.** Find mixed directions and sparse coefficients satisfying the boxed inequality for every raw address, with $H+\operatorname{nnz}(\beta)=o(N^2)$ at balance. A sufficient quantitative target is $O(m)$ nonzeros per column and $H=O(Nm)$, yielding $O(Nm)=O(n^2/\log n)$. More generally, $o(km)$ average nonzeros per column plus $H=o(N^2)$ is enough.

The plausible source of saving is that $K_c$ need only dominate at the selected address; it need not be the exact parity-cell indicator. Positive and negative leakage may be shaped jointly before the absolute-value condition is enforced. This is stronger than merely testing parity tables, but it avoids separately constructing every Walsh product. The condition exposes exactly which cancellation is useful and which is not: leakage within a column can cancel, whereas arbitrary independent table bits prevent cancellation between different nonselected columns in the final correctness test.

**Current blocker.** No such economical dictionary is known here. Exact parity-cell indicators obtained by Fourier expansion fall back to expensive independent ladders. Nonnegative unions of address regions are also problematic because a region containing opposite parity cells creates positive leakage. The boxed condition is a construction target, not evidence that the required dictionary exists. The architecture restricts each table-dependent gate to one table bit; unrestricted multi-table-bit gates could be essential.

**Next tractable experiment.** At $k=2,m=3$ or $k=3,m=2$, use a finite dictionary of mixed $0,\pm1$ directions, introduce $K_c(a)$ and auxiliary variables dominating $|K_c(a)|$, and impose the boxed inequalities with margin one. Start with an LP for feasibility and sparsity heuristics, then use a small support-bounded exact search only for a promising support. Verify any candidate by integer/rational arithmetic on all raw addresses. Compare the actual $H+\operatorname{nnz}(\beta)$ count with the inherited witnesses. Failure would concern that dictionary, not the general architecture.

## 5. Ranking and immediate next actions

1. **Best exact research target: shared selector dictionary.** Its correctness condition is necessary and sufficient within a clear alternative architecture, and the desired $O(Nm)$ accounting would already be subquadratic. It avoids the full-ladder commitment. First test whether low-cost kernels exist in a small mixed dictionary before expanding a solver campaign.
2. **Best developed building block: two-channel $k=4$ certificate plus joint windows.** The next finite experiment should optimize the whole raw-input margin using localized mixed gates, with the explicit 43-margin certificate as a baseline. Require an improvement in total layer/support cost, not merely another positive cover identity. The scalable quantization lemma gives a fallback certificate but not a plausible gate count on its own.
3. **Best proved asymptotic statement from this run: distributional truncated ridges.** It achieves near-perfect uniform agreement at roughly $n^{3/2}$ times a logarithmic factor. For exactness, the first needed lemma is economical shared repair of the explicitly defined tails; input-dependent Walsh sparsity alone is insufficient. Do not spend time optimizing truncation constants until a repair mechanism exists.

No claimed result here improves the exact $5/16$ leading constant. The report does give an exact new finite reconstruction identity, a stronger narrow impossibility proof, a general quantization lemma, an explicit approximation construction, and two testable exact bottlenecks. All correctness statements concern ordinary Andreev with independent tables; none use generalized/code-based Andreev or generator-family coverage.

## 6. Artifacts and reproduction

- `probe.py`: bounded LP discovery; 65536 tables collapse to 42 integer rows. It tries subsets of eight possible positive even thresholds, stopping at the first feasible channel count. Each LP has a five-second limit; the whole run completed. Successful rational candidates are checked against every distinct row.
- `probe_results.json`, `probe.log`: two rational two-channel certificates and discovery output. Infeasible LP statuses are not used as proof.
- `verify.py`: independent standard-library integer verification of the main $k=4$ certificate, the sign-only collision, the full mixed ridge identity, and six truncated radii on all $k=3,m=3$ raw inputs.
- `verification.json`, `verification.log`: exact results, including the certificate margin histogram and central-event checks.
- `quantizer_check.py`, `quantizer_results.json`, `quantizer.log`: independent integer checks of the scalable rounding-error inequality through $N=65536$.

Run `python3 /tmp/andreev_gap/upper_astra/verify.py` for the proof checks. Discovery additionally needs NumPy/SciPy; the script checks `/tmp/pydeps` and then the normal Python environment. No solver or other job from this run remains active. All newly authored files credit Christian Reitwiessner.
