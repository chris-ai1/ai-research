<!-- Copyright (c) 2026 Christian Reitwiessner. All rights reserved. -->
Authors: Christian Reitwiessner

# Andreev's function in depth two: the $\tfrac5{16}n^2$ circuit and the sign-coherent lower bound

This note explains two results from the paper *Depth-Two Threshold Circuits for Andreev's Function: Sharper Bounds* (`paper.tex`):

- **Upper bound** (Theorem 5): an exact depth-two threshold circuit with $(\tfrac5{16}+o(1))n^2$ gates.
- **Lower bound** (Section 6, Theorem 12): every depth-two circuit whose *bottom* gates each have a single sign inside every address block needs $\Omega(n^2/\log^3 n)$ gates. The top gate is arbitrary.

Together they say that the quadratic circuit is optimal, up to polylogarithmic factors, among circuits of the kind it belongs to. To beat $n^2$ by more than a polylogarithmic factor, a circuit needs bottom gates whose weights mix signs inside a block.

The note is meant to be read without the paper. It gives the ideas and proof skeletons; the paper has the full proofs.

---

## 1. Setting

**Andreev's function.** Fix $k,m\ge1$ and put $N=2^k$. The input has two parts:

- a *table* $x\in\{0,1\}^N$, with one bit $x_c$ for each address $c\in\{0,1\}^k$;
- $k$ *address blocks* of $m$ bits each. Write $a$ for the $km$ address bits and $s_i$ for the number of ones in block $i$.

The address is $b\in\{0,1\}^k$ with $b_i=s_i\bmod 2$, and the output is
$$A(x,a)=x_b .$$
The input length is $n=N+km$. In the *balanced case* $km=N$, so $n=2N$ and $k\approx\log_2 n$. Exact balance needs $k$ to divide $2^k$, i.e. $k$ a power of two. For other $k$ take $m=\lfloor N/k\rfloor$; all asymptotic statements hold in both regimes.

**Circuits.** For a statement $Q$, the bracket $[Q]$ is $1$ if $Q$ holds and $0$ otherwise. A threshold gate outputs $1$ if a weighted sum of its input bits is at least its threshold $\theta$, with arbitrary real weights. A depth-two circuit has *bottom* gates on the inputs and one *top* gate. The top gate reads the bottom gates **and the inputs directly**. So any affine function of the inputs is available in the top sum at no cost. This "free affine term" is used throughout. (If the top gate may not read inputs, turn each input into a bottom gate: at most $n$ extra gates.)

**State of the art.** Kane and Williams (2015) proved $\Omega(n^{3/2}/\log^3 n)$ gates and gave an $O(n^3/\log n)$ circuit. The paper improves the lower bound to $\Omega(n^{3/2}/\log^2 n)$ and the upper bound to $(\tfrac5{16}+o(1))n^2$. Between $n^{3/2}$ and $n^2$ the question is open. The two results below show where the gap lies.

---

## 2. The upper bound: $\tfrac5{16}n^2$ gates

*Plan.* Tool 1 writes $N(-1)^{x_b}$ as a sum of $N$ products, one per set $S$. Tool 3 turns each product into functions of single linear forms, and Tool 2 builds these from threshold gates. That gives $\tfrac34n^2=3N^2$ gates. Three savings (2.2) cut the cost per set to about $\tfrac34N^2$ in total. Repairs at $k+1$ special addresses (2.3) add about $\tfrac12N^2$. The total is $\tfrac54N^2=\tfrac5{16}n^2$ (2.4).

### 2.1 Three tools

**Tool 1: lookup as a Fourier sum.** For $S\subseteq\{1,\dots,k\}$ and an address $c$ write $S\cdot c=\sum_{i\in S}c_i$, and let $t_S=\sum_{i\in S}s_i$. Since $s_i\equiv b_i\pmod 2$, the sign $(-1)^{t_S}$ equals $(-1)^{S\cdot b}$. Then
$$\sum_S X_S\,(-1)^{t_S}=N(-1)^{x_b},\qquad X_S=\sum_c(-1)^{S\cdot c+x_c}.$$
(Exchange the two sums: $\sum_S(-1)^{S\cdot(b\oplus c)}$ is $N$ if $c=b$ and $0$ otherwise.) Each $X_S$ is an affine form in the table bits, since $(-1)^{x_c}=1-2x_c$, and each $t_S$ is a linear form in the address bits. So the output sign is a sum of $N$ products "affine form $\times$ parity of a linear form".

