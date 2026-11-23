<!-- Copyright (c) 2026 Christian Reitwiessner. -->
Authors: Christian Reitwiessner

# Continuing the research

Latest research snapshot: [9 November 2026 update](UPDATE_2026-11-09.md) — completed coherence, one-table-bit, and extractor investigations; proof and review status retained.


Read RESEARCH_STATE.md first. The primary objective is a smaller exact THR∘THR construction for ordinary Andreev, ultimately below quadratic size. Prioritize construction discovery over formalization; Lean verification can follow later.

## Current work

The earlier majority, small-instance SMT, mixed-sign upper-bound, and coarse-Fourier tasks have finished. Their reports are in `experiments/maj_sol`, `variants_sol`, `mixed_upper_sol`, and `coarse_mixed_general`. No old solver process needs resuming. The last report gives an exact localized mixed-sign product gadget, a varying-width cancellation identity, and a restricted obstruction for one middle-layer architecture. It obtains no subquadratic family. Pooling across growing-k characters is open.

The generator-SMT Sol campaign is completed and archived in `experiments/generator_smt_sol/`. Read its `report.md`, `campaign_matrix.md`, and independent `bounce/review.md`. It implements generic bounded binary-LUT descriptions and a symmetry-reduced AND/XOR alternative; the threshold circuit always receives only evaluated table bits and raw addresses. Small generator families are useful as a curriculum, not a compression of all table inputs. Full coverage at k=3,r=5 is checked; r=1 and r=2 are incomplete (38 and 152 of 256 tables).

The main new **ordinary-Andreev** result, independently reviewed and exactly certified, is

$$S_3(m)=6\lfloor m/2\rfloor+6m+\lfloor3m/2\rfloor+20$$

bottom gates plus one top, for every $m\ge1$. This removes six table-only gates from the inherited formula and keeps slope $21/2$. The fixed rational coefficient certificate covers all 2048 table/parity pairs; an exact ladder identity proves all m. Explicit m=3,4,6 witnesses have 48,62,83 bottoms and exact full-domain integer audits. The arbitrary-table symbolic checker verifies m=3; longer m=4 and m=6 checks remain UNKNOWN/timeouts, separately recorded. The uniform proof is independent of those timeouts. This does not improve the growing-k balanced leading constant.

Other exact family-only witnesses include k3m3 r1:S32, r2:S47; k3m4 r1:S43; k3m6 r1:S59; k4m2 r1:S49; k4m3 r1:S60. Each fails on arbitrary tables. Unrestricted-real CEGIS trials reached UNKNOWN. Canonical XAG descriptions preserve coverage but did not show a speedup in bounded comparisons. The independent agent's critique explains why dropping a few separable Walsh channels cannot beat the general full-ladder quadratic cost. Prioritize sharing bottom gates across characters or localized windows, using controlled-score identities rather than composing sign-only restricted-family witnesses. All experiment-owned jobs finished; do not resume old solvers blindly.

## The generator-SMT encoding: the essential quantifiers

Fix a finite Boolean gate basis and a size bound r for a k-input, one-output generator circuit. A description D specifies its gates and wiring. A fixed evaluator computes G_D(c). The table supplied to the candidate threshold circuit is

$$X(D)=(G_D(c))_{c\in\{0,1\}^k}.$$

The synthesis problem is

$$\exists\theta\ \forall D,a:\quad
\operatorname{Valid}_r(D)\Longrightarrow
T_\theta(X(D),a)=G_D(b(a)).$$

Here b(a) is the vector of address-block parities. The same threshold parameters θ must work for every valid generator description and address. The threshold circuit receives **evaluated table bits**, never D, generator gate values, or a description-dependent choice of weights. Universal descriptions are represented by finitely many symbolic bits and a universal evaluator, not higher-order quantification.

Use counterexample-guided synthesis: a learner finds θ on concrete evaluated tables and addresses; a checker fixes θ and searches existentially for valid D and a violating the equality. A SAT checker model supplies a new concrete example. An UNSAT checker certifies correctness on the declared generator family. A timeout or UNKNOWN certifies nothing. Record the family, basis, size convention, and validity rules.

