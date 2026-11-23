# Independent verification of construction (d): depth-2 threshold circuit for Andreev's function with N²/2 + (3/4)kmN + O(N+km) gates

**Verdict: the claim is correct.** The identities and closed forms hold; an independent re-implementation (from the mathematics only, `constr_d.py` was not read until after my code worked) is correct on every input tested; every gate is a genuine single threshold gate on the raw inputs; the exact gate count is the claimed formula 5. In the balanced case km = N the count is (5/16)n² + O(n) as n → ∞. No error was found. Minor points are in §5.

Notation: N = 2^k, n = N + km, x' = (x_c)_{c≠0}, |x'| = Σ_{c≠0} x_c, σ = Σ s_i, T_S = |S|m, t_S = Σ_{i∈S} s_i, e_S = t_S mod 2, Y_S = #{c≠0 : x_c = 1, S·c odd}. S ranges over nonempty subsets of [k] unless stated; S·c = parity of |S∩c|. Throughout, "S·c odd" for c≠0 holds for exactly N/2 sets S, and for two distinct nonzero c, c′ (linearly independent over F₂) exactly N/4 sets S have S·c and S·c′ both odd. Also b_i = s_i mod 2, so (−1)^{t_S} = (−1)^{S·b}.

## 1. Proofs (part a)

**(I1) Polarization identity.** Since ⌈(2Y+t)/2⌉ = Y + ⌈t/2⌉,
⌈(2Y+t)/2⌉² − Y² − ⌈t/2⌉² − Yt = 2Y⌈t/2⌉ − Yt = Y(2⌈t/2⌉ − t) = Y·(t mod 2).
Hence, using (−1)^t = 1 − 2(t mod 2): 4Y(−1)^t = 4Y − 8Y(t mod 2) = 4Y − 8⌈(2Y+t)/2⌉² + 8Y² + 8⌈t/2⌉² + 8Yt. ∎ (Also brute-forced for 0 ≤ Y,t < 200.)

**(I2) Odd-threshold staircase.** f(u) = ⌈u/2⌉². f(2r) = f(2r−1) = r², f(2r+1) = (r+1)². So the step f(θ) − f(θ−1) is 0 for θ = 2r (even) and 2r+1 = θ for θ odd. Thus f(u) = Σ_{θ odd, 1≤θ≤u} θ·[u ≥ θ]. For u ∈ [0, M] this needs ⌈M/2⌉ gates. Here u = 2Y_S + t_S ∈ [0, N + T_S] (Y_S ≤ N/2 exactly), giving N/2 + ⌈T_S/2⌉ gates (N even), and t_S ∈ [0, T_S] gives ⌈T_S/2⌉. Both gate forms are 0/1/2-weight forms on raw inputs: weight 2 on x_c (c≠0, S·c odd), weight 1 on every bit of the blocks i ∈ S. ∎

**(I3) Sums over S.**
* Σ_S Y_S = Σ_{c≠0} x_c·#{S: S·c odd} = (N/2)|x'|.
* Σ_S Y_S² = Σ_{c,c′≠0} x_c x_{c′} #{S : S·c, S·c′ odd} = (N/2)|x'| + (N/4)(|x'|² − |x'|) = (N/4)(|x'|² + |x'|). (Diagonal c = c′: N/2; off-diagonal: N/4.)
* Σ_S Y_S t_S = Σ_{c≠0} x_c Σ_i s_i #{S : i ∈ S, S·c odd}. The count is N/2 if c = e_i (i∈S ⇔ S·e_i = 1) and N/4 otherwise (e_i, c independent). So = (N/4)|x'|σ + (N/4)Σ_i x_{e_i} s_i.
* Σ_S t_S = (N/2)σ, Σ_S t_S² = (N/4)(σ² + Σ s_i²) (same counts; the latter is not used in (d)).
All four were also brute-forced over all tables and all block weights for (k,m) = (1,3), (2,2), (3,1) and on random samples for (3,3), (4,3), (5,2) (`algebra.py`). ∎

