Authors: Christian Reitwiessner

# LOW2 round three: analytic duals and signed path reductions

Status: completed research handoff. Model: exact ordinary THR o THR for Andreev lookup, arbitrary real bottom and top weights, and raw inputs at the top. $N=2^k$, $k$ parity blocks of length $m$, $M=km=\Theta(N)$, $n=N+M$.

## Outcome

**[PROVED, restricted-class result]** A connected graph on the address blocks gives an analytic nonnegative oriented-rectangle dual for heterogeneous two-scale/support-dependent address profiles with arbitrary dense signed table normals. With at most $R$ sign masks per unordered block profile, it forces

$$G=\Omega\!\left(\frac{n^2}{R\log^3 n}\right)$$

at balance when $R^2\le(m-O(\log^2 n))/2$. Magnitude ratios may be arbitrary real numbers, including irrational ratios and one zero level. Pure-address and pure-table helpers are unrestricted. For fixed or polylogarithmic $R$, the exponent is two; for $R\le n^\eta$, fixed $\eta<1/2$, the lower exponent is $2-\eta$. The full proof is §§2–3; §3.5 gives the strongest finite constants and semantic version. The inherited quadratic two-scale construction matches exponent two.

The graph mechanism is LOW2's contribution. UP2 independently supplied the same two-baseline refinement; UP1's inherited common-reorientation lemma and our independently derived bridge-occupation calculation reduce the mask loss from $2^R$ to $R$. LOW1 then extended the graph mechanism to arbitrary masks at bounded integer block magnitudes; that separate theorem is credited in §4.5. All peers exchanged substantive proof checks and corrections.

**[UNRESOLVED]** No unrestricted exponent improvement. General within-block magnitude variation and unrestricted sign-mask diversity with arbitrary incommensurable scales remain outside the new bound. No paper edit or additional subagent was used.

## Exactness constraints to preserve

[KNOWN, common brief and prior reports] Every table and every raw address, including rare extreme block weights, must be correct. Character tables restrict the function to parity on the corresponding blocks; the all-block character gives parity on all $M$ raw address bits. Arbitrarily tiny positive margins are allowed, and the sum of absolute top weights is unbounded. No average-case, bounded-margin, positive-path, owner-dominance, or survivor-only premise can be inferred.

## Initial plan, now completed

Read all round-one and round-two reports, the round-two board, paper and research state. Seek a scalable Fourier/oriented-rectangle dual for heterogeneous normals with semantic dense table activity, or a rigorous broad obstruction. Test signed reductions without controlling negative top contributions. Publish and exchange candidates on the round-three board. No claim of an unrestricted exponent improvement at this stage.

## 1. Address-profile isolation candidate

[INITIAL CONJECTURE, superseded by the proved theorems in §§2–3] A connected bipartite spanning tree on a middle character division $T,T^c$ should isolate its unordered two-scale address profile even when all table normals have dense Walsh coupling. Retain $r$ disjoint selected/ignored pairs per tree edge. Every other profile has equal magnitudes across at least one edge, hence survives random literal identification on all those pairs with probability at most $2^{-r}$. A union bound annihilates all nonmatching profiles.

For the matching profile, a bounded number of masks and bounded magnitude ratio permit a common baseline sweep making all its gates constant when its gate count is too small. This charges the exceptional gates before using parity orthogonality, respecting the one-survivor counterexample. A putative bound is $E_{\{T,T^c\}}=\Omega(m/(2^R k\Lambda\log S))$, hence $S=\widetilde\Omega(n^2)$ at balance for fixed $R,\Lambda$.

This is a candidate new class, not an unrestricted exponent. Full proof, support-zero handling, raw-top handling and finite checks remain to be supplied. The paired restriction originates in UP2 round one; baseline sweeping in UP2 round two. The proposed new ingredient is graph-based isolation by address profile, replacing sparse table-Walsh coupling.

## 2. A dense-table, heterogeneous two-scale profile theorem

### 2.1 Exact model and finite statement [PROVED, full proof below]

Let $G$ be the number of bottom gates reading both table and address inputs. Arbitrarily many additional pure-table gates and arbitrary pure-address gates are allowed. Every address normal of a gate counted in $G$ is either:

1. **Uniform magnitude:** a full-support row $c_j\sigma_j$, $c_j>0$, with arbitrary sign mask $\sigma_j\in\{\pm1\}^{M}$; or
2. **Two blockwise magnitudes:** for a nontrivial unordered block partition $P=\{U,U^c\}$, magnitudes $a_j,b_j\ge0$ with $a_j\ne b_j$ and $a_j+b_j>0$, and a sign mask $\sigma_j$,
   $$\gamma_{j,i,l}=\sigma_{j,i,l}\begin{cases}a_j&i\in U,\\b_j&i\notin U.\end{cases}$$

