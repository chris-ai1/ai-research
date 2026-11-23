<!-- Copyright (c) 2026 Christian Reitwiessner. -->
Authors: Christian Reitwiessner

# Exact mixed-sign constructions: finite improvements, no balanced subquadratic family

**Proved exact results:** $S(A_{3,2})\le8$, $S(A_{3,3})\le32$, and $S(A_{3,4})\le36$, improving the supplied 41, 48, and 62-bottom witnesses respectively. A separate explicit construction gives $S(A_{4,4})\le256$, versus 370 for the supplied general builder on that instance. Every count excludes the single top gate. These are upper bounds, not minimum-size claims.

**No improved asymptotic exact upper bound for balanced ordinary Andreev was obtained.** In particular, nothing here proves $o(n^2)$ at $km\asymp N$. The finite improvements are exact worst-case improvements, including an exactly balanced $(k,m)=(4,4)$ instance. Two new-to-this-attempt architectures scale in parameters: permutation-rank cancellation gives $S\le N^{\lceil m/2\rceil}$, in particular $S\le N$ for every $k$ when $m=2$; monochromatic hyperplane covers give subquadratic bounds in the **fixed-small-$m$, growing-$k$ regime only**. Neither establishes literature novelty.

All bottom gates below are expanded linear forms of the raw independent table and address bits. The rank, distance, and parity notation is used only to prove identities; no derived quantities are supplied as circuit inputs. The constructions do not use approximation, average-case correctness, a table generator, or an extra layer.

## 1. Permutation-rank cancellation: $N$ bottoms when $m=2$

Index blocks and table bits from zero. Define, for the proof only,
$$
U=\sum_{i=0}^{k-1}2^i a_{i,1},\qquad V=\sum_{i=0}^{k-1}2^i a_{i,2}.
$$
For each $c\in\{0,\ldots,N-1\}$ use the single bottom gate
$$
g_c=\left[x_c+\sum_i2^i a_{i,1}+\sum_i2^i(2c_i-1)a_{i,2}\ge c+1\right].
$$
The top gate is
$$
\boxed{\left[\sum_{c=0}^{N-1}g_c-\sum_i2^i a_{i,1}\ge1\right].}
$$
To prove it, let $T_c=\sum_i2^i(c_i+(1-2c_i)a_{i,2})=V\mathbin{\mathrm{xor}}c$. As $c$ varies, $T_c$ is a permutation of all integers $0,\ldots,N-1$. The gate equals one when $T_c<U$, equals $x_c$ when $T_c=U$, and equals zero when $T_c>U$. The unique equality index is $c=U\mathbin{\mathrm{xor}}V=b$. Hence, identically for every table and raw address,
$$
\sum_cg_c=U+x_b.
$$
This is cancellation of the *number of strict comparisons*, not extraction of a digit by a free operation. Each comparison is an actual charged bottom gate; the strict-comparison count is exactly the displayed raw linear form.

**Signs and weights.** In block $i$, the two coefficients are $(2^i,-2^i)$ when $c_i=0$ and $(2^i,2^i)$ when $c_i=1$. There is no common global reorientation making all these gates block-coherent: it would have to make both $(+,-)$ and $(+,+)$ coherent in the same block. Address weight magnitudes are at most $2^{k-1}$, thresholds at most $N$, top weights at most $2^{k-1}$, and table weights are one. Thus magnitude bit length is at most $k+1$, although weights are exponential in $k$.

### Pairing all address columns

Let $r=\lceil m/2\rceil$ and $M=2^{rk}=N^r$. Set a nonexistent final even-column bit to zero if $m$ is odd. For an index $C$ consisting of $r$ $k$-bit words $c^{(p)}$, put $\ell(C)=\bigoplus_pc^{(p)}$. Use
$$
g_C=\left[x_{\ell(C)}+\sum_{p,i}2^{pk+i}a_{i,2p+1}
+\sum_{p,i:\,2p+2\le m}2^{pk+i}(2c_i^{(p)}-1)a_{i,2p+2}\ge C+1\right].
$$
The top subtracts the raw odd-column rank $R=\sum_{p,i}2^{pk+i}a_{i,2p+1}$ and thresholds at one. For fixed even columns, the comparison targets permute $0,\ldots,M-1$. Equality picks the pairwise XORs of columns, whose wordwise XOR is precisely $b$. Therefore $\sum_Cg_C=R+x_b$ and $S=M$. Magnitudes are at most $M$; bit length is at most $rk+1$.