**(I4) Character sums.** Σ_{all S⊆[k]} (−1)^{S·v} = N[v=0], so Σ_{S≠∅} (−1)^{S·v} = N[v=0] − 1.
Y_S = Σ_{c≠0} x_c (1 − (−1)^{S·c})/2, so
Σ_{S≠∅} Y_S(−1)^{S·b} = ½ Σ_{c≠0} x_c [(N[b=0] − 1) − (N[b=c] − 1)] = (N/2)([b=0]|x'| − [b≠0]x_b).
(For b ≠ 0 the term c = b is the only one with [b=c]=1 and x_b is a non-address-zero entry; for b = 0, [b=c]=0 for all c≠0.)
Therefore 4Σ_S Y_S(−1)^{t_S} = 2N[b=0]|x'| − 2N[b≠0]x_b.

**(I5) Gated parity.** (−1)^t = 1 − 2t + 4⌊t/2⌋ and ⌊t/2⌋ = Σ_{j=1}^{⌊T/2⌋}[t ≥ 2j] for 0 ≤ t ≤ T. With B > T: [t + Bx₀ ≥ 2j + B] = x₀·[t ≥ 2j] (if x₀ = 0: t ≤ T < B < 2j+B; if x₀ = 1: t ≥ 2j). So x₀(−1)^{t_S} = x₀ − 2x₀t_S + 4Σ_j [t_S + Bx₀ ≥ 2j+B]. Likewise x₀σ = Σ_{l=1}^{km}[σ + Bx₀ ≥ l+B] and x_{e_i}s_i = Σ_{l=1}^{m}[s_i + Bx_{e_i} ≥ l+B] (B > km ≥ m). Using Σ_{S≠∅}1 = N−1 and Σ_S t_S = (N/2)σ:
−2N x₀ Σ_{all S}(−1)^{t_S} = −2N x₀ − 2N[(N−1)x₀ − Nσx₀ + 4Σ_SΣ_j gate] = −2N²x₀ + 2N²σx₀ − 8N Σ_SΣ_j [t_S + Bx₀ ≥ 2j+B].
By (I4)-type reasoning, −2N x₀ Σ_{all S}(−1)^{t_S} = −2N² x₀[b=0]. ∎

**(I6) |x'|·σ as staircases.** 4|x'|σ = (|x'|+σ)² − (|x'|−σ)². z² = Σ_{θ=1}^{z}(2θ−1) = Σ_{θ≥1}(2θ−1)[z ≥ θ]. For p = |x'|+σ ∈ [0, N−1+km]: N−1+km gates. For q = |x'|−σ ∈ [−km, N−1]: q² = Σ_{θ=1}^{N−1}(2θ−1)[q ≥ θ] + Σ_{θ=1}^{km}(2θ−1)[−q ≥ θ], N−1+km gates; weights ±1 on raw inputs. 2N|x'|σ = (N/2)(p² − q²), N/2 is an integer. Also |x'|² + |x'| = Σ_{θ=1}^{N−1} 2θ[|x'| ≥ θ]. (Brute-forced for p,q<60.) ∎

**(I7) Final closed form.** Define
P = N + Σ_{S≠∅}4Y_S(−1)^{t_S} − 2N²x₀[b=0].
By (I4): for b ≠ 0, P = N − 2N x_b; for b = 0, P = N + 2N|x'| − 2N²x₀ = N − 2N x₀ + 2N|x| − 2N²x₀ (as |x| = |x'| + x₀). Both are N − 2Nx_b + [b=0](2N|x| − 2N²x₀). Margins: b≠0: P = ±N. b=0, x₀=0: P = N + 2N|x'| ≥ N. b=0, x₀=1: P = N + 2N|x'| − 2N² ≤ N + 2N(N−1) − 2N² = −N. So output [P<0] equals x_b always, with |P| ≥ N. ∎