The partition, magnitudes, thresholds, and table normal may vary from gate to gate. For each unordered partition $P$, all its gates draw their masks from a fixed family of at most $R$ masks, where $R\ge1$. The families may differ arbitrarily between partitions. When a magnitude is zero, signs on those coordinates can be completed arbitrarily to a mask; the hypothesis asks that some such completions fit the family. There is **no bound** on the ratio of the two nonzero magnitudes; they may be irrational, or one may be zero. Uniform-magnitude gates have no mask cap. Every table coefficient, top coefficient, and raw top coefficient is unrestricted real.

Write $E_P$ for the number of gates of the second type assigned to $P$. This assignment is unique for unequal magnitudes, apart from swapping the two sides. Define

$$r=\max\{2,\lceil\log_2(G+1)\rceil\},\qquad L=(k-1)r,$$
$$D=\left\lceil\frac{m-(k-1)r}{2^R}\right\rceil,\qquad B=2L+1.$$

Assume $k\ge2$ and $m\ge(k-1)r$. Then every exact circuit satisfies, for **every** nontrivial unordered partition $P$,

$$\boxed{2E_P B\ge D+1.}\tag{2.1}$$

Consequently

$$\boxed{G\ge\left(\frac N2-1\right)\frac{D+1}{2\bigl(2(k-1)r+1\bigr)}.}\tag{2.2}$$

This is an analytic exact-dual theorem for a new specified class in this investigation, not an unrestricted bound. Its building blocks are UP2's round-one paired cancellation and round-two baseline sweep; the additional mechanism is a connected block graph isolating an address profile, **without imposing any table-Walsh sparsity or semantic incidence cap**. UP2 independently proposed the two-baseline refinement removing all ratio/support restrictions after my own board entry, and its contribution and audit are credited. UP1 flagged explicitly that unrestricted pure-address helpers require the complementary-table version stated here. No literature-priority claim is made.

### 2.2 Proof: graph isolation, two-dimensional baseline, and exact dual [PROVED]

Fix $P=\{T,T^c\}$ with both sides nonempty. Compare the two tables

$$x_c^\pm=\frac{1\pm\chi_T(c)}2.$$

The actual top-score difference $F(x^+,a)-F(x^-,a)$ has strict sign equal to parity on the raw address bits in blocks $T$. Every pure-address feature and raw address top term cancels, while table-only features contribute constants. This is a rare exact input family. No uniform-distribution correctness premise is substituted.

**A connected block graph.** Choose any spanning tree $\mathcal T$ of the complete bipartite graph between $T$ and $T^c$. It has $k-1$ edges and maximum degree at most $k-1$. For each edge retain $r$ disjoint raw-coordinate pairs, one coordinate in its selected endpoint block and one in its ignored endpoint block. No raw coordinate is reused. This is possible because every block needs at most $(k-1)r\le m$ live coordinates. There are $L=(k-1)r$ selected coordinates $z_1,\ldots,z_L$ and $L$ ignored coordinates $w_1,\ldots,w_L$, with each pair associated to one edge. Coordinates are initially independent; literal identification is postponed.

**Two baseline sweeps.** Pick one block $i_*\in T$ and one $j_*\in T^c$. At least $m-(k-1)r$ unused coordinates remain in each. Partition the unused coordinates of each chosen block by their sign vectors across the at most $R$ masks for $P$. There are at most $2^R$ such classes. Each block therefore has a class of size at least $D$. Select exactly $D$ coordinates from a largest class in each block. For integers $0\le s,t\le D$, fix the first $s$ of the selected-block class to one and its others to zero; do the same with the first $t$ of the ignored-block class. Set every other nonlive raw address bit to zero.

Consider an exceptional gate assigned to $P$, at either fixed character table. Let its selected/ignored magnitudes be $a,b\ge0$; its affine address form on the resulting pre-identification cube is

$$c+\epsilon a s+\eta b t+\sum_{\ell=1}^{L}u_\ell z_\ell+\sum_{\ell=1}^{L}v_\ell w_\ell,$$

where $|u_\ell|=a$, $|v_\ell|=b$, and $\epsilon,\eta\in\{\pm1\}$ are constant on the respective sweep classes. Its entire live range has width exactly $L(a+b)$, since the live bits are independent. Choose the larger of $a,b$, denoted $h>0$. Vary its corresponding sweep index and fix the other. The baseline moves by magnitude $h$ per integer step. Nonconstancy holds precisely when the threshold lies strictly above the live minimum and at or below the maximum. Thus the set of bad real sweep indices is an interval of length

$$\frac{L(a+b)}h\le2L.$$

It contains at most $2L+1=B$ integers. This count includes threshold ties conservatively. Consequently the fraction of bad baseline pairs in $\{0,\ldots,D\}^2$ is at most $B/(D+1)$ for this gate. The estimate works even if one magnitude is zero and with arbitrary, even unbounded, real scale ratios.

