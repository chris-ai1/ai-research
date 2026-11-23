# Balanced ordinary Andreev: creative Astra pass 2

Authors: Christian Reitwiessner

**No balanced asymptotic improvement.** This pass does not construct an exact $o(n^2)$ circuit. The supplied best bound remains

$$S=\frac{N^2}{2}+\frac34kmN-
\begin{cases}kN/2&m\text{ even},\\kN/4&m\text{ odd}\end{cases}
+O(N+km),$$

and hence $S+1=(5/16+o(1))n^2$ when $m=\lfloor N/k\rfloor$, $N=2^k$, and $n=N+km$.

The most developed fresh route was **nonlinear compression of the table's Walsh coefficients**, with the aim of replacing long table-amplitude ladders by a small collection of raw table halfspaces. This route has a concrete, scalable failure, rather than just an unresolved decoder condition. A five-point pattern proves that:

- hard clipping at any $B=o(N)$ cannot give a universally correct Walsh decoder;
- every fixed power compression $\operatorname{sgn}(t)|t|^\alpha$, $0<\alpha<1$, fails;
- every fixed logarithmic compression $t/\log^c(e+|t|)$, $c>0$, fails;
- these failures cannot be repaired by arbitrary affine raw table/address inputs at the top gate.

These statements concern the specified separable Walsh decoder, not arbitrary depth-two threshold circuits. They do not establish a new unrestricted lower bound. The upper-bound attempt was abandoned after its necessary decoding property was decisively falsified. No approximation result is substituted for exactness.

## 1. Model and why this route was examined

Write table bits as $y_c=2x_c-1\in\{-1,1\}$, and put

$$h_S(y)=\sum_c(-1)^{S\cdot c}y_c,\qquad
\chi_S(b)=(-1)^{S\cdot b}.$$

With the unnormalized Walsh matrix $H$, $H^2=NI$, so

$$Ny_b=\sum_S\chi_S(b)h_S(y).$$

There are two different large costs in the usual ridge treatment: the range of the table form $h_S$, and the range of the raw address form for $\chi_S$. Reducing just one does not establish $o(n^2)$. Nevertheless, a nonlinear code using only the signs or a few amplitude levels of the $h_S$ would remove the need to reproduce every possible coefficient amplitude. The proposed decoder to test was

$$F_\phi(y,b)=\sum_S\chi_S(b)\phi(h_S(y)),$$

where $\phi$ is odd and positive on positive arguments. The intended condition was

$$\operatorname{sgn}F_\phi(y,b)=y_b\quad\text{for every }y,b.$$

This is a specific table-coding proposal, not a reformulation of the original circuit problem. It can be tested before attempting any address sharing. The code tests $[h_S\ge r]$ are raw table LTFs; their use in a circuit still requires charging for the interaction with the address. In particular, neither $h_S$ nor $\phi(h_S)$ is treated as a precomputed circuit input.

The motivation was sign correctness, not exact reconstruction of the amplitudes. It was conceivable that compressing large spectral coefficients might preserve all coordinate signs even when $H\phi(Hy)$ was numerically far from $Ny$. The counterexamples below exclude several natural versions of that possibility.

## 2. A five-point pattern with an exactly calculable spectrum

In $\mathbb F_2^4$, take

$$A=\{e_1,e_2,e_3,e_4,e_1+e_2+e_3+e_4\},\qquad
z(c)=1-2\mathbf1_A(c).$$

Thus $z(0)=1$. If $s$ has Hamming weight $w$, then

$$\sum_{a\in A}(-1)^{s\cdot a}=4-2w+(-1)^w.$$

The values are $5$ at $w=0$, $1$ at $w=1,2$, and $-3$ at $w=3,4$. Consequently

$$Hz=16\delta_0-2H\mathbf1_A$$

has ten entries $-2$ and six entries $6$. At address zero,

$$F_\phi(z,0)=6\phi(6)-10\phi(2).$$

In particular, the sign-only code gives $6-10=-4$, although $z(0)=1$.

This is an algebraic seed, not a claim inferred from small circuit optima. Two different explicit extensions make its consequences asymptotic.

