# No balanced asymptotic improvement obtained.

Authors: Christian Reitwiessner

This restart did **not** prove an exact $o(n^2)$ upper bound for ordinary Andreev. Its principal developed route was modular rank retrieval with threshold-encoded tables. The raw-gate compiler is exact and has attractive balanced accounting, but a uniform averaging counterexample defeats its proposed small-channel implementation, even with genuinely mixed signs inside blocks and arbitrary nonlinear table encodings. A more flexible, explicitly stated gated-code construction remains unproved. No finite-size gate record or approximation result is claimed.

## Model and balance

Let $N=2^k$, $m=\lfloor N/k\rfloor$, and $n=N+km=2N-O(k)$. Thus $km\sim N$, $k\sim\log_2 n$, and

$$mN=\Theta(n^2/\log n).$$

This is a valid balanced family for every growing integer $k$; exact equality $km=N$ is unnecessary. All table bits are independent. Write $s_i=\sum_j a_{i,j}$, $b_i=s_i\bmod2$, and $y_c=2x_c-1$. Occurrences of $s_i$ below abbreviate affine sums of raw inputs, not intermediate gates. The required output is $[y_b>0]$.

## 1. Exact rank retrieval, including nonlinear table encodings

For any integer affine raw-address form $T(a)$ with $0\le T\le D$, and any period $Q$, the following identity holds:

$$\sum_{r=0}^{D}[T(a)+x_{r\bmod Q}\ge r+1]-T(a)=x_{T(a)\bmod Q}.$$

There are exactly $T$ certain-one terms, one term exposing the requested table bit, and all remaining terms are zero. This is a legitimate two-layer implementation: all displayed brackets are bottom gates and $-T$ is a direct raw-input term at the top. It does not compute a modular address in a hidden layer.

More generally, choose fixed integer affine forms

$$\ell_q(x)=\beta_q+\sum_c\alpha_{q,c}x_c$$

that never vanish on Boolean tables, and put $h_q(x)=[\ell_q(x)>0]$. An arbitrary integer-threshold table function can be put in this form by replacing its threshold expression $L$ by $2L+1$. Choose an integer $M>\max_{q,x}|\ell_q(x)|$. Then

$$G_r(x,a)=[2M T(a)+\beta_{r\bmod Q}+\sum_c\alpha_{r\bmod Q,c}x_c\ge2Mr]$$

satisfies

$$\sum_{r=0}^{D}G_r(x,a)-T(a)=h_{T(a)\bmod Q}(x).$$

Thus rank retrieval can query a threshold encoding of **many** table bits, with the same $D+1$ gate cost. Its code rows and coefficients are fixed for all inputs.

### Why the accounting initially looked useful

Set $Q=N$ and $T=\sum_i2^is_i$. Then $D=m(N-1)$, giving $m(N-1)+2=O(n^2/\log n)$ gates including the top. But the retrieved table index is the ordinary binary residue of $\sum_i2^is_i$, **not** $(s_i\bmod2)_i$. For instance, $s_0=2$ and all other counts zero have $b=0$, whereas $T=2$. Carries are a correctness failure, not a lower-order cost.

The attempted repair used $L$ independently fixed positional views. For view $l$, choose a permutation $\pi_l$ of the block positions and signs $\sigma_{l,i,j}\in\{-1,1\}$, and define

$$q_{l,i}(a)=\sum_j\left(\sigma_{l,i,j}a_{i,j}+\frac{1-\sigma_{l,i,j}}2\right),\qquad
T_l(a)=\sum_i2^{\pi_l(i)}q_{l,i}(a).$$

These are raw affine forms with $0\le T_l\le D$. Let $e_{l,r}(x)=2h_{l,r}(x)-1$. A proposed top score was

$$F(x,a)=u\cdot(x,a)+u_0+\sum_{l=1}^{L}\lambda_l e_{l,T_l(a)\bmod N}(x).$$

Substituting the rank identity yields exactly $L(D+1)$ bottom gates and one top. No code bit is computed in an intermediate layer. If this worked with $L=O(\log k)$, it would give

$$O\!\left(\frac{n^2\log\log n}{\log n}\right).$$

The desired correctness lemma was $y_bF(x,a)>0$ for every table and every raw address. **For these periodic positional views, that lemma is false whenever $k\ge2$ and $m-1>2^L$.**

## 2. Scalable falsification of the small-channel repair

This is a counterexample to the proposed architecture, not a lower-bound investigation of unrestricted depth-two circuits. It is stronger than merely showing that one chosen set of masks fails.

Reserve one raw coordinate $r_i$ in each block. Among the other $m-1$ coordinates, two coordinates $p_i,q_i$ have identical $L$-bit sign signatures when $m-1>2^L$:

$$\sigma_{l,i,p_i}=\sigma_{l,i,q_i}\quad\text{for every }l.$$

For each desired parity vector $b$ and each $t\in\{0,1\}^k$, construct the raw address

