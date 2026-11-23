# ETH matrix ideas for depth two Andreev circuits

Authors: Christian Reitwiessner

Date: 13 November 2026

## Outcome and scope

No improved exact upper bound is established. The promising transferable idea is an exact decomposition into a structured main term and a shared low-rank correction. The parity polynomial alone does not supply the saving. A concrete transfer to the table's Walsh space makes the correction inexpensive when its rank is small, but leaves shifted Andreev lookups in the main term. This identifies a missing circuit construction, rather than a general impossibility theorem.

The target is ordinary Andreev with an arbitrary input table, raw address bits, and one fixed depth-two threshold circuit for every input. Write $N=2^k$, $m=N/k$ at balance, and $n=N+km$. Put $y_c=(-1)^{x_c}$ and $b_i=\sum_j a_{i,j}\pmod2$. We want the sign $y_{b(a)}$. The existing exact bound is $(5/16+o(1))n^2$; constant-error approximation already uses $O(n^{3/2})$ gates. This investigation leaves both unchanged.

## The source mechanism

Sources inspected:

- [OpenAI manuscript, especially the matrix and replacement-form construction](https://github.com/openai/math/blob/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/build/main_full_version.tex).
- [Ryan O'Donnell's exposition, Sections 2–6](https://hexagonmath.org/pdf/2610.00572v1). Its provenance identifies LLM-assisted authorship.
- [Mark Sellke's outline](https://msellke.com/Files/ETH-False-Slides.pdf).
- [Anthropic's condensed tensor-contraction description](https://github.com/anthropics/formal-math/blob/main/eth/README.md), as a comparison; not a detailed audit of that proof.

The interpolation polynomial is

$$f_{a,d}(z)=(-1)^a\sum_{j=0}^d(-2)^j\binom{z-a}{j}.$$

It equals $(-1)^z$ on $a,a+1,\ldots,a+d$. Its values outside the interval are not bounded. For commuting SWAP involutions $S_i$, set $W=\sum_i(I-S_i)/2$, $U=\prod_iS_i$, and $M=Uf(W)$. Typical spectral layers are fixed by $M$, so $I-M$ has low rank. The degree bounds how many swaps a term can undo. Exceptional directions are retained as small-integer linear measurements. Polynomial replacement forms and exact interpolation then recover the count. The approximation is used to design an exact decomposition, not to discard rare SAT assignments. This is the relevant mechanism in the OpenAI manuscript and O'Donnell exposition.

## A precise transfer to the table index space

The following is our adaptation, using translations rather than the source's register swaps. For a table vector $y\in\mathbb R^N$, let

$$(T_i y)_c=y_{c\oplus e_i},\qquad W=\frac12\sum_{i=1}^k(I-T_i),\qquad U=\prod_{i=1}^kT_i.$$

For the character vector $\chi_S(c)=(-1)^{S\cdot c}$,

$$W\chi_S=|S|\chi_S,\qquad U\chi_S=(-1)^{|S|}\chi_S.$$

With $M=Uf_{a,d}(W)$ and $E=I-M$, put

$$\lambda_S=(-1)^{|S|}f_{a,d}(|S|).$$

Then

$$\operatorname{rank}E=\sum_{j:\,(-1)^jf_{a,d}(j)\ne1}\binom kj
\le\sum_{j\notin[a,a+d]}\binom kj.$$

The upper bound allows accidental equality outside the interpolation interval. Simultaneously, because the translations commute and square to the identity,

$$M=\sum_{|T|\le d}\gamma_T T_{[k]\setminus T}.$$

Consequently the exact lookup identity is

$$y_{b(a)}=\sum_{|T|\le d}\gamma_T y_{b(a)\oplus\mathbf1\oplus1_T}+(Ey)_{b(a)}.$$

Every lookup in the main sum is another ordinary Andreev lookup with a fixed table permutation. Alternatively one can complement one raw bit in each shifted address block. Thus this formula supplies no smaller recursive subproblem. Treating each shifted lookup separately costs copies of the original circuit; regrouping their Walsh expansions returns the spectral formula. This is an obstruction to these two direct implementations, not a lower bound on all joint implementations.

## The correction has a valid threshold implementation

Let $B=\{S:\lambda_S\ne1\}$ and $r=|B|$. Define the unnormalized table Fourier forms

$$X_S=\sum_c\chi_S(c)y_c,\qquad t_S=\sum_{i\in S}\sum_j a_{i,j}.$$

The exact correction is

$$(Ey)_{b(a)}=\frac1N\sum_{S\in B}(1-\lambda_S)X_S(-1)^{t_S}.$$

Each $X_S$ is an even integer for $k\ge1$, with range $[-N,N]$, and is affine in the raw table bits. For $\varphi(u)=(-1)^uu$,

$$X_S(-1)^{t_S}=\varphi(X_S+t_S)-\varphi(t_S).$$

Expanding both functions in threshold staircases uses at most $2N+2|S|m$ bottom gates. Thus the residual is an exact real-valued sum of outputs of $O(r(N+km))=O(rn)$ bottom gates, plus constants. Its coefficients can be absorbed into a final output gate when added to an exact main score. Large interpolation coefficients affect weight sizes, not this gate count. No extra threshold layer is hidden here.

This is a useful compiler for a correction supported on Walsh characters. A generic rank-$r$ factorization does not imply it: an arbitrary address factor may itself be difficult to realize. Similarly, small-integer linear measurements of the table can be wired into bottom gates, but arbitrary nonlinear decoding of their joint values is not free.

The missing result is a cheap threshold representation of $(My)_{b(a)}$. In its spectral representation, every character whose weight is in the interpolation interval still has multiplier exactly one. When $r\ll N$, almost all original channels remain. No new savings follow by implementing those channels with the existing staircases.

## A small-rank error can still reverse all answers

For $k=8$, take the interval $[2,6]$, so $d=4$. Exactly $18$ of the $256$ character directions are exceptional. But

$$f_{2,4}(1)=31,\qquad \lambda_{\{1\}}=-31.$$

The valid table $y_c=(-1)^{c_1}$ therefore satisfies $My=-31y$. Replacing $y$ by $My$ and taking signs gives the wrong output at every address for this table, despite the small correction rank.

There is a general version: if $a\ge1$, then

$$f_{a,d}(a-1)=(-1)^a(2^{d+1}-1),\qquad
(-1)^{a-1}f_{a,d}(a-1)=-(2^{d+1}-1).$$

Any character table of weight $a-1$ is sign-reversed. Thus the correction cannot be omitted merely because its rank is a small fraction of $N$. This says nothing against the source algorithm, which keeps the correction exactly. Nor does low rank by itself control the mean-square error under random tables: the exceptional eigenvalues can be large.

## Depth and sign coherence

There are three distinctions when attempting a stronger transfer.

First, a low-degree polynomial in an unweighted sum is still block-symmetric. Implementing it with threshold staircases retains sign coherence. The paper's coherent lower bound $\Omega(n^2/\log^3n)$ excludes an exact $n^{2-\delta}$ construction of this type for fixed $\delta>0$, though logarithmic improvements remain possible. Mixed signs in a matrix's table coefficients do not count as mixed address weights.

Second, the source counting algorithm can enumerate measurement values, multiply intermediate expressions, and perform interpolation. None of these is automatically a single threshold gate. Exact interpolation is linear in its evaluated scores, so it could be put in the final weighted sum if those scores and required derivatives were already cheap sums of raw-input threshold gates. The source does not establish that property. Boolean answers or signs at the interpolation points are insufficient.

Third, the linear measurements are not inputs supplied to our circuit. All bottom gates must read raw table and address bits. Replacing each original bit by a general linear form inside an exact polynomial for Andreev leads to products of those forms. The usual multilinear polynomial already has degree $km+1$. A fast arithmetic or tensor-contraction evaluation of those products does not by itself flatten into two threshold layers.

For the original SWAP construction applied just to table-index coordinates, a partial swap merely permutes the logical address coordinates. Such a term retains the lookup problem. Applied instead to raw-input positions, swaps within an address block leave Andreev invariant; swaps across blocks may offer more freedom, but require a new implementation and cost analysis. Neither observation rules out a more elaborate embedding inspired by the source.

## The concrete research target

Seek an input-independent exact identity

$$y_{b(a)}=B(y,a)+\sum_{\ell=1}^r u_\ell(y)v_\ell(a),$$

where $B$ has a cheap exact representation as a weighted sum of raw-input threshold gates, the $u_\ell$ are bounded-range affine table forms, and each product has a proved depth-two implementation. If both the main representation and total correction cost are $o(n^2)$, their scores can be combined in one output threshold. An exponent improvement also needs bottom gates with different signs inside some raw address blocks.

The target is stronger than low matrix rank: it asks for rank reduction together with a useful threshold basis. The original ETH matrix's support property is tailored to separability of a counting computation. An Andreev adaptation needs a support property tailored to threshold gates. This remains an open construction problem, not a claimed upper bound. It is the most relevant idea to retain from this investigation.

## A more concrete target using affine slices

The permutation entries in the SWAP expansion are conjunctions of equality constraints. This suggests connecting the matrix method to the repository's earlier mixed-sign affine-hyperplane constructions in `experiments/exact_creative_astra/report.md`, rather than to another unweighted staircase.

Here is a useful sufficient condition. Suppose the exact signed lookup admits

$$y_{b(a)}=\sum_{\ell=1}^R c_\ell y_{j_\ell}\,\mathbf1[L_\ell(a)=0],$$

where each $L_\ell$ is integer affine in the raw address bits. Then it has a depth-two threshold circuit with at most $2R$ bottom gates, since

$$y_j\mathbf1[L(a)=0]=\mathbf1[2L(a)+y_j\ge0]-\mathbf1[2L(a)-y_j\ge0].$$

This is exact for $y_j\in\{-1,1\}$ and integer $L(a)$; substituting $y_j=1-2x_j$ makes both gates affine in raw inputs. Coefficients $c_\ell$ go at the top. A constant or raw affine addition can likewise be handled at the top under the repository convention.

Conjunctions of bounded integer affine equalities can also be packed into one: if $|L_i(a)|\le B$ on Boolean inputs, then $\sum_i(2B+1)^iL_i(a)=0$ holds exactly when every $L_i(a)=0$. The largest nonzero digit dominates all smaller ones. Large positional coefficients need to be accounted for if imposing a weight bound, but are allowed in the unrestricted model.

This compiler makes equality-based decompositions a concrete route to mixed-sign gates. It does not produce a short decomposition: the ETH matrix bounds neither the number of these raw-address slices nor their required table dependence. If the matrix labels are logical address bits $b_i$, equality between labels is equality between block parities, not an affine equality of raw bits. If labels instead enumerate all raw address assignments, the matrix dimension becomes $2^{km}$ and its low relative rank can still be enormous. This dimension-versus-decoding issue must be resolved before the SWAP decomposition supplies a useful slice family. The earlier one-table-bit lower bounds also apply to this specific compiler; it is not an unrestricted architecture.

## Reproducible checks

Run `python3 experiments/eth_transfer/verify.py` from the repository root. It writes `verification.json` and uses exact rational or integer arithmetic, without external dependencies.

- For the genuine SWAP matrix on four pairs of two-dimensional registers, it verifies all 256 eigenvectors, their orthogonality, the spatial support property, and correction rank 13 for the interval $[0,2]$.
- For the translation adaptation it verifies the Fourier multipliers and spatial support, including the 18-dimensional residual and full sign reversal above.
- It exhaustively verifies the exact Fourier residual identity, including its parity-product implementation, on all 256 tables and 64 raw addresses of $A_{3,2}$: 16,384 input pairs. The main term is evaluated algebraically, not assigned a fictitious circuit cost.

These are finite checks of the stated identities. The symbolic arguments above explain their all-size scope; neither constitutes an independently reviewed or formalized new circuit upper bound.
