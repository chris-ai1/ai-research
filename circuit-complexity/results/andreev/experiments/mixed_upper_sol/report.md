<!-- Copyright (c) 2026 Christian Reitwiessner. -->
Authors: Christian Reitwiessner

# Resumed mixed-upper research: a new slope-$21/2$ ordinary-Andreev family

## Result and scope

**New construction:** for every positive integer $m$, ordinary $A_{3,m}$ has a block-symmetric threshold-of-threshold circuit with
$$
S_3(m)=6\lfloor m/2\rfloor+6m+\lfloor3m/2\rfloor+26
$$
**bottom gates and $S_3(m)+1$ total gates**. The top reads raw inputs as allowed. Thus the slope is $21/2$, improving the inherited $27/2$. This realizes the $(2,2,2,2,2,2,1)$ threshold-amplitude pattern left UNKNOWN in the old work. It does not improve the balanced leading constant $5/16$: $k$ is fixed at three, and no construction for growing $k$ is claimed.

**Recovered, not newly discovered:** the old $A_{2,4}$ witness has **10 bottoms + 1 top**, versus Theorem G's **12 + 1**. A newly recorded consequence is its restriction to $A_{2,3}$: **10 bottoms + 1 top**, improving the **11 + 1** baseline quoted in both earlier reports. The diagonal identity behind it generalizes, but the generalization has slope $7/2$, worse than Theorem G's $3$.

Everything here works for arbitrary independent table bits. No generator restriction is imposed. In the user's generator formulation, $G(u)$ would supply the evaluated table values; a circuit description $D$ is never an input feature of our threshold circuit. No Lean, online posting, or subagents were used.

## 1. New threshold-amplitude certificate for $k=3$

Identify table addresses and characters with subsets of $\{1,2,3\}$, represented as integers $0,\ldots,7$ in little-endian address order. Put
$$
\chi_S(c)=(-1)^{|S\cap c|},\qquad
h_S(x)=\sum_{c=0}^7\chi_S(c)x_c,
\qquad H_{S,r}(x)=[h_S(x)\ge r].
$$
For each singleton or pair $S$, use $r=0,1$. For the triple $S=7$, use only $r=0$. These are thirteen actual threshold functions of the table. Assign weights
$$
a_S=\begin{cases}18&|S|=2,\\15&|S|=1\text{ or }3.\end{cases}
$$
Define the linear table term
$$
D(x)=6(x_0+x_7)+8\sum_{c\notin\{0,7\}}x_c-30.
$$
The certificate is
$$
F(x,b)=D(x)+\sum_{(S,r)}a_S\chi_S(b)(2H_{S,r}(x)-1).
$$
**Exact finite theorem:** for all $x\in\{0,1\}^8$ and all $b\in\{0,1\}^3$,
$$
(2x_b-1)F(x,b)\ge15.
$$
This is an exhaustive integer certificate on just 2048 cases; it involves neither floating-point acceptance nor a solver UNKNOWN. A compact independently reproducible verification is:

```python
from itertools import product
chi = lambda s,c: (-1)**((s & c).bit_count() % 2)
for x in product((0,1), repeat=8):
    for b in range(8):
        value = 6*(x[0]+x[7])+8*sum(x[1:7])-30
        for s in range(1,8):
            h = sum(chi(s,c)*x[c] for c in range(8))
            a = 18 if s.bit_count()==2 else 15
            for r in ([0] if s==7 else [0,1]):
                value += a*chi(s,b)*(2*int(h>=r)-1)
        assert (2*x[b]-1)*value >= 15
```

The minimum is attained. The minima grouped by table weight $|x|=0,\ldots,8$ are respectively $15,19,23,15,15,15,23,19,15$.

**How found:** the simplest clipping $q_S=\operatorname{sgn}(h_S)$ already separates all three-bit tables with a suitable linear intercept. Keeping this map for singletons and pairs, replacing the triple by $2[h_7\ge0]-1$, and solving a small LP for the top coefficients gives the thirteen-amplitude certificate. Rational reconstruction and averaging under permutation of the three address coordinates produce the integers above. The LP was a discovery aid; the displayed exhaustive integer test is the certificate.

## 2. Explicit bottom gates and proof for every $m$

For character $S$, let $t_S=\sum_{i\in S}s_i$ and $T_S=|S|m$. Since $S$ is nonempty, $-4\le h_S(x)\le4$. For every amplitude $(S,r)$, introduce
$$
g_{S,r,j}=[6t_S+h_S(x)\ge12j+r],\qquad
j=0,\ldots,\lfloor T_S/2\rfloor,
$$
and one table-only bottom gate $H_{S,r}=[h_S(x)\ge r]$. Set $C_{S,r}=\sum_jg_{S,r,j}$.

