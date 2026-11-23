<!-- Copyright (c) 2026 Christian Reitwiessner. -->
Authors: Christian Reitwiessner

# Referee report on `explainer.md`

**File reviewed:** `/home/user/.t3/scratch/2026-11-02-improve-upper-bound-of-andreevs-93c6aee6/threshold_paper/explainer.md` (170 lines; not edited).
**Method:**
1. I read the explainer once on its own, as the intended reader would.
2. I tested every formula I could by computer, using scripts in this folder.
3. I then checked consistency with `paper.tex`: Theorem 5 (`thm:exact`) and Appendix B (`app:coherent`, Theorem 18 and Lemmas 19–20).

Line numbers refer to `explainer.md`.

---

## 0. Overall verdict

**Mathematics.** The displayed formulas are correct, and so are both theorem statements. Every identity, range, count and constant that can be checked by computer passed (Section 4 below), with one exception (A4). The two results are reported faithfully.

**Prose.** Several sentences around the formulas are false or misleading. They cluster in the description of the special-address repairs (Sections 2.2–2.3) and in some remarks in 3.7:
- The cause of the error at $b=0$ is misattributed.
- The amplification is called "cheap", but it costs one fifth of the circuit.
- The range saving is stated as a factor of 4, but the realized factor is 2.
- One formula uses the wrong variable.
- One theorem number is wrong.

**Readability rules.** The mandatory rules are violated in several places:
- Four symbols are reused with a different meaning ($S$, $c$, $P$, $z$), plus two minor cases ($j$, $W$).
- About fifteen symbols and terms are used without a definition.
- Four proof skeletons start without a plan.
- Several key steps are asserted without a reason, though a one-line reason exists.

**Recommendation:** revise before circulating. All fixes are local, and replacement text is given for each issue. With them, the note would meet the brief.

*Convention for replacement texts.* Section 3 replacements use the renaming proposed in B1: $G$ is the number of bottom gates, $q$ is a cube, and $F_i$ are prefix sums. If B1 is not adopted, read $G$ as $S$ and $q$ as $c$.

---

## 1. Errors (mathematical or factual), most serious first

### A1. The cause of the error at $b=0$ is misattributed (lines 56 and 70)

> line 56: "For $S\ne\varnothing$, $4Y_S$ equals $X_S$ up to terms that do not depend on $S$, so these terms collapse when summed over $S$."
>
> line 70: "The character sum misses the $S=\varnothing$ term, which leaves an error at the zero address. A correction of the form $-C\,x_0[b=0]$ fixes it."

**Why it is wrong.**
- The missing term $S=\varnothing$ is $X_\varnothing=N-2|x|$, an affine form in the table. The top gate could add it back for free. If that were the only problem, no correction would be needed.
- The dropped part does not simply collapse. Since $X_S=4Y_S-2|x|$, the dropped part is $\sum_{S\ne\varnothing}2|x|(-1)^{t_S}=2|x|(N[b=0]-1)$. This is affine except for $2N|x|$ at $b=0$.
- The real issue is that no $Y_S$ contains $x_0$, because $S\cdot 0=0$ is even. So the score never sees $x_0$.
- At $b=0$ every sign $(-1)^{t_S}$ equals $+1$, so all residues add up there. Before the correction, the score at $b=0$ is $N(w+2)$ with $0\le w\le R$ (definitions below). At balance this is about $n^2$, which is why $C=N(R+4)$ must be so large. The explainer never says how large $C$ is.

**Evidence.** `check_identities.py` checks, for all tables and block counts with $k\le3$ and $m\le4$:

$$\sum_{S\ne\varnothing}4Y_S(-1)^{t_S}=2N[b=0]\sum_{c\ne0}x_c-2N[b\ne0]\,x_b .$$

`build_circuit.py` confirms that $P=N(w+2)-Cx_0$ at $b=0$.

**Replace the last two sentences of line 56 by:**

> Write $|x|=\sum_cx_c$. For $S\ne\varnothing$ we have $X_S=4Y_S-2|x|$. Replacing $X_S$ by $4Y_S$ and dropping $S=\varnothing$ changes the lookup sum only by the constant $N$, except at $b=0$:
> $$N+\sum_{S\ne\varnothing}4Y_S(-1)^{t_S}=\begin{cases}N(1-2x_b),&b\ne0,\\ N+2N\sum_{c\ne0}x_c,&b=0.\end{cases}$$
> At $b=0$ the right side does not depend on $x_0$. Section 2.3 repairs this.

**Replace the $b=0$ bullet (line 70) by:**

> - **$b=0$.** No $Y_S$ contains $x_0$, since $S\cdot0=0$ is even. So the score never sees $x_0$. At $b=0$ every sign $(-1)^{t_S}$ equals $+1$, so the residues of all collapses add up there. Before the correction, the score at $b=0$ is $N(w+2)$, where
> $$w=2\sum_{c\ne0}x_c+2\alpha\sum_ix_{e_i}+\sigma$$
> lies in $[0,R]$ with $R=2(N-1)+2\alpha k+km$. We subtract $Cx_0[b=0]$ with $C=N(R+4)$. Then the score at $b=0$ is at least $2N$ if $x_0=0$, and at most $-2N$ if $x_0=1$. To build the correction, use
> $$x_0[b=0]=x_0-x_0\sigma+\frac4N\sum_{S\ne\varnothing}x_0\Big\lfloor\frac{t_S}{2}\Big\rfloor .$$
> A large weight $B=n+2$ lets $x_0$ switch gates on: the gate $[\,t_S+Bx_0\ge B+2r\,]$ fires exactly when $x_0=1$ and $t_S\ge2r$. So $x_0\lfloor t_S/2\rfloor$ costs $\lfloor|S|m/2\rfloor$ gates, and $x_0\sigma$ costs $km$ more.

