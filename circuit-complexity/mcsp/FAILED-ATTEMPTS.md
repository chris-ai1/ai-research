# Failed attempts and dead ends

These are the approaches from the 22 November 2026 MCSP session that did not work, along with the reason each one failed. A follow-up section records two attempts from Samuel Schlesinger's *Structure from optimality* notes. As with the results, all of these are unrefereed, AI-written arguments. Several of the "failures" are themselves proved barrier statements, and are marked as such. N = 2ⁿ is the truth-table length and s the gate budget.

## Aimed at a breakthrough

**Charging more branching gates with bounded changes to parity extensions.** For fixed $k$, even the complete radius-$k$ neighborhoods of all signed coordinate permutations of a parity extension with $O(\log n)$ core and unused address bits admit a deterministic $2N+O(N^{1-\eta_k})$-gate circuit agreeing with exact MCSP on the promise. The construction also covers $N^{o(1)}$ such cores. It recovers the changed addresses from graph incidence parities shared across the centers. For all orientations of one core, this obstruction extends to $\lfloor\log_2 n\rfloor-1$ flips with additive overhead $N\,2^{-\Omega(n/(\log n)^2)}$. For the distance and address-XOR labels, the circuit can even recover an arbitrary unknown core from the input. These tests alone cannot force a $2N+\Omega(N/\log\log N)$ lower bound. [Proof and scope](bounded-flips.md)

**Hardness magnification from the 2N bounds.** Chen–Li–Yang (CCC 2022) show that a lower bound above 2N + O(N/log log N) for probabilistic circuits deciding MCSP[s] at small s would separate P from exponential size. The session proved (2−o(1))N for deterministic circuits and 2N − O(N/n) at error N^(−1−ε) ([probabilistic](papers/probabilistic/main.pdf)).
*Why it failed:* both bounds fall short of the threshold by a lower-order additive term, so magnification never applies. No step of the argument suggests how to cross 2N.

**Getting a high-confidence 2N bound by restricting to a structured sublanguage.** One idea was to restrict MCSP to a simple projected language, such as the first-order Reed–Muller code, signed dictators, low-weight parities or any affine code of rank O(log N), and prove 2N − o(N) for that language.
*Why it failed (proved barrier):* every such language has randomized circuits of size (2−η)N with perfect completeness and error N^(−c). These are built from local parity checks on a high-girth 4-regular graph. So no lower bound of this form can come from these languages alone.

**Linear-check architectures.** For circuits that first compute linear checks and then AND them, the session found a rigorous lower bound of about 3N.
*Why it failed:* the bound uses the restricted architecture essentially and does not carry over to unrestricted circuits deciding MCSP.

**Direct-sum additivity of gate counts.** One lower-bound route wanted C(h(y) ⊕ g(z)) ≥ C(h) + C(g) in general.
*Why it failed:* general direct-product additivity of Boolean gate counts has known counterexamples. The final proof ([deterministic](papers/deterministic/main.pdf)) avoids this step by using teaching sets and complementation instead.

**Constant error at the stronger deterministic coefficient.** The tilted gate-elimination argument gives 2.5226N for deterministic circuits and extends to error 2^(−0.00564N).
*Why it failed:* the relative-entropy bound that drives it fails at constant error. At constant error, only the weaker (2.5−o(1))N bound from the dense manuscript survives.

**Finding affine spaces inside quadratic elimination paths.** The dense MCSP proof gives a small-circuit truth table in each affine space of sufficiently small codimension. A path with $2^{\lfloor N/10\rfloor}$ tables can contain no affine plane, even when the product substitutions have disjoint inputs. A second construction realizes an exponentially large plane-free accepting leaf under the published gate-selection rules on a small circuit. Affine synthesis still applies if the product inputs have a sufficiently small vertex cover. [Quadratic elimination paths](papers/tilted/quadratic-paths.md)

## Using the new RH and ETH results

**Riemann hypothesis.** The session monitored the Lean-verified proof and Alpöge's note throughout.
*Why it failed:* no step of any MCSP argument uses RH. The complex analysis in the degree and zeros manuscripts is classical: the maximum-modulus principle, Szegő's zero curve and Bernstein–Walsh.

