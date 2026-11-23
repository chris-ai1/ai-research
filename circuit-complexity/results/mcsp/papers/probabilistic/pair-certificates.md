# Pair certificates for MCSP: a smaller deficit at thresholds n−1 and n

**Status.** AI-written and not reviewed by a human. The proofs below are short and use only Schnorr's 2d−3 bound for the all-equal function, restrictions, and exhaustive tables of 4- and 5-variable functions. The tables are computer results; the scripts are in [`pair-certificates/`](pair-certificates/).

## Results

Notation: N = 2ⁿ, a *site* is one of the N truth-table positions (an address in {0,1}ⁿ), and distance between sites is the Hamming distance of their addresses. Circuits use arbitrary binary gates with free negations; MCSP[s] accepts the tables of functions with at most s gates.

1. **Theorem A (unconditional).** For s ∈ {n−1, n} and n ≥ 5, every circuit that decides MCSP[s] has at least

   2N − N/(1 + n + n(n−1)/2) − 2

   gates. The same holds for a probabilistic circuit whose error on every input is below 1/(c·N²n⁴), for an absolute constant c. The previous bounds at these thresholds had deficit about N/n ([high-confidence manuscript](main.tex), Wittcop). The deficit here is about 2N/n².
2. **A criterion for 2N − 2.** If every pair of sites has two kinds of four-input certificates (defined below), every circuit needs at least 2N − 2 gates. Exhaustive tables confirm the criterion for n = 4 at s = 3, 4, 5, 6 and for n = 5 at s = 5, 6. So MCSP on 16 inputs needs at least 30 gates at those thresholds and MCSP on 32 inputs needs at least 62.
3. **Where the criterion fails.** At s = n−2 no pair at distance 3 or more has the second kind of certificate (proved). At n = 5, s = 4 no antipodal pair has it (computed). So pair certificates alone cannot give 2N − 2 at the smallest thresholds.
4. **A conditional 2N − 2 near s = 2n.** If masking by an equality costs two gates (Conjecture M below, verified for all 149,184 instances with four variables), then for every n ≥ 4 and s ∈ {2n−5, …, 2n−2} every circuit for MCSP[s] needs at least 2N − 2 gates.

None of this crosses 2N.

## Certificates on a pair of sites

Fix a function F on N inputs, two sites a ≠ b and a table L. The *face* of (a, b) at L is the four values F(L), F(L⊕a), F(L⊕b), F(L⊕a⊕b), where L⊕a flips entry a.

- The face is *odd* if one or three of the four values are 1.
- The face is an *XOR face* if F(L) = F(L⊕a⊕b) ≠ F(L⊕a) = F(L⊕b).

For F = MCSP[s], an XOR face is a pair of easy tables that differ exactly at a and b while both tables in between are hard.

**Critical paths.** Take a circuit with no redundant gates in which every input is used. From an input, follow the unique outgoing wire while the current vertex has exactly one outgoing wire. The vertex where this stops is the input's *endpoint*. It has at least two outgoing wires or is the output.

**Lemma 1.** If the pair (a, b) has an odd face and an XOR face, then a and b have different endpoints in every circuit that agrees with F on the eight inputs of the two faces.

*Proof.* Suppose the endpoints coincide. The two paths meet first at a gate G, and they enter G through its two different inputs. Every vertex on either path before G has one outgoing wire. So with all other inputs fixed, the first input of G is a function φ of a alone, the second a function ψ of b alone, and the output is ρ(G(φ(a), ψ(b))) for a one-bit function ρ. On a face where the output depends on both a and b, the maps φ, ψ and ρ are bijections, so the face is G up to negations. An odd face then shows G is not an XOR gate, and an XOR face shows it is. ∎

**Lemma 2 (criterion).** If every pair of sites has an odd face and an XOR face, every circuit that agrees with F on these 8·N(N−1)/2 inputs has at least 2N − 2 gates. A probabilistic circuit with error below 1/(4N²) on every input has a member that agrees on all of them, so the bound holds for it too.

*Proof.* By Lemma 1 the N endpoints are distinct. At most one is the output, and the others have at least two outgoing wires. A circuit with H gates has 2H wires and N + H − 1 vertices other than the output, each with at least one outgoing wire. So H − N + 1 ≥ N − 1. ∎