Restricting descriptions restricts the table family unless coverage of all tables is proved. Family correctness alone is not an ordinary-Andreev upper bound. When a promising candidate is found, check it independently against arbitrary raw table bits and addresses. Reusing identical evaluated tables is allowed. Retaining all 2^k evaluated inputs also retains that many possible weights per bottom gate: generator encoding does not automatically shrink the synthesis parameter count.

Avoid the incorrect alternatives ∃D choosing an easy generator, ∀D∃θ giving a different circuit for each table, or feeding description bits to T. All three change the problem.

## Useful implementation starting points

- `workspace/smt_symbolic_check.py`: arbitrary-table symbolic miter, avoiding full truth-table enumeration. It is not itself the generator encoding.
- `experiments/mixed_sign/mscore.py`: existing real-weight learner and circuit conventions.
- `experiments/variants_sol`: earlier CEGIS experiments and failed candidates.
- `experiments/mixed_upper_sol`: exact construction certificates and ten-bottom A_(2,3)/A_(2,4) witnesses.

The top threshold may read the raw table and address inputs as well as bottom outputs; count S bottoms and S+1 total gates. Use exact rational/integer checking for any reported witness. A bounded integer-weight UNSAT result is only about that weight bound. Keep gate counts separate from coefficient multiplicity and wire counts.

Use increasing bounded budgets and persist progress promptly. Start with modest generator sizes and larger k,m; compare alternative targets with baselines before long runs. Aim for a useful SAT construction rather than prolonged attempts to prove small sizes impossible. Negative finite searches do not settle an asymptotic upper bound.

## User preferences

- Credit new files to **Christian Reitwiessner**. Preserve original contributors and mathematical citations in archived files.
- Use dollar-delimited mathematics in explanations.
- Use GPT Sol for the SMT work and for unfinished tasks that hit another provider's rate limit.
- Seek clever upper bounds. The user mostly trusts research proofs and intends Lean verification later.
- For the coarse-Fourier direction, require genuinely different mixed signs *inside* relevant blocks across gates. Merely giving different blocks uniform signs or applying one common input reorientation is not the requested direction.
- Keep proved results, exact finite checks, heuristic candidates, UNKNOWN, and conjectures distinct.

## Reproduction and updating

`tools/verify_archive.py` checks preserved file hashes. `tools/run_experiment.py` makes a writable staged copy and translates old absolute paths there; inspect scripts before running expensive searches. Dependencies are recorded, not vendored. Original logs and witnesses are retained verbatim, including obsolete claims; consult the curated summary for corrections.

After a new completed experiment, copy its whole directory into `experiments/`, update the curated notes, regenerate MANIFEST.json, run the integrity checker, and commit/push. Do not include installed dependencies, credentials, caches, or transient work copies. The original chat is not required to interpret the mathematical state in this archive.

## Latest continuation update: Astra investigations

The lower-bound Astra task completed; its three hand-proof proposals are archived in `experiments/lower_astra/report.md` and summarized, explicitly pending independent review, in RESEARCH_STATE.md section 7. Prioritize reviewing the VC class/adaptive-survivor argument before upgrading the small-advantage gate range to established status. The upper-bound Astra task is still running at this update. An older `mixed_upper/batch_finite.sh` solver batch was found still running after the generator campaign; do not infer that all historical processes stopped from an individual task's completion. No new jobs were left by the lower-bound Astra task.

## Both Astra tasks completed

The upper report is now archived as `experiments/upper_astra/report.md`. Read RESEARCH_STATE.md section 8 for its distributional $n^{3/2}$-up-to-logs construction, exact k4 certificate, and two explicit missing lemmas for exact subquadratic constructions. The highest-value upper follow-ups are economical shared tail repair and a sparse table-bit-gated selector dictionary. Both requested Astra tasks have finished and left no task-owned jobs. Lower proposals in section 7 still await independent review; upper analytical results also await independent review, while the k4 integer certificate received a separate parent recheck. Historical background processes should be checked separately if their status matters.

## Important correction: existing average-case bounds

Before treating any truncated-ridge approximation result as new, read `workspace/threshold_paper/paper.tex` theorem `thm:avgupper` and `workspace/andreev_depth_two_bounds.md` Theorem 2. They already give the same near-perfect-agreement bound and the epsilon-squared tradeoff. Astra's mixed-sign variant improves no asymptotic average-case upper bound. The earlier handoff omitted this fact and caused an overstated announcement; RESEARCH_STATE.md now explicitly corrects it.

