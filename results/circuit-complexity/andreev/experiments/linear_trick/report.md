# Free-linear-term ("parity trick") redesign of the depth-2 circuit for Andreev's function

Setting and notation as in the task: $N=2^k$, $n=N+km$, $s_i=|a_i|$, $b_i=s_i \bmod 2$, $t_S=\sum_{i\in S}s_i$ ($T_S=|S|m$),
$Y_S=\#\{c\ne0: x_c=1,\ S\cdot c \text{ odd}\}\in[0,N/2]$, $|x'|=\sum_{c\neq 0}x_c$, $\sigma=\sum_i s_i$, $e_S=t_S \bmod 2$.
The top gate sees all inputs linearly, so every linear form in the inputs is free.

## Main result: construction (d), $N^2/2+\tfrac34 kmN+O(N+km)$ gates, which is $\tfrac{5}{16}n^2$ in the balanced case

### The two new ingredients

**1. Polarization with a half-staircase.** For integers $Y\ge0$ and $t\ge0$, with $e=t\bmod 2$:

$$Y e \;=\; 2Y\lceil t/2\rceil - Yt \;=\; \Big\lceil\tfrac{2Y+t}{2}\Big\rceil^{2} - Y^2 - \lceil t/2\rceil^2 - Yt .$$

This works because $\lceil (2Y+t)/2\rceil = Y+\lceil t/2\rceil$. So

$$4Y(-1)^t = 4Y - 8\Big\lceil\tfrac{2Y+t}{2}\Big\rceil^{2} + 8Y^2 + 8\lceil t/2\rceil^2 + 8Yt .$$

The univariate functions here are $u\mapsto\lceil u/2\rceil^2$ on $u=2Y+t$ and $t\mapsto\lceil t/2\rceil^2$ on $t$. Their discrete derivative is **zero at every even threshold**, so each staircase needs only the odd thresholds: half the range. This is the "mostly constant steps" property the task asked for. Here the constant is 0 at every second step, rather than $\lambda$ for a linear part.

**2. Quadratic residues collapse across $S$.** The leftover terms $Y_S^2$ and $Y_St_S$ are quadratic polynomials in linear forms, so after summing over $S$ they become a few univariate staircases (the $t_S^2$ part of $\lceil t_S/2\rceil^2$ collapses the same way, but the $\lceil t_S/2\rceil^2$ staircase still has to be built; see the gate list):

$$\sum_{S\ne\emptyset}Y_S^2=\tfrac N4\left(|x'|^2+|x'|\right),\qquad
\sum_{S\ne\emptyset}Y_St_S=\tfrac N4|x'|\sigma+\tfrac N4\sum_i x_{e_i}s_i ,$$

$$\sum_{S\neq\emptyset} t_S^2 = \tfrac N4\left(\sigma^2+\textstyle\sum_i s_i^2\right) .$$

Then $|x'|^2$ is one staircase ($N-1$ gates) and $|x'|\sigma=\tfrac14\big[(|x'|+\sigma)^2-(|x'|-\sigma)^2\big]$ is two staircases of range $N+km$. Each product $x_{e_i}s_i$ uses $m$ gated gates $[s_i+Bx_{e_i}\ge l+B]$. In total this is $O(N+km)$ gates, compared with $\Theta(kmN)$ for the $\varphi(t_S)$ staircases they replace.

**3. Gated parity for the $b=0$ override.** This idea comes from construction (c) below. In (b), the override $-2N^2x_0[b=0]=-2Nx_0\sum_S\chi_S(b)$ cost $T_S+2$ gates per $S$. Using $(-1)^{t}=1-2t+4\lfloor t/2\rfloor$:

$$x_0(-1)^{t_S}=x_0-2x_0t_S+4\sum_{j\ge1}\,[\,t_S+Bx_0\ge 2j+B\,],\qquad B>km .$$

The gate $[t_S+Bx_0\ge 2j+B]$ equals $x_0\wedge[t_S\ge 2j]$. The leftover $x_0t_S$ terms sum to $\tfrac N2 x_0\sigma$, which is one gated staircase of $km$ gates. The override therefore costs $\lfloor T_S/2\rfloor$ per $S$.

### The circuit
The top-gate sum is

$$P = N+\sum_{S\ne\emptyset}4Y_S(-1)^{t_S}\;-\;2N^2x_0[b=0]
     \;=\; N-2Nx_b+[b=0]\big(2N|x|-2N^2x_0\big),$$

with output $x_b=[P<0]$. The margin is $|P|\ge N$: for $b\neq0$, $P=\pm N$. For $b=0$, $P=N+2N|x|$ when $x_0=0$ and $P\le -N$ when $x_0=1$. The gates are:

| part | linear form | thresholds | count |
|---|---|---|---|
| main ridge, each $S\ne\emptyset$: $-8\lceil u/2\rceil^2$ | $u=2Y_S+t_S\in[0,N+T_S]$ | odd $\theta$ only | $N/2+\lceil T_S/2\rceil$ |
| residue, each $S$: $+8\lceil t/2\rceil^2$ | $t_S\in[0,T_S]$ | odd $\theta$ only | $\lceil T_S/2\rceil$ |
| override, each $S$: $-8N\,x_0[t_S\ge 2j]$ | $t_S+Bx_0$ | $2j+B$ | $\lfloor T_S/2\rfloor$ |
| $2N(\lvert x'\rvert^2+\lvert x'\rvert)$ | $\lvert x'\rvert$ | all | $N-1$ |
| $2N\lvert x'\rvert\sigma$ | $\lvert x'\rvert\pm\sigma$ | all | $2(N-1+km)$ |
| $2N\sum_i x_{e_i}s_i$, $2N^2x_0\sigma$ | gated | all | $2km$ |

Here $B=N+km+2$. The remaining terms are free linear terms: $2N|x'|$ and $-2N^2x_0$.

**Exact gate count:**

$$G_d(k,m)=\sum_{\emptyset\ne S\subseteq[k]}\Big(\tfrac N2+2\big\lceil\tfrac{|S|m}{2}\big\rceil+\big\lfloor\tfrac{|S|m}{2}\big\rfloor\Big)+3(N-1)+4km
\;=\;\tfrac{N^2}{2}+\tfrac34kmN+O(N+km).$$

The script's gate count matches this formula in every case run.

**Balanced case** ($km=N$, so $n=2N$): $G_d=\tfrac54N^2+O(N)=\tfrac{5}{16}n^2\approx0.3125\,n^2$. This compares with $\tfrac58 n^2$ for (b) and $\tfrac34 n^2$ for (a). For a general split the count is $\tfrac34 nN-\tfrac14N^2$.

**Weights** (all integers): bottom weights are in $\{0,1,2\}$ plus one gating weight $B=N+km+2$. Top coefficients are at most $O(N(N+km))$; for example, $k=7,m=3$ has a maximum top coefficient of 65024. The threshold is 0, with integer slack $N$.

### Verification (`constr_d.py`, `verify_d_big.py`, `exact_check.py`)
- **Exhaustive** over all $2^n$ inputs for $(k,m)\in\{(1,1),(1,2),(1,3),(1,5),(2,1),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3)\}$, up to $n=17$: correct, margin exactly $N$.
- **Sampled with adversarial families** for $(4,1),(3,4),(4,3),(4,4),(5,3),(5,5),(6,3)$ with 40k inputs each, and for $(4,6),(4,8),(5,4),(5,6),(6,4),(6,6),(7,3)$ with 2×60k inputs each. The adversarial families are: forced $b=0$ (all-zero and random even weights), all-ones and all-zeros tables, single-1 and single-0 tables, all blocks of weight $m$, block weights in $\{0,1,m-1,m\}$, plus random. All correct.
- **Exact algebraic check** (`exact_check.py`): for $(k,m)\in\{(1,4),(2,3),(3,3),(4,4),(5,5),(6,3),(6,5)\}$, 30k inputs each, about 25% forced to $b=0$ and about 25% forced to $|b|=1$. The circuit's top sum equals the closed form $N-2Nx_b+[b=0](2N|x|-2N^2x_0)$ **exactly** at every input. That closed form implies correctness for all inputs.

| (k,m) | n | (b) 5/8 | (c) 9/16 | **(d) 5/16** |
|---|---|---|---|---|
| (3,3) | 17 | 179 | 149 | 141 |
| (4,4) | 32 | 655 | 568 | 421 |
| (5,5) | 57 | 2255 | 1997 | 1297 |
| (6,6) | 100 | – | – | 4077 |
| (7,3) | 149 | – | – | 10641 |

For tiny instances, (d) is worse than (b) because of its $O(N+km)$ overhead. For example, $(2,1)$ needs 30 gates against 31, and $(1,m)$ needs about $1.5m+O(1)$ against an exact optimum of $\lceil m/2\rceil$. The asymptotic gain shows up from about $k\ge3$.

## Intermediate construction (c): $\tfrac{9}{16}n^2$ (`constr_c.py`)
This is (b) with only the override replaced by the gated parity trick. It needs $N(N-1)+\sum_S(2T_S+\lfloor T_S/2\rfloor)+\lceil km/2\rceil$ gates, which is $N^2+\tfrac54kmN$, or $\tfrac{9}{16}n^2$ balanced. It is verified the same way, including the exact closed-form check.