**Tool 2: staircases.** Let $L$ be a linear form with integer values in $\{\ell,\dots,h\}$, and let $g$ be any function on the integers. Then
$$g(L)=g(\ell)+\sum_{\theta=\ell+1}^{h}\bigl(g(\theta)-g(\theta-1)\bigr)[L\ge\theta].$$
Each bracket is one bottom gate, and the top gate supplies the coefficients. The cost is one gate per value of $\theta$ where $g$ actually changes. For example, $\lceil u/2\rceil$ and $\lceil u/2\rceil^2$ change only at odd $u$, so their staircases need only the odd thresholds.

**Tool 3: removing the product.** A product $X(-1)^t$ is not a function of a single linear form, but an identity makes it one. Proposition 4 of the paper (the $\tfrac34n^2$ circuit, machine-checked in the Lean proof assistant) uses, for even $X$,
$$X(-1)^t=\varphi(X+t)-\varphi(t),\qquad \varphi(u)=(-1)^u u .$$
$X_S$ is even because it is a sum of $N$ signs. Each term is a function of one linear form, so Tool 2 applies. $\varphi(X_S+t_S)$ costs $2N+|S|m$ gates and $\varphi(t_S)$ costs $|S|m$. Each index $i$ lies in half of the sets, so $\sum_S|S|=kN/2$, and the total is $2N^2+kmN$. That is $\tfrac34n^2$ in the balanced case.

### 2.2 Three savings

Together these cut the cost of 2.1 from $3N^2$ to about $\tfrac34N^2$ (balanced).

**Saving 1: half the range.** For $S\ne\varnothing$ let
$$Y_S=\#\{c:\ x_c=1,\ S\cdot c\text{ odd}\}.$$
Write $|x|=\sum_cx_c$. Then $X_S=4Y_S-2|x|$. Replace $X_S$ by $4Y_S$ and drop the set $S=\varnothing$. This changes the sum only by the constant $N$, except at the address $b=0$:
$$N+\sum_{S\ne\varnothing}4Y_S(-1)^{t_S}=\begin{cases}N(1-2x_b),&b\ne0,\\ N+2N\sum_{c\ne0}x_c,&b=0.\end{cases}$$
At $b=0$ the right side does not depend on $x_0$; Section 2.3 repairs this. The staircases below are built over $2Y_S+t_S$, and $2Y_S$ ranges over $[0,N]$, half the range of $X_S$.

Section 2.3 uses the slightly larger form $W_S=Y_S+\alpha\sum_{i\in S}x_{e_i}$, where $e_i$ is the address whose only one is in coordinate $i$, and $\alpha=\lfloor(m-1)/2\rfloor$. On a first reading take $\alpha=0$, so $W_S=Y_S$.

**Saving 2: odd thresholds only.** Instead of $\varphi$, use the identity
$$4W(-1)^t=4W-8\Big\lceil\frac{2W+t}{2}\Big\rceil^2+8W^2+8Wt+8\Big\lceil\frac t2\Big\rceil^2 .$$
(Check it: for even $t$ the two ceilings are $W+t/2$ and $t/2$; for odd $t$ they are $W+(t+1)/2$ and $(t+1)/2$.) The main term $\lceil(2W_S+t_S)/2\rceil^2$ is a function of the single form $2W_S+t_S$. Its staircase needs only odd thresholds, so it costs half the range of $2W_S+t_S$: about $N/2$ gates from $2Y_S$, $\alpha|S|$ from the amplification and $|S|m/2$ from $t_S$.

