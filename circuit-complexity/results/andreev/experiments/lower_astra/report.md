<!-- Copyright (c) 2026 Christian Reitwiessner. -->
Authors: Christian Reitwiessner

# Lower-bound research report

## Outcome and status

**Main result [PROVED HERE, hand proof, not independently reviewed or Lean formalized].** For ordinary Andreev at balance, the unrestricted gate bound

$$S=\Omega\!\left(\frac{\varepsilon^2 n^{3/2}}{\log^2 n}\right)$$

holds throughout

$$\varepsilon\ge C/\sqrt n,$$

for an absolute sufficiently large constant $C$. Here $S$ counts **bottom gates**, and total size is $S+1$. This improves the advantage range in the archive from $C\sqrt{\log n/n}$ (latest hand argument) and $C\log n/\sqrt n$ (formalized pipeline). It does **not** improve the constant-advantage exponent or logarithmic denominator. The change is to use the VC/Rademacher complexity of the fixed-direction, fixed-top restricted family, rather than its cardinality. The unavoidable zero-survivor contribution becomes $O(N^{-1/2})$ instead of $O(\sqrt{\log N/N})$. An adaptive-survivor argument is included below; no independence of survivors and table is assumed.

**Second result [PROVED HERE].** Exact sign correctness, not exact-top-sum, implies

$$S\ge\binom{k}{r}\quad(1\le r\le k)$$

when $m\ge2$ and every bottom gate has a common absolute value for its nonzero address coefficients. Different gates may use different magnitudes; signs, zeros, table coefficients and all top coefficients are unrestricted. This follows by averaging the top score over each parity fiber and using all $2^N$ independent tables. It transfers the archived exact-sum Fourier-profile obstruction to THR-at-top **without a margin assumption**. Its quantitative bound is weaker than the established unrestricted balanced bound, but the accompanying necessary signature-rank conditions constrain mixed-sign construction architectures. It is a genuine global all-table constraint, not a survival argument.

**Third result [PROVED HERE].** Under the randomized count restriction, arbitrary-weight gate survival satisfies $p(g)=O(k/\sqrt m)$. The archive already has $O(k^{3/2}/\sqrt m)$, so the improvement is a factor $\sqrt k$, not a new $4/3$-to-$3/2$ exponent improvement. It gives an unrestricted-weight mixed-gate tradeoff with $\Omega(n^{3/2}/\log^{5/2}n)$ heavily mixed gates below the coherent size threshold. This remains within the old survival template.

No stronger worst-case unrestricted gate exponent, new unrestricted support-wire bound, or coherent quadratic lower bound is established. No solver was launched. All experiments completed.

## Definitions and inherited state

Let $N=2^k$, $b_i=\bigoplus_{j=1}^m a_{i,j}$, and $A_{k,m}(x,a)=x_b$, with all $N+km$ raw inputs independent. Write the target sign as $f(x,a)=2x_b-1$. The circuit score is

$$F(x,a)=\sum_{j=1}^S v_j[\alpha_j\cdot x+w_j\cdot a\ge t_j]+u\cdot x+z\cdot a-\theta.$$

The output is $[F\ge0]$. Real coefficients and direct input wires at the top are allowed. Exact balance means $km=N$, $n=2N$; this can be taken along powers-of-two $k$, or replaced by $m=\lfloor N/k\rfloor$ and constant-factor asymptotic balance.

The starting upper bound is the research construction $d''$, with leading balanced size $5n^2/16$ bottom gates. The fixed-$k=3$ improvement does not change that asymptotic. The established unrestricted lower bounds are $\Omega(\varepsilon^2 n^{3/2}/\log^2n)$ gates and $\Omega(\varepsilon^2n^{5/2}/\log^{5/2}n)$ support wires in their documented ranges. Coherent and block-symmetric exact lower bounds are respectively $\Omega(n^2/\log^3n)$ and $\Omega(n^2/\log^{5/2}n)$.

