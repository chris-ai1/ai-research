## 3. An explicit family for all $k$: "subcube dominance" (generalises Theorem G; beats the earlier constructions at $k=3$)

The periodic LP at $k=3$ (pure-parity atoms, period 2, single-bit table forms) returned a structured solution. Character $S$ uses exactly the table bits $x_c$ with $c_i=0$ for all $i\in S$. Theorem G at $k=2$ has the same shape: $A_1=2X_{00}+X_{01}$, $A_2=2X_{00}+X_{10}$, $A_{12}=2X_{00}$. The LP also gives linear $D$, and at $k=2,3,4$ (`subcube_k.py`) the weights depend only on $|c|$. This leads to a proof for all $k$.

### Theorem 3.1 [PROVED; VERIFIED]
Fix weights $\kappa_k=2$ and $\kappa_j=1+\sum_{t=1}^{k-j}\binom{k-j}{t}\kappa_{j+t}$ for $j<k$. For $|c|=j<k$ put $\lambda_c=\kappa_j/2^{k-j}$. The circuit has:
- **bottom gates** $[\,t_S+x_c\ge 2l\,]$ for every address $c$, every nonempty $S\subseteq\overline{\operatorname{supp}c}$ and $l=1,\dots,\lceil|S|m/2\rceil$. All bottom weights are $0/1$.
- **top weights** $-2\lambda_c$ on these gates, plus the linear part
$$\sum_{c,S}\lambda_c\,(t_S+x_c)+\sum_{|c|<k}\lambda_cx_c+\kappa_kx_{1\cdots1}-\tfrac{\kappa_k}2-\tfrac12\sum_{|c|<k}\kappa_{|c|}.$$
- **output** $[\,\mathrm{top}>0\,]$.

It computes $A_{k,m}$ for every $k,m$ with margin at least $\frac12$, using
$$G(k,m)=\sum_{t=1}^{k}\binom kt2^{k-t}\Big\lceil\frac{tm}2\Big\rceil\qquad\text{gates, slope }\frac k2\,3^{k-1}.$$

*Proof.*
1. By Lemma 1.2 the staircase of the pair $(S,c)$ contributes $\lambda_c\big((e_S+x_c)\bmod2\big)=\lambda_c\big(x_c+e_S(b)(1-2x_c)\big)$.
2. For fixed $c$ with support $C$, $\sum_{\emptyset\ne S\subseteq\bar C}e_S(b)=2^{k-|c|-1}[\,b\not\preceq c\,]$, where $b\preceq c$ means $\operatorname{supp}b\subseteq C$.
3. With $d_c=\lambda_c$, the coefficient of $x_c$ in the top sum is $\kappa_c[\,b\preceq c\,]$. Collecting constants,
$$\mathrm{top}(x,b)=-\tfrac{\kappa_k}2-\tfrac12\Big(\kappa_b+U_b-\kappa_k[b\ne1^k]\Big)+\kappa_bx_b+\sum_{c\succ b}\kappa_cx_c,\qquad U_b=\sum_{c\succ b}\kappa_c .$$
4. Since $\kappa_b>U_b$, this is $\ge(\kappa_b-U_b)/2$ when $x_b=1$ and $\le-(\kappa_b-U_b)/2$ when $x_b=0$. For $b=1^k$ the top sum is $\kappa_k(x_b-\frac12)$. ∎

Each table bit $c$ is "switched off" exactly at the addresses outside its upper subcube. At address $b$ only the bits $c\succeq b$ survive, and $x_b$ dominates them.

**Verification** (`subcube_family.py`, exact rationals):
- $k=2$: $m\le8$ exhaustively over all bit inputs, and $m\le30$ on all count vectors. The family *is* Theorem G: $4\lceil m/2\rceil+m$.
- $k=3$: $m\le4$ bit-exhaustive, and $m\le12$ on all count vectors.
- $k=4$: $m=1$ bit-exhaustive, and $m\le2$ on all count vectors.
- The gate count equals $G(k,m)$ in every case.

| $k=3$, $m$ | 1 | 2 | 3 | 4 | 6 | 8 | 10 | 20 | 40 |
|---|---|---|---|---|---|---|---|---|---|
| Theorem 3.1, $12\lceil m/2\rceil+6m+\lceil3m/2\rceil$ | 20 | 27 | 47 | 54 | 81 | 108 | 135 | 270 | 540 |
| (d') `constr2` | 71 | 96 | 125 | 150 | 204 | 258 | 312 | 582 | 1122 |
| (d'') `constr3` | 65 | 87 | 128 | 150 | 213 | 276 | 339 | 654 | 1284 |

Slopes:

| $k$ | Theorem 3.1 | (d'') |
|---|---|---|
| 2 | 3 | 6 |
| 3 | 13.5 | 18 |
| 4 | 54 | 48 |
| 5 | 202.5 | 120 |

So **Theorem 3.1 is the best known family for $k\le3$**. At $k=3$ it uses less than half of the earlier gate counts for every $m$. It loses for $k\ge4$, because it puts $2^{k-|S|}$ gadgets on character $S$, i.e. $\bar n=(3/2)^{k-1}$ in the notation of §5. **It is block-symmetric (coherent): mixed signs played no role.**

The LP's own $k=3$ circuit has rational weights and some odd-threshold atoms (`realize_k3_mono.py`, `k3_family.json`). It has $\lceil27m/2\rceil+12$ gates, verified bit-exhaustively for $m\le4$ and on all count vectors for $m\le20$. Theorem 3.1 has the same slope and 12 fewer gates.

### 3.2 Can $k=3$ go below slope $27/2$?
- **One two-valued gadget per character** (slope 6): **infeasible** even with arbitrary amplitude functions of $x$ [VERIFIED by CP-SAT for integer $\Delta_S\in[1,12]$; `onegadget_any.py`]. It stays infeasible when up to three characters (singletons, pairs or the triple) get a second gadget, and with pairs doubled.
- **Arbitrary two-valued amplitudes** with 2 gadgets on every singleton and pair and 1 on the triple (slope $10.5$): **feasible** [VERIFIED], all $\Delta=2$, so the amplitudes are *ternary* $\{-4,0,4\}$. Also feasible: $(3,3,3,2,2,2,1)$ (slope 12) and $(4,4,4,2,2,2,1)$ (slope 13.5).
- **Realising slope 10.5 with gates** requires every amplitude to be a sum of two threshold functions of $x$. These cost $|S|m/2+O(1)$ via period-$p$ staircases on $\frac p2t_S+\alpha\cdot x$ with $p>2\operatorname{range}(\alpha\cdot x)$. The CP-SAT model with threshold amplitudes, $|\alpha_c|\le3$ and linear $D$ (`gadget_thr.py`) ended **UNKNOWN** after 1500 s.
- Searches over realisable atoms found nothing better than $13.5$:
  - reweighted $L_1$ with 12 random restarts (`k3_restarts.py`): best $15.5$;
  - column generation with comb amplitudes up to support 3 (`run_cg_parity.py`): best $20$;
  - CP-SAT with single-bit monomials (`cpsat_parity_only.py`): best $15$ after 1800 s, bound $2.5$.
- **Open:** whether slope $10.5$ is realisable at $k=3$.
