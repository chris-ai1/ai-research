# Worst-case THR∘THR bounds for Andreev's function: improvements and barriers

Notation as in `andreev_depth_two_bounds.md`: N = 2^k, m = N/k, n = 2N, A(x,a) = x_b, b_i = parity(a_i).
Status before: Ω(n^{3/2}/log³ n) gates, Ω(n^{5/2}/log^{7/2} n) wires (Kane–Williams) vs (5/4)n² gates.

Source: a Fable consultation (report and code in /tmp/fable_work/). Its proof of Theorem A had a counting
error that reduces the bound to Ω(N). The corrected proof below recovers the claimed bound.

## Theorem A. Every THR∘THR circuit for A_n has s = Ω(N^{3/2}/k²) = Ω(n^{3/2}/log² n) bottom gates.

The circuit may have arbitrary real weights and direct input wires to the top gate.

*Restriction.* Independently in each block i, the restriction ρ picks a uniform free position J_i
(variable z_i) and assigns uniform random values to the other m−1 positions. Then
A(x, ρ(z)) = x_{z⊕c(ρ)}, and as z ranges over {0,1}^k this determines x.

*Survival.* Gate g_j = [α_j·x + β_j·a ≥ θ_j] restricts to [β_{j,J}·z ≥ τ_j(x, a_F)].
- The weights β_{j,J} depend on ρ only; x and a_F only move the threshold.
- A gate survives if the restricted gate is not constant.
- KW's Littlewood–Offord lemma (with errata E1–E3) gives, for every fixed x, Pr_ρ[g_j survives] ≤ c₀k/√N.
  Here x only shifts the window, so the bound is uniform in x.

*Counting.* Let B = c₀sk/√N. Then E_ρ|Q(x,ρ)| ≤ B for every x, so Markov plus averaging over x gives a single
ρ* for which X* = {x : |Q(x,ρ*)| ≤ 2B} has |X*| ≥ 2^{N−1}. We may assume s < N², since otherwise the theorem holds.
For x ∈ X*, encode the restricted circuit as follows:
1. the list of surviving gates: ≤ 2B indices, each ≤ log₂ s ≤ 2k bits;
2. for each survivor, which of its ≤ 2^k threshold classes τ falls in: k bits each. Its weight vector
   β_{j,J} is fixed by ρ*;
3. the top gate. Non-surviving gates are constants, so they fold into the top threshold, as do γ·x and
   δ_F·a_F. The top weights on survivors and the weights δ_J are fixed by ρ*. So only the class of the
   effective threshold among the ≤ 2^{2B+k} values of Σ_{j∈Q} w_j g_j + δ_J·z needs recording: 2B + k + 1 bits.

This encoding determines z ↦ x_{z⊕c} and hence x. So
  N − 1 ≤ 2B(2k + k + 1) + k + 1, which gives s ≥ Ω(N^{3/2}/k²). ∎

What changed from KW: a survivor costs O(k) bits, namely its index and threshold class, instead of the
Θ(k²) bits needed to name an arbitrary LTF on k variables. This works because ρ* is fixed before
counting over x.

(The Fable draft also recorded the 2^s pattern of constant gates and the full survivor set as an s-bit mask,
paying 3s bits. That only yields s = Ω(N). The index-list encoding above avoids this.)

## Theorem A'. Wires w = Ω(N^{5/2}/k^{5/2}) = Ω(n^{5/2}/log^{5/2} n).

Say a gate survives if it depends on ≥ 2 free variables. KW's wire lemma (with erratum E5) gives
E|Q| ≤ B_w = c₀wk^{3/2}/N^{3/2}. A gate depending on ≤ 1 free variable is a constant or a literal z_i or ¬z_i. Sum
these into the top form, so the top becomes an arbitrary LTF over (survivors, z). Since the survivor
functions are fixed by items 1–2, there are ≤ (2^k)^{2B_w+k+1} such LTFs, i.e. k(2B_w + k + 1) bits. Hence
N − 1 ≤ O(B_w k) + O(k²), which gives w = Ω(N^{5/2}/k^{5/2}). (We may assume w < N^3, so log s = O(k).) ∎

## Barriers

- **(B) Scope of the one-restriction strategy (corrected 2026-11-03).** Put N=2^k.
  Every function on the k live variables has a depth-two threshold circuit with at most N/2
  bottom gates: use its DNF or its CNF, whichever has fewer terms/clauses. Thus an argument
  using only unrestricted depth-two complexity of one restricted truth table can demand at
  most O(N) surviving gates. Combined with a survivor estimate E Q <= C s k/sqrt(N), this
  gives a best conceivable scale O(N^(3/2)/k) for that particular argument template.
  This is not a barrier theorem for all one-restriction methods: inherited weights, constrained
  circuit families and compatibility between restrictions contain information that unrestricted
  size discards. Tightness of the gate-survival estimate alone does not prove such a barrier.
  Majority has survival probability Theta(k/sqrt(N)), so uniformly improving that estimate for
  all LTFs is impossible. The old heading n^(3/2)*log(n) was a typo; the displayed template
  ceiling is n^(3/2)/log(n). The extension asserted for multiple live variables was not proved
  and is withdrawn pending an explicit target-complexity calculation.
- **(C) Communication methods cap at n².** Under every bipartition, D(A_n) ≤ 2k + 2. Alice sends her
  partial block parities; Bob either announces x_b or sends b back. Hence discrepancy ≥ Θ(n^{−2}) and
  sign-rank ≤ O(n²) under every partition. After the polynomial losses for gate CC and rank, discrepancy and
  sign-rank give nothing near n^{2−o(1)} for MAJ∘THR, THR∘MAJ or THR∘THR.
