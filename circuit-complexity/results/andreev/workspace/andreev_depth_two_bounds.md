# Depth-two threshold complexity of Andreev's function: a quadratic upper bound and tight average-case bounds

This note improves two results of Kane and Williams, *Super-Linear Gate and Super-Quadratic Wire Lower Bounds for Depth-Two and Depth-Three Threshold Circuits* (arXiv:1511.07860).

| Quantity | Kane–Williams | This note |
|---|---|---|
| Exact computation, gates | $O(n^3/\log n)$ | $(5/4+o(1))\,n^2$ (Theorem 1) |
| Agreement $1-\delta$, gates | no separate bound | $O(n^{3/2}\sqrt{\log(n/\delta)})$ (Theorem 2) |
| Agreement $\tfrac12+\varepsilon$, gates, upper bound | no separate bound | $O(\varepsilon^2 n^{3/2}\sqrt{\log n})$ (Theorem 2) |
| Agreement $\tfrac12+\varepsilon$, gates, lower bound | $\Omega(\varepsilon^3 n^{3/2}/\log^3 n)$ | $\Omega(\varepsilon^2 n^{3/2}/\log^3 n)$ (Theorem 3) |
| Agreement $\tfrac12+\varepsilon$, wires, upper bound | no separate bound | $O(\varepsilon^2 n^{5/2}\sqrt{\log n})$ (Theorem 2) |
| Agreement $\tfrac12+\varepsilon$, wires, lower bound | $\Omega(\varepsilon^3 n^{5/2}/\log^{7/2} n)$ | $\Omega(\varepsilon^2 n^{5/2}/\log^{7/2} n)$ (Theorem 3) |

So the average-case gate complexity is $\tilde\Theta(\varepsilon^2 n^{3/2})$ and the wire complexity is $\tilde\Theta(\varepsilon^2 n^{5/2})$, for all $C\log n/\sqrt n\le\varepsilon\le\tfrac12-1/\mathrm{poly}(n)$. The gaps are $O(\log^{7/2}n)$ for gates and $O(\log^4 n)$ for wires.

The worst case remains open: exact computation lies between $\tilde\Omega(n^{3/2})$ and $O(n^2)$. By Theorem 2(a), a size-$s$ circuit with $s\gg n^{3/2}\sqrt{\log n}$ errs on a set of density at most $\exp(-\Theta(s^2/n^3))$, so a worst-case lower bound of $s$ must be witnessed on a set that small: density $n^{-\omega(1)}$ just above $n^{3/2}\sqrt{\log n}$, $2^{-\Theta(n^{1-2\gamma})}$ at $s=n^{2-\gamma}$, and $2^{-\tilde\Omega(n)}$ only at $s=n^2/\mathrm{polylog}(n)$.

## 0. Setup

Let $N=2^k$, $m=N/k$, and $n=2N$ (the total input length). The input is $x\in\{0,1\}^N$, indexed by $c\in\mathbb F_2^k$, together with $a=(a_{i,j})_{i\in[k],\,j\in[m]}$. Define

$$s_i=\sum_j a_{i,j},\qquad b_i=s_i\bmod 2,\qquad A_n(x,a)=x_b.$$

As in the paper, $k$ is taken to be a power of two so that $k$ divides $2^k$; the results are stated for those $n$. The circuits below work for any block size $m\ge1$; only the gate counts use $km=N$.

Write $\xi_c=(-1)^{x_c}$. For $S\subseteq[k]$ define

$$X_S=\sum_{c}(-1)^{\sum_{i\in S}c_i}\,\xi_c,\qquad t_S=\sum_{i\in S}s_i.$$

Both are integer linear forms in the input:

- $X_S=\sum_c\pm(1-2x_c)$, with $|X_S|\le N$, and $X_S$ is always even (a sum of an even number of $\pm1$ values, for $k\ge1$).
- $0\le t_S\le|S|m$.

**Fourier inversion.** Since $(-1)^{\sum_{i\in S}b_i}=(-1)^{t_S}$, inversion on $\mathbb F_2^k$ gives

$$N\,\xi_b=\sum_{S\subseteq[k]}X_S\,(-1)^{t_S}.\tag{1}$$

The Kane–Williams circuit treats the $\Theta(n^2/\log n)$ parities arising from the Fourier expansion separately, at $O(n)$ gates each. The next lemma instead handles all $N$ coefficients of one $X_S$ with a single $O(N)$-gate block.

**Lemma 1 (linearising the product).** Let $\varphi(u)=(-1)^u u$ and $u_S^{\pm}=X_S\pm t_S$. Then

$$2X_S(-1)^{t_S}=\varphi(u_S^+)+\varphi(u_S^-).$$