$$a_{i,r_i}=b_i,\qquad a_{i,p_i}=a_{i,q_i}=t_i,$$

with all other coordinates zero. Its block parity is exactly $b$. In view $l$,

$$T_l(a)=C_l(b)+\sum_i2^{\pi_l(i)+1}\sigma_{l,i,p_i}t_i.$$

As $t$ ranges uniformly, this residue is uniform on one parity coset modulo $N$, with exactly two preimages for each residue in that coset. To see this, discard the position of weight $2^k$, which is zero modulo $N$, and divide the others by two. Signed binary weights $\pm1,\pm2,\ldots,\pm2^{k-2}$ give a bijection modulo $2^{k-1}$: successive low bits recover successive choice bits. Signs do not change this argument.

The parity of $C_l(b)$ depends on only one address bit, namely $b_{i_l}$ for the block $i_l$ of positional weight one. Consequently, for **any** code rows $e_{l,r}(x)$, even rows that are not threshold functions,

$$\mathbb E_t[e_{l,T_l(a(b,t))\bmod N}(x)]
 =A_l(x)+B_l(x)b_{i_l}.$$

Averaging the direct raw-input top term is also affine in $b$. The direct table term is constant for a fixed table. Therefore

$$\mathbb E_t F(x,a(b,t))=C(x)+\sum_iD_i(x)b_i.$$

Now fix the legitimate independent table assignment $x_b=b_0\mathbin{\mathrm{XOR}}b_1$. Exact correctness on every raw address would imply that the displayed affine function has the strict sign of XOR. This is impossible: fixing the other bits, any affine function obeys

$$F_{00}+F_{11}=F_{01}+F_{10},$$

whereas XOR requires both terms on the left to be negative and both on the right to be positive. A finite exact threshold circuit can always be given a strict separating top threshold, so threshold ties do not avoid the contradiction.

At balance, every $L=o(k)$ eventually satisfies $m-1>2^L$. Thus the particular route that would have supplied the logarithmic saving cannot work. Allowing larger **table** coefficients, arbitrary signed top coefficients, arbitrary table encodings, and mixed signs inside blocks does not repair it. The obstruction concerns the shared periodic address-query structure within each channel.

A simpler diagnostic, also derived, is that if code rows merely permute table bits, each view queries location zero on at most two of the $2^k$ pair-activation choices. With $2L<N$, some even-parity address queries zero in no view. The averaging argument above supersedes this diagnostic and also handles a direct table term at the top.

## 3. Remaining architecture: separately gated table-code rows

The concrete remaining relaxation is to let the address hyperplane vary **for each table-code row**, instead of requiring all rows of a rank channel to share a scalar $T_l$ and periodic table code. This destroys the common-residue averaging step. It has an exact two-gate compiler.

Choose fixed integer affine address forms and nonvanishing integer affine table forms

$$Z_r(a)=d_r+\sum_{i,j}w_{r,i,j}a_{i,j},\qquad
\ell_r(x)=\beta_r+\sum_c\alpha_{r,c}x_c.$$

For an integer $M_r>\max_x|\ell_r(x)|$, define the raw bottom gates

$$g_r^+=[2M_r\sum_{i,j}w_{r,i,j}a_{i,j}+\sum_c\alpha_{r,c}x_c
\ge-2M_rd_r-\beta_r],$$

$$g_r^-=[2M_r\sum_{i,j}w_{r,i,j}a_{i,j}-\sum_c\alpha_{r,c}x_c
\ge-2M_rd_r+\beta_r].$$

The exact identity is

$$g_r^+-g_r^-=\operatorname{sgn}(\ell_r(x))\,[Z_r(a)=0].$$

Indeed both gates agree when $Z_r\ne0$, while at $Z_r=0$ their difference is the sign of $\ell_r$. Thus a top gate can vote on threshold-encoded table bits selected by raw-address hyperplanes, without computing either selector or code bit in a hidden layer.

### Precise unproved lemma and the bound it would imply

One focused version uses signed positional address hyperplanes

$$Z_r(a)=\sum_i2^{\pi_r(i)}\sum_j\sigma_{r,i,j}a_{i,j}-t_r,$$

where the signs, permutation, and level may vary with **every row** $r$. Ask for fixed data with $R\le C mN$, fixed table halfspaces $\ell_r$, and fixed real weights $v_r$, satisfying

$$\boxed{\quad
(2x_b-1)\sum_{r:Z_r(a)=0}v_r\operatorname{sgn}(\ell_r(x))>0
\quad\text{for every }x\in\{0,1\}^N,\ a\in\{0,1\}^{km}.
\quad}$$

This is the missing **gated threshold-code lemma**. It is a finite, explicit feasibility condition on code rows and address slices, not an input-dependent choice of masks or a probabilistic correctness statement. A proposed instance can be falsified by one table/address pair. The lemma is **UNKNOWN**; no family satisfying it was obtained, and there is no evidence here that it is true. It is a structured remaining target, not a claimed solution or an established simplification of the general problem.

