Authors: Christian Reitwiessner

# UP2 round three — dense semantic table normals and heterogeneous address arrangements

## Scope and status

Completed round-three research handoff. Exact ordinary $\mathrm{THR}\circ\mathrm{THR}$ Andreev lookup, arbitrary real bottom/top weights and raw top inputs; $N=2^k$, $M=km=\Theta(N)$, $n=N+M$. No unrestricted exponent improvement is claimed. The full prior reports and round-two board were read; completed proofs, scope limits and substantive peer exchanges are below.

[KNOWN, previous rounds] Sparse table-Walsh channels, fixed-mask two-scale channels plus full-sign helpers, and equal-spectrum cancellation are closed routes under their explicit hypotheses. Finite palettes and numerical near equality alone are not hardness conditions.

[PROVED, lead result] Ordered groups of address coefficients with dominant subset-sum gaps and maximum width $q$ require $S\ge((3/2)^{km}-1)/(2km\,2^q)$ mixed gates. This is exponential for $q=o(km)$, permits arbitrary dense semantic table coupling, and follows from an explicit compiler plus the inherited BBGL parity-conjunction theorem. See §1.

[PROVED auxiliary contribution] An exact random-bridge occupation identity supplies LOW2's proposed linear-in-$R$ mask tradeoff for dense-table arbitrary-real two-scale profiles. See §2.4. No unrestricted exponent change.

## Exact constraints imposed from the start

[KNOWN, character restriction] Writing table signs $\xi_c=(-1)^{x_c}$, the two tables $\xi=\pm\chi_T$ force complementary outputs $\pm\chi_T(b)$, parity on $|T|m$ raw bits. One common top score must meet all such constraints and every non-character table, including rare inputs. Independent pair coverage or independent per-table tops are insufficient.

## Research log

Initialized before new research with the target of dense semantic table projections and address rows outside bounded mask/two-scale families. This log records the completed models, proofs and unresolved steps.

## 1. Arithmetic scales: candidate obstruction beyond exact equalities

[PROVED; initial candidate superseded by §§1.1–1.4] Gate-specific superincreasing absolute address coefficients, with arbitrary mixed signs, zero supports, dense table coefficients and unrestricted top weights, require $\Omega((4/3)^{km})$ gates for exact Andreev. The proposed proof fixes the full-character table and uses the sparsity of lexicographic thresholds in randomly complemented monomial bases. It does not use equal magnitudes, overlap histograms, small table-Walsh support or top norms. The stronger completed proof and grouped-scale extension are below; this paragraph preserves the original weaker candidate for provenance.

[PROVED elementary lemma] Let $P$ be the unique multilinear polynomial of a strict parity score on $d$ bits. For any corner $t$ of the cube, express $P$ in coordinates $u_i=z_i\oplus t_i$. For any $U\subseteq[d]$ its coefficient is
$$c_{t,U}=\sum_{V\subseteq U}(-1)^{|U|-|V|}P(t\oplus\mathbf1_V).$$
If $P(z)$ has strict sign $(-1)^{|z|}$ up to a fixed overall sign, every summand has sign equal to that overall sign times $(-1)^{|t|+|U|}$. Therefore every coefficient is nonzero. This holds for every magnitude profile of the correct score and every coordinate basis. The lemma is standard Möbius inversion with a parity sign condition; no literature priority claim.

[PROVED elementary lemma] A conjunction of $r$ literals in distinct variables expands into $2^v$ distinct $0/1$ monomials when $v$ of its literals are negative in the chosen basis. Uniform independent basis complementation gives $v\sim\operatorname{Bin}(r,1/2)$, so expected support size is $(3/2)^r$. Support of a sum is contained in the union of summand supports, regardless of cancellation or enormous coefficients. Thus an affine combination of $L$ conjunctions of widths at most $d$, plus raw affine terms, cannot sign-compute parity unless $L(3/2)^d+d+1\ge2^d$. This exact common-top obstruction is not a correlation or normalization bound.

### 1.1 Status update and inherited stronger theorem

