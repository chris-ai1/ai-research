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

**(d) Weight-bounded mixed gates.** These are covered by §3, where the bound holds for arbitrary weights. The barrier of `push_lower` (Prop. F) shows that it cannot be improved for $\pm1$ gates by survival arguments: they survive every one-live-bit restriction with probability $\ge1/(2\sqrt{2km})$. So bounded weights earn no better coefficient than arbitrary mixed gates, up to a factor $O(k)$ (§3).

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