## Latest upper-bound round completed: actual logarithmic saving

Astra round 2 is archived as `experiments/upper_astra_round2`. Unlike round 1's rediscovery, it replaces the approximation union bound by independent mixed-mask cancellation of cross-character error moments and an L2 estimate. Read RESEARCH_STATE.md section 9 and the report before quoting formulas: constant error now needs $O(n^{3/2})$ gates, and advantage epsilon has $O(epsilon^2 n^{3/2} sqrt(log(1/epsilon)))$ gates over the stated small-advantage regime. These are hand proofs, not Lean formalized or separately referee-reviewed. Exact bounds are unchanged. Next mathematical verification should focus on mask-selection quantifiers, mean-square cancellation, tail second moments, and threshold tie handling. Further exact progress still needs shared worst-case tail repair.

The explicit paper-versus-new comparison, parameter ranges, constant-advantage gaps, and Kane–Williams distinction are logged in RESEARCH_STATE.md section 10.


## Latest exact-construction update

The creative worst-case-only Astra task completed and is archived as `experiments/exact_creative_astra`. RESEARCH_STATE.md section 11 records newly verified 8/32/36/256-bottom upper bounds at (k,m)=(3,2),(3,3),(3,4),(4,4). These supersede older finite counts for those instances; the older +20 all-m k3 formula remains useful for its uniform statement/slope. Read the rank-permutation identity and monochromatic-plane sign-margin mechanisms before starting more Fourier searches. The m2 rank bound N is a genuine all-k family but highly unbalanced. No balanced subquadratic family, all-m slope improvement or necessity of superpolynomial-in-n weights was established. The parent reran the saved exact all-input verifiers successfully. The strongest immediate proposed experiment is one-sided gate selection on the A4,4 cover; the deeper target is comparison sharing across table labels.


## Latest user scope and asymptotic restart outcome

The user is interested ONLY in asymptotic exact worst-case upper bounds for balanced growing-k Andreev, and asked for a highly creative restart. `experiments/asymptotic_creative_astra/report.md` records no improved asymptotic bound. It falsifies the small-channel periodic positional rank-repair idea and proposes, without proving, a separately gated threshold-code lemma that would yield $O(n^2/log n)$. Read RESEARCH_STATE.md section 12 for the precise limitations. Do not present its compiler or unproved target as an upper bound. No new jobs remain from this task, and no new task is implicitly authorized merely by its completion.


## Coefficient-language design and latest blocker context

The user now asks for an Astra design of multiple or parameterized coefficient-rule languages that control SMT difficulty while generating uniform exact circuit families. This is the active design task. Its brief includes all upper/lower blockers, direct independent raw-table inputs, shared rules across sizes, solver-fragment/normalization issues, and accurate prior runtimes. The separate completed asymptotic pass2 is archived as `experiments/asymptotic_creative_astra_pass2`; it yields no upper improvement but rules out specific scalar Walsh shrinkers, including raw-affine repair. This new context has also been sent to the language agent. Treat these as scoped architecture obstructions, not general no-go statements for a DSL.


## Coefficient-language task completed

Read `experiments/coefficient_language_astra/report.md` and RESEARCH_STATE.md section 14. Astra recommends an affine-hole public-index language plus a complementary additive atom language, with vector-valued nested resource bounds and alternative finite-state/decision/tensor generators. `rules.py` is a tested compiler/evaluator/miter-export prototype, NOT a completed synthesizer. Parent reran eight tests and three expected SMT outcomes successfully. The natural next engineering task, only when requested, is an exact shared-rule multi-size CEGIS learner using raw table bits, strict tie semantics and scoped grammar claims. No new upper-bound family was proved. All requested Astra tasks have now completed; historical detached processes require separate status checks.


## Shared-rule experiment now completed