### 2.1 Repetition: hard clipping needs linear range

Let $N=16M$, with $M$ a power of two, and repeat the seed in a new coordinate group:

$$y(c,u)=z(c).$$

Its only nonzero Walsh coefficients are ten copies of $-2M$ and six copies of $6M$. For $\phi_B(t)=\max(-B,\min(B,t))$,

$$F_{\phi_B}(y,0)=6\min(B,6M)-10\min(B,2M).$$

For every $B>0$ this is strictly negative when

$$B<\frac{10M}{3}=\frac{5N}{24}.$$

For $B\le2M$, the score is simply $-4B$. For $2M\le B<10M/3$, it is $6B-20M$. Thus hard clipping cannot replace range $\Theta(N)$ by $o(N)$ in this decoder. This statement permits $B$ to depend arbitrarily on $N$.

### 2.2 Puncturing: a three-scale defect defeats soft compression

Instead put the five negative entries on one slice and make all other entries positive:

$$y_M(c,u)=1-2\mathbf1_A(c)\mathbf1_{u=0}.$$

Again $N=16M$ and $y_M(0,0)=1$. The spectrum consists of

- one coefficient $N-10$;
- $M-1$ coefficients $-10$;
- $10M$ coefficients $-2$;
- $5M$ coefficients $6$.

Indeed,

$$h_{s,t}=N\mathbf1_{s=0,t=0}-2\sum_{a\in A}(-1)^{s\cdot a}.$$

Define the explicit defect

$$D_\phi=\phi(10)+10\phi(2)-5\phi(6).$$

Then the exact score at the positive selected entry is

$$F_\phi(y_M,0)=\phi(N-10)+\phi(10)-M D_\phi.$$

Therefore, if $\phi(t)=o(t)$ and $D_\phi>0$, the score is negative for all sufficiently large powers-of-two $M$. The negative term is linear in $M$; the positive exceptional coefficient contributes only $o(M)$.

This proves a universal counterexample family for every fixed shrinker satisfying the displayed, directly checkable three-scale inequality.

## 3. Consequences for powers and logarithmic shrinkage

### 3.1 Every fixed sublinear power fails

For $\phi(t)=\operatorname{sgn}(t)|t|^\alpha$,

$$D_\alpha=2^\alpha\bigl(5^\alpha+10-5\cdot3^\alpha\bigr).$$

For $0<\alpha<1$ this is positive. To see this, put

$$g(\alpha)=5^\alpha+10-5\cdot3^\alpha.$$

We have $g(1)=0$, while

$$g'(\alpha)=5^\alpha\log5-5\cdot3^\alpha\log3<0
\quad(0\le\alpha\le1),$$

since $(5/3)^\alpha\le5/3<5\log3/\log5$. Thus the punctured family defeats every fixed $\alpha<1$, however close to one.

There is also a quantitative statement for powers changing with $N$. For $\alpha_N=1-\varepsilon_N$, $\varepsilon_N\to0$,

$$D_{1-\varepsilon}=10\log(27/5)\,\varepsilon+O(\varepsilon^2).$$

The same explicit family fails whenever

$$e^{-\varepsilon_N\log N}=o(\varepsilon_N).$$

For example this holds for

$$\varepsilon_N=c\frac{\log\log N}{\log N},\qquad c\ge1,$$

which would reduce the maximum amplitude to $N/(\log N)^c$. This particular calculation does not rule out every possible $N$-dependent near-linear map. It also does not convert amplitude reduction into a gate-count reduction: the required interactions would still need compilation.

### 3.2 Every fixed logarithmic shrinker fails

Allow a fixed repetition factor $Q$, also a power of two, after the punctured construction. With $N=16MQ$, the nonzero spectral values are multiplied by $Q$. Define

$$D_{\phi,Q}=\phi(10Q)+10\phi(2Q)-5\phi(6Q).$$

Then

$$F_\phi(y,0)=\phi(N-10Q)+\phi(10Q)-M D_{\phi,Q}.$$

For