- **(D) Block-symmetric gates [α·x + β·s ≥ θ].** Under the (x | a) partition, A is Index_N with repeated
  columns. So sign-rank gives only Ω(N) and discrepancy only Ω̃(√N).
- **Fourier-sum architecture** (from earlier): any circuit of the form sign(Σ_S A_S(x)χ_S(b)) needs all N
  characters and costs about N²/2. Fable's MILP experiments split the per-character cost:
  - the *sign* of X·(−1)^t needs only T + 1 half-planes, independent of the X-range;
  - its *value* needs a number of half-planes linear in the range.

  So a sub-quadratic circuit would have to combine signs, not magnitudes. No such design was found.

## Open
- Close the remaining log factor: n^{3/2}/log² n vs the method's ceiling n^{3/2}/log n.
- Beating n^{3/2} needs an argument that uses many restrictions jointly, or a non-restriction method.
  Communication methods are ruled out by (C).
- The average-case log² gate/log^(5/2) wire bounds are now formalized in PR #2377.
- The fixed-top refinement below improves the gate advantage range by a hand proof; it is not yet Lean-formalized.


## Follow-up to B: preserve the top weights (2026-11-03)

Author: Christian Reitwiessner, with AI assistance.
Status: mathematical derivation checked against the circuit restriction model; not Lean-formalized.
This strengthens the range of the average-case gate result, not its log² denominator.

Fix one original circuit c, one choice sigma of the live position in each block, and its output
gate. Let s bound the number of bottom gates (using c.size is safe), N=2^k, and Q the number of
bottom gates not forced to a constant. The live bottom weights and the output gate's coefficients
on bottom gates and live direct inputs are fixed independently of the fixed input values.

For an exact survivor set I of size q:

* There are at most binom(s,q) choices of I.
* Each survivor has at most N+1 threshold behaviours on the N live assignments.
* Once these behaviours are fixed, the top score is a fixed real function on N points. All
  constant bottom gates and fixed direct inputs change only the top threshold. It therefore
  has at most N+1 output behaviours.

Consequently the family H_(sigma,q) of restricted functions satisfies

    |H_(sigma,q)| <= binom(s,q) (N+1)^(q+1)
                  <= (s+1)^q (N+1)^(q+1).

The second inequality deliberately sacrifices constants for a simple simultaneous bound.
This count must keep actual survivor identities; replacing them by a single free family of
bottom functions would lose the fixed original top coefficients.

Let lambda>0 and put

    A = ln(s+1) + ln(N+1) + lambda,
    C = ln(N+1) + lambda,
    t_q = sqrt(N (A q + C)/2),
    delta = 1/(exp(lambda)-1).

For each fixed live function h, the subcube truth table of Andreev is a uniformly random
N-bit truth table, up to the residual-parity permutation. Conditional on the address bits,
Hoeffding gives upper-tail probability exp(-2 t_q^2/N). Hence

    Pr[exists q,h in H_(sigma,q): agreement-count(h,A) - N/2 >= t_q]
      <= sum_(q=0)^s exp(-(q+1)lambda)
      <= delta.

No union over sigma is required: apply this bound for each sigma and then average. The uniform
subcube averaging identity recovers global agreement. If B bounds E_(sigma,w) Q, concavity of
sqrt gives, for any circuit agreeing with Andreev on a 1/2+epsilon fraction,

    epsilon <= sqrt((A B + C)/(2N)) + delta.

For epsilon >= delta this yields the explicit finite inequality

    A B >= 2N (epsilon-delta)^2 - C.

Choosing lambda=ln(1+4/epsilon) makes delta=epsilon/4 exactly, giving

    B >= ((9/8) N epsilon^2 - ln(N+1) - ln(1+4/epsilon))
         / (ln(s+1)+ln(N+1)+ln(1+4/epsilon)).

At balanced parameters k*m=N, n=2N, the existing restriction theorem gives
B <= 4 sqrt(2) s k/sqrt(N). For k>=1 and

    4 sqrt((k+1)/N) <= epsilon <= 1/2,

the preceding inequality proves

    s >= [15/(256 sqrt(2))] epsilon^2 N^(3/2)/(k(k+1)).

Constant check: assume s<N² (otherwise the displayed claim is immediate). Then
ln(s+1)<=2k+1. The assumed epsilon implies epsilon>=1/sqrt(N), so
lambda<=ln(1+4sqrt(N))<=ln(5N)<=k+2. Thus C<=2k+3<=3(k+1),
A<=4(k+1), and N epsilon²>=16(k+1). The numerator is at least
(15/16) N epsilon², so B>=(15/64)N epsilon²/(k+1), yielding the stated s bound.
All logarithms in this argument are natural; N=2^k.

Thus the gate lower bound Omega(epsilon² n^(3/2)/log² n) extends by this derivation to
advantages epsilon >= C0 sqrt(log(n)/n), for a universal constant C0. This is a smaller
advantage threshold than the existing formalized condition of order log(n)/sqrt(n).

Limits: this does not remove the remaining logarithm from the gate lower bound. The survivor
identities alone cost log binom(s,q), which is Theta(q k) at the current critical scales
s~N^(3/2)/k² and q~N/k. Replacing an ordered list by an unordered set therefore improves
constants but not that logarithmic order. Removing it needs another structural argument.

The refinement does not directly transfer to the wire bound: the wire proof absorbs every
gate depending on at most one live variable. Such gates can change the top coefficients on
the live literals as fixed inputs vary; the top score is then no longer fixed.

Primary-source reference for the survival estimate and its majority tightness:
Kane-Williams, https://cseweb.ucsd.edu/~dakane/depth2LTF.pdf, Lemma 1.1 and the observation
immediately before its proof. The fixed-top count and range refinement above are original
reasoning here, not claims attributed to that source.
