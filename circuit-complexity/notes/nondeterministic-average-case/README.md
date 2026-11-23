# Average-case frontier lower bounds for nondeterministic circuits

[Note v1: the one-sided bound](nondet-average-case.md) · [Note v2: removing the witness factor](nondet-average-case-v2.md) · [Note v3: lifting theorems and the restated target](nondet-average-case-v3.md) · [Note v4: one witness bit](nondet-average-case-v4.md) · [Checks](checks/)

The frontier method of McGuire, Schlesinger and Williams (STOC 2027 submission 1432) proves explicit lower bounds of about $(L-\varepsilon)n$ gates for fan-in-two circuits. It works as follows:
- the circuit is compiled into a constraint network;
- a layout of the network turns it into a read-once branching program;
- small layout width gives rectangle bounds, and these force a lower bound on circuit size.

For deterministic circuits the branching program is unambiguous, and that gives average-case bounds. For nondeterministic circuits only the worst-case bound was known (`Nondeterministic.lean` in [cslib-frontier](https://github.com/cslib-community/cslib-frontier)). These notes ask how far the average-case bound extends to nondeterministic circuits.

The target is that, for every ε > 0, every nondeterministic circuit with at most (L−ε)n gates agrees with an explicit S_n on at most a 1/2 + O(b) + 2^(−γn) fraction of inputs. **This target is not proved.** v3 restates it with a smaller constant and reduces the first open case, one witness bit, to a deterministic question; v4 narrows that case. Whether the full constant L can be reached is open. The notes prove restricted versions and identify barriers.

## Results

| | Statement | Note |
| --- | --- | --- |
| One-sided bound | If every large rectangle R satisfies \|R∩S\| ≤ ρ\|R∖S\|, then Pr[x ∈ A∩S] ≤ ρ·E[1{x∉S}·#witnesses(x)] + \|U\|^(−γn). The proof peels by induction on (input, accepting path) pairs. | v1 |
| Perfect soundness | A circuit below (L−ε)n gates that never accepts outside a rectangle-free S accepts only a \|U\|^(−γn) fraction of all inputs. | v1 |
| Witnesses are almost free | Each witness input that feeds a gate lowers the cycle rank by one. So the frontier bounds hold under s − k_u ≤ (L−ε)n, where k_u counts those inputs. | v2, C1 |
| Bounded ambiguity (F, F2) | At most D accepting witnesses per input gives agreement ≤ 1/2 + 2^(D+1)b + \|U\|^(−γn), with the size budget scaled by about 1/D. A Chebyshev version needs degree O(√D·log 1/δ) in place of D. | v2 |
| Partial determinization (W) | If only O(log n) edges across each cut depend on the witness, the program can be made unambiguous, and the deterministic average-case bound applies. | v2 |
| Probability gap (M) | If every accepted input is accepted by at least an α fraction of witnesses, the bound holds at size (L−ε)n/d with d ≈ 1/√α. | v2 |
| Exact reformulation (D) | By LP duality, the target holds for an accepted set A iff 1_A is close to a signed combination of large rectangles with bounded total mass. This condition does not involve S. | v2 |
| Barriers B1–B4 | An argument that uses only the width of the branching program would give an explicit Arthur–Merlin communication lower bound (B1). Narrow programs simulate unions of boxes over a few blocks (B2). An argument uniform in the alphabet would give number-in-hand multiparty NP lower bounds for Li's sumset extractor (B3). Hashing reduces to the linear statements, and moment methods need degree about √(range of witness counts), beyond what the size budget allows (B4). | v1, v2 |
| Tree-like cones (T) | If no witness-dependent wire is used twice, the circuit is simulated exactly by a deterministic circuit over a three-letter alphabet. Two-sided bound for s − k_u ≤ (1 + (L−1)/log₂3 − ε)n ≈ 3.26n, with no limit on witnesses. | v3 §1 |
| Few entry wires (E) | If m input-determined wires feed the witness cone, the bound holds when s_det + (n − n_det) + c + m/A ≤ (L−ε)n. | v3 §2 |
| Profiles (P) | Run all witnesses in parallel. With k witness bits, two-sided bound for s − k_u ≤ (1 + (L−1)/2^k − ε)n: 2.79n, 1.89n, 1.45n for k = 1, 2, 3. | v3 §7 |
| Live branch points (L) | Each wire carries the relation between its value and the reused witness-dependent wires still live there: at most 2^(r+1) bits for r live points, whatever the number of witnesses. T is the case r = 0. | v3 §7 |
| Single cut is not enough | S = g(q,b) ⊕ g′(q′,b) has small bias on all large rectangles of one cut, yet agrees on 3/4 of inputs with g(q,b) ∨ g′(q′,b), a union of few large rectangles at that cut. | v3 §5 |
| One witness bit | For one witness bit the nondeterministic statement is equivalent to a deterministic one about h(y,0) ⊕ h(y,1). The method proves it up to 2.79n. Between 2.79n and Ln it is open, and a positive answer to question (Q) would make the target false. | v3 §6 |
| Restated target | For k witness bits the bound holds up to (1 + (L−1)/2^k)n (Theorem P); conjecturally the constant L is not reachable for all sets with small bias at all cuts. | v3 §8 |
| Few nonlinear gates (A) | One witness bit. The difference between the two runs on any wire is a fixed XOR of the differences at the m AND-type gates of the witness cone. The bound holds when A(s−n) + min(A(s−n), m) ≤ (1−δ)n: the full constant for m = o(n), 3.68n for m = n/4. | v4 §2 |
| Entropy of the difference (H) | One witness bit. If the pattern of differences takes at most 2^H values on all but an η fraction of inputs and A(s−n) + H ≤ (1−δ)n, the bound holds with extra error O(η). | v4 §5 |
| Deaths and copies (H1) | The pattern is determined by the gates where the difference dies. If it dies at o(n) gates on average, or the cycle rank weighted by the probability of a difference is o(n), the bound holds at the full constant L. A counterexample needs Ω(n) of both. | v4 §6 |
| Bottleneck criterion | A predecessor-closed set containing almost all inputs whose outgoing edges carry fewer than n bits (counted for the pair of runs) gives the bound without any layout. | v4 §7 |

Lemma 0 of v1 (accepting paths correspond to witnesses restricted to the *used* witness inputs) is stated in its precise form in both notes; `checks/reach_vs_used.py` shows why the restriction to used inputs matters. v2 also logs eleven failed approaches.

## Status

The notes were written with AI assistance at the request of Christian Reitwiessner. They were produced by AI working from the cslib-frontier Lean sources and the literature. The paper's PDF was not accessible. **v3 was checked by one independent AI review, and its corrections are incorporated; v1 and v2 (including Theorems F, W and M) have not been independently reviewed. No human has reviewed any of it, and nothing is formalized in Lean.** Theorems T, P and L also rely on a version of the Lean deterministic theorem with binary inputs and a larger wire alphabet, which is not formalized. **v4 has not been independently reviewed.** It also contains one small search experiment (v4 §4), which is weak evidence only. Every claim in the notes is labelled *proved here*, *verified from source*, *experiment* or *speculation*.

The scripts in `checks/` are brute-force checks of the bookkeeping on tiny instances, where the residual terms dominate. They do not test the asymptotic statements. All of them were rerun from this folder before publishing.

## Related work in cslib-frontier

The theorems are stated in terms of the layout constant A, with L = 1 + 1/A (`LayoutBound 3 A`). They therefore improve automatically whenever the general layout bound improves. The notes use the Gaussian value L ≈ 4.5625. Recent work by Samuel Schlesinger raises the constant:

- [#7539](https://github.com/cslib-community/cslib-frontier/pull/7539) (merged): unconditional (4.6362−ε)n bounds over U₂, worst-case, nondeterministic and average-case. They come from a U₂-specific matched-pair compression into 3-state branching programs, not from `LayoutBound`. Whether Theorems F, W and M carry over to that compiler has not been checked.
- [#7753](https://github.com/cslib-community/cslib-frontier/pull/7753) (open): a cubic layout coefficient below 5/36 (`layoutBound_five_div_eighteen`, i.e. `LayoutBound 3 (5/18)`), giving (4.60−ε)n for any basis. Since it is a general layout bound, the results here would hold with L ≈ 4.60.
- [#7411](https://github.com/cslib-community/cslib-frontier/pull/7411) (open, CI failing): a crossing-cover Gaussian-wave layout bound giving about 4.827n.
- [#7515](https://github.com/cslib-community/cslib-frontier/pull/7515) (merged): non-explicit polynomial witnesses with vanishing bias. Through them the results hold with b → 0. For an explicit S the bias is the fixed bias of Li's sumset extractor.

## Running the checks

From `checks/`, using only the Python standard library:

```
python3 peel_check.py 60          # v1 peeling bookkeeping (output: peel_check_output.txt)
python3 circuit_check.py          # v2 C0, W and cycle-rank count (circuit_output.txt)
python3 nbp_check.py              # layer-cake lemma, product programs, weighted peeling (peel_output.txt)
python3 peel_k2.py .              # weighted peeling at K = 2
python3 cheb_check.py             # Chebyshev polynomial for F2 and M (cheb_output.txt)
python3 binom_basis_check.py .    # binomial-basis coefficients (binom_output.txt)
python3 reach_vs_used.py .        # used versus output-reaching witness inputs
```

From `checks/v3/`:

```
python3 tree_cone_check.py        # Theorem T, with a control that reuses one witness
python3 live_profile_check.py     # Theorems P and L against brute force
python3 live_adversarial.py 2000  # the review's independent check of L and P on adversarial families
python3 xor_or_strong.py          # the single-cut example (needs numpy; several minutes)
```

The first three were rerun from this folder before publishing. `xor_or_strong_output.txt` is the review's recorded output and was not rerun.

From `checks/v4/`:

```
python3 few_ands_check.py         # the linear-span claim behind Theorem A (few_ands_output.txt)
PY=python3 ./run_search.sh 12 6000 6 "2 4 6 8 10 12 16 20 26 32"   # the search of v4 §4 (needs numpy; about 7 minutes on 18 cores)
```

`few_ands_check.py` was rerun from this folder before publishing. `search_n12.txt` is the recorded output of the search and was not rerun.
