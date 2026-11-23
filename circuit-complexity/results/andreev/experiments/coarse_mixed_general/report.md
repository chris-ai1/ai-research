<!-- Copyright (c) 2026 Christian Reitwiessner. -->
Authors: Christian Reitwiessner

# Mixed-mask coarse Fourier: exact localized products and the cancellation bottleneck

## Outcome and scope

**No $o(n^2)$ ordinary-Andreev family was obtained.** This bounded constructive attempt produced an exact, genuinely mixed-sign **windowed coarse-product gadget**, an exact example where different masks and different window widths cancel arrangement dependence, and a precise obstruction to using a single middle layer for that cancellation. These concern a proposed replacement mechanism, not a global impossibility theorem.

The useful distinction from simply changing signs in a full ladder is localization: a window costs its number of retained integer layers plus two endpoints, independently of the full address range. Its contribution vanishes identically outside the window. Thus there is no uncancelled linear tail. The remaining problem is to combine sufficiently few windows **across Fourier characters**, or obtain a sign-only reconstruction tolerating nonuniform coverage. Neither was solved here.

All results use raw, independent table bits. No generator restriction, fixed-$k$ asymptotic claim, coherent extension presented as mixed progress, subagents, Lean, or online posting was used. Everything created is in this directory. Other work and processes were preserved; no jobs remain from this attempt.

## 1. Exact mixed-sign localized coarse product [proved]

Fix a nonempty character $S$ and flatten its active address blocks into $a\in\{0,1\}^M$, $M=|S|m$. For a mask $z\in\{0,1\}^M$, put
$$
L_z(a)=|a\oplus z|=|z|+\sum_j(1-2z_j)a_j,
\qquad \chi(a)=(-1)^{|a|}=\chi_S(b).
$$
Let $h(x)$ be an integer linear form in the actual table bits, $H=[h\ge r]$, $q=2H-1$, and choose integer $B$ such that $|h(x)-r|<B$ everywhere. For example, the original Walsh form has $|h|\le N/2$, so $B=N/2+2$ suffices for $r=0,1$.

For an integer interval $I=[p,u]\subseteq[0,M]$, define actual bottom LTFs
$$
g_{z,\ell}=[BL_z+h\ge B\ell+r],\qquad
E_{z,\ell}=[L_z\ge\ell].
$$
Then the following identity holds exactly:
$$
\boxed{
\chi(a)q(x)[p\le L_z(a)\le u]
=(-1)^{|z|}\left(
2\sum_{\ell=p}^u(-1)^\ell g_{z,\ell}
-(-1)^pE_{z,p}-(-1)^uE_{z,u+1}
\right).}
$$
**Proof.** The range condition implies
$$
g_{z,\ell}=H[L_z=\ell]+[L_z\ge\ell+1].
$$
Therefore $q[L_z=\ell]=2g_{z,\ell}-E_{z,\ell}-E_{z,\ell+1}$. Alternating summation cancels all interior endpoint gates; multiplying by $(-1)^{|z|}$ gives the box.

**Weights and count.** Each data gate has address weights $B(1-2z_j)$, the original raw-table weights of $h$, and cutoff $B(\ell-|z|)+r$. Each endpoint has address weights $1-2z_j$, zero table weights, and cutoff $\ell-|z|$. Top coefficients are displayed explicitly. This costs at most
$$
(u-p+1)+2
$$
bottoms. Constant endpoints can be absorbed into the top threshold. Endpoints can also be shared across amplitudes with the same mask and window. If this is the entire score, one adds one top gate; it is normally a component of a larger top score.

If $z$ is nonconstant **inside every active block**, every gate here mixes positive and negative address weights inside every such block. Choosing distinct, noncomplementary masks gives distinct views; the construction is not one common input relabeling. No precomputed $H$ is being supplied to these gates.

This trades a long exact product for a short **localized** exact product. It does not by itself produce the unlocalized product.

## 2. The precise pooling problem