**Saving 3: the leftovers collapse.** *Plan:* the quadratic leftovers $8W_S^2$, $8W_St_S$ and $8\lceil t_S/2\rceil^2$ look expensive, one staircase per set. We show that their sums over $S$ are functions of a few global forms, so they cost $O(n)$ gates in total. With $|x|_\ast=\sum_{c\ne0}x_c$ and $\sigma=\sum_is_i$,
$$\sum_{S\ne\varnothing}Y_S^2=\tfrac N4\bigl(|x|_\ast^2+|x|_\ast\bigr),\qquad \sum_{S\ne\varnothing}Y_St_S=\tfrac N4\Bigl(\sigma|x|_\ast+\sum_ix_{e_i}s_i\Bigr).$$
All quadratic leftovers together become $\tfrac N2\bigl(w^2+\sum_is_i^2\bigr)+2N(1+\alpha)\sum_ix_{e_i}s_i$ plus affine terms, where $w=2|x|_\ast+2\alpha\sum_ix_{e_i}+\sigma$. Each square is one staircase over a single form. Each product $x_{e_i}s_i$ is $\sum_{\ell\le m}[\,s_i+Bx_{e_i}\ge B+\ell\,]$ with $B=n+2$: the large weight $B$ lets the bit $x_{e_i}$ switch these gates on. In total this costs $O(n)$ gates. The sum $\sum_S8\lceil t_S/2\rceil^2$ collapses the same way, apart from a residue at the addresses $e_i$ (see 2.3).

### 2.3 Repairing $k+1$ special addresses

*Plan.* The *score* $P$ is the weighted sum at the top gate, and the circuit outputs $[-P\ge0]$. An address is *ordinary* if it is neither $0$ nor one of $e_1,\dots,e_k$. At ordinary addresses the collapsed score is already $N(1-2x_b)$. At the $k+1$ special addresses we need only the right sign, with *margin* $|P|\ge N$. We add a large correction switched on by $x_0$ at $b=0$, and we amplify $x_{e_i}$ so that it outweighs the residue at $b=e_i$.

- **$b=0$.** No $Y_S$ contains $x_0$, so the score never sees $x_0$. At $b=0$ the score is $N(w+2)$, where $w$ (from Saving 3) lies in $[0,R]$ with $R=2(N-1)+2\alpha k+km$. Subtract $Cx_0[b=0]$ with $C=N(R+4)$. This uses the identity
  $$x_0[b=0]=x_0-x_0\sigma+\tfrac4N\sum_{S\ne\varnothing}x_0\lfloor t_S/2\rfloor,$$
  realized with the gates $[\,t_S+Bx_0\ge B+2r\,]$ for $r\le\lfloor|S|m/2\rfloor$ and $[\,\sigma+Bx_0\ge B+\ell\,]$ for $\ell\le km$. This costs about $|S|m/2$ gates per set.
- **$b=e_i$.** Here the collapse of $\sum_S8\lceil t_S/2\rceil^2$ leaves $-Ns_i$, where $s_i$ is odd with $1\le s_i\le2\alpha+1$ (for the largest odd value $\le m$). Two steps handle it.
  - *Shift (free).* The function $\lceil(2W_S+t_S)/2\rceil=W_S+t_S/2+\tfrac14-\tfrac14(-1)^{t_S}$ is the sum of the odd-threshold gates of $S$. Shifting their coefficients therefore adds any function of $b$. The shift $\kappa_S=-4(2\alpha+1)(k-2|S|)$ adds $N(2\alpha+1)$ at each $e_i$.
  - *Amplification (costs about $\tfrac14N^2$).* Using $W_S$ instead of $Y_S$ raises the weight of $x_{e_i}$ from $2N$ to $2N(1+\alpha)$.

After these repairs the score has the closed form
$$P=\begin{cases}N(w+2)-Cx_0,&b=0,\\ 2N(1+\alpha)(1-x_{e_i})-Ns_i,&b=e_i,\\ N(1-2x_b),&\text{otherwise.}\end{cases}$$
In every case $P\ge N$ if $x_b=0$ and $P\le-N$ if $x_b=1$.