(All three displays are verified; see Section 4.)

### A2. "Two cheap fixes remove it" is false (lines 71–73)

> "**$b=e_i$.** The residue of $\lceil t_S/2\rceil$ sits at these $k$ addresses, where it equals $-Ns_i$. Two cheap fixes remove it: shifting the coefficients of the existing odd-threshold staircases adds any function of the address $b$ for free; replacing $Y_S$ by $W_S=Y_S+\alpha\sum_{i\in S}x_{e_i}$, with $\alpha=\lfloor(m-1)/2\rfloor$, amplifies the table bits $x_{e_i}$ enough to absorb the rest."

**Why it is wrong.**
1. *The amplification is not cheap.* It widens the main staircase of each $S$ by $\alpha|S|$ odd thresholds. That is $\alpha kN/2\approx\tfrac14N^2$ gates at balance, one fifth of the total $\tfrac54N^2$. The note's own table (row 2, "$\tfrac14+\tfrac14$") charges exactly this.
2. *Nothing is removed.* The term $-Ns_i$ stays in the final score, which at $b=e_i$ is $2N(1+\alpha)(1-x_{e_i})-Ns_i$. The repairs only make it dominated.
3. The residue belongs to $\sum_S8\lceil t_S/2\rceil^2$, the leftover of Saving 2, not to $\lceil t_S/2\rceil$.
4. "Enough to absorb" hides the reason for $\alpha$. At $b=e_i$ the count $s_i$ is odd, so $1\le s_i\le2\alpha+1$.
5. The note gives no reason why a coefficient shift adds a function of $b$.

**Replace lines 71–73 by:**

> - **$b=e_i$.** Here the collapse of $\sum_S8\lceil t_S/2\rceil^2$ leaves the term $-Ns_i$ in the score. At $b=e_i$ the count $s_i$ is odd, so $1\le s_i\le2\alpha+1$. The term stays; two repairs make it harmless.
>   - *Coefficient shift (free).* Since $\lceil t/2\rceil=t/2+(1-(-1)^t)/4$, we have $\lceil(2W_S+t_S)/2\rceil=W_S+t_S/2+\tfrac14-\tfrac14(-1)^{t_S}$. The left side is the sum of all odd-threshold gates in the staircase of $S$. So adding $\gamma_S$ to each of their top coefficients adds $-\tfrac{\gamma_S}{4}(-1)^{t_S}$ plus an affine term. Summed over $S$, this adds any function of $b$ without new gates. The choice $\gamma_S=-4(2\alpha+1)(k-2|S|)$ adds $N(2\alpha+1)$ at each $e_i$ and nothing elsewhere.
>   - *Amplification (not free).* Using $W_S$ instead of $Y_S$ raises the weight of $x_{e_i}$ at $b=e_i$ from $2N$ to $2N(1+\alpha)$. It widens the staircase of $S$ by $\alpha|S|$ odd thresholds, about $\tfrac14N^2$ gates in total (row 2 of the table in 2.4).
>
>   Together they give $P=2N(1+\alpha)(1-x_{e_i})-Ns_i$ at $b=e_i$. This is at least $N$ if $x_{e_i}=0$, and at most $-N$ if $x_{e_i}=1$.

### A3. Saving 1 overstates the range gain (lines 54–56)

> "**Saving 1: half the range.** Replace $X_S$ by … But $Y_S$ ranges over $[0,N/2]$ instead of $[-N,N]$, so the range is four times smaller."

**Why it is wrong.**
- The heading says "half", the text says "four times smaller", and Section 4 says "halved ranges".
- The staircase of Saving 2 runs over $2Y_S+t_S$, and its table part $2Y_S$ ranges over $[0,N]$. That is half the range of $X_S$, not a quarter.
- A reader who combines "four times smaller" with Saving 2's "half the range" gets $2N/8=N/4$ gates per $S$. The table says $N/2$.
- Also, $X_S$ is replaced by $4Y_S$, not by $Y_S$.

**Replace lines 54–56 by** the following, followed by the A1 text:

> **Saving 1: half the range.** For $S\ne\varnothing$ let $Y_S$ be the number of ones of the table at the $N/2$ addresses $c$ with $S\cdot c$ odd:
> $$Y_S=\#\{c:\ x_c=1,\ S\cdot c\text{ odd}\}.$$
> We replace $X_S$ by $4Y_S$. [A1 text.] The gain: Saving 2 builds a staircase over $2Y_S+t_S$, and $2Y_S$ ranges over $[0,N]$, half the range of $X_S$.

(The condition "$c\ne0$" in the current definition is redundant, because $S\cdot0$ is even. Drop it, or say why it is harmless.)

### A4. Saving 3 uses the wrong variable (lines 63–64)

> "$\sum_{S\ne\varnothing}Y_S^2$ and $\sum_{S\ne\varnothing}Y_St_S$ are expressions in $|x|$, $\sigma=\sum_is_i$ and the products $x_{e_i}s_i$ only."

