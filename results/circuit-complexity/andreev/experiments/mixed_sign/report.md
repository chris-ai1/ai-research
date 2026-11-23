# Mixed signs inside address blocks: depth-two threshold circuits for Andreev's function

Directory: `/tmp/andreev_gap/mixed_sign/`. All scripts run with `python3 -I` and add `/tmp/pydeps` themselves.
Notation follows the task:
- $N=2^k$ table bits $x_c$, and $k$ address blocks of $m$ bits, with block weights $s_i$.
- $b=s\bmod 2$, $A=x_b$, $n=N+km$; the balanced case is $km=N$.
- A circuit has $S$ bottom threshold gates and a top gate that reads the gates **and** the inputs.
- par$(M)$ is the least $S$ for PARITY of $M$ bits in the same model.

Labels used below:
- **[PROVED]**: complete proof in this file.
- **[VERIFIED]**: exact computation. SMT over the reals is z3 QF_LRA; every SAT model is re-checked with `Fraction` arithmetic on all points, and every UNSAT is a proof because all symmetry breaking is WLOG, as proved here.
- **[CONJECTURE]** / **[EVIDENCE]**: not proved.

## 0. Summary

### Goal 1: do mixed signs beat coherent circuits asymptotically?
- **At fixed $k$: no, unless depth-two parity has sublinear circuits.**
  - [PROVED] $\mathrm{size}(A_{k,m})\ge\mathrm{par}(km+1)$ for all gates (Prop. 1.1), while coherent circuits need $\Theta(m)$. So an $o(m)$ mixed-sign family at some fixed $k$ would give $o(M)$-gate depth-two parity circuits (Cor. 1.5).
  - [VERIFIED] **par$(M)=\lfloor M/2\rfloor$ for every $M\le9$**: exactly the coherent optimum (Prop. 1.2). For parity, mixed signs save **nothing** at these sizes, even though minimum circuits *with* genuinely mixed gates exist (§1.3).
- **Small $k=2$ instances: no full-model circuit beats the block-symmetric minimum** in any instance decided.
  - New all-gate lower bounds [VERIFIED]: $\mathrm{size}(A_{2,3})\ge4$ (previously 3), $\mathrm{size}(A_{2,m})\ge m$ for $m\le4$, and $\ge4$ for every $m\ge4$.
  - These exceed the coherent-only bound $m-1$. So for $m\le4$ no circuit, mixed or not, can go below the coherent lower bound.
  - **Still open:** whether full $(2,3)$ or the two-dictator sub-instance at $m=3$ can be done with 4 gates. Block-symmetric circuits need $\ge5$ and exactly $5$ respectively; the SAT searches did not finish (§4, §6).
- **Balanced case: open, but heavily constrained** [PROVED, Theorem 3.2].
  - Every circuit with fewer than about $n^2/(24\log_2^3n)$ gates contains $\Omega(n^{3/2}/\log^3n)$ non-coherent gates. This improves the $n^{4/3}$ of `push_lower` to the survival barrier $n^{3/2}$.
  - At $n^{2-\epsilon}$ gates, $\Omega(n^{3/2}/\log^3n)$ gates have minority count $\Omega(n^\epsilon/\log^2n)$.
  - Some block must carry $\ge\epsilon\log_2n-O(\log\log n)$ distinct sign patterns.
  - A bounded number of "views" per block (for example $s_i$ plus alternating sums) gains at most a constant factor, at most 2 for two views.

### Goal 2: lower bounds beyond coherent gates [PROVED]
- **Runs Lemma (2.1).** A gate with $\rho_i$ monotone runs per block under the arrangement splits at most $m^k-\prod_i(m-\rho_i)$ cubes. The bound is tight and was verified exactly on 1200 random gates.
- **Bounds for the four classes.** Balanced case, up to the factor shown; $D_0\approx N/(3k)$.

| class | bound |
|---|---|
| (a) globally orientable | every coherent bound transfers verbatim, including $S\ge m-1$ at $k=2$ |
| (b1) at most $r$ sign changes per block in a common order | $S\ge\frac{m(2^k-3k-1)}{3k^2(r+1)}$ |
| (b2) coherent after deleting at most $r$ bits per block | $S\ge\frac{m(2^k-3k-1)}{3k^2(2r+1)}$, valid for every arrangement, so it also enters the hybrid |
| (c) at most $r$ sign patterns per block | $S\ge\frac{m(2^k-3k-1)}{3k^2(2^{r-2}+1)}$ |
| (d) dynamic range $\le W$ | $p(g)=O(kW/\sqrt m)$ (Lemma 3.3); tight up to $k^{3/2}$ by the $\pm1$ barrier |

- **Arbitrary gates (Lemma 3.1).** $p(g)\le k/m+O(k^{3/2}/\sqrt m)$, improving $O(km^{-1/3})$. The hybrid Theorem 3.2 follows, and it reproves the worst-case Kane–Williams bound $\Omega(n^{3/2}/\log^3n)$.

### Goal 3: exact data [VERIFIED] (table in §5)
| instance | result |
|---|---|
| parity | full $=$ coherent $=$ block-symmetric $=\lfloor M/2\rfloor$ for $M\le9$; half-slicing hs$(M)=\lfloor M/2\rfloor$ for $M\le9$ |
| $A_{1,m}$ | full $=$ coherent $=$ block-symmetric $=\lceil m/2\rceil$ for $m\le8$; unit block weights suffice |
| $A_{2,1}$, $A_{2,2}$ | full $=$ coherent $=$ block-symmetric $=3$ |
| $A_{2,2}$, address weights in $\{-1,0,1\}$ | $\ge4$, both full and block-symmetric |
| $A_{2,2}$, address weights in $\{-2..2\}$ | $3$ |
| $A_{2,3}$ | full $\ge4$, coherent $\ge4$, block-symmetric $\ge5$; 6-table sub-instances already force 4 |
| two-dictator sub-instance, $m=3$ | block-symmetric $=5$, full $\ge4$ |
| random features at (2,3) | about 96 block-symmetric gates suffice, against about 416 mixed |

### Conjectures and evidence
- [CONJECTURE] par$(M)=\lfloor M/2\rfloor$ for all $M$. It would give $\mathrm{size}(A_{2,m})\ge m$.
  - The natural geometric route to it is a linear lower bound on hs$(M)$ (Prop. 1.4). That would already imply a linear lower bound for slicing all edges of the hypercube, an open problem whose best known lower bound is $n^{13/19}$.
  - The best known gate lower bound for depth-two parity is $\Omega(\sqrt n)$.
- [EVIDENCE] At fixed $k$, mixed signs give no gain at all: every exact value computed coincides with the coherent or block-symmetric optimum.


---

## 1. Parity is the core of the fixed-$k$ problem