If $t_S=2\ell$, then $C_{S,r}=\ell+H_{S,r}$. If $t_S=2\ell+1$, then $C_{S,r}=\ell+1$. The bounds $-5\le h_S-r\le4$ make both equalities exact, including endpoints. Consequently
$$
4C_{S,r}-2t_S-1-2H_{S,r}
=\chi_S(b)(2H_{S,r}-1).
$$
Thus the actual top score is the integer expression
$$
P(x,s)=D(x)+\sum_{(S,r)}a_S\big(4C_{S,r}-2t_S-1-2H_{S,r}\big),
$$
and the output is $[P>0]$. The preceding identity gives $P=F$ on every input, proving correctness and margin at least 15 for every $m$.

Each $g$ has raw address weights $6$ on blocks in $S$ and zero elsewhere, table weights $\pm1$, top weight $4a_S$, and cutoff $12j+r$. Each table-only gate has top weight $-2a_S$. The remaining terms are direct input weights and a constant. No intermediate parity or amplitude computation is supplied for free.

There are six singleton amplitudes, six pair amplitudes, and one triple amplitude, each costing $\lfloor T_S/2\rfloor+2$ bottoms. This gives the claimed count. Equivalently,
$$
S_3(m)=\begin{cases}21m/2+26&m\text{ even},\\(21m+45)/2&m\text{ odd}.\end{cases}
$$
The inherited subcube construction uses
$$
G_3(m)=12\lceil m/2\rceil+6m+\lceil3m/2\rceil.
$$
The new family is smaller for even $m\ge10$ and odd $m\ge7$. Taking the minimum of the two is valid for all $m$. At $m=7$, counts are **96 bottoms / 97 total**, versus inherited **101 / 102**; at $m=10$, **131 / 132**, versus **135 / 136**; at $m=20$, **236 / 237**, versus **270 / 271**. These are comparisons of explicit constructions, not claims of finite optimum.

`constructions.py` additionally checks equality $P=F$ using the actual gate list on every table and every count vector for $m=1,2,3,4,7,10$, including 340736 cases at $m=10$. All arithmetic is Python integer arithmetic. Block symmetry makes this full-domain checking on the original raw input bits.

## 3. Recovery and explanation of the inherited 10-bottom witness

The old witness in `mixed_upper/k2m4.md`, `report_body.md`, and `verify_k2m4_10.py` is genuine. Write $x=(x_0,x_1,x_2,x_3)$. Its score is
$$
\begin{aligned}
P_2={}&16x_0+12x_1+2x_2-4s_1+14s_2-15\\
&-12\sum_{j=1}^2[s_2+x_1\ge2j]
-16\sum_{j=1}^2[s_2+x_0\ge2j]
+8\sum_{j=1}^2[s_1+x_1\ge2j]\\
&+6([s_1-s_2+x_3\ge1]-[s_1-s_2+x_1\ge1])\\
&+6([s_1+s_2+x_3\ge5]-[s_1+s_2+x_1\ge5]).
\end{aligned}
$$
It has ten bottoms, one top, and margin one. Its restriction to $s_i\le3$ gives the same ten-bottom circuit for $A_{2,3}$. This restricted consequence was missed by the earlier finite $m=3$ search and the newer GPT baseline; the $m=4$ circuit itself is inherited.

For integer $L$, the key identity is
$$
[L+x_3\ge h+1]-[L+x_1\ge h+1]=(x_3-x_1)[L=h].
$$
The two paired diagonals therefore add $6(x_3-x_1)d(s)$, where
$$
d(s)=[s_1=s_2]+[s_1+s_2=4].
$$
On $0\le s_i\le4$, $d=1$ at every odd–odd pair, $d=0$ at mixed parity, and $0\le d\le2$ at even–even pairs. Expanding the six axis gates, the four parity cases have scores:

- even–even: $16x_0+(12-6d)x_1+2x_2+6dx_3-15$;
- odd–even: $16x_0+20x_1+2x_2-19$;
- even–odd: $2x_2-1$;
- odd–odd: $2x_1+2x_2+6x_3-5$.

The designated table bit determines each sign with margin one. This proves the old witness directly and explains its boundary sharing.

### Parameterized boundary family: no slope improvement

For any $m$, retain the three axis staircases through $j=\lceil m/2\rceil$. Include difference diagonals $s_1-s_2=4z$ and sum diagonals $s_1+s_2=4z$ whenever the line contains an odd–odd pair in $[0,m]^2$. Realize each diagonal by its two threshold gates using the displayed identity. Every odd–odd pair lies on exactly one such line, mixed parities on none, and even–even pairs on at most two. The same four-case proof therefore works for every $m$.

Let $q=\lceil m/2\rceil$, the number of odd count values. There are $2q-2$ lines when $q$ is even, and $2q-1$ when $q$ is odd. The bottom count is
$$
S_{\rm diag}(m)=\begin{cases}7q-4&q\text{ even},\\7q-2&q\text{ odd}.
\end{cases}
$$
Its slope is $7/2$, so it does not improve Theorem G asymptotically. It gives 10 bottoms for $m=3,4$, 24 for $m=7,8$, and 38 for $m=11,12$. Exact all-count checks passed for every $m=1,\ldots,16$. The conclusion concerns this explicit extension, not every possible use of boundary sharing.