If true, the two-gate identity would immediately give $2R+1=O(mN)=O(n^2/\log n)$ gates at balance. More generally, $R=O(mN\log k)$ would still give $O(n^2\log\log n/\log n)$. Conversely, $R=\Theta(kmN)$ would supply no asymptotic improvement. The boxed condition requires sign dominance for **every** table; coverage by some slices, average correlation, or a second-moment estimate is insufficient.

The point of the table code is to permit cancellation between nonliteral table functions. For example, for three independent signs $y_1,y_2,y_3$, let the four coefficient rows be

$$(1,1,1),\ (1,1,-1),\ (1,-1,1),\ (-1,1,1),$$

and let $e_r$ be the sign of the corresponding table linear form. Direct enumeration, or the majority-of-three polynomial, gives

$$\sum_{r=1}^4\alpha_{r,i}e_r=2y_i\qquad(i=1,2,3).$$

This is a small algebraic illustration of cancellation using code rows that each depend on several table bits. It is **not** a scalable Andreev construction, a gate saving, or evidence that the boxed lemma holds. The unresolved part is assigning row-dependent raw-address slices so that the correct decoding occurs at every raw address within the $O(mN)$ budget.

Genuinely different signs within blocks are allowed in this remaining target. Their role would be to change which code rows are active; the modular counterexample shows why merely adding a few global mixed-sign views is insufficient. Large coefficients make the exact two-gate selector possible but do not establish the required incidence/decoding property.

## 4. Coefficient and description costs

In a rank channel, if table coefficients and the bias have at most $B$ magnitude bits, one can take $M$ with $O(B+\log N)$ bits. Positional raw coefficients and thresholds then have $O(B+\log N+\log(mN))$ bits. There are $L(D+1)$ gates, with up to $N+km$ coefficients each; the dense description is polynomial in that count times this bit bound. The table code has $LN$ rows before its periodic repetition. No unrestricted large number is being used as a free digit-extraction operation.

For a gated row, if the address coefficients, constant, table coefficients, and table bias have magnitude bit lengths at most $W$ and $B$ respectively, all bottom coefficients can be taken with $O(W+B+\log N)$ bits. For signed positional rows whose levels intersect the address range, $W=O(\log(mN))$. Rational top weights add their own numerator/denominator description lengths; the missing lemma currently supplies no bound on these. Every gate and every coefficient must be fixed before seeing the inputs.

## 5. Exact checks and research limits

`checks.py` uses only Python's standard library and completed normally. Its integer-arithmetic output is saved in `checks.json`.

- The nonlinear-table rank compiler was checked on all 256 tables for $Q=8$, every integer $T$ from 0 through 21, and fixed nontrivial affine table rows: 5,632 cases.
- The two-gate slice identity was checked on all 32 tables for a five-bit affine table row and all integer $Z$ from $-9$ through 9: 608 cases.
- The four-row, three-bit threshold-code identity was checked on all eight tables.
- The rank-averaging counterexample was checked on balanced instances $(k,m,L)=(6,10,3),(8,32,4),(10,102,6)$. For each of the four XOR corner parities and each view, all $2^k$ pair activations were enumerated. Every residue histogram was exactly uniform on the predicted parity coset, and the four-corner averaged-score identity held for nonliteral table code rows. These checks test the scalable mechanism; they are not finite gate records.

No solver or background job was launched. No commits, pushes, shared archive edits, or delegation were performed. Files were created only in the requested directory.

Other initial directions were rejected at their asymptotic accounting or realization step: positional whole-table digit extraction lacked an affine raw-input extraction identity; repeated rank flattening retained an exponential Cartesian product; full character ladders retained $\Theta(kmN)$ cost; spectral coefficient quantization did not eliminate the address-ladder cost and introduced non-affine residue corrections. None was promoted to an upper bound.

A narrow primary-source check on parity circuits was made to avoid treating a hypothetical sublinear parity circuit as an available ingredient: [Impagliazzo–Paturi–Saks, *Size–Depth Tradeoffs for Threshold Circuits*](https://epubs.siam.org/doi/10.1137/S0097539792282965) and [Uchizawa, *Size, Depth and Energy of Threshold Circuits Computing Parity Function*](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ISAAC.2020.54). Neither supplies the numerical two-layer substitution needed here. No literature novelty claim is made for the identities or counterexample in this report.

## Focused next step

Investigate an explicit, row-dependent signed-positional slice system with a threshold table code satisfying the boxed worst-case inequality at $R=O(mN)$, or falsify that restricted target. The first meaningful milestone is an exact all-table decoding identity for its active row sets; optimizing masks before such an identity is available would repeat the failed cover/dictionary approach. Do not continue the $o(k)$ periodic rank-channel proposal: the averaging counterexample already rules out its intended balanced saving.
