# AI Research

Research papers, proofs, and reproducible experiments. Each result is an unrefereed, AI-assisted proof unless the project says otherwise.

The repository is organized by topic. Each topic has up to two subdirectories:

- `results/`: potentially publishable results, each with a manuscript.
- `notes/`: exploratory notes, barriers, partial results, failed attempts and open problems.

## Circuit complexity

| | Project | Paper or contents |
| --- | --- | --- |
| Result | [Andreev’s function and depth-two threshold circuits](circuit-complexity/results/andreev/) | [Threshold-circuit paper (PDF)](circuit-complexity/results/andreev/workspace/eccc_draft/paper.pdf) |
| Result | [Boolean MCSP: results and literature check](circuit-complexity/results/mcsp/) | [Summary and literature check](circuit-complexity/results/mcsp/README.md) · [15 manuscripts](circuit-complexity/results/mcsp/papers/) |
| Notes | [Boolean MCSP: notes, barriers and minor results](circuit-complexity/notes/mcsp/) | Barriers, exploratory computations, two minor manuscripts, failed attempts |
| Notes | [Size of almost-universal hash functions and PRFs](circuit-complexity/notes/hashing-and-prf-size/) | **Unreviewed.** Claimed tight bounds `2n + n·2^{-Θ(log² n/ℓ)}` and `3n − o(n)`; improves the seed length of Chen–Li–Yang |
| Notes | [Average-case frontier lower bounds for nondeterministic circuits](circuit-complexity/notes/nondeterministic-average-case/) | Partial results and barriers; the target is not proved |

## Space complexity

| | Project | Paper |
| --- | --- | --- |
| Result | [LogCFL = UAuxPDA via Hoza's isolation for proof trees](space-complexity/results/logcfl-unambiguous/) | [LogCFL is unambiguous (PDF)](space-complexity/results/logcfl-unambiguous/paper.pdf) |

## Algebraic complexity

| | Project | Paper |
| --- | --- | --- |
| Result | [The Shub–Smale conjecture and integer roots](algebraic-complexity/results/shub-smale/) | [How many integer roots can a short arithmetic program have? (PDF)](algebraic-complexity/results/shub-smale/paper.pdf) |