## 4. Recovered old results and exact search frontier

The following prior results were read before experimenting:

- `mixed_upper/report_assembled.md`, `report_body.md`, `sec3.md`, `k3_explicit.md`, `fix3.md`, `finite_table.md`, `notes_theory.md`, scripts and relevant logs: inherited subcube family, periodic LP reduction, finite witnesses and incomplete threshold-amplitude work.
- `push_upper/report.md`, `constr3.py`, and `linear_trick/constr_d.py`: $d''$ remains the growing-$k$ benchmark $N^2/2+3kmN/4-\Theta(kN)+O(N+km)$, balanced leading constant $5/16$.
- `push_lower/report.md`, `review_lower/report.md`, and `mixed_sign/report.md`: coherent/mixed-sign barriers and their scope; no new unrestricted impossibility is asserted here.
- `variants_sol/report.md`: the seven-bottom candidate remains refuted, with 56 failures. It was not used as a circuit.

The inherited all-$k$ subcube construction remains
$$
G(k,m)=\sum_{t=1}^k\binom kt2^{k-t}\lceil tm/2\rceil,
$$
with $G+1$ total gates and slope $k3^{k-1}/2$. Its proof uses $\kappa_k=2$, $\kappa_j=1+\sum_{t=1}^{k-j}\binom{k-j}{t}\kappa_{j+t}$ and top score $\sum_{c\succeq b}\kappa_{|c|}(x_c-1/2)$. The old `fix3.md` corrects the intermediate expression in `sec3.md`; the final dominance identity is correct. This construction is inherited, not a discovery of this continuation.

Old finite pool minima, extracted from `logs/finite_k2.log`, for $m=1,2,3,4,5$ respectively: axis $3,5,11,12,17$; richer block-symmetric $3,4,11,10,19$; mixed halves $3,6,14,13,$ unrecorded. They are upper bounds from restricted searches, not full optima. The known full optimum at $m=2$ is three; those pools miss it. The new restriction improves the $m=3$ recorded upper bound to ten.

**New bounded SAT attempt:** `pool_search.py 3 50 9` searched all 88 distinct single-table-bit gates with count directions $(1,0),(0,1),(1,1),(1,-1)$, all thresholds, integer top weights in $[-64,64]$, direct input weights in the same interval, and cutoff constant in $[-256,256]$. It used all 256 count/table constraints and four CP-SAT workers. Result after 50 seconds: **UNKNOWN**, no nine-bottom witness. This is not UNSAT or a lower bound.

**Exact failure of a simple growing-$k$ extension:** let $q_S=\operatorname{sgn}(h_S)$ for all nonempty $S$, and scores $R_b=\sum_Sq_S\chi_S(b)$. Allow an arbitrary table-dependent intercept. The necessary and sufficient ordering $\min_{x_b=1}R_b>\max_{x_b=0}R_b$ holds for every table when $k=2,3$, but fails for **14336 of 65536 tables at $k=4$**. `frontier.py` exhaustively verifies this using integer matrices and records an explicit failing table. This rules out only this fixed clipping rule with equal reconstruction weights. It does not rule out adaptive thresholds, unequal weights, extra atoms, or a general ordinary-Andreev improvement. In particular, the new thirteen-amplitude certificate was obtained by changing the triple rule and allowing unequal character weights.

The old $k=4$ arbitrary-amplitude run `sym_k4_2221.log` ended **UNKNOWN after 2406 seconds**; the suggestion in one old summary that this was feasible should not be inherited as a theorem. Likewise, no general noncancellation theorem for distinct fluctuating atoms is established here.

## 5. Artifacts and reproduction

New files are confined to `/tmp/andreev_gap/mixed_upper_sol/`. Existing worker directories and processes were preserved. No research jobs remain from this continuation.

- `constructions.py`: standalone standard-library construction builders, exact finite certificate, actual gate-list verification, and JSON export.
- `exact_checks.log`: all integer verification results.
- `explicit_2_3.json`, `explicit_2_4.json`: recovered/restricted ten-bottom witnesses.
- `explicit_3_10.json`: new 131-bottom circuit; 132 total gates.
- `fourier_probe.py`, `fourier_probe.log`: LP discovery of the thirteen-amplitude pattern; exact proof does not depend on the LP.
- `pool_search.py`, `pool_m3_9.log`: bounded nine-bottom search and UNKNOWN outcome.
- `frontier.py`, `frontier.log`: exact failure frontier for the simplest Walsh-sign extrapolation.

Run `python3 constructions.py` from this directory for the main certificates. Discovery/frontier scripts add `/tmp/pydeps` themselves. The useful next constructive target is adaptive threshold quantization of Walsh coefficients at $k=4$; the former $k=3$ slope-$10.5$ realizability question is now resolved affirmatively.
