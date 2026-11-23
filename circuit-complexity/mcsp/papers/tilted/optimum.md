# The sharp coefficient of the tilted gate-elimination inequality

Write $N=2^n$. At the fixed inner threshold $\lfloor0.99435N/n\rfloor$, the tilted gate-elimination theorem gives a lower bound of **more than $2.52286N$ gates** for deterministic full-binary-basis circuits deciding MCSP, for all sufficiently large $n$. The manuscript reports $2.5226N$ at this threshold. Optimizing over thresholds as well gives an exact limiting coefficient between $2.5229339$ and $2.5229340$. A single fixed threshold realizes this limit. [Tilted theorem and its proof](main.tex)

## Optimizing over thresholds

Let $p$ be the probability of the stronger ordinary elimination branch and $q$ the probability of the common output of a private gate. The theorem assumes $1/2<p<1$ and $3/4\le q<1$. Put

$$
d(p)=1-H_2(p),\qquad D(q)=q\log_2(4q/3)+(1-q)\log_2(4(1-q)).
$$

For thresholds $\lfloor(1-a)N/n\rfloor$ and $\lfloor(1-b)N/n\rfloor$, with $0<b\le a<1$, the theorem certifies $(G-o(1))N$ gates whenever

$$
\kappa=d+(D-2d)_+a/q<b,\qquad
G=2+p-a\max\{3+p,(2+2p)/q\}.
$$

Since $d+(D-2d)a/q\le\kappa<a$, we have $q-D+2d>0$ and $a/q>d/(q-D+2d)$. Keeping just the second term in the maximum gives

$$
G < 2+p-\frac{(2+2p)d}{q-D+2d}
    \le 1+\frac{(1+p)L}{L+2d}=:\Phi(p),
\qquad L=\log_2(7/4).
$$

The last step uses $q-D(q)\le L$. Indeed, $q-D(q)$ is strictly concave and has derivative $1-\log_2(q/(3(1-q)))$, vanishing at $q_*=6/7$, where its value is $L$.

The derivative of $\Phi$ has the sign of $L+2d-2(1+p)d'$. Using $(1+p)d'-d=\log_2(p/(1-p)^2)-1$, the unique maximum occurs at the root $p_*\in(1/2,1)$ of

$$
\frac{p_*}{(1-p_*)^2}=\sqrt{7}.
$$

The left side increases from $2$ to infinity. Define

$$
a_*=\frac{q_*d(p_*)}{L+2d(p_*)},\qquad G_*=\Phi(p_*).
$$

**Sharpness at a fixed threshold.** Hold $a=b=a_*$ and $q=q_*$. The private-gate term $(2+2p_*)/q_*$ strictly exceeds $3+p_*$ since $p_*>1/2$. Also $D(q_*)>2d(p_*)$, as verified by the rational bounds below. At $p=p_*$ we have $\kappa=a_*$ and the gate expression equals $G_*$. To meet the strict entropy condition, take any $p<p_*$ sufficiently close to $p_*$. The changing part of $\kappa$ is $(1-2a_*/q_*)d(p)$, with strictly positive coefficient $L/(L+2d(p_*))$. Hence $\kappa<a_*$ and the feasible gate coefficients approach $G_*$. Taking a lower limit in $n$ first gives

$$
\liminf_{n\to\infty}
\frac{C_{B_2}\bigl(\mathrm{MCSP}[\lfloor(1-a_*)N/n\rfloor]\bigr)}{N}\ \ge G_*.
$$

Here $C_{B_2}$ counts outer gates with unrestricted fanout. Numerically $1-a_*\approx0.99365943$ and $G_*\approx2.52293396$. Every feasible parameter choice in the theorem, including choices for a gap promise, gives $G<G_*$. Improving on this ceiling requires a stronger inequality.

## Certified bounds at specific thresholds

Each row uses exact rational parameters. The first row uses the manuscript's exact threshold, the second its gap, and the fourth a threshold near the optimum. The third retains the manuscript's pointwise error exponent at the original exact threshold, using the condition $e>\kappa$ for error at most $2^{-eN}$. [Confidence extension](confidence.tex)

| $a$ | $b$ | $p$ | $q$ | $\kappa$ strictly below | Gates strictly above, for large $n$ |
| --- | --- | --- | --- | --- | --- |
| .00565 | .00565 | .543317 | .8526 | .0056497 | $2.52286N$ |
| .007 | .00565 | .543101 | .8523 | .0056490 | $2.51775N$ |
| .00565 | .00565 | .543275 | .8525 | .0056390 | $2.52281N$ at $e=.00564$ |
| .00635 | .00635 | .545836 | $6/7$ | .0063495 | $2.52293N$ |

All four gate expressions have strict rational slack to absorb the $o(1)$ term. To check the entropy margins, enclose $\ln x$ using the first 16 terms of its series in $y=(x-1)/(x+1)$, with remainder at most $2|y|^{33}/(33(1-y^2))$. The same bounds applied on a rational bracket for $p_*$ give $2.5229339<G_*<2.5229340$. The checker verifies all displayed strict bounds with rational arithmetic. [Numerical certificate](check_optimum.py)