I read `docs/RESEARCH_STATE.md`, `docs/CONTINUE.md`, `experiments/push_lower/report.md`, `experiments/review_lower/report.md`, `experiments/mixed_sign/report.md`, `experiments/maj_sol/report.md`, and the fixed-top follow-up in `workspace/worst_case_notes.md`. The reviewer corrections are essential: the coherent split bound is tight; construction (d) has about $5kN/8$ splitting gates per cube; uniform split arguments cannot reach a full quadratic coherent bound. The majority-survival obstruction is a limitation of a specified template, not a universal lower-bound barrier.

## Route 1: remove the spurious logarithm at small advantage

### 1.1 Fixed-direction restricted classes

Fix one restriction $\rho$ of the address inputs leaving one bit in every block alive, and fix its live positions. The remaining $k$ live bits form $z\in\{0,1\}^k$, a domain of size $N$. For a fixed table $x$, let $Q_\rho(x)$ be the number of bottom gates nonconstant on this cube.

For a survivor set $I\subseteq[S]$, the restricted output belongs to the class

$$\mathcal H_I=\left\{z\mapsto\operatorname{sgn}\left(\sum_{j\in I}v_j[\lambda_j\cdot z\ge\tau_j]+\mu\cdot z-\kappa\right):\tau_j,\kappa\in\mathbb R\right\}.$$

Here $\lambda_j,v_j,\mu$ are the original circuit coefficients restricted to the live inputs. They do not depend on $x$. All fixed inputs and constant gates can be absorbed into $\tau_j,\kappa$. Allowing these shifts independently only enlarges the class. In particular, we retain actual survivor identities and original top coefficients.

Let $\mathcal H_q=\bigcup_{|I|=q}\mathcal H_I$. On any $h$ domain points, a single fixed-direction threshold has at most $h+1$ patterns. Once all bottom patterns are fixed, varying $\kappa$ produces at most $h+1$ output patterns. Therefore the growth function satisfies

$$\Pi_{\mathcal H_q}(h)\le\binom Sq(h+1)^{q+1}.$$

For $q=0$, this is a chain of threshold sets in the fixed order of $\mu\cdot z$, and its VC dimension is at most one. For $1\le q\le S$, solving $2^h\le\binom Sq(h+1)^{q+1}$ gives

$$d_q:=\operatorname{VCdim}(\mathcal H_q)\le C_0\big(q\log(S+1)+1\big).\tag{1}$$

For clarity, use $\binom Sq\le(eS/q)^q$; the usual solution is $O(q\log(eS/q)+(q+1)\log(q+2))$, which is $O(q\log(S+1)+1)$. The $q=0$ case is handled directly, rather than estimated by $\log N$.

### 1.2 Fixed-design random-label complexity

For any class $\mathcal H\subseteq\{\pm1\}^N$ of VC dimension $d$, independent signs $\xi_1,\ldots,\xi_N$ satisfy

$$\mathbb E_\xi\sup_{h\in\mathcal H}\frac1N\sum_{c=1}^N\xi_ch_c\le C_1\sqrt{\frac{d+1}{N}}.\tag{2}$$

This is the fixed-design VC Rademacher bound, not an i.i.d.-sample generalization assertion. A proof uses the VC packing bound in normalized Hamming distance and the Rademacher entropy integral: the $L_2$ covering logarithm is $O(d\log(C/\eta))$, whose square-root integral over $0<\eta<2$ is $O(\sqrt d)$. Constant-function terms contribute $O(N^{-1/2})$.