*Proof.* $X_S$ is even, so $(-1)^{u_S^\pm}=(-1)^{t_S}$. Also $u_S^++u_S^-=2X_S$. $\square$

So a product of two linear forms, each with $\Theta(N)$ possible values, is a sum of two functions of a single linear form. Each of those has $O(N)$ values instead of $\Theta(N^2)$.

**Lemma 2 (ramps).** Let $u$ be an integer linear form and $\ell<h$ integers. Then for $g:\mathbb Z\to\mathbb R$,

$$g(\operatorname{clamp}(u,\ell,h))=g(\ell)+\sum_{\theta=\ell+1}^{h}\bigl(g(\theta)-g(\theta-1)\bigr)\,[u\ge\theta],$$

which uses $h-\ell$ threshold gates. $\square$

## 1. Quadratic upper bound

**Theorem 1.** $A_n$ has a $\mathrm{THR}\circ\mathrm{THR}$ circuit with $4N^2+kmN=5N^2=\tfrac54n^2$ bottom gates, bottom weights in $\{0,\pm1,\pm2\}$, integer top weights of magnitude $O(n)$, and a top threshold of magnitude $O(n^2)$. It therefore has $O(n^3)$ wires.

*Proof.* By (1) and Lemma 1,

$$2N\,\xi_b=\sum_{S}\bigl(\varphi(u_S^+)+\varphi(u_S^-)\bigr).$$

Each $u_S^\pm$ lies in an interval of length $2N+|S|m$, so Lemma 2 uses $2N+|S|m$ gates per sign. The jumps are $\varphi(\theta)-\varphi(\theta-1)=\pm(2\theta-1)$, of magnitude $O(N)$. The total is

$$\sum_S 2(2N+|S|m)=4N^2+2m\cdot\frac{kN}{2}=4N^2+kmN.$$

The top gate outputs 1 exactly when the sum is negative. $\square$

## 2. Average-case upper bound

Hoeffding's inequality shows that for random inputs each $u_S^\pm$ stays within $O(\sqrt{N\log N})$ of a known centre, so only that many gates per form are needed. Using only $S\subseteq[r]$ trades accuracy for size.

Fix $0\le r\le k$ and $\delta\in(0,1)$, and set $t=2^r$, $L=N/t$. Let

$$G=\sum_{S\subseteq[r]}X_S(-1)^{t_S}.$$

**Lemma 3.** $G=t\sum_{c\in Q(b)}\xi_c$, where $Q(b)=\{c: c_i=b_i\ \forall i\le r\}$ has size $L$.

*Proof.* Substitute the definition of $X_S$ and use $\sum_{S\subseteq[r]}(-1)^{\sum_{i\in S}(b_i+c_i)}=t\cdot\mathbf 1[c\in Q(b)]$. $\square$

So $G$ computes the majority of $x$ on the subcube fixed by the first $r$ address bits.

**Lemma 4.** Let $O=+1$ if $G\ge0$ and $O=-1$ otherwise. For uniform inputs, $\mathbb E[\xi_b\,O]=p(L)$, where $p(1)=1$ and for even $L$,

$$p(L)=\binom{L-1}{L/2}2^{-(L-1)}\ge\frac1{\sqrt{2L}}.$$

*Proof.* The case $L=1$ is immediate from (1). For even $L$, let $R=\sum_{c\in Q(b)\setminus\{b\}}\xi_c$, a sum of the odd number $L-1$ of signs. Given $a$, the sign $\xi_b$ is uniform and independent of $R$, and $G/t=\xi_b+R$.

- If $R\ge1$ then $O=+1$ whatever $\xi_b$ is, contributing 0.
- If $R\le-3$ then $O=-1$ whatever $\xi_b$ is, contributing 0.
- If $R=-1$ then $G/t\in\{0,-2\}$ and $O=\xi_b$, contributing 1.

So the correlation is $\Pr[R=-1]$. With $q=L/2$, this equals $\binom{2q}{q}4^{-q}\ge\frac1{2\sqrt q}=\frac1{\sqrt{2L}}$. $\square$

**Theorem 2.** Let $\lambda=\sqrt{2N\ln(4t/\delta)}$. There is a $\mathrm{THR}\circ\mathrm{THR}$ circuit with at most $4t(\lceil2\lambda\rceil+1)$ gates, each of fan-in at most $n$, that agrees with $A_n$ on at least a $\tfrac12+\tfrac12p(N/t)-\delta$ fraction of inputs. Consequently:

- (a) Taking $t=N$: agreement $1-\delta$ with $O(\min\{n^2,\ n^{3/2}\sqrt{\log(n/\delta)}\})$ gates.
- (b) For every $\varepsilon\in[1/\sqrt N,\,1/2)$ with $\tfrac12-\varepsilon\ge1/\mathrm{poly}(n)$: agreement $\tfrac12+\varepsilon$ with $O(\varepsilon^2n^{3/2}\sqrt{\log n})$ gates and $O(\varepsilon^2n^{5/2}\sqrt{\log n})$ wires.

