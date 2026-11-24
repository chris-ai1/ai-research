# Size of almost-universal hash functions and PRFs: 2n + o(n) and 3n

> **Unreviewed.** Everything here is an AI-written proof from one research thread (24 November 2026).
> No human has checked any of it. Two of the three notes were read once by a second AI agent; the
> third has had no review at all. Nothing is formalized. The literature search for later work on
> these questions was shallow. Treat every statement as a claim, not a theorem.

Starting point: Fan, Li, Yang, [ECCC TR21-125](https://eccc.weizmann.ac.il/report/2021/125/) (FLY)
and Chen, Li, Yang, [ECCC TR22-086](https://eccc.weizmann.ac.il/report/2022/086/) (CLY). They build
almost-universal hash functions and PRFs with `2n + o(n)` gates over the full binary basis, prove
`2n − O(1)` lower bounds, and use the hash for hardness magnification.

The work is by proof only. There are no computations or experiments.

## Claims

Notation: `n` inputs, `m` outputs, collision probability `2^{-ℓ}`, security against time `T`.

| Claim | Before | Note | Review |
|---|---|---|---|
| Hash of size `2n + n·2^{-Ω(log² n/ℓ)}` with seed `O(ℓ)`, for `ω(log n) ≤ ℓ ≤ c log² n/log log n` | size `2n + O(n/log log n)` at the top, seed `O(ℓ log^{1+β} n)` (CLY) | [hash](hash-seed-complexity.md), Theorem 3 | one AI review |
| Every hash family needs `2n + n·2^{-O(log² n/ℓ)} − 3m` gates (any gates, also nonlinear hashes) | `2n − 2m` (FLY) | [hash](hash-seed-complexity.md), Theorem 1 | one AI review |
| A `T`-secure PRF needs `2n + n·2^{-O(1 + log² n/log T)}` gates; in particular `2n + n^{1−o(1)}` for polynomial security | `2n − O(1)` (FLY) | [PRF](prf-lower-bound.md), Theorem 4 | one AI review |
| Collision probability `2^{-ℓ}` needs `3n − O(n log² n/ℓ) − 4m` gates; a `T`-secure PRF needs `3n − O(n log³ n/log T)` | FLY ask for a `2n`-size hash with inverse sub-exponential collision probability; their non-uniform construction has `3n` | [3n](three-n-bound.md), Theorems 7 and 8 | **none** |

Consequences claimed in the notes, not rechecked in detail: sharper thresholds in CLY's
magnification theorems (for MCSP at `s = n`: `2N + N^{1−Ω(1/log log N)}`), a smaller kernel for
sparse NP languages, and PRFs of size `2n + n^{1−o(1)}` for superpolynomial security.

## What would need checking first

1. Theorem 1 of the hash note (the separator argument) and Lemma 2 (the detector needs only
   `O(ℓ/log n)`-wise independence). The other results build on them.
2. Lemma 5 of the PRF note (the type lemma) and the case analysis of Lemma 6.
3. All of the 3n note, in particular Lemma 9, the use of Alon–Hoory–Linial in Lemma 10, and
   Section 4, which depends on a reference whose parameters were not checked.
4. Whether any paper after 2022 already contains these results.