Primary-source verification: Bartlett–Mendelson, *Rademacher and Gaussian Complexities: Risk Bounds and Structural Results*, [Theorem 6 and Lemma 4](https://jmlr.org/papers/volume3/bartlett02a/bartlett02a.pdf), give the fixed-sample VC Gaussian bound and comparison with Rademacher complexity. Haussler's [Boolean-cube packing theorem](https://www.cs.columbia.edu/~djhsu/coms4995-s20/haussler-packing.pdf) supplies the entropy estimate. These are standard ingredients; the Andreev application below is the present derivation.

For fixed $\rho$, the target vector is $\xi_c=2x_{c\oplus p(\rho)}-1$, hence genuinely independent uniform signs. Define

$$Z_q(\xi)=\sup_{h\in\mathcal H_q}\frac1N\sum_c\xi_ch_c.$$

Equation (2), then (1), imply, with $L=\log(S+1)$,

$$\mathbb E Z_q\le C_2\sqrt{\frac{qL+1}{N}}.$$

Changing one table sign changes $Z_q$ by at most $2/N$. Bounded differences gives

$$\Pr\left[Z_q>\mathbb E Z_q+\sqrt{2u/N}\right]\le e^{-u}.$$

### 1.3 Adaptive survivors: the necessary uniform step

The circuit's $Q_\rho(x)$ depends on $x$. Substituting $q=Q_\rho(x)$ into an expectation bound for a fixed $q$ would be invalid. Instead take $u=t+q+1$ and union over $q=0,\ldots,S$. Since $\sum_{q\ge0}e^{-(q+1)}<1$, simultaneously for every $q$, except with probability at most $e^{-t}$,

$$Z_q\le C_3\sqrt{\frac{qL+1+t}{N}}.\tag{3}$$

For $S\ge1$, the term $q$ from the union penalty is absorbed by $qL$. For $S=0$ use only $q=0$.

Equivalently, there is a nonnegative random variable $T_\rho(x)$ with $\Pr[T_\rho>t]\le e^{-t}$ and $\mathbb E T_\rho\le1$ such that (3) holds with $t=T_\rho(x)$ for all $q$ and all tables. One may define $T_\rho$ as the positive part of the maximum of $N(Z_q^+)^2/C_3^2-qL-1$.

The circuit's actual restricted correlation is at most $Z_{Q_\rho(x)}$. Thus, by Jensen, **without any independence assumption**,

$$\mathbb E_x\operatorname{corr}_\rho(x)\le C_3\sqrt{\frac{L\mathbb E_xQ_\rho(x)+2}{N}}.$$

Now average over the standard uniform address restriction (uniform live coordinate in each block, all other bits fixed independently uniformly). Uniform live inputs together with this restriction generate uniform raw addresses, exactly. Applying Jensen again, with $B=\mathbb E_{\rho,x}Q_\rho(x)$, gives the central inequality

$$2\varepsilon\le C_3\sqrt{\frac{B\log(S+1)+2}{N}}.\tag{4}$$

No union over restrictions is needed. This proves a general fixed-circuit random-table inequality independently of any particular survival theorem.

### 1.4 Consequence for ordinary Andreev

The archive's existing unrestricted restriction theorem gives, at balance,

$$B\le 4\sqrt2\,S\frac{k}{\sqrt N}.$$

Combining this inherited theorem with (4), there are absolute constants $c,C>0$ such that

$$S\log(S+1)\ge c\,\frac{\sqrt N}{k}\big(N\varepsilon^2-C\big).\tag{5}$$

The inequality is understood as vacuous when the right side is negative. For $\varepsilon\ge C'/\sqrt N$, with a sufficiently large absolute $C'$, and $S<N^2$, equation (5) yields

$$S=\Omega\!\left(\frac{\varepsilon^2N^{3/2}}{k^2}\right)
=\Omega\!\left(\frac{\varepsilon^2n^{3/2}}{\log^2n}\right).\tag{6}$$

When $S\ge N^2$, the conclusion is immediate. Floors with $km=\Theta(N)$ preserve these asymptotic statements and only change constants in the inherited survival estimate.

This is the strongest unrestricted result from this investigation. It is a new derivation relative to the supplied archive; no exhaustive novelty claim is made.

### 1.5 Sharp endpoint and limitations

With **zero bottom gates**, the top LTF can output majority of the table bits and ignore the address. Its advantage is

$$\varepsilon_0=\frac{\mathbb E|\xi_1+\cdots+\xi_N|}{2N}
=\frac{\binom N{N/2}}{2^{N+1}}=\Theta(N^{-1/2})\quad(N\text{ even}).$$

Therefore a positive lower bound for $S$ cannot uniformly extend to all advantages of order $N^{-1/2}$ with an arbitrarily small leading constant. The subtraction in (5) is necessary. This is the first sharp counterexample to test any further range claim against.

Random-sign high-survival gates do not refute (4): the survival estimate is unchanged. The gain removes an artificial complexity cost for a chain of thresholds and integrates the exceptional tail, rather than trying to reduce survival. The method still pays $q\log S$ for survivor identities, so it does not remove the balanced $\log^2n$ denominator at constant advantage.

The proof does **not** automatically extend the support-wire advantage range. Absorbing one-variable gates changes the live top coefficients as the table varies, so the zero-survivor class need no longer have VC dimension one. A wire version needs a separate growth bound for that enlarged class.

## Route 2: global parity-fiber span, with a complete sign-model theorem

### 2.1 Orthant lemma

For $b\in\{0,1\}^k$, let $\nu_b$ be the uniform distribution on raw addresses with block parities $b$. Define

$$\overline F_x(b)=\mathbb E_{a\sim\nu_b}F(x,a).$$

For an exact circuit, we can first shift the top threshold slightly to make every score strictly positive on outputs 1 and strictly negative on outputs 0. This is possible because the domain is finite. Averaging within a fiber preserves these strict signs:

$$\operatorname{sgn}\overline F_x(b)=2x_b-1.$$

**Lemma.** If a fixed linear subspace $V\subseteq\mathbb R^N$ contains $\overline F_x$ for every table $x$, then $V=\mathbb R^N$.

**Proof.** Otherwise choose nonzero $p\in V^\perp$. Choose a table with $2x_b-1=\operatorname{sgn}p_b$ whenever $p_b\ne0$, arbitrarily elsewhere. Then $\sum_b p_b\overline F_x(b)>0$, contradicting orthogonality. This uses the full independent table family. It does not apply to a generator family that omits the witness table. $\square$

This is an exact global correctness constraint. It involves the same bottom directions across all fibers and all tables, rather than counting each restriction separately.

### 2.2 Equal-magnitude address gates

Assume every nonzero address coefficient of gate $j$ has absolute value $\lambda_j>0$. Let $J_j$ be its address support, and $\epsilon_{j,i,t}\in\{\pm1\}$ its signs on that support. Set

$$Q_j=\{i:\{i\}\times[m]\subseteq J_j\},\qquad
\eta_{j,i}=\prod_{t=1}^m\epsilon_{j,i,t}\quad(i\in Q_j).$$

For a block set $R$, put $T_R=R\times[m]$ and $\chi_R(b)=(-1)^{\sum_{i\in R}b_i}$. Fourier projection onto parity fibers obeys

$$\widehat{\overline g_{j,x}}(R)=\mathbb E_a[g_j(x,a)\chi_{T_R}(a)].$$

After flipping negative-weight address inputs, the gate is symmetric on its $|J_j|$ supported address coordinates. Therefore, for $|R|=r$,

$$\widehat{\overline g_{j,x}}(R)=h_{j,rm}(x)\,v_{j,r}(R),\qquad
v_{j,r}(R)=\mathbf1[R\subseteq Q_j]\prod_{i\in R}\eta_{j,i}.\tag{7}$$

The scalar $h_{j,rm}(x)$ may depend arbitrarily on the table; the vector $v_{j,r}$ is fixed. If $T_R$ contains an unsupported coordinate, its coefficient is zero by averaging that independent bit. Otherwise symmetry makes the coefficient depend only on $rm$, and flipping signs supplies the displayed product.

When $m\ge2$, every individual address bit has conditional mean $1/2$ on every parity fiber. Hence direct raw-address top terms become constant in $b$. Table terms and bias are also constant. The degree-$r$ projection of $\overline F_x$, for $r\ge1$, consequently lies in

$$V_r=\operatorname{span}\{v_{j,r}:1\le j\le S\}.$$

The full score belongs to $\mathbb R\mathbf1\oplus\bigoplus_{r=1}^kV_r$. By the orthant lemma this containing subspace must equal $\mathbb R^N$. Thus

$$\operatorname{rank}[v_{j,r}(R)]_{R,j}=\binom kr,\qquad
S\ge\binom kr.\tag{8}$$

This proves the claimed **THR-at-top** theorem. It does not assume equality of the score to the target, controlled score amplitude, bounded top weights, or a normalized margin. The exact-sum theorem is not being transferred without justification: parity-fiber averaging and the all-orthant lemma supply the missing argument.

For $m=1$, direct address terms contribute degree one, so (8) remains valid as written for $r\ge2$; degree one needs those direct vectors included. The main balanced regime has $m\ge2$.

### 2.3 Necessary mixed-sign diversity and support

Gates with the same signature $(Q_j,\eta_j)$ contribute the same vector at every level, regardless of their threshold, table coefficients, magnitudes, or multiplicity. Consequently at least $\binom{k}{\lfloor k/2\rfloor}=\Omega(N/\sqrt k)$ distinct nonzero middle-level signature vectors are necessary. Repeating a ladder in a few fixed signatures cannot bypass this condition.

For gates with full address support, $Q_j=[k]$. Equation (8) says that at every level $r$, the Walsh evaluation matrix of their block sign-parity masks must have full row rank. There must be at least $\binom{k}{r}$ different masks even up to any identifications that produce proportional level-$r$ columns. This is much more specific than counting raw sign patterns: many distinct in-block masks have the same product signs and are indistinguishable by this obstruction.

For example, if $m$ is even and all these full-support gates are sign-coherent, then all $\eta_{j,i}=+1$. At level one their vectors coincide. Such gates cannot compute ordinary Andreev for $k\ge2$, no matter how many are used. This does not contradict the known upper constructions, which use different block supports and/or different coefficient magnitudes.

Also (8) forces $\#\{j:|Q_j|\ge r\}\ge\binom kr$. Thus, counting only bottom address support wires,

$$W_a\ge m\sum_{r=1}^k\max_{t\ge r}\binom kt=\Omega(mN\sqrt k).$$

Indeed the tail count at $r$ is nonincreasing and must dominate all later binomial requirements. This support-profile consequence is weaker than the known unrestricted **total** wire bound at balance; it is recorded as a structural statement, not as a new leading wire lower bound.

### 2.4 Several magnitudes and the first counterexample

If a gate has $d_j$ distinct nonzero address magnitudes, split its support into magnitude classes. For level $r$, the profile of $T_R$ is the vector of its intersection sizes with these classes. Let $P_j(r)$ count the profiles actually realized by supported $T_R$, $|R|=r$. The same argument gives

$$\binom kr\le\sum_jP_j(r),\qquad
P_j(r)\le\min\left(\binom kr,\binom{rm+d_j-1}{d_j-1}\right).\tag{9}$$

This extension also applies to THR-at-top, without a margin condition. Profiles can proliferate quickly; (9) does not imply $\Omega(Nm/V)$ for integer weights of magnitude at most $V$.

**Exact counterexample to a rank-one unrestricted extension:** take $k=m=2$ and address weights $(1,1,1,2)$. As the threshold varies, the unnormalized level-one coefficient vectors include $(-1,-1)$ and $(0,-2)$, which have rank two. One change from magnitude 1 to magnitude 2 already breaks the key rank-one property.

For fully unrestricted weights the obstruction is sharper: choose address coefficients $1,2,4,\ldots,2^{km-1}$. Threshold differences isolate individual raw addresses. After parity-fiber averaging, these differences include a nonzero multiple of every coordinate vector $e_b$. Thus the span of the threshold-shift family of **one** gate is already all $\mathbb R^N$. Allowing arbitrary independent threshold shifts loses all useful unrestricted rank information.

The remaining unrestricted research problem is to exploit that the actual threshold shift is the affine form $t_j-\alpha_j\cdot x$, shared across all tables. In particular it satisfies parallelogram identities on table faces. Any extension must retain this affine dependence; full span alone is insufficient.

### 2.5 Relation to the survivor obstruction

Random-sign majority gates can survive many restrictions, but at a fixed Fourier level each equal-magnitude gate still supplies only the single vector (7). High survival does not create missing directions. The theorem therefore genuinely lies outside the uniform-survival template. Its modest $N/\sqrt k$ size is the present limitation, not an invalidity caused by high survival.

## Route 3: a sharper arbitrary-weight count-restriction lemma

The randomized count restriction has an equivalent description: independently in each block choose a uniform live coordinate $\ell_i$, choose $q_i$ uniformly in $[0,1]$, and set all nonlive coordinates independently to Bernoulli($q_i$). This is the Beta-mixture identity proved in the archive.

Fix a gate, a table, and the live positions. Let $Y$ be the sum of all fixed address contributions. Set

$$L_0=\sum_i\min(0,w_{i,\ell_i}),\qquad d_i=|w_{i,\ell_i}|.$$

The gate splits precisely when its effective threshold lies in

$$\left(Y+L_0,\;Y+L_0+\sum_i d_i\right].$$

Partition this interval into $k$ consecutive half-open intervals of lengths $d_i$. These correspond to the monotone path from the minimum gate-score vertex to the maximum. A split is a crossing of exactly one path interval.

For interval $i$, rank all nonzero weights in block $i$ by decreasing absolute value, with ties broken deterministically. Suppose the live coordinate has rank $r$. The other $r-1$ earlier coordinates are fixed, have magnitude at least $d_i$, and, conditional on $q_i$, are independent Bernoulli($q_i$). All live endpoints on the path depend only on weights and live identities, not on those fixed Bernoulli bits.

Apply the equal-scale Kolmogorov–Rogozin bound at scale $d_i/2$ and cover the crossing interval by two such intervals. For $r\ge2$,

$$\Pr[\text{cross interval }i\mid\ell,q_i]
\le\min\left(1,\frac{2C_{KR}}{\sqrt{(r-1)\min(q_i,1-q_i)}}\right).$$

For $r=1$ use the bound 1, and for $d_i=0$ the crossing probability is zero. Since

$$\int_0^1\min(q,1-q)^{-1/2}\,dq=2\sqrt2,$$

averaging the uniform live coordinate among all $m$ positions gives, if block $i$ has $s_i$ nonzero weights,

$$\Pr[\text{cross interval }i]
\le\frac1m\left(1+4\sqrt2 C_{KR}\sum_{r=2}^{s_i}(r-1)^{-1/2}\right)
\le\frac{1+8\sqrt2 C_{KR}\sqrt{s_i}}m$$

when $s_i>0$, and zero otherwise. Summing over the $k$ intervals proves the useful support-sensitive form

$$p(g)\le\frac1m\sum_{i:s_i>0}(1+C\sqrt{s_i})\le C'\frac{k}{\sqrt m}.\tag{10}$$

The source inequality used here is the equal-scale concentration theorem stated in Juškevičius, [*The sharp form of the Kolmogorov–Rogozin inequality*](https://arxiv.org/abs/2201.09861). Negative weights do not affect the two-atom concentration calculation.

The distinction from the archived proof is consequential: that proof selects the globally largest live weight, pays a factor $k$ for the entire window and another $\sqrt k$ for the selected rank. Here each interval uses the rank of its **own block's live coordinate**. Its location may depend on other blocks, but those blocks can be conditioned on before applying concentration within block $i$.

Combining (10) with the archive's entropy requirement and minority-count runs bound gives

$$\sum_{j=1}^S\min\left\{\frac{k+2\mu_j}{m},\frac{Ck}{\sqrt m}\right\}\ge D_0(S),\qquad
D_0(S)=\frac{N-k-1-\log_2(S+1)}{k+\log_2(S+1)},\tag{11}$$

where $\mu_j$ is the sum over blocks of the minority-sign counts.

If $S\le D_0m/(4k)$, gates with $\mu_j<\mu_0=D_0m/(8S)$ contribute at most $D_0/2$ to (11). Hence at least

$$\Omega\left(\frac{D_0\sqrt m}{k}\right)
=\Omega\left(\frac{n^{3/2}}{\log^{5/2}n}\right)$$

gates have $\mu_j\ge\mu_0$. For $S\le n^{2-\delta}$ at balance, this threshold is $\mu_0=\Omega(n^\delta/\log^2n)$. Compared with the archived arbitrary-weight mixed-gate theorem, this saves $\sqrt{\log n}$; it removes the bounded-dynamic-range assumption previously needed for this denominator.

This does not improve the strongest unrestricted overall size bound. It is compatible with random-sign survivor examples, since $k/\sqrt m$ remains above their observed $\sqrt{k/m}$ scale. Applying it to average-case agreement under uniform raw inputs would require additional work: count restrictions do not generate uniform raw addresses.

## Bounded experiments and artifacts

`checks.py` uses only the Python standard library and exact integers/Fractions. It completed and wrote `checks.json` and `checks.log`.

- 72 signed-support equal-magnitude gate instances at $(k,m)=(2,2),(2,3),(3,2)$: all attainable threshold states satisfy the predicted level-by-level rank-one factorization, including zeros and mixed signs.
- Exact two-magnitude counterexample $(1,1,1,2)$: degree-one rank is two. This rejects the first false unrestricted extension.
- Exhaustive mask-subset search finds full-support signature sets attaining all necessary layer ranks with 2, 3 and 6 masks for $k=2,3,4$, respectively. These are **rank-condition witnesses**, not Andreev circuit constructions or sufficiency theorems.
- 30 exact randomized-count distributions at $(k,m)=(1,6),(2,3),(3,2)$, with heavy, zero and mixed weights: every split occurs on exactly one min-to-max path interval; the probability masses sum to one and the split probability equals the sum of crossing probabilities. These validate the decomposition, not an experimentally fitted concentration constant.

The proofs are analytical. Finite checks are guardrails, not substitutes for their universal claims.

## Ranked next actions and precise blockers

1. **Review Route 1 first.** Check the class growth bound with original top weights retained, the fixed-design use of VC complexity, and the adaptive $Q(x)$ tail argument. If accepted, record the improved gate advantage range $C/\sqrt n$ and its unavoidable additive constant. Do not claim a wire-range improvement. This is the highest-value concrete unrestricted advance here.
2. **Use Route 2 as a construction filter.** Before searching equal-magnitude mixed-mask pools, compute the rank of the signature matrices at every block Fourier degree. A deficient level supplies an explicit obstructing table: take a nonzero annihilating polynomial $p(b)$ and set $2x_b-1=\operatorname{sgn}p(b)$. This is cheap, exact, and tests the full ordinary table family. It can reject large pools without an SMT search.
3. **Pursue affine threshold coupling for unrestricted gates.** Keep the functions $h_{j,R}(t_j-\alpha_j\cdot x)$ jointly across table faces, rather than replacing each scalar by an independent parameter. Test any proposed rank/entropy lemma first against binary-place address weights, whose threshold family already spans all parity fibers, and against the $(1,1,1,2)$ two-magnitude counterexample. A successful lemma must charge the affine realization of threshold positions across tables, not merely their available span.
4. **Integrate Route 3 into the mixed-sign tradeoff after checking conditioning.** Its proof is short and addresses the archived rank-selection loss. Further improving survival alone cannot establish the desired unrestricted quadratic exponent. For coherent/block-symmetric quadratic bounds, the reviewer caps remain in force; a new theorem about the usefulness of high-split gates across tables is still needed.

No jobs were left running, no other directory was modified, and no commits or pushes were made.