**(I8) P is a linear form in (gates, inputs).** Expand by (I1):
P = N + Σ_S[4Y_S − 8⌈u_S/2⌉² + 8Y_S² + 8⌈t_S/2⌉² + 8Y_St_S] − 2N x₀ Σ_{all S}(−1)^{t_S}.
With (I2),(I3),(I5),(I6):
* 4ΣY_S + (from 8ΣY_S² the |x'| part): free linear terms, coefficient 4N on each x_c, c≠0 (2N from 4ΣY_S; 2N from 2N(|x'|²+|x'|)); in my implementation |x'|² is the staircase with coefficients 2N(2θ−1) and the |x'| part is the linear term.
* ridge gates [2Y_S+t_S ≥ θ], θ odd ≤ N+T_S, coefficient −8θ; residue gates [t_S ≥ θ], θ odd ≤ T_S, coefficient +8θ; override gates [t_S + Bx₀ ≥ 2j+B], coefficient −8N.
* [p ≥ θ] with +(N/2)(2θ−1); [q ≥ θ] and [−q ≥ θ] with −(N/2)(2θ−1); [s_i + Bx_{e_i} ≥ l+B] with +2N; [σ+Bx₀ ≥ l+B] with +2N²; direct x₀ term −2N².
Every coefficient is an integer. The top gate is [−(P−N) ≥ N+1], i.e. v = −coef, direct weights −lin, threshold N+1. Nothing is a product of two things: each "term" is a gate or a direct input.

## 2. Implementation (part b) — `impl.py`
Written from the above, without reading `constr_d.py`/`common.py`. Bottom gates are explicit (integer weight vector on the n raw bits, integer threshold); the top gate is an explicit integer weight vector over gates plus a vector over the n inputs plus a threshold. Evaluation: bottom gates and top gate by exact integer data in float64 (all values < 2^50, asserted, so exact), cross-checked by a pure-Python big-integer evaluator (`audit.py`). The target A(x,a) is computed independently from the block weights.

Bottom weights are in {0,1,2} plus a gating weight B = N+km+2 and ±1 for the p,q forms. Max top coefficient: 64768 at (7,3), 16000 at (6,6) (the report quotes 65024 for (7,3); the difference is how |x'|²+|x'| is split, immaterial).

## 3. Test table (parts b, d)
All entries: wrong = 0 outputs, and the top sum P equals the closed form N − 2Nx_b + [b=0](2N|x|−2N²x₀) **exactly at every input**, min|P| = N exactly.

**Exhaustive, all 2^n inputs, n ≤ 20: every (k,m) with n ≤ 20, 31 pairs, for both (d) and (c)** (62 runs, `exhaustive.log`): k=1, m=1..18; k=2, m=1..8; k=3, m=1..4; k=4, m=1. Max n = 20 (2^20 inputs each). Representative lines:

| (k,m) | n | gates (d) | gates (c) | inputs | wrong | P = closed form |
|---|---|---|---|---|---|---|
| (2,2) | 8 | 43 | 36 | 2^8 | 0 | yes |
| (3,3) | 17 | 141 | 153 | 2^17 | 0 | yes |
| (3,4) | 20 | 169 | 188 | 2^20 | 0 | yes |
| (4,1) | 20 | 233 | 320 | 2^20 | 0 | yes |
| (2,8) | 20 | 127 | 108 | 2^20 | 0 | yes |
| (1,18) | 20 | 103 | 65 | 2^20 | 0 | yes |

**Structured adversarial + random** (`adversarial.py`, `b0_focus.py`): for each b (all N values if N ≤ 64, else 64 incl. 0, every e_i, N−1) × 4 block-weight modes (all-minimal-parity weights, all-maximal-parity weights, random-parity-correct, mixed extremes) × ~40 tables (all-zeros, all-ones, x₀=0 & rest 1, only x₀, single-1 and single-0 at c ∈ {0,b,1,N/2,N−1}, random densities 0.1/0.5/0.9, tables with |x'| ∈ {0,1,N/2,N−2,N−1} and x₀ ∈ {0,1}) plus 6k–20k fully random inputs. Plus a b=0-only sweep over every |x'| ∈ [0,N−1] × x₀ ∈ {0,1} × 3 even-weight modes.

| (d) (k,m) | n | gates | gates after merging identical gates | inputs tested | wrong |
|---|---|---|---|---|---|
| (3,5) | 23 | 201 | 194 | 21312 | 0 |
| (3,6) | 26 | 229 | 220 | 21312 | 0 |
| (4,2) | 24 | 293 | 289 | 22656 | 0 |
| (4,3) | 28 | 361 | 355 | 22656 | 0 |
| (4,4) | 32 | 421 | 413 | 22656 | 0 |
| (4,6) | 40 | 549 | 537 | 22656 | 0 |
| (4,8) | 48 | 677 | 661 | 22656 | 0 |
| (5,3) | 47 | 1017 | 1010 | 25344 | 0 |
| (5,4) | 52 | 1149 | 1139 | 25344 | 0 |
| (5,5) | 57 | 1297 | 1285 | 25344 | 0 |
| (5,6) | 62 | 1429 | 1414 | 25344 | 0 |
| (6,3) | 82 | 3157 | 3148 | 16720 | 0 |
| (6,4) | 88 | 3453 | 3441 | 16720 | 0 |
| (6,6) | 100 | 4077 | 4059 | 16720 | 0 |
| (7,2) | 142 | 9909 | 9902 | 15040 | 0 |
| (7,3) | 149 | 10641 | 10631 | 16048 | 0 |
| (8,1) | 264 | 35037 | 35033 | 16888 | 0 |

Same for (c) at (3,5), (4,3), (4,6), (5,3), (5,5), (6,3), (6,6): all correct, exact closed form (`adv_c.log`). b=0 sweep for (2,3),(3,3),(4,4),(5,5),(6,3),(6,6),(7,3): min P over x₀=0 equals N exactly, max P over x₀=1 equals −N exactly (the margin is tight and attained, so there is no hidden slack). Pure-Python exact-integer evaluator: 1500 inputs each on 5 sizes for (d) and for (c), 0 errors.

## 4. Gate count (part c)
Exact count of my implementation (explicit bottom gates, before any merging):
G_d(k,m) = Σ_{∅≠S}(N/2 + 2⌈|S|m/2⌉ + ⌊|S|m/2⌋) + 3(N−1) + 4km,
verified equal to the built circuit for all 17+ (k,m) built, including (3,3)=141, (4,4)=421, (5,5)=1297, (6,6)=4077, (7,3)=10641, which coincide with the report's table. Breakdown by row: ridge N/2+⌈T/2⌉, residue ⌈T/2⌉, override ⌊T/2⌋ per S; |x'|² staircase N−1; p² and q² staircases 2(N−1+km); x_{e_i}s_i gates km; x₀σ gates km.

Asymptotics: Σ_{S≠∅} N/2 = N(N−1)/2; Σ_S (3T_S/2 + [T_S odd]/2) = (3/4)kmN + O(N); so G_d = N²/2 + (3/4)kmN + O(N+km) exactly, with explicit remainder 3N − 3 + 4km − N/2 + (1/2)#{S: |S|m odd}. Balanced km = N: G_d = (5/4)N² + O(N) = (5/16)n² + O(n). Exact ratio G_d/n² in the balanced case: k=1: 0.94; k=2: 0.67; k=4: 0.411; k=8: 0.3188; k=16: 0.31252 (→ 5/16 = 0.3125; formula-evaluated for k=16, not built). So the constant 5/16 is only an asymptotic statement: at the n tested (≤ 264) the lower-order O(N+km) terms still matter (e.g. 0.408 n² at n = 100, vs 0.3125); for tiny n, (d) is bigger than the older constructions (as the report says).

**No hidden non-threshold gates.** Audited: (i) all gates have the form [w·z ≥ θ] with w an integer vector on the n raw bits; none is a product or a polynomial. (ii) None is constant (θ strictly inside (min w·z, max w·z]); `const_gates` = 0 in every audited size. (iii) Every nonlinear quantity (ceil²-ridge, |x'|², |x'|σ, x₀·(...), x_{e_i}s_i) is expressed in the top gate as an integer-coefficient *linear* combination of such gates; the only "free" terms are direct input weights (4N on x_c for c≠0, −2N² on x₀), allowed by the problem statement. If the top gate were *not* allowed to read inputs, n identity gates would be added: +n = O(n), which does not change the n² constant. (iv) Weight sizes: bottom weights ≤ B = N+km+2 (poly(n)); top coefficients ≤ ~4N² (65k at k=7). No exponential weights.

**Duplicate gates (improvement).** The gates [σ + Bx₀ ≥ l+B] coincide with the S=[k] override gates [t_{[k]} + Bx₀ ≥ 2j+B] for even l (t_{[k]} = σ). Merging identical (weight, threshold) pairs (summing top coefficients) removes ⌊km/2⌋ gates, a purely lower-order saving: e.g. (6,6): 4077 → 4059. This is correct (checked: rows "after merging" above). The report's formula does not use it, so its count is an upper bound on the optimum in this family.

## 5. Part (d): construction (c), N² + (5/4)kmN
Re-derived from scratch. Identity φ(u) = (−1)^u u = Σ_{θ=1}^{u}(−1)^θ(2θ−1) gives 2Y(−1)^t = φ(2Y+t) − φ(t) (since (−1)^t(2Y+t) − (−1)^t t). So 4Y(−1)^t = 2φ(2Y+t) − 2φ(t): N + T_S gates for the first (all thresholds), T_S for the second. Together with the same gated-parity override: G_c = N(N−1) + Σ_S(2T_S + ⌊T_S/2⌋) + km = N² + (5/4)kmN + O(N+km) (my version, 153 at (3,3), 576 at (4,4), 2009 at (5,5), 6948 at (6,6)). With the same duplicate-gate merging as above (⌈km/2⌉ instead of km), the counts are 149, 568, 1997 — exactly the report's numbers, which it obtains by that merging. Verified exhaustively (n ≤ 20, 31 pairs) and adversarially as in §3, exact closed form at every input. The report's (c) claim is correct; balanced: (1 + 5/4)N² = (9/16)n².

## 6. Minor remarks / what was not checked
* The report's wording "gate count … 5/16 n²" is asymptotic (see §4); the exact formula and its remainder are fine.
* The report's `P = N − 2N x_b + …` and margin N are exact (tight), not just a bound.
* Not checked: optimality (lower bounds), and the "what did not work" section's claims; also the problem's comparison to the literature (what the previous best known bound is) — outside the scope of this verification. Only the stated upper bound was checked.
* Sampled, not exhaustive, above n = 20 (as expected: 2^n too large); there the *algebraic proofs* (I1–I8) are what cover all inputs, and the exact closed-form match P = N − 2Nx_b + … on ~10⁵ structured inputs is a check of the proof, not a replacement for it.

Files: `impl.py` (my circuits), `exhaustive.py/.log`, `adversarial.py` (`adv_d.log`, `adv_c.log`), `b0_focus.py`, `algebra.py`, `audit.py` (`audit.log`).