This extension is exact but expensive: at balance its count is roughly $2^{km/2}$, not subquadratic. In particular, it is not a way to hide parity preprocessing inside a large real weight.

## 2. Monochromatic hyperplanes and positive exact margins

Here is the second mechanism, which produces the 32- and 36-bottom witnesses.

Suppose an integer affine raw-address form $L(a)$ has the property that $L(a)=0$ only at addresses with $b=c$. The two actual gates
$$
g^+=[L(a)+x_c\ge1],\qquad g^-=[-L(a)+x_c\ge1]
$$
satisfy
$$
g^++g^--1=(2x_c-1)[L(a)=0].
$$
This follows by checking the three cases $L<0$, $L=0$, and $L>0$. Thus a collection of such hyperplanes covering all addresses yields an exact circuit: sum the two-gate expressions and threshold at zero. Multiple coverage is harmless, since all active contributions have the same correct sign.

The improvement is to retain only selected **one-sided** gates, then find a raw affine top correction whose score stays on the correct side on every address. This need not cancel the address-dependent contribution exactly. If
$$
g_j=[\eta_jL_{c_j,t_j}(a)+x_{c_j}\ge1],\quad \eta_j\in\{-1,1\},\quad v_j>0,
$$
write
$$
V(a)=u\cdot a+K+\sum_jv_j[\eta_jL_{c_j,t_j}(a)\ge1],\qquad
W_c(a)=\sum_{j:c_j=c}v_j[L_{c,t_j}(a)=0].
$$
Monochromaticity implies the exact top score is
$$
P(x,a)=V(a)+x_bW_b(a).
$$
Consequently the finite conditions
$$
V(a)\le-1,\qquad V(a)+W_b(a)\ge1\quad\text{for every raw }a
$$
prove correctness for **all** $2^N$ tables. These are worst-case, integer inequalities; no statistical margin is involved. They allow nonconstant coverage and uncancelled but safely bounded tails. Requiring the stronger exact affine cancellation condition failed in the bounded search; relaxing to these exact sign margins succeeded.

### The 32-plane family for $k=3$, $m=3$ or $4$

For $t\in\{0,1,2,3\}$, write $t=u+2v$. For each label $c$ and block $i=0,1,2$, let
$$
e_i(c,t)=(u,v,c_i\oplus u\oplus v)\quad(m=3),
$$
and append a zero coordinate when $m=4$. Define the affine form
$$
L_{c,t}(a)=\sum_{i=0}^2 3^i\left(|e_i|-2+\sum_{j=1}^m(1-2e_{i,j})a_{i,j}\right).
$$
Each summand in parentheses is $d_H(a_i,e_i)-2$. Its range is $[-2,1]$ for $m=3$ and $[-2,2]$ for $m=4$. The largest nonzero base-three place exceeds the maximum absolute contribution of all lower places, so
$$
L_{c,t}(a)=0\iff d_H(a_i,e_i)=2\quad\text{for all }i.
$$
Each equality forces the block parity to be $c_i$.

For $m=3$, within each local parity class of four vertices, the layer excludes exactly the vertex $e_i$. Thus, for an address of parity $c$, each block excludes one value of $t$. Three blocks exclude at most three of the four choices, leaving at least one plane containing the address. For $m=4$, a local parity class has eight vertices; the layer excludes $e_i$ and its complement. As $t$ varies these four excluded pairs partition the class, so the same four-choice argument works. The resulting 32 hyperplanes are genuinely varied within-block mixed-sign views.

For each entry $(\eta,v)$ in the certificate tables below, insert exactly one bottom gate
$$
\boxed{g_{c,t,\eta}=\left[x_c+\sum_{i,j}\eta3^i(1-2e_{i,j})a_{i,j}\ge
1-\eta\sum_i3^i(|e_i|-2)\right]}
$$
with top coefficient $v$. A cell with two entries inserts two gates. The top is $[\sum v g+u\cdot a+K\ge0]$. All numbers in these formulas and tables are fixed independently of the input.

### Explicit certificate for $A_{3,3}$: 32 bottoms