If $2E_P B<D+1$, the union bound over both fixed-table versions yields **one common** $(s,t)$ for which every exceptional gate is constant at each table on the entire $2L$-variable live cube. The two constants need not agree. No top coefficient sizes or signs were used, and these gates remain constant after every later literal identification.

**Annihilate all other profiles.** For a gate with profile $Q=\{U,U^c\}\ne P$, some tree edge has both endpoints on the same side of $Q$. Otherwise its membership in $U$ would be a proper two-coloring of the connected bipartite tree, whose two colorings are exactly $T$ and $T^c$; that would give $Q=P$.

On this edge the gate has equal absolute coefficients on each of its $r$ raw pairs. Identify the ignored member with an independent uniform literal of the selected member. In sign coordinates write $w_\ell=\tau_\ell z_\ell$, $\tau_\ell\in\{\pm1\}$ independently. The new coefficient is $u_\ell+\tau_\ell v_\ell$. For a nonzero equal-magnitude pair it vanishes with probability exactly $1/2$; a zero-zero pair vanishes with probability one. Hence this gate retains all $L$ variables with probability at most $2^{-r}$. Uniform-magnitude full-support gates have this estimate on every tree edge as well. Pure-table gates are already constant.

The union bound over at most $G$ nonexceptional address gates gives failure probability at most

$$G2^{-r}<1.$$

There exists one choice of all literal signs on which **every** nonexceptional table/address gate omits at least one selected live variable at both table offsets. The union bound counts $G$, not $2G$: the canceled coefficient is independent of the offset. This choice can be made after the good baselines: cancellation depends only on normals, while exceptional constancy was guaranteed for every live assignment and thus every subsequent identification. This order of quantifiers is essential.

**The exact nonnegative dual.** Let $y\in\{\pm1\}$ select the table $x^y$. The target after these substitutions is $y$ times, up to the fixed parity of the selected baseline ones, full parity on $L\ge2$ independent bits. Put uniform mass on the $2^{L+1}$ resulting original inputs. Its signed average against every exceptional bottom is zero because that bottom is constant at each table; against every other table/address bottom it is zero because that bottom omits a live variable at each table. Pure-address features vanish by averaging $y$; pure-table features vanish by averaging live parity. These statements also cover every raw input and the constant. Thus the measure is nonnegative, normalized, and exactly annihilates every label-signed circuit feature.

A correct finite top threshold can be strictified by a harmless shift of its intercept. Its signed score is then strictly positive on every input in this support, so its positive uniform average cannot be zero. This contradicts the annihilation equations for all its features, regardless of arbitrary real top weights. Thus $2E_P B\ge D+1$. Summing over the $2^{k-1}-1=N/2-1$ disjoint nontrivial unordered profiles proves (2.2). $\square$

**Oriented-rectangle form.** Pair each live address of positive selected parity with one of negative selected parity, for example by flipping the first selected live variable and also its identified ignored partner. Each pair, together with $x^+,x^-$, is a forced-sign rectangle. Summing its row $g(x^+,a_+)-g(x^-,a_+)-g(x^+,a_-)+g(x^-,a_-)$ uniformly over the $2^{L-1}$ pairs gives zero in every bottom coordinate by the preceding Fourier annihilation. Every row would have strictly positive inner product with the actual top vector. This is a scalable analytic **nonnegative dependence of oriented rectangle rows**, with no finite LP discovery step. Individual rows may be zero; the theorem does not require them all nonzero.

If instead all address-reading gates, including pure-address ones, obey the normal hypothesis, the one-character-table proof gives the sharper $E_PB\ge D+1$. The free-pure-address version above is the lead statement because its broader scope is more useful.

### 2.3 Balanced exponent and nonvacuity [PROVED]

For constant $R$, balanced $M=km=\Theta(N)$, and $G<n^2$ (larger $G$ already satisfies the desired asymptotic conclusion), $r=O(\log n)$ and $kr=O(\log^2 n)=o(m)$. Therefore (2.2) implies

$$\boxed{G=\Omega\!\left(\frac{n^2}{2^R\log^3 n}\right).}$$

In particular the exact exponent of this class is two. The matching $O(n^2)$ construction is UP2 round-two §2: use odd unit magnitudes on character blocks and even magnitude two elsewhere, and expand $\varphi(X_T+L_T)-\varphi(L_T)$. Choose the same mask for complementary characters $T,T^c$; then each unordered profile has just one mask, so $R=1$ already includes an exact quadratic family. Those masks can differ arbitrarily among profiles and can be mixed inside every block. Thus the class need not be sign-coherent or have a globally bounded set of masks. The construction and its original Fourier identity remain attributed to UP2 and the inherited paper.

