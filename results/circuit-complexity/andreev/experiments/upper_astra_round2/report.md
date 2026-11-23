<!-- Copyright (c) 2026 Christian Reitwiessner. -->
Authors: Christian Reitwiessner

# Ordinary Andreev upper bounds: Astra round 2

## 1. Result and scope

**A real logarithmic improvement for uniform average-case computation is proved below. No exact subquadratic construction, exact leading-constant improvement, or competitive new fixed-size exact witness was found.**

For $N=2^k$, $n=N+km$, independent uniform raw table and address bits, and $0<\delta\le1/2$, the new bound is

$$
S=O\left(N\sqrt{(N+km)\log\frac{N+km}{N\delta}}\right)
$$

bottom LTFs plus **one** top LTF, with agreement at least $1-\delta$. In the balanced regime $km\asymp N$, this becomes

$$
\boxed{S=O\left(n^{3/2}\sqrt{\log(1/\delta)}\right).}
$$

In particular, **constant error needs $O(n^{3/2})$ gates**, improving the previously established $O(n^{3/2}\sqrt{\log n})$ upper bound. This is not the previous concentration/union-bound rediscovery. The new step is cancellation of cross-character truncation errors after independently randomizing the address masks, followed by fixing one deterministic circuit.

For $N^{-1/2}\le\varepsilon\le1/8$, the same method gives

$$
\boxed{S=O\left(\varepsilon^2n^{3/2}\sqrt{\log(1/\varepsilon)}\right),\qquad
W=O\left(\varepsilon^2n^{5/2}\sqrt{\log(1/\varepsilon)}\right)}
$$

at balance, with agreement at least $1/2+\varepsilon$. Here $W$ counts support wires, including the top. For $1/8<\varepsilon<1/2$, use the first bound with $\delta=1/2-\varepsilon$. The logarithmic improvement is strict when $\log(1/\varepsilon)=o(\log n)$; it does **not** change the asymptotic order for polynomially small advantage. Similarly, polynomially small error still costs $O(n^{3/2}\sqrt{\log n})$.

These are hand-proved existence/construction bounds with explicit raw-input gate formulas and exact finite audits, not Lean results or independently reviewed theorems. There is no claim of an exhaustive literature novelty check. The comparison is against the supplied archive, including the corrected earlier paper theorem.

## 2. Quantitative finite theorem

Assume $k,m\ge1$. Choose $1\le r\le k$, put $t=2^r$, and define

$$
V=N+\frac{rm}{4},\qquad
R=\left\lceil4\sqrt{V\log\frac{16V}{t\delta}}\right\rceil,
\qquad 0<\delta<1.
$$

There is a fixed depth-two raw-input threshold circuit with

$$
\boxed{S\le4(t-1)(R+1)}
$$

bottoms, $S+1$ total gates, agreeing with ordinary Andreev on at least

$$
\frac12+\frac12p(N/t)-\delta,
\qquad p(1)=1,\qquad
p(L)=2^{-L}\binom{L}{L/2}\quad(L\text{ even}).
$$

One can use $t=1$ separately: majority of the whole table uses zero bottoms and has advantage $p(N)/2$.

The construction uses only bottom table weights $\pm2$ and nonzero address weights $\pm1$. Top weights and thresholds are integers. Masks are fixed in the circuit; **there is no fresh randomness, supplied mask input, computed parity input, or Walsh-feature input at evaluation time**. The mask-selection proof is nonuniform and does not claim polynomial-time construction. A finite deterministic exhaustive selection algorithm is specified in §5.

## 3. Explicit gates and exact score

Write $\xi_c=2x_c-1$ and

$$
X_S=\sum_{c\in\{0,1\}^k}\chi_S(c)\xi_c,
\qquad \chi_S(c)=(-1)^{\sum_{i\in S}c_i}.
$$

Only characters $S\subseteq[r]$ are used. For every nonempty $S$, independently choose a mask $z_S\in\{0,1\}^{M_S}$, where $M_S=m|S|$ indexes its active raw address coordinates. Define

$$
h_S=\lfloor M_S/2\rfloor,\quad
D_S=|a_S\oplus z_S|-h_S,\quad
\sigma_S=(-1)^{|z_S|+h_S},\quad
\phi(u)=(-1)^u u.
$$

Since $X_S$ is even,

