# Exact decoding from adaptive slabs

Authors: Christian Reitwiessner

Date: 13 November 2026

## Outcome

The adaptive-slab proposal now has an exact dense-table decoding identity. It yields a binomial-shaped address window. Plain alternating shifts annihilate this window, but polynomially weighted alternating shifts restore parity exactly. The resulting implementation still costs linearly many address centers for a fixed table-code size; it does not improve the Andreev upper bound.

Two bounded dictionary searches also produced complete arbitrary-table circuits made only of dense three-table-bit adaptive slabs and a raw affine table term. Their integer coefficients pass independent exhaustive checks. They are expensive feasibility witnesses, not finite records or scalable constructions. The results strengthen the previous note's building-block analysis without resolving its global gate-sharing problem.

## 1. An exact dense-table decoder

Fix odd $t\ge3$, let $q=(t-1)/2$, and take table signs $y\in\{-1,1\}^t$. Choose one representative of each pair $\{\alpha,-\alpha\}$ of sign vectors; for example

$$\mathcal R=\{\alpha\in\{-1,1\}^t:\alpha_1=1\}.$$

For an integer raw-address affine form $L$, define

$$H_\alpha(y)=\sum_{j=1}^t\alpha_jy_j,\qquad
E_\alpha(y,L)=[2L+H_\alpha\ge0]-[2L-H_\alpha\ge0].$$

Each $H_\alpha$ is odd, and each $E_\alpha$ uses two bottom gates. The exact identity is

$$\boxed{\sum_{\alpha\in\mathcal R}\alpha_iE_\alpha(y,L)
=K_t(L)y_i,\qquad K_t(L)=\binom{t-1}{q+L}.}$$

The binomial coefficient is zero outside its usual index range. For $t=3$, the kernel has values $1,2,1$ at $L=-1,0,1$. For $t=5$, its values are $1,4,6,4,1$ on $[-2,2]$.

**Proof.** Since all relevant arguments are odd,

$$E_\alpha(y,L)=\tfrac12\bigl(\operatorname{sgn}(H_\alpha+2L)+
\operatorname{sgn}(H_\alpha-2L)\bigr).$$

First sum over the entire sign cube and substitute $z_j=\alpha_jy_j$. For a fixed choice of the other $t-1$ signs, with even sum $s$, summing over $z_i$ gives

$$\operatorname{sgn}(s+1+2L)-\operatorname{sgn}(s-1+2L)
=2[s=-2L].$$

There are $\binom{t-1}{q-L}=K_t(L)$ such choices. The shift $-2L$ gives the same count. Thus the full-cube sum is $2K_t(L)y_i$. Terms indexed by $\alpha$ and $-\alpha$ coincide, giving the representative identity.

This proves exact cancellation of nonlinear table dependence. The same bank of gates supplies each coordinate through a different fixed linear readout. Choosing that readout according to the parity address is not free: it is part of the unresolved lookup problem. The identity must not be interpreted as computing all table bits and then supplying them to another circuit layer.

## 2. Why the first parity attachment vanishes

A natural proposal is to attach parity by alternating the centers of these decoded windows. It fails exactly:

$$\sum_{u=-q}^{q}(-1)^uK_t(u)=0.$$

Indeed the kernel's generating function is $z^{-q}(1+z)^{t-1}$, which vanishes at $z=-1$. Consequently

$$\sum_r(-1)^rK_t(L-r)=0$$

whenever the center range contains the full kernel support around $L$. This is a local algebraic cancellation, not an asymptotic or numerical failure. In fact, for every polynomial $p$ of degree less than $t-1$,

$$\sum_r(-1)^rp(r)K_t(L-r)=0.$$

This scoped obstruction applies to the binomial decoder with these center weights. It does not rule out irregular centers, different table codes, or a joint score that avoids reconstructing individual parity products.

## 3. Higher-degree weights restore parity

The same calculation supplies an exact repair:

$$\boxed{\sum_r(-1)^r r^{t-1}K_t(L-r)
=(-1)^{L+q}(t-1)!.}$$

Substitute $u=L-r$. The alternating binomial sum is a finite difference of order $t-1$. It annihilates lower powers and evaluates the leading power to the displayed factorial and sign. Therefore