For a fixed amplitude, combine windows with arbitrary real coefficients $\mu_{z,I}$, giving
$$
\chi(a)q(x)W(a),\qquad
W(a)=\sum_{z,I}\mu_{z,I}[L_z(a)\in I].
$$
Constant coverage $W\equiv1$ reconstructs the exact product. Different masks can cancel arrangement dependence through this equation. The unmerged bottom cost is at most $\sum_{\mu_{z,I}\ne0}(|I|+2)$, followed by one shared top for an entire construction. The weights' magnitudes do not enter this count.

A desirable replacement would solve this equation very cheaply, or avoid reconstructing each amplitude separately. For independent full ladders the leading cost remains
$$
\frac m2\sum_{S\ne\varnothing}|S|=\frac{mkN}{4}.
$$
At $km=N$, this is $N^2/4=n^2/16$ already for one full ladder per character, before other costs. Changing masks leaves that range sum intact. The localized identity changes this architecture only if its coverage/cancellation cost can be controlled.

For integral balanced instances take $k$ along powers of two; rounding $m=\lfloor N/k\rfloor$ gives the same asymptotic calculation for general growing $k$.

## 3. Single-middle-layer cancellation is exponentially expensive [proved]

Let $M$ be even and $f(a)=[|a|=M/2]$. Suppose
$$
\sum_z\mu_z f(a\oplus z)=1\quad\text{for every }a.
$$
Coefficients may have either sign. For a Boolean character of degree $d$, the unnormalized Fourier coefficient of $f$ is
$$
\lambda_d=\sum_j(-1)^j\binom dj\binom{M-d}{M/2-j}.
$$
Odd degrees vanish by complement symmetry. For $d=2j$,
$$
\lambda_{2j}=(-1)^j\binom{M}{M/2}
\frac{\binom{M/2}{j}}{\binom{M}{2j}}\ne0.
$$
The convolution equation forces every nonconstant even-degree Fourier coefficient of $\mu$ to vanish. Consequently
$$
\mu(z)+\mu(\bar z)=\frac{2}{\binom{M}{M/2}}
$$
for every complementary pair. At least one member of each of the $2^{M-1}$ pairs has nonzero coefficient. This bound is sharp: choose one representative from every complementary pair, all with weight $2/\binom{M}{M/2}$.

There is a useful relaxation. Allow a freely available table-only $q$ correction at the top, so that it suffices to have
$$
W(a)=1+c\chi(a).
$$
Now even Fourier degrees other than $0,M$ must vanish. Thus $\mu(z)+\mu(\bar z)=A+C(-1)^{|z|}$ with $A\ne0$. At least one parity class has a nonzero pair sum, requiring at least $2^{M-2}$ masks. This support bound is also sharp when arbitrary masks are permitted: retain one representative per complement pair in one parity class and scale appropriately.

If at least two active blocks have length at least two, a pool consisting **only** of masks mixed inside every active block cannot satisfy even this relaxed equation. There are forbidden complementary pairs in both total-mask parity classes: fix one block uniformly zero and vary another block's parity. The two forbidden pair sums force $A+C=A-C=0$, contradicting $A\ne0$.

**Scope.** This is an exact-product obstruction for translates of one specified kernel. It is not a lower bound for arbitrary mixed THR∘THR, joint nonlinear Fourier reconstruction, sign-only reconstruction, asymmetric windows, varying widths, or a pool with extra gate types. It also does not cover odd $M$ by this proof. In balanced even-block subsequences it already excludes this particular middle-layer shortcut for the relevant characters.

## 4. Varying widths really can cancel mixed-mask fluctuations [exact witness]

