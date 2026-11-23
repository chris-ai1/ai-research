# Halfplane gadgets for $y(-1)^t$: report

All scripts are in `/tmp/andreev_gap/work/`. Run them with `python3 -I`; they add `/tmp/pydeps` themselves. Notation: $G=\{0..R\}\times\{0..T\}$, $f(y,t)=y(-1)^t$, and $h(R,T)$ is the minimum number of halfplanes, with arbitrary real weights and a free constant.

## 0. Short answers

1. **I found no explicit family with $2R+T+O(1)$ halfplanes.** For $T>4R+O(1)$ no such family exists: a rigorous strip argument (§3) gives $h(R,T)\ge\lceil 3T/2\rceil$ for $R\ge 3$. The best general construction I have is $2R+2T-2$, a two-gate improvement of the known one (§1A). For $R\le 2$ there are better explicit families: $h(1,T)=T+1$ exactly, and $h(2,T)\le\lfloor T/2\rfloor+2\lceil T/2\rceil+2\approx 1.5T+2$ (§1B).
2. **Boundary or interior.** All exact data for $R\ge 2$, $T\ge 2$ fit $h=2R+\lfloor 3T/2\rfloor-2$ (table in §2). The apparent fit to $2R+T-1$ was a small-$T$ artefact: $h(2,4)=8$, not 7. So the saving over $2R+2T$ looks like about $T/2$, not $T$. I could not find a general family achieving $2R+1.5T$ either, so for large $R$ and $T$ the saving beyond $O(1)$ is **unproven**. Restricted searches show the optimal solutions are irregular and do not come from a 2y+t staircase plus corner fixes (§4).
3. **Exact data.** See the table in §2.
4. **What the circuit gets.** The main $Y$-gadget gains only 2 gates per $S$ from what is proven. Q5 gives a real and fully verified saving: the $x_0$ part of each per-$S$ gadget drops from about $2T$ to about $1.5T$, which is optimal for the 2-row gadget at $T\le 6$. The new per-$S$ cost is $N+2T_S+\lfloor (T_S+1)/2\rfloor-2$ instead of $N+3T_S+2$. The circuit total goes from $(N-1)(N+2)+\tfrac32 kmN+1$ to $\approx N^2+\tfrac54 kmN$, a saving of about $kmN/4+4N$ gates (§5).

## 1. Explicit constructions (all checked exactly on every grid point)

Verification code: `constr.py`, which checks with exact integer arithmetic.

### A. General: $2R+2T-2$ (all $R,T$), verified for $0\le R,T\le 30$
Let $H(c)=(-1)^c(c-1)$. Then
$$y(-1)^t=\sum_{c=2}^{2R+T}H(c)\,[2y+t\ge c]\;-\;\sum_{c=2}^{T}H(c)\,[t\ge c].$$
This is $f=\mathcal G(2y+t)-\mathcal G(t)$ with $\mathcal G(u)=\varphi(u)/2-(-1)^u/4$. The added 2-periodic term cancels in the difference, and it kills the jump at $c=1$ in both staircases. Within the family "one staircase on $2y+t$ plus a function of $t$" this is optimal: the jumps are forced up to one parameter $q$, and $q$ can cancel only the jump at $c=1$ in each staircase.

### B. Lexicographic floor family: $R+\lfloor T/2\rfloor+R\lceil T/2\rceil$, verified for $0\le R,T\le 30$
With $L=(2R+1)t+y$:
$$y(-1)^t=\sum_{k=1}^R[y\ge k]+2R\sum_{j}[t\ge 2j]-2\sum_{j=1}^{\lceil T/2\rceil}\sum_{k=1}^R[L\ge (2R+1)(2j-1)+k].$$
This is the identity $y(-1)^t=y-2y\,[t\text{ odd}]$. For $R=1$ it reads $x(-1)^t=x+2\lfloor t/2\rfloor-2\lfloor (t+x)/2\rfloor$, which uses **$T+1$** gates and is optimal. For $R=2$ it uses $\lfloor T/2\rfloor+2\lceil T/2\rceil+2$ gates, which is optimal at $T=2,4$. For $R\ge 3$ it is worse than A. This is the only use of the $(2R+1)t\pm y$ forms I found that pays off.

### C. Q5 gadget: $-2\varphi(t)-C\,x_0(-1)^t$ on $\{0,1\}\times\{0..T\}$ in $T+\lfloor (T+1)/2\rfloor+1$ gates
Using $x_0(-1)^t=x_0+2\lfloor t/2\rfloor-2\lfloor (t+x_0)/2\rfloor$:
$$-2\varphi(t)-Cx_0(-1)^t=\underbrace{\big(-2\varphi(t)-2C\lfloor t/2\rfloor\big)}_{T\text{ gates on }t}+\underbrace{2C\sum_{j\ge1}[t+x_0\ge 2j]}_{\lfloor (T+1)/2\rfloor\text{ gates}}-C[x_0\ge1].$$
I verified this for $T\le 60$ and $C\in\{0,2,6,64,1000\}$. The old cost was $2T+2$ (a $t$-staircase plus a $2x_0+t$-staircase). With the variant $-4\mathcal G(t)$ (as used in the circuit), the $t$-staircase loses its $c=1$ gate.

