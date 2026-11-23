# Applying the new techniques to the other results in Kane–Williams

Source: Kane–Williams, arXiv:1511.07860v1. Notation follows their paper.

Our techniques, as tools:

- **(T1) Uniform correlation + Jensen.** Bound the correlation of every circuit with $q$ survivors simultaneously for all $q$, then average with Jensen. This replaces Markov and gives $\varepsilon^2$ instead of $\varepsilon^3$. It is formalized in complexitylib (#2372).
- **(T2) Fixed-weight counting.** After a restriction $\rho$, a surviving gate keeps its original weights on the live variables, and only its threshold moves. The restricted circuits therefore lie in a class $H_\sigma$ that depends only on the free positions $\sigma$. Each gate costs $O(k+\log s)$ bits there, against $\Theta(k^2)$ for an arbitrary LTF. See `worst_case_notes.md`.
- **(T3) Parity trick and staircases.** $X(-1)^t=\varphi(X+t)-\varphi(t)$ for even $X$. This applies only to upper bounds.

## 1. Approximate-majority and TC0_3 lower bounds for Andreev's function (rigorous)

KW Corollary `apx-majority`: every $\varepsilon$-approximate majority of THR∘THR for $A_n$ needs $\Omega(\varepsilon^3 n^{3/2}/\log^3 n)$ gates and $\Omega(\varepsilon^3 n^{5/2}/\log^{7/2}n)$ wires.

**Improved statement.** It needs $\Omega(\varepsilon^2 n^{3/2}/\log^3 n)$ gates and $\Omega(\varepsilon^2 n^{5/2}/\log^{7/2}n)$ wires, for $\varepsilon\ge C\log n/\sqrt n$.

The proof is KW's averaging argument verbatim. Some single circuit in the collection agrees on a $1/2+\varepsilon$ fraction of inputs, and our $\varepsilon^2$ theorem applies to it.

**TC0_3 consequence.** Consider a MAJ∘MAJ∘MAJ circuit with $s$ gates and top fan-in $t$ computing $A_n$. On each input more than half of the $t$ subcircuits are correct. So some subcircuit has advantage $\ge 1/(2t)$, and therefore
$$s \ge c\,\frac{n^{3/2}}{t^2\log^3 n},\qquad\text{i.e.}\qquad t \ge \tilde\Omega\!\left(\frac{n^{3/4}}{\sqrt s}\right).$$
KW obtain $t\ge\tilde\Omega(n^{1/2}/s^{1/3})$. Their example "no $O(n^{1.1})$-gate TC0_3 circuit with top fan-in $o(n^{2/15})$" improves to top fan-in $o(n^{1/5}/\log^{3/2}n)$. In general, $s=n^{3/2-\delta}$ forces top fan-in $n^{\delta/2-o(1)}$, where KW get $n^{\delta/3}$.

For wires: $t\ge\tilde\Omega(n^{5/4}/\sqrt w)$.

## 2. The depth-three hard function $B_n$ (proof sketch; details to be checked)

KW Theorem `depth3lbThm`: MAJ∘THR∘THR needs $\Omega(n^{3/2}/\log^3 n)$ gates or $\Omega(n^{5/2}/\log^{7/2}n)$ wires to compute $B_n$.

**(a) Worst case, one log factor better.** MAJ∘THR∘THR needs $\Omega(n^{3/2}/\log^2 n)$ gates and $\Omega(n^{5/2}/\log^{5/2}n)$ wires.

KW first fix an $x$ that is bad for *all* small THR∘THR circuits (Corollary `badEntryCor`). Counting all such circuits forces $q=o(n/\log^2 n)$ survivors. We swap the quantifiers: fix the circuit $C$ first, then choose $x$.

1. For each $\sigma$ (free positions, with $(n/k)^k=2^{O(\log^2 n)}$ choices), let $H_\sigma$ be the THR functions over at most $Q$ fixed-weight shifts from $C$'s bottom gates plus the $k$ literals. Include also their $2^k$ input translates $z\mapsto h(z\oplus c)$, because the restricted function is $F(z\oplus c,x)$. Then
$$\log|H_\sigma|=O\bigl(Q(k+\log s)+k^2\bigr)=O(Q\log n+\log^2 n),$$
assuming $s\le n^2$; otherwise the bound is immediate.
2. By KW Lemma `uncorrAgreeLem` with Cor. `uncorrFunctCor` ($m=n^{16}$, $\epsilon'=n^{-7}$), each fixed $h$ has $|\text{agreement}-1/2|>n^{-3.5}$ with $F(\cdot,x)$ for only $O(n^7)$ strings $x$. Summing over $\sigma$, translates and $h$ gives at most $2^{O(Q\log n+\log^2 n)}$ bad $x$. This is $<2^{n-1}$ for $Q=cn/\log n$.
3. For *every* fixed $x$, the restriction lemmas give $\mathbb E_\rho[\#\text{survivors}]\le B=O(sk/\sqrt n)$ or $O(wk^{3/2}/n^{3/2})$. The randomness is over the $a$-part only, since $x$ merely shifts thresholds.
4. Choose a good $x$ and a $\rho$ with at most $2B$ survivors. If $2B\le Q$, every middle THR∘THR subcircuit lies in $H_\sigma$. So each has correlation at most $n^{-3.5}$, while the top majority needs correlation $\Omega(1/s)$. This is a contradiction.
5. Hence $sk/\sqrt n\gtrsim n/\log n$, i.e. $s\gtrsim n^{3/2}/\log^2 n$; and $wk^{3/2}/n^{3/2}\gtrsim n/\log n$, i.e. $w\gtrsim n^{5/2}/\log^{5/2}n$.

**(b) Average case against THR∘THR, linear in ε.** The same steps with $x$ uniformly random give, for every THR∘THR circuit with $s$ gates or $w$ wires,
$$\Pr_{x,a}[C=B_n]\le \tfrac12+O\!\left(\frac{s\log^2 n}{n^{3/2}}\right)+O(n^{-3}),
\qquad \tfrac12+O\!\left(\frac{w\log^{5/2} n}{n^{5/2}}\right)+O(n^{-3}).$$
The sum is over: the bad-$x$ probability, which is exponentially small; the correlation of $H_\sigma$ when $q\le Q$, at most $n^{-3.5}$; and Markov $\Pr[q>Q]\le B/Q$. Markov is harmless here because the class correlation is negligible.

Equivalently, agreement $1/2+\varepsilon$ needs $\Omega(\varepsilon n^{3/2}/\log^2 n)$ gates, for $\varepsilon\ge Cn^{-3}$. This is linear in $\varepsilon$, compared with $\varepsilon^2$ for $A_n$.

KW state no average-case bound for $B_n$. Their concluding remark says their approach cannot give correlation below $1/\sqrt n$ in general. Our bound is consistent with that: at $s\approx n$ it gives about $\log^2 n/\sqrt n$. It is new only in being stated, and in the $\log^2$ factor; the method is theirs plus (T2).

## 3. Answers to KW's open questions

- **Q1 ("asymptotically tight results for $A_n$").** The average-case complexity of $A_n$ against THR∘THR is $\tilde\Theta(\varepsilon^2 n^{3/2})$ gates and $\tilde\Theta(\varepsilon^2 n^{5/2})$ wires, for $C\log n/\sqrt n\le\varepsilon\le 1/2-1/\mathrm{poly}$. The worst case is between $n^{3/2}/\log^2 n$ and $\tfrac34 n^2$, using (T3) in the form $\varphi(X+t)-\varphi(t)$.
- **Q3 ("a concentration version of the restriction lemma").** For the correlation application, concentration is not needed. (T1) handles a random survivor count through uniform-in-$q$ bounds plus Jensen.

## 4. Areas with nothing new

- **PARITY approximation (KW Thm `parity-approx`).** For agreement $1/2+\varepsilon$, a window staircase gives $O(\varepsilon\sqrt n)$ gates. A matching lower bound would need a correlation bound for THR∘THR against parity on $\ell$ bits. We do not have one. Later work (Kabanets–Kane–Lu 2017, Chen–Santhanam–Srinivasan) already goes much further for parity.
- **MOD3∘MOD2, parity decision trees, the O(n) TC0_3 circuit.** (T3) gives no improvement.
- **IP2 in THR∘THR (Q2).** Our trick needs "linear form × character of a single linear form". IP2 is a product of many characters, so it does not apply.
