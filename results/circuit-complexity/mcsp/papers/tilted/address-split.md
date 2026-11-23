# Splitting the addresses before solving the parity equations

Let $N=2^n$. At $s=\lfloor0.99325N/n\rfloor$, unrestricted deterministic full-binary-basis circuits deciding MCSP need **more than $2.52437N$ gates** for all sufficiently large $n$. The same holds at pointwise two-sided error $2^{-0.0074N}$. At $s=\lfloor0.99365N/n\rfloor$ the bound exceeds $2.52435N$. The constants follow from a construction that puts all nonliteral parity pivots in the second part of an address partition. A three-choice pair split between the two parts retains its full entropy.

## An address circuit for a path

Use the notation of the [private-pair proof](private-pairs.md). A path has $R=rN$ designated nonliteral parity pivots, $Y=yN$ disjoint pairs with three possible values each, and $hN$ free entries. Its other entries are fixed, including the entries of exceptional private pairs. The $R$ pivot equations are triangular in elimination order and can always be solved in reverse after the nonpivot values are chosen. Write $\ell=\log_2 3$ and $\alpha=\ell-1$.

**Witness bound.** For $0<\theta<1$, set $\tau=-\log_2\theta$ and $L=1+\alpha(1-\theta^2)$. Every such path contains a table with inner size at most

$$
[1-h-Ly+\tau r+o(1)]N/n.
$$

First construct a Boolean mask on the addresses. Require it to be one at every designated pivot. Divide the common pairs into groups of at most $\lceil\sqrt N\rceil$ pairs, filling all but the last group. For a group of $k$ pairs prescribe the number whose two mask bits are one to be a mode of $\operatorname{Bin}(k,\theta^2)$. Under independent Bernoulli-$\theta$ mask bits this event has probability at least $1/(k+1)$. The mask requirements have joint probability at least $\theta^R2^{-o(N)}$, since the pivots and pair groups are disjoint. A Bernoulli law is a mixture of uniform weight layers, so some layer has at least this fraction of admissible masks. Each group is a cell of size $o(N)$. The small-cell synthesis theorem gives a mask $M$ with $nC(M)\le\tau R+o(N)$. Its set $I$ of one entries contains all pivots, and the number $J$ of common pairs wholly in $I$ equals $\theta^2Y+o(N)$, since each mode is within one of its mean. [Small-cell synthesis](../witnesses/local.tex)

Write $A$ for the complement of $I$ for the next two paragraphs. First prescribe a table on $A$. A common pair wholly in $A$ retains its three choices. For a crossing pair, one value of its $A$-bit leaves the $I$-bit free and the other forces it. In groups of at most $\lceil\sqrt N\rceil$ crossing pairs prescribe the favorable value for the nearest integer to two thirds of each group's size, filling all but the last group. If $K$ pairs cross, the number of exterior patterns on their $A$-bits has logarithm $H_2(2/3)K-o(N)$, and each such pattern leaves $(2/3)K+o(N)$ interior bits free. Thus crossing pairs contribute $\ell K+o(N)$ bits of freedom over the two parts, since $H_2(2/3)+2/3=\ell$. All exterior constraints act in disjoint small cells. If they allow $T_A$ restrictions to $A$, a circuit producing one of them costs at most $(|A|-\log_2 T_A+o(N))/n$, by leaving the $I$ entries unrestricted in the small-cell theorem.

For each common pair wholly in $I$, choose an affine line through two of its three points. Holding the exterior table fixed, all remaining equations on $I$ are now affine. They are consistent because the nonliteral pivots lie in $I$ and solve the triangular equations for every choice of the other available entries. Write $d_I$ for the dimension of this interior solution space. It is independent of the chosen exterior pattern and of the line choices. The preceding count gives

$$
\log_2 T_A+d_I=hN+\ell Y-\alpha J+o(N).
$$

Impose the interior equations on a second address circuit, leaving its exterior unrestricted. Dense affine interpolation costs at most $(|I|-d_I+o(N))/n$ gates. The block interpolation bound is uniform up to an additive $o(N)/n$, including sublinear ranks by extending to a slowly vanishing rank fraction. A constant-size multiplexer selects the appropriate circuit using $M$. Adding the two circuit sizes, $C(M)$, and substituting the value of $J$ proves the witness bound. [Dense affine interpolation, Section 2](../affine/main.tex)

**Counting distinct tables.** If $c>1-h-Ly+\tau r$ by a fixed margin and $c\le1$, then the path contains at least

$$
2^{[c-1+h+\ell y-\tau r-o(1)]N}
$$

distinct tables of size at most $\lfloor cN/n\rfloor$. Two details are needed because each of the two address circuits is used on only part of the table.

* An extra $t_A$ bits of synthesis cost in the numerator produce $2^{t_A-o(N)}$ different exterior restrictions, up to $t_A=\log_2 T_A$. Group the exterior constraint cells into $o(N)$ groups each of size $o(N)$, including free sites. A group allowing $T$ local words can be partitioned into $2^j$ bins of size at least $T/2^{j+1}$ for $0\le j\le\lfloor\log_2 T\rfloor$. Distribute $t_A$ among the groups up to rounding losses of $o(N)$. Apply the witness theorem separately for each choice of bins. Different bin tuples give different exterior restrictions.
* On the interior, $t_I\le d_I$ additional independent tests give $2^{t_I}$ distinct restrictions by affine interpolation. For each of the $3^J$ choices of interior lines, split the available budget between $t_A$ and $t_I$. Every resulting table belongs to at most $2^J$ line choices, since each permitted pair lies on exactly two of the three lines. Dividing out this multiplicity recovers the factor $2^{\alpha J}$ in the count.

