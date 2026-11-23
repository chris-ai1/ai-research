# UP1 round 2: coupled tail corrections

Authors: Christian Reitwiessner

Date: 2026-11-11. Role: UP1. No additional subagents.

## Outcome

**No unrestricted exact exponent improvement was obtained.** The gap remains $\widetilde\Omega(n^{3/2})$ to $(5/16+o(1))n^2$.

[PROVED positive building block] A logarithmic-scale four-halfspace integral approximates the product of two bounded nonzero integer affine signs. It compiles a wide table guard into an exact classification repair, conditional on the ideal branch margin, using $\widetilde O(S_0+J+n(B/\mu)^2)$ raw gates. Here $J$ is the correction-bank size, $B$ its top variation, and $\mu$ its protected margin. Complete expansions and finite counts are in §2; no computed top score is fed to a bottom.

[PROVED obstruction to its intended use] Saturated middle-character tails force $B/\mu\ge2\sqrt{|T|m}=\Omega(\sqrt n)$ for **any** correcting raw-threshold representation, even with arbitrary table-only guards. Consequently this generic sampler still certifies only quadratic-or-worse repair cost (§4). The earlier hoped-for low-variation target is explicitly refuted, not left as an open route.

[PROVED architecture closure, using UP2's round-two theorem] Table-only guarding preserves bounded relative integer address weights and increases table-Walsh support only by the guard supports. Thus bounded/polylogarithmic Walsh coupling still forces exponent two (§3). Shared incidence-mask quadratic cancellations cost only $O(km)$, but low-degree corrections cannot repair spectral saturation (§1).

[VERIFIED] Exact integer/rational guardrails and a reproducible finite product-bank certificate passed. They verify the algebra and a conditional branch fixture; they are not asymptotic evidence. No shared paper edits, extra agents, package installs, or online posts were made.

[KNOWN, UP1 round one] Sparse-table lookup has a depth-two promise implementation; exact level guarding pays once per admitted integer layer. Wide Walsh tails include exponentially many central-weight tables. Character tables obstruct all top refits of the central-window library. Independent full-support equal-magnitude address directions face UP2's stronger exponential obstruction. These routes will not be repeated as new results.

## Working agenda

[CONJECTURE / research targets] Investigate shared corrections coupling two or more Walsh statistics; conditional cancellation identities that compile wide intervals without a detector-to-circuit handoff; and structured address supports or unequal weights. Every candidate must be expanded into raw affine thresholds with an honest all-input gate count. Multiscale decisions are paid for unless absorbed into one affine bottom gate. Small checks are guardrails, not asymptotic evidence.

## 1. Shared-mask algebra and a polynomial-repair barrier

### 1.1 Explicit coupled affine forms [PROVED]

Write $\xi_c=1-2x_c$, $X_S=\sum_c\chi_S(c)\xi_c$, and $M=km$. Assign raw variable $a_{ij}$ to an oriented label-cube edge $v_{ij}\to v_{ij}+e_i$. Repetitions are allowed. Let $d_c(a)$ be outflow minus inflow at vertex $c$ (each active raw bit contributes its value to its assigned edge). Define

$$D_S(a)=\frac12\sum_{ij}(\chi_S(v_{ij})-\chi_S(v_{ij}+e_i))a_{ij}
=\frac12\sum_c\chi_S(c)d_c(a).$$

Each coefficient is zero for $i\notin S$ and $\chi_S(v_{ij})\in\{\pm1\}$ for $i\in S$. Consequently $D_S\equiv t_S\pmod2$, including arbitrary mixed signs within active blocks. These are character-dependent supports, outside the full-support class excluded in round one. Walsh orthogonality gives exactly

$$\sum_S X_SD_S=\frac N2\sum_{ij}a_{ij}(\xi_{v_{ij}}-\xi_{v_{ij}+e_i}),\qquad
\sum_SD_S^2=\frac N4\sum_c d_c(a)^2.$$

Thus the table/address cross term consists of at most $2M$ raw products $a_{ij}x_c$, each one threshold $[a_{ij}+x_c\ge2]$, plus affine terms. If $\Delta_c$ is the incidence degree at $c$, then $d_c$ is an integer in an interval of length $\Delta_c$, and its square telescopes into at most $\Delta_c$ raw thresholds. Since $\sum_c\Delta_c=2M$, the second quadratic expression costs at most $2M$ gates as well. This latter bound is independent of maximum graph degree; no unproved bounded-divergence hypothesis is necessary. These identities are classical Walsh orthogonality applied to an explicitly chosen incidence map; no novelty priority is claimed.

For odd integer edge weights $w_{ij}$, replace $a_{ij}$ by $w_{ij}a_{ij}$. Parity is unchanged; the range bound becomes $2\sum_{ij}|w_{ij}|$. This gives unequal-magnitude variants, but does not give a free range reduction. Scaling odd weights upward only increases this elementary count.

[CONJECTURE / failed immediate use] Cheap global quadratic terms might permit truncated quadratic ridges to repair broad table tails. The ordinary full ladders remain quadratic because each individual form $X_S+D_S$ has the original table range. The following obstruction rules out the simplest nonlinear-ridge truncation plus polynomial-tail correction.

### 1.2 Low-degree corrections cannot cure spectral saturation [PROVED]

Let $T\ne\varnothing$ and $d=|T|m$. Consider any central-window library whose gates on the two tables $\xi=\pm\chi_T$ have address-independent table-pair differences. This includes the round-one $[X_S\pm D_{r,S}\ge\theta]$ library whenever its windows lie strictly between all attained negative and positive $T$-channel forms. Let a proposed score be an arbitrary linear combination of these gates plus **any** polynomial $R(x,a)$ of address degree at most $r<d$. Even granting this entire polynomial for free, no such score computes ordinary Andreev exactly.

**Proof.** Take the difference between the score on the two complementary tables. All gate differences are constant in $a$ by hypothesis. The polynomial difference still has address degree at most $r$. Exactness requires that this difference have strict sign equal to $\chi_T(b(a))$, up to a fixed global sign: one table's selected bit is one precisely when the other's is zero. In raw sign coordinates, the character is the degree-$d$ monomial on the selected blocks. Its uniform correlation with every address polynomial of degree less than $d$ is zero. Its correlation with a strict sign-correct score is instead nonzero with the fixed strict sign. Contradiction. Threshold ties do not matter, because the difference of a nonnegative positive-class score and a strictly negative negative-class score is strictly positive.

[REFUTED, specified route] In particular, every polynomial correction generated by the two quadratic identities above has $r\le2$ and cannot repair central clipping when $|T|m>2$. The conclusion allows all top coefficients and arbitrary dependence of $R$ on the table, so fitting quadratic coefficients anew does not evade it. The known exact construction retains full ladders and is unaffected. This is an architecture obstruction, not an unrestricted size bound, and extends the round-one affine-repair argument rather than claiming a new general parity theorem.

### 1.3 Substantive peer exchange

[PROVED CHECK / attribution] LOW1 answered the early tail request: flipping $h$ arbitrary entries of a character yields an arbitrary sparse signed Walsh sum; when $h=\Theta(N)$ the family has exponentially many members. Thus Parseval alone provides no cheap residual or guard. UP2 independently emphasized the triangular-domain requirement for one-threshold guards. I answered both and posted the exact incidence identities and polynomial-repair obstruction for attack. All communication is append-only in the round-two board.

## 2. A logarithmic-range compiler for approximate wide guards

This is a new derivation within this investigation, with no literature-priority claim. It is a positive depth-two building block, **not** an Andreev circuit. Its real limitation is its dependence on score variation divided by margin, rather than interval width.

### 2.1 Four raw thresholds give a sign-pure interaction [PROVED]

For $\lambda,t>0$ define

$$K_{\lambda,t}(u,v)=[u+\lambda v\ge t]+[-u-\lambda v\ge t]-[u-\lambda v\ge t]-[-u+\lambda v\ge t].$$

Because $t>0$, the first pair is $[|u+\lambda v|\ge t]$ and the second pair is $[|u-\lambda v|\ge t]$. If $u,v\ne0$, put $A=|u|$, $B=|v|$, $y=\operatorname{sgn}(uv)$. Then exactly, including threshold ties,

$$K_{\lambda,t}(u,v)=y[|A-\lambda B|<t\le A+\lambda B].$$

In particular $K\in\{0,y\}$. If $u,v$ are affine forms of raw inputs, every displayed indicator is one raw bottom threshold; there is no computed-feature handoff. Its direction is an unequal-scale combination of the two original affine directions.

A deterministic sign-only consequence: if $1\le A,B\le R$, taking $\lambda$ and $t$ over the powers of two with $-\lceil\log_2R\rceil\le\log_2\lambda\le\lceil\log_2R\rceil$ and $0\le\log_2t\le\lceil\log_2R\rceil$ gives a sum with strict sign $y$. Choose $\lambda$ so $A\le\lambda B<2A$, then a power $t$ in $[A,2A)$ satisfies $|A-\lambda B|<t\le A+\lambda B$. Thus $O(\log^2R)$ raw thresholds sign-compute the product of two nonzero affine signs. Its magnitude is not constant, so it cannot be substituted termwise into an arbitrary common top score. This observation by itself does not compile a real-valued interval guard.

### 2.2 A constant-amplitude integral [PROVED]

The exact identity is

$$\int_0^\infty\int_0^\infty K_{\lambda,t}(u,v)\frac{dt}{t}\frac{d\lambda}{\lambda}
=C\operatorname{sgn}(uv),\qquad
C=4\sum_{j=0}^\infty\frac1{(2j+1)^2}=\frac{\pi^2}{2}.$$

**Proof.** Since the integrand has a fixed sign, apply monotone integration to its absolute value. Integrating in $t$ gives $\log((A+\lambda B)/|A-\lambda B|)$ except at the single $\lambda=A/B$, a null set. Substitute $z=\lambda B/A$ and use $z\mapsto1/z$ above one to get

$$2\int_0^1\frac1z\log\frac{1+z}{1-z}\,dz
=4\sum_{j\ge0}(2j+1)^{-2}.$$

The series converges, justifying the improper integral. The proof and compiler need only $4\le C\le5$, which follows from $(2j+1)^2\ge4j(j+1)$ for $j\ge1$; the evaluation using $\pi$ is optional.

### 2.3 Uniform truncation and a finite raw gate bank [PROVED]

Let $R\ge1$ be an integer, $0<\epsilon\le1$, and $u,v\in\{-R,\ldots,-1,1,\ldots,R\}$. Set $\eta=\epsilon/40$ and restrict to the logarithmic rectangle

$$\eta/R\le\lambda\le R/\eta,\qquad \eta\le t\le2R^2/\eta.$$

The discarded integral has absolute value at most $10\eta$, uniformly in $u,v$.

To verify this, after $z=\lambda B/A$, the omitted lower $\lambda$ tail lies inside $z\le\eta$, and the upper tail lies inside $z\ge1/\eta$. On $0<z\le1/2$, $\log((1+z)/(1-z))\le3z$, so the two tails together cost at most $6\eta$. No $t$ above $2R^2/\eta$ can be active on the retained $\lambda$ interval. Removing $t<\eta$ affects only $|1-z|<e=\eta/A\le\eta$ and costs at most

$$\int_{1-e}^{1+e}\frac{\log(e/|1-z|)}z\,dz
\le\frac{2e}{1-e}\le4\eta.$$

This proves the claim; endpoints have measure zero.

Let

$$V=\log(R^2/\eta^2)\log(2R^2/\eta^2).$$

Draw $(\lambda,t)$ uniformly with respect to logarithmic area on that rectangle. For each fixed pair $(u,v)$, $K$ takes two values with range length one. Hoeffding's elementary bounded-variable bound and a union bound over the $4R^2$ input pairs show that there exist

$$Q=\left\lceil2V^2\epsilon^{-2}\log(16R^2)\right\rceil$$

samples such that the single fixed sum

$$P(u,v)=\frac{V}{CQ}\sum_{q=1}^QK_{\lambda_q,t_q}(u,v)$$

satisfies $|P(u,v)-\operatorname{sgn}(uv)|<\epsilon$ on every pair. Indeed, the normalized truncation bias is at most $10\eta/C\le\epsilon/16$. A sample-mean error at most $C\epsilon/(2V)$ has failure probability at most $2\exp(-QC^2\epsilon^2/(2V^2))$ per pair; the displayed conservative $Q$ makes the total less than one. Sampling is an existence proof for one deterministic fixed gate bank, not run-time randomness. The gate count is

$$4Q=O\bigl(\epsilon^{-2}\log^4(R/\epsilon)\log(2R)\bigr).$$

All coefficients may be arbitrary reals as allowed. Choosing a successful sample off every finitely many threshold-equality curve permits sufficiently close rational perturbations with identical gate truth tables; no uniform efficient sampler or short coefficient-bit guarantee is asserted.

### 2.4 Wide interval score guarding [PROVED conditional compiler]

For integer affine forms $L_1,L_2$ and integer thresholds $h_1,h_2$, put $u=2(L_1-h_1)+1$, $v=2(L_2-h_2)+1$. Then $g_1=[L_1\ge h_1]=(1+\operatorname{sgn}u)/2$ and similarly for $g_2$. If $|u|,|v|\le R$, the preceding bank gives

$$\widetilde{g_1g_2}=\frac{g_1+g_2}{2}+\frac{P(u,v)-1}{4},\qquad
|\widetilde{g_1g_2}-g_1g_2|<\epsilon/4.$$

This is a real top-linear score on at most $4Q+2$ raw gates. In particular the first predicate may be a wide tail $[U\ge h]$; the cost depends polylogarithmically on its range, not on the number of admitted layers. An interval is the difference of two such tails, at a factor-two cost/error adjustment.

Suppose $H_0,H_1$ are given scores and $G=[U\ge h]$ is an integer-affine guard. The desired branch score is

$$H_*=H_0+G(H_1-H_0).$$

Write $H_1-H_0=c+\sum_{j=1}^Jv_jg_j$, treating every raw affine top bit as a Boolean threshold feature, and put $B=|c|+\sum_j|v_j|$. If $H_*$ has strict signed margin at least $\mu>0$ on a specified set of inputs, replace each $Gg_j$ by its approximant with $\epsilon=\min\{1/2,\mu/B\}$. The $cG$ term is exact. The total score error is less than $\epsilon B/4\le\mu/4$, so correctness on that entire set is preserved. After choosing fixed samples, this is an exact classification guarantee. No sign of $H_0$ or $H_1$ is fed to a new bottom gate.

A safe gate count is

$$S_0+1+J(4Q+2)
=\widetilde O\bigl(S_0+J\max\{1,(B/\mu)^2\}\bigr),$$

where the suppressed logarithms are in $R$ and $B/\mu$. If both branches are correct on their designated regions, the compiled circuit is exact everywhere. If one branch is only an approximate circuit, this remains a hybrid guarantee on the set where the ideal branch score was already correct; it does not repair arbitrary exceptional inputs.

[CONJECTURE / potential exponent use] For polynomial $R$, a correction with $J=N^a$ and $B/\mu=N^b$ would compile at exponent $a+2b$, without an integer-layer factor. It is useful for the task only if that exponent is below two **and** the ideal branches cover all inputs. No such shared correction was constructed.

### 2.5 Why the inherited sparse/Fourier repair does not benefit [PROVED cost audit]

The norm $B$ is a property of the actual gate expansion, not merely of the numerical score. For the ordinary parity ladder on $M$ raw bits, the exact sign function has $M$ threshold jumps of magnitude two. Its written top variation is $\Theta(M)$, with unit margin. A character-product staircase can therefore have variation/margin polynomially large even if the represented function has small absolute magnitude. Replacing it by the sign-only dyadic gadget from §2.1 does not preserve its amplitude cancellations.

For a full Fourier score, the elementary $\varphi(X+t)-\varphi(t)$ representation has $\Theta(N)$ gates of typical coefficient magnitude $\Theta(N)$ per character at balance. Its written variation is $\Theta(N^3)$ across $\Theta(N)$ characters, while its exact margin is $N$: ratio $\Theta(N^2)$. The truncated radius-$W$ library has coefficient variation $O(NW^2)$, which at $W\asymp\sqrt N$ is $O(N^2)$; where it agrees with its exact score at margin $\Theta(N)$, the available generic ratio bound is only $O(N)$. These are audits of displayed representations, not lower bounds on every possible representation. Either way the new generic compiler's squared ratio is too expensive to establish a subquadratic hybrid from those scores. The sparse promise score's address ladders also have large variation; no small-variation replacement was proved.

Thus the integral construction removes the **range** bottleneck in approximate guarding and replaces it with an explicit **margin/variation** bottleneck. It must not be advertised as a width-independent exact zero-extension compiler or an unrestricted exponent improvement.

### 2.6 Sampling the whole correction removes a multiplicative bank factor [PROVED]

The per-feature compiler is not the best existence bound. Let the entire input have $n$ bits, retain the notation $H_1-H_0=c+\sum_{j=1}^Jv_jg_j$, and put $B'=\sum_j|v_j|>0$. Assume every gate score and the guard have an odd-integer affine encoding $v_j^{\rm aff}$ and $u$ with $1\le|u|,|v_j^{\rm aff}|\le R$. The superscript distinguishes the affine score from its top weight. Put $\epsilon=\min\{1/2,\mu/B'\}$ and use the rectangle of §2.3, of log area $V$.