The lower theorem itself needs neither one Walsh table statistic per gate nor any bound on semantic character-pair incidence. For example choose a two-scale mixed-sign address row with at least one positive coefficient of magnitude two, and take table coefficients $\alpha_0=2$, with every other $\alpha_c$ nonzero of arbitrarily chosen mixed signs satisfying $\sum_{c\ne0}|\alpha_c|<1/4$. Set threshold one. On every nonconstant complementary character pair, the difference is one at the zero address and zero when that positive magnitude-two coordinate alone is one. Hence every one of the $N-1$ character pairs is semantically active. Such gates fit the model. The theorem does not exploit their particular near-one-bit table representation; arbitrary dense table rows are allowed.

[KNOWN / scope] Generic many-mask profiles, magnitudes varying within a block beyond a sign mask, or more than two blockwise magnitude classes escape this theorem. Small positive perturbations can change those hypotheses even when truth tables remain fixed; only a semantically equivalent allowed representation would inherit the bound. No unrestricted exponent above $3/2$ is claimed.

## 3. Linear mask cost via reoriented random prefix paths

### 3.1 A shuffled-bridge occupation lemma [PROVED]

Let $h=p+q$ with $p\ge q$, $\Delta=p-q$, and uniformly shuffle $p$ steps $+1$ and $q$ steps $-1$. Let $S_0=0,S_1,\ldots,S_h=\Delta$. For an integer level $a$, put $t=\operatorname{dist}(a,[0,\Delta])$, the nonnegative integer distance to that interval. Then

$$\boxed{\mathbb E|\{s:0\le s\le h,\ S_s=a\}|=
\frac{\sum_{i=0}^{q-t}\binom{h+1}{i}}{\binom hq}.}\tag{3.1}$$

An upper limit below zero means an empty sum. In particular, for every $a$,

$$\boxed{\mathbb E|\{s:S_s=a\}|\le\frac{2(h+1)}{\Delta+2}.}\tag{3.2}$$

The same upper bound holds for negative total drift with $\Delta$ replaced by its absolute value.

**Proof of the identity.** All generating functions in this argument are formal power series. Let $U_a(z)$ count unrestricted nearest-neighbor walks from zero to $a$ by their length. The walk recurrence $U_a=\mathbf1_{a=0}+z(U_{a-1}+U_{a+1})$ gives

$$U_a(z)=\frac{W(z)^{|a|}}{\sqrt{1-4z^2}},\qquad
W(z)=\frac{1-\sqrt{1-4z^2}}{2z},\qquad W=z(1+W^2).$$

This can also be checked directly in the recurrence; the solution is uniquely determined coefficient by coefficient. A walk from zero to $\Delta$ with a marked visit at $a$ is uniquely the concatenation of a walk to $a$ and a walk of displacement $\Delta-a$. Its marked-visit count is therefore

$$[z^h]U_a(z)U_{\Delta-a}(z)
=[z^h]\frac{W(z)^{\Delta+2t}}{1-4z^2}.$$

For integers $d\ge0$, the coefficient of $z^h$ in $W^d/(1-4z^2)$, when $h-d=2j\ge0$, is

$$\sum_{i=0}^j\binom{h+1}{i}.$$

Here is an elementary verification avoiding any unproved generating-function extraction rule. For $d=0$, the coefficient is $2^h$ for even $h$, and the displayed binomial sum is exactly half the sum of row $h+1$, whose length is even. For $d\ge1$, the identity $W^d=z(W^{d-1}+W^{d+1})$ reduces the assertion to the two coefficients at $(h-1,d-1)$ and $(h-1,d+1)$. Their partial sums combine to the displayed sum by Pascal's identity. Coefficients are zero when $d>h$ or parity differs. Induction on $h$ completes the proof. Apply this with $d=\Delta+2t$ and divide by the $\binom hq$ walks to obtain (3.1).

For (3.2), the numerator is maximal at $t=0$. Consecutive terms in its lower binomial tail have ratio at most $q/(h+2-q)<1$, so

$$\sum_{i=0}^{q}\binom{h+1}{i}
\le\binom{h+1}{q}\frac{h+2-q}{h+2-2q}.$$

Divide by $\binom hq$, use $h+2-2q=\Delta+2$ and $(h+2-q)/(h+1-q)\le2$, and obtain (3.2). Reflection handles negative drift. This is a classical one-dimensional walk calculation supplied in full, with no novelty claim.

### 3.2 Simultaneous drift from a common reorientation [KNOWN lemma; proof reproduced]

UP1 round-one §2.1 proved: for $R$ sign vectors $p_1,\ldots,p_R\in\{\pm1\}^h$, some $z\in\{\pm1\}^h$ has

$$|\langle p_j,z\rangle|\ge h/R-R\qquad\text{for every }j.$$

Its complete elementary proof is short. Choose signs $\epsilon_j$ maximizing the squared Euclidean norm of $v=\sum_j\epsilon_jp_j$. Flipping one sign shows $\epsilon_j\langle p_j,v\rangle\ge h$. Thus $u=v/R\in[-1,1]^h$ has these oriented projections at least $h/R$. Move to a vertex of the polytope $\{w\in[-1,1]^h:P w=P u\}$, where $P$ has rows $p_j$. Such a vertex has at most $\operatorname{rank}P\le R$ fractional coordinates; otherwise a nullvector supported on fractional coordinates permits a two-sided feasible move. Round them to nearest signs. Every projection changes by at most $R$. This proves the lemma. It is an attributed inherited ingredient, not a new LOW2 discrepancy result.

