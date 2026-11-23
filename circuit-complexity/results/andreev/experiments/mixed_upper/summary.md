## 0. Summary

**Bottom line.**
- I found **no mixed-sign family that beats the coherent constructions**, at fixed $k$ or in the balanced case.
- I found, and proved, a new explicit **block-symmetric** family for every $k$ (Theorem 3.1). It contains Theorem G at $k=2$, and at $k=3$ it needs less than half the gates of the earlier constructions. For $k\ge4$ it is worse than (d'').
- Most of the work is a reduction that turns the fixed-$k$ slope question into a finite problem, plus a set of proved obstructions explaining why mixed signs did not help in it.

### Positive results
1. **Periodic reduction** [PROVED] (§1).
   - Staircases whose coefficients are periodic in the threshold have *no boundary effects*. The top sum of such a circuit is exactly $D(x)+\sum_aw_a((L_a-r_a)\bmod p_a)$ for every $m$.
   - So the slope at fixed $k$ is the optimum of a finite sparse sign-representation problem on $\{0,1\}^N\times(\mathbb Z/P)^d$. This holds for any partition of the blocks, hence for mixed signs.
   - Together with a count-vector reduction for part-symmetric gates (Lemma 1.1), it gives exact verification for all $m$ at once.
2. **Theorem 3.1** [PROVED; VERIFIED].
   - For all $k,m$ there is a block-symmetric circuit with
   $$G(k,m)=\sum_{t=1}^k\binom kt2^{k-t}\lceil tm/2\rceil\quad\text{gates},$$
   bottom weights $0/1$, rational top weights, and top sum exactly $\sum_{c\succeq b}\kappa_{|c|}(x_c-\frac12)$.
   - $k=2$ gives Theorem G.
   - $k=3$ gives $12\lceil m/2\rceil+6m+\lceil3m/2\rceil$, slope $13.5$ against $18$ for (d''). For example, 135 against 312 (d') and 339 (d'') at $m=10$.
   - Verified exactly: bit-exhaustive for $n\le20$, and on all count vectors for $k=2$, $m\le30$; $k=3$, $m\le12$; $k=4$, $m\le2$.

### The key question: no
3. **At fixed $k$, size cannot grow slower than $m$ in the periodic world, mixed or not** [PROVED, Lemma 2.1].
   - Every periodic construction has slope $\ge k/2$, the conjectured parity value.
   - At $k=2$ this is slope $\ge1$, the slope of the coherent lower bound $m-1$. So inside periodic constructions **mixed signs cannot beat the slope of the coherent lower bound**.
4. **Beating Theorem G's slope 3 at $k=2$ needs fluctuating atoms** [PROVED, Theorem 2.4 + Lemma 2.2].
   - Pure-parity constructions, of any sign pattern, need slope $\ge3$. Mixed signs make no signal-carrying atom cheaper (Lemma 2.6).
   - Every unrestricted search over fluctuating and mixed atoms returned slope 3, using pure parity atoms only (§4.1): two halves at period 4 (261 600 atoms) and block-symmetric at periods up to 8 (2.08 million atoms). When the pure atom on $\{1,2\}$ was excluded, the best was $3.5$, with three fluctuating $(1,-1)$ atoms. PLACEHOLDER-CAPSUM
5. **Balanced case** [PROVED bounds, §5].
   - Pure-parity constructions of any sign pattern cost $\ge n^2/16$. They pay **no $Y$-range cost**, so they beat $\frac5{16}n^2$ iff the $|S|$-weighted number of gadgets per character stays below 5 with cheap $D$.
   - Data on $\bar n$: 1.5 at $k=2$ (exact); 1.75 at $k=3$ with arbitrary amplitudes, 2.25 realised; 1.875 at $k=4$ with arbitrary amplitudes (PLACEHOLDER-K4S). Whether $\bar n$ stays bounded with *realisable* (threshold) amplitudes is open; it is the most concrete route to a better constant.
   - $o(n^2)$ needs fluctuating atoms with periods $n^{\Omega(\epsilon)}$ that are heavily mixed ($\gtrsim\epsilon\log n$ patterns per block). Bounded-view designs are capped by the existing lower bounds.

### Other proved obstructions
- One monomial gadget per character is impossible for every $k\ge2$ (Lemma 2.5).
- One gadget per character with arbitrary amplitudes is impossible at $k=2$ (proved) and at $k=3$ (CP-SAT).
- No hyperplane in count space is parity-pure for two characters (Lemma 2.7), which rules out minterm-style designs.

### LP/MILP data
- §4.1: slopes per atom class.
- §4.2: finite-$m$ pool minima for $k=2$. The mixed pool never beats the block-symmetric pools.