$$
\sigma_S\bigl(\phi(X_S+D_S)+\phi(X_S-D_S)\bigr)
=2X_S\chi_S(b).
$$

Use **zero truncation**, not the prior report's constant-extension clipping:

$$
f_R(u)=\phi(u)\mathbf1[|u|\le R],
\qquad
P_z=2X_\varnothing+\sum_{\varnothing\ne S\subseteq[r]}
\sigma_S\bigl(f_R(X_S+D_S)+f_R(X_S-D_S)\bigr).
$$

The corresponding untruncated score is

$$
P_*=2\sum_{S\subseteq[r]}X_S\chi_S(b)
=2t\sum_{c\in Q(b)}\xi_c,
\qquad Q(b)=\{c:c_i=b_i\text{ for }i\le r\}.
$$

Every staircase is an explicit linear combination of raw-input LTFs:

$$
f_R(U)=\sum_{\ell=-R}^{R+1}\bigl(f_R(\ell)-f_R(\ell-1)\bigr)[U\ge\ell].
$$

For each sign $q\in\{-1,1\}$, the affine form is

$$
U=X_S+qD_S
=2\sum_c\chi_S(c)x_c-\sum_c\chi_S(c)
+q\left(|z_S|-h_S+\sum_{j\text{ active}}(1-2z_{S,j})a_j\right).
$$

Thus the actual gate has table weights $2\chi_S(c)$, active address weights $q(1-2z_{S,j})$, and cutoff

$$
\ell+\sum_c\chi_S(c)-q(|z_S|-h_S).
$$

Its top coefficient is $\sigma_S(f_R(\ell)-f_R(\ell-1))$. There are at most $2R+2$ gates per form, two forms per nonempty character. Zero coefficients and constant/duplicate gates can be removed, but are not needed for the bound. The top directly reads table bits through $2X_\varnothing=4\sum_cx_c-2N$.

When $t=N$, output $[P_z\ge0]$. When $t<N$, output $[P_z\ge-2t]$. The latter threshold implements positive ties for the subcube majority: $|Q|$ is even, so $P_*$ is a multiple of $4t$ and every attainable value is at least $2t$ away from $-2t$. In both cases an error relative to the untruncated majority requires

$$|P_z-P_*|\ge2t.$$

## 4. The new mean-square argument

Let $e_S$ be the clipped-minus-exact contribution from character $S$.

### 4.1 Cross-character errors vanish in expectation

Fix any raw input $(x,a)$. For uniform $z_S$, $D_S$ has distribution

$$D_S\sim\operatorname{Bin}(M_S,1/2)-h_S,$$

independent of $a$. Also,

$$\sigma_S=\chi_S(b)(-1)^{D_S}.$$

It follows that

$$\mathbb E_{z_S}[e_S\mid x,a]=\chi_S(b)g_S(X_S)$$

for a function $g_S$ of the table form alone. Different characters use independent masks. Therefore, for distinct $S,T$,

$$
\begin{aligned}
\mathbb E_{z,x,a}e_Se_T
&=\mathbb E_{x,a}\bigl[\chi_S(b)\chi_T(b)g_S(X_S)g_T(X_T)\bigr]\\
&=\mathbb E_x[g_S(X_S)g_T(X_T)]\,
\mathbb E_a[\chi_{S\triangle T}(b)]=0.
\end{aligned}
$$

Here uniform independent raw bits induce uniform independent block parities. Table bits are independent of addresses. **No independence of different Walsh coefficients is used or claimed.** Hence

$$
\boxed{\mathbb E_{z,x,a}(P_z-P_*)^2
=\sum_{\varnothing\ne S\subseteq[r]}\mathbb E e_S^2.}
$$

This is the step absent from the prior simultaneous-window argument. A single common global reorientation would not give the conditional independence used here.

### 4.2 Bound each diagonal term

For $U=X_S\pm D_S$, its centered version $Y=U-\mathbb E U$ is a sum of independent centered variables with subgaussian variance proxy

$$V_S=N+M_S/4\le V,$$

so $\Pr(|Y|>u)\le2e^{-u^2/(2V_S)}$. The mean of $U$ has absolute value at most $1/2$. For integer $R\ge1$, $|U|>R$ implies $|Y|>R/2$, and $U^2\le2Y^2+1/2$. Integrating the subgaussian tail gives