$$\phi(t)=\frac{t}{\log^c(e+|t|)},\qquad c>0,$$

choose $Q=4$. Set $\psi(t)=\phi(t)/t$ for $t>0$ and $t_0=2Q=8$. We have

$$D_{\phi,Q}=5t_0\bigl(\psi(5t_0)+2\psi(t_0)-3\psi(3t_0)\bigr)>0.$$

For completeness, $u\mapsto\psi(e^u)$ is strictly decreasing and strictly convex on $e^u\ge8$. Writing $L(u)=\log(e+e^u)$, the sign of its second derivative is the sign of

$$(c+1)e^u-e\log(e+e^u),$$

which is positive in this range. Jensen's inequality and

$$\frac{\log(5t_0)+2\log t_0}{3}<\log(3t_0)$$

give the strict displayed inequality. Since $\phi(N)=o(N)$, the negative defect again wins for sufficiently large $M$.

This covers fixed $c>0$, including arbitrarily small logarithmic compression exponents. Uniformly rescaling every coefficient is a different operation: it preserves signs but does not reduce the number of distinct thresholds needed to reproduce the code.

## 4. Raw top wires cannot repair these decoders

A wrong score at a single address would not by itself exclude repair by the raw table/address wires permitted in the model. The following lemma closes that loophole for this particular decoder.

**Affine-repair lemma.** Suppose an odd $\phi$ has a table $z\in\{-1,1\}^N$ with $z_0=1$ and

$$F_\phi(z,0)=-d<0.$$

Put

$$p=(N-1)\phi(2)-\phi(N-2).$$

A universally correct score of the form

$$F_\phi(y,b)+\sum_c w_cy_c+q(a)$$

requires

$$(N-2)d<p.$$

Here $q(a)$ can even be an arbitrary function of the raw address, stronger than the allowed affine raw address contribution.

**Proof.** For any fixed address, correctness on both $y$ and $-y$ implies that

$$y_b\left(F_\phi(y,b)+\sum_cw_cy_c\right)>0.$$

Indeed the address term has the same value on these two tables and cannot rescue a nonpositive odd part. This argument also handles a fixed top bias and either standard threshold tie convention.

Translate the bad table so its selected positive entry is at $b$, and then modulate it by each character centered at $b$:

$$z^{b,r}(c)=z(c+b)(-1)^{r\cdot(c+b)}.$$

Oddness and Walsh covariance give

$$z^{b,r}(b)=1,\qquad F_\phi(z^{b,r},b)=-d.$$

Averaging the necessary strict inequality over $r$ leaves only $w_b$, so $w_b>d$ for every $b$. Hence $W=\sum_bw_b>Nd$.

Now test the positive singleton table $v^b=2\delta_b-\mathbf1$. Its spectral score at $b$ is exactly $p$. Correctness requires

$$p+2w_b-W>0.$$

Sum over $b$ to obtain $Np-(N-2)W>0$. Combining this with $W>Nd$ proves the claim. $\square$

For the punctured families and fixed shrinkers above, $d=\Theta(N)$ whereas $p=O(N)$. Thus the necessary inequality fails for large $N$. The same conclusion holds for the stated $N$-dependent powers because their negative deficit tends to infinity and $p=O(N)$.

For clipping, the repetition family gives $d=4B$ when $B\le N/8$, while

$$p=(N-1)\min(2,B)-\min(N-2,B).$$

The lemma immediately excludes every $B=o(N)$, even after arbitrary raw affine corrections. In the next range, $d=5N/4-6B$; it also gives the necessary bound $B>5N/24-O(1)$ for this decoder to be repairable.

The counterexamples use arbitrary independent table assignments. Every required address $b$ has a raw representative for every $m\ge1$, for example with first bit $b_i$ in block $i$ and all other bits zero. Consequently these are legitimate worst-case tests in the balanced regime, not a restriction to a different Andreev family.

## 5. Exact raw-gate realization and honest accounting

The decoding failure already occurs if address characters are granted for free. Nevertheless, the layer accounting matters: a nonlinear table code is not itself a raw affine form.

For a character $S$, choose any raw signed sum