| $c$ | $t=0$ | $t=1$ | $t=2$ | $t=3$ |
|---:|---|---|---|---|
| 0 | $(+,18)$ | $(-,14)$ | $(-,18)$ | $(+,18)$ |
| 1 | $(-,18)$ | $(+,18)$ | $(+,16)$ | $(-,18)$ |
| 2 | $(+,18)$ | $(-,18)$ | $(-,20)$ | $(+,16)$ |
| 3 | $(-,18)$ | $(+,18)$ | $(-,2)$ | $(-,18)$ |
| 4 | $(+,18)$ | $(+,2)$ | $(-,18)$ | $(+,18)$ |
| 5 | $(-,16)$ | $(+,20)$ | $(+,18)$ | $(-,18)$ |
| 6 | $(+,18)$ | $(-,16)$ | $(-,18)$ | $(+,18)$ |
| 7 | $(-,18)$ | $(+,18)$ | $(+,14)$ | $(-,18)$ |

In block-major coordinate order,
$$
u=(2,-2,-18,6,-6,4,18,-20,-14),\qquad K=-251.
$$
Exhaustive integer evaluation checks all **131,072** raw table/address assignments with minimum signed margin **1**. The largest absolute integer, including the top constant, is **251**.

### Explicit certificate for $A_{3,4}$: 36 bottoms

| $c$ | $t=0$ | $t=1$ | $t=2$ | $t=3$ |
|---:|---|---|---|---|
| 0 | $(+,24)$ | $(-,26)$ | $(-,22)$ | $(+,24)$ |
| 1 | $(-,24)$ | $(-,2)$ | $(-,2)$, $(+,24)$ | $(-,24)$ |
| 2 | $(-,2)$, $(+,24)$ | $(-,26)$ | $(-,24)$ | $(+,24)$ |
| 3 | $(-,22)$ | $(+,22)$ | $(+,24)$ | $(-,24)$ |
| 4 | $(+,18)$ | $(-,22)$ | $(-,18)$ | $(+,18)$ |
| 5 | $(-,20)$ | $(+,16)$ | $(+,20)$ | $(-,21)$, $(+,1)$ |
| 6 | $(+,18)$ | $(-,22)$ | $(-,18)$ | $(+,18)$ |
| 7 | $(-,22)$ | $(+,18)$ | $(-,1)$, $(+,23)$ | $(-,22)$ |

In block-major coordinate order,
$$
u=(-2,2,-24,2,-6,6,-2,6,-16,16,-12,16),\qquad K=-333.
$$
Exhaustive integer evaluation checks all **1,048,576** raw table/address assignments with minimum signed margin **1**. The largest absolute integer, including the top constant, is **333**.

## 3. Exactly balanced $A_{4,4}$: 256 bottoms

The same four-bit-block layer works with a different code of mask choices. Use
$$
\mathcal C=\{(t,t,t,t):t\in\mathbb Z/4\mathbb Z\}
\cup\{(t,t+1,t+2,t+3):t\in\mathbb Z/4\mathbb Z\}.
$$
For any $s\in\{0,1,2,3\}^4$, some $z\in\mathcal C$ differs from $s$ in **every** coordinate. If $s$ omits a symbol, use its constant word. Otherwise $s$ is a permutation. The four residues $s_i-i$ cannot be all distinct: their sum is zero modulo four, whereas the sum of four distinct residues is two modulo four. Thus some $t$ is absent among those differences; the word $(t+i)_i$ avoids $s$ in every coordinate.

For each $c\in\{0,\ldots,15\}$ and $z\in\mathcal C$, define
$$
e_i=(z_{i,0},z_{i,1},c_i\oplus z_{i,0}\oplus z_{i,1},0),\qquad
L_{c,z}=\sum_{i=0}^33^i\left(|e_i|-2+\sum_{j=1}^4(1-2e_{i,j})a_{i,j}\right).
$$
The local excluded-pair index gives a word $s$. The covering property supplies a plane containing the address. As before, every plane is monochromatic for its label. Use the two bottom gates $[L_{c,z}+x_c\ge1]$ and $[-L_{c,z}+x_c\ge1]$ for every $(c,z)$ and top
$$
\left[\sum_{c,z}(g^+_{c,z}+g^-_{c,z})-128\ge0\right].
$$
There are $2\cdot16\cdot8=256$ bottoms. The score is $(2x_b-1)$ times the positive coverage multiplicity. Here $N=km=16$ and $n=32$ exactly. All 65,536 raw addresses were checked with exact affine dependence on all 65,536 independent tables, certifying all $2^{32}$ inputs without enumerating those tables individually. The minimum signed margin is one. Address coefficients are at most 27, bottom thresholds at most 81 in absolute value, and the largest integer anywhere is the top constant 128.

