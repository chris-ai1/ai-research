# Lower bounds for depth-two threshold circuits computing Andreev's function

**Scope:** block-symmetric and sign-coherent circuits.

All scripts are in `/tmp/andreev_gap/push_lower/`. Run them with `python3 -I`; they add `/tmp/pydeps` themselves.

Notation follows the task:
- $N=2^k$ table bits $x$, and $k$ address blocks of $m$ bits.
- $s_i$ is the weight of block $i$, $b=s\bmod 2$, $A=x_b$, $n=N+km$.
- The balanced case is $km=N$, so $n=2N$ and $k=\log_2(n/2)$.
- A circuit has $S$ bottom threshold gates and one top threshold gate that reads the gates **and** the inputs.

Labels used below:
- **[PROVED]**: complete proof in this file.
- **[VERIFIED]**: exact computation or exhaustive check, done here.
- **[CONJECTURE]** / **[EVIDENCE]**: not proved.

---

## 0. Summary

### Rigorous results

1. **Quadratic lower bound for sign-coherent circuits** [PROVED] (§2: Theorem A, Lemma B1, Corollary C).
   - **Definition.** A bottom gate is *sign-coherent* if, inside every address block, its weights are all $\ge0$ or all $\le0$. Its table weights are arbitrary, its magnitudes are arbitrary, and the top gate is arbitrary. Every block-symmetric gate $[\alpha\cdot x+\beta\cdot s\ge\theta]$ is sign-coherent, as is every gate that is monotone in the address bits.
   - **Bound.** If all bottom gates are sign-coherent, then
     $$S\;\ge\;\frac{m^k}{m^k-(m-1)^k}\cdot\frac{2^k-k-1-\log_2(S+1)}{k+\log_2(S+1)}\;\ge\;\frac mk\cdot\frac{N-k-1-\log_2(S+1)}{k+\log_2(S+1)} .$$
   - **Balanced case:**
     $$S\ge\frac{N(N-3k-1)}{3k^3}=\frac{n^2}{12\log_2^3n}(1-o(1)).$$
   - **Block-symmetric gates** satisfy a sharper splitting bound (Lemma B2, via Ball's cube-slicing theorem):
     $$S\ge\frac{N(N-3k-1)}{6\sqrt2\,k^{5/2}}=\Omega\!\left(\frac{n^2}{\log^{5/2}n}\right).$$
   - **Consequences.**
     - This is far beyond $n^{3/2}$.
     - The (5/16)$n^2$ construction consists of block-symmetric gates, so **within this class the construction is optimal up to a polylog factor** in the balanced case. The same holds whenever $km=\Omega(N)$; for $m\ll N/k$ the gap between $Nm$ and $N^2$ remains open. Any $n^{2-\varepsilon}$ circuit must use gates with mixed signs inside a block.
   - **Where it starts to bite** (§2.6). As expressions, the bound exceeds $n^{3/2}/\log_2^2n$ from $k=11$ (block-symmetric) or $k=12$ (coherent); Kane–Williams' constant is not known here, so this is only a comparison of expressions. It exceeds $n^{3/2}$ itself only from $k=35$ (block-symmetric) or $k=37$ (coherent). The gain is real but asymptotic.
2. **Hybrid form** [PROVED]. For every circuit,
   $$S_{\rm coh}\big(1-(1-\tfrac1m)^k\big)+S_{\rm other}\ge \frac{2^k-k-1-\log_2(S+1)}{k+\log_2(S+1)}.$$
   In addition, Lemma B3 shows that *every* gate splits an $O(km^{-1/3})$ fraction of cubes on average over a random arrangement. This uses a crude Littlewood–Offord argument and the Kolmogorov–Rogozin inequality.
   - **Consequence (balanced case).** Every circuit with fewer than about $n^2/(24\log_2^3n)$ gates contains $\Omega(n^{4/3}/\log^{7/3}n)$ gates that are **not** sign-coherent (Corollary C(iv)).
   - A Kane–Williams-quality survival bound $\tilde O(k/\sqrt m)$ would raise $n^{4/3}$ to $n^{3/2}$.
3. **$k=2$, both directions** [PROVED and VERIFIED] (§3).
   - Every sign-coherent (in particular block-symmetric) circuit has $S\ge m-1$. This is new for $m=8$ (7 against the previous 6) and $m=10$ (9 against 6).
   - An explicit block-symmetric circuit has $4\lceil m/2\rceil+m$ gates. This is new: the earlier constructions give $12m+18$ (the 5/8 construction) and about $14m$ (construction (d)) for $k=2$.
   - Hence the $k=2$ minimum is $\Theta(m)$, between $m-1$ and about $3m$.
   - The corner-cut argument behind the lower bound is exactly tight for itself: the cover number is $m-1$ at $m=5,6$ and the LP value is $m-1$ for $m=3..6$.
4. **Exact-sum model** [PROVED for $k=1$, VERIFIED for small $k=2$] (§4).
   - For $k=1$ the minimum is exactly $2\lceil m/2\rceil$, twice the sign-model value $\lceil m/2\rceil$. Lower-bound proof and construction are given for all $m$.
   - For $k=2$ (block-symmetric): $m=1$ needs 4, $m=2$ needs 5, and $m=3$ needs at least 6, against 3, 3 and at least 5 in the sign model.
   - In every case computed, exactness costs a constant factor (exactly 2 for $k=1$). Whether that holds in general is open. The quadratic bounds above apply to the exact model unchanged, but I found no argument that is specific to exactness and gives more.
5. **Barrier** [PROVED] (§5).
   - For **every** distribution of restrictions leaving one live bit per block, a gate with $\pm1$ weights survives with probability $\ge1/(2\sqrt{2km})$.
   - So every survival-based argument is capped at $O(N\sqrt{km})=O(n^{3/2})$ for general circuits, and also for MAJ∘MAJ. This covers Kane–Williams and ours, with any restriction distribution and any complexity measure for the restricted function.
   - Coherent gates escape the cap because under the *count restriction* they split at most a $k/m$ fraction of cubes, not $\Theta(1/\sqrt m)$.

### Conjectures (§6)
- Block-symmetric and coherent complexity is $\Theta(n^2)$ in the balanced case. The loss is entirely in the per-cube count: about $3.6N$ splitting gates per cube in the construction, against $N/(3k)$ in the proof.
- For $k=2$, the slope of the linear growth is strictly between 1 and 3.

### Most promising next step (§7)
Improve Lemma B3's survival bound for **arbitrary** gates under the randomised count restriction from the proven $O(km^{-1/3})$ to the Kane–Williams-type $\tilde O(k/\sqrt m)$. With the hybrid inequality this would give: every circuit has $\tilde\Omega(n^{3/2})$ mixed-sign gates or $\tilde\Omega(n^2)$ gates in total. That would reduce the whole $n^{3/2}$ versus $n^2$ question to gates with mixed signs inside a block.

---

## 1. The count restriction

Fix permutations ("arrangements") $\sigma_1,\dots,\sigma_k$ of $[m]$. For $s\in\{0..m\}^k$, let $a_\sigma(s)$ set bit $\sigma_i(t)$ of block $i$ to 1 exactly when $t\le s_i$. Then block $i$ has weight $s_i$, and $A(x,a_\sigma(s))=x_{s\bmod2}$.

A gate $[\alpha\cdot x+\sum_{i,t}\gamma_{i,t}a_{i,t}\ge\theta]$ becomes $[\alpha\cdot x+\sum_iP_i(s_i)\ge\theta]$ with
$$P_i(s)=\sum_{t\le s}\gamma_{i,\sigma_i(t)} .$$
For a block-symmetric gate, $P_i(s)=\beta_is$.

For a unit cube $c\in\{0..m-1\}^k$, put $s=c+z$ with $z\in\{0,1\}^k$. This means: fix $c_i$ ones and $m-1-c_i$ zeros in block $i$, and leave bit $\sigma_i(c_i+1)$ live. The restricted circuit computes
$$h_{x,c}(z)=x_{c'\oplus z},\qquad c'=c\bmod 2,$$
and this function determines $x$.

Gate $g$ **splits** $c$ under table $x$ if $z\mapsto g$ is non-constant on the cube. Let $d_c(x)$ be the number of splitting bottom gates.

Kane–Williams fix the other bits uniformly at random, so each block's fixed weight is concentrated within $\sqrt m$. Here $c_i$ ranges uniformly over $\{0..m-1\}$. For gates whose block contributions are monotone, this spreads the effective threshold over a range of length $m$; that is the whole gain.

---

## 2. Quadratic bound for sign-coherent circuits

### Theorem A (information inequality) [PROVED]
Let $C$ be **any** depth-two threshold circuit computing $A_{k,m}$ with $S$ bottom gates. Fix $\sigma$, and let $x$ be uniform on $\{0,1\}^N$. Then for every unit cube $c$,
$$\mathbb E_x[d_c(x)]\ge D_0(S):=\frac{2^k-k-1-\log_2(S+1)}{k+\log_2(S+1)}.$$

*Proof.* Fix $c$, and let $\ell_i=\sigma_i(c_i+1)$ be the live bit of block $i$.

On the cube, bottom gate $j$ becomes
$$z\mapsto[\lambda_j\cdot z\ge\tau_j(x)],\qquad \lambda_{j,i}=\gamma_{j,i,\ell_i},\qquad \tau_j(x)=\theta_j-\alpha_j\cdot x-\sum_iP_{j,i}(c_i).$$
The top gate becomes
$$z\mapsto\Big[\sum_jv_jg_j+\mu\cdot z\ge\kappa(x)\Big],$$
where $\mu_i$ is the top weight of bit $\ell_i$, and $\kappa$ absorbs the threshold, the table part, the fixed bits and all non-splitting gates, which are constant on the cube.

The data $\lambda_j$, $v_j$ and $\mu$ are **independent of $x$**. So $h_{x,c}$, and hence $x$, is determined by:
- the set $G$ of splitting gates;
- for each $j\in G$, which non-constant function $[\lambda_j\cdot z\ge\tau]$ occurs, with at most $2^k-1$ choices since only the position of $\tau$ among the at most $2^k$ values $\lambda_j\cdot z$ matters;
- the position of $\kappa$, with at most $2^k+1$ choices.

With $D=|G|=d_c(x)$:
$$2^k=H(x)\le H(D)+\mathbb E\log_2\!\Big[\tbinom SD(2^k-1)^D(2^k+1)\Big]\le\log_2(S+1)+\mathbb E[D](\log_2S+k)+k+1 .$$
∎

### Lemma B1 (coherent gates split few cubes) [PROVED; VERIFIED in exact integers, `split_checks_exact.py`]
A sign-coherent gate splits at most $m^k-(m-1)^k\le km^{k-1}$ cubes, for every $x$ and every $\sigma$.

*Proof.* Let $\varepsilon_i=\pm1$ be the sign of block $i$. Then each $P_i$ is monotone in direction $\varepsilon_i$, so $F(s)=\sum_iP_i(s_i)$ satisfies $F(s+\varepsilon)\ge F(s)$.

The extreme vertices of cube $c$ are $c^\pm=c+(\mathbf1\pm\varepsilon)/2$, and $c$ is split iff
$$F(c^-)<\theta-\alpha\cdot x\le F(c^+).$$
On a line of cubes $c_t=c+t\varepsilon$ we have $c_t^+=c_{t+1}^-$, so the intervals $(F(c_t^-),F(c_{t+1}^-)]$ are disjoint and at most one cube per line is split. The grid splits into $m^k-(m-1)^k$ such lines (count their first cubes). ∎

In the exact-integer check, random coherent gates with heavy-tailed or sparse weights and random arrangements attain the bound exactly. For example, $k=4,m=4$ gives 175 of 175, and $k=5,m=3$ gives 211 of 211.

### Lemma B2 (block-symmetric gates) [PROVED; VERIFIED]
A block-symmetric gate with direction $\beta$ splits at most
$$\min\!\big(m^k-(m-1)^k,\;2\sqrt2\,(\|\beta\|_1/\|\beta\|_2)\,m^{k-1}\big)\le\min(k,2\sqrt{2k})\,m^{k-1}$$
cubes.

*Proof.* The split cubes have disjoint interiors and lie in the slab $\{y\in[0,m]^k:|\beta\cdot y-\theta'|\le\|\beta\|_1\}$, of width $2\|\beta\|_1/\|\beta\|_2$. Every hyperplane section of $[0,m]^k$ has volume at most $\sqrt2m^{k-1}$: Ball (1986) for central sections, and Brunn's principle shows that central sections are the largest. ∎

Exact check: for $k=2$ the maximum is $2m-1$; for $k\ge3$ every observed value is below the bound.

### Corollary C [PROVED]
Let $f$ be an upper bound on every gate's split *fraction* (number of split cubes divided by $m^k$). Then $Sf\ge D_0(S)$.

**(i) Coherent circuits.** Here $f\le1-(1-\frac1m)^k\le\frac km$. If $S<2^{2k}$, then
$$S\ge\frac{m(2^k-3k-1)}{3k^2}.$$
In the balanced case this is $S\ge N(N-3k-1)/(3k^3)$.

**(ii) Block-symmetric circuits.** Here $f\le\min(k,2\sqrt{2k})/m$, which gives
$$S\ge\frac{m(2^k-3k-1)}{3k\min(k,2\sqrt{2k})}.$$
In the balanced case with $k\ge8$, this is $S\ge N(N-3k-1)/(6\sqrt2k^{5/2})$.

**(iii) Hybrid.** $S_{\rm coh}\big(1-(1-\frac1m)^k\big)+S_{\rm other}\ge D_0(S)$. ∎

**Small $k$.** Here one should use $C_k$, the largest number of bottom gates that any $h:\{0,1\}^k\to\{0,1\}$ needs. Exact LP enumeration (`ck.py`) gives $C_2=C_3=1$, so for $k\le3$ Corollary C only gives about $m/k$. For $k=2$, Theorem E below is stronger.

### Lemma B3 (arbitrary gates under the randomised count restriction) [PROVED, using the Kolmogorov–Rogozin inequality]
Let the arrangement $\sigma$ be uniformly random as well. Then every bottom gate $g$, whatever its weights, satisfies, for every integer $r\ge1$,
$$p(g):=\Pr_{\sigma,c,x}[g\text{ splits }c]\ \le\ \frac{kr}m+\frac{2\sqrt2\,C_{KR}(2k+1)}{\sqrt r}\ =\ O\!\big(k\,m^{-1/3}\big)\quad(r=\lceil m^{2/3}\rceil).$$
Here $C_{KR}$ is the absolute constant of the Kolmogorov–Rogozin inequality.

*Proof.*
1. **Reformulate the restriction.** For a uniformly random permutation and an independent uniform $c_i$, the live bit $\ell_i$ is uniform. Given $\ell_i$, the set of fixed ones is a uniform subset of $[m]\setminus\{\ell_i\}$ of uniform size. By the Beta-integral identity $\int_0^1q^a(1-q)^{M-a}dq=1/((M+1)\binom Ma)$, this equals: draw $q_i\sim U[0,1]$, then set the fixed bits i.i.d. Bernoulli($q_i$).
2. **Split off heavy live bits.** Let $T_i$ be the $r$ heaviest positions of block $i$, and let $\mu_i$ be the $(r+1)$-st largest $|\gamma_{i,t}|$. Let $\Lambda=\max_i\mu_i$, attained at block $i^*$. The event $E=\{\ell_i\notin T_i\ \forall i\}$ fails with probability at most $kr/m$.
3. **Window length.** On $E$, the window has length $\sum_i|\gamma_{i,\ell_i}|\le k\Lambda$.
4. **Anti-concentration.** On $E$, all $r$ positions of $T_{i^*}$ are fixed. Each carries a weight of magnitude $\ge\Lambda$ and is i.i.d. Bernoulli($q_{i^*}$) given everything else. By Kolmogorov–Rogozin, their sum lands in a given interval of length $\Lambda/2$ with probability at most $C_{KR}/\sqrt{r\min(q,1-q)}$. An interval of length $k\Lambda$ is covered by $2k+1$ such intervals.
5. **Integrate over $q$.** Using $\int_0^1\min(q,1-q)^{-1/2}dq=2\sqrt2$ gives the second term. If no block has more than $r$ nonzero weights, all live weights vanish on $E$ and only the first term remains. ∎

### Corollary C(iv) (hybrid with arbitrary gates) [PROVED]
Average Theorem A over a random $\sigma$. Lemma B1 holds for every $\sigma$. Hence
$$S_{\rm coh}\Big(1-(1-\tfrac1m)^k\Big)+S_{\rm other}\cdot O(km^{-1/3})\ \ge\ D_0(S).$$
So if $S<D_0m/(2k)$, then $S_{\rm other}=\Omega(D_0m^{1/3}/k)$. In the balanced case: every circuit with fewer than $N(N-3k-1)/(6k^3)\approx n^2/(24\log_2^3n)$ gates contains $\Omega(N^{4/3}/k^{7/3})=\Omega(n^{4/3}/\log^{7/3}n)$ gates that are not sign-coherent. ∎

### 2.6 How large is this? (`bound_table.py`, `crossover.py`; balanced case, bound solved self-consistently in $S$)

| k | n | coherent LB | block-sym. LB | $n^{3/2}$ | $n^{3/2}/\log_2^2n$ | $5n^2/16$ |
|---|---|---|---|---|---|---|
| 10 | 2.0e3 | 560 | 596 | 9.2e4 | 764 | 1.3e6 |
| 16 | 1.3e5 | 4.8e5 | 6.7e5 | 4.7e7 | 1.6e5 | 5.4e9 |
| 20 | 2.1e6 | 6.0e7 | 9.4e7 | 3.0e9 | 6.9e6 | 1.4e12 |
| 30 | 2.1e9 | 1.7e13 | 3.3e13 | 1.0e14 | 1.0e11 | 1.4e18 |
| 40 | 2.2e12 | 7.4e18 | 1.6e19 | 3.3e18 | 1.9e15 | 1.5e24 |
| 50 | 2.3e15 | 3.9e24 | 9.5e24 | 1.1e23 | 4.1e19 | 1.6e30 |

Crossovers:
- against $n^{3/2}/\log_2^2n$: $k=12$ (coherent), $k=11$ (block-symmetric);
- against $n^{3/2}$: $k=37$ (coherent), $k=35$ (block-symmetric).

**Where the loss is** (`percube_d.py`). For construction (d), the mean number of splitting gates per cube is 56, 127 and 232 at $(k,m)=(4,4),(5,5),(6,6)$, against $D_0=0.2$, 1.0 and 2.5. The largest per-gate split fraction is 0.52–0.61, against a coherent bound of 0.67–0.68. So the splitting lemma is nearly tight; the polylog loss is in the per-cube complexity.

---

## 3. $k=2$: $m-1\le\min\le 4\lceil m/2\rceil+m$

### Theorem E (lower bound) [PROVED]
For $k=2$, every circuit with sign-coherent bottom gates (in particular every block-symmetric circuit) has $S\ge m-1$.

*Proof.*
1. Take the XOR table. On every unit square, the circuit computes XOR or XNOR.
2. If all restricted bottom gates were constants or literals, the top gate would be a threshold function of $z$, which is impossible. So some gate restricts to one of the 8 non-literal threshold functions of two variables. These are exactly the "corner cuts": one vertex on one side, three on the other.
3. By the Ring Lemma, each gate cuts corners of at most 4 of the $4(m-1)$ boundary squares.
4. Every boundary square needs a cut, so $S\ge m-1$. ∎

### Ring Lemma [PROVED; VERIFIED exhaustively for all lines and $m\le12$, `ring_lemma.py`]
Let $U$ be an up-set of the vertex grid $\{0..m\}^2$. After the reflections $s_i\mapsto m-s_i$, the 1-set of a coherent gate has this form, for every table and arrangement. Then at most 4 boundary squares $Q$ have $|U\cap Q|\in\{1,3\}$.

*Proof.*
1. The mixed squares form a monotone lattice path with steps $R$ and $D$. A square is a corner cut iff the path turns there, counting the virtual steps that enter and leave the grid.
2. By monotonicity, the boundary squares in the top row or left column form a prefix of the path, and those in the bottom row or right column form a suffix.
3. Inside the prefix, all internal steps point the same way: $R$ along the top row, $D$ down the left column, with a switch possible only at the corner square. So the prefix contains at most 2 turns, at its first and last squares. The same holds for the suffix. ∎

**This argument cannot give more.** The minimum number of lines that cut a corner of every unit square is $\tau_m=2,3,4,4,5$ for $m=2..6$. Its LP value is $m-1$ for $m=3..6$, and the optimal dual puts weight $1/4$ on each boundary square, which is exactly the Ring Lemma (`cornercover.py`, `cc_dual.py`). The solver's $\ge6$ at $m=6$ therefore comes from interaction between several tables.

### Theorem G (upper bound) [PROVED; VERIFIED in exact rationals for $m\le20$, `k2_construction_exact.py`]
For $k=2$ there is a block-symmetric circuit with $4\lceil m/2\rceil+m$ bottom gates. Its bottom weights are in $\{0,1\}$; its top weights are $-4$ and $-2$ on the gates, $(5,5)$ on $s$ and $(8,2,\tfrac32,1)$ on $x$.

The table index is $c=b_1+2b_2$. The bottom gates are:
- $[s_1+x_0\ge2j]$ with top weight $-4$, and $[s_1+x_2\ge2j]$ with top weight $-2$, for $j\le\lceil m/2\rceil$;
- $[s_2+x_0\ge2j]$ with top weight $-4$, and $[s_2+x_1\ge2j]$ with top weight $-2$, for $j\le\lceil m/2\rceil$;
- $[s_1+s_2+x_0\ge2j]$ with top weight $-4$, for $j\le m$.

The top gate is
$$F=\sum v_jg_j+5s_1+5s_2+8x_0+2x_1+\tfrac32x_2+x_3-\tfrac{13}2,\qquad \text{output }[F\ge0].$$

*Proof.* The sawtooth identity
$$Vt-2V\sum_{j\le\lceil T/2\rceil}[t+x_c\ge2j]=V(-1)^{x_c}(t\bmod2)\qquad (0\le t\le T)$$
gives
$$F=D(x)+4(-1)^{x_0}[b\ne00]+(-1)^{x_2}b_1+(-1)^{x_1}b_2,$$
which no longer depends on $m$. A finite check over 16 tables × 4 addresses shows $[F\ge0]=x_b$. ∎

**How it was found** (`k2_gadget_search3.py`, `k2_gadget_search4.py`). It is the optimum of a family: one sawtooth gadget per sign-controlled amplitude per character.
- A dominance argument shows that each character's own table needs its amplitude to dominate the other two.
- Hence at most one character can use a single gadget, and the cheapest feasible configuration costs $\approx3m$.
- Exhaustive search confirms that cheaper configurations, such as $(1,1),(1,1),(1)$ and $(2,1),(2,1),(1)$, are infeasible.
- The solver's optimal 3-gate circuits at $m=1,2$ use non-axis directions such as $(3,2),(1,3),(2,3)$, so this family is not optimal for small $m$.

---

## 4. Exact-sum model

### $k=1$: minimum $=2\lceil m/2\rceil$ [PROVED; VERIFIED for $m\le6$ by `exact_min.py` and for $m\le40$ by `k1_exact_constr.py`]

**Lower bound.** Let $w$ be the top weight on $s$.
- If $w\ne0$: the constant tables need total step $-w$ in every gap, so $S\ge m$.
- If $w=0$: the tables $(0,1)$ and $(1,0)$ need steps $\pm1$ in every gap, so $S\ge m$.
- Now let $m$ be odd and $S=m$, so every gap is crossed exactly once.
  - Case $w\ne0$: all effective steps equal $-w$. Table $(0,1)$ needs $1-(-1)^a/w$ gates in gap $a$, and table $(1,0)$ needs $1+(-1)^a/w$. Each total must be at most $m$, and they sum to $2m$, so each equals $m$. That forces $1/w=0$.
  - Case $w=0$: the multiset of steps would have to be both $\{+1^{(m+1)/2},-1^{(m-1)/2}\}$ and its mirror image.

**Construction.**
$$x_{s\bmod2}=s+x_0-\sum_{j\le2\lceil m/2\rceil}[s\ge p_j(x)]$$
with
$$p_{2i-1}=2i-\tfrac32-\tfrac3{10}x_0+\tfrac34x_1,\qquad p_{2i}=2i-\tfrac12-\tfrac35x_0+\tfrac25x_1 .$$

### $k=2$, exact (block-symmetric) [VERIFIED, z3 with exact re-verification]

| m | 1 | 2 | 3 |
|---|---|---|---|
| exact | 4 | 5 | at least 6 (S=5 UNSAT in 372 s; S=6 undecided, stopped after about 14 min) |
| sign | 3 | 3 | at least 5 |

### What the exact model does and does not add
- Theorems A, E and Corollary C apply to it verbatim.
- It does **not** help the per-cube method: the exact per-cube complexity of a random function is also $2^k/\mathrm{poly}(k)$ (count subspaces with Odlyzko's bound).
- The Kane–Williams restricted function, an OR of $N$ ANDs, is itself an exact sum, so the barrier of §5 holds verbatim for exact circuits.
- I found no exact-model argument that beats the sign-model results.

---

## 5. Barrier for survival-based methods in the general model [PROVED]

**Proposition F.** Let $\mathcal D$ be any distribution over partial assignments that leave exactly one live bit per address block. For uniformly random $\varepsilon\in\{\pm1\}^{km}$, let
$$g_\varepsilon=\Big[\sum\varepsilon_{i,t}a_{i,t}\ge\tfrac12\Big].$$
Then $\mathbb E_\varepsilon\Pr_\rho[g_\varepsilon|_\rho\text{ non-constant}]\ge1/(2\sqrt{2km})$.

*Proof.* Fix $\rho$, and let $K\le k(m-1)$ be its number of fixed ones.
- The fixed part $F$ is a sum of $K$ independent random signs.
- With $P$ the number of live weights equal to $+1$ and $Q=k-P$, the gate is non-constant iff $F\in\{1-P,\dots,Q\}$.
- For $k\ge2$, both $0$ and $1$ lie in this window with probability $\ge\frac12$, and $\Pr[F\in\{0,1\}]=\binom K{\lfloor K/2\rfloor}2^{-K}\ge(2K+2)^{-1/2}$.
- For $k=1$, use the point allowed by parity. ∎

**Consequence.** Every argument of the form

> $\sum_j\Pr[g_j\text{ survives}]\ge R$, with $R$ at most the complexity of the restricted function

satisfies $R\le N+1$, because the restricted function is an OR of $N$ ANDs (or a $k$-bit function). A circuit made of gates like $g_\varepsilon$ would therefore defeat it, so such an argument can prove at most
$$S\le2\sqrt{2km}(N+1)=O(n^{3/2}).$$
This applies to:
- Kane–Williams and Theorem A, for any restriction distribution and any arrangement;
- MAJ∘MAJ, since $g_\varepsilon$ has weights $\pm1$. So bounded weights alone do not help survival-based methods (Target 3).

Counting the whole window improves the survival probability to $\Omega(\sqrt{k/m})$. Coherent gates escape because of Lemma B1. The obstruction is exactly **gates that are balanced inside a block**.

Monte Carlo of the randomised count restriction (`survival_mc.py`, $k=3$, $m=64$, 40k samples per gate, threshold at the median):

| gate type | split probability $p(g)$ |
|---|---|
| block-symmetric | 0.035 |
| heavy-tailed coherent | 0.025 |
| subset-majority | 0.033 |
| balanced $\pm1$ | 0.185 |
| Gaussian weights | 0.127 |

The three coherent gate types stay below the Lemma B1 bound of 0.046. The balanced $\pm1$ gate sits at about $0.85\sqrt{k/m}$ ($\sqrt{k/m}=0.217$). All five values are below the Lemma B3 bound $km^{-1/3}=0.75$.

---

## 6. Data table and sanity checks

"lb" means proven by `/tmp/andreev_gap/verify/min_circuit.py` (z3, real weights; runs in `/tmp/andreev_gap/big2/` and `verify/report.md`) or by `exact_min.py`. "ub" means a verified circuit.

| model | (k,m) | solver | our rigorous bounds (this report) | consistent? |
|---|---|---|---|---|
| sign, block-sym. | (1,m) | min = ⌈m/2⌉ (m ≤ 12) | known 1-D argument ⌈m/2⌉ | yes |
| sign, block-sym. | (2,1) | min = 3 | lb 0; ub 5 | yes |
| sign, block-sym. | (2,2) | min = 3 | lb 1; ub 6 | yes |
| sign, block-sym. | (2,3) | lb 5 | lb 2; **ub 11** | yes |
| sign, block-sym. | (2,4) | lb 5 | lb 3; **ub 12** | yes |
| sign, block-sym. | (2,5) | lb 5 | lb 4; **ub 17** | yes |
| sign, block-sym. | (2,6) | lb 6 | lb 5; **ub 18** | yes |
| sign, block-sym. | (2,8) | lb 6 | **lb 7**; **ub 24** | yes |
| sign, block-sym. | (2,10) | lb 6 | **lb 9**; **ub 30** | yes |
| sign, block-sym. | (3,1) | lb 3 | lb 1 ($C_3=1$); ub 81 (constr. d) | yes |
| exact, block-sym. | (1,m) | min = 2⌈m/2⌉ (m ≤ 6) | = 2⌈m/2⌉ for all m | yes |
| exact, block-sym. | (2,1), (2,2) | min = 4, 5 | – | – |
| exact, block-sym. | (2,3) | lb 6 | – | – |

None of our claimed lower bounds exceeds a known minimum.

The bounded-weight CP-SAT searches (`ub_search.py`; $|\beta|\le3$, $|\alpha|\le12$, $v\le40$) recover the optima at $(2,1)$ and $(2,2)$ in seconds. For $(2,3)$ they returned UNKNOWN after 900 s at both $S=5$ and $S=6$, and I stopped the loop. So there is no small-$S$ upper bound for $m\ge3$ beyond Theorem G.

**$k=2$ growth law [EVIDENCE].** Both bounds are linear: $m-1\le\min\le4\lceil m/2\rceil+m$. At $m=6$ the solver lower bound of 6 exceeds $m-1$, which points to a slope strictly above 1. The small-$m$ optima (3 at $m=1,2$, against 5 and 6 for Theorem G) show that Theorem G is not optimal. My guess for the slope is about 1.5–2 [CONJECTURE].

**Consistency with the general bounds.**
- For fixed $k=2$ the general constructions are already linear in $m$ ($12m+18$ for the 5/8 construction, about $14m$ for (d)). A Kane–Williams-type survival argument gives only about $\sqrt m$ there, since the restricted function needs $C_2=1$ gate and survival is about $k/\sqrt m$. The bounds $m-1\le\min\le4\lceil m/2\rceil+m$ are consistent with both.
- For growing $k$, Corollary C sits below (5/16)$n^2$ by the polylog factor in the table of §2.6, and above $n^{3/2}/\log^2n$ from $k\approx12$.

**[CONJECTURE] Block-symmetric and coherent complexity is $\Theta(n^2)$ in the balanced case.** Proving it needs $\Omega(N)$ splitting gates per cube: a depth-two lower bound of $\Omega(2^k)$ for random $k$-bit functions under the constraint of fixed gate directions across cubes, which counting alone cannot give.

---

## 7. Most promising next steps

1. **Sharpen Lemma B3.** Improve the $O(km^{-1/3})$ survival bound for arbitrary gates to $\tilde O(k/\sqrt m)$, on average over random $\sigma$ and $x$.
   - Uniform size followed by a uniform subset is exactly a mixture of $p$-biased product measures with $p\sim U[0,1]$, so Littlewood–Offord applies conditional on $p$.
   - The remaining difficulty is the Kane–Williams one: heavy live weights.
   - With Corollary C(iii), the result would be that every circuit has $\tilde\Omega(n^{3/2})$ mixed-sign gates or $\tilde\Omega(n^2)$ gates.
2. **Mixed-sign gates in the exact model.** Averaging over within-block permutations preserves exactness, giving $A=\sum v_j\hat g_j+L$.
   - Block-balanced gates become smooth functions of $s$ (hypergeometric tails) and cannot carry the parity of $s_i$.
   - With weights bounded by $V$, this should give $\Omega(Nm/V)$ for exact MAJ∘MAJ [sketch only, unproved].
3. **$k=2$.** Combine the Ring Lemma (XOR table) with boundary-row and boundary-column conditions from the dictator tables, using fixed slopes, to beat $m-1$. Search for upper bounds with fixed direction menus.

---

## 8. Files

| file | content |
|---|---|
| `report.md` | this report |
| `ck.py` | $C_2=C_3=1$ (exact LP enumeration of all threshold functions) |
| `cornercover.py`, `cc_dual.py` | $k=2$ corner-cut covers, LP value and dual |
| `ring_lemma.py` | exhaustive Ring Lemma check, and check that at most $2m-1$ squares are cut, for $m\le12$ |
| `split_checks_exact.py` | Lemmas B1 and B2 in exact integers (`split_checks.py`: superseded float version) |
| `percube_d.py` | per-cube splitting statistics of construction (d) |
| `survival_mc.py` | Monte Carlo of gate survival under the randomised count restriction |
| `bound_table.py`, `crossover.py` | explicit bounds of Corollary C; crossovers |
| `k2_gadget_search*.py`, `k2_construction.py`, `k2_construction_exact.py` | the $k=2$ construction (Theorem G): search and exact verification |
| `exact_min.py`, `exact_runs.log`, `exact_23.log`, `k1_exact_constr.py` | exact-sum model solver, runs, and $k=1$ construction |
| `ub_search.py`, `ub_k2_a.log` | CP-SAT upper-bound search (bounded weights; SAT answers are verified exactly) |
