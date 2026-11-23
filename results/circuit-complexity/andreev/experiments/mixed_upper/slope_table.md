| $k$ | atom class (domain) | #atoms | method | best slope | status |
|---|---|---|---|---|---|
| 2 | pure parity, any two-valued amplitudes | – | proof (Thm 2.4) | **3** | **exact (lower bound = Theorem G)** |
| 2 | block-sym., period 2, all 16 monomial table forms ($P=2$) | 48 | CP-SAT, $\lvert w\rvert\le6$ | 3 | exact within bounds |
| 2 | block-sym., periods 2,4, $\alpha\in\{0..3\}^4$ ($P=4$) | 15 456 | rw-$L_1$ + prune; CG | 3 | heuristic |
| 2 | block-sym., periods 2,4, $\alpha\in\{0,1\}^4$, CP-SAT asked for slope $\le2.75$ | 1 056 | CP-SAT | PLACEHOLDER-CAP | |
| 2 | block-sym., only cheap atoms (cost $\le\frac12$, incl. all fluctuating ones), $P=4$ | 10 304 | rw-$L_1$ + prune | 3.5 | heuristic |
| 2 | block-sym., periods 2,4,8, $\alpha\in\{0..7\}^4$ ($P=8$) | 2 079 840 | CG + prune | 3 | heuristic |
| 2 | **two halves (mixed)**, periods 2,4, $\beta\in\{-1..2\}^4$, $\alpha\in\{0..3\}^4$ ($P=4$) | 261 600 | CG + prune | 3 | heuristic; optimum used only $\beta=(2,2\,\lvert\,\cdot)$ |
| 2 | any periodic construction, any signs | – | proof (Lemma 2.1) | lower bound 1 | |
| 3 | pure parity, single-bit monomials ($P=2$) | 3 584 | rw-$L_1$ + prune | **13.5** (Thm 3.1) | heuristic; = Theorem 3.1 |
| 3 | pure parity, monomials and comb amplitudes (support $\le3$) | 53 676 | CG + prune | 20 | heuristic |
| 3 | pure parity, arbitrary two-valued amplitudes, counts $(2,2,2,2,2,2,1)$ | – | CP-SAT | 10.5 feasible | not realised by gates |
| 3 | same, one gadget per character | – | CP-SAT | infeasible ($\Delta\le12$) | |
| 3 | any periodic construction | – | Lemma 2.1 | lower bound 1.5 | |
| 4 | subcube dominance (Thm 3.1) | 65 | proof + LP | 54 (vs (d'') 48) | exact family |
| 4 | arbitrary two-valued amplitudes, counts $(2,2,2,1)$ by $\lvert S\rvert$ (slope 30) | – | CP-SAT on 222 table orbits | PLACEHOLDER-K4R | |