The preceding obstruction does not persist unchanged when widths vary. On two four-bit blocks, let
$$
Z=\{z\in\{0,1\}^8:|z_{1:4}|,|z_{5:8}|\in\{1,3\}\}.
$$
There are 64 masks, each genuinely mixed inside both blocks. For **every** raw address $a\in\{0,1\}^8$,
$$
\boxed{\sum_{z\in Z}\left(
3[L_z=4]+4[3\le L_z\le5]+21[1\le L_z\le7]
\right)=1568.}
$$
This is checked on all 256 addresses using integers in `central_windows.py`. It was discovered by a symmetry-reduced LP, then reduced to the displayed integer identity. Together with §1 it reconstructs $\chi_{\{1,2\}}(b)(2[h\ge r]-1)$ exactly, using varying masks and widths. Cancellation holds for every arrangement, not only block counts.

For a fully explicit instance take $h=x_0-x_1+x_2-x_3$, $r=0$, $B=4$. `symmetric_witness.json` contains actual raw-table/raw-address bottom weights and rational top weights. Choosing one mask per complementary pair and doubling the coefficients gives 544 unmerged bottoms; merging proportional identical LTFs and cancelling zero top weights leaves **416 bottoms, 417 including a top**. All 4096 table/address inputs pass exact rational equality checks.

This is a successful cancellation **subproblem**, not a finite gate improvement or an ordinary-Andreev upper bound. It is far more expensive than an independent full product ladder. Its significance is that a mixed-only positive pooling identity exists once widths vary; a global noncancellation claim would be false. No economical scalable extension of this identity was found.

The unrestricted nonnegative covering LP for this same $(4,4)$ subproblem also produced a rationally verified 48-window solution with 264 unmerged bottoms. It has less transparent coefficients, saved in `cover_results.json`; it is not an improved ordinary-Andreev circuit. The corresponding $(3,3)$, $(2,2,2)$ and $(2,2,2,2)$ pools returned floating-point infeasible statuses. These statuses are search diagnostics, **not certified impossibility results**.

## 5. Wider-window diagnostics and the remaining constructive target

For a symmetric window $[M/2-w,M/2+w]$, the same Fourier test uses
$$
\lambda_d=\sum_{t=M/2-w}^{M/2+w}\sum_j(-1)^j\binom dj\binom{M-d}{t-j}.
$$
If all nonzero even degrees have nonzero eigenvalue, the same $2^{M-1}$ support bound holds for constant coverage by translates of that **one** window. The exact scan covers the listed even $M\le64$ and radii $0,1,2,3$ where proper. There are genuine spectral holes: at $M=10$, radius one vanishes at degree eight, and radius two vanishes at degree four. Thus extrapolating the single-layer argument to every fixed width would be wrong. See `exact_results.json` for the finite scan; no asymptotic conclusion is inferred from it.

The best subproblem reached is therefore: **an exact localized coarse amplitude with mixed weights, plus a real mixed-mask cancellation identity using several widths, but no gate-efficient pooling or sharing across characters.** To reach the requested bound, the next construction must reduce the total support/layer cost across growing-$k$ characters, or use table-dependent sign margins without requiring exact amplitude reconstruction. Simply repeating the $(4,4)$ identity per character would make costs worse. The previous $k=3$ coarse certificate remains coherent and is not promoted to an admissible extension here.

## 6. Artifacts and reproduction

- `central_windows.py`: standard-library exact identity checks, integer spectral calculations, and the simple mixed-only cover certificate. `exact_checks.log` and `exact_results.json` record 24,576 window evaluations plus the independent spectral and cover checks.
- `cover_search.py`: bounded LP discovery with exact `Fraction` checking of successful covers; `cover_results.json`, `cover_checks.log`.
- `symmetric_cover.py`: small symmetry-reduced LP discovery, actual gate construction, and 4096 exact rational checks; `symmetric_witness.json`, `symmetric_checks.log`.

Run each script with `python3 /tmp/andreev_gap/coarse_mixed_general/<script>.py`. The two discovery scripts load installed NumPy/SciPy from `/tmp/pydeps`; the main integer certificates require only the standard library. New files carry Christian Reitwiessner authorship. No unbounded solver jobs were started.
