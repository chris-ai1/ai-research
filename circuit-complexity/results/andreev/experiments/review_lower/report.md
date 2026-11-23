# Referee report on `/tmp/andreev_gap/push_lower/report.md` (lower bounds)

Referee: independent and adversarial. I did not modify any file in `push_lower/`. All my code and logs are in `/tmp/andreev_gap/review_lower/`. Run them with `python3 -I`; they add `/tmp/pydeps` themselves. My checks share no code with the author's scripts, with two exceptions: `percube_cap.py` imports the author's `constr_d.build`, but only as a gate list, and the reruns of the author's scripts are labelled as such.

Model: $N=2^k$ table bits, $k$ blocks of $m$ address bits, $b_i=s_i \bmod 2$, output $x_b$. There are $S$ bottom threshold gates, and the top threshold gate reads the bottom gates and all raw inputs. All weights are real.

---

## 0. Verdicts at a glance

| # | Claim | Verdict | Issue (short) |
|---|---|---|---|
| 1 | Theorem A (information inequality) | **Correct** | None. The constant can be improved (§1.4). |
| 2 | Lemma B1 (coherent gate splits $\le m^k-(m-1)^k$ cubes) | **Correct, tight** | Brute force finds no violation (exhaustive on small cases). Equality is attained for all $k,m$. |
| 3 | Corollary C (i)–(iii), balanced $S\ge N(N-3k-1)/(3k^3)$ and $N(N-3k-1)/(6\sqrt2k^{5/2})$ | **Correct; small fixable gaps** | The closed forms need $S<2^{2k}$. They are unconditional only when $m\lesssim 3k^2 2^k$, which always holds in the balanced case. "Balanced" needs $k$ to be a power of 2. "Whenever $km=\Omega(N)$" needs $\log m=o(N)$. |
| 4 | Lemma B2 (Ball and Brunn) | **Correct** | None. |
| 5a | Theorem E ($k=2$: $S\ge m-1$) and the Ring Lemma | **Correct** | Brute force over **all up-sets** for $m\le 11$. |
| 5b | "This argument cannot give more" ($\tau_m$, LP $=m-1$) | **Correct** (for $m\le6$ with lines, $m\le7$ with coherent gates) | Reproduced with a different enumeration and solver. |
| 5c | "Hence the $k=2$ minimum is $\Theta(m)$" | **Fixable (wording)** | Holds only for the **coherent / block-symmetric** minimum. |
| 6 | Lemma B3, Corollary C(iv) | **Correct** (constant not explicit) | The Beta-mixture identity checks out exactly, and the Kolmogorov–Rogozin step is applied correctly. |
| 7 | §5 barrier (Proposition F and its consequence) | **Correct within its template** | Exact computation shows no violation, with equality at $(k,m)=(1,2)$. The step "$R\le N+1$" needs a sentence of justification. The template does not cover the algorithmic method. |
| 8a | Theorem G (the $k=2$ circuit with $4\lceil m/2\rceil+m$ gates) | **Correct** | Checked bit by bit over all inputs for $m\le8$, and over all $(x,s)$ for $m\le120$. |
| 8b | Side claims in §0/§3 about earlier constructions and the gadget search | **Wrong (minor)** | "$12m+18$" should be $12m+19$. The "cheaper" configurations have the *same* cost. The "dominance argument" is not given. |
| 8c | §4, $k=1$ exact minimum $2\lceil m/2\rceil$ | **Correct** | Proof checked line by line; construction verified for $m\le300$. |
| 8d | §4, $k=2$ exact table | **Reproduced** with an independent z3 encoding (§8.3) | $(2,1)=4$ and $(2,2)=5$ confirmed (UNSAT and SAT sides). "$(2,3)\ge6$" not re-run. |
| 8e | §4 remark "exact per-cube complexity is $2^k/\mathrm{poly}(k)$ (Odlyzko)" | **Unsupported** | Counting gives only one direction of the claim. |
| 9 | §0 / §2.6 / §6: "the loss is entirely in the per-cube count: about $3.6N$ … against $N/(3k)$"; "the polylog loss is in the per-cube complexity"; "proving [$\Theta(n^2)$] needs $\Omega(N)$ splitting gates per cube" | **Wrong** | (d) splits about $\tfrac58kN+3k$ gates per cube, not $3.6N$. The Theorem-A-plus-uniform-split-bound method is **capped** at $O(n^2/\log n)$ for coherent circuits and $O(n^2/\sqrt{\log n})$ for block-symmetric ones, however much the per-cube count improves (§9). |
| 10 | Novelty | **Partly classical** | The single-crossing-along-a-monotone-chain fact behind B1 is Impagliazzo–Paturi–Saks 1997, Lemma 2.1. I found no prior instance of the count restriction combined with the quadratic bound for coherent circuits (§11). |

