<!-- Copyright (c) 2026 Christian Reitwiessner. -->
Authors: Christian Reitwiessner

**Archive correction:** This source report contains claims rejected or narrowed by the completed [independent referee](../review_coherence/report.md). In particular, do not use its zero-sum supersession claim, universal method-barrier wording, Proposition 5.1, or old one-table-bit frontier without the corrections. See [the update](../../docs/UPDATE_2026-11-09.md).

# Must every depth-two threshold circuit for Andreev's function be essentially sign-coherent?

Directory: `/tmp/andreev_gap/coherence_fable/`. Scripts run with `python3 -I` and put `pydeps_local/` (a local numpy/scipy install, because the compiled extensions in `/tmp/pydeps` are missing) and `/tmp/pydeps` (z3) on `sys.path` themselves. Logs are in `logs/`.

Scope, after the user's update: only exponents matter. Everything below is about the balanced case $km=N=2^k$, $n=2N$, unless a parameter is written explicitly. Constants and polylog factors are ignored in the verdicts, but kept in theorem statements where they are free.

Notation follows the brief and `push_lower/report.md`: $N=2^k$ table bits $x_c$, $k$ address blocks of $m$ bits, $s_i=|a_i|$, $b=s\bmod 2$, $A=x_b$. A circuit has $S$ bottom gates $g_j=[\alpha_j\cdot x+\sum_{i,l}\gamma_{j,i,l}a_{i,l}\ge\theta_j]$ and a top gate that reads the gates and the raw inputs. An *arrangement* $\sigma=(\sigma_1,\dots,\sigma_k)$ is one permutation per block; the *count restriction* fixes block $i$ to the thermometer string of weight $s_i$ along $\sigma_i$; a *cube* is $c\in\{0..m-1\}^k$ with vertices $c+z$, $z\in\{0,1\}^k$, and $F_j(s)=\sum_iP_{j,i}(s_i)$ with $P_{j,i}(s)=\sum_{t\le s}\gamma_{j,i,\sigma_i(t)}$ is the walk of gate $j$.

Labels: **[PROVED]** complete proof in this file; **[VERIFIED]** exact or Monte-Carlo computation done here, with the script named; **[CONJECTURE]**; **[REFUTED]**.

---

## 0. Summary

1. **The parity obstacle is about methods, not statements** [PROVED, §1]. $\mathrm{size}(A_{1,m})=\mathrm{par}(m+1)$ exactly. A *syntactic* coherence normal form would prove $\mathrm{par}(M)\ge M/\mathrm{polylog}$ (open). A normal form proved only for circuits computing $A_{k,m}$ implies nothing about parity, and no parity lower bound implies anything about balanced Andreev by restrictions; the missing link is a direct-sum theorem over the $N$ characters (§5.2, [CONJECTURE]).
2. **Information form of the cube count** [PROVED, Thm 2.1]: on every cube, $2^k\le\sum_jH(Z^c_j)+\log_2(2^k+1)$ where $Z^c_j$ is the position of the gate's table part $\alpha_j\cdot x$ among its $\le2^k$ breakpoints. Pure-address gates contribute nothing, however many cubes they split; gates with many table weights above the live-weight scale are active on few tables (Littlewood–Offord in $x$).
3. **The barrier holds for adaptive arrangements and for information accounting** [PROVED, Thm 3.1; VERIFIED]: $O(n^{3/2}\log n)$ random one-table-bit $\pm1$ gates meet the (refined) demand on every cube of **every** arrangement simultaneously. Hence no argument "demand per cube $+$ per-gate supply", with the arrangement chosen after seeing the circuit and with any per-gate charge $\le O(k)\cdot$[split], can exceed $n^{3/2}\log n$. This closes the T2 routes "re-choose the order per gate group", "charge mixed gates differently", "use the table to kill pure-address gates".
4. **Drift Lemma** [PROVED, Lemma 4.1; VERIFIED to the constant]: under a random arrangement a gate whose block has relative signed drift $\delta$ (and bounded weight ratio) splits a $\tilde O(k/(\delta m))$ fraction of cubes. Minority count is irrelevant; only *balance* matters. Numerically the split fraction is $\approx(\text{coherent rate})/\delta$ for $\delta\ge1/16$ (e.g. $k/(\delta m)$ at $k=2$) and $\approx1.4\sqrt{k/m}$ at $\delta=0$.
5. **Structure of sub-quadratic circuits** [PROVED, Thm 4.2]: a circuit with $n^{2-\varepsilon}$ gates contains $\tilde\Omega(n^{3/2})$ gates that are balanced to relative drift $n^{-\varepsilon+o(1)}$ in every bounded-range block and read table bits. "Essentially coherent" fails as a necessary structure only through such zero-sum gates.
6. **No asymptotic refutation** (§5): at fixed $k$ a polynomial saving is equivalent to sublinear depth-two parity [known]; the only known mechanism, staircases on linear forms, is sign-blind [PROVED, Prop. 5.1]; a mixed family would need the four properties of §5.4, and none is known.
7. **Smallest honest target** (§6): circuits whose gates read one table bit. There correctness is an explicit $\ell_1$-dominance condition on affine functions of the table [PROVED, Prop. 6.1], the barrier gates live in the class, and beating $n^{3/2}$ requires exactly the non-additive, cross-cube argument that the general problem needs.

---

## 1. What the parity reduction does and does not block

Write $\mathrm{par}(M)$ for the least number of bottom gates of a depth-two threshold circuit (top gate reading gates and inputs) for PARITY of $M$ bits, and $\mathrm{par}_{\rm coh}(M)=\lfloor M/2\rfloor$ for its coherent (unate-gate) version (`mixed_sign/report.md`, Prop. 1.2).

### 1.1 $k=1$: Andreev *is* parity [PROVED]

**Proposition 1.1.** $\mathrm{size}(A_{1,m})=\mathrm{par}(m+1)$ for every $m$.