## What did not work, and why
1. **A single $\lambda$ on the φ-staircases.** The steps $(-1)^\theta(2\theta-1)$ are pairwise distinct, so this saves at most one gate.
2. **Redesigning the univariate function on a single direction $2Y+t$** (floor or mod variants, $\varphi(u)-u$, $\lfloor u/2\rfloor(u\bmod 2)$, and so on). A mixed-difference analysis shows the following. Along a direction $(2,\pm1)$ the required mixed difference $-2(-1)^t$ is constant on each line. The gate coefficients along each parity chain must therefore *drift* (grow linearly), so every step is distinct. With one direction, the only freedom is $g=\varphi/2+\text{affine}+\gamma(u\bmod2)$, which always leaves the residue $\varphi(t)/2$. With the pair $(2,1),(2,-1)$, the cheapest options either keep the $\varphi(t)$ residue or trade it for a $-2Y^2$ residue. The way out was to allow **quadratic residues**, which collapse across $S$. The mixed-difference constraint then gains a free constant, and half the chains no longer need any gates.
3. **The two-ridge polarization** $(Y+\lceil t/2\rceil)^2-(Y-\lceil t/2\rceil)^2$ has no residue but costs $2R+T$, which is $N+T$ per $S$. This is worse than $N/2+T$ (one ridge plus the $\lceil t/2\rceil^2$ residue).
4. **Removing the $\lceil t_S/2\rceil^2$ residue**, about $kmN/4$ in total. Its non-collapsible part is $\sum_S t_Se_S=\tfrac12(\sum t_S-F)$, where $F=\sum_S\varphi(t_S)=\tfrac N2\sum_i\varphi(s_i)[b_{-i}=0]$ is needed exactly at $b=e_i$.
   - Mixing $\lceil\cdot\rceil$ and $\lfloor\cdot\rfloor$ versions per $S$, or using other odd coefficients in $t'_S\equiv t_S \pmod 2$, only moves the residue. With signs $\varepsilon_S=\chi_S(c)$ it lands on $\{c\}\cup\{c+e_i\}$. More generally, Parseval forces $\sum_{b\ne0}A_i(b)^2\ge N^2/4$, which is far too large to hide below the margin when $km>\sqrt N$.
   - Overriding the $k$ addresses $e_i$ costs about $kmN/4$ each.
5. **Merging the override into the main ridge**, as in $(Y+Kx_0+\lceil t/2\rceil)^2$ or a second ridge $(-Kx_0+\lceil t/2\rceil)^2$. The override needs $K\approx N/2$ because the $b=0$ defect is as large as $2N|x'|$. The cost becomes $N+T$ per $S$, which beats $N/2+\tfrac32T$ only when $T_S>N$; that never happens, since $T_S\le km=N$.
   - Shrinking the defect by shifting $A_S=Y_S+\nu(x)$ needs $\nu=-|x|/2$, which is not integral. Integral versions keep a defect of order $N^2$, so the override must still recognise $b=0$ against everything else with ratio about $2N$, which needs (essentially) every character $\chi_S$. A low-degree override does not work.
6. **Shrinking the $Y$-range part** ($N/2$ per $S$). Any substitute $A_S=Y_S+L$ must use the same linear $L$ for every $S$, otherwise $\sum_S(A_S-Y_S)e_S$ does not collapse. Averaging over $S$ gives $\sum_S\operatorname{range}(A_S)\ge (N-1)^2/2$, so $N^2/2$ is optimal *within this family*.
   - Using the ridge $Y+t$, or $4Y+t$ with residues mod 4, brings in parities of $Y_S$ (characters in $x$) or doubles the $Y$-range.
7. **Bit-decomposition of $Y$ with progression sums** $\sum_i[Y+2^jt\ge\theta_0+2^{j+1}i]$. Each progression yields $e\cdot\text{bit}_j(Y)$ at cost $R/2^{j+1}+T/2$, so the total is $2R+\tfrac T2\log_2R$. This is worse for large $k$.
8. **Sign-only slack** (direction 2 of the task) is used only at $b=0$, as in (b). At $b\neq0$, every per-$S$ error adds up over $N-1$ sets against a margin of $N$, so the gadgets must be essentially exact. The $k=1$ optimum of $\lceil m/2\rceil$ exploits sign slack with a single $S$, and I found no way to carry that over.
9. **Exact 2-D MILPs** for $f=Y(-1)^t$ mod affine (`g2d.py`, `g2d_sat.py`, with directions $|a|,|b|\le2$). They give $(R,T)=(3,3)\to6$ (optimal), $(2,4)\to6$, $(1,4)\to4$, $(2,2)\to3$, compared with $2R+2T$ for the φ-gadget. These hinted that cheaper gadgets exist, but the solvers stall from $4\times4$ onward ($\le12$, lower bound 8). The reweighted-$L_1$ upper bounds (`rwl1.py`) on larger grids are noisy and inconclusive. The useful gain came from collapsing quadratic residues *across* $S$, which a single 2-D gadget does not capture.

## Remaining cost breakdown of (d), balanced, in units of $N^2$
- $Y$-range of the main ridge: 0.5
- $t$-range of the main ridge: 0.25
- $\lceil t/2\rceil^2$ residue: 0.25
- gated override: 0.25

Each of the three $t$-terms is one "parity-type" staircase of $T_S/2$ gates per character $\chi_S$. A further gain would need two of them to share gates.

Files (all in `/tmp/andreev_gap/linear_trick/`): `common.py` (staircase builder, evaluator, adversarial inputs), `constr_c.py`, `constr_d.py`, `verify_d_big.py`, `exact_check.py`, `g2d.py`, `g2d_sat.py`, `rwl1.py`, `sat_more.log`.