**Why it is wrong.** No $Y_S$ contains $x_0$, so the sums depend on $\sum_{c\ne0}x_c$, not on $|x|$. Here is a counterexample with $k=m=1$ and $s_1=0$. The tables $(x_0,x_1)=(0,1)$ and $(1,0)$ have the same $|x|$, $\sigma$ and $x_{e_1}s_1$. But $\sum_SY_S^2$ is $1$ for the first and $0$ for the second (found by `check_identities.py`). In addition, $|x|$ is never defined, and "costs $O(n)$" has no mechanism.

**Replace lines 62–64 by:**

> **Saving 3: the leftovers collapse.** Built separately, the leftovers $8W_S^2$, $8W_St_S$ and $8\lceil t_S/2\rceil^2$ would cost at least about $N/2$ gates per set $S$. Summed over $S$, they become functions of a few global forms. Let $|x|_\ast=\sum_{c\ne0}x_c$ be the number of ones of the table outside address $0$, let $\sigma=\sum_is_i$, and let $e_i$ be the address with a single one, in coordinate $i$. Then
> $$\sum_{S\ne\varnothing}Y_S^2=\frac N4\bigl(|x|_\ast^2+|x|_\ast\bigr),\qquad\sum_{S\ne\varnothing}Y_St_S=\frac N4\Bigl(\sigma|x|_\ast+\sum_ix_{e_i}s_i\Bigr).$$
> All quadratic leftovers together equal $\tfrac N2\bigl(w^2+\sum_is_i^2\bigr)$, with $w$ the single form defined in 2.3, plus $2N(1+\alpha)\sum_ix_{e_i}s_i$ and affine terms. The staircase of $w^2$ costs $R=O(n)$ gates. The squares $s_i^2$ cost $km$ gates. Each product $x_{e_i}s_i=\sum_{\ell=1}^m[\,s_i+Bx_{e_i}\ge B+\ell\,]$ costs $m$ gates. That is $O(n)$ in total, not per character. The sum $\sum_S8\lceil t_S/2\rceil^2$ collapses the same way, except for a residue at the $k+1$ addresses $0,e_1,\dots,e_k$ (see 2.3).

If $w$ is introduced here, as suggested in B1, the forward reference goes away. Both displayed sums are verified exhaustively for $k\le3$, $m\le4$.

### A5. Wrong theorem number (line 8)

> "**Upper bound** (Theorem 7)"

In `paper.tex`, theorems, lemmas, propositions, corollaries and facts share one counter. `thm:exact` is the fifth numbered environment. The compiled `paper.pdf` reads "Theorem 5. Put $\alpha$…". Theorem 7 is the general lower bound `thm:lower`. "Appendix B, Theorem 18" is correct.

**Replace with:** "**Upper bound** (Theorem 5)".

### A6. The gate formula is an upper bound, not an exact count (line 88)

> "The exact count is $$\frac{N(N-1)}2+\dots+\Big\lceil\frac{km}2\Big\rceil$$ bottom gates plus one top gate"

The paper says "at most". In my rebuild the realized circuit is sometimes smaller:

| $(k,m)$ | realized | formula |
|---|---|---|
| $(4,4)$ | 370 | 374 |
| $(6,10)$ | 5072 | 5088 |
| $(8,32)$ | 82350 | 82414 |

In both cases I checked, the gap equals the number of main-staircase coefficients $-8\theta+\kappa_S$ that vanish (4 and 64). The paper's own `upper_update_checks.json` shows the same counts.

**Replace with:**

> The count is at most
> $$\frac{N(N-1)}2+\frac{kN(m+\alpha)}2+2(N-1)+2\alpha k+3km+\Big\lceil\frac{km}2\Big\rceil$$
> bottom gates plus one top gate. The first two terms are the main staircases and the correction at $b=0$. Then come $R=2(N-1)+2\alpha k+km$ gates for $w^2$, $km$ for the squares $s_i^2$, $km$ for the products $x_{e_i}s_i$, and $\lceil km/2\rceil$ for the gates of $x_0\sigma$ that are not shared with $S=\{1,\dots,k\}$. A few coefficients vanish, so the realized circuit can be slightly smaller; for example, 370 instead of 374 bottom gates for $k=m=4$.

(The decomposition is verified for all $k\le10$, $m\le40$.)

### A7. The random-sign remark is incomplete as stated (line 156)

> "A gate with random $\pm1$ weights inside a block is non-constant with probability at least $1/(2\sqrt{2km})$ under *every* restriction that leaves one live bit per block. Arguments that count surviving gates therefore cannot exceed $O(n^{3/2})$. This includes majority-of-majority circuits."

**Problems.**
- The threshold is not specified, and the claim fails for large thresholds. With threshold $km$ and $m\ge2$, the probability is $0$ under the restriction that sets all fixed bits to $0$.
- "Inside a block" leaves open which weights are random.
- The step to $O(n^{3/2})$ needs a missing fact: a restricted circuit never needs more than $N$ survivors.
- "This includes majority-of-majority circuits" is unclear.

**Evidence.** I computed the exact probability with threshold $0$ and validated the formula by brute force on six small cases. The bound holds for every restriction with $k\le12$ and $m\le60$, and it is attained with equality at $k=1$, $m=2$.

**Replace with:**