### 2.4 The count

Per nonempty $S$ the circuit uses:

| Part | Gates per $S$ | Total, balanced, in units of $N^2$ |
|---|---|---|
| Main staircase, range of $2Y_S$ (odd thresholds) | $\approx N/2$ | $\tfrac12$ |
| Main staircase, range of $t_S$ | $\approx \lvert S\rvert m/2$ | $\tfrac14$ |
| Main staircase, amplification | $\alpha\lvert S\rvert$ | $\tfrac14$ |
| Correction at $b=0$ | $\approx \lvert S\rvert m/2$ | $\tfrac14$ |
| Collapsed leftovers | $O(n)$ in total | $0$ |

Using $\sum_S|S|=kN/2$, $km=N$ and $\alpha\approx m/2$, the rows add up to $(\tfrac12+\tfrac14+\tfrac14+\tfrac14)N^2=\tfrac54N^2=\tfrac5{16}n^2$. The number of bottom gates is at most
$$\frac{N(N-1)}2+\frac{kN(m+\alpha)}2+2(N-1)+2\alpha k+3km+\Big\lceil\frac{km}2\Big\rceil .$$
The lower-order terms are $R$ gates for $w^2$, $km$ for the squares $s_i^2$, $km$ for the products $x_{e_i}s_i$, and $\lceil km/2\rceil$ for the $x_0\sigma$ gates not shared with $S=\{1,\dots,k\}$. A few coefficients can vanish; for example, $k=m=4$ needs 370 gates instead of 374. At exact balance the total, top gate included, is $\tfrac5{16}n^2-\tfrac n4\log_2(n/2)+O(n)$. All weights are integers: bottom coefficients and thresholds are $O(n)$, and the largest top coefficient is $C\approx n^2$.

**Verification.** A script writes every gate as a weight vector on the table bits and the block counts and checks the score exactly. It covers all tables and all block counts for $k\le3$, $m\le4$ (58264 cases), plus spot checks up to $k=8$, $m=32$. Every gate sees a block only through $s_i$, so checking all block counts covers all address assignments. An independent rebuild by the referee checked $k\le3$, $m\le6$ (202,780 cases) with margin exactly $N$.

**A structural remark.** Every bottom gate sees each block only through $s_i$, with a nonnegative coefficient. This matters for the lower bound below.

---

## 3. The lower bound for sign-coherent circuits

### 3.1 The class

A bottom gate is **sign-coherent** if its weights inside each address block are all $\ge0$ or all $\le0$. Different blocks and different gates may use different signs. The table weights and the top gate are arbitrary, and so are the magnitudes. Every gate of the $\tfrac5{16}$ circuit is sign-coherent, and so is every gate that sees a block only through $s_i$, or that is monotone in the address bits.

**Theorem.** Let a depth-two threshold circuit compute $A$ exactly, and let all of its $G$ bottom gates be sign-coherent. Then
$$G\ \ge\ \frac{m^k}{m^k-(m-1)^k}\,D_0\ \ge\ \frac mk\,D_0,\qquad D_0=\frac{\max\{0,\;N-k-1-\log_2(G+1)\}}{k+\log_2(G+1)} .$$
In the balanced case this gives $G\ge N(N-3k-1)/(3k^3)=\Omega(n^2/\log^3n)$. The same order holds for $m=\lfloor N/k\rfloor$.

### 3.2 The idea in one paragraph

Walk over the grid $\{0,\dots,m\}^k$ of block counts, one unit cube at a time. On every cube the circuit reveals the entire table. Each gate that is non-constant on the cube carries only about $k+\log_2G\le3k$ bits, so about $N/(3k)$ gates must be non-constant there. On the other hand, a sign-coherent gate is non-constant on at most a $k/m$ fraction of the cubes. So $G\cdot k/m\gtrsim N/(3k)$, i.e. $G\gtrsim N^2/(3k^3)$ at balance.

### 3.3 The cube restriction