### Proposition 1.1 (parity reduction) [PROVED]
For all $k,m$: $\ \mathrm{size}(A_{k,m})\ \ge\ \mathrm{par}(km+1)$. The parity circuit obtained keeps every address weight unchanged. So the inequality also holds inside any gate class that only constrains address weights: coherent, sign patterns, bounded address weights.

*Proof.* Restrict to the two tables $x_c=y\oplus(|c|\bmod 2)$, $y\in\{0,1\}$.
- Then $A=x_b=y\oplus\bigoplus_i b_i=y\oplus\bigoplus_{i,l}a_{i,l}$, which is PARITY of the $km+1$ bits $(y,a)$.
- In every gate, and in the top gate, $\alpha\cdot x=\sum_c\alpha_c(y+p_c-2yp_c)$ with $p_c=|c|\bmod2$. This is affine in $y$.
- So the restriction is a depth-two circuit of the same size on $(y,a)$, with the same address weights. ∎

For $k=2$ the restricted function is just parity: $A$ with the XOR/XNOR tables.

### Proposition 1.2 (coherent parity) [PROVED]
Suppose every bottom gate is monotone or antimonotone in all $M$ inputs (more generally, becomes so after flipping a fixed set of inputs). Then $S\ge\lfloor M/2\rfloor$. The symmetric circuit
$$|x|-2\sum_{j=1}^{\lfloor M/2\rfloor}[|x|\ge 2j]=|x|\bmod 2$$
shows that this is tight.

*Proof.*
1. Write $F=\sum_jv_jg_j+u\cdot x-\tau$, with output $[F\ge0]$. Flipping inputs maps parity to parity or its negation, so the flipped case reduces to this one.
2. Take a maximal chain $0=c_0<c_1<\dots<c_M$ with $c_t=c_{t-1}+e_{\sigma(t)}$.
3. If no gate changes value at step $t$, then $F$ changes by $u_{\sigma(t)}$. The parity change then forces $u_{\sigma(t)}>0$ for odd $t$ and $u_{\sigma(t)}<0$ for even $t$.
4. Every other step is a *switch step*. A monotone or antimonotone gate changes at most once along a chain, so there are at most $S$ switch steps.
5. Let $P=\{d:u_d>0\}$ and $Q$ its complement. Put the coordinates of $Q$ at odd steps and those of $P$ at even steps, as far as possible.
6. This forces $\min(|Q|,\lceil M/2\rceil)+\min(|P|,\lfloor M/2\rfloor)\ge\lfloor M/2\rfloor$ switch steps. ∎

### Proposition 1.3 (exact parity minima) [VERIFIED] (`parity_min.py`, logs `logs/par_*.log`)

| $M$ | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|
| par$(M)$ | 1 | 1 | 2 | 2 | 3 | 3 | **4** | **4** | 4 or 5 (S=4 undecided after 55 min; still running) | $\ge4$ (run stopped) |
| time of the refuting run ($S=\lfloor M/2\rfloor-1$) | <0.1 s | <0.1 s | <0.1 s | <0.1 s | <0.1 s | 0.1 s | 6.3 s | 15.6 s | | |
| hs$(M)$ (Prop. 1.4) | – | – | 2 | 2 | 3 | 3 | **4** | **4** | | |

The upper bound $\lfloor M/2\rfloor$ comes from the symmetric circuit; the solver also returns SAT at $S=\lfloor M/2\rfloor$ for $M\le7$. For $M\le9$ the minimum is therefore exactly $\lfloor M/2\rfloor$, the value forced on coherent circuits by Prop. 1.2.