### 3.3 Stronger profile theorem [PROVED]

Retain the model of §2, including arbitrary pure-address and pure-table helpers. Put

$$r=\max\{2,\lceil\log_2(G+1)\rceil\},\quad L=(k-1)r,\quad
h=m-L,\quad B=2L+1,\quad \delta=h/R-R.$$

Assume $h>0$ and $\delta\ge0$. Then every nontrivial unordered profile satisfies

$$\boxed{E_P\ge\frac{\delta+2}{4B}.}\tag{3.3}$$

In particular if $R^2\le h/2$,

$$\boxed{E_P\ge\frac{h}{8RB},\qquad
G\ge\left(\frac N2-1\right)\frac{h}{8RB}.}\tag{3.4}$$

**Proof.** Keep the spanning tree and its disjoint $r$-fold pairs from §2. Choose one selected block and one ignored block. Reserve exactly $h$ unused coordinates in each; there are at least this many. In each chosen block apply §3.2 to the at-most-$R$ masks of the exceptional profile, padding by repeats if necessary. Obtain a common reorientation $z$ for that block so every exceptional mask has absolute drift at least $\delta$ on these $h$ positions.

In the selected block begin with bits $(1-z_l)/2$. Choose a uniform random permutation of its $h$ coordinates and flip the first $s$ bits, where $s$ is independently uniform in $\{0,\ldots,h\}$. Do the same, independently, for the ignored block with prefix count $t$. Set all other nonlive coordinates to zero. This is one shared distribution on actual fixed raw-address assignments, independent of which gate will be tested.

Consider an exceptional gate at either fixed complementary-character table. Let its selected and ignored magnitudes be $a,b\ge0$, and choose its larger magnitude $W=\max(a,b)>0$. Condition on the entire random choice in the other baseline block. In the $W$ block, its baseline value, divided by $W$, is a constant plus a uniform shuffled walk with increments equal to its mask times the common reorientation signs. Its absolute total drift $\Delta_j$ is at least $\delta$. The live range divided by $W$ has width $L(a+b)/W\le2L$, so the gate can be nonconstant only when this integer walk is at one of at most $B$ consecutive levels (the interval may be shifted by any real offset).

By (3.2), summing over these at-most-$B$ levels and averaging the uniform prefix index gives

$$\Pr[\text{this fixed-table gate is nonconstant}]
\le\frac{2B}{\Delta_j+2}\le\frac{2B}{\delta+2}.$$

This estimate is conditional on every choice in the other block and hence holds unconditionally. It does not require the different gates' walks or events to be independent. If $4E_PB<\delta+2$, the union bound over both table versions yields one realization of both reoriented prefix baselines making all exceptional gates constant. Now choose literal signs to annihilate every nonmatching-profile gate exactly as in §2; that step depends only on the normals and is unaffected by the more general baseline bits. The resulting uniform two-table/live-cube measure is again an exact nonnegative dual and a positive oriented-rectangle dependence, contradicting correctness. This proves (3.3). If $R^2\le h/2$, then $\delta\ge h/(2R)$, giving (3.4). $\square$

### 3.4 Exponents, limits, and novelty scope [PROVED consequences]

At balance, for $G<n^2$, we have $L=O(\log^2 n)$ and $h=\Theta(m)$. Under $R^2\le h/2$,

$$\boxed{G=\Omega\!\left(\frac{n^2}{R\log^3 n}\right).}$$

Thus any fixed $\eta<1/2$ and mask budget $R\le n^\eta$ give exponent at least $2-\eta>3/2$ in this explicit two-block-magnitude-profile class. Fixed or polylogarithmic $R$ force exponent two, matched by the inherited quadratic construction. This is a **new restricted-class theorem within this investigation**, not a new unrestricted ordinary-Andreev exponent. It allows arbitrary signed dense semantic table-Walsh activity, zero support on one side, arbitrary noncommensurable real ratios, and arbitrary real top weights. The simple signature-class theorem in §2 remains a separate proof requiring no random-walk calculation.

The common-mask bound is essential to the stated improved exponent. If one simply replaces $R$ by the number $E_P$ of gates in a profile, (3.4) gives a square-root requirement $E_P\gtrsim\sqrt{m/(k\log G)}$, unless $E_P$ is already larger than a constant multiple of $\sqrt m$. Summing does not improve exponent $3/2$. This is a limitation of that naive self-substitution, not a proof that the unrestricted two-scale class has a subquadratic construction.

### 3.5 Peer-sharpened finite inequality and semantic activity [PROVED]