This is the counting argument of Chen, Li and Yang (Section 4.4 of their paper). The high-confidence manuscript uses it with XOR faces for pairs at distance 2 only, which is why it loses N/n.

## Padding

**Lemma 3.** Let φ be a function of k variables c, and let ρ be a fixed assignment to n − k further variables r. Then C(φ(c) ∧ [r = ρ]) ≤ C(φ) + (n − k), and if φ is not constant 0, also C(φ(c) ∧ [r = ρ]) ≥ C(φ) + (n − k).

*Proof.* The upper bound adds one AND gate per variable. For the lower bound, fix the variables of r to ρ one at a time. Each is essential, so each restriction removes at least one gate. ∎

So a face of k-variable functions at threshold t becomes a face of n-variable functions at threshold t + (n − k), for sites that agree outside the k coordinates. The quantity s − n is preserved.

## Proof of Theorem A

Let U be the set of sites that share their endpoint with another site. A circuit with H gates has at least N − |U| + 1 distinct endpoints when U is nonempty, so H ≥ 2N − |U| − 1 by the count in Lemma 2. It remains to show that no two sites of U are at distance 4 or less. Then the balls of radius 2 around the sites of U are disjoint, and |U| ≤ N/(1 + n + n(n−1)/2).

**Lemma 4.** Let a, b be sites, and suppose that for every third site v there are easy tables L and L′ = L⊕a⊕b such that L⊕a, L⊕b, L⊕v and L′⊕v are all hard. Suppose also that every pair of sites has an odd face. Then a and b are not both in U.

*Proof.* By Lemma 1, a and b have different endpoints. Suppose both are in U, with partners a′ and b′ sharing their endpoints. Let G_a be the first common gate of the paths of a and a′, and G_b that of b and b′. One of them is not a descendant of the other, say G_a is not a descendant of G_b. The influence of b stays on its own path until that path has passed G_b, so the two inputs of G_a do not depend on b. By the odd face of (a, a′), G_a is not an XOR gate. Take L and L′ for v = a′. At L, flipping a changes the output and flipping a′ changes the output, so G_a sits at its unique input pair where it is sensitive to both inputs. After flipping a it is no longer sensitive to its other input, and flipping b does not change that. So the circuit gives the same output on L′ = L⊕a⊕b and on L′⊕a′. But L′ is easy and L′⊕a′ is hard. If instead G_b is not a descendant of G_a, exchange the roles, using v = b′. ∎

It remains to produce the tables of Lemma 4 for every pair at distance d ≤ 4 and every third site, and odd faces for all pairs. Write e = s − n ∈ {−1, 0} and t = 4 + e.

**Easy pairs.** Choose four coordinates c that contain the coordinates where a and b differ, and let ρ be the common value of a and b on the other coordinates r. Take 4-variable functions X and X′ with at most t gates that differ exactly at the two 4-bit parts of a and b, and whose two intermediate functions need t + 1 gates. Put L = X(c) ∧ [r = ρ] and L′ = X′(c) ∧ [r = ρ]. By Lemma 3, L and L′ are easy and L⊕a, L⊕b are hard.

**Flipping a third site v.** Write v = (γ, ρ′) and let J be the set of coordinates of r where ρ′ ≠ ρ.

- If J is empty, L⊕v = (X⊕1_γ)(c) ∧ [r = ρ], which is hard when C(X⊕1_γ) ≥ t + 1.
- If J is nonempty, fix the coordinates of r outside J to ρ. This removes at least n − 4 − |J| gates and leaves Ψ = X(c)·[r_J = ρ_J] ⊕ 1_γ(c)·[r_J = ρ′_J]. We need C(Ψ) ≥ t + |J| + 1.

  Let m be the distance from γ to the nearest point of the support of X, and M the set of coordinates where they differ. Fix the coordinates of c outside M to those of γ. Each is essential, so at least 4 − m gates go. Inside the remaining subcube X is 1 only at the point opposite γ, so what remains is the all-equal function on m + |J| signed variables. By Schnorr's theorem it needs 2(m + |J|) − 3 gates. Hence C(Ψ) ≥ m + 2|J| + 1, which is at least t + |J| + 1 whenever **m + |J| ≥ e + 4**.

  The finitely many remaining cases have m + |J| ≤ e + 3, so |J| ≤ 3, and Ψ has at most 7 variables. Each is checked by restricting essential variables down to a 5-variable function and looking it up in the exhaustive table.