Symmetry breaking, all WLOG:
- **Top weights.** Complementing a gate maps $(\alpha,\theta,v)\mapsto(-\alpha,1-\theta,-v)$ and $\tau\mapsto\tau-v$, and gates can be permuted. So $0\le v_1\le\dots\le v_S$.
- **Direct weights.** Let $T_d$ = flip input $d$, then negate the whole circuit; negation is followed by complementing all gates to restore $v\ge0$.
  - $T_d$ maps a parity circuit to a parity circuit. Its only effect on $u$ is to flip the sign of **every $u_{d'}$ with $d'\ne d$**.
  - $T_dT_{d'}$ flips exactly $u_d$ and $u_{d'}$.
  - For even $M$, every sign pattern is reachable, so $u\ge0$ WLOG; sorting by input permutation then gives $0\le u_1\le\dots\le u_M$.
  - For odd $M$, only even-size flips are available, so $u_2,\dots,u_M\ge0$ and $u$ is sorted.
- **Cross-checks.**
  - Re-running without the $u$-normalisation (only $v$ sorted, and with no symmetry breaking at all) gives the same UNSAT answers for $M\le7$ (`parity_nosym.py`).
  - For $M=8$, par$(8)\ge4$ also follows from hs$(8)\ge4$ (Prop. 1.4). That is a different encoding (`halfslice.py`, no top gate, no $v$/$u$ variables) that uses only the $u\ge0$ normalisation.
  - par$(9)\ge$ par$(8)$ by restriction.

**Mixed gates are possible but useless at these sizes** (`parity_rigid.py`). Minimum circuits **with** a genuinely mixed gate exist for $M=4,\dots,7$. With margin-1 normalisation, a relevant variable has $|w|\ge1$, so "genuinely mixed" means relevant variables of both signs. For example, for $M=4$:
$$g_0=[-x_0-x_1-3x_2-x_3\ge-3],\qquad g_1=[x_2-x_0-x_1-x_3\ge-1],\qquad \text{top }[2g_0+2g_1+|x|\ge5].$$
Mixed signs are usable, but they never save a gate here.

### Proposition 1.4 (half-slicing) [VERIFIED for $M\le9$] (`halfslice.py`)
**Necessary condition.** Let $M$ be even and normalise $u\ge0$. Then every edge $(x,x+e_d)$ with $|x|$ odd must be cut by a bottom gate: otherwise $F$ changes by $u_d\ge0$ along the edge and cannot become negative. So $\mathrm{par}(M)\ge \mathrm{hs}(M)$, the least number of hyperplanes cutting all edges of
$$E_1=\{(x,x+e_d):x_d=0,\ |x|\text{ odd}\}.$$

**Computation.** hs$(M)=\lfloor M/2\rfloor$ for $M\le9$. This is UNSAT at $\lfloor M/2\rfloor-1$; the hyperplanes $|x|=2j-\tfrac12$ give the upper bound.

**Consequence.** Already the geometric part of the problem (no top gate) is tight for these $M$.

**Barrier for this route.** Every hyperplane family cutting **all** edges of the cube cuts $E_1$. So a linear lower bound hs$(M)\ge cM$ would prove the conjectured linear lower bound for slicing all edges of the hypercube.
- The best known slicing bounds are a lower bound of $n^{13/19}$ up to logs (Sauermann–Xu 2025, improving Klein's $\tilde\Omega(n^{2/3})$) and an upper bound of $\lceil5n/6\rceil$ (Paterson).
- For depth-two threshold circuits computing parity, the best known gate lower bound is $\Omega(\sqrt n)$ (Impagliazzo–Paturi–Saks; tight on average by Kane–Williams).
- So par$(M)=\lfloor M/2\rfloor$ for all $M$ is open, and the natural geometric route to it is at least as hard as the slicing conjecture.

### Corollary 1.5 (fixed $k$: what mixed signs can and cannot do)
1. **[PROVED]** If $\mathrm{size}(A_{k_0,m})=o(m)$ for some fixed $k_0$, then par$(M)=o(M)$ (par is monotone in $M$ by restriction). In words: *mixed signs can beat coherent circuits asymptotically at fixed $k$ only if depth-two parity has sublinear circuits.* Coherent circuits need $\Omega(m)$ for every fixed $k\ge2$, by Theorem E of `push_lower` applied to a 2-block sub-table.
2. **[VERIFIED]** For $M\le9$, mixed signs give no saving at all for parity: par $=\lfloor M/2\rfloor$ equals the coherent minimum of Prop. 1.2.
3. **[VERIFIED + PROVED]** New full-model lower bounds:
   - $\mathrm{size}(A_{1,m})\ge\mathrm{par}(m+1)=\lceil m/2\rceil$, so $\mathrm{size}(A_{1,m})=\lceil m/2\rceil$ for $m\le8$ (upper bound: `push_upper`, §3.4).
   - $\mathrm{size}(A_{2,m})\ge\mathrm{par}(2m+1)=m$ for $m\le4$. This is **above** the coherent bound $m-1$ of Theorem E, and it holds for all gates.
   - The task's targets "≤4 or ≤5 gates for $m=6..10$": since $\mathrm{size}(A_{2,m})\ge\mathrm{par}(9)=4$ for every $m\ge4$, **≤3 gates is impossible for all $m\ge4$**. Excluding 4 gates for $m\ge5$ needs par$(10)\ge5$ or par$(11)\ge5$. par$(10)\ge5$ (S=4) was undecided after 55 min, so this work does **not** exclude 4 gates for $m\ge5$. The same holds for 5 gates, which would need par$(12)\ge6$.

---

## 2. Lower bounds beyond coherent gates (count restriction)

The setting is the count restriction of `push_lower` §1:
- an arrangement $\sigma$ (one permutation per block);
- a unit cube $c$ of the $s$-grid;
- one live bit per block;
- block functions $P_i(s)=\sum_{t\le s}\gamma_{i,\sigma_i(t)}$;
- $d_c(x)$, the number of bottom gates that split $c$.

Theorem A of `push_lower` gives $\mathbb E_x d_c(x)\ge D_0(S)=\frac{2^k-k-1-\log_2(S+1)}{k+\log_2(S+1)}$ for **every** $\sigma$ and $c$. For $S<2^{2k}$, $D_0\ge\frac{2^k-3k-1}{3k}$.

### Lemma 2.1 (Runs Lemma) [PROVED; VERIFIED in exact integers, `runs_lemma_check.py`]
Fix a gate $g$ and an arrangement $\sigma$. Let $\rho_i=\rho_i(g,\sigma)$ be $1+{}$the number of sign changes of the step sequence $(\gamma_{i,\sigma_i(1)},\dots,\gamma_{i,\sigma_i(m)})$, with zeros ignored. This is the number of maximal *runs* on which $P_i$ is monotone. Then, for every table $x$, $g$ splits at most
$$m^k-\prod_{i=1}^k(m-\rho_i)\ \le\ m^{k-1}\sum_i\rho_i$$
unit cubes. Lemma B1 of `push_lower` is the case $\rho\equiv1$.

*Proof.*
1. **Boxes.** The runs of block $i$ partition the cube coordinates $c_i\in\{0..m-1\}$ (cube $c_i$ uses step $c_i+1$) into $\rho_i$ intervals $I_{i,1},\dots$ of lengths $\ell_{i,p}$. A *box* is a product $B=\prod_iI_{i,p_i}$.
2. **Monotone in a box.** Inside $B$ every step in direction $i$ has sign $\varepsilon_i$ or is zero. So $F=\sum_iP_i$ restricted to the vertices of the cubes of $B$ is monotone in direction $\varepsilon$.
3. **Splitting condition.** On cube $c$ the gate is $[\lambda\cdot z\ge\theta-\alpha x-F(c)]$ with $\lambda_i=\gamma_{i,\sigma_i(c_i+1)}$. It is split iff $F(c^-)<\theta-\alpha x\le F(c^+)$, where $c^\pm=c+(\mathbf 1\pm\varepsilon)/2$.
4. **Lines.** On a line $c_t=c_0+t\varepsilon$ inside $B$ we have $c_t^+=c_{t+1}^-$. So the half-open intervals $(F(c_t^-),F(c_t^+)]$ are disjoint, and at most one cube per line is split.
5. **Counting lines.** $B$ contains $\prod_i\ell_{i,p_i}-\prod_i(\ell_{i,p_i}-1)$ such lines: count the cubes $c\in B$ with $c-\varepsilon\notin B$.
6. **Sum over boxes.** This gives $m^k-\prod_i\sum_p(\ell_{i,p}-1)=m^k-\prod_i(m-\rho_i)$. ∎

*Check.* 1200 random gates were tested, from five weight families (coherent, few runs, two minority bits, uniform random, heavy-tailed), with random arrangements and $(k,m)\in\{(2,4),(2,6),(2,9),(3,3),(3,5),(4,3),(4,4),(5,3)\}$. The maximum over **all** thresholds was found by an exact sweep. There were no violations, and the bound was **attained** in 121 cases, so it is tight.

### Corollary 2.2 (one arrangement for all gates) [PROVED]
If a single arrangement gives $\rho_i(g,\sigma)\le\rho$ for every gate and block, then $S\,k\rho/m\ge D_0(S)$. Hence
$$S\ \ge\ \frac{m\,(2^k-3k-1)}{3k^2\rho},\qquad\text{balanced: }\ S\ge\frac{N(N-3k-1)}{3k^3\rho}.$$

### The classes of the task
**(a) Globally orientable** [PROVED]. Suppose some flip pattern $\phi\in\{0,1\}^{km}$ makes every gate coherent.
- Set $f_i=|\phi_i|\bmod2$ and $C'(x,a)=C\big((x_{c\oplus f})_c,\ a\oplus\phi\big)$.
- Then $C'(x,a)=A\big((x_{c\oplus f})_c,a\oplus\phi\big)=x_{(b\oplus f)\oplus f}=x_b$, so $C'$ computes $A$ with the same number of gates.
- In $C'$ the weight of $a_{i,l}$ is $(-1)^{\phi_{i,l}}\gamma_{i,l}$, so every gate of $C'$ is coherent; the table weights are permuted and the thresholds shifted.

So **every coherent bound transfers verbatim**: Corollary C of `push_lower`, and Theorem E ($k=2$, $S\ge m-1$). For Theorem E, the XOR table goes to the XOR or XNOR table, and the proof covers both.

**(b1) At most $r$ sign changes per block in a common order** (after an optional global flip): use that order as $\sigma$. Then $\rho\le r+1$, and
$$S\ge\frac{m(2^k-3k-1)}{3k^2(r+1)}.$$

**(b2) Coherent after deleting at most $r$ bits per block** (the deleted bits may depend on the gate). Let the *minority count* of a block be $\mu_i(g)=\min(\#\{\gamma_{i,l}>0\},\#\{\gamma_{i,l}<0\})$. Each minority bit creates at most two sign changes, so $\rho_i\le 2\mu_i+1$ **for every arrangement**. Hence
$$S\ge\frac{m(2^k-3k-1)}{3k^2(2r+1)},$$
and the per-gate bound $p(g)\le(k+2\mu(g))/m$, with $\mu(g)=\sum_i\mu_i(g)$, also enters the random-arrangement hybrid (Theorem 3.2).

**(c) At most $r$ distinct sign patterns per block** (sign vectors, up to negation; arbitrary magnitudes).
- *Zeros.* Replacing zeros by $+$ can only increase the number of sign changes, so take the patterns in $\{\pm\}^m$.
- *Flip.* Flip the bits where pattern 1 is $-$, as in (a). Then the bits fall into at most $2^{r-1}$ *atoms* (equal sign vector under patterns $2..r$).
- *Order.* Order the atoms along a reflected Gray code on $r-1$ bits. Coordinate $j$ of that code changes $2^{r-2-j}$ times, so every pattern has at most $2^{r-2}$ sign changes, and $\rho\le2^{r-2}+1$ for $r\ge2$.
- *Bound.* $$S\ge\frac{m(2^k-3k-1)}{3k^2(2^{r-2}+1)}.$$

Consequences:
- *Two views per block.* Gates that see each block through $s_i$ or through the alternating sum $\sum_l(-1)^la_{i,l}$ (any magnitudes, either sign) form a class with $r=2$, so $\rho\le2$. Such views gain **at most a factor 2** over coherent circuits.
- *Many patterns are needed.* A balanced circuit with $S\le n^{2-\epsilon}$ needs $2^{r-2}+1\ge n^{\epsilon}/(12k^3)$, i.e. $r\ge\epsilon\log_2n-3\log_2\log_2n-O(1)$ distinct sign patterns in some block.

**(d) Weight-bounded mixed gates.** These are covered by §3, where the bound holds for arbitrary weights. The barrier of `push_lower` (Prop. F) shows that it cannot be improved for $\pm1$ gates by survival arguments: they survive every one-live-bit restriction with probability $\ge1/(2\sqrt{2km})$. So bounded weights earn no better coefficient than arbitrary mixed gates, up to a factor $O(k^{3/2})$ (Lemma 3.3).

**$k=2$ version** [PROVED]. Assume one arrangement gives at most $(\rho_1,\rho_2)$ runs for every gate.
- Inside each box the gate is coherent, so by the Ring Lemma at most 4 of the box's boundary squares are corner cuts.
- Each global side meets a box in a segment on which the monotone mixed path turns at most twice.
- So one gate corner-cuts at most $4\min(\rho_1\rho_2,\rho_1+\rho_2)$ of the $4(m-1)$ boundary squares. With the XOR table every square needs a corner cut, so
$$S\ge\frac{m-1}{\min(\rho_1\rho_2,\rho_1+\rho_2)}.$$
- For $\rho=(1,1)$ this is Theorem E. For **arbitrary** gates, Prop. 1.1 gives the stronger $S\ge$ par$(2m+1)$ (§1).

---

## 3. Arbitrary gates: a sharper survival lemma and the hybrid theorem

The *randomised count restriction* takes uniform independent arrangements $\sigma_i$ and a uniform cube $c$. By the Beta-integral identity (`push_lower`, Lemma B3, step 1):
- the live bit $\ell_i$ of each block is uniform;
- given $\ell_i$, the other bits of the block are i.i.d. Bernoulli$(q_i)$ with $q_i\sim U[0,1]$;
- the blocks are independent.

### Lemma 3.1 (improved Lemma B3) [PROVED; Monte Carlo consistent, `survival_mc2.py`]
For **every** threshold gate $g$ (any real weights) and every fixed table $x$,
$$p(g):=\Pr_{\sigma,c}[g\text{ splits }c]\ \le\ \frac km+8\sqrt2\,C_{KR}\,k\sqrt{\frac{k}{m}}\,(1+o(1))\ =\ \frac km+O\!\Big(\frac{k^{3/2}}{\sqrt m}\Big).$$
Here $C_{KR}$ is the Kolmogorov–Rogozin constant. This improves the $O(km^{-1/3})$ of Lemma B3 in `push_lower`, which was its "most promising next step".

*Proof.*
1. **Split event.** Given the live bits $\ell$ and the fixed parts, put $\lambda_i=\gamma_{i,\ell_i}$ and $\Phi=\sum_i\sum_{l\in F_i}\gamma_{i,l}$. The gate is split iff $\Phi$ lies in a half-open interval $J$ of length $\Lambda=\sum_i|\lambda_i|$. If $\Lambda=0$ there is no split.
2. **The heaviest live bit.** Let $w_i=|\lambda_i|$, $i_0=\arg\max_iw_i$, $w^*=w_{i_0}>0$. Let $R=R_{i_0}(\ell_{i_0})$, where $R_i(l)=\#\{l':|\gamma_{i,l'}|\ge|\gamma_{i,l}|\}$. Block $i_0$ has $R-1$ **fixed** bits of weight $\ge w^*$.
3. **Anti-concentration.** Condition on $\ell$, $q_{i_0}$ and all other blocks. Kolmogorov–Rogozin with every $\lambda_l=w^*/2$ gives $Q(\Phi;w^*/2)\le C_{KR}/\sqrt{(R-1)\min(q,1-q)}$. Each of those $R-1$ summands $\gamma_l\xi_l$ has $1-Q(\cdot\,;w^*/2)=\min(q,1-q)$.
4. **Covering.** $|J|=\Lambda\le kw^*$, so $J$ is covered by $2k$ intervals of length $w^*/2$. Integrating over $q\sim U[0,1]$, with $\int_0^1\min(q,1-q)^{-1/2}dq=2\sqrt2$:
$$\Pr[\text{split}\mid\ell]\le h(R-1),\qquad h(y)=\min\big(1,\ A\,y^{-1/2}\big),\quad A=4\sqrt2\,k\,C_{KR}.$$
5. **Ranks.** At most $r$ indices $l$ satisfy $R_i(l)\le r$. Since $R\ge\min_iR_i(\ell_i)$ and $\ell_i$ is uniform, $\Pr[R-1\le y]\le k(y+1)/m$.
6. **Average over $\ell$.** $h$ is non-increasing, so $\mathbb E\,h(R-1)$ is at most its value for the stochastically smallest law allowed by step 5. That law is uniform on $\{0,\dots,\lceil m/k\rceil-1\}$, giving
$$\mathbb E\,h(R-1)\le\frac km\Big(1+A\sum_{y=1}^{\lceil m/k\rceil}y^{-1/2}\Big)\le\frac km+2A\sqrt{\frac km}\,(1+o(1)).$$ ∎

The old proof truncated at a **fixed** rank $r$, which cost $kr/m$; using the live bit's own rank removes that trade-off.

*Monte Carlo* (`survival_mc2.py`). Seven weight profiles were tested: balanced $\pm1$, signed and unsigned geometric, Gaussian, one huge weight, Cauchy, and $\sqrt m$ heavy weights; the threshold was maximised over a grid, with $k\in\{2,3,4\}$ and $m\in\{16,64,256\}$. The ratio $p\sqrt m/k^{3/2}$ stays at most $0.52$ throughout. Balanced $\pm1$ gates sit at $p\approx\sqrt{k/m}$ (for example 0.092 against 0.088 at $k=2$, $m=256$).

### Theorem 3.2 (hybrid) [PROVED]
Average Theorem A over the randomised count restriction. With Lemmas 2.1 and 3.1, every circuit computing $A_{k,m}$ satisfies
$$\sum_{g}\ \min\Big(\frac{k+2\mu(g)}{m},\ \frac km+C_1\frac{k^{3/2}}{\sqrt m}\Big)\ \ge\ D_0(S).$$
In the balanced case, with $D_0\ge\frac{N-3k-1}{3k}$ and $m=N/k$:
1. **All circuits.** $S=\Omega(n^{3/2}/\log^3n)$. This reproves the worst-case Kane–Williams bound, with the same polylog, and is a consistency check against the survival barrier.
2. **Many mixed gates.** If $S<D_0m/(2k)\approx n^2/(24\log_2^3n)$, then at least $\frac{D_0\sqrt m}{4C_1k^{3/2}}=\Omega(n^{3/2}/\log^3n)$ gates are **not** coherent. This is the target named in `push_lower` §7.1: *every circuit has $\tilde\Omega(n^{3/2})$ mixed-sign gates or $\tilde\Omega(n^2)$ gates.*
3. **Heavily mixed.** If $S=n^{2-\epsilon}$ (any $\epsilon>0$, $n$ large), then $\Omega(n^{3/2}/\log^3n)$ gates have total minority count $\mu(g)\ge D_0m/(8S)=\Omega(n^{\epsilon}/\log^2n)$. Split the gates at $\mu_0=D_0m/(8S)$: those below $\mu_0$ contribute $<D_0/2$.


### Lemma 3.3 (bounded dynamic range: class (d)) [PROVED]
Let the nonzero address weights of $g$ satisfy $1\le|\gamma_{i,l}|\le W$ after scaling, e.g. integer weights in $[-W,W]$. Let $r^*\ge2$ be the largest number of nonzero weights in one block, attained at block $i^*$. Then, under the randomised count restriction,
$$p(g)\ \le\ \big(2\,\mathbb E\Lambda+\Pr[\Lambda>0]\big)\frac{2\sqrt2\,C_{KR}}{\sqrt{r^*-1}}\ \le\ \frac{(2W+1)\,k\,r^*}{m}\cdot\frac{2\sqrt2\,C_{KR}}{\sqrt{r^*-1}}\ =\ O\!\Big(\frac{kW}{\sqrt m}\Big).$$
If $r^*=1$ the gate is coherent and Lemma B1 applies.

*Proof.*
1. **Fixed block.** Use block $i^*$, which is fixed and does not depend on $\ell$. Given $\ell$, its fixed bits include at least $r^*-1$ nonzero weights of magnitude $\ge1$.
2. **Anti-concentration.** Kolmogorov–Rogozin with $L=\tfrac12$ gives $Q(\Phi_{i^*};\tfrac12)\le C_{KR}/\sqrt{(r^*-1)\min(q,1-q)}$.
3. **Covering.** The window $J$ has length $\Lambda=\sum_i|\gamma_{i,\ell_i}|$ and is covered by $2\Lambda+1$ intervals of length $\tfrac12$; when $\Lambda=0$ there is no split.
4. **Expectations.** $\mathbb E\Lambda=\|\gamma\|_1/m\le Wkr^*/m$ and $\Pr[\Lambda>0]\le kr^*/m$. Integrate over $q$, using the factor $2\sqrt2$. ∎

For $\pm1$ gates this gives $p=O(k/\sqrt m)$. The barrier (Prop. F of `push_lower`) gives $p\ge1/(2\sqrt{2km})$ for suitable $\pm1$ gates under **every** one-live-bit restriction. So for weight-bounded gates the survival coefficient is $\Theta(\sqrt{1/m})$ up to a factor $k^{3/2}$, and no survival-based argument can give them a better coefficient.

**Hybrid for (d).** Theorem 3.2 holds with the per-gate term $\min\big(\frac{k+2\mu(g)}m,\ \frac km+C_1\frac{k^{3/2}}{\sqrt m},\ C_2\frac{kW(g)}{\sqrt m}\big)$. Suppose a balanced circuit has $S<D_0m/(2k)$ and all its non-coherent gates have dynamic range $\le W$. Then it has at least
$$\frac{D_0\sqrt m}{2C_2kW}=\Omega\Big(\frac{n^{3/2}}{W\log^{5/2}n}\Big)$$
such gates. For MAJ-like bottom gates, $W=O(1)$, this is slightly stronger than the general $n^{3/2}/\log^3n$.

In short, a sub-quadratic circuit must contain $\tilde\Omega(n^{3/2})$ gates that are heavily mixed in at least one block, and must use $\gtrsim\epsilon\log n$ sign patterns in some block (class (c)).

---

## 4. Goal 1: searching for mixed-sign circuits that beat block-symmetric ones

### 4.1 What a winning circuit would need (all PROVED above)
- **Fixed $k$.** Mixed signs can only change the constant (Cor. 1.5). For $k=2$ a circuit needs at least $\mathrm{par}(2m+1)$ gates, which equals $m$ for $m\le4$. An $o(m)$ family would give sublinear depth-two parity circuits, which is open and contradicted by every exact value computed.
- **Balanced case.** Below $n^2/(24\log_2^3n)$ gates, a circuit must contain $\tilde\Omega(n^{3/2})$ non-coherent gates (Thm 3.2(2)). At $n^{2-\epsilon}$ gates these must be heavily mixed, with minority count $\tilde\Omega(n^\epsilon)$ (Thm 3.2(3)), and the circuit must use $\gtrsim\epsilon\log_2n$ sign patterns in some block (class (c)). Constructions built from a bounded number of "views" of a block, such as $s_i$ plus alternating sums, can win at most a constant factor.

### 4.2 Small sizes: methods
| method | script | outcome |
|---|---|---|
| z3 QF_LRA, full model, symmetry breaking ($v$ sorted $\ge0$; $u_{i,l}\ge0$ and sorted inside blocks, via single-bit flips + table permutation) | `andreev_min.py` | much faster on known cases: full (2,2) S=2 is UNSAT in 1.6 s, against 48.4 s with **no** symmetry breaking (`--nosym`, same answer; `logs/f22_S2_nosym.log`). Proves full(2,3) $\ge4$ (§5). |
| sub-instances: table sets closed under $c\mapsto c\oplus e_i$, so the symmetry breaking stays valid and UNSAT transfers to $A$ | `andreev_min.py --tables` | 6 tables suffice to force 4 gates at (2,3) (177 s) |
| **table-CEGAR**: solve on a closed table set, add the orbit of a failing table, repeat (incremental z3) | `table_cegar.py` | (2,3), S=4, starting from XOR $\cup$ single-1: round 1 (6 tables) SAT in 216–438 s, and the circuit fails on 8–9 of the other 10 tables; round 2 (8–10 tables) was undecided after about 50 min (2 seeds). S=5: round 1 undecided after 39 min. |
| point-CEGAR | `mscore.solve_cegar` | no gain on these instances (as found before in `verify_opus`) |
| CP-SAT with bounded integer weights (SAT-finder only) | `cpsat_find.py` | (2,2) S=3 found with $W=2$ in 97 s; UNKNOWN in 120 s on the two-dictator instance at S=5, which is feasible for block-symmetric circuits. Too slow |
| redundant edge clauses: with $u_{i,l}\ge0$ and $v\ge0$, an address edge on which the output drops $1\to0$ needs a gate that turns off | `andreev_min.py --edgeclauses`, `parity_min2.py` | about 1.5–2× on UNSAT proofs; (2,3) 6-table sub-instance S=3: 122 s against 177 s |
| smooth relaxation (sigmoid hidden units + skip connections, annealed to steps; truth tables then certified by exact LPs in z3 and `Fraction` re-check) | `nnsearch.py` | finds (2,2) S=3 in seconds; on (2,3) the best training error stayed at 44–133 of 1024 points for S=4..6. For block-symmetric S=11 it found an exactly verified 11-gate circuit with non-axis directions such as $2s_1+15s_2$ and $s_1-5s_2$ (`logs/nn23_bs_S11.log`). That equals Theorem G's count, so it is no improvement. At S=9 the best error was 8. On the two-dictator instance with S=4 (256 points), 3 runs of about 1500–1900 restarts each reached error **2** but never 0. **LNS repair** (`lns_repair.py`) froze the gate truth tables except within address distance $\le3$ of the errors (up to 100 free points) and solved exactly; it was UNSAT every time. This is heuristic evidence that 4 gates do not suffice there. |
| coherent model (Boolean sign per gate and block) | `andreev_min.py --cls coherent` | used for the coherent columns. (2,3) S=4 was undecided after 87 min; the two-dictator instance at $m=3$, S=4, was undecided after 44 min. |
| block-symmetric model on reduced points $(x,s)$ | `andreev_min.py --cls bsreduced` | reproduces (2,2)=3 in 4 s and gives the two-dictator value $=5$ at $m=3$ (S=4 UNSAT 108 s, S=5 SAT 30 s). (2,3) S=5 (point-CEGAR, a block-symmetric SAT search) was undecided after 68 min, so the best known (2,3) circuit still has 11 gates. |

### 4.3 What the found circuits look like
- The 4-gate circuit for the 6-table sub-instance of (2,3) (`logs/sub23_S4_x1.log`) is heavily mixed. Its block-1 weights are, for example, $(-6,-7,22)$ and $(19,-22,-16)$.
- The 3-gate full (2,2) circuits found by the solver and by the relaxation are also mixed, e.g. block weights $(-7,7)$ and $(-10,19)$. But block-symmetric circuits reach 3 as well.
- Minimum **parity** circuits can contain genuinely mixed gates (§1.3) without saving anything.

Mixed signs are therefore *available* to optimal circuits, but in every instance decided so far they do not lower the gate count below the coherent/block-symmetric optimum (parity, $k=1$, (2,1), (2,2)).

### 4.4 What mixed signs compute
1. **Inside one block.** A gate sees block $i$ only through $L_i=\sum_l\gamma_{i,l}a_{i,l}$.
   - With odd integer weights, $L_i\equiv s_i\pmod 2$. Parity is visible through $L_i$ exactly as through $s_i$; for example, the alternating sum takes the values $\{-\lfloor m/2\rfloor,\dots,\lceil m/2\rceil\}$.
   - The range of $L_i$ is still $\sum_l|\gamma_{i,l}|\ge m$. A staircase on $L_i$, which is how all constructions extract parity, costs range$/2$, the same as on $s_i$.
2. **Along one arrangement.** $P_i$ is the prefix walk of the weights.
   - A monotone walk (coherent gate) gives at most one split per line, a $\le k/m$ fraction of the cubes.
   - A pattern that alternates *along that arrangement* makes $P_i$ a function of $s_i\bmod2$, and the gate can split every cube. That is the precise sense of "a mixed gate splits many cubes of a fixed arrangement".
3. **Over all arrangements.** The circuit must work on every input, i.e. on every arrangement simultaneously.
   - A gate with minority count $\mu$ has at most $1+2\mu$ runs on every arrangement (Lemma 2.1, class (b2)).
   - Lemma 3.1 caps every gate at $O(k^{3/2}/\sqrt m)$ split probability; balanced $\pm1$ gates achieve $\Theta(\sqrt{k/m})$.
   - So a mixed gate is a *random-walk view* of the block: it splits a $\sqrt{k/m}$ fraction of the cubes, against $k/m$ for a monotone view.
   - Whether these thinly spread splits can be made *useful* simultaneously is exactly the open $n^{3/2}$ vs $n^2$ question. Survival-type counting cannot decide it.
4. **The parity analogue.** A balanced gate switches $\Theta(\sqrt M)$ times along a random chain, a monotone gate once. Yet the exact minimum stays $\lfloor M/2\rfloor$ for $M\le9$: the extra switches could not be coordinated across chains.

## 5. Exact data (Goal 3)

All entries are exact SMT over the reals with the WLOG symmetry breaking proved in §1.3 and in the `andreev_min.py` docstring. "$\ge s$" means $S=s-1$ was refuted (UNSAT is a proof); "$=s$" also has a verified SAT circuit.
- *full*: arbitrary real weights.
- *coherent*: per-gate, per-block sign chosen by the solver.
- *b-sym*: block-symmetric.
- *addr W*: integer address weights in $[-W,W]$ with real table weights. This restricts only the address side, so it is weaker than bounding all bottom weights as `bigw/wmin.py` does; UNSAT here is therefore the stronger statement.

| instance | full | coherent | b-sym | bounded / other | evidence (logs) |
|---|---|---|---|---|---|
| PARITY, $M=2..9$ | $\lfloor M/2\rfloor$ | $\lfloor M/2\rfloor$ (Prop. 1.2) | $\lfloor M/2\rfloor$ | the symmetric circuit has weights 1 | `par_M*.log`, cross-checks `parity_nosym.py`, `hs_M*.log` |
| PARITY, $M=10$ | 4 or 5 (S=4 undecided after 55 min; still running) | | | | `par2_M10_S4_s*.log` |
| PARITY, $M=11$ | $\ge4$ (run stopped) | | | | `par2_M11_S4_s1.log` |
| half-slicing hs$(M)$, $M=4..9$ | $\lfloor M/2\rfloor$ | | | | `hs_M9_S3.log` + inline runs |
| $A_{1,m}$, $m\le8$ | $\lceil m/2\rceil$ (lower bound par$(m+1)$) | $\lceil m/2\rceil$ | $\lceil m/2\rceil$, already with block weight 1 | full with address weights in $\{-1,0,1\}$: $\lceil m/2\rceil$ ($m=3..6$) | inline runs |
| $A_{2,1}$ | 3 | 3 ($m=1$) | 3 | | `andreev_min.py 2 1 2` UNSAT 1.2 s |
| $A_{2,2}$ | 3 | 3 | 3 | address weights in $\{-1,0,1\}$: **$\ge4$**, full (34.8 s) and b-sym (4.1 s). Address weights in $\{-2..2\}$: 3, full and b-sym | `f22_S3_intaddr*.log` |
| $A_{2,3}$ | **$\ge4$** (2 seeds, about 950 s each) | $\ge4$ | $\ge5$ (`verify`) | sub-instances XOR$\cup$single-1, XOR$\cup$single-0, two-dictator already force 4. S=4: undecided. Plain z3 ran 1 h and table-CEGAR 60 min; relaxation best error $\ge44$ of 1024. | `f23_S3_s*.log`, `sub23_S3_*.log`, `tcg23_*.log`, `c23_S4_s1.log` |
| $A_{2,4}$ | **$\ge4$** (par(9)) | $\ge4$ | $\ge5$ (`verify_opus`) | 6-table sub-instance at $S=4$: undecided after 74 min | `sub24_S4_x1*.log` |
| $A_{2,m}$, $m\ge4$ | $\ge4$ (par(9)) | $\ge m-1$ (Thm E) | | | |
| two-dictator, $m=2$ | 2 | | | | `td_loop_m2to5.log` |
| two-dictator, $m=3$ | $\ge4$ | $\ge4$ | **$=5$** | full $S=4$: undecided. z3: 2 seeds 44 min, and with edge clauses 3 seeds 9–33 min, still running. Relaxation best error 2 of 256; LNS repair UNSAT. | `td_loop_m2to5.log`, `td3_bsreduced.log`, `td3_S4_*.log` |
| two-dictator, $m=4$ | $\ge3$ | | | | `td_loop_m2to5.log` |
| random features at $A_{2,3}$ (gates for exact LP representation, $\ge50\%$ of 5 draws) | mixed about 416, $\pm1$ about 288 | about 416 | **about 96** | heuristic | `random_features_23.log` |

The "two-dictator" sub-instance uses the tables $\{0101,1010,0011,1100\}$: the output is $b_1$, $\bar b_1$, $b_2$ or $\bar b_2$, selected by the table. It is the smallest instance found on which the block-symmetric minimum (5) is known exactly and the full-model minimum is still open (4 or 5).

## 6. What failed, and why

1. **The SAT side at (2,3) with 4 gates.** This is the smallest place where mixed signs could still beat block-symmetric circuits (b-sym $\ge5$, full $\ge4$). Every exact method stalled on the two decisive SAT questions:
   - full (2,3) with S=4: plain z3 1 h, point-CEGAR, table-CEGAR (round 2 open after 50 min);
   - the two-dictator instance at $m=3$ with S=4: 5 z3 runs, the relaxation (best error 2) and LNS repair.

   The cause is the size of the Boolean search over gate patterns. The same solver proves the UNSAT side at S=3 in 2–16 min. The heuristic evidence (error 2 but never 0; repairs UNSAT) points towards **5** for the two-dictator instance, i.e. no gain over block-symmetric circuits, but this is not a proof.
2. **The smooth relaxation** (`nnsearch.py`). It finds (2,2) S=3 in seconds and rediscovers 11-gate block-symmetric (2,3) circuits. On (2,3) its best training error stayed at 44–133 of 1024 points for S=4..6. On the two-dictator instance at S=4 it reached error 2 but never 0, and LNS repair of those near-solutions was always UNSAT. Parity-type targets defeat gradient methods, and the relaxation produced no circuit below the known minima.
3. **Random features** (`random_features.py`, `logs/random_features_23.log`). Draw random gates of each class and solve an exact LP for the top gate. To represent $A_{2,3}$ exactly one needs about **96** block-symmetric gates, but about **416** coherent, **416** mixed and **288** $\pm1$ gates. Generic mixing makes gates *worse* features; any gain from mixed signs would have to come from structure.
4. **A general proof of par$(M)\ge\lfloor M/2\rfloor$.**
   - Every local argument (square faces, chains, edges) only gives $\Theta(\sqrt M)$. The reason is that a balanced $\pm1$ gate switches $\Theta(\sqrt M)$ times along a random chain (O'Neil's edge bound), while a monotone gate switches once.
   - The natural geometric route, a linear lower bound on hs$(M)$, would already settle the hypercube-slicing conjecture (Prop. 1.4).
   - The known general lower bound for depth-two parity is still $\Omega(\sqrt n)$ gates.
5. **Rigidity.** Minimum parity circuits are not unique and can contain mixed gates (§1.3), so there is no "the optimum is unique, hence coherent" route.
6. **Mixed constructions in the balanced case.**
   - In the character-sum family of all known constructions (one staircase per character $\chi_S$ on a linear form with parity $e_S$), a mixed odd-weight form $L_S$ has the same parity as $t_S$ and range at least $|S|m$. Every staircase therefore costs the same.
   - A bounded number of "views" per block, such as $s_i$ plus alternating sums, is capped at a constant-factor gain by class (c).
   - I found no mechanism by which a mixed gate serves several characters.
7. **Point-CEGAR** (`mscore.solve_cegar`) and **plain z3 on all 16 tables** for (2,3) with S=4 and S=5: no answer within their time limits (see the data table).

## 7. Most promising next steps

1. **Decide full(2,3) and TD(3).** Both are $\ge4$; block-symmetric needs $\ge5$ and $=5$ respectively.
   - Use table-CEGAR with more seeds, or a portfolio on the 4-table two-dictator instance, which has only 256 points.
   - If either value is 4, mixed signs beat block-symmetric circuits at that size, and the circuit should be studied to see whether it generalises in $m$.
   - If both are 5, the evidence points to "no gain at $k=2$".
2. **Make "no gain at fixed $k$" rigorous for weight-bounded gates.**
   - For polynomially bounded weights, Paturi–Saks give an (almost optimal) edge lower bound for depth-two parity. I could not check its exact form here.
   - If it is $\tilde\Omega(M^2)$ edges, as I recall, it gives par$_{W}(M)=\tilde\Omega(M)$ gates, hence $\mathrm{size}_W(A_{k,m})=\tilde\Omega(km)$. That would mean MAJ-like mixed gates cannot beat coherent circuits by more than a polylog factor at fixed $k$.
   - For arbitrary weights the question contains hypercube-slicing-type difficulties.
3. **Balanced case.** Theorem 3.2 locates the whole $n^{3/2}$ vs $n^2$ gap in $\tilde\Omega(n^{3/2})$ gates that are heavily mixed (minority count $\tilde\Omega(n^\epsilon)$) and use $\Omega(\epsilon\log n)$ patterns. Survival arguments cannot go further (barrier).
   - The most concrete next target is a *circuit-adapted* arrangement: choose $\sigma$ greedily, block by block, to minimise the total runs $\sum_g\rho_g(\sigma)$ weighted by how often $g$ splits. Then show that a small circuit whose splitting mass sits on few patterns has a cheap arrangement.
   - Alternatively, exploit the top gate across *neighbouring* cubes, the analogue of the edge clauses that made the parity proofs fast. A single cube sees only the survival count, but a pair of adjacent cubes sharing a facet forces the same splitting gates to align their thresholds.

## 8. Files

| file | content |
|---|---|
| `report.md` | this report |
| `mscore.py` | encoder: point sets, gate classes, symmetry breaking, exact `Fraction` re-check of every SAT model, point-CEGAR |
| `parity_min.py`, `parity_min2.py` | exact parity minima; `parity_min2.py` adds the valid edge clauses of Prop. 1.4 |
| `parity_nosym.py` | cross-check of the parity UNSATs with weaker or no symmetry breaking |
| `parity_rigid.py` | minimum parity circuits containing a mixed gate |
| `halfslice.py` | half-slicing numbers hs$(M)$ |
| `andreev_min.py` | Andreev full / coherent / block-symmetric (`bsreduced`) / sub-instance (`--tables`) / bounded address weights (`--intaddr`) |
| `table_cegar.py` | CEGAR over table orbits |
| `nnsearch.py` | relaxation search plus exact certification; `andreevsub:` instances |
| `lns_repair.py` | large-neighbourhood exact repair of near-solutions |
| `cpsat_find.py` | CP-SAT SAT-finder with bounded integer weights |
| `random_features.py` | random-feature comparison of gate classes |
| `runs_lemma_check.py` | exact-integer check of Lemma 2.1 |
| `survival_mc2.py` | Monte Carlo for Lemmas 3.1 and 3.3 |
| `vo_min_circuit.py`, `common.py` | copies of `verify_opus/min_circuit.py` used for block-symmetric runs |
| `logs/` | every run quoted above (one line per result; SAT logs include the circuit when run with `--show`) |
| `mykill.sh` | kills only this directory's own python3/timeout processes |

## 9. Literature used for context (read-only web search, nothing posted)
- Kane, Williams, *Super-linear gate and super-quadratic wire lower bounds for depth-two and depth-three threshold circuits*, STOC 2016 — https://ar5iv.labs.arxiv.org/html/1511.07860 . Used for the $\Omega(n^{3/2}/\log^3n)$ bound reproved in Thm 3.2(1), and for the statement that the IPS $\Omega(\sqrt n)$ parity bound is tight on average.
- Impagliazzo, Paturi, Saks, *Size–depth tradeoffs for threshold circuits*, SIAM J. Comput. 1997 — https://cseweb.ucsd.edu/~paturi/myPapers/pubs/ImpagliazzoPaturiSaks_1997_siamjc.pdf . Gives the $\Omega(\sqrt n)$ gate lower bound for depth-two parity.
- Paturi, Saks, *Approximating threshold circuits by rational functions*, Inf. Comput. 1994. Gives a near-optimal edge lower bound for depth-two parity with polynomially bounded weights; I did not check its exact form (§7.2).
- Hypercube edge slicing:
  - Yehuda, Yehudayoff, $\Omega(n^{0.51})$ — https://arxiv.org/abs/2102.05536
  - Klein, $\tilde\Omega(n^{2/3})$ — https://arxiv.org/abs/2212.03328
  - Sauermann, Xu: the current best lower bound, $n^{13/19}$ up to logs. See https://arxiv.org/abs/2507.00773 and https://arxiv.org/abs/2510.16592; I did not check which of the two records the bound.
  - The upper bound $\lceil 5n/6\rceil$ is Paterson's.

## 10. Runs left running when this report was written (07 Nov, 10:05 UTC)
These six runs have hard timeouts and stop by themselves. Their verdicts, if any, will appear as an `ANDREEV …`/`PARITY2 …` line in the log; SAT lines come with the exactly verified circuit.

| run | log | ends by |
|---|---|---|
| two-dictator $m=3$, S=4, full, z3 seeds 1 and 2 | `logs/td3_S4_full_s1.log`, `logs/td3_S4_full_s2.log` | 10:21 |
| same with edge clauses, seeds 4 and 5 | `logs/td3_S4_full_edge_s4.log`, `logs/td3_S4_full_edge_s5.log` | 10:32, 10:37 |
| cross-check: (2,3) 6-table sub-instance, S=3, **no** symmetry breaking | `logs/sub23_S3_x1_nosym.log` | 10:34 |
| par(10), S=4 (with edge clauses) | `logs/par2_M10_S4_s1.log` | 12:09 |

Reading the verdicts:
- A **SAT** line in a `td3_S4_full*` log means full $<$ block-symmetric $=5$ on that sub-instance: the first separation of the two models. **UNSAT** means 5.
- **UNSAT** in `par2_M10_S4_s1.log` means $\mathrm{size}(A_{2,m})\ge5$ for all $m\ge5$, which excludes the task's "≤4 gates for $m=6..10$".
- **UNSAT** in the cross-check confirms full(2,3) $\ge4$ without any symmetry breaking.