$$\sum_r\sum_{\alpha\in\mathcal R}
(-1)^r r^{t-1}\alpha_iE_\alpha(y,L-r)
=(-1)^{L+q}(t-1)!y_i.$$

If $L$ is a signed sum with odd address coefficients, its parity is the required parity of the selected raw bits. Thus this is a genuine exact product construction with mixed address signs, dense table tests, and one final linear combination.

The cost is the problem. If $L$ ranges from $\ell$ to $h$ and $D=h-\ell$, it suffices to include centers $r\in[\ell-q,h+q]$. There are $D+t$ centers, $2^{t-1}$ representative table rows, and two gates per atom, giving at most

$$2^t(D+t)$$

bottom gates. For fixed $t$ this is linear in the address range, as in the old ladders. Large polynomial coefficients only affect weights, not the number of required centers. In this construction the restoration does not provide the cross-character sharing needed for a better Andreev bound.

## 4. Complete finite circuits from the proposed atom class

The search considered $k=2$, so the table contains four independent bits. Every table form is a signed sum of three of the four table signs, modulo overall sign. Every address form is

$$L(a)=\sum_{j=1}^m\sigma_ja_{1,j}
+s\sum_{j=1}^m\tau_ja_{2,j}-c,$$

where both sign masks contain both signs and $s\in\{1,2,3\}$. Overall sign duplicates are removed. Atoms are the two-gate $E(H,L)$ above, with arbitrary signed top coefficients. Four raw table-sign coefficients are also allowed at the top.

For $m=3$, centers range over all integer values that can give a nonzero atom. The pool contains 8,640 distinct atom truth tables. A 30-second-budget linear program minimizes the L1 norm of atom coefficients subject to strict signed margin at least one; it does not minimize gate count. It completed and produced 189 nonzero atoms, hence at most 378 bottom gates before merging.

For $m=4$, all slabs are centered at the midpoint of their address form: $c=\frac12\sum w_j$. This more structured pool contains 4,704 distinct atoms. The same optimization completed within its 30-second budget and produced 461 atoms, hence at most 922 unmerged bottoms.

Both circuits are substantially larger than the known small-instance constructions. Their purpose is to check that the dense-table adaptive-slab architecture can actually decode every independent table and raw address, rather than merely pass singleton-table or coverage tests. They provide no evidence for a better asymptotic bound.

Because the atoms, target, and raw table terms are odd under table complement, imposing the constraints on one representative of each complementary table pair suffices. The final verifier nevertheless checks all tables. Multiplying the floating-point coefficients by $10^6$ and rounding gives integer certificates; correctness is then established separately with Python integer arithmetic, not by the LP status or tolerances.

- `slab_certificate_m3.json`: all 1,024 raw table/address inputs pass, with minimum signed score 999,998.
- `slab_certificate_m4_centered.json`: all 4,096 inputs pass, with minimum signed score 999,988.

The top outputs $[-F\ge0]$ because the certificates use $y_c=1-2x_c$. Both certificates have incompatible within-block sign patterns, so no common raw-input reorientation makes the entire circuit coherent. All stated counts exclude the one top gate and allow the raw table term at that gate.

## 5. What this changes about the next target

The dense-table cancellation is now explicit, and its straightforward parity attachment has both a precise failure and an exact repair. The independent-center implementation still incurs the full address-range cost. The most useful remaining question is whether *different decoded products can share these centers or raw gates*, or whether a joint sign score can avoid decoding the products separately.

The LP witnesses show finite feasibility of one concrete joint atom class. Their sizes and unstructured coefficients do not suggest an all-size rule. Any further search should be directed at shared patterns or a symbolic identity; repeating larger unconstrained dictionary fits would not establish a construction.

## Reproduction

`python3 experiments/noncoherent_routes/followup_checks.py` uses only the standard library. It checks the decoder on 9,304 parameter/input cases, the parity cancellation, 63 higher-degree restoration cases, and both complete integer circuits. Results are in `followup_verification.json`.

The optional discovery script `slab_search.py` requires NumPy and SciPy. Run it with `--m 3 --seconds 30` or `--m 4 --seconds 30 --centered`. It uses `scipy.optimize.linprog(method='highs')` with the documented time limit. Search metadata and dependency versions are recorded in `slab_search_m3.json` and `slab_search_m4_centered.json`. Optimizer versions may produce different witnesses; the saved certificates are checked independently.