**What the tables show** ([`isolate.py`](pair-certificates/isolate.py), [`isolate2.py`](pair-certificates/isolate2.py), [`d4n5.c`](pair-certificates/d4n5.c)):

| t | distance 1 | distance 2 | distance 3 | distance 4 |
| --- | --- | --- | --- | --- |
| 3 (s = n−1) | 84 pairs (X, X′) pass for every γ and J | 34 | 12 | for each (γ, J) some pair passes |
| 4 (s = n) | 70 | 52 | 24 | for each (γ, J) with J nonempty or γ at even distance from a, some pair passes |

For s = n, distance 4, J empty and γ at odd distance from a, no 4-variable pair works. There a 5-variable pair is used instead: for a = 00000, b = 11110 and every third point of the 5-cube, one of the 340 XOR faces at threshold 5 has both flips hard. Padding it needs n ≥ 5.

Example for distance 4 at t = 3: X = (x₀ ∧ ¬x₂) ∨ (x₁ ∧ ¬x₃) and X′ = (x₀ ∨ ¬x₃) ∧ (x₁ ∨ ¬x₂). They have three gates each and differ exactly at 0000 and 1111, and X⊕1₀₀₀₀ and X⊕1₁₁₁₁ need four gates.

**Odd faces.** The tables 0, 1_a, 1_b are easy when s ≥ n − 1. The table 1_{a,b} is an AND of n − d literals with an all-equal function on d variables, so it needs at least n + d − 3 gates. This gives an odd face when d ≥ 3 (for s = n−1) or d ≥ 4 (for s = n). For smaller d, pad a 4-variable odd face; the tables contain them.

**Probabilistic circuits.** The proof evaluates the circuit only on the listed inputs. There are O(Nn⁴) pairs at distance at most 4, N third sites for each, and O(N²) inputs for the odd faces. A probabilistic circuit with error below the reciprocal of this number has a member correct on all of them. ∎

## Where XOR faces exist

Exhaustive counts of XOR faces. A zero means that no pair at that distance has one.

| n, s | distance 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- |
| 4, 2 | 44 | 12 | 0 | 0 | |
| 4, 3 | 266 | 72 | 12 | 12 | |
| 4, 4 | 1022 | 436 | 142 | 48 | |
| 4, 5 | 1568 | 918 | 478 | 228 | |
| 4, 6 | 194 | 98 | 32 | 8 | |
| 5, 3 | 284 | 52 | 0 | 0 | 0 |
| 5, 4 | 4152 | 644 | 84 | 24 | 0 |
| 5, 5 | 40004 | 8630 | 1466 | 340 | 240 |
| 5, 6 | 396704 | 102406 | 26378 | 8094 | 4440 |

Odd faces exist for every pair in every row with s ≥ n − 1. The numbers of functions with at most s gates agree with Knuth's tables (for example 122,648 five-variable functions with at most 4 gates).

**Proposition 5 (limit at s = n−2).** At s = n − 2 an XOR face exists only for pairs at distance 1 or 2.

*Proof.* A circuit with n − 2 gates reads at most n − 1 variables. So the two easy tables f and f′ = f⊕1_{a,b} are independent of some variables i and j. If i = j then 1_{a,b} is independent of xᵢ, so b = a⊕eᵢ. Otherwise apply the derivative in direction i and then j to f⊕f′ = 1_{a,b}. The left side vanishes, so the four translates of a by 0, eᵢ, eⱼ, eᵢ+eⱼ coincide as a set with those of b, and b − a is one of eᵢ, eⱼ, eᵢ+eⱼ. ∎

In the rows above, the largest distance with an XOR face is 2, 4, and at least 5 for s − n = −2, −1, 0.

## A route to 2N − 2 near s = 2n

The distance-5 faces at n = 5, s = 5 are the distance-4 example above with one variable doubled: X(x₀, x₁, x₂, x₄) ∧ [x₂ = x₃]. Doubling a variable costs two gates, adds one variable, and adds one to the distance if a and b differ there.

**Conjecture M (equality mask).** Let ψ(c, w) be a function, not constant 1, whose restrictions to c = 0 and to c = 1 are both nonzero. Then C(ψ(c, w) ∧ [c = c′]) ≥ C(ψ) + 2.

