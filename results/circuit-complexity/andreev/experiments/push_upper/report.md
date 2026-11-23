# Pushing the depth-2 upper bound for Andreev's function: report

Directory: `/tmp/andreev_gap/push_upper/`. Python is run with `python3 -I`; scripts add `/tmp/pydeps` themselves.

Notation follows the task. $N=2^k$, $n=N+km$, $s_i$ is the weight of block $i$, $t_S=\sum_{i\in S}s_i$, $T_S=|S|m$, $e_S=t_S\bmod 2$, $\sigma=\sum_i s_i$, $|x'|=\sum_{c\ne0}x_c$, $Y_S=\#\{c\ne0:x_c=1,\ S\cdot c\text{ odd}\}$, and $E=\sum_i x_{e_i}$. The output is $[P<0]$, where $P$ is the top sum.

## 0. Bottom line

1. **The leading constant $\tfrac{5}{16}$ was not improved.** Every idea in the brief was implemented or tested with exact MILPs on small instances. The per-character, linear-in-$x$ family that all known constructions belong to has three $t$-items, each costing $\approx kmN/4$, and a $Y$-part of $N^2/2$. I show (§3) that inside this family each item is forced up to lower-order terms, and that every trade-off between items is linear with exchange rate $N/2:T_S/2$, which never pays when $T_S\le N$.
2. **Best construction: (d''), a second-order improvement.** It is fully verified (§1).
   - It has **no residue staircases at all.** The residue's garbage lives only at the weight-1 addresses $e_i$, where it equals $-Ns_i$. It is centred by a **free address function** and absorbed by a cheap **amplification of $x_{e_i}$** inside the main ridges.
   - It also contains the two exact savings of (d'): one staircase on $u=2|x'|+\dots$ replaces the three staircases $|x'|^2$, $(|x'|\pm\sigma)^2$, and duplicate gates are merged.
   - Its size is
   $$G_{d''}=\tfrac{N^2}{2}+\tfrac34kmN-\begin{cases}\tfrac12kN& m\text{ even}\\ \tfrac14kN& m\text{ odd}\end{cases}+O(N+km),$$
   so in the balanced case it is still $\tfrac5{16}n^2$, now minus $\Theta(n\log n)$.

   | (k,m) | n | (d) | (d') | **(d'')** |
   |---|---|---|---|---|
   | (5,4) | 52 | 1149 | 1098 | **1038** |
   | (6,4) | 88 | 3453 | 3366 | **3182** |
   | (6,6) | 100 | 4077 | 3978 | **3812** |
   | (7,3) | 149 | 10641 | 10493 | **10262** |
   | (8,1) | 264 | 35037 | 34774 | **34138** |
3. **Side results** (explicit and verified):
   - **$k=1$.** A closed-form circuit with $\lceil m/2\rceil$ gates, which equals the SMT optimum.
   - **Block size $m\le2$.** A circuit (d2) with $\tfrac{N^2}{2}+\tfrac14kmN+O(N)$ gates, without both the residue and the per-character override. The zero test uses the "corner trick", $2^k$ gates instead of $kN/2$.

   These show that the residue and override costs come entirely from large block size, which in the balanced case is $m=N/k$.
4. **New, reusable facts** (all checked by computer):
   - **L1, free address functions.** Any $x$-independent $f(b)$ can be added to $P$ at zero gate cost, by shifting the coefficients of odd-threshold staircases that already exist (main ridges or residues).
   - **L4, amplification at weight-1 addresses.** Adding $\alpha x_{e_i}$ to $Y_S$ for $S\ni i$ costs $\alpha|S|$ gates per $S$. It multiplies the $x_{e_i}$-coefficient at $b=e_i$ by $1+\alpha$ and creates garbage elsewhere only at $b=0$.
   - **The $m=2$ zero test** is $[b=0]=\sum_{\varepsilon\in\{\pm1\}^k}[\varepsilon\cdot(s-\mathbf1)\ge k]$.

## 1. Best construction (d'') — `constr3.py`

**Parameters.** $\alpha=\lfloor(m-1)/2\rfloor$ and $c'=$ the largest odd number $\le m$. The gating weight is $B=N+km+2$, and $\kappa_S=-4c'(k-2|S|)$.

**Main ridges**, one per $S\ne\emptyset$. The table form is $W_S=Y_S+\alpha\sum_{i\in S}x_{e_i}$, with range $[0,N/2+\alpha|S|]$. The staircase is
$$-8\lceil u/2\rceil^2+\kappa_S\lceil u/2\rceil,\qquad u=2W_S+t_S,$$
which uses only the odd thresholds $\theta\le N+2\alpha|S|+T_S$, with coefficients $-8\theta+\kappa_S$. Gates whose coefficient is 0 are dropped. The $\kappa_S$-part adds $\kappa_SW_S+\kappa_St_S/2+\kappa_S/4-(\kappa_S/4)(-1)^{t_S}$. The first three terms are removed by direct input weights and the constant. Summed over $S$, the last term is the free address function $f(b)=Nc'\sum_i[b=e_i]$ minus its mean $c'k$, which is added back in the constant (L1).

**Why it is correct.** The identity $W e=\lceil(2W+t)/2\rceil^2-W^2-\lceil t/2\rceil^2-Wt$ gives
$$\textstyle\sum_S4W_S(-1)^{t_S}=\sum_S\big[4W_S-8\lceil u_S/2\rceil^2+8W_S^2+8W_St_S+8\lceil t_S/2\rceil^2\big].$$
- **Residue term (L2).** $\sum_S8\lceil t_S/2\rceil^2=\tfrac N2(\sigma^2+\sum_is_i^2)+N\sigma[b\ne0]+N\sum_is_i[b=e_i]+N[b\ne0]$. I **compute only** $\tfrac N2(\sigma^2+\sum s_i^2)+N\sigma+N$; the address-dependent part is left as an error.
- **Collapsed quadratics.**
$$\textstyle 8\sum W_S^2+8\sum W_St_S=\tfrac N2\big(w^2-\sigma^2\big)+2N|x'|+(4\alpha+2\alpha^2)NE+(2+2\alpha)N\sum_ix_{e_i}s_i,\qquad w=2|x'|+2\alpha E+\sigma .$$
  The $\pm\tfrac N2\sigma^2$ terms cancel.
- **Main sum (L4).** $\sum_S4W_S(-1)^{t_S}=2N[b=0]|x'|-2N[b\ne0]x_b+2\alpha N\sum_ix_{e_i}([b=0]-[b=e_i])$.
- **Override.** $-C\,x_0[b=0]$ with $C=2N^2+2\alpha Nk+Nkm+2N$, built as in (d) from $x_0$-gated even thresholds plus $C\,x_0\sigma$.

**Closed form of the top sum** (proved by the identities above, and checked to equal the built circuit's $P$ at every tested input):
$$P=\begin{cases}N+2N|x'|+2\alpha NE+N(\sigma+1)-C\,x_0 & b=0\\[2pt] N(1+c')-2N(1+\alpha)\,x_{e_i}-N s_i & b=e_i\\[2pt] N-2Nx_b & \text{otherwise.}\end{cases}$$
At $b=e_i$, $s_i$ is odd and lies in $[1,c']$. So $x_{e_i}=0$ gives $P\ge N$, and $x_{e_i}=1$ gives $P\le N(1+c')-2N(1+\alpha)-N\le-N$, because $2+2\alpha\ge c'+1$. Hence **$|P|\ge N$ always.**

**Gate list:**

| part | count |
|---|---|
| ridges | $\sum_S\#\{\theta\text{ odd}\le N+2\alpha|S|+T_S:\ 8\theta\ne\kappa_S\}$ |
| override | $\sum_S\lfloor T_S/2\rfloor$ |
| $w^2$ | $2(N-1)+2\alpha k+km$ |
| $\sum_is_i^2$ | $km$ |
| $x_{e_i}s_i$ (gated) | $km$ |
| $x_0\sigma$ (gated) | $km$ |
| duplicates (the $x_0\sigma$ gates with even $l$ equal the $S=[k]$ override gates) | $-\lfloor km/2\rfloor$ |

**Exact count:**
$$G_{d''}(k,m)=\sum_{S\neq\emptyset}\Big(\#\{\theta\text{ odd}\in[1,N+2\alpha|S|+T_S]:8\theta\ne\kappa_S\}+\lfloor\tfrac{T_S}{2}\rfloor\Big)+2(N-1)+2\alpha k+3km+\lceil\tfrac{km}{2}\rceil .$$
This equals the built circuit for every $k\ge3$ tested; for $k\le2$ a few more coincidences merge. Asymptotically it is $\tfrac{N^2}{2}+\tfrac{\alpha kN}{2}+\tfrac{kmN}{2}+O(N+km)$, which is the expression in §0.

**Weights.** Bottom weights are in $\{0,1,2,2+2\alpha\}$ plus $B$. Top coefficients are integers bounded by $O(N^2+Nkm)$. All arithmetic is exact int64, with an overflow guard.

**Verification** (`constr3.py exh|adv`, logs `verify_dpp_exh.log` and `verify_dpp_adv.log`). Every case is correct, has $\min|P|=N$, and has **$P$ equal to the closed form at every input**.

| range | instances |
|---|---|
| exhaustive, all $2^n$ inputs, every $(k,m)$ with $n\le20$ | $k=1$, $m=1..18$; $k=2$, $m=1..8$; $k=3$, $m=1..4$; $(4,1)$; 31 pairs |
| adversarial + random | $(4,2),(4,3),(4,4),(4,6),(4,8),(5,3),(5,4),(5,5),(5,6),(6,3),(6,4),(6,5),(6,6),(7,2),(7,3),(8,1)$ |

The adversarial inputs (`circ.adversarial_inputs`) range over every address $b$ (all $b$ if $N\le128$; otherwise $0$, every $e_i$, $N-1$, weight-2 addresses and random ones). Block weights are minimal, maximal, mixed-extreme or random, always with the correct parities. Tables are all-0, all-1, single-1 and single-0 at $\{0,1,N/2,N-1,e_i\}$, densities 0.1/0.5/0.9, and tables with $x_b$ forced and the rest all-0 or all-1. On top of that come 6–12k random inputs, half of them forced to $b=0$ or $b=e_i$.

For small $k$ with large $m$, (d') (`constr2.py`) can be smaller; for example $(4,8)$ needs 629 gates against 634. It is verified in the same way (`verify_dp_exh.log`, `verify_dp_adv.log`). Its count is $\sum_S(\lceil\frac{N+T_S}{2}\rceil+\lceil\frac{T_S}{2}\rceil+\lfloor\frac{T_S}{2}\rfloor)+2(N-1)+3km$.

## 2. Cost breakdown (balanced, in units of $N^2$)

| part | (d) | (d'') |
|---|---|---|
| main ridge, $Y$-range | 0.5 | 0.5 |
| main ridge, $t$-range | 0.25 | 0.25 |
| residue | 0.25 | 0 |
| amplification $\alpha|S|$ | – | 0.25 (precisely $(m-2)kN/4$ or $(m-1)kN/4$) |
| override | 0.25 | 0.25 |
| lower order | $3N+4km$ | $2N+2\alpha k+3.5km$ |

The residue's $kmN/4$ is replaced by $\alpha kN/2\approx(m-1\text{ or }2)kN/4$. The saving, $kN/4$ or $kN/2$, comes from centring the garbage with the free address function, and from the fact that the margin $2N$ already covers one unit of spread.

## 3. What failed and why (with computational evidence)

### 3.1 Killing the residue (idea 1)
* **The garbage cannot be removed, only moved (L3).** With any main-ridge address form $\tau_S\equiv t_S\pmod 2$, the garbage $\sum_S\tau_Se_S$ has Walsh energy $\sum_{b\ne0}\hat h_i(b)^2\ge N^2/4$ for every block $i$. When it is concentrated at $e_i$ it equals $-Ns_i$. Its spread over valid inputs is at least $N(m-1)$ for every choice of odd bit coefficients.
* **Spreading the garbage fails.** A single bit of garbage at an address equals the margin $N$.
* **Absorbing it costs $\ge kmN/4-O(kN)$ for every mechanism I found:**
  - the exact residue: $\sum_S\lceil T_S/2\rceil$;
  - Y-form amplification, as in (d''): $\alpha kN/2$ with $\alpha\approx m/2$;
  - D-form amplification: $\approx(m-3)kN/4$.

  By the triangle inequality, amplifying the $x_{e_i}$-coefficient at $e_i$ by $A$ needs table-form weight at least $A$ summed over the characters, so amplification cannot be cheaper.
* **Tolerance helps only for tiny $m$** (`psi_milp.py`). The garbage needs to be cancelled only to within $\pm1$ margin unit, that is, $\Psi=\sum_is_i[b=e_i]$ to within $\pm1$. The exact MILP gives:
  - $k=2$: $m=3\to3$, $m=4\to4$, $m=5\to\le8$ (lower bound 6), against 7/8/11 for the character count;
  - $k=3$: $m=2\to0$, $m=3\to5$, against 12/20.

  For $m\ge5$, approximation by univariate functions is infeasible: the spread of 4 exceeds the combined tolerance below 2. Polynomial-in-$|b|$ approximations need precision $\approx 1/m=k/N$, hence degree $\gtrsim k^{1.5}$.
* **A 2-D gadget modulo quadratics** (`g2q.py`, exact MILP). This is the minimum number of halfplanes representing $Y(-1)^t+q(Y,t)+a(-1)^t$, with $q$ any quadratic, against $R+T$ for ridge plus residue:

  | (R,T) | (2,2) | (2,4) | (2,6) | (2,8) | (3,3) | (3,4) | (3,6) | (4,4) | (4,6) |
  |---|---|---|---|---|---|---|---|---|---|
  | min (≤: time limit) | 2 | 3 | 5 | ≤7 | 3 | 4 | ≤6 | ≤6 | ≤8 |
  | $R+T$ | 4 | 6 | 8 | 10 | 6 | 7 | 9 | 8 | 10 |

  Every optimum or incumbent is $R+T-2$ or $R+T-3$; at $(2,8)$ that is 7, above $R+T/2=6$. The solutions are a ridge with $c_\theta=\kappa-2\theta$ (one coefficient vanishes), one or two vertical lines, and one boundary line, so these are corner effects. With finitely many parallel families, the cell equations $\sum_Fv_F(t-\alpha_FY)=4(Y+a)$ force affine weights, so a full ridge ($R+T/2$) plus a full vertical family ($T/2$) are needed. Reweighted $L_1$ (`rw2.py`) is far worse than the MILP and was dropped.

### 3.2 Reducing the override (ideas 1, 4)
* **The override must be large.** Take a construction that is linear in $x$, uses range-$N/2$ table forms, and has one override address. Integrality ($M\ge N/2$ for the Fourier coefficient) forces every entry $c\ne0$ into the defect with $|D_c|\ge N/2$. So the defect has range $\ge2N(N-1)$ in margin units, and the gated correction must be $\ge2N^2$.
  - Free address functions (L1) cannot cover an $x$-dependent defect.
  - Y/Z table mixtures change the defect's sign but not its range. Spreading the defect over a subspace $V$ costs $\sqrt{|V|}\,N/2$ per character for ridge shifts, or $|V|\cdot kmN/4$ for gated overrides.
* **Shift merges** ($t_S+2jx_0$ or $2W_S-2jx_0+t_S$) give $4jN$ of override for $j$ gates per $S$. That needs $j\approx N/2$, against $T_S/2$ for the separate gated staircase. It pays only when $T_S>N$, which never happens in the balanced case.
* **The zero-test MILP** (`zt_milp.py`) asks for the fewest halfspaces whose combination is $0$ wherever $b\ne0$ and $>0$ at $b=0$:
  - $k=2$: $m=2\to4$, $m=3\to5$ (both equal to the character count), $m=4\to\le8$ (character count 8, lower bound 6);
  - $k=3$, $m=2\to\le7$ against 12 (corner trick $\le 2^k$);
  - $k=3$, $m=3$: the run timed out with a poor incumbent of 34, against the character count of 16, so this point is inconclusive. Its summary line was lost to a HiGHS log line, and the 34 is the number of solution lines left in `zt_more.log`.

  For $m\ge3$ the even points are no longer corners. Isolating points costs $(m/2+1)^k\gg kmN/4$.
* **Polynomial-in-$|b|$ zero tests** (cheap through gated parities) need precision $1/(2N)$, hence degree $\gtrsim0.35k^{1.5}>k$.

### 3.3 Sharing staircases across characters (idea 2)
* Every linear form with parity $e_S$ has odd coefficients on all $|S|m$ bits of the blocks in $S$, so its range is at least $T_S$. Each character therefore needs its own $t$-range, in every item.
* **Combined ridges.** Lexicographic ridges ($u_S+Ku_{S'}$) cost range × range. Sum ridges give the wrong products $(Y_S+Y_{S'})e_{S\oplus S'}=Y_{S\oplus S'}e_{S\oplus S'}+2n_{11}e_{S\oplus S'}$.
* **Triples $S,S',S\oplus S'$.** Their sum is $(M+n_{ab})[(a,b)\ne0]$, a $k=2$ Andreev function on coset counts. Ridges for it cost more.
* **Complement pairs $S,S^c$.** Since $(-1)^{t_{S^c}}=(-1)^\sigma(-1)^{t_S}$, pairing needs products with the global parity.
* **$Y$-part.** For 0/±1 table forms with defects at a fixed address set $V$, every entry outside $V$ lies in at least $N/2$ characters, so $\sum_S\mathrm{range}\ge(N/2)(N-|V|)$.
* **Fixed table parity.** Any half-range D-form ridge on $D_S+t_S$ inherits the table parity $(-1)^{|x|}$ as a global sign flip.

### 3.4 Sign slack (idea 3)
* At $b\ne0$ the margin is exactly $N$, and one bit of garbage equals it.
* At $e_i$ the garbage is sign-compatible when $x_{e_i}=1$. The case $x_{e_i}=0$ needs an $x$-independent term of size $\approx Ns_i$ at $e_i$, which is the residue or amplification again.
* **The $k=1$ optimum** is $P'=C(x_0+x_1-1)-u+4\sum_{\theta\equiv3\ (4)}[u\ge\theta]$ with $u=2s+x_1-x_0$ and output $[P'>0]$. It has $\lceil m/2\rceil$ gates (`k1_opt.py`, all inputs, $m\le16$). It works because the D-form has range 2 when $N=2$. For larger $N$, $N$ characters are summed, so per-character errors must vanish.
* **Lexicographic top weights** reduce to overrides at more addresses, each costing $kmN/4$.

### 3.5 Small exact optima (idea 5)
`min_circuit.py --show` for $(2,1)$ and $(2,2)$ gives 3-gate circuits with generic weights, for example $[3,-1,-4,16,12,-2]\ge16$. I could not see a pattern that generalises.

### 3.6 Block size $m\le2$: circuit (d2), `constr_m2.py`
For $m\le2$, an odd block weight equals 1, so the garbage at $e_i$ is the constant $-N$. One free address function cancels it, so no residue is needed. The override uses the corner trick: $2^k$ gates for $m=2$, one gate for $m=1$. (d2) costs $\sum_S(N/2+T_S/2)+O(N+km)$. It is exhaustive for $n\le20$ and adversarial up to $(7,2)$ and $(8,1)$: 8958 gates at $(7,2)$ and 33751 at $(8,1)$.

## 4. Lemmas checked by computer (`lemma_check.py`)
* **L1 (free address functions).** Adding $\kappa_S=-4U/N$ to every odd-threshold gate on $t_S$ changes $P$ by $U[b=0]$ plus terms linear in $s$ and a constant; checked on all $s$. In (d'') the same shift is applied to the main ridges, where it also adds the linear term $\kappa_SW_S$.
* **L2.** $\sum_St_Se_S=\tfrac N4\sigma[b\ne0]+\tfrac N4\sum_is_i[b=e_i]$, checked on all $s$.
* **L3 (Parseval).** For integer $h$ with $h(S)$ odd exactly when $i\in S$, $\sum_{b\ne0}\hat h(b)^2=N\sum_S(h(S)-\bar h)^2\ge N^2/4$, because the nearest odd and nearest even integers to any real lie at distances summing to at least 1.
* **L4 (amplification)** and the closed form of (d'') are checked through the $P{=}$closed-form test on all verified inputs.

## 5. Files
- `circ.py`: circuit container, exact evaluation, target, exhaustive and adversarial inputs.
- `constr.py`: (d); `constr2.py`: (d'); **`constr3.py`: (d'')**, with its count formula, closed form and verification driver.
- `constr_m2.py`: (d2) for $m\le2$; `k1_opt.py`: the $k=1$ optimum.
- `verify_dp.py` with `verify_dp_exh.log` and `verify_dp_adv.log`: (d') verification; `verify_dpp_exh.log` (31/31 pairs correct, $P$ equal to the closed form) and `verify_dpp_adv.log`: (d'') verification.
- `g2q.py` (with `g2q_batch.log`), `rw2.py`, `show2d.py`: 2-D gadget searches; `zt_milp.py` (with `zt_k3m2.log` and `zt_more.log`): zero tests; `psi_milp.py` (with `psi_k3.log`): residue tolerance.
- `lemma_check.py`: computer checks of the lemmas.