Fix an order of the positions in each block. For $s\in\{0,\dots,m\}^k$, let $a(s)$ put the ones of block $i$ on its first $s_i$ positions. A *cube* is a point $q\in\{0,\dots,m-1\}^k$. Its corners are the inputs $(x,a(q+z))$ for $z\in\{0,1\}^k$. Moving from corner $q$ to corner $q+z$ flips exactly one bit in each block $i$ with $z_i=1$, namely the bit at position $q_i+1$. Call it the *live* bit of block $i$. All other address bits are the same at every corner. The address at corner $q+z$ is $(q\bmod2)\oplus z$, so
$$z\ \mapsto\ A(x,a(q+z))=x_{(q\bmod2)\oplus z}.$$
This is the whole table, permuted. A gate *splits* a cube if it is non-constant on its corners. Let $d_q(x)$ be the number of bottom gates that split cube $q$ for table $x$.

Compare Kane–Williams' random restriction. They fix the non-live bits at random, which spreads the fixed part of a gate's sum over about $\sqrt m$ values per block, so a gate survives with probability $O(\sqrt{k/m})$. The cube walk moves each block count through all of $0,\dots,m-1$. A sign-coherent gate's sum then moves monotonically, and it splits at most a $k/m$ fraction of the cubes. A mixed-sign gate can split every cube.

### 3.4 Step 1: many gates split each cube (any circuit)

**Lemma.** For every circuit with $G$ bottom gates, every cube $q$, and a uniformly random table $x$: $\mathbb E_x[d_q(x)]\ge D_0$.

*Plan.* We describe $x$ by a short code read off the circuit on the cube $q$. The code must carry all $N$ bits of $x$, but each splitting gate adds only about $k+\log_2G$ bits. So on average many gates must split.

*Why.* On the corners of $q$, bottom gate $j$ computes $[\lambda_j\cdot z\ge\tau_j]$. The live weights $\lambda_j\in\mathbb R^k$ are fixed by the circuit; only the threshold $\tau_j$ depends on $x$. The same holds for the top gate: its weights on the bottom gates and on the live bits are fixed. All non-splitting gates are constant on the cube, so they fold into the top threshold, which is the only other part that depends on $x$.

Hence the restricted function, and therefore $x$, is determined by:

- the number $D=d_q(x)$ of splitting gates: at most $G+1$ choices;
- which gates split: at most $\binom{G}{D}$ choices;
- for each splitting gate, which of at most $2^k-1$ non-constant threshold functions it is (only the position of $\tau_j$ among the at most $2^k$ values $\lambda_j\cdot z$ matters);
- the position of the top threshold: at most $2^k+1$ choices.

Let $H(x)$ be the Shannon entropy of $x$; for a uniform table $H(x)=N$. By the chain rule for entropy, with $\log_2\binom GD\le D\log_2G$, $\log_2(2^k-1)\le k$ and $\log_2(2^k+1)\le k+1$,
$$N\le\log_2(G+1)+\mathbb E[D]\,(\log_2G+k)+k+1 .$$
Rearranging gives the lemma.

### 3.5 Step 2: a sign-coherent gate splits few cubes

**Lemma.** For every table, a sign-coherent gate splits at most $m^k-(m-1)^k\le km^{k-1}$ cubes.

*Plan.* Walk through the cubes along a line in the gate's monotone direction. The gate's sum never decreases along the line, so its threshold is crossed in at most one cube of the line. Then count the lines.

*Why.* Let $\varepsilon_i=+1$ if the gate's weights in block $i$ are $\ge0$, and $\varepsilon_i=-1$ otherwise. Let $F(s)$ be the gate's weighted sum on the input $(x,a(s))$. It is a constant plus $\sum_iF_i(s_i)$, where $F_i(s_i)$ adds the weights on the first $s_i$ positions of block $i$. Because these weights share a sign, $F$ never decreases when $s$ moves one step in direction $\varepsilon$.