**The October ETH preprint (fixed-width #SAT in subexponential time).** The plan was to encode "is there an s-gate circuit for this table?" as fixed-width SAT and beat brute-force enumeration of circuit descriptions.
*Why it failed:* the general circuit-synthesis encoding has too many witness variables, and the clause width is not bounded. The subexponential saving is therefore smaller than the cost of the encoding. The transfer works only in a restricted setting: minimum DNF when the prime implicants have bounded coverage or each positive entry has bounded incidence.

**Strassle–Subercaseaux (nondeterministic machines in subexponential time).** The plan was to apply their simulation to the natural MCSP verifier.
*Why it failed:* their exponent depends on the verifier's running time, and verifying a candidate circuit directly against the truth table costs too much. The result does not improve the general circuit-search bound.

## Restricted models

**Two-way input tapes via head geometry.** The first idea for a lower bound with a freely reversible input head was a separator argument based on the order in which individual sweeps visit positions.
*Why it failed (proved obstruction):* a constant union of increasing partial matchings can form a constant-degree expander, and two heads can traverse every edge of such a matching in one sweep with linear motion. So sweep geometry alone admits no small separators. The nondeterministic crossing argument also does not carry over to bounded error, because equality of two permuted strings has constant public-coin communication across the natural cut. The final result ([twoway](papers/twoway/twoway.pdf)) needs perfect soundness (one-sided error) for this reason.

**A single balanced cut for decomposable predicates.** One rectangle-cut argument for DNNF and witness predicates did not need a further decomposition guarantee.
*Why it failed:* a counterexample built from local predicates breaks it even with a single macroscopic factor. The final DNNF bound ([branching](papers/branching/branching.pdf)) uses a common hard pair over all balanced rectangles instead.

**A graph-based equality argument.** An early graph argument was superseded by an exact gate-elimination proof, C(EQ_d) = 2d − 3, which is shorter and tight.

## Parity constraints and degree

**Counting all three outcomes at private gates using only affine tests.** Fix $h$ table entries and exclude one pattern from each of $k$ disjoint pairs. The path has uniform information cost $h+k\log_2(4/3)$. A sparse set of size $2^{h+k+o(N)}$ can nevertheless miss the whole path while assigning near-uniform mass to every affine test up to rank $h+k-o(N)$. A second construction gives the same obstruction for near-full-rank linear encoders. A stronger MCSP bound needs additional information about small address circuits or about the path. [Extremum and counterexamples](papers/tilted/ternary-flats.md)

**A universal n + O(r/log r) upper bound for r parity constraints.**
*Why it failed (proved):* 3k+1 suitable algebraic-normal-form constraints on disjoint variable triples force size at least n − 1 + (k−2)/18. So the conjectured bound fails as r → ∞, even for r = o(n). The correct answer for r ≤ c log n is n + 2^Θ(r) ([parity-excess](papers/parity-excess/main.pdf)).

**Reaching the parity-query threshold rate exactly at budget c₁N/n.**
*Why it failed (proved):* a single scope of ⌊αN⌋ raw bits already tests membership in the projection of all easy tables. At α = c₁ the circuit census makes that projection's uniform mass tend to zero, so the rate stops strictly below c₁.

**Ordinary approximate degree for gap MCSP (s = N^a versus t = N^b).** The aim was degree of order s√(N/t), matching the quantum query bound.
*Why it is still open:* the replicated-mask construction proves only Ω(max{s, max(1, s²/t)·√(N/t)}). Threshold, rational and postselected degrees are all Θ(s), but none of these arguments controls bounded polynomials at the quantum scale.

## Follow-up on isolating blocks

**Inferring superlinear size from sparse acceptance and isolated minterms.** Suppose that on every block of at most $q$ bits, each labeling is the unique accepted assignment for some fixing of the other bits. Every $q$-bit block then exposes an identity matrix of order $2^q$, even if the entire class of accepted words is small.

For every polynomially bounded $q\ge1$, a complement-closed language can have this property, log-cardinality $q+O(\log(nq))$, and an $O(N)$-gate membership circuit. At $q\ge n^2$ the example can also accept every affine table and all tables within distance $n$ of a constant. A single sparse linear map is shared across the whole recognizer. The proof leaves open what follows from the full YES set of MCSP. [Construction and proof](isolation-barrier.md)

**Charging the same gates at many block sizes.** Let $m=2^d$, put $g_i=y_i\oplus t$, and compute the AND of the $m$ tests $[x_i=g_i]$ in a balanced tree. The circuit uses $3m-1$ gates. On each dyadic block $B$ of the $x$ inputs, the corresponding subtree has $|B|$ incoming context signals $g_i$. Every minterm occurs on that block by choosing the $y_i$ and satisfying the tests outside it.

Summing the context counts over block sizes $2,4,\ldots,m$ gives $md$. Each of the same $m$ source gates supplies one signal at each of the $d$ scales. Even with arbitrary nonnegative block weights, the total charge is the sum over those $m$ gates of their individual charges, hence at most $m$ times the maximum load. A superlinear charge on paper needs a separate theorem controlling how often a gate is counted in an actual MCSP circuit.

**Choosing the sign that deletes two gates at every merge.** For a matching of address pairs with a common difference, both constant sign patterns retain $2^{(1+o(1))s\log_2s}$ easy tables when $n=o(s)$ and $s=o(2^n/n)$. Optimizing the signs with exact fiber counts still gives the same $0.45689339\ldots$ deficit coefficient as the signed-merge proof when the favorable sign is constant. The obstruction concerns the gate savings and the terminal population estimate used in that proof. [Fiber counts and the sharp coefficient](papers/deterministic/parallel-derivatives.md)

## Priority corrections (claims that turned out not to be new)

- **Testing the whole size-s circuit class.** Alon–Blais–Chakraborty–García-Soriano–Matsliah already prove Ω(s^(1/c)) directly. The degree manuscript first credited them only for isomorphism testing and was corrected.
- **The scalar rate–distortion rate for approximate circuits** is due to Pippenger (1977). The types manuscript now claims only the joint-type refinement.
- **Local-generator lower bounds for MCSP** come from the Cheraghchi–Kabanets–Lu–Myrisiotis framework. The communication generator is an instance of it.
- **Andreev's nondeterministic functions** already cover selector synthesis for aligned rows with row-local relations. The witness manuscript claims only the unaligned and random-pairing cases.
- **The quantum query upper bounds** are corollaries of Kothari's oracle-identification theorem.

## Earlier Shub–Smale attempt (same day, separate project)

Before the MCSP work, the team tried to disprove the Shub–Smale τ-conjecture. Sums of two squares give curves with exponentially many integer points from short programs, but eliminating the second variable cost a square-root factor. The construction therefore recovered only the known exponent 2, due to Strassen and Bostan–Gaudry–Schost. A rational-parametrization doubling from 16 to 32 integer roots could not be repeated, because the next curve has genus 3. See [algebraic-complexity/shub-smale](../../algebraic-complexity/shub-smale/).
