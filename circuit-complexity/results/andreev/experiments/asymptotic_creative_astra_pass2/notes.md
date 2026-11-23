# Creative asymptotic pass 2: working notes

Authors: Christian Reitwiessner

The objective is an exact depth-two real threshold circuit for balanced ordinary Andreev with $N=2^k$, $km\sim N$, and $o(N^2)$ bottom gates. No parity preprocessing is allowed.

Initial fresh directions to examine:

1. Group several independent table bits into a single multi-bit threshold interaction, seeking an amortized cost smaller than one channel per table bit. Account for the address predicates required by such grouping.
2. Replace independent masked Fourier ladders by a uniformly exact signed cubature or discrepancy construction. Test whether the arbitrary-table requirement forces an $\ell_1$ kernel condition and whether there is a tractable algebraic cancellation.
3. Use discrete derivatives of raw mixed-sign threshold gates. Address parity is a high-order character; derivatives might pack multiple table interactions into one gate, but extraction must be performed by the single top gate.
4. Exploit structured comparisons of encoded table integers with raw address sums, distinct from a few periodic global rank channels. Look for a local identity that survives carries and can be shared.

No claim of improvement is made at this stage. All costs will be evaluated with $m\asymp N/k$ before pursuing finite examples.

## Developed route: nonlinear compression of the table spectrum

A concrete way to attack the quadratic table-range cost is to replace each Walsh coefficient $h_S$ by an odd compressed code $\phi(h_S)$. This is not proposed as a completed circuit: address interactions still need raw-gate compilation and sharing. The immediate necessary condition is universal sign-correctness of $H\phi(Hy)$, even if all address characters were supplied for free. The test is stronger than checking average reconstruction error.

An exact 16-entry witness was found. Its Walsh spectrum consists of ten $-2$ entries and six $6$ entries, and its selected table bit at address zero is $+1$. Clipping all nonzero coefficients to magnitude one gives score $-4$. Tensoring with an all-one table gives a strict failure for every clipping bound $B<5N/24$, at arbitrarily large powers-of-two $N$.

More importantly, a different extension defeats EVERY fixed power compression $\phi(t)=\operatorname{sgn}(t)|t|^\alpha$, $0<\alpha<1$. Put the 16-entry table on one slice and fill all other slices with $+1$. For $N=16M$, its spectrum has one coefficient $16M-18$, $M-1$ coefficients $-18$, $9M$ coefficients $-2$, and $6M$ coefficients $6$. Its true selected bit at the zero address remains $+1$. The compressed score is

$$\phi(16M-18)+\phi(18)-M\bigl(\phi(18)+9\phi(2)-6\phi(6)\bigr).$$

For powers, the parenthesized defect is exactly

$$2^\alpha(3^\alpha-3)^2>0.$$

Consequently the $\Theta(M)$ negative defect eventually beats the $O(M^\alpha)$ positive term. This gives an explicit asymptotic counterexample, not an extrapolation from a small instance.

The same construction tests general odd shrinkers through one fixed three-scale inequality. In particular it can falsify logarithmic compression as well. Next: verify the spectrum formula, formulate precise quantifiers (fixed shrinker versus $N$-dependent shrinker), and analyze whether simple uniform linear repairs actually repair the failure without restoring linear coefficient range.