On the cube $q$, $F$ is smallest at the corner $q^-=q+(\mathbf1-\varepsilon)/2$ and largest at $q^+=q+(\mathbf1+\varepsilon)/2$. The gate splits $q$ exactly when its threshold lies in the interval $(F(q^-),F(q^+)]$. Now take a *line* of cubes $q,\ q+\varepsilon,\ q+2\varepsilon,\dots$. Since $q^+=(q+\varepsilon)^-$, the intervals along a line are consecutive and disjoint, and the threshold lies in at most one of them.

Every cube lies on exactly one line. A line starts at a cube $q$ for which $q-\varepsilon$ is not a cube, and exactly $(m-1)^k$ cubes are not starting points. So there are $m^k-(m-1)^k$ lines and at most that many split cubes.

The bound is tight: a gate with one positive weight on the last position of each block, and threshold equal to that weight, splits exactly the $m^k-(m-1)^k$ cubes with some $q_i=m-1$. The underlying fact is classical: a function that is monotone or antitone in each input bit changes value at most once along a chain compatible with its orientation (Impagliazzo, Paturi and Saks 1997, Lemma 2.1). The cube restriction and the resulting quadratic bound appear to be new; our literature search was limited.

### 3.6 Step 3: combine

If $G\ge N^2$ there is nothing to prove. Otherwise, summing Step 1 over all $m^k$ cubes and comparing with Step 2 gives
$$m^kD_0\ \le\ \sum_q\mathbb E[d_q]\ \le\ G\,(m^k-(m-1)^k).$$
With $1-(1-1/m)^k\le k/m$ this gives $G\ge(m/k)D_0$. Since $G<N^2$, $\log_2(G+1)\le 2k$ and $D_0\ge(N-3k-1)/(3k)$. In the balanced case $m=N/k$.

### 3.7 What it means and what it does not

- **Matching up to polylog.** The $\tfrac5{16}n^2$ circuit is sign-coherent, so within this class it is optimal up to a $\log^3 n$ factor.
- **Where the gap is.** For general gates the best lower bound is still $\Omega(n^{3/2}/\log^2n)$. Only circuits with mixed-sign bottom gates can beat $n^2$ by more than a polylogarithmic factor.
- **Why restriction arguments stop at $n^{3/2}$ for general gates.** Take a gate with threshold $0$ and independent uniform signs on all $km$ address bits. Under every restriction that leaves one live bit per block, it is non-constant with probability at least $1/(2\sqrt{2km})$. A restricted circuit never needs more than $N$ surviving gates, because the restricted function is an OR of $N$ ANDs. So survivor counting proves at most $N\cdot2\sqrt{2km}=O(n^{3/2})$, even for depth-two circuits of majority gates.
- **Limits of the method.** The $\tfrac5{16}$ circuit itself has only $O(kN)$ gates splitting each cube: on one cube, the staircase of $S$ crosses only about $|S|/2$ of its thresholds. So Step 1 can never certify more than $O(kN)$ per cube. Step 2 is tight, so this method cannot prove more than about $\tfrac mk\cdot O(kN)=O(mN)=O(n^2/\log n)$. A $\Theta(n^2)$ bound needs a different argument, for example one that does not bound each gate's split cubes separately.
- **Asymptotic only.** The bound beats $n^{3/2}$ itself only from about $k=38$, i.e. $n\approx2^{38}$ (and from $k=64$ at exact balance).
- **Status.** The proof was checked by an independent referee and by brute force on small cases. It is not yet formalized in Lean.

---

## 4. Summary

| Circuits for Andreev's function | Lower bound | Upper bound |
|---|---|---|
| General depth-two threshold | $\Omega(n^{3/2}/\log^2n)$ | $(\tfrac5{16}+o(1))n^2$ |
| Sign-coherent bottom gates | $\Omega(n^2/\log^3n)$ | $(\tfrac5{16}+o(1))n^2$ |

The upper bound gets its constant from three things: a Fourier score over a half-range table count, staircases that need only odd thresholds, and quadratic leftovers that collapse when summed over all sets $S$. The lower bound gets its exponent from walking over every cube of the block-count grid instead of a random one. That walk is exactly what sign-coherent gates cannot survive cheaply.
