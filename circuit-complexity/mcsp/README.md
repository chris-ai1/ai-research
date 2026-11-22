# Boolean MCSP: research summary and literature check

Summary of a research session that ended on 22 November 2026, together with a literature-priority search run the same day. MCSP asks whether a truth table of N = 2ⁿ entries can be computed by a circuit with at most s gates. Below, T = s log₂ s.

**Status.** Every result here is an unrefereed, AI-written proof. The internal "referee" notes came from the same agent team. Three Lean files formalize only small combinatorial lemmas. The manuscripts are not in this repository yet. No result here is a breakthrough.

## Claimed results (written proofs, not independently checked)

| # | Result | Manuscript |
| --- | --- | --- |
| 1 | A deterministic circuit that decides MCSP exactly needs (2−o(1))N gates over the full binary basis, for every s = o(N/n). The short proof reduces to Schnorr's lower bound for "all bits equal". | deterministic |
| 1b | Circuits allowed error N^(−1−ε) need 2N−O(N/n) gates, for every s from n−2 up to cN/n. | probabilistic |
| 2 | Quantum query complexity and approximate degree are Θ(√(NT/(1+log(N/T)))) for (2+η)n ≤ s ≤ (1−ε)N/n. They are Θ(√N) for very small s and, for AND/OR/NOT circuits, up to (1+c)n. | degree, queries, low-budget |
| 3 | Gap MCSP (size ≤ s = N^a versus > t = N^b): Θ(Ns/t) classical queries and Θ(s√(N/t)) quantum queries. Threshold degree, rational degree and postselected queries are all Θ(s). | gap |
| 4 | Read-k branching programs and DNNF circuits need size 2^Θ(s log s). One-tape machines with one-way input need Ω(N²) time; with a two-way input head, Ω(N log N) under one-sided error. | branching, tape, twoway |
| 5 | At s = cN/n: parity decision trees need (c+o(1))N queries, circuits allowed error need 2.5N gates, and deterministic circuits need 2.5226N at one fixed threshold. | dense-circuits, tilted, affine |
| 6 | Sign-rank 2^Ω(N), and sharp bounds on how well small-circuit tables can hide parities, with communication corollaries. | sign-rank, gap |
| 7 | Parity constraints: n+2^Θ(r) gates are needed and suffice for r ≤ c log n. | parity-excess |
| 8 | Counting results (joint-type counts, prescribed cell quotas and marginals) and complex zeros of the acceptance polynomial, which follow a Szegő curve. | types, witnesses, zeros |

**Still open:** query bounds in the window between (1+c)n and (2+η)n gates, approximate degree for gap MCSP, and the circuit lower bound that hardness magnification would need.

## How each result compares with the literature

These verdicts come from targeted searches, mostly of abstracts, so they are preliminary.

- **#1 is the strongest result.** Chen–Li–Yang (CCC 2022, [ECCC TR22-086](https://eccc.weizmann.ac.il/report/2022/086/)) explicitly leave "an unconditional 2n−o(n) circuit size lower bound for MCSP, even against deterministic circuits" open. No later paper proves it. It is a short, clean answer to a published open question, suitable for a conference such as CCC, STACS or ICALP. Wittcop's earlier manuscript at s = n−1 must be credited; the draft does.
- **#1b is new but not a breakthrough.** Hardness magnification needs more than 2N + O(N/log log N) gates. This bound reaches 2N − O(N/n), so it stops just short and has no consequence for P versus NP.
- **#2 looks new.** The upper bound follows from Kothari's oracle-identification theorem ([arXiv:1311.7685](https://arxiv.org/abs/1311.7685)), and the draft should say so plainly. No matching lower bound for the MCSP decision problem was found.
- **#3 looks new.** The nearest work (Oliveira–Pich–Santhanam, Allender–Ilango) proves no query bounds of this kind.
- **#4 extends known work.** It sharpens Cheraghchi–Hirahara–Myrisiotis–Yoshida ([STACS 2021](https://eccc.weizmann.ac.il/report/2020/103/)), who proved an N^1.99 bound against randomized one-tape machines. It generalizes Glinskih–Riazanov (LATIN 2022) from read-once programs at linear s. Both are cited.
- **#5 overlaps with prior work.** Hoza–Lv ([RANDOM 2025](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.APPROX/RANDOM.2025.35)) nearly imply a one-sided 2.49N bound without mentioning MCSP. The dense manuscript cites them; the tilted one does not and should. No manuscript cites Mishra–Santhanam ([ECCC TR26-260](https://eccc.weizmann.ac.il/report/2026/260/), revised 3 Nov 2026), who prove 4n−O(log n) for an explicit function in P, now the record for explicit lower bounds. It does not cover MCSP, but the drafts' comparisons should mention it. The 2.5226N constant is a modest result.
- **#6 and #7 look new.** For #6, the method is the Cheraghchi–Kabanets–Lu–Myrisiotis local-generator framework; the sharp constants and the sign-rank result appear new. For #7, a standard small-bias construction may beat 2^O(r) when r is much larger than log n, which the paper should discuss.
- **#8 is the weakest.** The counting results are natural sharpenings of Pippenger (1977) and Andreev–Clementi–Rolim, which the drafts cite. The zeros result is a new application of Szegő's classical theorem. Both could only be minor papers.

## RH and ETH

- **RH:** the [Lean community post](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/) (21 Nov 2026) exists and certifies a formal proof by Levent Alpöge.
- **ETH:** the October ["ETH is False" preprint](https://github.com/openai/math) exists, with a review group led by Impagliazzo, Paturi and Williams. [Strassle–Subercaseaux](https://arxiv.org/abs/2611.11832) carry it over to nondeterministic Turing machines.

Neither helps with MCSP beyond one small application, to minimum DNF under restrictions.

## Before submitting anything

1. Have a human expert check #1 and #2 first. They are the shortest proofs and the most valuable.
2. Add the Mishra–Santhanam citation to the papers that compare constants, and the Hoza–Lv citation to the tilted paper.
3. Check the 2025–26 ECCC listings of Ilango, Hirahara, Ren and Santhanam by hand, because search engines index recent ECCC reports poorly.