$$
\mathbb E[U^2\mathbf1_{|U|>R}]
\le(R^2+8V_S+1)e^{-R^2/(8V_S)}
\le16V_S e^{-R^2/(16V_S)}.
$$

For completeness, $\mathbb E[Y^2\mathbf1_{|Y|>q}]\le2(q^2+2V_S)e^{-q^2/(2V_S)}$, with $q=R/2$. For the final simplification use $v=R^2/(8V_S)$, $V_S\ge1$, and $(v+2)e^{-v/2}\le2$.

Zero truncation gives

$$
e_S^2\le2\sum_{q\in\{-1,1\}}
(X_S+qD_S)^2\mathbf1[|X_S+qD_S|>R].
$$

Consequently

$$
\mathbb E_{z,x,a}(P_z-P_*)^2
\le64(t-1)V e^{-R^2/(16V)}.
$$

Markov's inequality at squared distance $4t^2$, followed by averaging over masks, produces one fixed circuit whose disagreement with subcube majority is at most

$$
\frac{16(t-1)V}{t^2}e^{-R^2/(16V)}
\le\frac{16V}{t}e^{-R^2/(16V)}\le\delta.
$$

The exact majority agreement $1/2+p(N/t)/2$ is the already-established subcube-vote calculation in the earlier paper. This completes the finite theorem.

## 5. Determinism and genuinely mixed, different masks

The theorem is not a randomized circuit guarantee. It averages the uniform-input loss of a finite collection of fixed circuits, so at least one fixed mask collection achieves the stated guarantee. An explicit finite deterministic algorithm can enumerate all mask collections and all raw inputs and choose the collection minimizing its exact squared score error. Conditional expectation can instead fix masks successively; both algorithms may be exponential. No efficient derandomization is claimed.

The required genuinely mixed patterns can be imposed without changing the asymptotic balanced result. A union bound over every active block of every character gives

$$
\Pr[\text{some mask is constant inside an active block}]
\le\sum_{S\ne\varnothing}|S|2^{1-m}=rt2^{-m}.
$$

For $r\ge2$, also exclude collections obtained by restricting one global mask to every character, even allowing a separate whole-mask complementation per character. Counting these collections bounds their probability by

$$
2^{rm+(t-1)-mrt/2}.
$$

Let

$$q=rt2^{-m}+2^{rm+(t-1)-mrt/2}.$$

Whenever $q<1$, condition the distribution of **circuits**, not inputs, on neither bad event occurring. The conditional expected nonnegative squared error is at most its unconditional expectation divided by $1-q$. Thus use $\delta(1-q)$ in the radius formula. A fixed circuit exists with every active block genuinely mixed and with patterns that cannot come from one common reorientation, still attaining error budget $\delta$.

For $km\asymp N$ with growing $k$ and $2\le r\le k$, $q=o(1)$ uniformly. Exact balance can be taken along valid $k\mid2^k$; $m=\lfloor N/k\rfloor$ gives the same asymptotic estimates. This restriction is harmless in that regime. At $r=1$, only one nonempty character is used, so cross-character diversity is inapplicable. The unconditioned theorem itself holds for every $k,m\ge1$, including small $m$ where the mixed-mask conditioning bound is unavailable.

Each ladder's two forms have opposite address orientations, but masks across characters are independently chosen; this is not merely assigning opposite uniform signs to blocks.

## 6. Gate and wire comparisons to the corrected baselines

At exact balance $km=N$, $n=2N$, and $V\le5N/4$. Taking $t=N$ gives explicitly

$$
S\le4(N-1)\left(\left\lceil4\sqrt{\frac{5N}{4}\log\frac{20}{\delta}}\right\rceil+1\right)
$$

before optional mixed/diversity conditioning. The leading bound is $16\sqrt{5/4}\,N^{3/2}\sqrt{\log(20/\delta)}+O(N)$. Constants here are deliberately conservative.

For $N^{-1/2}\le\varepsilon\le1/8$, choose the least power of two $t\ge32\varepsilon^2N$, and set $\delta=\varepsilon$. Then $t<64\varepsilon^2N$, $t\le N$, and $p(N/t)/2\ge\sqrt{t/(8N)}\ge2\varepsilon$. Also

$$\log\frac{16V}{t\delta}=O(\log(1/\varepsilon))$$

at balance. This proves the claimed advantage dependence. Every bottom has fan-in at most $n$, and the top has at most $S+N$ nonzero inputs, so $W\le nS+S+N$.