> - **Why survivor counting stops at $n^{3/2}$ for general gates.** Take a gate with threshold $0$ whose $km$ address weights are independent uniform signs. Under every restriction that leaves one live bit per block, the gate is non-constant with probability at least $1/(2\sqrt{2km})$ over the signs. A restricted circuit never needs more than $N$ surviving gates, because the restricted function is an OR of at most $N$ ANDs of the live bits. So an argument that only counts surviving gates proves at most about $N\cdot2\sqrt{2km}=O(n^{3/2})$ gates. These random gates are majority gates, so the limit applies even to depth-two circuits of majority gates.

### A8. "About $N/(2k)$" does not match the constant that is proved (line 110)

> "so on average about $N/(2k)$ bottom gates must be non-constant there. … So $S\cdot k/m\gtrsim N/(2k)$."

Each splitting gate costs about $k+\log_2G$ bits. At the relevant size $G\approx N^2/k^3$ this is about $3k$, and Step 3 uses $D_0\ge(N-3k-1)/(3k)$. With $N/(2k)$, the paragraph promises $G\gtrsim N^2/(2k^3)$, which is more than is proved. Numerically, $D_0$ at the smallest gate count allowed by the theorem lies between $N/(3k)$ and $N/(2k)$ and tends to $N/(3k)$:

| $k$ | $D_0$ | $N/(2k)$ | $N/(3k)$ |
|---|---|---|---|
| 16 | 1878 | 2048 | 1365 |
| 32 | $5.39\cdot10^7$ | $6.71\cdot10^7$ | $4.47\cdot10^7$ |

**Replace with:**

> On every cube, the circuit reveals the entire table. Each non-constant bottom gate carries only about $k+\log_2G\le3k$ bits, so on average about $N/(3k)$ bottom gates must be non-constant there. On the other hand, a sign-coherent gate is non-constant on at most a $k/m$ fraction of the cubes. So $G\cdot k/m\gtrsim N/(3k)$, that is $G\gtrsim N^2/(3k^3)$ in the balanced case.

### A9. The case $G\ge N^2$ is not handled (line 150)

> "If $S<N^2$ then $\log_2(S+1)\le 2k$ and $D_0\ge(N-3k-1)/(3k)$."

As written, the derivation of the balanced bound in line 106 does not cover $G\ge N^2$. That case is trivial, but it should be said. The paper states it as $G\ge\min\{N^2,\ m(N-3k-1)/(3k^2)\}$.

**Replace with:**

> If $G\ge N^2$ there is nothing to prove. Otherwise $\log_2(G+1)\le2k$, so $D_0\ge(N-3k-1)/(3k)$ and $G\ge m(N-3k-1)/(3k^2)$. With $m=N/k$ this is the stated bound. Exact balance needs $k$ to be a power of two; with $m=\lfloor N/k\rfloor$ the same line still gives $\Omega(n^2/\log^3n)$.

### A10. The comparison with Kane–Williams describes the wrong mechanism (line 118)

> "They fix the non-live bits at random, which concentrates a gate's weighted sum within about $\sqrt m$. Here the fixed part ranges over all $m$ values in each block, which spreads it out."

The Kane–Williams survival bound rests on *anti*-concentration: the random fixed part is spread over about $\sqrt m$ per block, for unit weights. "Concentrates" says the opposite. "The fixed part ranges over all $m$ values" is unclear.

**Replace with:**

> Kane and Williams fix the non-live bits at random. The fixed part of a gate's sum is then spread over a window of width about $\sqrt m$ per block (for unit weights), and a gate survives with probability $O(\sqrt{k/m})$. The cube walk instead moves the number of fixed ones in each block through all values $0,\dots,m-1$. For a sign-coherent gate, the fixed part then moves monotonically across a window of width about $m$ per block. So the gate survives on at most a $k/m$ fraction of the cubes (Step 2). A gate with mixed signs can survive on every cube.

