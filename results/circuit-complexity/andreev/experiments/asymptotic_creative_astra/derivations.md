# Structural scratch derivations

Authors: Christian Reitwiessner

This file records research attempts, not established asymptotic improvements.

The balanced model is $N=2^k$, $m=\lfloor N/k\rfloor$, $n=N+km\sim2N$.

Initial independent directions:

1. Encode the entire table as a large affine integer, and turn parity addressing into a rank/digit query. Obstruction: a single threshold only cuts an order once; the needed bit extraction has input-dependent positions. No valid two-layer extraction identity yet.
2. Express the arbitrary table as Walsh coefficients, but replace full parity ladders by signed, localized ladders over many raw-coordinate views. The useful target is exact cancellation of the *whole inverse Walsh kernel*, rather than coordinatewise approximation. An exact kernel needs diagonal dominance on every address; mean-square estimates are insufficient.
3. Construct a new threshold representation of parity with fewer than linearly many gates and a strong numerical identity, then share it across table characters. Merely computing parity in sign does not permit composition. A bounded-error numerical identity, strong enough for simultaneous arbitrary table coefficients, would be needed.
4. Use large-weight table-dependent hyperplanes to implement rank identities with many address columns at once. Direct flattening is exponential in the number of columns. A useful construction must sum out internal ranks without charging their full Cartesian product.
5. Use nonuniformly weighted random views and exact finite-difference identities to build kernels whose off-diagonal coefficients cancel, including kernels with negative lobes. This escapes one-sided cover accounting, but requires an explicit raw-coordinate ridge representation and a uniform norm certificate.

Early accounting: a character-wise ladder of length $m|S|$ has total cost $m k2^{k-1}=\Theta(N^2)$ at balance. A family of $L$ localized views of width $W$ per character costs $O(LWN)$, so a useful mechanism must give $LW=o(km)$ while controlling the full kernel for every raw address.

## Modular rank channels

For any integer $0\le T\le D$,

$$\sum_{r=0}^{D}[T+x_{r\bmod Q}\ge r+1]-T=x_{T\bmod Q}.$$

With $Q=N$, $T=\sum_i2^i\sum_j a_{i,j}$, $D=m(N-1)$, this is an exact $O(mN)=O(n^2/\log n)$ circuit for the *wrong*, carry-contaminated lookup. It is not an Andreev upper bound.

Generalization: let $h_r(x)=[\ell_r(x)\ge0]$ where $\ell_r$ is integer affine and never zero, and let $M>\max_{r,x}|\ell_r(x)|$. Then

$$\sum_{r=0}^{D}[2M(T-r)+\ell_{r\bmod Q}(x)\ge0]-T=h_{T\bmod Q}(x).$$

Thus one rank channel can retrieve an arbitrary threshold-encoded table bit at an affine modular address, using $D+1$ raw-input bottom gates and a direct top term $-T$. No modulo operation is a free input.

Candidate: $L$ channels, each using a different mixed raw-coordinate sign pattern and a positional ordering of blocks, query fixed threshold encodings of the table. A fixed signed top vote should recover $x_b$. If the required threshold code exists with $L=o(k)$, the gate count is $o(N^2)$; $L=O(\log k)$ would give $O(N^2\log k/k)$.

Important falsification: for channels that merely permute the original table, $L<\log_2m$ cannot work by a signed vote alone. In each block choose two raw coordinates having the same $L$-bit sign signature. Activate either both or neither. Every such address has parity zero. In any one positional channel, the $2^k$ pair-activation choices map uniformly onto one coset of the even residues modulo $N$, with two preimages per residue. Each channel therefore queries table location zero on at most two choices. If $2L<N$, some choice queries zero in no channel. Flipping only $x_0$ then leaves the entire channel vector unchanged. This argument allows arbitrary fixed table permutations and arbitrary signed top weights. It does not cover arbitrary threshold-encoded rows or a direct table term at the top.