**Overall:** every theorem-level claim (A, B1, B2, B3, C(i)–(iv), E, Ring Lemma, F, G, $k=1$ exact) is correct as stated, apart from small regime caveats. The headline is correct: sign-coherent and block-symmetric depth-2 circuits for Andreev's function need $\tilde\Omega(n^2)$ gates in the balanced case. The interpretive claims about *where the loss is* and *what would prove $\Theta(n^2)$* are wrong. They should be replaced by the cap in §9.

---

## 1. Theorem A — correct

### 1.1 Independence of $x$
Fix the circuit, $\sigma$ and $c$. The live positions $\ell_i=\sigma_i(c_i+1)$ are then fixed. The restricted bottom gate is $[\lambda_j\cdot z\ge\tau_j(x)]$ with $\lambda_{j,i}=\gamma_{j,i,\ell_i}$, a circuit parameter. Only $\tau_j(x)=\theta_j-\alpha_j\cdot x-\sum_iP_{j,i}(c_i)$ depends on $x$. The top gate's coefficients on gates ($v_j$) and on live bits ($\mu_i$, the top weight of bit $\ell_i$) are also circuit parameters. Its table weights, its fixed-bit weights and all non-splitting gates (constant on the cube, with an $x$-dependent value) shift only the threshold $\kappa(x)$. So yes, $\lambda_j$, $v_j$ and $\mu$ are independent of $x$.