UP1 and UP2 independently derived the same bridge occupation identity after my request, and each supplied the sharper bound

$$\mathbb E|\{s:S_s=a\}|\le\frac{h+1}{\Delta+1}.$$

For example, UP1 observed that the geometric-tail estimate already in §3.1 satisfies

$$\frac{(h+1)(p+2)}{(p+1)(\Delta+2)}\le\frac{h+1}{\Delta+1},$$

since $\Delta\le p$. This reduces the conditional bad-prefix probability to $B/(\delta+1)$. The resulting strongest finite version is

$$\boxed{2E_P B\ge h/R-R+1,\qquad
G\ge\left(\frac N2-1\right)\frac{h/R-R+1}{2(2(k-1)r+1)}}$$

when $h=m-(k-1)r>0$ and $h/R-R\ge0$. If $R^2\le h/2$, this gives

$$G\ge\left(\frac N2-1\right)\frac{h}{4R(2(k-1)r+1)}.$$

The exponent and scope are unchanged from §3.4. Attribution: independent marked-walk derivations by LOW2, UP1, and UP2; the sharper constant was supplied on the board by UP1 and UP2. I retained my direct Pascal-recurrence proof to make the report self-contained.

A semantic strengthening is immediate, parallel to LOW1's earlier activity refinement. For each chosen representative $T$ of $P$, count only exceptional-profile gates for which $a\mapsto g_j(x_T^+,a)-g_j(x_T^-,a)$ is nonconstant. Every inactive difference is already a constant, so its labelled integral vanishes without making either gate restriction individually constant. The same lower inequality holds for that smaller count. Fix one allowed representation per Boolean gate before applying the geometric proof; a truth-table-equivalent allowed representation suffices. Numerical perturbations alone do not supply one.

One may also grant, without charging $G$, any extra feature which becomes an affine function of the raw address bits after every fixed table. After the literal substitution it still has degree at most one, hence vanishes in the parity dual. This does **not** grant arbitrary table-gated pure-address thresholds: their fixed-table address dependence can be nonlinear.

## 4. Signed paths, character-test limitations, and upper-agent audits

### 4.1 How the new dual handles signed paths [PROVED interpretation]

The graph reductions in §§2–3 never normalize top signs and never posit a nonnegative table-to-output path. They apply the exact linear operation $F(x_T^+,a)-F(x_T^-,a)$ to the **actual common score**. After the common restriction, each gate difference is either constant or omits a live parity variable. Its signed integral is exactly zero, independently of its top coefficient's sign or magnitude. Thus arbitrary negative contributions are annihilated algebraically, not bounded or thrown away. This is the successful signed-path extension in this round; the old private-owner argument is not being generalized by a false small-negative-mass assertion.

[KNOWN / not an open candidate] Round-two LOW2 §4.1 already refuted private-owner containment with one arbitrarily small negative table coefficient. Counting negative-coordinate incidences alone did not produce a new valid reduction in this round. The analytic profile dual replaces that route under its stated geometric hypotheses. No unrestricted normalization into this class is asserted.

### 4.2 Character correctness is not sufficient, even for one common raw score [PROVED elementary counterexample]

UP2 suggested testing translation-invariant table-linear kernels with positive Walsh eigenvalues but without row diagonal dominance. The explicit choice $K=I+J$, where $J$ is the all-one matrix, gives

$$F(\xi,a)=\xi_{b(a)}+\sum_c\xi_c.$$

For every nonconstant signed character table $\xi=\pm\chi_T$, the sum is zero, so the score is exactly the desired sign. For either constant table it is $(N+1)\xi_b$, also strictly correct. Thus **all** character-table tests are satisfied by the same score, on every raw address.

For $N\ge4$, however, take $\xi_b=-1$ and $\xi_c=1$ elsewhere. Then $F=N-3>0$, the wrong sign. This is an actual all-size raw depth-two example: multiply by $N$, implement the inherited exact equality score $N\xi_b$ by the paper's Fourier staircases, and add the free table-affine term $N\sum_c\xi_c$ at the top. Its cost is $O(n^2)$ at balance, with no extra bottom gate for the false-positive bias.

This refutes character-test **sufficiency**, not the usefulness of character-supported lower-bound duals. It does not establish any cheaper promise circuit or upper bound on what a character-only dual can prove. The algebraic template is attributed to UP2; the explicit $I+J$ instance and raw-score audit are supplied here. Sparse/co-sparse promise constructions were already known and are not counted as new.

### 4.3 UP1's local amplitude results and a closure correction [PROVED CHECKS]

I read UP1 round-three §§2–5 and checked the one-scale result. If

$$H(u,v)=f(u+v)+g(u-v)+h(u)+j(v),$$