*Proof.* For each $S\subseteq[r]$, Hoeffding gives (trivially for $t_\emptyset=0$)

$$\Pr[|X_S|>\lambda]\le2e^{-\lambda^2/2N}=\frac{\delta}{2t},$$

$$\Pr\bigl[|t_S-|S|m/2|>\lambda\bigr]\le2e^{-2\lambda^2/(|S|m)}\le\frac{\delta}{2t},$$

using $|S|m\le N$. By a union bound over the $2t$ events, with probability at least $1-\delta$ all of them fail to occur, and then every $u_S^\pm$ is within $\lceil2\lambda\rceil+1$ of the integer centre $\pm\lfloor|S|m/2\rfloor$.

Apply Lemma 2 on those windows, with $2(\lceil2\lambda\rceil+1)$ gates per form. On this good event the circuit's sum equals $2G$ exactly, so its output differs from $O$ only on a $\delta$ fraction of inputs. Lemma 4 finishes the main claim.

(a) Here $p(1)=1$. The $n^2$ term is Theorem 1.

(b) If $\varepsilon\le1/\sqrt{32}$, take $\delta=\varepsilon$ and let $t$ be the least power of 2 with $t\ge32\varepsilon^2N$. Then $1\le t<64\varepsilon^2N$ and $\tfrac12p(N/t)\ge\tfrac12\sqrt{t/(2N)}\ge2\varepsilon$, so agreement is at least $\tfrac12+\varepsilon$. Since $\varepsilon\ge N^{-1/2}$, we have $\log(4t/\delta)=O(\log n)$. If $\varepsilon>1/\sqrt{32}$, use (a) with $\delta=\tfrac12-\varepsilon$. $\square$

## 3. Average-case lower bound

Kane and Williams apply Markov's inequality to the number of surviving gates, losing a factor of $\varepsilon$. This proof avoids that loss in two linked steps: Lemma 5 bounds correlation uniformly at every survivor count $q$, which is needed because $q$ depends on $(x,\rho)$, and Jensen's inequality then applies because that bound is concave in $q$.

**Counting class.** For $q\ge0$, let $\mathcal H_q$ be the set of functions $\{0,1\}^k\to\{0,1\}$ of the form $\mathrm{THR}(g_1,\dots,g_q,z_1,\dots,z_k)$ with each $g_i$ an LTF. There are $2^{O(k^2)}$ LTFs on $k$ bits, and at most $(2^k+1)^{q+k+1}$ threshold functions over any $q+k$ fixed functions (Roychowdhury–Orlitsky–Siu; Theorem 2.3 of the paper, label `number-ckts`). So $\log_2|\mathcal H_q|\le c_0k^2(q+1)$. Also, $\mathcal H_q$ is closed under $z\mapsto z\oplus c$.

**Lemma 5.** There is a constant $c_1$ such that all but a $2^{-k^2}$ fraction of $x\in\{0,1\}^N$ satisfy, for all $q\ge0$ and all $h\in\mathcal H_q$,

$$\bigl|\mathbb E_z[(-1)^{x_z+h(z)}]\bigr|\le c_1k\sqrt{(q+1)/N}.$$

*Proof.* For fixed $h$, Hoeffding bounds the failure probability at level $\lambda$ by $2e^{-\lambda^2N/2}$. Choose $c_1$ so that this is at most $2^{-(c_0+2)k^2(q+1)}$ at $\lambda=c_1k\sqrt{(q+1)/N}$, and sum over $h\in\mathcal H_q$ and over $q$. $\square$

**Restriction lemmas (Kane–Williams, Lemmas `rr-LTF` and `wire-rr-Lem`).** Let $\rho$ leave one uniformly random variable free in each block of $a$ and set the other $a$-variables uniformly. For any LTF on the $a$-variables that depends on $u$ of them:

- it is not forced to a constant with probability $O(k/\sqrt N)$;
- it is not forced to a constant or a single literal with probability $O(uk^{3/2}/N^{3/2})$.

Fixing $x$ only shifts a gate's threshold, so these apply to every gate for every fixed $x$.

**Theorem 3.** There is a constant $C$ such that for every $\varepsilon\ge C\log n/\sqrt n$, every $\mathrm{THR}\circ\mathrm{THR}$ circuit agreeing with $A_n$ on a $\tfrac12+\varepsilon$ fraction of inputs has $\Omega(\varepsilon^2n^{3/2}/\log^3n)$ bottom gates and $\Omega(\varepsilon^2n^{5/2}/\log^{7/2}n)$ wires.