$$t_S(a)=\sum_{i\in S}\sum_{j=1}^m\epsilon_{ij}a_{ij},\qquad\epsilon_{ij}\in\{-1,1\}.$$

Then $(-1)^{t_S}=\chi_S(b)$. Its integer range is an interval of length $T_S=m|S|$, regardless of the signs. Translation of the interval changes only known signs and biases.

For an integer table form $h=h_S$, $|h|\le N$, and an integer $j$ in the range, the two raw LTFs

$$[M(t_S-j)+h\ge1]-[M(t_S-j)-h\ge1],\qquad M>N,$$

equal $\operatorname{sgn}(h)\mathbf1_{t_S=j}$, with $\operatorname{sgn}(0)=0$. Multiplying their top coefficients by $(-1)^j$ and summing over $j$ implements the sign-code contribution exactly. This is a valid two-layer implementation, but it costs

$$2\sum_S(T_S+1)=kmN+2N$$

bottom gates. Even if its decoder were correct, this particular implementation would still be quadratic at balance.

For integer $B$, the clipped amplitude has the exact identity

$$\operatorname{clip}_B(h)=\frac12\sum_{r=-B+1}^{B}\operatorname{sgn}(2h-2r+1).$$

For each $r,j$, use

$$[M(t_S-j)+(2h-2r+1)\ge0]
-[M(t_S-j)-(2h-2r+1)\ge0],$$

with $M=2N+2B+2$. The difference is the indicated sign times $\mathbf1_{t_S=j}$. These are explicitly raw gates: substitute $h_S=\sum_c\chi_S(c)(2x_c-1)$ and the raw formula for $t_S$. No code, parity, or product is supplied as a helper input.

This elementary implementation costs at most

$$4B\sum_S(T_S+1)=2BkmN+4BN$$

bottom gates. It is not a competitive compiler. In particular, it would be wrong to claim an $O(N(B+T))$ circuit merely because a nonlinear coefficient's amplitude was bounded by $B$. The supplied linear-amplitude ridge identities do not automatically apply to a clipped nonlinear form.

For these integer gates, bottom coefficients and thresholds have $O(\log((N+B)(km+1)))$ bits; multiplying the top score by two makes its coefficients integers of constant magnitude. Thus the failed route is not failing because large weights were prohibited. Arbitrary real weights do not fix its explicit sign errors.

These gate formulas are included only to audit the proposed code interaction. They are not claimed as a new useful compiler, and the equality interaction is not a replacement name for the previously unresolved hyperplane-incidence problem.

## 6. Other structural directions and early accounting

Several alternatives were considered before developing the table-code route. None produced a new exact upper construction.

**Packing independent table bits into positional digits.** Packing $q$ bits gives $2^q$ possible values. A bit of an ordinary binary positional encoding has exponentially many alternations in that one-dimensional order. Thus replacing $q$ independent bit interactions by a unary threshold ladder on that encoding does not yield an automatic factor-$q$ saving. This observation concerns that encoding only; it is not an obstruction to general multi-table-bit gates. No alternate carry-free packing with a shared address decoder was obtained.

**Pairing raw coordinates to cancel within blocks.** For each fixed input, pairing equal bits leaves at most one unequal pair per block, suggesting a short residual address. The pairing must be fixed in a circuit, however. For a block with an even number $r$ of ones, a uniformly random perfect matching pairs only equal values with probability

$$\frac{(r-1)!!(m-r-1)!!}{(m-1)!!}.$$

At $r=m/2$ this is $\exp(-\Theta(m))$. Thus enumerating enough fixed pairings to guarantee such a residual is exponentially expensive at $m\asymp N/k$. Implementing input-dependent pairing would require another layer. No compression of those matching incidences was found.

**Central windows and orthogonal mixed-sign masks.** If a $d\times d$ Hadamard matrix supplies masks for a raw sign vector $a$, then

$$\sum_r\langle v_r,a\rangle^2=d^2.$$