Comparisons:

- **Earlier paper `thm:avgupper` and depth-two notes Theorem 2:** previously $O(n^{3/2}\sqrt{\log(n/\delta)})$ for error $\delta$, and $O(\varepsilon^2n^{3/2}\sqrt{\log n})$ gates / $O(\varepsilon^2n^{5/2}\sqrt{\log n})$ wires over the stated regime. Those sources were read before making this comparison. The improvement is replacement of the global union-bound logarithm by the error/advantage-dependent logarithms above. At constant error or advantage it removes a factor $\sqrt{\log n}$. It does not improve the $3/2$ power or the $\varepsilon^2$ power.
- **General exact $d''$:** the $N^2/2+(3/4)kmN-\Theta(kN)+O(N+km)$ bound, leading $5n^2/16$, remains the strongest supplied general exact result. This round does not improve it. Driving our probabilistic error bound below one input's mass requires an exponentially small error parameter and restores quadratic cost. The old $3n^2/4$ Lean result remains separate.
- **Fixed $k=3$:** the all-$m$ $6\lfloor m/2\rfloor+6m+\lfloor3m/2\rfloor+20$ result, slope $21/2$, and 48/62/83 bottoms at $m=3,4,6$ are unchanged. This round's exact selector witness at $m=2$ costs 213 versus the inherited formula's 41. Its finite ridge audits are likewise noncompetitive as exact circuits.
- **Fixed $k=2$:** the ten-bottom $A_{2,3}$ and $A_{2,4}$ witnesses, and three-bottom minima at $m=1,2$, are unchanged. Our selector dictionary yields 92 bottoms at $m=3$, not an improvement. No claim against the larger-$m$ diagonal family is made. The seven-bottom 968/1024 candidate remains failed and was not used.
- **Prior Astra $k=4$ certificate:** the $4X_\varnothing+\sum\chi_S(b)(11q_2(X_S)+32q_4(X_S))$ score, margin 43, and noncompetitive independent-ladder count $64m-16[m\text{ odd}]+120$ remain unchanged. We neither improve its exact cost nor claim its certificate anew.
- **Prior Astra approximation:** random reorientation alone was not the advance. The present independent-mask cross-moment cancellation and zero-truncation error analysis supply the new quantitative improvement. Parseval's input-dependent tail sparsity is not charged as free adaptive hardware.

All claims concern arbitrary independent tables, not generator-family coverage. The lower report's signature filter is an exact-correctness constraint and is not being invoked as a statement about these approximate circuits.

## 7. Bounded exact search and exact finite checks

The exact route tested was the suggested selector dictionary. For each block, directions were either zero or a genuinely mixed vector in $\{-1,1\}^m$. All products of these block choices were included, up to reversing an entire direction, and every nonconstant integer threshold was included. Reverse gates are representable with the constant and signed coefficients. This is a **restricted dictionary**, not all ternary halfspaces or unrestricted THR circuits.

For kernels $K_c=d_c+\sum_j\beta_{cj}E_j$, the LP imposed, on every raw address,

$$K_b\ge1+\sum_{c\ne b}|K_c|.$$

Absolute-value auxiliaries and split signed coefficients gave a linear program. Four iteratively reweighted $\ell_1$ objectives were run per instance, each with a 15-second cap. Every solve finished normally. Best coefficients were rationally reconstructed and checked on every raw address. Gate cost was counted exactly as

$$\operatorname{nnz}(\beta)+\#\{j:\sum_c\beta_{cj}\ne0\}.$$

This counts both each table-bit-gated $x_cE_j$ and every surviving shared address-only gate. Such a product is the actual LTF $[w_j\cdot a+B_jx_c\ge t_j+B_j]$ for $B_j>\max_a(w_j\cdot a-t_j)$.

Bounded run matrix:

| Task | Domain / budget | Status | Result |
|---|---|---|---|
| Mixed selector $k=2,m=3$ | 126 address gates; four LPs, cap 15 s each | Feasible / exact rational SAT witness | Counts 256,144,100,92; best 92, margin 1 |
| Mixed selector $k=3,m=2$ | 54 address gates; four LPs, cap 15 s each | Feasible / exact rational SAT witness | 213 each; margin 1 |
| Cross-error moment audit | $k=2,m=3$, seven radii, all 1024 raw inputs, every mask marginal | Exact PASS | Every cross-character moment zero |
| Raw staircase implementation | $k=3,m=3$, $r=1,2,3$, seven radii, all 131072 raw inputs per circuit | Exact PASS | Gate score equals clipped formula in every case |
| Serialized approximate witness | $k=3,m=3$, $r=3,R=4$ | Exact PASS for reported agreement | 140 bottoms, 8823 errors / 131072 inputs |
| Generic builder / saved witness agreement | Entire serialized gate list and affine top | Exact PASS | Identical coefficients and thresholds |

Intermediate LP support counts are floating-point diagnostics; the best 92- and 213-bottom counts and margins were recomputed exactly from rational coefficients. There were **no UNSAT claims and no UNKNOWN/timeouts** in this round. Optimal LP objective status is not optimal gate support. Failure to beat an inherited count is not an impossibility result. All task-owned solver processes have finished; no old process was stopped or altered.

The cross-moment audit enumerates every mask for each character separately and expands the second moment under their independent product distribution exactly. This evaluates all terms of the joint average over 4096 mask collections without looping over the Cartesian product. Exact expected squared errors for radii $1,2,3,4,5,6,7$ are respectively

$$10993/256,\quad8425/256,\quad1225/64,\quad457/64,\quad553/256,\quad49/256,\quad0.$$

The saved $k=3,m=3,R=4$ circuit has exact agreement $122249/131072$. It is explicitly an **approximate** witness, not an exact ordinary-Andreev construction. At $R=8$ the audited fixed masks happen to give zero errors with 252 bottoms, far worse than the inherited 48. None of these small witnesses is used to infer the asymptotic theorem; that theorem follows from §4.

## 8. Failures, limitations, and one next lemma

The exact selector experiment produced valid but far too dense kernels; reweighting did not approach the inherited counts. It gives no evidence of an $O(Nm)$ family. Shared exact tail repair was not established. A mean-square estimate cannot be promoted to a worst-case score bound. Nor may one choose masks separately for each input: the mask selection quantifier is once per circuit.

The remaining exact target can now be stated with a quantitatively sharper base. Fix $t=N$ and $R=C\sqrt N$ at balance. The construction already has $O(N^{3/2})$ bottoms and constant mean-square relative error, without a union-bound logarithm. Let $E_z=P_*-P_z$. The next sufficient lemma is:

> Choose genuinely mixed diverse masks $z$ and a score $Q_z$, realizable by $o(N^2)$ additional raw-input bottom LTFs plus affine top terms, such that $|Q_z-E_z|<2N$ for every independent table and every raw address.

This would make $P_z+Q_z$ exact. The present proof only controls $\mathbb E E_z^2$, not the displayed supremum. The repair gates must be a single fixed family; input-dependent sparsity cannot reduce their count by itself. No claim that this lemma holds is made.

A separate, narrower follow-up is an efficient deterministic mask-selection algorithm preserving the proved mean-square bound; it is not required for the nonuniform gate upper bound.

## 9. Artifacts and reproduction

All files in `/tmp/andreev_gap/upper_astra_round2` are credited to Christian Reitwiessner. Nothing was committed, pushed, or written to the shared research archive.

- `construction.py`: reusable raw-input circuit builder and finite-theorem radius.
- `mean_square_proof.md`: early saved derivation; the complete final statement and mixed-mask refinement are in this report.
- `dictionary.py`, `dictionary_results.json`, `dictionary.log`: eight bounded LPs, exact rational witnesses, direction lists and timings.
- `verify.py`, `verification.json`, `verification.log`: exact integer cross moments, raw gate identities, all-input agreement counts, and exact dictionary cost/dominance checks.
- `fixed_mask_witness.json`: explicit 140-bottom approximate circuit, all raw weights and top data.
- `audit_saved.py`, `saved_audit.json`: separately load the serialized witness, compare it to the generic builder, and directly audit every raw input.

Reproduce with `OPENBLAS_NUM_THREADS=1 python3 /tmp/andreev_gap/upper_astra_round2/dictionary.py`, then `verify.py`, then `audit_saved.py`. NumPy/SciPy are imported from `/tmp/pydeps` when available; exact proof checks use integer arrays and `Fraction`, not floating tolerance. LP discovery is floating point; its selected witnesses are checked rationally. The expectation proof itself does not depend on an LP or an empirical success rate.
