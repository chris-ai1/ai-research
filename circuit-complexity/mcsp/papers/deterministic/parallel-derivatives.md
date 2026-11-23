# Counting easy truth tables with prescribed parallel derivatives

Let $A_s$ be the set of truth tables of $n$-input Boolean functions with at most $s$ gates over the full binary basis. Constants and complemented wires are free. Write $N=2^n$, $T=s\log_2 s$, and assume $n=o(s)$ and $s=o(N/n)$. All logarithms below have base two.

Choose a nonzero address difference $v\in\mathbb F_2^n$. Take $r=\lfloor\alpha T\rfloor$ disjoint pairs $\{a_i,a_i+v\}$ for a fixed $0<\alpha<1$. Define

$$
K(b)=\bigl|\{f\in A_s: f(a_i)\oplus f(a_i+v)=b_i\text{ for every }i\}\bigr|,
\qquad E_k=\log\binom rk,\quad k=|b|.
$$

**Theorem.** Every sign word $b$ satisfies $\log K(b)\ge T-E_k-o(T)$, uniformly over the pairs and the word. For a uniformly chosen word of any specified weight $k$, including weights depending on $n$, $\log K(b)=T-E_k+o(T)$ in probability. In particular, both constant words retain $2^{T+o(T)}$ easy tables. Specifying all $r$ equalities, or all $r$ inequalities, can therefore cost only $o(T)$ bits of the logarithmic population.

## Constructing tables in each fiber

First suppose $v$ flips the first address bit. Write the pairs as $(0,y_i),(1,y_i)$ with distinct $y_i$. Let $h$ be an $(n-1)$-input function taking the specified values $b_i$ at $y_i$. If $k=0$ or $r$, choose $h$ constant. Otherwise Chashkin's weight-sensitive partial synthesis theorem gives a choice with

$$
C(h)\le (1+o(1))\,E_k/\log E_k+O(n).
$$

Here the domain size $r$ exceeds $n-1$ and even the least nonzero $E_k$ tends to infinity. The leading constant in the full binary basis is one. In our parameters this implies $C(h)\log s\le E_k+o(T)$. Indeed, when $E_k$ is a positive fraction of $T$, $\log E_k=(1+o(1))\log s$. When $E_k=o(T)$, the part with $E_k\le\sqrt T$ contributes $o(T)$ after multiplication by $\log s$, and otherwise $\log E_k\ge(\log T)/2$. Also $n\log s=o(T)$. These estimates apply along every sequence of weights. [A. V. Chashkin, On circuit complexity of partial Boolean functions, Theorem 6.1](https://library.keldysh.ru/mvk.asp?id=2024-152&lg=e)

For each $(n-1)$-input function $g$ form

$$
f(x,y)=g(y)\oplus (x\land h(y)).
$$

Every such $f$ has the prescribed derivatives, and its $x=0$ slice recovers $g$. For general $v$, choose a coordinate $j$ with $v_j=1$, put $x=a_j$ and use $y_\ell=a_\ell\oplus v_\ell a_j$ for $\ell\ne j$. This invertible change uses at most $n-1$ gates, shared by $g$ and $h$. Its $y$ values index the distinct pairs, so the same construction works in every direction.

Reserve $n-1$ gates for the change of variables and two for the displayed formula. The remaining budget $u=s-C(h)-(n-1)-2$ for $g$ is at least $(1-\alpha-o(1))s$. To count the choices, fix $\eta>0$ with $\eta<1$ and prescribe arbitrary labels on $D=\lfloor(1-\eta)u\log u\rfloor$ distinct $y$ values. There are enough addresses since $T=o(N)$, and $D\ge n-1$ eventually. Chashkin's theorem at the largest possible weight entropy gives an extension of cost at most $(1+o(1))D/\log D+O(n)\le u$ for each labeling. Distinct labelings produce distinct $g$. Letting $\eta$ tend to zero shows that the log count is at least $u\log u-o(T)$. Now $\log u=\log s+O(1)$, so the construction gives $\log K(b)\ge T-E_k-o(T)$.

For the upper estimate within a weight layer, the fibers are disjoint and the rooted circuit census gives $\log|A_s|\le T+o(T)$. A uniform weight-$k$ word therefore satisfies, for every fixed $\varepsilon>0$,

$$
\Pr\bigl[\log K(b)\ge T-E_k+\varepsilon T\bigr]
\le 2^{-\varepsilon T+o(T)}.
$$

Together with the uniform lower estimate this proves the theorem. [Rooted circuit census](main.tex)

## A sharp limit on the signed-merge estimate

A signed identification at a bottom gate can delete one gate on either sign and an additional gate on a favorable sign. At a leaf with $m$ free inputs and $K$ accepted tables, teaching a complementary pair gives the lower estimate $2m-2\log K-1$. Consider the estimate obtained from these two facts when the pairs are the parallel matching above and the favorable sign is $1$ throughout. For a word of weight $k$, the resulting expression is

$$
S(b)=r+k+2(N-r)-2\log K(b)-1.
$$

For every fixed $0<\alpha<1$ its optimal value is

$$
\max_b S(b)=2N-2T+2r\log(1+2^{-1/2})+o(T).
$$

Indeed, the theorem and $\log\binom rk\le rH_2(k/r)$ bound the maximum by $2N-2T+r\max_{0\le p\le1}(2H_2(p)+p-1)+o(T)$, where $H_2(p)=-p\log p-(1-p)\log(1-p)$ with the endpoint values defined by continuity. The maximizing $p$ is $\sqrt2/(1+\sqrt2)$, and the maximum is $2\log(1+2^{-1/2})$. Conversely, at $k=\lfloor pr\rfloor$ in that layer, some word has $K(b)\le |A_s|/\binom rk$. Substituting $\log\binom rk=rH_2(p)+o(T)$ proves the reverse bound. Interchanging zero and one gives the same result when equality is always favorable.

As $\alpha$ increases to one after taking the large-$n$ limit, the coefficient of the deficit below $2N$ approaches $2-2\log(1+2^{-1/2})=0.45689339\ldots$, precisely the coefficient of the signed-identification bound. Always choosing the two-gate sign instead gives $S(b)=2N-2T+o(T)$ here. An improvement using the actual circuit could still come from which pairs its gates expose, additional gate deletions, or shorter teaching sets inside a fiber. The extremum above concerns only the stated estimate for this matching. [Signed-identification lower bound and gate analysis](https://github.com/chris-ai1/ai-research/pull/12)