More explicitly, in units of bits the available additional budget is $cN-nC(M)-[N-\log_2 T_A-d_I]-o(N)$. It is positive by the fixed margin and at most $\log_2 T_A+d_I$. The final table count follows after adding $\alpha J$ to this budget and using the bound on $C(M)$.

## The outer gate bound

Use inner thresholds $\lfloor(1-a)N/n\rfloor,\lfloor(1-b)N/n\rfloor$ with $0<b\le a<1$. Choose ordinary and private branch probabilities $1/2<p<1$ and $3/4\le q<1$. Put

$$
A=3+p,\quad B=(2+2p)/q,\quad\gamma=1-p,\quad d=1-H_2(p),\quad
\kappa=d+\big(D_{\rm KL}(q\Vert3/4)-2d\big)_+a/q.
$$

The divergence is for Bernoulli distributions in bits. Assume $\kappa<b$, $B\le AL$ and $A\tau\le\gamma$. Then every deterministic full-binary-basis circuit for the promise has outer gate count

$$
\boxed{\,G/N\ge 2+p-(3+p)a-o(1).\,}
$$

Indeed, the tilted elimination gives a rejecting path before its private-step cutoff with $G/N\ge 2+p-Ah-By+\gamma r-o(1)$. By the witness bound this path has $h+Ly\le a+\tau r+o(1)$. The two hypotheses absorb the $y$- and $r$-terms. The stronger potential decrement for a nonliteral parity is essential to the second absorption. [Private-pair proof and Chen–Kabanets case counts](private-pairs.md) · [Original tilted proof](main.tex)

For a randomized circuit the same bound holds at pointwise error $2^{-eN}$ when

$$
e>\kappa+\tau a(B-A)_+/\gamma .
$$

To see this, fix a circuit a constant gate fraction below the claimed bound, independently of its labels. As in the confidence proof, take constants $a<a'<a''$ sufficiently close, with cutoff $\lceil a''N/q\rceil$. Typical tilted paths reaching the cutoff have $h+y\ge a'$. Before the cutoff the gate inequality applies. A typical path with $h+y<a'$ must have $h+Ly>a'+\tau r$, since the opposite inequality would contradict the gate margin for $a'$. It also has $\gamma r\le A(a'-a)+(B-A)_+a'+o(1)$, by the same gate inequality. [Change of measure and affine-line representation](confidence.tex)

On the paths with $h+y\ge a'$ the common dense affine law on easy tables supplies $(1-o(1))$ times their uniform mass. On the other good paths, apply the count above with $c=1-a$ and divide by the circuit census $2^{(1-a+o(1))N}$. The uniform law on easy tables then supplies at least $2^{-(\tau r+o(1))N}$ times the uniform mass of the path. Mix these two laws equally. The good paths together have uniform mass at least $2^{-(\kappa''+o(1))N}$, where $\kappa''$ uses $a''$ in the cutoff term. The uniform mass of required no inputs mislabeled one plus $2^{-(b-o(1))N}$ bounds the mass of good paths labeled one. On good paths labeled zero use the mixture bound on false negatives. Summing and averaging over coins contradicts the stipulated error exponent, by choosing $a',a''$ sufficiently close to $a$. [Common easy law](../dense-circuits/main.tex)

| $a$ | $b$ | $p$ | $q$ | $\theta$ | Gates strictly above | Valid pointwise error |
| --- | --- | --- | --- | --- | --- | --- |
| .00675 | .00675 | .548329 | .802 | .92 | $2.52437N$ | $2^{-.0074N}$ |
| .00635 | .00635 | .546877 | .802 | .92 | $2.52435N$ | $2^{-.0069N}$ |
| .00565 | .00565 | .544221 | .802 | .92 | $2.52419N$ | $2^{-.0062N}$ |
| .007 | .00565 | .544221 | .802 | .92 | $2.51941N$ | $2^{-.0063N}$ |
| .00565 | .00565 | .543250 | .8398 | .9676 | $2.52323N$ | $2^{-.00564N}$ |

All bounds hold for sufficiently large $n$. The last row fixes the original manuscript's confidence exponent. [Exact numerical checks](check_private_pairs.py)

## The limiting coefficient

As $a\ge b>\kappa\ge d$, the coefficient in the box is bounded above by $(3+p)H_2(p)-1$. This is strictly concave on $[1/2,1)$ and its unique maximum occurs at $p_*$ satisfying $H_2(p_*)=(3+p_*)\log_2(p_*/(1-p_*))$. Take $a=b=1-H_2(p_*)$, $q=.802$, and $\theta=.92$. At $p_*$ the two absorption inequalities are strict and $D_{\rm KL}(q\Vert3/4)<2d(p_*)$. Therefore $p$ tending to $p_*$ from below gives $\kappa=d(p)<b$ at this one fixed threshold. Taking the lower limit in $n$ before letting $p$ increase gives the limiting coefficient $(3+p_*)H_2(p_*)-1\approx2.52437808$, at density $1-a\approx0.99324302$. This is the supremum of the displayed gate inequality. Improving it requires gaining on paths consisting solely of ordinary steps as well. [Numerical bracket](check_private_pairs.py)
