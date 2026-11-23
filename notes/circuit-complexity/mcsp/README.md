# Boolean MCSP: notes, barriers and minor results

Exploratory material from the MCSP project. The potentially publishable results and their manuscripts are in [`results/circuit-complexity/mcsp/`](../../../results/circuit-complexity/mcsp/), which also defines the notation (N = 2ⁿ, threshold s, T = s log₂ s).

Everything here is an unrefereed, AI-written proof. These notes explain why certain approaches fail, record small exact computations, or give results that the literature check judged minor.

## Minor results

| # | Model | Statement | Source |
| --- | --- | --- | --- |
| 1c | Restrictions of exact B₂ MCSP | If n = o(s) and T³ = o(N), arbitrary blocks admit every isolated pattern up to size (1+o(1))T. After t signed identifications, this holds on any k remaining representatives with t+k ≤ (1−ε)T. On every eligible p-bit block the communication matrix has rank 2ᵖ over every field. | [local isolation](isolation.md) · [signed restrictions](signed-isolation.md) |
| 8a | Joint-type counting | Fix a reference labeling of the addresses with prescribed joint frequencies between label and output. Let I be their mutual information and H the entropy of the output bit, and take s = cN/n. If I < c, almost every reference labeling admits 2^((min(c,H)−I+o(1))N) distinct matching tables of size at most s, and every labeling admits at least that many. If 0 < c < I, only a 2^(−(I−c+o(1))N) fraction of labelings admits even one. A deterministic algorithm running in nearly linear time builds a realization with (N/n)(I_N + O(log n/n)) gates. | [types](types/main.pdf) |
| 8c | Complex zeros of the acceptance polynomial | For a center L, let P_L(z) = Σ z^dist(L,x) over accepted tables x. Assume n = o(s) and s = o(N/n), and define K as the smaller solution of K log(N/K) = s log s. Around every center of complexity o(s), the nearest zero is asymptotic to −W(1/e)K/N, and the rescaled zeros follow Szegő's limit curve. Among centers computable with θs gates, the minimum zero modulus is (W(1/e)+o(1))(1−θ)K/N, attained by exponentially many centers. If K³ = o(N), at a uniformly random accepted center the nearest zero is farther away by a factor tending to infinity in probability. | [zeros](zeros/main.pdf) |

The row numbers match the original summary table. The literature check rated the counting results in 8a as natural sharpenings of Pippenger and Andreev–Clementi–Rolim, and 8c as a new application of Szegő's theorem. Either could at most become a minor paper. The prescribed-marginals manuscript (8b) stays with the results, because the dense lower bound uses its small-cell theorem.

## Barriers and limits of arguments

- [`isolation-barrier.md`](isolation-barrier.md), with [`check_isolation_barrier.py`](check_isolation_barrier.py): a complement-closed language that isolates every small pattern yet has a linear-size circuit. Isolation alone cannot give superlinear bounds.
- [`bounded-flips.md`](bounded-flips.md): sparse perturbations of parity centers have circuits of size 2N plus lower-order terms, so they cannot prove more than that.
- [`ternary-flats.md`](ternary-flats.md): affine tests alone cannot certify all three input choices at a private gate. The 2.52437N bound needs actual synthesis.
- [`quadratic-paths.md`](quadratic-paths.md): quadratic gate-elimination steps can produce leaves that contain no affine plane, even on a (1+ε)N-gate circuit.
- [`parallel-derivatives.md`](parallel-derivatives.md): exact fiber counts after signed merges recover the same coefficient as the signed-identification bound, so better sign choices alone cannot improve it.

## Exploratory computations

- [`four-flips.md`](four-flips.md), with [`check_four_flips.py`](check_four_flips.py): exact costs of flipping pairs of entries in parity extensions, and bounds for two disjoint pairs.
- [`core-faults.md`](core-faults.md): a single flipped entry has different costs over centers of identical clean size.
- [`isolation.md`](isolation.md) and [`signed-isolation.md`](signed-isolation.md): the proofs behind row 1c. [`formal/LocalIsolation.lean`](formal/LocalIsolation.lean) checks its counting step.

## Manuscripts

- [`types/`](types/): joint-type counting (row 8a).
- [`zeros/`](zeros/): complex zeros of the acceptance polynomial (row 8c).

## Failed attempts

[`FAILED-ATTEMPTS.md`](FAILED-ATTEMPTS.md) lists the approaches that did not work and why. It includes the RH/ETH transfer attempts and priority corrections.