*Proof.* $\ge$: substitute $x_1=1-x_0$ in every gate (an affine substitution keeps threshold gates); then $A_{1,m}=x_0\oplus\bigoplus_la_l$, parity of $m+1$ bits.
$\le$: let $T(a,y)$ be the normalised score of a parity circuit on $(a,y)$ with $T\ge1$ when the parity is $1$, $T\le-1$ otherwise, and $|T|\le B$. Put $y:=x_0$ and output $[T(a,x_0)+2B(x_0+x_1-1)\ge0]$. If $x_0\ne x_1$ this is $[T\ge0]=x_0\oplus\mathrm{par}(a)=x_{s\bmod2}$. If $x_0=x_1=1$ it is $1$, if $x_0=x_1=0$ it is $0$; both equal $x_{s\bmod2}$. No gate was added. ∎

So at $k=1$ the coherence question for Andreev is literally the open question whether $\mathrm{par}(M)=\Theta(M)$ (known: $\Omega(\sqrt M)$, Impagliazzo–Paturi–Saks). At fixed $k\ge2$, `mixed_sign` Cor. 1.5 gives the one-sided reduction $\mathrm{size}(A_{k,m})\ge\mathrm{par}(km+1)$: an $o(m)$ mixed-sign family at fixed $k$ would give sublinear depth-two parity circuits.

### 1.2 The barrier constrains the method, not the statement [PROVED]

The brief states: "(T1) with $f(S)=S\cdot\mathrm{polylog}$ would imply a near-linear lower bound for parity". This is true for a **syntactic** normal form and false for a **function-dependent** one:

* **Syntactic.** If a map $\Phi$ turns *every* depth-two circuit $C$ into a coherent circuit computing the same function with $|\Phi(C)|\le|C|\cdot\mathrm{polylog}$, apply it to a parity circuit: $\lfloor M/2\rfloor\le\mathrm{par}_{\rm coh}(M)\le\mathrm{par}(M)\,\mathrm{polylog}$, so $\mathrm{par}(M)\ge M/\mathrm{polylog}$, which is open. Such a $\Phi$ is therefore out of reach today.
* **Function-dependent.** Suppose only: every circuit computing $A_{k,m}$ with $S$ gates can be converted into a coherent one computing $A_{k,m}$ with $S\cdot\mathrm{polylog}$ gates. This implies $\mathrm{size}(A_{k,m})\ge n^2/\mathrm{polylog}$, which is the goal, but it implies **nothing** about parity: the only parity instance inside $A_{k,m}$ has $M=km+1\le n$ bits, its coherent lower bound $\lfloor M/2\rfloor\le n/2$ is already below the known general bound $\mathrm{size}(A_{k,m})=\tilde\Omega(n^{3/2})$ (Kane–Williams), and a parity circuit is not an Andreev circuit, so there is nothing to feed into the normal form.

So the parity obstacle says: *any proof of T1 must use the table.* It does not say T1 is as hard as the parity conjecture. Conversely (§6) there is no implication from a parity lower bound to an Andreev bound in the balanced case either, so the two problems are linked by method, not by reductions.

---

## 2. The information form of the cube count: only table-reading gates count [PROVED]

Theorem A of `push_lower` counts *all* gates that are non-constant on a cube. Tracking what each gate's restriction actually depends on gives a sharper and more structured inequality.

Fix $\sigma$ and a cube $c$. For gate $j$ put $Y_j(x)=\alpha_j\cdot x$ (its table part), $\lambda_{j,i}=\gamma_{j,i,\sigma_i(c_i+1)}$ (live weights) and the breakpoint set
$$B_j(c)=\{\theta_j-F_j(c+z):z\in\{0,1\}^k\},\qquad |B_j(c)|\le2^k .$$
On the cube the gate is $z\mapsto[\lambda_j\cdot z\ge\theta_j-F_j(c)-Y_j(x)]$, and this function is determined by the **position** of $Y_j(x)$ among the breakpoints, $\#\{\beta\in B_j(c):\beta\le Y_j(x)\}$. Positions $0$ and $|B_j(c)|$ give the two constant functions; we merge them into one symbol and let $Z^c_j(x)\in\{\text{inactive},1,\dots,|B_j(c)|-1\}$ be the result, so that $Z^c_j$ records the restricted gate when it is non-constant and only the fact of constancy otherwise.

**Theorem 2.1 (information form).** For every circuit computing $A_{k,m}$, every $\sigma$ and every cube $c$, with $x$ uniform on $\{0,1\}^N$,
$$2^k\ \le\ \sum_{j=1}^S H\big(Z^c_j(x)\big)+\log_2(2^k+1).$$
Moreover, with $W_j(c)=(\min B_j(c),\max B_j(c)]$ (the activity window, of length $R_j(c)=\sum_i|\lambda_{j,i}|$) and $p^c_j=\Pr_x[Y_j(x)\in W_j(c)]$:

1. $H(Z^c_j)\le h(p^c_j)+p^c_j\,k\le p^c_j\big(k+\log_2(e/p^c_j)\big)+ (1-p^c_j)\log_2\frac1{1-p^c_j}$, where $h$ is binary entropy and the last term is at most $p^c_j\log_2e$;
2. $H(Z^c_j)\le\log_2\big(1+\#\{\text{values of }Y_j\}\big)\le\min\big(k,\ |\mathrm{supp}\,\alpha_j|\big)$ when the gate is non-constant on the cube, and $H(Z^c_j)=0$ if $\alpha_j=0$;
3. $p^c_j\le Q\big(Y_j;R_j(c)\big):=\sup_t\Pr_x\big[Y_j(x)\in(t,t+R_j(c)]\big]$, the Lévy concentration function of the table part at the scale of the live address weights. In particular, if at least $r$ table weights of gate $j$ have $|\alpha_{j,d}|\ge R_j(c)$, then $p^c_j\le C_{\rm LO}/\sqrt r$ (Erdős–Littlewood–Offord).

*Proof.* The restricted top gate is $z\mapsto[\sum_jv_jg_j|_c(z)+\mu\cdot z\ge\kappa(x)]$, and the data $(v_j)$, $(\lambda_j)$, $\mu$ do not depend on $x$ (`push_lower`, Thm A). Given $(Z^c_j(x))_j$, the restriction of every *active* gate is known; the constant gates (symbol 'inactive') are absorbed into $\kappa$: with $L'_x(z)=\sum_{j\text{ active}}v_jg_j|_c(z)+\mu\cdot z$ and $\kappa'(x)=\kappa(x)-\sum_{j\text{ inactive}}v_jg_j|_c$, the output is $[L'_x(z)\ge\kappa'(x)]$, so the positions of the active gates plus the position of $\kappa'$ among the $\le2^k$ values of $L'_x$ (one of $2^k+1$ possibilities) determine $h_{x,c}(z)=x_{c'\oplus z}$, hence $x$. Subadditivity gives $H(x)=2^k\le\sum_jH(Z^c_j)+\log_2(2^k+1)$. (1): $Z^c_j$ is 'inactive' with probability $1-p$ and one of at most $2^k-1$ interior positions otherwise, so $H(Z^c_j)\le h(p)+p\log_2(2^k-1)$, and $h(p)\le p\log_2(e/p)+(1-p)\log_2(1/(1-p))$. (2): $Z^c_j$ is a function of $Y_j$, and $Y_j=\alpha_j\cdot x$ takes at most $2^{|\mathrm{supp}\,\alpha_j|}$ values. (3) is the definition of $Q$ and the Erdős bound for sums of independent two-valued variables. ∎

**What this adds.**
* A gate with no table weights contributes **zero**, however many cubes it splits. The alternating "$\sigma$-parity gate" $[\sum_{i,l}(-1)^{\sigma_i^{-1}(l)}a_{i,l}\ge\tfrac12]$, which splits *every* cube of $\sigma$, is inert for the count. Theorem A charged it $k+\log_2S$ bits per cube.
* A gate that reads many table bits with weights at least the live-weight scale is active on few tables (item 3). A gate that is active on many cubes for many tables must have a table part that is *concentrated at the scale of its live address weights*: at most $O(1/(p^c_j)^2)$ table weights of magnitude $\ge R_j(c)$.
* The demand is now a sum over gates of a *per-gate information budget*; the next section shows that even this sharper demand is met by gate sets of size $\tilde O(n^{3/2})$ under **every** arrangement at once, so no per-gate accounting, however clever, and no choice of arrangement can lift the method above $n^{3/2}$.

---

## 3. The barrier survives adaptive arrangements and information accounting [PROVED, VERIFIED]

`push_lower` Prop. F shows that for every *fixed* distribution over one-live-bit restrictions a random $\pm1$ gate survives with probability $\ge1/(2\sqrt{2km})$. It leaves open the two escape routes named in the brief: choose the arrangement **after seeing the circuit** (one arrangement per circuit, or a few), and **charge gates by information** instead of by survival. Both are closed by the following theorem.

**Barrier gate.** $g_{\varepsilon,d}=[\sum_{i,l}\varepsilon_{i,l}a_{i,l}+x_d\ge\tfrac12]$ with $\varepsilon\in\{\pm1\}^{km}$ uniform and $d\in\{0,1\}^k$ uniform. It reads one table bit; its address part is a balanced random signed sum.

**Lemma 3.0 (one gate, one cube).** Fix any $\sigma$ and cube $c$ and let $K=\sum_ic_i$. For the barrier gate, let $P$ be the number of live weights $\varepsilon_{i,\sigma_i(c_i+1)}$ equal to $+1$ and $Q=k-P$, and let $F$ be the sum of the $K$ fixed weights. Then the restriction of $g_{\varepsilon,d}$ to the cube **depends on $x_d$** (so $H(Z^c)=1$ bit) iff $F\in[-P,Q]$, and
$$\Pr_\varepsilon\big[F\in[-P,Q]\big]\ \ge\ \frac{1}{2\sqrt{2km}}\qquad\text{for every }(\sigma,c).$$
*Proof.* On the cube the gate is $[F+\lambda\cdot z+x_d\ge\tfrac12]$ with $\lambda\in\{\pm1\}^k$. The integer $F+\lambda\cdot z$ takes every value in $[F-Q,F+P]$ as $z$ varies. The two values of $x_d$ give $[F+\lambda\cdot z\ge1]$ and $[F+\lambda\cdot z\ge0]$, which differ iff some vertex has $F+\lambda\cdot z=0$, i.e. iff $F\in[-P,Q]$. This window contains $0$ and, since $P+Q=k\ge1$, also $-1$ or $+1$, so $\Pr[F\in[-P,Q]]\ge\Pr[F=0]$ for even $K$ and $\ge\Pr[F=\mp1]$ for odd $K$ (whichever sign the window allows). Both are $\binom{K}{\lfloor K/2\rfloor}2^{-K}\ge(2K+2)^{-1/2}$ (`push_lower` Prop. F, verified there for $K\le2\cdot10^6$), and $K\le k(m-1)$ gives $(2K+2)^{-1/2}\ge(2km)^{-1/2}\ge1/(2\sqrt{2km})$. ∎

Exact values (`barrier_const.py`, `logs/barrier_const.log`): the minimum over cubes of this probability is $2.0$–$10.1$ times the bound $1/(2\sqrt{2km})$ for $k\le8$, $m\le64$, and the average over a uniform cube is $(0.64$–$0.93)\sqrt{k/m}$ — the cube-averaged information activity of a barrier gate is $\Theta(\sqrt{k/m})$ bits.

**Theorem 3.1 (adaptive-arrangement barrier).** There is an absolute constant $C$ such that for $S\ge C\,(km)^{3/2}\ln(km)$ a set of $S$ independent barrier gates satisfies, with probability $\ge1/2$ over the gates, **simultaneously for every arrangement $\sigma$ and every cube $c$**:
$$\sum_{j=1}^SH_x\big(Z^c_j(x)\big)\ \ge\ \#\{j:\ g_j|_c\text{ depends on }x\}\ \ge\ \frac{S}{4\sqrt{2km}}\ \ge\ 2^k .$$
In the balanced case $S=O(n^{3/2}\log n)$.

*Proof.* Fix $(\sigma,c)$. The indicators $I_j=[g_j|_c$ depends on $x_{d_j}]$ are independent over $j$ (independent gates) with $\Pr[I_j=1]\ge p:=1/(2\sqrt{2km})$ by Lemma 3.0, so $\mu=\mathbb E\sum_jI_j\ge Sp$ and by the Chernoff bound $\Pr[\sum_jI_j<\mu/2]\le e^{-\mu/8}\le e^{-Sp/8}$. The number of pairs $(\sigma,c)$ is $(m!)^km^k\le e^{km\ln m+k\ln m}\le e^{2km\ln m}$. A union bound gives failure probability $\le e^{2km\ln m-Sp/8}\le1/2$ once $Sp/8\ge2km\ln m+1$, i.e. $S\ge16\sqrt2\,(km)^{3/2}\ln m+O(\sqrt{km})$. When $I_j=1$ the position variable $Z^c_j$ is a fair coin (it is a function of $x_{d_j}$ that takes two values), so $H(Z^c_j)\ge1$, and $\mu/2\ge Sp/2\ge 2^k$ for the stated $S$ in the balanced case ($km=2^k$). ∎

**What it rules out.** Every lower-bound argument of the form
> "a correct circuit meets the demand of Theorem 2.1 (or Theorem A) on every cube of some arrangement $\sigma^*$ chosen as a function of the circuit; a gate of class $\mathcal C$ contributes at most $f_{\mathcal C}$ to the demand on average; hence $S\ge\dots$"

is capped at $S=O(n^{3/2}\log n)$: the barrier set meets the demand under *every* $\sigma^*$, and it does so with gates that read a single table bit, have minority count $\approx m/2$, and are balanced. The same holds if the demand is averaged over cubes, over arrangements, or over *several* arrangements at once, and if the per-gate charge is any function bounded by $O(k)$ times the split indicator (information, number of breakpoints crossed, etc.), since $\sum_jH(Z^c_j)\ge2^k$ already with one bit per split gate. The only way past $n^{3/2}$ is a demand that the barrier set does **not** meet, which must use that the top gate is a *threshold* of the gate outputs with weights $v_j$ fixed across all cubes and tables (§6).

**Numerical check of the adaptive route below the union-bound regime** (`adaptive_arr.py`, `logs/adaptive_k2.log`, `logs/adaptive_k3.log`). For random $\pm1$ gate sets we minimised the total demand met, $T(\sigma)=\sum_j\#\{c:g_j$ informative on $c\}$, by local search over arrangements (300–600 accepted-if-not-worse swap steps, two starts; a heuristic, so the ratios are upper bounds on the true minimum) and compared with the mean over random arrangements:

| $k$ | $m$ | $S=km/4$: $\min T/\bar T$ | $S=km$: $\min T/\bar T$ | $S=(km)^{3/2}$: $\min T/\bar T$ |
|---|---|---|---|---|
| 2 | 8 | 0.18 | 0.41 | 0.72 |
| 2 | 16 | 0.21 | 0.43 | 0.78 |
| 2 | 32 | 0.22 | 0.49 | 0.85 |
| 2 | 64 | 0.37 | 0.69 | – |
| 2 | 128 | 0.53 | 0.76 | 0.94 |
| 3 | 8 | 0.16 | 0.55 | 0.79 |
| 3 | 16 | 0.21 | 0.53 | 0.80 |
| 3 | 32 | 0.25 | 0.55 | 0.87 |

With few gates an adapted arrangement does lower the demand met by a factor 2–5 (one can nearly sort a handful of sign patterns), exactly as the Runs Lemma predicts; at $S=(km)^{3/2}$ the reduction shrinks with $m$, consistent with Theorem 3.1. (The log also reports the per-cube minimum, which is about half the per-cube mean because corner cubes have fewer fixed bits.)

---

## 4. Which mixed gates can split many cubes? Only balanced ones [PROVED, VERIFIED]

The Runs Lemma (`mixed_sign` 2.1) bounds the splits of a gate by its number of sign changes along $\sigma$, a worst case over thresholds and arrangements. Under a *random* arrangement the picture is much sharper: what matters is not how many weights have the minority sign but whether the signed sum of the block is close to zero.

**Monte Carlo** (`defect_split.py`, `logs/defect_k{2,3,4}.log`; split fraction under a random arrangement and uniform cube, threshold at the median of the walk):

| $k=2$, $m$ | coherent ($+1$ everywhere) | coherent with $\lceil\sqrt m\rceil$ random $-1$ per block | balanced $\pm1$ |
|---|---|---|---|
| 16 | 0.121 ($k/m=0.125$) | 0.225 | 0.365 ($\sqrt{k/m}=0.354$) |
| 64 | 0.031 | 0.040 | 0.176 |
| 256 | 0.0078 | 0.0088 | 0.095 ($\sqrt{k/m}=0.088$) |

The "defect" gate has minority count $\sqrt m$ per block, hence up to $1+2\sqrt m$ runs, and the Runs Lemma allows it a split fraction of order $k\sqrt m/m$; in reality it splits like a coherent gate. The reason is drift: its walk has slope $1-2/\sqrt m$ with unit dips, so it crosses any level $O(1)$ times. This is a general phenomenon.

**Lemma 4.1 (Drift Lemma).** Let $g$ be a bottom gate, $g_{\max}=\max_{i,l}|\gamma_{i,l}|$ its largest address weight. Suppose some block $i$ has all weights in $[g_{\max}/W,\,g_{\max}]$ in magnitude and relative drift
$$\delta:=\frac{|\sum_l\gamma_{i,l}|}{m\,g_{\max}}\ \ge\ \frac2m .$$
Then under the randomised count restriction (uniform arrangement, uniform cube) and for every table $x$,
$$\Pr[g\text{ splits the cube}]\ \le\ \frac{8C_{KR}(2kW+1)}{m}\Big(\frac{2\sqrt{\ln m}}{\delta}+\sqrt{\frac{k+2\ln m}{\delta}}\Big)+\frac2m
\ =\ O\!\Big(\frac{kW}{m}\big(\tfrac{\sqrt{\ln m}}{\delta}+\sqrt{k/\delta}\big)\Big),$$
where $C_{KR}$ is the Kolmogorov–Rogozin constant. For constant $\delta$ and $W$ this is $\tilde O(k^{3/2}/m)$: coherent up to polylog. The gate behaves like a random walk ($\Theta(\sqrt{k/m})$) only when $\delta\lesssim\sqrt{k\ln m/m}$, i.e. when $|\sum_l\gamma_{i,l}|\lesssim g_{\max}\sqrt{km\ln m}$.

*Proof.* Condition on everything except block $i$: the live bits and fixed parts of the other blocks, and the live bit $\ell$ of block $i$. The gate splits the cube iff the fixed part $\Phi$ of block $i$ lies in a half-open window $J$ of length $R=\sum_{i'}|\lambda_{i'}|\le kg_{\max}$ (`mixed_sign` Lemma 3.1, step 1). By the Beta-integral identity, given $\ell$ the fixed set of block $i$ is a Bernoulli$(q)$ sample of $[m]\setminus\{\ell\}$ with $q\sim U[0,1]$, so $\Phi=\Phi_q=\sum_{l\ne\ell}\gamma_{i,l}\xi_l$ with $\xi_l$ i.i.d. Bernoulli$(q)$. Write $D'=\sum_{l\ne\ell}\gamma_{i,l}$, so $|D'|\ge(\delta m-1)g_{\max}\ge\delta mg_{\max}/2$; WLOG $D'>0$. Let $g=g_{\max}$.

*Anti-concentration.* For each $l$, an interval of length $L=g/(2W)$ contains at most one of the two atoms of $\gamma_{i,l}\xi_l$, so its concentration function at scale $L$ is $\max(q,1-q)$. Kolmogorov–Rogozin gives $Q(\Phi_q;L)\le C_{KR}/\sqrt{(m-1)\min(q,1-q)}$, and $J$ is covered by $\lceil R/L\rceil\le2kW+1$ intervals of length $L$. Hence
$$\Pr[\Phi_q\in J]\ \le\ \frac{A}{\sqrt{\min(q,1-q)}},\qquad A=\frac{(2kW+1)C_{KR}}{\sqrt{m-1}} .$$
*Concentration.* $\mathbb E\Phi_q=qD'$ and $\mathrm{Var}\,\Phi_q\le q(1-q)(m-1)g^2$, with summands bounded by $g$. Bernstein's inequality gives, for $u(q):=2g\sqrt{q(1-q)(m-1)\ln m}+2g\ln m$: if $\mathrm{dist}(qD',J)\ge u(q)$ then $\Pr[\Phi_q\in J]\le2/m$. (If $\mathrm{Var}\ge gu/3$ the exponent is $\ge u^2/(4\mathrm{Var})\ge\ln m$; otherwise it is $\ge3u/(4g)\ge\ln m$.)

*The near set.* Let $Q=\{q:\mathrm{dist}(qD',J)<u(q)\}$. Writing $J=[t,t+R)$ and $q_0=t/D'$, every $q\in Q$ satisfies $|q-q_0|<a+b\sqrt{q(1-q)}$ with
$$a=\frac{R+2g\ln m}{D'}\le\frac{2(k+2\ln m)}{\delta m},\qquad b=\frac{2g\sqrt{(m-1)\ln m}}{D'}\le\frac{4\sqrt{\ln m}}{\delta\sqrt m}.$$
On $[0,\tfrac12]$ substitute $q=r^2$: the condition becomes $|r^2-q_0|<a+br$, which confines $r$ to an interval of length at most $b+2\sqrt a$ (solve the two quadratics; the difference of the roots is $b+\big(\sqrt{b^2+4q_0+4a}-\sqrt{b^2+4q_0-4a}\big)/2\le b+4a/\sqrt{4a}$, and if $q_0\le a$ the lower root is replaced by $0$ and the length is $\le b+\sqrt{2a}$). Therefore $\int_{Q\cap[0,1/2]}dq/\sqrt q=2\int dr\le2(b+2\sqrt a)$, and the same holds on $[\tfrac12,1]$ with $1-q$.

*Integrate.* $\Pr[\text{split}]=\int_0^1\Pr[\Phi_q\in J]\,dq\le\int_Q\frac{A\,dq}{\sqrt{\min(q,1-q)}}+\frac2m\le4A(b+2\sqrt a)+\frac2m$, which is the claim after inserting $a,b,A$ (and $\sqrt{m-1}\ge\sqrt m/\sqrt2$, absorbed in the constant). ∎

**Check** [VERIFIED] (`drift_split.py`, `logs/drift_k{2,3}.log`): gates with a fraction $(1+\delta)/2$ of $+1$ weights and $(1-\delta)/2$ of $-1$ weights per block (relative drift exactly $\delta$), $k=2$, split fraction under a random arrangement, multiplied by $m/k$:

| $m$ | $\delta=1$ | $\delta=1/2$ | $\delta=1/4$ | $\delta=1/8$ | $\delta=1/16$ | $\delta=0$: fraction$/\sqrt{k/m}$ |
|---|---|---|---|---|---|---|
| 32 | 0.98 | 1.90 | 3.17 | 4.73 | 5.23 | 1.35 |
| 128 | 1.00 | 1.92 | 3.69 | 6.74 | 9.16 | 1.38 |
| 512 | 1.00 | 1.94 | 3.87 | 7.04 | 13.05 | 1.42 |

For fixed $\delta$ the normalised split fraction converges to $\approx1/\delta$ (the small-$m$ values are capped by the balanced rate $\sqrt{k/m}$), so the true behaviour is $\Theta(k/(\delta m))$ with constant about 1; Lemma 4.1 proves this up to the factor $\sqrt{\ln m}+\sqrt{k\delta}$. The $\delta=0$ column is the barrier rate, $\approx1.4\sqrt{k/m}$ at the median threshold. At $k=3$ (`logs/drift_k3.log`) the same pattern holds with the coherent median-threshold value $0.75\,k/m$ as the unit: the normalised fractions at $m=256$ are $0.75,\ 1.50,\ 2.99,\ 5.50,\ 9.13$ for $\delta=1,\tfrac12,\tfrac14,\tfrac18,\tfrac1{16}$, i.e. $\approx0.75/\delta$ once $m\gg k/\delta^2$.

### 4.1 Consequence: sub-quadratic circuits are made of zero-sum gates [PROVED]

Combine Theorem 2.1 (demand $D_0\approx N/(3k)$ per cube), Lemma B1 (coherent gates: $\le k/m$), Lemma 3.1 of `mixed_sign` (any gate: $\le k/m+C_1k^{3/2}/\sqrt m$) and Lemma 4.1.

**Theorem 4.2.** Fix $W\ge1$. Call a gate *$(\delta,W)$-drifting* if some block of it has all weights of magnitude in $[g_{\max}/W,g_{\max}]$ and relative drift $\ge\delta$; call it *balanced* otherwise (every bounded-range block has $|\sum_l\gamma_{i,l}|<\delta mg_{\max}$). Let $C$ compute $A_{k,m}$ in the balanced regime with $S\le N^{2-\varepsilon}$ gates, $\varepsilon>0$ fixed, $n$ large. Then for $\delta_0=N^{-\varepsilon}\cdot k^{O(1)}W\sqrt{\ln m}$, at least
$$\Omega\Big(\frac{N\sqrt m}{k^{5/2}}\Big)=\tilde\Omega(n^{3/2})$$
gates are **balanced at level $\delta_0$**: in each of their bounded-range blocks, $|\sum_l\gamma_{i,l}|\le\delta_0\,m\,g_{\max}=N^{-\varepsilon+o(1)}\,m\,g_{\max}$. For $S=\tilde O(N^{3/2})$ this says $|\sum_l\gamma_{i,l}|\le\tilde O(\sqrt m)\,g_{\max}$: the hard gates are balanced to within the random-walk scale in every bounded-range block.

*Proof.* Theorem 2.1 averaged over the randomised restriction gives $\sum_j p_j\ge D_0\ge N/(3k)$ with $p_j$ the split probability of gate $j$. Gates that are coherent or $(\delta_0,W)$-drifting have $p_j\le C'k^{3/2}W\sqrt{\ln m}/(\delta_0m)+2/m$ by B1 and Lemma 4.1 (since $\delta_0\le1$, the term $\sqrt{(k+2\ln m)/\delta_0}$ is at most $\sqrt{k+2}\cdot\sqrt{\ln m}/\delta_0$). We may assume $\varepsilon\le1/2$, since $S\ge n^{3/2}/\mathrm{polylog}$ for every circuit; then $\delta_0\ge2/m$ as Lemma 4.1 requires. With $\delta_0=6C'k^{5/2}W\sqrt{\ln m}\,S/(Nm)=N^{-\varepsilon}k^{O(1)}W\sqrt{\ln m}$ (which is $\le1$ for $S\le N^{2-\varepsilon}$) their total contribution is at most $S\cdot C'k^{3/2}W\sqrt{\ln m}/(\delta_0m)+2S/m=N/(6k)+2kN^{1-\varepsilon}\le D_0/2\,(1+o(1))$. The remaining gates are balanced at level $\delta_0$ and each contributes at most $k/m+C_1k^{3/2}/\sqrt m\le2C_1k^{3/2}/\sqrt m$, so there are at least $(D_0/2)\sqrt m/(2C_1k^{3/2})=\Omega(N\sqrt m/k^{5/2})$ of them. ∎

**Reading.** T2 asked whether "mixed gates split few cubes in an effective sense". The honest answer is: *most* mixed gates do — any gate whose blocks have a definite sign bias, however many minority weights it has, is as harmless as a coherent gate up to polylog. The exception is exactly the class the barrier is built from: gates whose signed block sums vanish to within $\sqrt m$ (relative drift $N^{-1/2+o(1)}$). A proof of $n^{2-o(1)}$ therefore needs to handle only *balanced* address parts, and it needs a non-additive argument to do so (§3). Gates with unbounded dynamic range inside a block are not covered by Lemma 4.1; Lemma 3.1 caps them at the $\sqrt m$ rate, and the rank trick of its proof should extend the drift lemma to them, but this is not done here.

---

## 5. Can mixed signs save a polynomial factor? Assessment of (R)

### 5.1 Fixed $k$: equivalent to sublinear depth-two parity [PROVED, known]
`mixed_sign` Cor. 1.5 and Prop. 1.1 above: $\mathrm{size}(A_{k,m})\ge\mathrm{par}(km+1)$, coherent circuits need $\Theta(m)$ at fixed $k$, so a polynomial saving at fixed $k$ is exactly a sublinear depth-two parity circuit. Known bounds on $\mathrm{par}(M)$: $\Omega(\sqrt M)\le\mathrm{par}(M)\le\lfloor M/2\rfloor$, with equality on the right for $M\le9$. No asymptotic refutation is available at fixed $k$ without solving that problem.

### 5.2 Balanced case: no reduction in either direction, by restrictions [PROVED]
* From Andreev to parity: §1.2. A sub-quadratic Andreev circuit restricts to a parity circuit on $N+1$ bits with $S\gg N$ gates, which says nothing.
* From parity to Andreev: every restriction of an Andreev circuit that isolates one block (fix the table to a parity table and all other blocks to constants) is a parity circuit on $m+1$ bits with at most $S$ gates, hence gives only $\mathrm{size}(A_{k,m})\ge\mathrm{par}(m+1)$. The quadratic bound would need $\mathrm{size}(A_{k,m})\gtrsim N\cdot\mathrm{par}(m)$, a **direct-sum theorem** across the $N$ characters. For depth-two threshold circuits with a shared bottom layer no such theorem is known, and the coherent proof is itself a direct-sum argument that works only because the per-gate supply bound $k/m$ is additive. [CONJECTURE] $\mathrm{size}(A_{k,m})\ge N\,\mathrm{par}(m)/\mathrm{polylog}(n)$; this would make the balanced coherence question equivalent, up to polylogs, to the parity question.

### 5.3 The only known mechanism is sign-blind [PROVED]
All known constructions (Prop. basic, the $5/16$ circuit, the subcube-dominance family, the $k=2$ family) realise, for each character $S$, a function of one integer linear form $L_S$ that is congruent to $t_S$ mod 2 by a **staircase**: $f(L)=f(\ell)+\sum_{\theta=\ell+1}^h(f(\theta)-f(\theta-1))[L\ge\theta]$. The gate count of the staircase is the range $h-\ell$ of the form (or half of it when only every second difference is nonzero).

**Proposition 5.1.** Let $L=\sum_lc_l\,y_l$ be an integer form on $M$ bits with $L\equiv\sum_ly_l\pmod2$ for all $y$ (so every $c_l$ is odd). Then $\mathrm{range}(L)=\sum_l|c_l|\ge M$, and any sum $\sum_jv_j[L\ge\theta_j]+c$ whose sign alternates with the parity of $L$ on all values of $L$ in its range has at least $\lceil\mathrm{range}(L)/2\rceil$ gates.
*Proof.* Each gate changes the sum at one value of $L$; between consecutive changes the sum is constant, so the sign can alternate only at changes; the range contains $\mathrm{range}(L)+1$ consecutive integers. ∎

Hence inside the character-staircase framework mixed address signs can change the constant (via the shape of the form) but never the exponent: the cost is $\sum_S\mathrm{range}(L_S)/2\ge\sum_S|S|m/2=kNm/4=\Theta(n^2)$. The table part of the known circuits costs another $\Theta(N^2)$ (range of $X_S$) and is not addressed by the coherence question at all.

### 5.4 What a polynomial saving would have to look like [PROVED consequences, CONJECTURE on existence]
By Theorems 2.1, 3.1, 4.2 and `mixed_sign` 3.2, a circuit with $S=n^{2-\varepsilon}$ gates must contain $\tilde\Omega(n^{3/2})$ gates that
1. read table bits (pure-address gates are inert, §2),
2. are balanced to relative drift $n^{-\varepsilon+o(1)}$ in every bounded-range block (§4), i.e. are random-walk views of the address blocks,
3. have table parts concentrated at the scale of their live address weights (Theorem 2.1(3)), i.e. few table weights above that scale,
4. and are *useful* on a $\gtrsim n^{\varepsilon}$ times larger fraction of cubes than a coherent gate, under **every** arrangement simultaneously.

Random-walk gates do have the split rate (that is the barrier), but their restrictions to cubes are random-direction threshold functions whose thresholds move with the walks $F_j(c)$ shared across all cubes. Nobody has a mechanism that coordinates them; the search reports (`mixed_upper`, `variants_sol`, `mixed_sign` §4) found none, and pool-LP searches with random mixed features need 4× *more* gates than block-symmetric ones. [CONJECTURE] No mixed-sign family saves a polynomial factor; i.e. $\mathrm{size}(A_{k,m})=n^{2-o(1)}$ in the balanced case.

---

## 6. What a proof beyond $n^{3/2}$ must do, and the smallest honest target

### 6.1 The table-circuit view [PROVED]
Fix an arrangement and a grid point $s\in\{0..m\}^k$ (not just a cube). The circuit, as a function of the table alone, is the depth-two threshold circuit
$$\Phi_s(x)=\sum_jv_j\big[\alpha_j\cdot x\ \ge\ \theta_j-F_j(s)\big]+u\cdot x+C(s),\qquad[\Phi_s\ge0]=x_{s\bmod2}.$$
Its bottom directions $\alpha_j$ and top weights $v_j,u$ are the **same for every $s$**; only the thresholds move, by the walks $F_j$. Along a grid edge $(s,s+e_i)$ the computed dictator changes from $x_b$ to $x_{b\oplus e_i}$, which a change of $C(s)$ alone cannot do (sign argument as in Prop. 1.1), so some threshold must cross a value of its $\alpha_j\cdot x$. Correctness is thus a statement about one *fixed* family of $S$ hyperplanes in table space whose offsets are driven by $S$ coupled walks on the address grid. Theorem 2.1 only uses, for each cube, how many hyperplanes have offsets inside the cube's window; it ignores that the offsets of the *same* hyperplane on different cubes are tied together by the walk, and that the top weights do not change. Any argument that beats $n^{3/2}$ must use one of these two.

### 6.2 One-table-bit circuits: the minimal non-additive problem [PROVED reformulation; OPEN]
Let $\mathcal T_1$ be the class of circuits whose bottom gates read at most one table bit: $g_j=[\alpha_jx_{d_j}+L_j(a)\ge\theta_j]$. The barrier set of Theorem 3.1 lies in $\mathcal T_1$, so **no per-gate argument proves $\mathrm{size}_{\mathcal T_1}(A_{k,m})\ge n^{3/2+\varepsilon}$**, while every known construction uses gates reading all $N$ table bits. In $\mathcal T_1$ the structure is completely explicit:

**Proposition 6.1.** For a $\mathcal T_1$ circuit and every address $a$, each gate is, as a function of $x$, one of $0,1,x_{d_j},1-x_{d_j}$, so $\Phi_a(x)=\sum_dw_d(a)x_d+c(a)$ is **affine in $x$**, with
$$w_d(a)=u_d+\sum_{j:\,d_j=d,\ j\text{ active at }a}\pm v_j ,$$
where "active at $a$" means $\theta_j-L_j(a)\in(\min(0,\alpha_j),\max(0,\alpha_j)]$. Correctness is equivalent to the **dominance condition**
$$w_{b(a)}(a)\ >\ \sum_{d\ne b(a)}|w_d(a)|\qquad\text{for every }a\in\{0,1\}^{km},$$
together with the matching value of $c(a)$.
*Proof.* An affine threshold $[w\cdot x+c\ge0]$ equals the dictator $x_b$ iff $c+\sum_{d\ne b}w_d^+<0\le c+w_b+\sum_{d\ne b}w_d^-$, which implies $w_b>\sum_{d\ne b}|w_d|$; conversely if the dominance holds, $c$ can be chosen. ∎

So in $\mathcal T_1$ the problem is: $N$ families of "window gates" $[L_j(a)\in W_j]$ (differences of two parallel hyperplanes), family $d$ reading $x_d$, with signed weights, such that the family of the parity vector $b(a)$ dominates the $\ell_1$ mass of all other families at **every** address. Equivalently each family $d$ must weakly compute the $k$-fold parity indicator $[b(a)=d]$ (large exactly on its own parity class, small elsewhere, in the $\ell_1$-dominance sense). The per-gate count gives $S\ge N\sqrt{km}/O(1)$ here as well (a hyperplane cuts an $O(1/\sqrt{km})$ fraction of the edges of $\{0,1\}^{km}$, O'Neil, and cannot concentrate its cuts on one parity class by more than a constant factor); the dominance condition is the extra, non-additive constraint. [OPEN] Prove $\mathrm{size}_{\mathcal T_1}(A_{k,m})\ge n^{3/2+\varepsilon}$. This is the smallest setting in which the coherence question is non-trivial and the only obstacle is the coordination of balanced gates; a solution would almost certainly extend, since gates reading $t$ table bits have $x$-parts that are $t$-variable threshold functions and the dominance condition generalises to "the restriction to the $2^t$ sub-tables is a dictator".

### 6.3 Why the exact model does not help [PROVED remark]
In the exact-sum model symmetrisation over within-block permutations is legitimate and turns each gate into a smooth function $\hat g_j(x,s)$ of the block counts. The parity signal of a balanced $\pm1$ gate after symmetrisation is $\Theta(1/\sqrt s)$ (`maj_sol` §3: $q(0)=1,q(1)=\tfrac12$, and in general $\Pr[\text{hypergeometric sum}=0]$), so along a line of the grid the alternating sum $\sum_s(-1)^{s}\hat g_j(x,s)$ is $O(\sqrt m)$ per gate while the target needs $\Theta(m)$. This yields $\sum_j|v_j|\ge\Omega(\sqrt m)$, a weight bound, and nothing about $S$; with bounded top weights it gives only $S\ge\Omega(\sqrt m)$. The exact model therefore faces the same barrier.

---

## 7. Verdict

**T1 (coherence normal form with polylog or $S^{c}$, $c<4/3$, loss).**
* As a syntactic transformation: at least as hard as $\mathrm{par}(M)\ge M/\mathrm{polylog}$ [PROVED, §1.2], which is open; so not available.
* As a statement about circuits computing Andreev: not implied by, and not implying, any parity bound [PROVED, §1.2, §5.2]. It is equivalent to the goal itself. All evidence (exact minima, Prop. 5.1, the failure of every search for mixed constructions) is consistent with it. [CONJECTURE] T1 is true in the weak form "$\mathrm{size}(A_{k,m})=n^{2-o(1)}$", but no known technique proves it, and §3 shows that none of the per-gate techniques can.

**T2 (structural statement sufficient for the counting proof).**
* Every version in which the demand is Theorem A's (or its information refinement, Theorem 2.1) and the supply is accounted per gate — with any potential bounded by $O(k)\times$ the split indicator, under any arrangement chosen as a function of the circuit, or any mixture of arrangements — is **capped at $O(n^{3/2}\log n)$** [PROVED, Theorem 3.1]. This includes "most gates can be made coherent", "re-choose the order per gate group", and "charge mixed gates differently". The brief's suggestion to use the table does enter (pure-address gates are inert, table-heavy gates are rarely active, Theorem 2.1), but the barrier gates read one table bit and defeat the refined count as well.
* What *is* true and new: in any circuit with $n^{2-\varepsilon}$ gates, $\tilde\Omega(n^{3/2})$ gates must be **balanced** — signed block sums of relative size $n^{-\varepsilon+o(1)}$ in every bounded-range block [PROVED, Theorem 4.2 via the Drift Lemma 4.1, VERIFIED numerically]. Gates with any definite sign bias are as harmless as coherent gates up to polylog, whatever their minority count. So "essentially sign-coherent" fails as a *necessary* structure only through zero-sum gates, and the whole $n^{3/2}$ versus $n^2$ question is the question whether $\tilde\Theta(n^{3/2})$ zero-sum gates can be coordinated.

**(R) (asymptotic refutation).** Not found, and not expected: at fixed $k$ it is equivalent to sublinear depth-two parity [known]; in the balanced case the only known mechanism is sign-blind [PROVED, Prop. 5.1] and a mixed family would need the four properties of §5.4. No formal reduction links the balanced case to parity in either direction [PROVED, §5.2]; a direct-sum theorem $\mathrm{size}(A_{k,m})\gtrsim N\cdot\mathrm{par}(m)$ would, and is the natural conjecture.

**Where to push.** The smallest honest target is $\mathrm{size}_{\mathcal T_1}(A_{k,m})\ge n^{3/2+\varepsilon}$ for circuits whose gates read one table bit (§6.2): there the table dependence is affine, correctness is the explicit $\ell_1$-dominance condition of Prop. 6.1, the barrier gates live in the class, and the only missing ingredient is a non-additive argument about $N$ families of window gates each of which must weakly compute a $k$-fold parity indicator. A proof there would be the first use of the top gate's fixed weights across cubes, which §6.1 shows is unavoidable.

## 8. Files

| file | content |
|---|---|
| `report.md` | this report |
| `barrier_const.py`, `logs/barrier_const.log` | exact informative probability of the barrier gate (Lemma 3.0), min over cubes and cube average |
| `adaptive_arr.py`, `logs/adaptive_k2.log`, `logs/adaptive_k3.log` | demand met by random gate sets under identity / random / locally optimised arrangements (Theorem 3.1 check) |
| `defect_split.py`, `logs/defect_k{2,3,4}.log` | split fraction of coherent, $\sqrt m$-defect and balanced gates versus $m$ |
| `drift_split.py`, `logs/drift_k{2,3}.log` | split fraction of gates with relative drift $\delta$ (Drift Lemma 4.1 check) |
| `pydeps_local/` | local numpy/scipy/ortools/pysat install (the compiled extensions in `/tmp/pydeps` are missing) |

No process started by earlier sessions was touched; nothing was posted online.
