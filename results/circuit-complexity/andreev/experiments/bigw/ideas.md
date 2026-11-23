# What large weights can and cannot buy (2026-11-06)

## Primitives that only large weights give
1. Gated threshold: [B*x_c + L(s) >= B + th] = x_c AND [L(s) >= th]. More generally, for a form l of range R_l:
   [B*l + L >= ...] packs l and L lexicographically.
2. Line-equality: g(Bq+r) - g(B(q+1)) = [L1 = q] AND [L2 >= r]. This corrects a single level set of L1.
3. Decision lists at the top: top weights +-2^{-j} realize "first gate that fires decides".
   So THR∘THR contains decision lists of LTFs, and an "abstain" architecture is possible:
   sign(M*P1 + P2), where P2 only matters when P1 = 0.
4. Injective encodings: a form B*u + v determines (u, v) completely.

## Cost law (key observation)
A staircase in one linear form costs #jumps along that form. If L = B*u + v packs two forms
injectively, then every additive target g1(u) + g2(v) has about range(u)*jumps(g2) jumps.
So packing multiplies costs. The character score Sum_S Y_S chi_S(b) is additive across characters.
Large weights therefore cannot help by packing characters. They help only for:
 - gating by forms of tiny range R_l (R_l = 1: a single table bit), at a cost of about R_l * jumps;
 - genuinely non-additive targets: comparisons, priorities, abstention.

## Ruled out quickly (proof sketches)
- Pure-sign Fourier: sign(Sum_S alpha_S (-1)^{lambda_S(x)} chi_S(b)) with cheap parities lambda_S.
  We would need a cube bijection eps -> sign(H diag(alpha) eps + c) whose coordinates are LTFs and
  whose inverse is GF(2)-affine. That forces a signed permutation, which in turn forces one
  dominant alpha per row b. Impossible already for N=2.
- Per-table-bit gating: A = sign(Sum_c x_c F_c(s) + G(s)), where F_c is built from gated thresholds.
  This needs F_{b(s)}(s) > Sum_{c != b(s)} F_c(s) for all s. So F_c must resolve the full
  checkerboard [b = c]. Doing that with thresholds costs about kmN/4 per c, i.e. N^2 km/4 in total.
- Lex-packing two characters into one ridge: by the cost law, about R*T per pair.

## Still open, and where large weights are plausibly useful
- Gating by small-range forms, so that the k+1 special addresses {0, e_1..e_k} (where the 5/16
  residue and override live) are handled together. Assigned to the upper-bound delegate (idea 1).
- Abstain/priority top: P1 = cheap coarse score that is exactly 0 when unsure; P2 = correction.
  Example: P1 = Andreev on the folded table u+v (k-1 blocks). This is exact only when u = v,
  so it buys nothing unless P1 can be made cheaper than exact by exploiting the 0-level set.
- Few-level coefficients: sign(Sum_S A_S(x) chi_S(b)) with A_S taking 3 levels.
  3^N >= 2^N cones could be met, but each level change costs about T_S, giving about N^2 balanced.
  That is worse than the ridge (the ridge gets the whole Y-range in one diagonal).

## Data: does a weight bound change the exact minimum?
k=2, m=1 (full model, top weights unbounded): 3 gates already with bottom weights in {-1,0,1}.
So that circuit is MAJ-bottom, and large bottom weights do not help there.
k=2, m=2 with W=1,2 and k=3, m=1 with W=1,2: running (wmin.py, logs k2m2.log, k3m1.log).