This finite improvement does not imply a family at the balanced growing-$k$ limit.

## 4. General hyperplane-cover bound and its actual parameter range

Let $r=\lfloor m/2\rfloor$, $p_m=\binom mr/2^{m-1}$, and $Q=m+1$. For each $c$, choose tuples of masks with $|e_i|\equiv c_i+r\pmod2$ and use the planes
$$
L_{c,e}=\sum_iQ^i\left(|e_i|-r+\sum_j(1-2e_{i,j})a_{i,j}\right)=0.
$$
Since every digit has absolute value at most $m$, $Q^i>m\sum_{h<i}Q^h$ proves that zero forces every distance to equal $r$. Hence each plane is monochromatic. A uniformly chosen allowed mask tuple contains any fixed raw address of label $c$ with probability $p_m^k$.

There are $M=2^{k(m-1)}$ such addresses for each $c$. Taking
$$
T=\left\lceil\frac{\log M+1}{p_m^k}\right\rceil
$$
independent mask tuples leaves expected uncovered count at most $Me^{-Tp_m^k}<1$. Therefore a covering family of at most $T$ tuples exists for each $c$. Fix one such family once and for all, then use the two-gate identity. This proves the nonuniform exact bound
$$
\boxed{S\le2N\left\lceil\frac{k(m-1)\log2+1}{p_m^k}\right\rceil.}
$$
This is a probabilistic existence proof of a **fixed, everywhere-correct circuit**, not an average-case correctness statement. Exhaustive search can select the masks; no efficient selection algorithm is claimed. Magnitude bit length is $O(k\log(m+1))$ for bottom coefficients and thresholds, plus $O(\log(NT))$ for the top constant.

For fixed $m\le8$, $p_m>1/2$, and the bound is $O(kN^{1+\log_2(1/p_m)})$. In particular, for $m=3,4$ it is $O(kN^{\log_2(8/3)})$; for $m=5,6$, $O(kN^{\log_2(16/5)})$; and for $m=7,8$, $O(kN^{\log_2(128/35)})$. Since $n=N+O(k)$ in these regimes, these are exact subquadratic **unbalanced** families. They do not answer the balanced problem.

At balance $m\asymp2^k/k$, $p_m=\Theta(m^{-1/2})$. The count supplied by this cover bound has logarithm
$$
\log_2 S=\tfrac12k^2-\tfrac12k\log_2k+O(k),
$$
which is superpolynomial in $N$. Thus merely scaling this central-layer cover is quantitatively inadequate. We must still use the supplied quadratic general construction in that regime.

## 5. Comparison with the supplied baselines

| Instance/regime | Supplied exact upper bound | This attempt | Interpretation |
|---|---:|---:|---|
| $A_{3,2}$ | 41 bottoms | **8** | permutation-rank identity |
| $A_{3,3}$ | 48 bottoms | **32** | one-sided mixed hyperplane margins |
| $A_{3,4}$ | 62 bottoms | **36** | one-sided mixed hyperplane margins |
| $A_{4,4}$, exactly balanced | 370 from supplied `count_dpp(4,4)` | **256** | explicit eight-word mask cover |
| $A_{2,2}$ | minimum 3 | paired-rank construction uses 4 | no improvement |
| $A_{2,3}$ and $A_{2,4}$ | 10 | paired-rank construction uses 16 | no improvement |
| $A_{3,6}$ | 83 | no competitive replacement established | retain supplied witness |
| fixed $k=3$, all $m$ | slope $21/2$ formula supplied in task | no better all-$m$ slope proved | finite improvements only |
| balanced growing $k$ | leading $5n^2/16$ supplied exact research bound | **unchanged** | no subquadratic claim |

The 370 comparison uses the exact counting function from the supplied `push_upper/constr3.py`, reproduced only for comparison in `constructions.py`; the $O(N+km)$ term in the asymptotic formula is not silently dropped. The older Lean-formalized $3n^2/4$ upper is not used as the benchmark. The failed seven-bottom $A_{2,3}$ candidate and all approximate witnesses play no role. We do not claim the new finite witnesses are optimal or formally verified in Lean.

## 6. Experiments, validation, and precise limitations

Search was confined to explicit hyperplane-cover hypotheses. There was no unrestricted CEGIS and no delegated work.