### 1.2 Entropy count
The map $x\mapsto Y=(G,(\mathrm{pos}\,\tau_j)_{j\in G},\mathrm{pos}\,\kappa)$ determines $h_{x,c}$, and $h_{x,c}(z)=x_{c'\oplus z}$ determines $x$. So $H(x)\le H(Y)$.
- A non-constant $[\lambda\cdot z\ge\tau]$ has at most $r-1\le 2^k-1$ positions, where $r$ is the number of distinct values of $\lambda\cdot z$.
- Given $G$ and the bottom functions, $L(z)=\sum_{j\in G}v_jg_j(z)+\mu\cdot z$ is fixed, so $\kappa$ has at most $2^k+1$ positions.

Then $H(Y)\le H(D)+\sum_d\Pr[D{=}d]\log_2\#\{Y:|G|=d\}$, with $H(D)\le\log_2(S+1)$ and $\binom SD\le S^D$. This gives
$$2^k\le\log_2(S+1)+\mathbb E[D](\log_2S+k)+k+1 .$$
Replacing $\log_2S$ by $\log_2(S+1)$ in the denominator only weakens the bound when the numerator is positive, and the bound is trivial otherwise. The edge case $S=0$ is harmless: for $k\ge2$ it gives a contradiction, consistent with $S=0$ being impossible.

### 1.3 The top gate reading live inputs
This contributes the fixed linear term $\mu\cdot z$ to $L$. It changes neither the number of positions of $\kappa$ nor the independence from $x$. Nothing breaks.

### 1.4 Optional improvement
Use $\log_2\binom SD\le D\log_2(eS/D)$ and Jensen's inequality (the map $D\mapsto D\log_2(eS/D)$ is concave). For $S\approx N^2$ and $D\approx N/k$ the denominator becomes about $2k+\log_2k$ instead of $3k$. This turns the constant $3k^3$ of Corollary C(i) into roughly $2k^3$ asymptotically.

---

## 2. Lemma B1 — correct and tight

**Proof check.**
- With the block signs $\varepsilon$, each $P_i$ is monotone in direction $\varepsilon_i$. On cube $c$ the address part is affine in $z$, so its minimum and maximum lie at $c^\mp=c+(\mathbf1\mp\varepsilon)/2$, and the cube is split iff $F(c^-)<\theta'\le F(c^+)$.
- Along $c_t=c+t\varepsilon$ we have $c_t^+=c_{t+1}^-$, so the split intervals $(F(c_t^-),F(c_{t+1}^-)]$ are consecutive half-open intervals. One threshold lies in at most one of them.
- The cubes $c$ with $c-\varepsilon$ in the grid number $(m-1)^k$, so the lines number $m^k-(m-1)^k$.
- All-zero blocks are fine with either sign. Ties ($F(c^-)=F(c^+)$) mean a constant gate, which does not split.

**Brute force** (`b1_brute.py`, log `b1_brute.log`; exact integers).
- Split status is computed from all $2^k$ vertex values, not from the extreme-vertex formula.
- The count is maximised over *every* dichotomy threshold. This covers every $x$, because $\alpha\cdot x$ only shifts the threshold.
- Weight families tested: small integers with many zeros and ties; heavy-tailed weights; sparse weights; one huge weight per block plus ties; whole blocks set to zero; geometric weights (all subset sums distinct). Arrangements are random.
- Cases: $(k,m)\in\{(1,5),(2,2),(2,3),(2,5),(2,8),(3,2),(3,3),(3,5),(4,2),(4,3),(4,4),(5,2),(5,3),(6,2),(6,3)\}$.
- **Exhaustive** cases: all coherent matrices with entries $0..2$ times block signs for $(2,2),(2,3),(3,2)$, and entries $0..1$ for $(2,4),(3,3)$.
- Result: **0 violations.** The maximum equals the bound in almost every case (for example 665 of 665 at $(6,3)$, 19 of 19 at $(3,3)$ exhaustive).
- Sanity of the checker: random $\pm1$ (mixed-sign) gates split 16 of 16, 64 of 64 and 64 of 64 cubes at $(2,4)$, $(3,4)$ and $(2,8)$, far above the coherent bound.

**Tightness for all $(k,m)$.** Give the last element of each block's arrangement a huge weight $M$ and all other elements small positive weights, and set $\theta'=M$. Every maximal $\mathbf1$-line ends in a cube touching some face $s_i=m$, and starts in a cube whose vertices all have $s_i\le m-1$. So every line contains a split cube. Hence $\max f_{\rm coh}=1-(1-1/m)^k$ exactly. This fact is used in §9.

---

## 3. Corollary C and the constants — correct; small fixable gaps

- Summing Theorem A over cubes against B1 gives $Sf\ge D_0(S)$. This is correct, and (iii) is immediate.
- (i): for $S<2^{2k}$, $D_0\ge(2^k-3k-1)/(3k)$, so $S\ge m(2^k-3k-1)/(3k^2)$. Balanced ($m=N/k$): $N(N-3k-1)/(3k^3)$. This equals $\frac{n^2}{12(\log_2n-1)^3}(1-o(1))\ge\frac{n^2}{12\log_2^3n}(1-o(1))$. Correct.
- (ii): $3k\cdot\min(k,2\sqrt{2k})\cdot k=6\sqrt2k^{5/2}$ when $k\ge8$. Correct.

**Gaps (fixable):**
1. *Regime.* If $S\ge2^{2k}$, the closed form $S\ge m(2^k-3k-1)/(3k^2)$ follows only when that value is at most $2^{2k}$, that is when $m\lesssim3k^22^{k}$. The unconditional statement is $S\ge\min\{2^{2k},\,m(2^k-3k-1)/(3k^2)\}$, or use the self-consistent form. In the balanced case the minimum is always the second term, so the balanced statements are unconditional.
2. *Balanced* means $km=N$, which requires $k$ to be a power of 2. Otherwise state the bound with $m=\lfloor N/k\rfloor$, as `bound_table.py` already does.
3. "*The same holds whenever $km=\Omega(N)$*" (polylog optimality) needs $D_0$ to be non-trivial. Since $\log_2(S+1)=O(\log m+k)$, this requires $\log m=o(N)$.

**Recomputation** (`bounds_recompute.py`, log `bounds_recompute.log`, independent code). The §2.6 table matches to all printed digits:
- $k=10$: 560 / 596; $k=16$: $4.82\times10^5$ / $6.71\times10^5$; …; $k=50$: $3.85\times10^{24}$ / $9.53\times10^{24}$.
- Crossovers against $n^{3/2}/\log_2^2n$: $k=12$ (coherent) and $k=11$ (block-symmetric). Against $n^{3/2}$: $k=37$ and $k=35$. Confirmed.
- Every value is below $\tfrac5{16}n^2$ and below the exact gate count $G_d$ of (d).

---

## 4. Lemma B2 — correct

- The split cubes have disjoint interiors and lie in $\{|\beta\cdot y-\theta'|\le\|\beta\|_1\}\cap[0,m]^k$, a slab of width $2\|\beta\|_1/\|\beta\|_2$.
- Ball (1986) bounds central sections of the unit cube by $\sqrt2$. Brunn's principle, together with central symmetry, makes the central section the largest among parallel ones.
- Hence at most $2\sqrt2(\|\beta\|_1/\|\beta\|_2)m^{k-1}\le2\sqrt{2k}\,m^{k-1}$ split cubes.

Exact check (`b2_check.py`): about 270 directions per case, including extremal ones, for 13 values of $(k,m)$ up to $(8,3)$. The ratio actual/bound is at most 1. It equals 1 only where B1 is already tight ($k=2$, or $m=2$).

For later use (§9): the all-ones direction attains a split fraction of about $\sqrt{6k/\pi}/m$. Exact values are 0.190 at $(8,20)$ and 0.380 at $(12,12)$. This is about half of the Ball bound.

---

## 5. Theorem E, the Ring Lemma, and "cannot give more" — correct

- **Theorem E logic.**
  - With the XOR table, every square computes XOR or XNOR.
  - If every restricted gate were a constant or a literal, the top gate would be a threshold function of $z$, which is impossible.
  - The 8 non-literal two-variable threshold functions are exactly the functions with 1 or 3 ones.
  - For a coherent gate, the 1-set on $\{0..m\}^2$ is $\{P_1(s_1)+P_2(s_2)\ge\theta'\}$ with monotone $P_i$, i.e. an up-set after reflections. Reflections map boundary squares to boundary squares.
- **Ring Lemma.** Write $U=\{b\ge h(a)\}$ with $h$ non-increasing. Column $a$ is mixed exactly on rows $[h(a{+}1){-}1,\,h(a){-}1]$, and corner cuts sit at the two ends of each drop of $h$. Monotonicity makes the top-row/left-column part of the path a prefix and the bottom-row/right-column part a suffix, each with at most 2 turns. The clipped cases (path entering from the top, leaving at the bottom) also check out.
- **Brute force** (`ring_brute.py`): **all** $\binom{2m+2}{m+1}$ up-sets for $m=2..11$ (2.7 million at $m=11$). The maximum number of boundary corner cuts is 4 (3 at $m=2$). The maximum total number of cut squares is $2m-1$. Random separable monotone $P_1+P_2$ functions with zero steps and ties give the same result.
- **Cover numbers and LP values** (`cover_check.py`, `cover_upsets2.py`; my own enumeration by sweeping generic directions, HiGHS MILP):

| $m$ | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|
| $\tau_m$, lines | 2 | 3 | 4 | 4 | 5 | – |
| LP, lines | 4/3 | 2 | 3 | 4 | 5 | – |
| cover number, coherent gates (up-sets, both orientations) | 2 | 3 | 4 | 4 | 5 | 6 |
| LP, coherent gates | 4/3 | 2 | 3 | 4 | 5 | 6 |

  All optimal dual weight lies on the boundary ring. So "$\tau_m=2,3,4,4,5$" and "LP $=m-1$ for $m=3..6$" are confirmed, and the same holds for coherent gates up to $m=7$. Side remark: the cover number gives a valid coherent lower bound $S\ge\tau^{\rm coh}_m$, which is slightly stronger than $m-1$ for $m\le4$.
- **Wording to fix (5c).** "Hence the $k=2$ minimum is $\Theta(m)$" should read "the coherent (and the block-symmetric) $k=2$ minimum is $\Theta(m)$". For general circuits no linear lower bound is shown.
- **Consistency.** The solver logs (`big2/`) give $S=5$ UNSAT at $m=6,8,10$, i.e. lower bounds of 6. These are not exact minima, so Theorem E's 7 and 9 at $m=8,10$ do not conflict. The exact minima at $m=1,2$ (3 gates) exceed Theorem E's 0 and 1.

---

## 6. Lemma B3 and Corollary C(iv) — correct (constant not explicit)

- **Step 1, exact check** (`b3_reform_check.py`, all $m\le6$, Fractions). $\Pr[\ell,A]=\frac1m\cdot\frac1{m\binom{m-1}{|A|}}=\frac1m\int_0^1q^{|A|}(1-q)^{m-1-|A|}\,dq$ for every $\ell$ and every $A\subseteq[m]\setminus\{\ell\}$. No mismatches. The live bit and the $q_i$ are independent across blocks, and the non-live bits are i.i.d. Bernoulli($q_i$).
- **Steps 2–5.**
  - $\Pr[\bar E]\le kr/m$ by a union bound.
  - On $E$, every live weight is at most $\mu_i\le\Lambda$, so the window has length at most $k\Lambda$.
  - The $r$ heaviest positions of block $i^*$ are fixed, i.i.d. Bernoulli($q$) given everything else, and each has magnitude at least $\Lambda$.
  - Kolmogorov–Rogozin with $\lambda_j=L=\Lambda/2$: $Q(X_j;\Lambda/2)=\max(q,1-q)$, because an interval of length $\Lambda/2$ holds at most one atom. This gives $C/\sqrt{r\min(q,1-q)}$.
  - $2k$ intervals of length $\Lambda/2$ already suffice; $2k+1$ is safe.
  - $\int_0^1\min(q,1-q)^{-1/2}\,dq=2\sqrt2$.
  - The case $\Lambda=0$ is handled.
- C(iv) is correct: Theorem A holds for every $\sigma$, B1 holds for every $\sigma$, and B3 holds on average over $\sigma$. The threshold $S<N(N-3k-1)/(6k^3)$ and the conclusion $\Omega(N^{4/3}/k^{7/3})$ are recomputed correctly.

---

## 7. §5 barrier — correct within its template

- **Proposition F, exact verification** (`barrier_check.py`). For each $K\le k(m-1)$:
  $$\Pr[\text{non-constant}]=\sum_P\binom kP2^{-k}\Pr[1-P\le F\le k-P]$$
  is computed exactly for $k\in\{1,2,3,4,6,8\}$ and $m\in\{2,3,5,10,30,64\}$. Every value is at least $1/(2\sqrt{2km})$, with **equality at $(k,m)=(1,2)$, $K=1$**. Since the bound holds for every single $\rho$, it holds for every distribution $\mathcal D$.
- The inequality $\binom K{\lfloor K/2\rfloor}2^{-K}\ge(2K+2)^{-1/2}$ holds for all $K\le2\cdot10^6$, with equality at $K=1$ and limiting ratio $\sqrt{4/\pi}$.
- The aside "counting the whole window gives $\Omega(\sqrt{k/m})$" is numerically true, at about $0.40\sqrt{k/m}$ across all tested cases. It is unproven in the text.
- **The step "$R\le N+1$".** The cleanest justification: any valid bound "every circuit has $\mathbb E[\#\text{surviving}]\ge R$" must hold for the DNF circuit $\bigvee_a(x_{b(a)}\wedge[\text{addr}=a])$. That circuit uses $\pm1$-weight AND gates and an OR, it is exact, and at most $N$ of its gates survive any one-live-bit-per-block restriction. Hence $R\le N$. With this sentence the "consequence" is rigorous for the template "uniform per-gate survival bound times expected number of survivors".
- **Scope.** The barrier does not cover non-survival methods. For context: super-quadratic gate lower bounds for THR∘THR are now known for a function in $E^{NP}$ — $n^{2.5-\varepsilon}$, Chen–Tal–Wang, ECCC TR26-039 (2026) — via the algorithmic method. For Andreev's function itself, Kane–Williams' $\tilde\Omega(n^{3/2})$ remains the best general bound I found.
- Rerun of the author's `survival_mc.py` with the same seed: 0.0350, 0.0254, 0.0332, 0.1853 and 0.1270, identical to the report's table.

---

## 8. Theorem G and the §4 results

### 8.1 Theorem G — correct
- `thmG_check.py` builds the circuit as explicit integer weight vectors (everything scaled by 2) over all $4+2m$ bits.
- It checks **all $2^{4+2m}$ inputs for $m=1..8$** (about $10^6$ inputs at $m=8$), with 0 errors.
- It also checks all 16 tables and all $(s_1,s_2)$ for $m\le120$, again with 0 errors (`thmG_blocklevel.log`).
- The gate count is $4\lceil m/2\rceil+m$. I re-derived the identity $Vt-2V\lfloor(t+x)/2\rfloor=V(-1)^x(t\bmod2)$ and checked the 16×4 core table by hand. The minimum slack is 0, which is legitimate for the threshold "$\ge$".

### 8.2 Side claims — minor errors
1. "the 5/8 construction gives $12m+18$ for $k=2$": its formula $(N-1)(N+2)+\tfrac32kmN+1$ gives **$12m+19$** for $k=2$. The $-1$ is the off-by-one already flagged in `verify_opus/report.md` for `cpsat_min.py`. "About $14m$" for (d) is right: the exact count is $G_d=14m+15$ for even $m$, e.g. 155 at $m=10$.
2. "cheaper configurations, such as $(1,1),(1,1),(1)$ and $(2,1),(2,1),(1)$, are infeasible". Rerunning `k2_gadget_search3.py` and `k2_gadget_search4.py` confirms that they are infeasible. But they cost **the same** $4\lceil m/2\rceil+m$ gates as the chosen $(2,1),(2,1),(2)$: cost depends only on the number of gadgets, not on amplitudes. No configuration that is actually cheaper (for example 3 or fewer singleton gadgets) was tested, and the "dominance argument" is not written down. So "the cheapest feasible configuration costs $\approx3m$" is unproven even within the family.

### 8.3 Exact-sum model
- **$k=1$ — correct.**
  - If $w\neq0$: the constant tables force step $-w$ in every gap. A block-symmetric gate crosses at most one gap per table, so $S\ge m$.
  - If $w=0$: the tables $(0,1)$ and $(1,0)$ force steps $\pm1$, so again $S\ge m$.
  - For odd $m$ and $S=m$ with $w\ne0$: every gate's effective step is $\operatorname{sign}(\beta_j)v_j=-w$, independent of the table. The crossing counts per table are $n_a=1\mp(-1)^a/w$, with totals $m\mp1/w\le m$. This forces $1/w=0$, a contradiction.
  - For odd $m$ and $S=m$ with $w=0$: the multiset of effective steps would have to be both $\{+1^{(m+1)/2},-1^{(m-1)/2}\}$ and its mirror image.
  - Scope: this is the block-symmetric model. The top gate's $s$-part must be linear in $s$, so the argument does not extend verbatim to coherent gates with arbitrary top weights.
  - The construction is verified for $m\le300$ (`k1_exact_check.py`): the sum equals $x_{s\bmod2}$ exactly.
- **$k=2$ and $k=1$ solver claims — independently reproduced.** I used my own z3 encoding (`exact_z3_indep.py`): own point generator, and every SAT model is re-verified exactly with Fractions.
  - Plain version (only symmetry breaking: gate ordering): $(1,3)$: $S=3$ UNSAT, $S=4$ SAT. $(1,5)$: $S=6$ SAT. $(2,1)$: $S=3$ UNSAT (197 s), $S=4$ SAT. $(2,2)$: $S=5$ SAT.
  - Version with two more symmetry reductions that are valid without loss of generality (`exact_z3_indep_sb.py`): $v_j\ge0$ by gate complementation, and top weight on each $s_i\ge0$ by reflecting $s_i\mapsto m-s_i$ and permuting the table. Results: $(1,5)$: $S=5$ UNSAT (46 s); $(2,2)$: $S=4$ UNSAT (83 s).
  - Hence the exact minima are 4 and 6 at $k=1$, $m=3,5$ (matching $2\lceil m/2\rceil$), and **4 and 5 at $(2,1)$ and $(2,2)$**, as claimed.
  - Not re-checked: "$(2,3)$ needs at least 6", which rests on the author's 372 s run.
- **The Odlyzko remark is unsupported.** "The exact per-cube complexity of a random function is also $2^k/\mathrm{poly}(k)$ (count subspaces with Odlyzko's bound)": counting gives only a *lower* bound, while "does not help" needs an upper bound or a construction. With fixed directions and fixed top coefficients (the Theorem A setting), the exact model admits at most $\binom SD(2^k-1)^D\cdot2$ restricted functions. So exactness does not improve Theorem A's count; that would be a valid replacement sentence.

---

## 9. Wrong: "where the loss is" and the route to $\Theta(n^2)$

The report says (§0, Conjectures): "The loss is entirely in the per-cube count: about $3.6N$ splitting gates per cube in the construction, against $N/(3k)$ in the proof". In §2.6 it says the polylog loss is in the per-cube complexity, and in §6 that proving $\Theta(n^2)$ "needs $\Omega(N)$ splitting gates per cube".

**Data** (`percube_cap.py`, log `percube_cap.log`). For each gate of construction (d), I take the exact number of split cubes from the distribution of $\beta\cdot c$, averaged over 64 random tables. The author's `percube_d.py` used 4 tables, and the count depends strongly on $x_0$.

| $(k,m)$ | $S_d$ | mean splitting gates/cube $R_d$ | $R_d/N$ | $R_d/(kN)$ | $\tfrac58kN+3k$ | mean split fraction | max per-gate fraction | $f_{\rm coh}$ |
|---|---|---|---|---|---|---|---|---|
| (4,4) | 421 | 52.8 | 3.30 | 0.83 | 52 | 0.126 | 0.605 | 0.684 |
| (5,5) | 1297 | 116.1 | 3.63 | 0.73 | 115 | 0.090 | 0.560 | 0.672 |
| (6,6) | 4077 | 264.6 | 4.13 | 0.69 | 258 | 0.065 | 0.515 | 0.665 |
| (7,18) | 21109 | 573.6 | 4.48 | 0.64 | 581 | 0.027 | 0.197 | 0.330 |
| (8,32) | 83581 | 1271.6 | 4.97 | 0.62 | 1304 | 0.015 | 0.119 | 0.224 |

**Facts.**
1. **The per-cube count of (d) is about $\tfrac58kN+3k$, not $3.6N$.** Per set $S$, the ridge, the residue and the override contribute about $|S|/2$, $|S|/2$ and $|S|/4$ splitting gates per cube; summing $\tfrac54|S|$ over $S$ gives $\tfrac58kN$. The global staircases add $3k$. The "3.6N" is a small-$k$, 4-sample snapshot.
2. **The uniform split bound loses a growing factor.** In the balanced case, (d)'s gates split on average a $\tfrac{1}{2m}$ fraction of cubes. But the worst coherent gate splits $1-(1-1/m)^k\approx k/m$, which is attained (§2). The all-ones block-symmetric gate splits about $\sqrt{6k/\pi}/m$ (§4). Already at $(6,6)$ the gap is 10× out of a total gap of 1084×.

**Proposition (cap for the Corollary C method).** Consider any argument of the form "every cube needs at least $R$ splitting gates on average over $x$, and every gate of the class splits at most an $f$ fraction of cubes, so $S\ge R/f$". Then:
- $R\le R_d$, because (d) is block-symmetric and hence in both classes;
- $f\ge 1-(1-1/m)^k$ for coherent gates, and $f\ge\sqrt{6k/\pi}/m\,(1-o(1))$ for block-symmetric gates.

So the argument can output at most about $\tfrac58Nm$ (coherent) and $0.45\sqrt k\,Nm$ (block-symmetric). In the balanced case that is $\approx\tfrac{5N^2}{8k}=O(n^2/\log n)$ and $\approx0.45N^2/\sqrt k=O(n^2/\sqrt{\log n})$. Measured: the cap is 6.8% (coherent) and 12.7% (block-symmetric) of $S_d$ at $(8,32)$, and this fraction keeps falling with $k$.

**Corrected statements.**
- "Construction (d) has $\approx\tfrac58kN+3k$ splitting gates per cube ($3.3N$–$5.0N$ for $k=4..8$, growing like $kN$), against $D_0\approx N/(3k)$. That is a per-cube slack of $\approx1.9k^2$."
- "A further slack of $\Theta(k)$ (coherent) or $\Theta(\sqrt k)$ (block-symmetric) comes from the uniform split bound, which is attained by gates the construction barely uses."
- "Theorem A plus a uniform split bound can never prove $\Theta(n^2)$; it is capped at $O(n^2/\log n)$ and $O(n^2/\sqrt{\log n})$. A $\Theta(n^2)$ proof needs a non-uniform argument, for example showing that a correct circuit cannot consist mostly of high-split gates."
- The *conjecture* itself ($\Theta(n^2)$ for these classes) remains plausible. Only its stated route is wrong. Within the method there is still room for a factor of about $1.9k^2$ (coherent) or $3.8k^2$ (block-symmetric) from a better per-cube bound.

---

## 10. Sanity checks — pass
- Against the exact block-symmetric $k=2$ minima: Theorem E gives $m-1=0,1$ at $m=1,2$ (minimum 3), and $2,3,4,5$ at $m=3..6$ (solver lower bounds $\ge5,5,5,6$). At $m=8,10$ it gives 7 and 9, while the solver bound there is only $\ge6$, so there is no conflict. Theorem G gives 24 and 30. For $k=1$ the claims are $\lceil m/2\rceil$ (sign model) and $2\lceil m/2\rceil$ (exact model).
- Against $\tfrac5{16}n^2$ and the exact count of (d): every claimed lower bound is far below them (§3 table; at $k\le20$, $G_d$ is computed exactly). For $k\le3$, Corollary C gives only $\approx C_km/k$ with $C_2=C_3=1$. I confirmed $C_2=C_3=1$ constructively by integer-weight search (`ck_check.py`): all 16 and all 256 functions are computable with one bottom gate.

---

## 11. Novelty

- **Classical ingredient.** That a unate ("generalized monotone") function changes value at most once along an assignment chain consistent with its orientation is **Impagliazzo–Paturi–Saks, SIAM J. Comput. 1997, Lemma 2.1**. Paraphrasing: "Let $f$ be a nonconstant generalized monotone function with orientation $\beta$ and $\pi$ an ordering of $X$; then there is $j$ such that $f(\beta_\pi(\le j))\equiv0$ and $f(\bar\beta_\pi(\ge j))\equiv1$". The paper notes such functions "are sometimes referred to in the literature as 'unate'". Its Lemma 3.2 uses the same property to fix all gates via a partition into $|F|^2+1$ blocks. The 1-D case (symmetric or monotone gates on a Hamming-weight chain, giving $\approx\lceil m/2\rceil$ for parity) is folklore.
- **Lemma B1** is that single-crossing fact applied to the $m^k-(m-1)^k$ maximal $\varepsilon$-chains of the count-restriction grid. Sign coherence is exactly the condition that makes *one fixed arrangement* orientation-consistent for every gate at once.
- **Apparently new** (not found in my searches): the count restriction as a common restriction family for all coherent gates, together with Theorem A's fixed-direction count, giving $\tilde\Omega(n^2)$ for block-symmetric or coherent THR∘THR on Andreev's function; the Ring Lemma bound for $k=2$; the hybrid inequality. The closest general results are Kane–Williams (STOC 2016; $\tilde\Omega(n^{3/2})$ gates for Andreev's function, random restrictions plus Littlewood–Offord), Chen–Tal–Wang (ECCC TR26-039; $n^{2.5-\varepsilon}$ gates for $E^{NP}$), and Nag (ECCC TR26-167; wire bounds for $E^{NP}$).
- **Search limits.** I searched the web over arXiv, ECCC and author pages with about ten queries (block-symmetric, unate, monotone bottom gates, thermometer or weight-preserving restrictions, Andreev 2025–26). I did not do an exhaustive library search, so novelty is "not refuted", not "established".

Sources: [Kane–Williams, arXiv:1511.07860](https://arxiv.org/abs/1511.07860); [ECCC TR15-188](https://eccc.weizmann.ac.il/report/2015/188); [Impagliazzo–Paturi–Saks 1997](https://cseweb.ucsd.edu/~paturi/myPapers/pubs/ImpagliazzoPaturiSaks_1997_siamjc.pdf); [Chen–Tal–Wang, ECCC TR26-039](https://eccc.weizmann.ac.il/report/2026/039/); [Nag, ECCC TR26-167](https://eccc.weizmann.ac.il/report/2026/167/).

---

## 12. Overall verdict

- **Mathematics: sound.** Theorem A, Lemmas B1, B2 and B3, Corollary C(i)–(iv), Theorem E with the Ring Lemma, Proposition F, Theorem G and the $k=1$ exact result are all correct. The constants of the balanced bounds $N(N-3k-1)/(3k^3)$ and $N(N-3k-1)/(6\sqrt2k^{5/2})$ ($k\ge8$) are right, and so are the §2.6 numbers.
- **Needed edits.**
  1. State the regime of C(i) and C(ii) for $m\gtrsim3k^22^k$, require $k$ to be a power of 2 for "balanced", and add $\log m=o(N)$ to the "$km=\Omega(N)$" sentence.
  2. Qualify "$k=2$ minimum is $\Theta(m)$" as the coherent or block-symmetric minimum.
  3. Correct $12m+18$ to $12m+19$, and "cheaper" to "equal-cost".
  4. Justify $R\le N$ in §5 via the DNF circuit, and note that non-survival methods are outside the barrier.
  5. Replace the Odlyzko remark.
  6. **Rewrite the loss analysis and the route to $\Theta(n^2)$ (§9 of this review).** The per-cube count of (d) is about $\tfrac58kN$. The Corollary C method is capped at $O(n^2/\log n)$ and $O(n^2/\sqrt{\log n})$ for the two classes.
- **Novelty:** the key monotone-chain fact is classical (IPS97). Its use with the count restriction and the resulting quadratic bound appear new as far as I could find.

### Files (in `/tmp/andreev_gap/review_lower/`)
| file | content |
|---|---|
| `b1_brute.py` / `.log` | Lemma B1: random adversarial and exhaustive checks; tightness; mixed-sign sanity check |
| `ring_brute.py` / `.log` | Ring Lemma over all up-sets, $m\le11$ |
| `cover_check.py`, `cover_upsets2.py` / `.log` | $\tau_m$ and LP values for lines and for coherent up-sets (own enumeration, HiGHS) |
| `b2_check.py` / `.log` | Lemma B2, exact |
| `bounds_recompute.py` / `.log` | Corollary C numbers, §2.6 table, crossovers, sanity checks |
| `percube_cap.py` / `.log`, `percube_d_rerun.log` | per-cube counts of (d), split fractions, method cap |
| `barrier_check.py` / `.log` | Proposition F, exact |
| `b3_reform_check.py` / `.log` | Beta-mixture identity, exact |
| `thmG_check.py`, `thmG_bitlevel.log`, `thmG_blocklevel.log` | Theorem G, bit level and block level |
| `k1_exact_check.py` / `.log` | §4 $k=1$ exact construction, $m\le300$ |
| `ck_check.py` / `.log` | $C_2=C_3=1$, constructive |
| `exact_z3_indep.py`, `exact_z3_indep_sb.py`, `exact_z3_indep*.log` | independent z3 exact-model checks (plain, and with symmetry reductions valid without loss of generality) |
| `survival_mc_rerun.log`, `gadget3_rerun.log`, `gadget4_rerun.log` | reruns of the author's scripts |
| `ext_ips/`, `pdf_lzw_text.py` | text extracted from the IPS97 PDF (treated as untrusted data) |