Draw an index $j$ with probability $|v_j|/B'$, followed by one log-uniform $(\lambda,t)$ in that rectangle. Define the single sampled four-gate feature

$$Y=\operatorname{sgn}(v_j)K_{\lambda,t}(u,v_j^{\rm aff})\in[-1,1].$$

The exact Boolean product identity gives

$$H_*=H_0+\left(c+\tfrac12\sum_jv_j\right)G
+\tfrac12\sum_jv_jg_j-\tfrac14\sum_jv_j
+\tfrac14\sum_jv_j\operatorname{sgn}(u)\operatorname{sgn}(v_j^{\rm aff}).$$

Replace the last sum by $(B'V/(4CQ))\sum_{q=1}^QY_q$. Its expectation differs from the desired last sum by at most $10\eta B'/(4C)\le\mu/64$. Hoeffding with the range length two, followed by a union bound over at most $2^n$ raw inputs, shows that

$$Q=\left\lceil(n+2)(B'V/\mu)^2\right\rceil$$

samples suffice for one fixed realization with sampling error at most $\mu/2$ on every input. For example the required sample-mean tolerance is $2C\mu/(B'V)$; its failure probability is at most $2\exp(-2QC^2\mu^2/(B'V)^2)$ per input, much smaller than $2^{-n}$. If that tolerance exceeds the possible range, the event is automatic. The stated count is therefore conservative and valid in all cases. When $B'=0$, simply use $H_0+cG$ exactly.

The final score is an explicit linear combination of the original $H_0$ bank, the $g_j$ bank, the guard, and **four raw thresholds per sample**. Its total score error is strictly below $\mu$, preserving every protected sign. Thus the stronger count is

$$\boxed{S_{\rm guarded}\le S_0+J+1+4\left\lceil(n+2)(B'V/\mu)^2\right\rceil
=\widetilde O\bigl(S_0+J+n(B'/\mu)^2\bigr).}$$

Only logarithms in $R$ and $B'/\mu$ are suppressed. The statement assumes bounded integer affine scores (or explicitly supplied finite gaps and a corresponding count of attainable values); it is not a range guarantee for arbitrary unnormalized real scores. One fixed nonuniform gate bank works for every raw input. This is a conditional exact-classification compiler, not an exact real-valued zero extension.

[CONJECTURE / quantitatively sharpened target] For polynomial ranges and a candidate correction with $J=N^a$, $B'/\mu=N^b$, and $n=\Theta(N)$, the gate exponent becomes $\max\{a,1+2b\}$. A genuinely global branch repair with $a<2$ and $b<1/2$ would therefore be sufficient to change the unrestricted exponent. No such low-variation correction was found; the existing staircase banks are far above this variation threshold.

## 3. A peer theorem closes the bounded-coupling branch of this mission

### 3.1 Character-slab charging [PROVED by round-two UP2; checked here]

Let $r_j$ be the number of nonconstant Walsh coefficients in bottom gate $j$'s **table normal**. UP2 derived

$$\sum_jr_j\ge\frac12\sum_{T\ne\varnothing}\operatorname{slice}(m|T|).$$

The proof is direct and was checked independently by LOW1, LOW2 and me on the board. Compare complementary character tables $x_c^\pm=(1\pm\chi_T(c))/2$. Gate $j$ cancels unless its table normal has nonzero $T$-coefficient. Raw address top terms cancel and raw table terms give only a constant. The common score difference strictly sign-represents parity on the $m|T|$ selected raw address bits. Each noncancelled gate gives at most two boundary halfspaces, and every parity edge must be sliced. Summing this necessary inequality over $T$ gives the displayed charge.

[KNOWN downstream geometric theorem, attribution preserved] The bounded-integer slicing estimate $\operatorname{slice}_C(d)\ge d/(4C)$ is the Sauermann–Xu corollary used in the supplied round-one reports. If each address normal can individually be rescaled to integer entries in $[-C,C]$, then

$$\sum_jr_j\ge\frac{m}{8C}\sum_T|T|=\frac{kmN}{16C}.$$

Thus $r_j\le r$ gives $S\ge kmN/(16Cr)$. For fixed or polylogarithmic $r,C$, the balanced exponent is two. No stronger slicing theorem or unrestricted exponent is asserted. The underlying new reduction and the matching two-scale upper family are UP2's work, not mine.

[PROVED refinement by LOW1; checked here] One may instead charge $r_j^{\rm sem}$, the number of character-table pairs where a gate's difference is **nonconstant in the raw address**. All constant differences can be absorbed in the top constant on the selected cube. This is at most $r_j$ and is stable under perturbations preserving the gate's Boolean truth table. Pure-table gates have semantic charge zero, irrespective of written Walsh support.

### 3.2 Closure of table-only guards [PROVED corollary / application]

Suppose the initial address-dependent bottom bank has table-Walsh support at most $r_0$ per gate, and rescalable address bound $C$. Apply exact integer-layer guards, or the approximate guard compiler of §2, using table-only affine guard forms. Along any resulting bottom's construction path, suppose the union of guard Walsh supports has size at most $q$.

Every resulting address-dependent threshold still has address normal proportional to ONE original address normal. For example a sampled product gate has form $[\pm U\pm\lambda V\ge t]$, where $U$ is table-only and $V$ is an original affine gate score. Its address normal is $\pm\lambda$ times the original. Its table-Walsh support lies in the union of the original and guard supports. The same holds for $[B(U-r)+V\ge0]$ in the exact compiler. Repeating this observation gives $r_j\le r_0+q$ and the same $C$, after rescaling. Additive combination of scores changes no bottom normal.

Guarded raw **address** bits obey the same conclusion, starting with a single-coordinate address normal and no table support. Guarded raw **table** terms yield pure-table gates and therefore have semantic charge zero; arbitrary unguarded affine top terms are already allowed in the charging proof. This handles the direct-input terms rather than silently assuming them away.

Consequently an exact ordinary-Andreev circuit obtained by this route must satisfy

$$\boxed{S\ge\frac{kmN}{16C(r_0+q)}}$$

for $r_0+q>0$ and $C\ge1$, counting all bottoms as a safe upper count on contributing bottoms. For zero coupling the charge inequality itself rules out computation. Hence a fixed/polylogarithmic number of jointly used Walsh table statistics, followed by any such table-only guarding and top refitting, cannot change exponent two if address integer ratios stay bounded/polylogarithmic.

This is a meaningful obstruction to the assigned wide-tail strategy. Arbitrarily real mixing coefficients in the table guard **do not** by themselves create unequal relative address weights. The same is true even if exponentially wide guard intervals could be handled cheaply. It does not rule out gates coupling polynomially many Walsh coefficients, semantically new generic table rows, or address forms with growing/incommensurate relative magnitudes. A harmless generic perturbation escapes written sparsity but not LOW1's semantic charge.

### 3.3 What the other round-two upper identity establishes

[PROVED by UP2, checked from its displayed raw identity] Assign magnitudes $1$ to all raw bits in character $T$ and $2$ to all other raw bits, with arbitrary signs. The resulting full-support affine count $L_T$ has $(-1)^{L_T}=\chi_T(b)$. The common score

$$X_\varnothing+\sum_{T\ne\varnothing}\bigl(\varphi(X_T+L_T)-\varphi(L_T)\bigr)=N(1-2x_b)$$

is exact and costs $O(n^2)$ full ladders. This illustrates a real escape from round-one full-support/equal-magnitude impossibility, but the character-slab theorem pins its bounded-table-coupling/bounded-address-integer class to exponent two. LOW2 further observed that odd/even consecutive scales yield arbitrarily close fixed magnitude ratios at quadratic size. Thus neither near equality nor full support alone is a valid obstruction; the exact algebraic/support hypotheses matter.

## 4. A norm barrier blocks the new compiler on the actual character tails

This section supersedes the optimistic low-variation target in §§2.4 and 2.6 **for saturated character-tail repair**. The compiler theorems remain correct; their hoped-for application fails for a structural reason, not merely because the displayed Fourier representation is inefficient.

### 4.1 Unate parity correlation [PROVED, elementary standard Fourier argument]

For any Boolean unate function $g$ of $d$ independent raw bits,

$$|\widehat g([d])|\le\frac1{2\sqrt d}.$$

In particular this holds for every threshold with arbitrary real weights. Input complements make $g$ monotone increasing in sign coordinates $z_i\in\{\pm1\}$ and do not change the absolute target Fourier coefficient. Let $I_i=\Pr(g(z)\ne g(z^{\oplus i}))$. The discrete derivative is nonnegative, takes values $0$ and $1/2$, and has expectation $I_i/2$. Expressing the top-degree Fourier coefficient using this derivative gives $2|\widehat g([d])|\le I_i$ for every $i$. Monotonicity also gives $I_i=2\widehat g(\{i\})$. Hence Cauchy–Schwarz and Parseval imply

$$\sum_i I_i=2\sum_i\widehat g(\{i\})
\le2\sqrt{d\sum_i\widehat g(\{i\})^2}
\le2\sqrt{d\operatorname{Var}(g)}\le\sqrt d.$$

Sum the first inequality over $i$ and divide by $2d$. Conditioning on any ignored raw variables and averaging proves the same bound for correlation with a parity on any selected $d$ coordinates of a larger threshold gate. This uses only unateness, not bounded or comparable weights, nor a common sign orientation across gates. No new literature-priority claim is made for this basic influence argument.

### 4.2 Consequence for any norm-based guarded correction [PROVED]

Choose complementary character tables $x^\pm_c=(1\pm\chi_T(c))/2$, and put $d=|T|m\ge2$. Let $y\in\{\pm1\}$ select these two tables, independently of uniformly random raw addresses, and orient the target sign as $f=y\chi_T(b)$. Suppose the base score $H_0$ has address-constant difference between these two tables, as the saturated central-window library does. Then $\mathbb E[fH_0]=0$. The same conclusion holds if a free polynomial address correction of degree less than $d$ was already added.

Permit the repair even more freedom than the compiler: arbitrary Boolean **table-only** guards $G_j(x)$, not necessarily affine threshold guards. Write its non-affine raw-threshold part as $\sum_jv_jG_j(x)g_j(x,a)$, with arbitrary table/affine terms allowed as well. On either fixed table, $G_j$ is a constant in $\{0,1\}$. By §4.1,

$$|\mathbb E[fG_jg_j]|\le\frac1{2\sqrt d}.$$

All table-only terms and guarded raw affine address terms have zero correlation for $d\ge2$. If the corrected score has strict target margin at least $\mu$ on every input from these two tables, then

$$\mu\le\mathbb E[fH_*]
\le\frac{\sum_j|v_j|}{2\sqrt d}.$$

Therefore the actual correcting threshold variation obeys

$$\boxed{B/\mu\ge2\sqrt d.}$$

The statement does not assume independent errors, finite top weights, random masks, or a particular correction formula. It permits arbitrary real table and address directions. It is a variation/margin lower bound, **not a gate lower bound**; huge weights are allowed in the task, and are fully consistent with it.

For middle characters $|T|\asymp k$, $d=\Theta(n)$ at balance. The generic whole-correction compiler of §2.6 then has certified resource $n(B/\mu)^2=\Omega(n^2)$ before logarithms. Thus this particular sampling proof cannot establish a subquadratic repair of the saturated character tails, even with a more efficient representation of the correcting score. An optimized deterministic common-amplitude identity may cost less than this generic upper bound; the norm argument does not rule that out. Nor does it apply to a base bank which already has nonzero useful correlation on every character tail.

[REFUTED target, corrected explicitly] The proposal to find $B/\mu=N^b$ with $b<1/2$ while repairing a saturated middle-character pair is impossible. This corrects the exploratory target posted before deriving §4.1. The broader conditional compiler remains a valid tool for other branch problems or corrections to a different base bank.

## 5. Exact checks, board exchanges, and next step

### 5.1 Reproducibility [VERIFIED]

Run only the standard-library script:

```bash
python3 -I /tmp/andreev_gap/swarm_round2/up1/checks.py
```

It writes `checks.json` and the exact rational finite bank `product_bank.json`. Counts:

- 18,792 exhaustive table/address incidence identities with signed odd edge weights, including raw Boolean-product expansions;
- 2,197 exact signed-square staircase expansions;
- 8,728 four-threshold kernel identities, including equality endpoints;
- 5,564 dyadic sign-product inputs (the unsigned witness count ranges from 1 to 16, demonstrating why sign correctness does not mean constant amplitude);
- 246 exact low-degree parity orthogonalities;
- 3,935 arbitrary-weight threshold cases verifying both influence inequalities and $4d\widehat g([d])^2\le1$;
- every one of the 256 signed integer pairs with $1\le|u|,|v|\le8$ for a fixed bank of 8,192 four-threshold kernels. The absolute kernel sums range from 189 to 247, so the **rational** normalization $1/218$ has exact uniform product error $29/218<1/4$;
- all 256 raw inputs of an artificial two-branch classification fixture using that same bank. Its ideal margin is one, every compiled sign is correct, and the maximum exact score error is $29/218$.

The product bank uses 32,768 raw thresholds before merging; it is deliberately a proof-of-algebra guardrail, not a competitive small circuit. Floating logarithms choose candidate coefficients, which are immediately rounded to rational values with denominator $2^{30}$. Every saved gate evaluation, top normalization, error bound and branch check is then exact integer/rational arithmetic. The all-size existence proof is §2, independent of this finite search. No numeric integration is used to certify the theorem.

### 5.2 Substantive peer exchanges and attribution

[PROVED CHECKS / credited peer work] I posted the wide-tail question immediately, then the shared incidence-mask identities, the polynomial-repair obstruction, and the logarithmic product integral before finishing their audits. LOW1 answered with the arbitrary character-flip residual family, ruling out an inference from Parseval to cheap residuals. UP2 emphasized the triangular-domain limitation of one-threshold guards. I answered both and kept exact score composition costs explicit.

LOW1 and LOW2 independently checked the product kernel and the convergent logarithmic integral. LOW1 supplied the same dyadic sign-only covering observation independently; its point was that the magnitude still varies. LOW2 stressed that arbitrary real affine scores need an explicit minimum gap: the written compiler accordingly assumes integer scores with a stated range. Neither peer endorsed an unrestricted circuit or a width-free exact real-valued product.

UP2's new character-slab charging theorem directly attacked my few-statistic scheme. I checked its cancellation and edge accounting, incorporated it with explicit attribution, and sent back the closure observation: table-only guards leave each address direction proportional to its original, so arbitrary real mixing coefficients in that compiler do not evade bounded relative address weights. LOW1's semantic incidence refinement handles harmless dense perturbations. UP2's genuine two-scale common-top construction and LOW2's near-equality refinements prevent overextending round one's exponential theorem to unequal magnitudes.

I subsequently attacked my own small-variation application using the elementary unate parity-correlation bound. The board and this report explicitly supersede the earlier proposed $b<1/2$ target for saturated character tails. The conditional compiler remains valid, but no exponent gain is claimed from it.

### 5.3 Dead ends and the single most promising next step

[REFUTED specified routes]

1. Shared quadratic identities plus central clipping: complementary character-table differences remain below the required address degree, even if all resulting polynomial corrections are free.
2. Coupling only fixed/polylogarithmically many Walsh table statistics with bounded relative integer address weights: UP2's character-slab charge forces exponent two, and both guard compilers preserve this class.
3. Logarithmic-range approximate guarding followed by norm-based sampling of a correction for a saturated middle character: its required variation/margin is at least $\Omega(\sqrt n)$, restoring quadratic certified cost. Exact signs of individual product gadgets cannot replace common amplitudes.
4. Treating broad Walsh tails as sparse-table promises: LOW1's arbitrary-flip residual family still contains exponentially many central-weight tables, and there is no free detector-to-score composition.

[CONJECTURE / single next step] Seek a **deterministic common-amplitude correction identity using semantically dense table-Walsh normals**, with structured unequal address directions, that already resolves complementary middle-character tables. The proposed search should impose those character-pair parity differences exactly, not begin with a central-window base that has zero information there and hope for small-norm sampling to recover it. The concrete missing object is a raw affine threshold bank that shares amplitude reconstruction across many character channels while avoiding the bounded-Walsh charging class; independent sign feasibility or high pair coverage is insufficient. The integral kernel is a valid local tool, but the norm barrier shows that generic concentration is not the mechanism that will finish this task.

All new artifacts credit Christian Reitwiessner. Prior Walsh/influence methods, the inherited slicing bound, and the separate agents' new reductions retain attribution. No novelty priority, Lean formalization, or new unrestricted upper/lower exponent is asserted.

### Final peer-audit addendum

[PROVED CHECK, attributed to UP2] Before handoff, UP2 independently checked §4's influence proof, its extension by conditioning ignored bits, and the table-only guard argument. It endorsed the square-root variation/margin obstruction with the same scope: it defeats the desired norm budget for the sampler, not unrestricted top cancellation or arbitrary circuit size. UP2's report also records a stronger few-mask real-two-scale hybrid obstruction; that further supports requiring address directions beyond a bounded family of such masks in the next upper-bound search. I have not claimed a separate independent audit of that entire new hybrid theorem.