- `search_planes.py`: attempted exact affine cancellation of the one-sided tails, choosing one orientation per plane. The fixed two-orientation pool (64 options) and all lexicographic priorities/signs (1,536 options) returned HiGHS infeasible. These floating-solver statuses are **not** certified impossibility results.
- `search_margin.py`: six bounded positive-margin LPs on the larger pool gave support counts 173, 126, 107, 96, 93, and 88. Their rationalized margins were checked exactly, but all are inferior to the trivial 64-bottom cover and are not the reported improvements.
- `search_sparse.py`: the fixed 64-option pool, with a 47-gate feasibility target and top-weight cap 128, produced an exactly checked 44-bottom intermediate $A_{3,3}$ witness.
- `search_sparse_opt.py`: minimizing support in that concrete pool produced 32 bottoms for $m=3$. The $m=4$ run hit its 25-second limit with a 36-bottom incumbent. Its incumbent was verified exactly; the timeout proves **no optimality statement**. Both used bounded top weights during discovery, not a restriction on the mathematical model.
- `test_extension.py`: extending precisely the final $m=3$ orientations to $m=4$ returned LP infeasible. This is an unverified search diagnostic, not a proof that no 32-bottom $m=4$ circuit exists.
- `refine_verify.py`: with the chosen supports fixed, integer optimization simplified the coefficients. Independent exhaustive gate evaluation then checked all 131,072 and 1,048,576 table/address inputs respectively, with margin one. The largest integers are 251 (8 magnitude bits) and 333 (9 magnitude bits). This check evaluates the actual gates; it does not assume the monochromatic-plane reduction.
- `constructions.py`: exact all-address/all-table coefficient checks for paired-rank instances $(1,2),(2,2),(3,2),(4,2),(2,3),(2,4)$ and for the $(4,4)$ cover. The general rank and cover identities also have the algebraic proofs above.

All solver calls completed or stopped at their own time limit. No solver remains running from this attempt. Other jobs and historical files were preserved. No shared archive file was edited, and no commit or push was made.

### Focused next step

The most useful concrete mechanism is **one-sided monochromatic hyperplanes with worst-case tail margins**, combined with the independent observation that a structured family of comparisons can have an exactly linear rank sum. Exact cancellation is unnecessarily restrictive: it failed in the tested 32-plane family, whereas the two-sided inequalities produced the new 32-gate circuit.

A sharply defined next experiment is to take the explicit 128 planes for $A_{4,4}$ and seek one-sided orientations and positive top coefficients satisfying $V(a)\le-1<V(a)+W_b(a)$ on all 65,536 addresses, starting from the guaranteed two-sided 256-gate cover. This tests the new mechanism at an exactly balanced instance and a larger $k$, rather than merely refining the fixed-$k=3$ slope.

For the actual asymptotic target, central monochromatic layers are too sparse under the proved cover accounting. The unresolved step is a construction that shares comparisons across labels—potentially by letting a bottom gate depend on several independent table bits—and proves a simultaneous worst-case sign margin, with a total $o(N^2)$ gate count at $km\asymp N$. Nothing in the finite certificates supplies this step. Large positional coefficients successfully flatten conjunctions and realize rank cancellation, but they do not by themselves solve it.

## 7. Files and reproduction

Final exact witnesses, with every raw bottom coefficient and top parameter:

- `exact_k3_m2.json`: 8-bottom rank circuit.
- `exact_k3_m3.json`: 32-bottom certificate, margin one.
- `exact_k3_m4.json`: 36-bottom certificate, margin one.
- `exact_k4_m4.json`: 256-bottom exactly balanced cover.

`final_checks.json`, `verification_results.json`, and `construction_checks.json` contain the exact check summaries. `verify_final.py` independently verifies the saved final witnesses without running a solver. Search scripts and their result JSON files preserve the intermediate attempts separately; the files named `exact_...` are the final witnesses. All new artifacts credit Christian Reitwiessner.

To verify the saved final witnesses without a solver, run from this directory:

```sh
OPENBLAS_NUM_THREADS=1 python3 verify_final.py
```

For reconstruction, `constructions.py` rebuilds the explicit families and checks all table coefficients; `refine_verify.py` re-solves the small fixed-support integer simplification and exhaustively verifies its output. NumPy/SciPy are loaded from the supplied `/tmp/pydeps`. None of these commands modifies the shared archive.