This guarantees a projection of magnitude at most $\sqrt d$. But the direct cover uses $d$ masks, each with a window of $\Theta(\sqrt d)$ threshold positions, costing $\Theta(d^{3/2})$ even for one parity channel. This does not beat its full ladder. It also does not build the required shared table/address incidence. The identity is a useful warning against confusing a pointwise existence of a short projection with a cheap circuit covering all inputs.

**Higher spectral powers and softer compression.** These were pursued beyond counting through the explicit defect analysis above. Spectral powers correspond to convolution powers of the table, rather than to coordinatewise powers of its selected bit. Sign-only decoding, clipping, and sublinear powers all fail on the developed families. This is why that line was stopped rather than proposing an unproved sign-preservation lemma.

None of these calculations uses the excluded few-global-periodic-rank-channel proposal, finite-size record optimization, an unbalanced regime, or an average-case error guarantee.

## 7. The sharpest next target from this pass

The five-point defect says that **independent scalar treatment of one Walsh basis is too rigid** for the natural shrinkers studied here. A genuine escape would have to couple spectral information, use genuinely different table bases, or make the address interactions more than scalar Walsh modulation.

A concrete next experiment would be redundant table codes from **nonlinear permutations of the address labels with sparse Walsh expansions**, not just more sign masks in the same basis. There is an explicit starting family. Write $b=(t,u)$, let $A$ be an invertible binary matrix, and define

$$\pi(t,u)=(t,A^t u).$$

For a Walsh character indexed by $(s_0,s)$,

$$\chi_{(s_0,s)}(\pi(t,u))
=\frac{(-1)^{s_0t}}2
\left(\chi_s(u)+\chi_{A^Ts}(u)
+(-1)^t\bigl(\chi_s(u)-\chi_{A^Ts}(u)\bigr)\right).$$

Thus a code row for a permuted table is still a raw linear table form, and its decoder character expands into at most four ordinary address characters. This is an explicit structure with bounded expansion, rather than an unspecified incidence family.

There are already two concrete limitations:

1. Affine permutations and character modulations merely rearrange the original Walsh decoder; averaging them does not repair it.
2. A family of the displayed shears with the same control coordinate has a common fixed slice $t=0$. Place the five-point puncture in that slice, with all other table entries positive. Every permutation fixes that table, so every such basis gives the same bad decoded value at the selected point. Arbitrarily many same-control shears therefore do not repair the counterexample.

The next specific question is whether a small family with **different controls and global mixing** avoids this common-puncture failure and has a uniformly correct sign decoder using raw table halfspace codes. This question is narrower than constructing an Andreev circuit and has explicit finite objects to test. No positive answer is established here.

Even a positive table-coding result would leave a second, separate obligation: share or shorten the raw address interactions enough that their total count is $o(N^2)$. The full-ladder implementation in §5 remains quadratic per constant number of bases. The sparse four-character expansion alone does not solve that cost. I do not claim that this next target, by itself, implies a subquadratic circuit.

## 8. Verification and artifacts

All work was confined to this directory. No agents, commits, pushes, shared-archive edits, or background solver jobs were used.

- `notes.md` records the initial routes and the first scalable spectral witness before the stronger five-point form was developed.
- `clipping_probe.py` found an exact 16-entry clipping witness by integer Walsh transforms; `clipping_witness.json` records it.
- `shrinker_probe.py` verified the initial punctured and repeated families and found the sharper five-point pattern; `shrinker_checks.json` records its checks. Floating-point calculations there were exploratory only.
- `verify_mechanism.py` independently checks the final five-point spectrum, both extension formulas for $M=1,2,4,8,16,32,64$, 1,386 integer raw-gate evaluations, and the modulation/spike identities used by the affine-repair lemma.
- `verification.json` records those passing exact checks.

Run the final exact checks with:

```sh
python3 /tmp/andreev_gap/asymptotic_creative_astra_pass2/verify_mechanism.py
```

The asymptotic conclusions follow from the displayed proofs, not from extrapolating these tests. The substantive outcome is the explicit falsification of the developed compression route, including its raw-top-wire repair, and the controlled-permutation alternative with its common-slice failure identified. There is no new balanced exact upper bound.