**Optimality (exact MILP over all dichotomies, `q5.py`, $C=64$):** the minimum equals the construction for every $T\le 6$, and for $x_0(-1)^t$ up to $T=8$:

| T | min for $x_0(-1)^t$ | min for $-2\varphi(t)-Cx_0(-1)^t$ | min for $-4\mathcal G(t)-Cx_0(-1)^t$ | old |
|---|---|---|---|---|
| 1 | 2 | 3 | 2 | 4 |
| 2 | 3 | 4 | 3 | 6 |
| 3 | 4 | 6 | 5 | 8 |
| 4 | 5 | 7 | 6 | 10 |
| 5 | 6 | 9 | 8 | 12 |
| 6 | 7 | 10 | 9 | 14 |
| 7 | 8 | – | – | 16 |
| 8 | 9 | – | 12 (time limit, no better found) | 18 |

There is also a proof sketch of the lower bound $\lceil 3T/2\rceil$ for $C\ge 2T$, $C$ even. Every line crosses row 0 and row 1 at most once, so lines are edges or half-edges on the $2T$ row gaps, all of which have nonzero demand. A component with no half-edge must have zero total demand. A parity check shows such components have at least 4 vertices when $C\ge 2T$. Hence the number of lines is at least $2T-\#\{\text{balanced components}\}\ge 2T-\lfloor 2T/4\rfloor$.

## 2. Table of $h(R,T)$

Methods:
- **E** = exact via combinatorial Benders (`benders.py`). This has **no** weight bound: a set-cover MILP is solved and a supporting set is accepted only if $f\in\mathrm{span}$, checked by exact rational arithmetic.
- **M** = big-M MILP over *all* halfplane dichotomies of the grid. The enumeration is complete (`dich.py`, every critical direction). The lower bound is valid under $|w_j|\le 4|G|+8$. All upper bounds are rechecked with exact rational weights.
- "ub" = best solution found when the time limit was hit. "dual" = the MILP's proven lower bound at that time.

| R \ T | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| 1 | 2 (M) | 3 (M) | 4 (M) | 5 (M) | 6 (M) | 7 (M) | 8 (M, from Q5 run) |
| 2 | 4 (M) | 5 (M) | **6 (E)** | **8 (M)** | 8–**9** (M dual 8) | 8–**11** | 9–**12** |
| 3 | 6 (M) | **7 (E)** | **8 (M)** | 8–**10** | 8–12 | | |
| 4 | 8 (M) | 8–**9** | 8–**10** | 8–13 | | | |
| 5 | 10–10 (ub 10, lb 2R) | 10–**11** | 10–14 | | 10–16 (parallel) | | |
| 6 | 12–12 (ub, lb 2R) | | | | | 12–20 (parallel) | |

* An entry "a–b" means a proven lower bound $a$ and a verified construction of size $b$. Lower bounds are the largest of $2R$ (rigorous, §3), $\lceil 3T/2\rceil$ for $R\ge3$ (rigorous, §3), and the MILP dual bound, which assumes $|w_j|\le 4|G|+8$.
* Bold values equal the fitted formula $2R+\lfloor 3T/2\rfloor-2$ ($R\ge2$, $T\ge2$). The fitted formula predicts 11 for (3,5), 12 for (4,4), 12 for (5,3), 15 for (5,5) and 19 for (6,6). There the MILP, run under heavy machine load with 3000 s limits, found nothing better than 12, 13 (lines restricted to the $2y+t$ family, verticals and row-0-crossing lines), 14, the parallel construction, and the parallel construction respectively. **For grids of size 5×5 and up, my exact tools only reproduce the $2R+2T-2$ construction.** The formula is therefore not tested there.
* $T=1$: $h(R,1)=2R$, which is tight by the vertical-strip bound. The parallel construction A also gives $2R$ there.
* The MILP solutions with exact rational weights are stored in `work/milp_*.json`, `work/m2_all_*.json` and `work/r0x_*.json`. They can be viewed with `python3 -I work/view.py FILE`.

The prediction $2R+\lfloor 3T/2\rfloor-2$ applies for $R\ge2$, $T\ge2$. The exceptions are $T=1$, where $h=2R$, and $R=1$, where $h=T+1$.

## 3. Rigorous lower bounds (perimeter/strip argument)

