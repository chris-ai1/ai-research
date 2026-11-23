# Average-case frontier lower bounds for nondeterministic circuits

[Note v1: the one-sided bound](nondet-average-case.md) · [Note v2: removing the witness factor](nondet-average-case-v2.md) · [Checks](checks/)

The frontier method of McGuire, Schlesinger and Williams (STOC 2027 submission 1432) proves explicit lower bounds of about $(L-\varepsilon)n$ gates for fan-in-two circuits. It works as follows:
- the circuit is compiled into a constraint network;
- a layout of the network turns it into a read-once branching program;
- small layout width gives rectangle bounds, and these force a lower bound on circuit size.

For deterministic circuits the branching program is unambiguous, and that gives average-case bounds. For nondeterministic circuits only the worst-case bound was known (`Nondeterministic.lean` in [cslib-frontier](https://github.com/cslib-community/cslib-frontier)). These notes ask how far the average-case bound extends to nondeterministic circuits.

The target is that, for every ε > 0, every nondeterministic circuit with at most (L−ε)n gates agrees with an explicit S_n on at most a 1/2 + O(b) + 2^(−γn) fraction of inputs. **This target is not proved.** The notes prove several restricted versions and identify barriers that any full proof must get past.

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

v2 also corrects v1's Lemma 0. Accepting paths correspond to witnesses restricted to the *used* witness inputs, not to those reaching the output. The two readings differ on 240 of 728 test inputs (`checks/reach_vs_used.py`). The inequalities v1 uses are unaffected. v2 also logs eleven failed approaches.

## Status

The notes were written with AI assistance at the request of Christian Reitwiessner. Each was produced by one AI agent working from the cslib-frontier Lean sources and the literature. The paper's PDF was not accessible. **No independent review, human or AI, has been done, and nothing here is formalized in Lean.** Every claim in the notes is labelled *proved here*, *verified from source*, or *speculation*.

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
python3 reach_vs_used.py .        # the 240-of-728 correction
```