($O(\sqrt{k/m})$ is the paper's Lemma 8, $\mathbb E[U]\le4s\sqrt n/m$, at balance. That mixed signs can split every cube: a gate with weights $+1,-1,+1,\dots$ on block 1, zero weights elsewhere and threshold $1$ splits every cube, for every $k$. `lower_checks.py` confirms this for $k=1$.)

### A11. The Tool 3 count does not follow from the stated per-character cost (line 48)

> "Per character this costs about $2N$ gates for the range of $X+t$. Summed over the $N$ characters it gives $2N^2+kmN$ gates"

As written, $N\cdot 2N=2N^2$, and the reader cannot see where $kmN$ comes from.

**Replace lines 46–48 by:**

> **Tool 3: removing the product.** A product $X(-1)^t$ is not a function of a single linear form. But for even $X$ it is a difference of two such functions:
> $$X(-1)^t=\varphi(X+t)-\varphi(t),\qquad\varphi(u)=(-1)^u u,$$
> because $X+t$ has the parity of $t$. Each $X_S$ is even, being a sum of $N$ terms $\pm1$. The function $\varphi$ changes at every integer. So by Tool 2, $\varphi(X_S+t_S)$ costs $2N+|S|m$ gates (its argument ranges over $[-N,N+|S|m]$), and $\varphi(t_S)$ costs $|S|m$ gates. Each index $i$ lies in half of the $N$ sets $S$, so $\sum_S|S|=kN/2$. The total is $\sum_S(2N+2|S|m)=2N^2+kmN$, which is $3N^2=\tfrac34n^2$ in the balanced case. This simpler circuit is Proposition 4 of the paper, and it is machine-checked in the Lean proof assistant.

### A12. "Lemma 2" is an undefined reference (line 159)

> "Lemma 2 is tight for every $k,m$."

The explainer does not number its lemmas. In the paper this is Lemma 20.

**Replace with:**

> The bound of Step 2 is tight for every $k,m$. Take a gate with one positive weight on the last position of each block, zero weights elsewhere, and threshold equal to that weight. It splits exactly the $m^k-(m-1)^k$ cubes $q$ that have some $q_i=m-1$.

(Verified for $k\le4$, $m\le6$.)

### A13. "Gates" should be "bottom gates" (line 9)

> "every circuit whose gates have a single sign inside each address block needs $\Omega(n^2/\log^3 n)$ gates."

The top gate is unrestricted (line 102). **Replace with:**

> every depth-two circuit whose *bottom* gates have a single sign inside each address block needs $\Omega(n^2/\log^3n)$ gates; the top gate is arbitrary.

---

## 2. Readability

### B1. Symbols reused with a different meaning (this violates a mandatory rule)

| Symbol | First meaning | Second meaning | Fix |
|---|---|---|---|
| $S$ | set of block indices (2.1–2.4) | number of bottom gates (lines 104–106, 128–132, 149–150) | Write "$G$ bottom gates". Use $G$ in $D_0$, $\binom GD$ and $\log_2(G+1)$. |
| $c$ | table address (lines 21, 39, 55) | cube (3.3–3.6); line 115 uses both in $x_{(c\bmod2)\oplus z}$ | Call a cube $q\in\{0,\dots,m-1\}^k$, with corners $(x,a(q+z))$, live bit at position $q_i+1$, and $d_q(x)$, $q^\pm$. |
| $P$ | score (line 75) | prefix sums $P_i$ (line 138) | Rename the prefix sums $F_i$, so that $F(s)=\text{const}+\sum_iF_i(s_i)$. |
| $z$ | gate input in $[\,w\cdot z\ge\theta\,]$ (line 28) | corner offset (3.3–3.4) | Line 28: "A threshold gate outputs $1$ if a weighted sum of its input bits, with real weights, is at least its threshold $\theta$, and $0$ otherwise." |
| $j$ | threshold index in $B+2j$ (line 70) | gate index (3.4) | Use $r$ in line 70. |
| $W$, $W_S$ | generic integer in Saving 2 | $W_S$ used at line 62, but defined only at line 73 | Define $W_S$ in Saving 1 (text below). |

**Add to Saving 1, after the definition of $Y_S$:**

> Section 2.3 will need the slightly larger form $W_S=Y_S+\alpha\sum_{i\in S}x_{e_i}$, with $\alpha=\lfloor(m-1)/2\rfloor$. Here $e_i$ is the address with a single one, in coordinate $i$. On a first reading take $\alpha=0$, so that $W_S=Y_S$.

### B2. Undefined symbols and jargon

| Line | Term | Replacement |
|---|---|---|
| 25 | $a$ in $A(x,a)$ | "Write $a$ for the $km$ address bits." |
| 28 | bracket $[\cdot]$ | "For a statement $Q$, $[Q]$ is $1$ if $Q$ holds and $0$ otherwise." |
| 38 | "character", $\chi_S(b)$ | "the sign $(-1)^{\sum_{i\in S}b_i}$, called the *character* of $S$ at $b$". Then drop $\chi_S$; the note never uses it again. |
| 39 | $S\cdot c$ | "where $S\cdot c=\sum_{i\in S}c_i$" |
| 39 | "Fourier inversion" | Add: "(exchange the two sums; $\sum_S(-1)^{S\cdot(b\oplus c)}$ is $N$ if $c=b$ and $0$ otherwise)". |
| 40 | "linear form" for $X_S$ | "affine form" ($X_\varnothing$ has the constant term $N$) |
| 42 | "integer linear form" | "a linear form with integer values" |
| 56 | "odd half of $S$" | fixed in A3 |
| 64 | $\lvert x\rvert$ | fixed in A4 |
| 75 | "score", "ordinary address", "margin" | defined in the plan of 2.3 (B3) |
| 46, 159 | "Lean" | "the Lean proof assistant (machine-checked proofs)" |
| 132 | $H(x)$ | "the Shannon entropy of $x$; for a uniform table, $H(x)=N$" |
| 138 | $\varepsilon_i=\pm1$ when a block has only zero weights | "$\varepsilon_i=+1$ if the gate's weights in block $i$ are $\ge0$, and $-1$ otherwise" |
| 140 | $F$ | "Let $F(s)$ be the gate's weighted sum on the input $(x,a(s))$." |
| 140 | $c^-$, $c^+$ | "$q^-=q+(\mathbf 1-\varepsilon)/2$ and $q^+=q+(\mathbf 1+\varepsilon)/2$; then $q^+=(q+\varepsilon)^-$" |
| 144 | "unate" | "monotone or antitone in each input bit" |
| 156 | "majority-of-majority" | "depth-two circuits of majority gates" |

### B3. Proof skeletons without a plan

Add these plans.

- **Start of Section 2** (before 2.1):
  > *Plan.* Tool 1 writes $N(-1)^{x_b}$ as a sum of $N$ products, one per set $S$. Tool 3 turns each product into functions of single linear forms, and Tool 2 builds these from threshold gates. That gives $\tfrac34n^2=3N^2$ gates. Three savings (2.2) cut this to about $\tfrac34N^2$. Repairs at $k+1$ special addresses (2.3) add about $\tfrac12N^2$. The total is $\tfrac54N^2=\tfrac5{16}n^2$ (2.4).
- **Start of 2.3:**
  > *Plan.* The *score* $P$ is the weighted sum at the top gate, and the circuit outputs $[-P\ge0]$. An address is *ordinary* if it is neither $0$ nor one of $e_1,\dots,e_k$. At ordinary addresses the collapsed score is already $N(1-2x_b)$. At the $k+1$ special addresses we need only the right sign, with *margin* $|P|\ge N$. We add a large correction switched on by $x_0$ at $b=0$, and we amplify $x_{e_i}$ so that it outweighs the residue at $b=e_i$.
- **Step 1, before "Why."** Also add a bullet for $D$ and the entropy facts:
  > *Plan.* We describe $x$ by a short code read off the circuit on the cube $q$. The code must carry all $N$ bits of $x$, and each splitting gate adds only about $k+\log_2G$ bits. So on average many gates must split.
  >
  > Add the first bullet: "the number $D=d_q(x)$ of splitting gates: at most $G+1$ choices." After the list: "By the chain rule for entropy, with $\log_2\binom GD\le D\log_2G$, $\log_2(2^k-1)\le k$ and $\log_2(2^k+1)\le k+1$: …".
- **Step 2, before "Why.":**
  > *Plan.* Walk through the cubes along a line in the gate's monotone direction. The gate's sum never decreases along the line, so its threshold is crossed in at most one cube of the line. Then count the lines.
- **Saving 3** has no plan; the replacement in A4 starts with one.

### B4. Claims stated without enough reason (not already covered above)

- **Line 44**, "If all steps of $g$ are equal except on a subset, the equal part is affine in $L$ and therefore free." This sentence is never used. The example after it illustrates the previous sentence. **Replace lines 44–45 by:** "The cost is one gate per value of $\theta$ where $g$ actually changes. For example, $\lceil u/2\rceil$ and $\lceil u/2\rceil^2$ change only at odd $u$, so their staircases need only the odd thresholds." Delete the equal-steps sentence, or keep it and name its use.
- **Line 88**, "Using $\sum_S|S|=kN/2$ and $km=N$, the total is $\tfrac54N^2$." This also needs $\alpha\approx m/2$. **Replace with:** "Using $\sum_S|S|=kN/2$, $km=N$ and $\alpha\approx m/2$, the rows add up to $(\tfrac12+\tfrac14+\tfrac14+\tfrac14)N^2=\tfrac54N^2=\tfrac5{16}n^2$."
- **Line 157**, "Combining Step 1 with a bound on how many cubes each gate splits can never give more than $O(n^2/\log n)$ for coherent circuits. A $\Theta(n^2)$ bound would need an argument that does not treat the gates separately." The first sentence has no reason, and the second is speculation stated as fact. **Replace with:**
  > The $\tfrac5{16}$ circuit itself has only $O(kN)$ gates splitting each cube: on one cube, the staircase of $S$ crosses only about $|S|/2$ of its thresholds. So Step 1 can never certify more than $O(kN)$. Step 2 is tight, so this method cannot prove more than about $\tfrac mk\cdot O(kN)=O(mN)=O(n^2/\log n)$. A $\Theta(n^2)$ bound needs a different argument, for example one that does not bound each gate's split cubes separately.

### B5. Ambiguous or vague sentences

| Line | Quote | Replacement |
|---|---|---|
| 11 | "To go below $n^2$ substantially, a circuit must mix signs inside a block." | "To beat $n^2$ by more than a polylogarithmic factor, a circuit needs bottom gates whose weights mix signs inside a block." |
| 30 | "The two results below explain what sits in between." | "Between $n^{3/2}$ and $n^2$ the question is open. The two results below show where the gap lies." |
| 46 | "The first version (the $\tfrac34n^2$ circuit, formalized in Lean)" | covered by the A11 replacement |
| 52 | "Each one cuts the dominant cost." | "Together they cut the cost of 2.1 from $3N^2$ to about $\tfrac34N^2$." |
| 70 | "The bit $x_0$ gates it through a large weight" | covered in A1 ("lets $x_0$ switch gates on") |
| 92 | "A script expands every gate in the raw inputs" | "A script writes every gate as a weight vector on the table bits and the block counts, and checks the score exactly." (That is what the paper's script does. Line 92 already says why block counts suffice.) |
| 114 | "flips exactly one fixed bit in each block $i$ with $z_i=1$: the *live* bit at position $c_i+1$." | "flips exactly one bit in each block $i$ with $z_i=1$, namely the bit at position $q_i+1$. Call it the *live* bit of block $i$. All other address bits are the same at every corner." |
| 118 | "Here the fixed part ranges over all $m$ values in each block" | covered in A10 |
| 156 | "This includes majority-of-majority circuits." | covered in A7 |

### B6. Structure

- **Line 26.** Say early that exact balance needs $k$ to be a power of two: "Exact balance needs $k$ to divide $2^k$, that is, $k$ a power of two. For other $k$ take $m=\lfloor N/k\rfloor$; all asymptotic statements hold in both regimes."
- **Line 28.** Many readers expect the top gate to read only bottom gates. Add: "If the top gate may not read inputs directly, each input becomes a bottom gate, so at most $n$ extra gates."
- **Line 75.** Display the closed form. It makes the margins checkable at a glance (verified):
  $$P=\begin{cases}N(w+2)-Cx_0,&b=0,\\ 2N(1+\alpha)(1-x_{e_i})-Ns_i,&b=e_i,\\ N(1-2x_b),&\text{otherwise.}\end{cases}$$
- **Line 83.** The row label "range of $2W_S$" should be "range of $2Y_S$", since the amplification has its own row.
- **Line 104.** State the hypotheses in full: "Let a depth-two threshold circuit compute $A$ exactly, and let all of its $G$ bottom gates be sign-coherent. Then …".

---

## 3. Optional improvements (not errors)

- **O1 (line 90).** "top coefficients are $O(n^3)$" is true but loose; it repeats the paper's bound. In the construction the largest top coefficient is $C=N(R+4)$, about $0.99\,n^2$ at $(k,m)=(6,10)$ and $(8,32)$. The note could say "at most about $n^2$".
- **O2 (line 158).** On "beats $n^{3/2}$ only from about $k=37$": the sharp form (Steps 1–3, with $m=N/k$ real) crosses $n^{3/2}$ at $k=37$, where $n\approx2.7\cdot10^{11}$. The simplified bound $N(N-3k-1)/(3k^3)$ crosses at $k=38$. The first exact-balance case past the crossover is $k=64$. Adding "$n\approx2^{38}$" makes the point concrete.
- **O3 (line 11 or 3.7).** "Must mix signs" can be quantified by the same argument, since a mixed gate splits at most all $m^k$ cubes. If $M$ bottom gates have mixed signs, then $m^kD_0\le Mm^k+(G-M)(m^k-(m-1)^k)$. Hence a balanced circuit with fewer than $N(N-3k-1)/(6k^3)$ gates has more than $(N-3k-1)/(6k)$ mixed-sign bottom gates. This is my own one-line consequence, not stated in the paper.
- **O4.** The paper's Remark (1) improves the denominator to $6\sqrt2\,k^{5/2}$ for gates that see blocks only through $s_i$, a class that contains the $\tfrac5{16}$ circuit. The note could mention it in one sentence.

---

## 4. Verification log

All scripts are in `/tmp/andreev_gap/explainer_review/` and were run with `python3 -I`. The numpy in `/tmp/pydeps` has no compiled extensions, so the scripts are pure Python. The circuit was rebuilt from the text of Theorem 5's proof, independently of the paper's `verify_upper_updates.py`; it reproduces that script's gate counts exactly.

| Claim (line) | Check | Result |
|---|---|---|
| Fourier lookup (39); $X_S$ even, in $[-N,N]$ | all tables and addresses, $k\le4$ | pass |
| staircase telescoping (43) and the equal-steps remark (44) | 200 random $g$ | pass |
| $\lceil u/2\rceil$, $\lceil u/2\rceil^2$ change exactly at odd $u$ (44) | $u\in[-40,40]$ | pass |
| $X(-1)^t=\varphi(X+t)-\varphi(t)$ for even $X$ (47) | $X,t\in[-30,30]$ | pass; fails for odd $X$, as expected |
| $2N^2+kmN$, and $\tfrac34n^2$ at balance (48) | $k,m\le8$; $k\in\{1,2,4,8\}$ | pass (once $2\lvert S\rvert m$ per $S$ is included) |
| $X_S=4Y_S-2\lvert x\rvert$, $0\le Y_S\le N/2$; "$c\ne0$" redundant (55–56) | exhaustive, $k\le3$, $m\le4$ | pass |
| $\sum_{S\ne\varnothing}4Y_S(-1)^{t_S}=2N[b=0]\sum_{c\ne0}x_c-2N[b\ne0]x_b$ | exhaustive | pass |
| $4W(-1)^t$ identity and the ceiling check (59–60) | all $W,t\in[-40,40]$ | pass |
| $\sum Y_S^2$, $\sum Y_St_S$ "expressions in $\lvert x\rvert$, $\sigma$, $x_{e_i}s_i$" (64) | exhaustive | **fails**; true with $\sum_{c\ne0}x_c$, with the explicit formulas of A4 |
| the paper's three collapse identities, the $\kappa_S$ identity, the $x_0[b=0]$ identity | exhaustive | pass |
| a coefficient shift adds a function of $b$ (72): $\sum_{\theta\text{ odd}}[L_S\ge\theta]=\lceil L_S/2\rceil=W_S+t_S/2+\tfrac14-\tfrac14(-1)^{t_S}$ | exhaustive | pass |
| range $0\le2W_S+t_S\le N+2\alpha\lvert S\rvert+\lvert S\rvert m$; $0\le w\le R$ | exhaustive | pass |
| closed form of $P$, output $[-P\ge0]=x_b$, margin $\ge N$ (75) | rebuilt circuit; all tables and block counts, $k\le3$, $m\le6$ (202,780 cases); raw address bits for 6 small $(k,m)$; 62 tables $\times$ all block counts for $k=4,5$ | pass; the minimum signed score is exactly $N$ |
| 58264 cases (92) | $\sum_{k\le3,m\le4}2^N(m+1)^k$ | pass |
| cost-table rows and $\tfrac54N^2$ (81–88) | exact sums at balance | pass; rows tend to $\tfrac12,\tfrac14,\tfrac14,\tfrac14$ (total $1.232N^2$ at $k=8$, $1.24987N^2$ at $k=16$) |
| gate-count formula (89) | rebuild vs formula | upper bound; equal for $k=3,5$, strict for $k=1,2,4,6,8$ in my runs (A6) |
| $\tfrac5{16}n^2-\tfrac n4\log_2(n/2)+O(n)$ (90) | exact arithmetic, $k=1,2,4,\dots,128$ | pass; the $O(n)$ term is exactly $3n-2\log_2(n/2)-1$ including the top gate |
| weights (90) | rebuild | integers; bottom weights $\le n+2$; thresholds $\le2n+2$; top coefficients about $n^2$ |
| nonnegative block coefficients (94, 102) | rebuild | pass |
| cube restriction: live bit, address $(c\bmod2)\oplus z$, bijection (114–115) | $k\le3$, $m\le5$ | pass |
| lines: $m^k-(m-1)^k$ lines, $(m-1)^k$ non-starts, a partition (142) | every $\varepsilon$, $k\le4$, $m\le6$ | pass |
| Step 2 bound (136) | 4000 random sign-coherent gates (zeros, ties, offsets); 5/16 circuit gates | pass; tight example attains it |
| $m^k-(m-1)^k\le km^{k-1}$; $1-(1-1/m)^k\le k/m$ (136, 150) | exact, $k\le40$, $m\le300$ | pass |
| entropy-count steps (132) | $\log_2\binom SD\le D\log_2S$; $\log_2(2^k\pm1)$ bounds | pass |
| $S<N^2\Rightarrow D_0\ge(N-3k-1)/(3k)$; balanced bound (106, 150) | grid; smallest admissible $S$ for $k=4,8,16,32$ | pass |
| "beats $n^{3/2}$ from about $k=37$" (158) | direct search | 37 (sharp form), 38 (stated form), 64 (exact balance) |
| random $\pm1$ gate, $1/(2\sqrt{2km})$ (156) | exact formula, brute-force validated | pass with threshold $0$ (equality at $k=1$, $m=2$); fails for large thresholds |
| $\tfrac5{16}$ circuit on cubes | $k=3,4,5$ | every gate splits $\le m^k-(m-1)^k$ cubes; $0.55$–$0.72\,kN$ splitting gates per cube on average |

---

## 5. Consistency with `paper.tex`

**Consistent:**
- the setting and the model (the top gate reads inputs);
- the $\tfrac34n^2$ circuit and its Lean status;
- the $4W(-1)^t$ identity;
- $\alpha=\lfloor(m-1)/2\rfloor$ and the definition of $W_S$;
- the count formula and the balanced asymptotics;
- the integrality and the stated weight bounds;
- sign-coherence of the construction;
- the class definition, Theorem 18, $D_0$, both lemmas and their proofs;
- the remarks on tightness, IPS 1997, $k\approx37$ and $O(n^2/\log n)$;
- the status box (independent referee, brute force, not formalized).

**Inconsistent or not in the paper:**
1. Theorem number: 7 in the explainer, 5 in the paper (A5).
2. "The exact count is" versus the paper's "at most" (A6).
3. $|x|$ versus the paper's $z=\sum_{c\ne0}x_c$ (A4).
4. The $b=0$ story: "misses the $S=\varnothing$ term" is not in the paper and is not the mechanism (A1).
5. "Two cheap fixes remove it": the paper says only that amplification "absorbs" the errors (A2).
6. Line 132 has $\log_2S$ where the paper has $\log_2(S+1)$. Both are valid.
7. The case "$\min\{N^2,\dots\}$" is dropped (A9).
8. Remark (4): the paper says "every distribution of restrictions", the explainer "every restriction". The explainer's version is stronger and true, with threshold $0$ (A7).
9. Not in the paper: the "$N/(2k)$" heuristic (A8), the Kane–Williams comparison (A10), "majority-of-majority" (A7), and "a $\Theta(n^2)$ bound would need …" (B4).
10. "Lemma 2" is the paper's Lemma 20 (A12).

The paper's abstract also says "gates" where it means "bottom gates" (compare A13).

---

## 6. Files in this folder

- `check_identities.py`, `check_identities.out` — Section 2 identities, ranges, collapse formulas, and the counterexample of A4.
- `build_circuit.py`, `build_circuit.out`, `build_circuit.json` — independent rebuild of the 5/16 circuit: exhaustive and raw-bit checks, counts, weights, coherence.
- `count_checks.py`, `count_checks.out` — cost table, count decomposition, floor balance, weights, vanishing coefficients. Its exact-balance line is wrong for $k\ge32$ because of a float `log2`; this is superseded by:
- `balance_exact.py`, `balance_exact.out` — exact-arithmetic balanced asymptotics.
- `lower_checks.py`, `lower_checks.out` — cube restriction, lines, Step 2 bound and tightness, inequalities, constants, crossover, random-sign remark.
- `circuit_split_checks.py`, `circuit_split_checks.out` — per-gate split counts and splitting gates per cube for the 5/16 circuit.
- `pdfcheck/pdfgrep.py` — reads theorem numbers from the compiled `paper.pdf`.