Take any axis-parallel sub-rectangle of the grid. Each line meets its boundary cycle in exactly two unit edges, on two *different* sides, and contributes $+w$ at one and $-w$ at the other. So the lines crossing the rectangle form a graph on its boundary edges. Each boundary edge has a demand, namely the jump of $f$ along it. Every connected component must have zero total demand, and the number of lines is at least (#nonzero-demand edges) − (#components).

* **Vertical strip $[t,t+1]\times[0,R]$:** all $2R$ side edges have demand $-(-1)^t$, the top edge has $2R(-1)^t$, and the bottom edge has 0. Everything therefore lies in one component, so **at least $2R$ lines cross every vertical strip**, and $h\ge 2R$. This is tight for $T=1$.
* **Horizontal strip $[y,y+1]\times[0,T]$, $y\ge2$:** the bottom gaps have demand $-2y(-1)^g$, the top gaps $2(y+1)(-1)^g$, and the two sides $\pm1$. A component that avoids both sides must satisfy $y\,a=(y+1)\,b$ with $a,b$ alternating sums, and must contain both bottom and top gaps. That forces at least 4 vertices (at least 3 when $y=1$). Hence **$h\ge\lceil 3T/2\rceil$ for $R\ge3$**, and $h\ge\lceil 4T/3\rceil$ for $R=2$.

So no family with $2R+T+O(1)$ halfplanes exists when $T\gtrsim 4R$. In the regime $R\approx T$ these bounds give only $\max(2R,1.5T)$, against an upper bound of $2R+2T-2$. Combining the row and column bounds failed: corner-to-corner lines count towards both, so pure counting cannot beat $\max$.

## 4. Structure of optimal solutions; what failed

* **No line crosses row 0** in the optimal 3×3 solution: the 5 lines pass left of $(0,0)$ and 3 pass right of $(0,T)$. Restricting to row-0-avoiding lines keeps the optimum for 3×3 and 2×4. Lines avoiding both row 0 and row $R$ are infeasible.
* In 2×5 (9 gates), 4 lines form a pencil through the row-0 point $(0,3.5)$ with weights summing to 0. In 3×4 (10 gates), two vertical lines sit at odd gaps 1 and 3, as in the floor family, together with near-vertical lines that shift by one gap at a single row.
* Restricted searches that did **not** reach the optimum:

| Restriction | 3×3 | 3×4 |
|---|---|---|
| (2,1)-staircase plus one pencil | 10 | |
| Two pencils left and right of row 0 | ≥9 | |
| (2,1)-staircase, verticals and corner-cutting lines | | 11 vs 10 |
| (2,1)-staircase, verticals and *all* row-0-crossing lines | | 11 vs 10 |

  So the optimal solutions are not "2y+t staircase plus local boundary fixes".
* A parallel-family obstruction: if every line comes from a few parallel families, the rows-$\ge1$ conditions force the $2y+t$ jumps to be $(-1)^c c+p(c \bmod 2)$. That leaves at least $T-2$ vertical jumps. Moving a single line's row-0 crossing by one gap is possible geometrically (tilt below $1/(R-1)$), but it does not remove the vertical lines.

## 5. Consequences for the circuit (verified)

The per-$S$ function is $P_S=(-1)^t(4Y_S-Cx_0)$ with $C=M/N=2N$:
$$P_S=4\mathcal G(2Y_S+t_S)-\big[4\mathcal G(t_S)+2C\lfloor t_S/2\rfloor\big]+2C\lfloor (t_S+x_0)/2\rfloor-Cx_0 .$$

| Term | Gates |
|---|---|
| $4\mathcal G(2Y+t)$ | $N+T_S-1$ |
| $t$-staircase | $T_S-1$ |
| $t+x_0$ staircase (even thresholds only) | $\lfloor (T_S+1)/2\rfloor$ |
| $-Cx_0$ | merged into the existing single $x_0$ gate (the $S=\emptyset$ term) |

**Per $S$:** $N+2T_S+\lfloor (T_S+1)/2\rfloor-2$, against the old $N+3T_S+2$, a saving of $\lfloor T_S/2\rfloor+4$ per set.

**Total:**
$$\sum_{S\ne\emptyset}\big(N+2|S|m+\lfloor (|S|m+1)/2\rfloor-2\big)+1\;\approx\;N^2+\tfrac54 kmN,$$
against the old $(N-1)(N+2)+\tfrac32kmN+1$.

`circuit_new.py` rebuilds both circuits and compares the final weighted sums $P$ input by input:
- **Identical on all inputs** for $(k,m)\in\{(1,1),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2)\}$, which are all inputs since $n\le 16$.
- Identical on 4000 structured random inputs for $(4,3),(5,4),(6,5)$.

The output equals Andreev's $x_{\text{addr}}$ in every case. Gate counts match the formula exactly, for example $k=6$, $m=5$: 7039 → 6323.

| $k$ | $m$ | old | new | saving | saving ÷ $(kmN/4)$ |
|---|---|---|---|---|---|
| 4 | 3 | 559 | 455 | 104 | 2.17 |
| 6 | 5 | 7039 | 6323 | 716 | 1.49 |
| 8 | 32 | 164095 | 146691 | 17404 | 1.06 |
| 10 | 100 | 2585599 | 2325507 | 260092 | 1.02 |

The ratio in the last column tends to 1: the extra $4N$ term matters only when $km$ is small.

If a general $2R+\tfrac32T+O(1)$ family existed (the data fit it, but it is unproven), the $Y$-gadget would save another $\approx T_S/2$ per set, about $kmN/4$ more in total. A $2R+T$ family would save $kmN/2$ in total, but §3 rules it out when $T\gg R$.