its odd-in-both-variables projection is $F(A+B)-F(A-B)$ for an even $F$. Therefore summing the tests $(A,B)=(2i-1,1)$ for $1\le i\le r$ telescopes to the test $(r,r)$. This gives the exact optimal amplitude distortion $r=\lfloor(R+1)/2\rfloor$ and approximation error $(r-1)/(r+1)$ on the punctured integer square; the clipped staircase witness in UP1 §4.4 attains both. I checked the raw $4r$-halfspace expansion and posted the audit. These are UP1's local-model theorems, not an unrestricted Andreev lower bound or a positive sign-computation dual.

UP1's exact table-conjunction compiler also checks: $C(x)[L(x,a)\ge0]=[L+B(U_C-r)\ge0]$ when $B>\max|L|$. Multiplying a whole score by one raw-table affine form gives a shared positive amplitude after its guard sign is factored, with overhead proportional to its raw table support. It is not a general branch-selection identity.

I flagged an important closure qualification on the board: gating a structured profile gate preserves its address normal, and gating a raw affine helper remains affine after fixing the table. But gating an **arbitrary pure-address** threshold with a table conjunction turns it into a mixed gate. Its previously free cancellation between character tables disappears, and its unrestricted address normal need not satisfy the profile hypothesis. Such helpers cannot silently be included in a table-gating closure claim. The compiler itself is valid; only applicability of the lower-bound model needs this qualification.

UP1 accepted this correction and revised its report before handoff. I subsequently checked its mixed-integer-direction finite-difference stencil as well: on odd inputs the two coordinate differences turn the sign product into four times one point mass; perpendicular differences annihilate the ridge directions; a generic exposed subset-sum vertex ensures a nonzero remaining coefficient. Its radius and approximation bounds have the stated finite-grid scope.

### 4.4 UP2 and LOW1 arithmetic/helper bounds [PROVED CHECKS, credited]

I checked UP2's complemented-face lemma: every multilinear coefficient of a strict full-parity score is nonzero in every complemented $0/1$ basis, because all summands of each alternating face difference have the same strict sign. I also checked the exact disjoint-prefix expansion of a superincreasing comparator and the preservation of superincreasing order under disjoint signed identifications. The earliest original coefficient in a merged group dominates all later originals; subtracting its own partners still leaves more than the total later merged magnitudes.

LOW1's resulting costed monomial support argument genuinely avoids the old survivor error. A helper depending on $s$ of $d$ live variables is charged $2^{s-d}$, rather than discarded. Its soft matrix entries $1/2,3/4,1$ for zero-zero, equal-nonzero, and unequal pairs correctly encode the expected factor. I checked these steps and sent the audit. The full hybrid theorem belongs to LOW1, with UP2's face/lex ingredients; its use of any stronger external conjunction theorem retains the original literature attribution in those reports.

### 4.5 LOW1 removes the mask cap at bounded integer scales [PROVED CHECK; theorem attributed to LOW1]