The previously missing affine-hole learner has now been implemented and run at the user's request: `experiments/uniform_rule_smt`. Read its report and RESEARCH_STATE.md section15. Two shared multi-size skeletons plus curricula, a300s balanced n32-only run and frozen-bottom diagnostics found no new verified circuit. Calibration and four exact infrastructure tests passed. All actual constraints, counterexamples, parameters, initialization policies and runtimes are saved. No experiment-owned solver remains. Do not describe this as a full structural grammar search or unrestricted n32 circuit optimization; the unknowns are shared coefficients of fixed public feature menus.


## Latest requested experiment: n64 UNSAT targets completed

The user requested lower-bound feasibility at n64 with small bottom budgets. `experiments/n64_unsat` and RESEARCH_STATE.md section16 preserve both model conventions, exact timing/results and exported UNSAT instances. Strongest proved conclusion: at least4 bottoms/5 total via an exact parity8 restriction valid in both64-input targets. Four-bottom600s direct runs, five-bottom300s balanced run and parity10/S4 edge probe all remained UNKNOWN. This is unrestricted real-gate feasibility, not a coefficient-language lower bound, and no n64 optimum or new asymptotic lower bound was established. All experiment-owned jobs ended. Read exact definitions before reusing “balanced n64”: it uses unequal block lengths, while equal-block A4,12 is64 inputs but has a16/48 split.


## Current manuscript now updated

The user requested a selective paper update. The source/PDF in workspace/threshold_paper now include the refined5/16 exact bound and improved mean-square average-case upper bounds, with complete proofs, updated summaries and accurate merged/open Lean statuses. Read RESEARCH_STATE.md section17 and the paper's REVISION.md. The PDF is19 pages and built/checked cleanly. Finite solver records, language experiments and failed approaches stay in this archive rather than the paper. No experiments or reviews are running from this paper-editing task; no new research pass is implicitly requested by completion.

## Completed modern-extractor investigation

Read `experiments/extractors_astra/report.md` and RESEARCH_STATE.md section 19 before proposing an extractor transfer. Both upper and lower routes were investigated for unrestricted ordinary Andreev, exact and uniform average case; no new unrestricted exponent was obtained. The report gives explicit source, entropy, seed, error, independence, depth, and table-lookup obstacles, and separates generalized functions from this target. Its elementary one-table-bit bound is superseded by the completed slicing result, and is labeled accordingly. The stronger restricted results remain intact.

The final report, evidence record, standard-library checker, check results, and exponent chart are archived together. Run `python3 experiments/extractors_astra/verify_claims.py` to reproduce the finite checks, then `python3 tools/verify_archive.py` to check archive integrity. The former deterministically rewrites its own `verification.json`. Hand derivations are not independent referee certifications or Lean formalizations. No further research or review assignment follows merely from this archive update.

## Completed ETH matrix transfer investigation

Read `experiments/eth_transfer/report.md` and RESEARCH_STATE.md section 34 before proposing a direct transfer of the ETH parity interpolation or low-rank SWAP construction. The correction supported on r Walsh characters costs O(rn) bottom gates; the structured main term still contains shifted lookups. No upper bound was improved. The more concrete open route is a short signed affine-slice decomposition, connecting the SWAP equality structure to the earlier mixed-sign hyperplane constructions. Logical-label equalities cannot be treated as free affine constraints on raw addresses. `verify.py` reproduces the exact finite checks; no research process remains running.


## Further mixed-sign routes examined

Read `experiments/noncoherent_routes/report.md` and RESEARCH_STATE.md section 35. The strongest proposed relaxation is a sum of dense-table adaptive slabs, where two bottom gates let a table form control a signed address window's width. Diagonal packing can share changing table thresholds across address slices. Exact identities and quadratic noncoherent baselines are checked; a subquadratic all-table decoder remains unproved. Walsh masks provide a family with no common bounded-run ordering/reorientation. Do not treat either the primitives or the mask generator as a new upper bound.


The adaptive-slab follow-up is in `experiments/noncoherent_routes/followup.md`. Exact dense-table decoding produces a binomial window. Plain alternating shifts vanish; degree-(t-1) polynomial weights restore parity but retain linear address-range cost. Two finite LP witnesses prove complete feasibility of a dense-table atom pool, with large noncompetitive gate counts and independently verified integer margins. The next useful question is sharing across decoded products, not larger unstructured pool fitting. All search processes completed.