*Proof.* Let the circuit $D$ have $s$ bottom gates and $w$ wires. For fixed $x$ and $\rho$, let $q(x,\rho)$ be the number of bottom gates not forced to a constant or a literal. Constants fold into the top threshold and literals into the coefficients of $z_1,\dots,z_k$, as do any direct wires from inputs to the top gate, so the restricted circuit lies in $\mathcal H_{q(x,\rho)}$. The restriction lemmas give, for every $x$,

$$\mathbb E_\rho[q(x,\rho)]\le B:=c_2\min\{sk/\sqrt N,\ wk^{3/2}/N^{3/2}\}.$$

Restricted to $\rho$, $A_n$ becomes $z\mapsto x_{z\oplus c(\rho)}$. Sampling $(x,\rho,z)$ uniformly yields a uniform input. So, using shift-closure and Lemma 5, with correlation at most 1 on the bad $x$,

$$2\varepsilon\le2^{-k^2}+c_1k\,\mathbb E_{x,\rho}\sqrt{\frac{q(x,\rho)+1}{N}}\le2^{-k^2}+c_1k\sqrt{\frac{B+1}{N}},$$

where the last step is Jensen's inequality for the square root. For $\varepsilon\ge2c_1k/\sqrt N$ and $n$ large, this gives $B+1\ge\varepsilon^2N/(c_1k)^2\ge4$, hence $B=\Omega(\varepsilon^2N/k^2)$. Substituting the two terms of $B$ gives the two bounds. $\square$

The same averaging as in the paper's Corollary `apx-majority` improves the bounds for $\varepsilon$-approximate majorities of $\mathrm{THR}\circ\mathrm{THR}$ circuits from $\varepsilon^3$ to $\varepsilon^2$.

## 4. Remarks

**Range of $\varepsilon$.** Some cutoff is unavoidable: the single gate $\mathrm{Maj}(x)$ already achieves agreement $\tfrac12+\Theta(1/\sqrt n)$. Theorem 3 needs $\varepsilon\gtrsim\log n/\sqrt n$, while the paper states $\varepsilon\gg\sqrt{\log n/n}$. The difference comes from the $2^{\Theta(k^2)}$ LTFs on $k$ bits: the union bound behind the paper's Corollary `hardFunctionCor` cannot go below $k/\sqrt N$ once even one LTF is allowed. Between those two values the paper's gate bound is below one gate, so nothing is lost for gates. Its stated wire bound is nontrivial there, about $n/\log^2 n$ up to $n/\sqrt{\log n}$, but its own argument does not prove it, and Theorem 3 does not recover it. So the two wire statements are not comparable in that range.

**Errata in the source paper.** These do not affect the truth of the restriction lemmas, which were rechecked by hand with the repairs below.

- In the proof of Lemma `rr-LTF`, $k_i$ is defined as the number of $j$ with $|a_i|\ge|a_j|$. The proof needs the reverse, $|a_j|\ge|a_i|$, as the paper's own line `k_i >= k_j iff |a_i| <= |a_j|` confirms. The count $k'_i$ needs the same reversal.
- In the same proof, the second forcing condition should use $\ge$ rather than $>$, and indices with $a_i=0$ must be dropped, because the Littlewood–Offord lemma fails for an interval of length 0.
- In Lemma `wire-rr-Lem`, first remove the irrelevant variables, then apply the union bound to $B\cap S$ rather than $B$. Two of the displayed equalities should be $\le$.

**Verification.** `verify_construction.py` builds every gate as an explicit weight vector and threshold, so it evaluates the circuit and not identity (1).

- **Theorem 1.** The top sum equalled $2N\xi_b$ on every input tested, and the gate count equalled $4N^2+kmN$ exactly. Testing was exhaustive for all inputs up to 14 bits and used 400 random and extreme-weight inputs for sizes up to $k=6$, $m=4$ (88 input bits, 17,920 gates). At these sizes, it is a test and not a proof; the proof is above.
- **Theorem 2.** A separate high-precision run (400,000 samples at $k=6$, $r=1,2,3$; 120,000 at $k=8$, $r=2$) gave agreement within 0.8 standard errors of $\tfrac12+\tfrac12p(N/t)$ in every case. That run set $\delta=0.001$ and used windows one unit narrower than Theorem 2. The script's own run, with the theorem's windows, reached $k=10$ (74,240 gates, 4,000 samples), and at $k=8$, $t=N$ it agreed on all 4,000 samples.
- **Theorem 3.** A lower bound cannot be tested this way, so it rests on the proof alone. An independent referee pass checked all three theorems and found no errors in them; it did find errors in surrounding remarks, which are corrected here.