The upper bound C(ψ) + 2 is clear. Both hypotheses are needed: for ψ = c ∧ θ(w) the left side is C(θ) + 2 and the right side is C(θ) + 3. [`blow2.py`](pair-certificates/blow2.py) checks the conjecture for every 4-variable ψ with at most 5 gates and every choice of c that meets the hypotheses, 149,184 cases in all, with no exception. It is a relative of Schnorr's theorem that the all-equal function needs 2d − 3 gates, and I could not prove it. The case that resists is when c and c′ each have a single reader, both XOR gates whose other inputs are internal signals.

**Conditional theorem.** Assume Conjecture M. Then for n ≥ 4 and s ∈ {2n−5, 2n−4, 2n−3, 2n−2}, every pair of sites has an odd face and an XOR face for MCSP[s], so every circuit needs at least 2N − 2 gates, also with error below 1/(4N²).

*Sketch.* Start from a 4-variable face at threshold s₀ = s − 2n + 8 ∈ {3, 4, 5, 6} for a pair at distance d₀ = min(d, 3), or d₀ = 4 when d = n. Double variables n − 4 times: d − d₀ times at coordinates where the pair differs and the rest at coordinates where it agrees. Easy corners gain exactly two gates per doubling by construction, and hard corners gain at least two by Conjecture M. The hypothesis of the conjecture is preserved by doubling. [`base4.py`](pair-certificates/base4.py) confirms that for every d₀ and s₀ there are XOR faces and odd faces whose hard corners have all eight restrictions nonzero. ∎

A second family is verified for small cases: with E the all-equal function on c₁, …, c_{d−1} and P an OR of literals of the other variables, the functions E ∧ (P ∨ ¬c_d) and E ∧ (P ∨ c₁) have n + d − 4 gates and differ at two sites at distance d. SAT confirms that the two intermediate functions need one more gate for d = 3, 4, 5 with a single literal in P ([`alleq.py`](pair-certificates/alleq.py)).

## Relation to hardness magnification

The summary and the manuscripts quote Chen, Li and Yang's Theorem 1.6: a probabilistic lower bound above 2N + O(N/log log N) would give a major separation. Their formal statement for MCSP is Theorem 4.3, which is sharper. (I read it from the text of the ECCC PDF, where some symbols were lost in extraction, so the exact statement should be checked against the paper.) For n ≤ s ≤ O(n²/log² n) and g = s log s, it is enough to rule out probabilistic circuits of size **2N + O(N·g/log² N)** with error **exp(−Ω(g))**.

- The error allowed there is far smaller than 1/poly(N). So the bounds of this note and of the high-confidence manuscript, which need error below 1/poly(N), apply in that model.
- At s = n the threshold is 2N + O(N log n / n). Theorem A gives 2N − O(N/n²). The gap between what is proved and what would be a breakthrough is an additive O(N log n / n).

## Reproducing the tables

Run in [`pair-certificates/`](pair-certificates/). The SAT scripts need `python-sat` (`pip install --target lib python-sat`).

```
PYTHONPATH=lib python3 n4.py        # exact gate counts of all 65,536 four-variable functions (comp4.pkl)
python3 faces4.py                   # faces for n = 4
gcc -O2 -o enum5 enum5.c
for g in 1 2 3 4 5 6; do ./enum5 $g; done   # five-variable functions with at most g gates, faces for n = 5, bitmaps bm5_g.bin (512 MB each)
python3 isolate.py; python3 isolate2.py     # the finite cases of Theorem A
gcc -O2 -o d4n5 d4n5.c && ./d4n5            # distance 4 at s = n
python3 blow2.py; python3 base4.py          # Conjecture M on four variables, base faces
PYTHONPATH=lib python3 alleq.py 4           # all-equal family
```

The 6-gate enumeration takes about two minutes. `alleq.py 5` takes about 15 minutes.

## References

- L. Chen, J. Li and T. Yang, *Extremely efficient constructions of hash functions, with applications to hardness magnification and PRFs*, CCC 2022. [ECCC TR22-086](https://eccc.weizmann.ac.il/report/2022/086/).
- C. P. Schnorr, *The combinational complexity of equivalence*, Theoretical Computer Science 1 (1976), 289–295.
- D. E. Knuth, *The Art of Computer Programming*, Volume 4A, Section 7.1.2 (gate counts of all functions of four and five variables).