[KNOWN, primary source inspected] Basu–Bhatnagar–Gopalan–Lipton, [*Polynomials that Sign Represent Parity and Descartes' Rule of Signs*, Theorem 6.5](https://arxiv.org/html/math/0702773), prove that any strict parity sign representation as a real linear combination of literal conjunctions needs at least $(3/2)^d$ terms, counting the constant as an empty conjunction. Their paper also credits the standard-monomial parity sparsity result to Minsky and Papert. Thus neither the preceding face lemma nor a parity/conjunction exponential lower bound is claimed as new literature. The following application to scale-separated raw threshold directions is the current investigation's additional reduction.

For completeness, the inherited term-count proof is short. Split a conjunction representation into $P=z_d A+(1-z_d)B+C$, with respective counts $a,b,c$. Both restrictions and their difference sign-represent parity or its complement on $d-1$ bits. By induction, $a+c,b+c,a+b\ge(3/2)^{d-1}$. Adding gives $a+b+c\ge(3/2)^d$. The zero-variable case needs one constant term. This argument counts the actual terms; it does not assume their expression is unique or their coefficients bounded.

### 1.2 Ordered groups with subset-sum gaps: exact model

Let $M=km$. For each bottom with a nonzero address normal, independently partition its nonzero address coordinates into ordered groups
$$B_{j,1},\ldots,B_{j,h_j}.$$
Signs, partitions, orders and magnitudes may differ arbitrarily between gates. Let $w_i=|\gamma_{j,i}|$ for the current gate and
$$\Sigma_{j,\ell}=\left\{\sum_{i\in B_{j,\ell}}w_i z_i:z_i\in\{0,1\}\right\},\qquad
W_{j,\ell}=\sum_{s>\ell}\sum_{i\in B_{j,s}}w_i.$$
For every group except the last, require its $2^{|B_{j,\ell}|}$ subset sums to be distinct and their minimum positive gap to exceed $W_{j,\ell}$. The final group is arbitrary; no gap or distinctness condition is needed there. Let
$$D_j=\sum_{\ell=1}^{h_j}2^{|B_{j,\ell}|}.$$
A zero address normal is table-only and will contribute only a constant in the comparison below. Table normals, thresholds, top weights and all raw top wires are arbitrary real numbers. There is no bounded-table-Walsh or normalized-margin assumption.

This class contains superincreasing single-coordinate scales, but also arbitrary incommensurate arrangements within each group. The class is nonvacuous: choose any finite injective subset-sum profile inside each group, then scale successive earlier groups enough to dominate the later total. Positive and negative signs and missing raw coordinates are freely permitted. A completely unrestricted normal can always be put into one group of width $M$, but then the bound below becomes vacuous; small group width is a substantive hypothesis.

### 1.3 Exact compiler to disjoint conjunctions [PROVED]

After fixing a table, flip each raw address bit with negative coefficient. This only shifts the threshold, and makes all nonzero coefficients positive. In one unresolved prefix branch of the ordered groups, consider a current group assignment whose contribution is $v$. Its remaining possible total lies in the closed interval $[v,v+W_{j,\ell}]$, plus the fixed prefix contribution. If the threshold is at or below the lower endpoint, the entire branch outputs one; if it is above the upper endpoint, the entire branch outputs zero. Otherwise the branch is unresolved, with the tie-safe condition
$$v<\theta'\le v+W_{j,\ell}.$$
Because the distinct current-group values are separated by more than $W_{j,\ell}$, at most one assignment is unresolved. Continue only along that assignment. At the last group every assignment is decided.

Each accepted branch is a conjunction of the fixed prefix literals, including the decisive current-group assignment. Different accepted branches are disjoint. The threshold function is therefore EXACTLY the sum of their indicators, not merely the sign or an OR of overlapping terms. There are at most $D_j$ accepted branches. Restoring the negative coefficient flips gives ordinary signed literals and changes no count. Constant functions use zero or one empty conjunction.

For single-coordinate groups with $w_r>\sum_{s>r}w_s$, at most one accepted branch is added at each stage, so a nonconstant gate uses at most its support size $r\le M$ conjunctions. This is the familiar lexicographic decision-list expansion, now with arbitrary table shifts and gate-specific orders. The compiler is an algebraic equality at the score level and introduces no circuit layer in the argument.

### 1.4 Exponential obstruction with unrestricted pure-address helpers [PROVED]

Consider an exact Andreev circuit whose table-and-address-dependent bottoms satisfy the group-gap hypothesis. Allow any number of arbitrary pure-address bottoms, arbitrary table-only bottoms, and all raw top wires. Let $J$ index only the table-and-address-dependent bottoms. Then
$$\boxed{1+2\sum_{j\in J}D_j\ge(3/2)^M.}$$

**Proof.** Compare the two tables $x_c^\pm=(1\pm\chi_{[k]}(c))/2$. For every raw address they select complementary outputs. Their actual common-top score difference $F(x^+,a)-F(x^-,a)$ therefore has strict sign $\chi_{[k]}(b(a))$, the full parity on all $M$ raw address bits. No top strictification is even needed for this difference: the difference of a nonnegative true-class score and a negative false-class score is strictly positive.

All raw address terms and all pure-address gates cancel. All raw table and table-only terms become one constant. Each mixed bottom contributes two fixed-table threshold functions, each with an exact conjunction expansion of at most $D_j$ terms by §1.3. Their actual top coefficients are retained, with a sign change for the second restriction. Thus the strict parity score has at most $1+2\sum_j D_j$ literal-conjunction terms. Apply the inherited Basu–Bhatnagar–Gopalan–Lipton bound. $\square$

If every group has size at most $q$, then $h_j\le M$ and $D_j\le M2^q$. Thus the number $S$ of mixed bottoms satisfies
$$\boxed{S\ge\frac{(3/2)^M-1}{2M2^q}.}$$
For $q=o(M)$ this is $2^{\Omega(M)}=2^{\Omega(n)}$ at balance. More quantitatively, any polynomial-size family in this class must have
$$q\ge \log_2(3/2)M-O(\log M).$$
For genuinely superincreasing singleton scales the sharper compiler gives
$$S\ge\frac{(3/2)^M-1}{2M}.$$
These are restricted-family lower bounds, not an unrestricted exponent improvement. They tolerate completely dense semantic table-Walsh activity, all-distinct irrational address magnitudes and unrelated sign masks across gates. They do not require any comparable eligible block or zero drift. The known two-scale quadratic circuit violates the group-gap property except when its large interacting groups are retained, so there is no contradiction.

### 1.5 Semantic scope and relation to earlier barriers

[PROVED] The argument is semantic at the fixed-table level: it suffices that every bottom on each of the two complementary full-character tables admit an exact real expansion using at most $D_j$ literal conjunctions. The written weights need not themselves obey a group-gap condition if an equivalent restricted truth function does. Harmless generic coefficient perturbations therefore do not invalidate this form of the statement.

[KNOWN / comparison] Round-one low-rank table-register obstructions already exclude one huge TABLE register; §1.4 instead permits full-rank arbitrary dense table normals and excludes a different resource, namely small-group lexicographic ADDRESS arithmetic. The all-distinct coefficients generally give no exact pair cancellations, so the old permanent/survivor inequalities can be vacuous here. This is not a reformulation of equal-magnitude hardness. It is nevertheless a direct application of an established parity-conjunction theorem, and no literature-priority claim is made for the derived architecture corollary.

[PROVED scope limit] Comparable, interacting unequal magnitudes need not have short conjunction expansions. For instance a Hamming majority on $M$ bits has exponentially many positive boundary minterms; the generic bound by all positive minterms gives no useful gate lower bound. One cannot silently put all unrestricted weights into tiny separated groups. The known quadratic helper identity uses such broad threshold functions and is fully consistent with §1.4.


### 1.6 Ordered-gap groups survive literal identifications [PROVED; late extension sent to LOW1]

The group-gap class itself, not merely singleton superincrease, is closed under arbitrary disjoint signed literal identifications and fixed coordinates. Group each nonzero merged live coefficient according to the earliest original group containing any of its nonzero original coefficients. Each new group has at most the original maximum width $q$.

For a subset-sum difference of absolute merged coefficients in such a group, undo the signs of those merged coefficients. Its contribution from the earliest original group is a nonempty signed sum with coefficients in $\{-1,0,1\}$ of distinct original magnitudes. Disjoint identifications ensure that an original coordinate is used at most once. If this is not the last original group, subset-sum injectivity makes the contribution nonzero of magnitude at least its old gap $\Delta$. The absolute contribution of later original coordinates assigned to these same merged variables is at most $W_{\rm partners}$. New variables first appearing in a later group have total absolute coefficient at most $W_{\rm remaining}$. These sets use disjoint original tail coordinates, so
$$W_{\rm partners}+W_{\rm remaining}\le W_{\rm old\ tail}<\Delta.$$
Thus the new subset-sum difference has magnitude at least $\Delta-W_{\rm partners}>W_{\rm remaining}$, which is at least the new later tail. This proves the required distinctness and gap. Variables first appearing in the last original group form an arbitrary permitted last group; their zero coefficients can be discarded. Fixing coordinates only removes coefficients and shifts thresholds. This proves closure, including unequal irrational coefficients and heterogeneous supports.

[PROVED corollary, combined mechanism credited LOW1] LOW1's §4.6 costed profile hybrid therefore extends from superincreasing helpers to these grouped helpers. Suppose $F$ additional mixed gates have group width at most $q$ and $S$ structured gates have bounded integer magnitudes constant by original block. Under a live restriction of dimension $L$, one grouped helper has an exact conjunction expansion with at most $M2^q$ terms by §1.3 and closure. Its table difference has expected normalized monomial support at most $2M2^q(3/4)^L$. The structured nonseparated differences have budget at most $(3/4)^r$ each, as in LOW1's proof.

Choose
$$r=\left\lceil\log_{4/3}\bigl(16(S+2FM2^q+1)\bigr)\right\rceil,\qquad D=m-(k-1)r>0.$$
If LOW1's skew-cover charge failed on a character cut, its uncovered baseline would make every separated structured gate constant. On the remaining graph cube, $L\ge r$, average literal signs and complemented coordinate bases. The total mixed-feature support budget is at most
$$S(3/4)^r+2FM2^q(3/4)^L<1/16.$$
The free affine positions occupy at most $(L+1)/2^L<1/2$, whereas a strict parity score needs all monomial positions. Contradiction. Thus LOW1's same structured profile-incidence lower bound holds with this new $r$. The same argument applies to the two-level/tree specialization.

For polynomial $S+F$, fixed structured coefficient bound $C$, and helper width $q=(\log n)^{O(1)}$, the structured requirement still has exponent two. The constants and logarithmic powers depend on the chosen width regime; no literal $\Theta(n^2)$ assertion is intended. This is a heterogeneous union theorem, not a consequence of separately quoting class lower bounds. It uses LOW1's complete costed-hybrid proof and inherited skew-cover theorem, together with this identification-stable grouped compiler. The final theorem is recorded here with that division of attribution; no unrestricted exponent follows.

## 2. Substantive peer work and a new two-baseline refinement

### 2.1 LOW1's costed heterogeneous hybrid [PROVED CHECK, credited to LOW1]

LOW1 combined the face-coefficient lemma with random selected/ignored literal restrictions. After restricting to $d$ live parity bits, a gate depending on $s$ variables has at most $2^s$ monomial positions in every complemented basis. A superincreasing gate has expected at most $3(3/2)^d$ positions. Consequently support union, before discarding ANY helpers, gives
$$1-(d+1)/2^d\le3F(3/4)^d+\sum_{j\in H}\mathbb E2^{s_j-d}.$$
For full-sign equal-magnitude helpers, $s_j\sim\operatorname{Bin}(d,1/2)$, so $\mathbb E2^{s_j-d}=(3/4)^d$. Thus their hybrid requires
$$H+3F\ge(4/3)^d(1-(d+1)/2^d).$$
The combination belongs to LOW1. I independently checked the key closure under arbitrary disjoint signed identifications: order merged coordinates by the earliest original nonzero coordinate they contain. Its original magnitude exceeds the entire later original tail; subtracting its partners still leaves more than the sum of magnitudes of all later merged coordinates. Thus the surviving merged normal is again superincreasing, with any all-zero merged coordinates discarded.

This genuinely charges missing-variable helpers and avoids the disproved survivor-only amplification. I also supplied the histogram extension's soft matrix: entries $1/2$ for two zeros, $3/4$ for equal nonzero magnitudes, and $1$ otherwise, yielding half the previous cancellation deficit. LOW1 completed that extension and owns its full statement.

### 2.2 Two independent baselines for LOW2's dense profile theorem [PROVED refinement, parent argument credited to LOW2]

LOW2 proposed a new profile-tree construction, removing round two's sparse table-Walsh assumption. A gate has two magnitudes constant by original address block, with profile $U\subseteq[k]$ recording which level occurs in a block. Signs may vary within blocks. At most $R$ masks are used per unordered profile $\{U,U^c\}$. On a middle character $T$, a connected bipartite tree with classes $T,T^c$ has $L=k-1$ edges. Reserve $r$ disjoint selected/ignored coordinate pairs per edge. A profile other than $T,T^c$ has an equal-magnitude edge; random literal identification there makes a missing live coefficient except with probability at most $2^{-r}$.

LOW2's initial exceptional-profile constancy argument assumed a bounded magnitude ratio. The following refinement removes that assumption and permits one level to be zero. LOW2 posted the same two-baseline refinement independently immediately before my board entry; the independent derivations and mutual audit are both credited.

Pick blocks $u\in T$, $v\notin T$. After reserving the live coordinates, in each of these blocks partition the remaining coordinates by their $R$ mask signs. Choose a class of common size
$$D\ge\left\lfloor\frac{m-Lr}{2^R}\right\rfloor$$
from each block. Set exactly $s$ coordinates of the first class and exactly $t$ of the second to one, with $(s,t)\in\{0,\ldots,D\}^2$; all other nonlive bits are fixed. Every exceptional mixed gate has a magnitude $W>0$ equal to the larger of its two levels, and at least one of these two blocks carries that level. Conditional on the other baseline variable, sweeping the corresponding count changes its affine offset in steps of magnitude $W$, with a fixed sign throughout that class. The entire live-address range, BEFORE identifications, has width at most $2LrW$.

At either fixed complementary table, nonconstancy therefore occurs for at most $B=2Lr+1$ swept integer values. There are at most $(D+1)B$ bad grid points per fixed-table gate. If $E_T$ exceptional gates satisfy $2E_TB<D+1$, a union bound gives one common baseline pair making every exceptional gate constant at BOTH tables. No selected sweep is chosen globally: each gate may use whichever of the two coordinates has its own maximum magnitude when bounding its bad fraction. Independence of the two counts is precisely what permits that.

After this common baseline is fixed, LOW2's random literal signs kill all nonmatching-profile mixed gates simultaneously when $S2^{-r}<1$. The actual difference score would then be orthogonal to full live parity, contradiction. Thus
$$E_T\ge\frac{D+1}{2(2Lr+1)}.$$
The profile-tree theorem and its final summed bound belong to LOW2; this two-baseline argument is my contributed strengthening. All table normals can be arbitrary and semantically dense. Pure-address gates cancel in the table comparison and pure-table terms are constants. Zero-zero pairs only make the nonmatching-profile cancellation easier. There is no remaining scale-ratio restriction in this refinement.

### 2.3 Compulsory helper support for one full AND [PROVED auxiliary lemma]

For $d\ge3$, suppose a strict parity score uses exactly one fully dependent bottom, which is a point indicator, and all other bottoms omit at least one variable. Complement coordinates so the point indicator is $\prod_i z_i$. In this basis every degree-$(d-1)$ score coefficient is nonzero by §1's face lemma. The point indicator contributes zero at that degree; affine raw terms have degree at most one. A helper missing two variables contributes zero as well. The coefficient on $[d]\setminus\{i\}$ can only be supplied by a helper semantically dependent on every coordinate except $i$. Hence every one of the $d$ omission types must occur, requiring at least $d$ such helpers.

This was sent to LOW1 as a guardrail, not a quadratic lower bound. The statement is specific to a point-indicator survivor; an arbitrary fully dependent threshold may already contribute all lower-degree coefficients. UP1 correctly emphasized central-majority survivors as an essential different stress family.

### 2.4 Exact bridge occupation: linear mask loss for the profile theorem [PROVED auxiliary lemma]

LOW2 asked whether random permutation-prefix sweeps could replace $2^R$ signature pigeonholing by an $O(R)$ loss. UP1, LOW2 and I independently derived and posted the same exact bridge identity needed for that proposal; all three derivations are credited. My derivation and checks follow. Let a uniform shuffle of $p$ plus and $q$ minus unit steps have length $h=p+q$, endpoint $\Delta=p-q\ge0$, and partial sums $S_t$, including $S_0=0$. For an integer $y$ put $\nu=\operatorname{dist}(y,[0,\Delta])$. Then
$$\boxed{\mathbb E\#\{t\in\{0,\ldots,h\}:S_t=y\}
=\frac{\sum_{j=0}^{q-\nu}\binom{h+1}{j}}{\binom hq}
\le\frac{h+1}{\Delta+1}.}$$
An upper sum limit below zero means an empty sum. Thus every level between the two endpoints has the same maximal expected local time; levels outside have smaller local time.

**Proof of identity.** Let $G_y(z)$ enumerate all unrestricted finite unit-step walks from zero to $y$ by length. The recurrence $G_y=z(G_{y-1}+G_{y+1})$ for $y\ne0$, together with $G_0=1+2zG_1$ and symmetry, gives
$$G_y(z)=\frac{\rho(z)^{|y|}}{\sqrt{1-4z^2}},\qquad
\rho(z)=\frac{1-\sqrt{1-4z^2}}{2z}.$$
These are formal power series; the displayed solution is also verified directly from $\rho=z(1+\rho^2)$. Marking a visit to $y$ splits a walk into two pieces, so the number of length-$h$, endpoint-$\Delta$ walks with a marked visit is the coefficient of $z^h$ in
$$G_y(z)G_{\Delta-y}(z)=\frac{\rho(z)^{\Delta+2\nu}}{1-4z^2}.$$
For $a\ge0$ of the same parity as $h$, this coefficient in $\rho^a/(1-4z^2)$ equals $\sum_{j=0}^{(h-a)/2}\binom{h+1}{j}$. To verify the last assertion without integration, both sides obey the recurrence $C(h,a)=C(h-1,a-1)+C(h-1,a+1)$ for $a\ge1$. At $a=0$, even $h=2v$ gives $4^v=\sum_{j=0}^v\binom{2v+1}{j}$; coefficients with $a>h$ vanish. Induction on $h$ proves the formula. Divide the marked count by the total $\binom hq$ bridges.

For the inequality, descending binomial terms have successive ratio at most $q/(p+1)<1$, so
$$\sum_{j=0}^q\binom hj\le\binom hq\frac{p+1}{\Delta+1},\qquad
\sum_{j=0}^{q-1}\binom hj\le\binom hq\frac{q}{\Delta+1}.$$
Pascal's identity gives the numerator bound. The same estimate covers $q=0$ directly. $\square$

[PROVED application, conditional on the already-proved common-correlation lemma] UP1 round one gives a common sign flip on $h$ coordinates such that all $R$ sign masks have absolute drift at least $h/R-R$. If $R^2\le h/2$, this is at least $h/(2R)$. Use a uniformly random permutation and an independent uniform prefix time $0\le t\le h$ to select a baseline assignment after that flip. For each mask its individual signed walk is the uniform bridge just analyzed (reverse its sign if its drift is negative). Its probability of lying in any prescribed set of at most $2L+1$ integer levels is at most
$$\frac{2L+1}{\Delta+1}\le\frac{2R(2L+1)}h.$$

Perform this independently in one selected and one ignored baseline block. For each exceptional two-scale gate, condition on the other block's random data and sweep the block with its own maximum magnitude. Its normalized nonconstancy interval contains at most $2L+1$ integer levels. Union bounding the two fixed-table versions of $E_T$ gates, if
$$4E_T R(2L+1)<h,$$
one choice makes all exceptional gates constant. LOW2's subsequent tree identification then gives the same parity contradiction. Hence the free-pure-address-helper version has
$$E_T\ge\frac{h}{4R(2L+1)},\qquad h=m-(k-1)r,\quad L=(k-1)r.$$
Keeping the unsimplified drift gives the sharper finite inequality $2E_T(2L+1)\ge h/R-R+1$ whenever $h/R-R\ge0$. Summing distinct unordered profiles gives an $\widetilde\Omega(n^2/R)$ obstruction while $R^2\le h/2$, with arbitrary real scales including zero. LOW2 proposed the random-prefix improvement; the common-drift lemma is UP1's earlier work; the bridge identity and its supplied proof were independently derived by UP1, LOW2 and me; my sharper inequality was supplied independently of UP1’s equivalent sharpening. The theorem remains a restricted profile/mask result. Correlations between different gates' walks cause no problem because the union bound uses only individual probabilities under the same global random choice.

### 2.5 Dense semantic activity is genuinely permitted [PROVED example]

The arithmetic class is not merely a syntactically perturbed sparse-Walsh class. Take any mixed mask and any superincreasing positive weights with minimum at least one; let $L(a)$ be their nonnegative sum after the mask's raw bit flips. Define
$$g(x,a)=\left[L(a)+\frac{Nx_0-\sum_cx_c}{N}\ge0\right].$$
Its written table normal is nonzero at every table coordinate. For every nonempty character $T$, the complementary character-table offsets are $+1/2$ and $-1/2$. At the masked zero address their gate difference is one, while at any address of positive $L$ their difference is zero. Therefore this single gate has semantic character-pair activity $N-1$, the maximum possible. It can use all-distinct irrational superincreasing address magnitudes and arbitrarily mixed signs. This example is not a computing circuit; it confirms that §1.4 genuinely allows the dense semantic table coupling requested in the task.

## 3. Dense transforms and common amplitudes: precise failures and remaining scope

### 3.1 All-table correctness is stronger than character correctness [KNOWN condition; PROVED counterexample]

The row-dominance criterion is inherited from `RESEARCH_STATE.md` and earlier upper reports, not new here. If a proposed reconstruction has the form
$$F(\xi,a)=Q(\xi,a)\left(c(a)+\sum_c K_c(a)\xi_c\right),\qquad Q(\xi,a)>0,$$
then exact sign $\xi_{b(a)}$ for EVERY independent table is equivalent to
$$K_{b(a)}(a)>|c(a)|+\sum_{c\ne b(a)}|K_c(a)|.$$
The minimum signed bracket is the left side minus the two terms on the right, by choosing every other independent sign adversarially and choosing the selected sign to oppose the intercept. Thus positive common-amplitude factoring really would preserve exact classification, but positivity alone cannot fix an incorrect inner reconstruction.

As a useful growing-family counterexample, take a translation-invariant table-linear operator $K=I+J$, where $J$ is the all-ones matrix. Every Walsh character is an eigenvector with a POSITIVE eigenvalue: one for every nonempty character, and $N+1$ for the constant character. Thus all complementary-character tests pass under one common linear score. For a table with selected sign $-1$ and every other sign $+1$, however, the selected output score is $N-3>0$ for $N\ge4$, which is wrong. Equivalently row diagonal $2$ is dominated by the $N-1$ off-diagonal entries. LOW2 and I independently supplied this concrete example after discussing the spectral shortcut. As LOW2 observed, multiplying the score by $N$ lets the inherited exact quadratic Walsh circuit implement it with one additional free table-affine term. It is therefore an actual $O(n^2)$ raw-score false positive, not a subquadratic promise construction. It rejects sufficiency of character correctness, not the validity of character-supported lower-bound duals.

[REFUTED inference] Positive spectral eigenvalues, independent per-character recovery and dense table mixing do not establish all-table exactness. This closes the proposed shortcut, not all dense nonlinear table transforms. To use dense table rows constructively, an explicit shared score must either satisfy the displayed all-table condition after factorization or use a genuinely nonlinear table representation with its own all-input proof.

### 3.2 Deterministic products and table-only modulation

[PROVED CHECKS, UP1's current-round results] I checked UP1's odd-odd telescoping identity for the four directions $u+v,u-v,u,v$. It forces amplitude ratio at least $\lfloor(R+1)/2\rfloor$ for sign-correct scores on the punctured integer square, and precludes exact constant amplitude already at $R=3$. I also checked the continuous-model convex-hull obstruction for $R>3$, including coincident boundaries and the distinction between jumps and equality spikes. These are UP1's results, not my theorems. Different-slope FINITE integer-grid identities are not refuted by either argument.

UP1's exact table-conjunction and polynomial-modulation compiler preserves each original address normal. Consequently dense table coupling introduced by such guards does not escape LOW2's new profile theorem or LOW1's bounded-palette extension when the original address directions satisfy their hypotheses. This is a stronger limitation than the old sparse-Walsh charge: the table rows may now be semantically dense. A successful local product compiler alone still needs a globally economical bank of terms and one sign-correct all-table score.

### 3.3 Finite bases and arithmetic alternatives

[KNOWN closed routes, retained as exclusions rather than open candidates] Rank-two per-block address spaces, fixed-degree moment-curve normals, scalar table registers, dedicated character staircases, equal-magnitude random masks, few-Walsh guards, norm-sampled saturated-tail repairs and independent pair/transcript tests were already closed in the required earlier reports. They were not re-proposed as unsolved candidates here. The finite-basis thought at initialization produced no new raw identity; in particular I make no impossibility claim for a completely arbitrary rank-three address basis.

[PROVED new arithmetic exclusion] The actual all-size advance from that triage is §1.4: increasing real precision and using many distinct address magnitudes do not help when their subset-sum groups are lexicographically separated and small. It allows all table-side density and top cancellation, and even arbitrary pure-address helpers. Combining that result with LOW1's heterogeneous hybrid excludes a further union of previously separate structured classes.

[UNRESOLVED] Genuinely interacting unequal magnitudes within blocks remain outside these proofs. Numerical irrationality alone is not enough: sufficiently small perturbations can preserve every old Boolean truth table, and such perturbations inherit the old semantic obstruction. No explicit bank of new dense semantic normals in the surviving regime was found that yields an exact subquadratic common score.

## 4. Verification, reading, exchanges and attribution

[VERIFIED EXACT] The standard-library command

```bash
python3 -I /tmp/andreev_gap/swarm_round3/up2/checks.py
```

completed successfully. The final `checks.json` records 384,520 raw inputs for grouped arithmetic thresholds, 2,976 threshold choices including exact ties, 21,844 strict parity face coefficients, 35 exact complemented-basis conjunction support averages, 2,300 superincreasing signed-identification rows, 1,660 grouped signed-identification rows, 3,997 two-baseline grid bounds, 21,504 final-group collision cases, and 64,158 bridge occupation identities/inequalities through $h=70$. The final expanded run uses a changed deterministic random stream, so its threshold sample counts supersede the earlier board counts. These check formulas and endpoints only; the asymptotics follow from the written universal arguments.

[READING] Read the common brief, every completed round-one and round-two report, the round-two board, the research-state file and the relevant exact upper/coherent/full-sign sections of the current paper. The current-round board was read repeatedly after major ideas, and other agents' candidate statements were actively audited. The BBGL primary theorem and its conjunction-basis proof were inspected online; no new-literature priority is asserted. The bridge formula is a self-contained application of classical walk enumeration, also without a priority claim.

[EXCHANGES] Posted the arithmetic candidate before completing its proof; UP1, LOW1 and LOW2 checked its face/prefix steps. LOW1 used that mechanism for a genuinely costed superincreasing-plus-histogram helper hybrid; I checked identification closure and supplied its soft support matrix. LOW2 proposed profile-tree isolation; both of us independently found the two-baseline arbitrary-scale refinement and audited one another's versions. LOW2 then proposed reducing the mask dependence through random prefix sweeps; I supplied the exact bridge occupation identity, proof and exact checks. UP1's earlier drift lemma is an inherited input to this improvement. I checked LOW1's later bounded-palette, arbitrary-mask extension and its magnitude-class incidence count; that extension belongs to LOW1. Finally I checked UP1's amplitude obstructions and sent LOW2 the distinction between positive spectral response and all-table dominance. These exchanges are preserved append-only in `../board.md`.

[PROVED peer extension, attribution LOW1; scope checked here] LOW1's bounded-integer palette theorem uses the complete bipartite block graph and skew hyperplane covers to remove the mask cap for magnitudes constant within each block. The decisive gate incidence is the number of character cuts formed by unions of its magnitude classes, at most $2^{q_j-1}-1$. This gives exponent two for fixed bounded integer palettes despite dense signed table normals and arbitrary within-block signs. I checked its nonzero paired baseline coefficients and class-incidence accounting. The nondegenerate hyperplane-cover ingredient is inherited from Sauermann–Xu; I did not claim to prove that geometric theorem. Arbitrary incommensurate within-block variation is outside the hypothesis.

## 5. Final handoff

[PROVED, strongest own restricted result] For mixed bottoms whose address coefficients split into ordered groups of width at most $q$, with each earlier group's distinct subset-sum gaps exceeding the entire later magnitude sum,
$$S\ge\frac{(3/2)^{km}-1}{2km\,2^q}.$$
For $q=o(km)$ this is exponential at balance, with arbitrary dense table normals, unrelated supports and masks, real irrational scales, arbitrary top weights/raw wires, and unrestricted pure-address helpers. Full proof: §§1.2–1.4. The parity/conjunction lower bound is attributed to BBGL; the additional step is the exact disjoint-conjunction compiler and character-pair application. This is a newly characterized research class in this run, not a claim of literature novelty.

[PROVED, strongest collaboration contribution] The independently derived bridge identity in §2.4 supplies LOW2's random-prefix estimate and reduces the two-scale profile mask loss from $2^R$ to $R$ while $R^2\le(m-O(k\log S))/2$. The resulting dense-table arbitrary-real-scale profile obstruction is $\widetilde\Omega(n^2/R)$, with zero levels allowed. LOW2 owns the profile-isolation theorem; UP1 owns the inherited common-drift lemma. Our two-baseline derivations were independent and are credited as such.

[PROVED late combined extension] Ordered-gap groups remain in the same class under every disjoint signed literal identification. Consequently LOW1's costed structured/helper theorem extends to polynomially many such helpers of polylogarithmic group width, retaining exponent two for its bounded-integer blockwise magnitude gates. The complete closure proof and changed logarithmic parameter are in §1.6. This extension was sent to LOW1 for audit; the proof is recorded independently of whether that late review finishes.

[REFUTED specified routes] Lexicographically separated address arithmetic with small groups, including all-distinct/incommensurate normal encodings, cannot provide a polynomial-size solution. Positive character eigenvalues do not give universal table decoding. Dense table-only modulation does not change the obstructed address profiles. The older dead ends remain closed under their stated hypotheses and were not silently revived.

[UNRESOLVED unrestricted goal] No exact $n^{2-\varepsilon}$ construction, and no unrestricted lower exponent above $3/2$, was obtained. The requested ordinary-Andreev gap is unchanged. No paper or repository files were edited, no subagents started, no packages installed, and nothing posted online. All task-owned calculations have finished. Newly created artifacts carry Christian Reitwiessner's authorship credit.

[CONJECTURE / single most promising next step] Search for a deterministic common-amplitude raw-threshold identity with semantically dense table rows and **interacting, non-lexicographic within-block magnitude profiles**, imposing all independent-table inequalities from the outset. A concrete test family should use many different masks and genuinely new comparable unequal weights inside each original block, rather than a bounded palette constant by block or a precision perturbation preserving the old gates. The exact target is a single score factoring as $Q(x,a)(1-2x_{b(a)})$, with $Q>0$, using $n^{2-\varepsilon}$ raw thresholds. Establish the factorization or a universal sign certificate before optimizing constants. This is a sharply stated missing identity, not evidence that such a circuit exists.