LOW1 extended the graph mechanism by pairing unused baseline coordinates and using the known skew-cover theorem. I read its complete §3 proof and the primary statement of [Sauermann–Xu, *Nondegenerate hyperplane covers of the hypercube*, Theorem 1.1](https://arxiv.org/html/2507.00773v2). That theorem supplies the inherited bound $D/2$ for a skew hyperplane cover; I do not claim to prove it here.

After individually rescaling a gate to integer magnitudes bounded by $C$, disjoint magnitude sets across a character cut give nonzero integer baseline coefficients $\pm a\pm b$. The live-width interval contains at most $2CL_T+1$ integers. If every baseline is bad, the two fixed-table banks give a skew cover. Otherwise every exceptional gate becomes constant, and my graph identification kills all remaining gates. LOW1 uses the complete bipartite block graph for multiple magnitude classes, and a tree for two classes. I checked the coordinate allocation, simultaneous table constancy, real-offset/integer-value distinction, and the exact incidence count: a gate with $q_j$ classes is separated by $2^{q_j-1}-1$ unordered cuts.

Its resulting bounds are $\Omega(n^2/\log^4 n)$ for fixed bounded integer block magnitudes, with arbitrary masks and dense signed table normals; for two levels the denominator improves to $C\log^3 n$. This is LOW1's additional skew-cover and multiclass result, not a separate LOW2 theorem. It is complementary to §3: it removes every mask cap at bounded commensurable scales, whereas §3 permits arbitrary irrational/huge ratios with a mask budget. Neither covers arbitrary within-block magnitude variation. The graph ancestry, new LOW1 contribution, and inherited geometric theorem are kept distinct.

### 4.6 A broad real-band extension of the skew-cover step is false [REFUTED by explicit family]

One cannot replace LOW1's bounded integer-level argument by a universal real-band cover statement based only on unequal raw magnitudes and nonzero paired baseline coefficients. Let the two magnitudes be $1$ and $1+\varepsilon$, and use opposite signs on each selected/ignored pair. Identifying $D$ unused baseline pairs as equal bits yields the baseline form

$$-\varepsilon\sum_{i=1}^D z_i.$$

Keep $L$ selected/ignored live pairs independent; their form has minimum $-L(1+\varepsilon)$ and maximum $L$. At threshold zero, if $0<\varepsilon D<L$, every baseline assignment leaves the gate nonconstant on that live cube: the minimum remains negative, and the maximum is at least $L-\varepsilon D>0$. Thus ONE admissible nonconstancy band covers the entire baseline cube. Every baseline coefficient is nonzero, and the original ratio can be arbitrarily near one, even irrational.

This explicitly refutes a magnitude-free $\Omega(D/L)$ band-cover inference in that paired-baseline architecture. It does not refute LOW1's stated integer theorem, the two-independent-baseline theorem here, or any Andreev gate bound. The different hypotheses protect the two proofs for concrete reasons: integer-level counting fails in this example, while independent baseline sweeps can still use the larger raw magnitude. The example was sent to LOW1 as a next-step guardrail.

## 5. Verification and artifacts [VERIFIED EXACT]

All computations used the Python standard library and exact integer/rational arithmetic. No packages were installed. Run:

```bash
python3 -I /tmp/andreev_gap/swarm_round3/low2/checks.py
python3 -I /tmp/andreev_gap/swarm_round3/low2/bridge_checks.py
python3 -I /tmp/andreev_gap/swarm_round3/low2/verify_certificate.py
```

Recorded checks:

- 86,360 connected-tree profile/coloring cases;
- 115,567 rational baseline-sweep slices, including zero magnitudes and threshold ties;
- 708 complete literal-sign survival counts;
- 94,423 exact marked-walk convolution identities and both occupation bounds;
- 97 common-reorientation mask cases and 5,760 exact random-prefix interval probabilities;
- 119 dense semantic character-activity checks;
- one 512-input exact dual with 326 label-signed annihilation equations, including 12 structured mixed gates, three arbitrary pure-address gates, two pure-table gates, every raw input, and the constant;
- its 128 positively weighted oriented rectangles sum exactly to zero in every bottom coordinate; 116 of the rows are individually nonzero.

The finite dual is saved in `profile_dual_certificate.json` and checked by the independent `verify_certificate.py`. Summaries are `checks.json`, `bridge_checks.json`, and `certificate_verification.json`. The saved library obeys the global one-mask-per-profile hypothesis, not merely the target profile's cap. The proof does not infer any exponent from these examples or claim an optimal small circuit size. No LP, solver approximation, or floating-point feasibility claim was used.

## 6. Final assessment and next step

[PROVED strongest own result] The connected-profile graph plus a two-baseline exact dual gives a near-quadratic lower bound despite **arbitrary dense semantic table-Walsh coupling and arbitrary signed top paths**. The random-prefix refinement gives $\Omega(n^2/(R\log^3 n))$ for the stated arbitrary-real two-scale block-profile model when $R^2\le(m-O(\log^2 n))/2$. Fixed/polylogarithmic mask budgets have exponent two, matched by a known exact construction. This fulfills the restricted-class and scalable-analytic-dual alternatives; it does not improve the unrestricted exponent.

[PROVED / credited peer advances] UP1 and UP2 checked and sharpened the bridge calculation and two-baseline quantifiers; UP1 identified the pure-address-helper scope issue, incorporated here via complementary tables. LOW1 combined graph isolation with skew baseline covers to remove mask bounds for bounded integer block magnitudes, then added a costed superincreasing-helper hybrid. I checked the relevant geometry, integer offsets, class counting, and support-budget terms. I also checked UP1's fixed-scale amplitude optimum and later multiscale finite-difference stencil, and UP2's lex/conjunction reduction. The graph idea, peer refinements, and classical imported results are attributed separately throughout.

[REFUTED / closed routes] Character-table tests alone do not guarantee all-table correctness, as $I+J$ demonstrates. Free pure-address cancellation is lost after nontrivial table gating. Thin real nonconstancy bands can cover the whole paired-baseline cube singly. Small-negative-mass owner repair, survivor-only amplification, bounded-margin sampling, and separate pair coverage remain previously refuted; none is reopened as a candidate here.

[CONJECTURE / single best next step] Remove the mask cap for **arbitrary real two-scale block profiles** by constructing a nonnegative exact dual that handles the near-cancellation real bands in §4.6. The bounded-integer/unlimited-mask case and arbitrary-real/few-mask case are now separately controlled. A successful bridge between them must use joint top-score constraints or genuinely independent baseline geometry; it cannot assert a universal real skew-band count or silently bound top coefficients. General within-block magnitudes remain a further escape beyond this focused next target.

[UNRESOLVED unrestricted objective] The supplied exact $\widetilde\Omega(n^{3/2})$ versus $O(n^2)$ gap is unchanged. No new unrestricted upper circuit, new literature-priority claim, Lean formalization, paper edit, online post, package installation, or additional agent is claimed. All task-owned computations finished. Every newly created file credits Christian Reitwiessner.
