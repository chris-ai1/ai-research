<!-- Copyright (c) 2026 Christian Reitwiessner. -->
Authors: Christian Reitwiessner

# Generic generator-SMT construction campaign

This is a completed GPT Sol research campaign for depth-two threshold circuits. Exact witnesses, failed generalizations, examples, solver logs and reproduction code are retained. The main result is a uniform six-bottom improvement for ordinary Andreev at fixed $k=3$, proved by an exact coefficient certificate and an all-$m$ identity. No restricted-family success is asserted to improve ordinary Andreev.

## Exact specification and coverage

Put $N=2^k$, and $b_i(a)=\bigoplus_{j=0}^{m-1}a_{i,j}$. The implemented problem is

$$\exists\theta\;\forall D\in\operatorname{Valid}_{k,r}\;\forall a\in\{0,1\}^{km}:\quad T_\theta(X(D),a)=G_D(b(a)),\qquad X(D)_c=G_D(c).$$

Index $c$ is little endian. The threshold circuit receives exactly $N+km$ Boolean inputs: all evaluated table bits, then raw address blocks. It receives neither description bits nor intermediate generator values. One fixed parameter vector works across the entire generator family.

Generator sources are numbered 0 (constant false), 1 (constant true), then $2,\ldots,k+1$ (the $k$ input coordinates). There are $r$ gate slots. Slot $j$ has two independent predecessor selectors in $[0,k+2+j)$, allowing equal predecessors and arbitrary fanout, and four independent Boolean LUT entries. For predecessor values $p,q$, the entry index is $p+2q$. The gate is appended as source $k+2+j$. A final selector in $[0,k+2+r)$ chooses the output. Constants and output selection are free; each binary LUT costs one gate. Unused slots are permitted. Consequently descriptions cover **every acyclic circuit with at most $r$ binary LUTs**, not a fixed selected topology. Every such circuit admits a topological ordering and can be padded. No negated input edge is implicit, but negation is a possible LUT. Invalid selector values are excluded explicitly. Constrained integers represent finite selectors, equivalently finitely many description bits; there are no higher-order variables.

At $r=0$ the family consists of the $k$ positive projections and two constants. At $r=1$ it is exactly the functions depending on at most two coordinates: $2+2k+10\binom{k}{2}$ distinct tables, giving 16, 38 and 70 at $k=2,3,4$. Thus $k=2,r=1$ already covers **all tables**. At $k=3,r=2$, exact independent enumeration gives 152 tables out of 256. Five LUTs cover every three-input truth table: two LUTs implement the two-variable cofactors $f_0,f_1$, then three implement $f_0\oplus(c\land(f_0\oplus f_1))$. This is exhaustively regressed for all 256 tables. Repeating Shannon expansion gives a sufficient $r=13$ at $k=4$; no claim is made that these sufficient budgets are minimal. The engine supports these larger budgets, but the productive generator search here concentrates on $r\le2$.

## Circuit model and proof conventions

Each bottom gate is $[w_j\cdot(X,a)\ge t_j]$. The top is $[\sum_jv_jg_j+u\cdot(X,a)\ge\tau]$, with direct raw inputs. Ties are true. $S$ counts bottoms; total gates are $S+1$. Coefficients in saved witnesses are integers or exact rational strings, never floating point. The unrestricted learner allows arbitrary real coefficients and independently arbitrary raw-address signs at every bottom and the top. It does not impose mixed-sign-only, block coherence, integer bounds, or coefficient magnitude bounds. A unit separation on negative examples is imposed without loss on this finite domain, by scaling a strictly separated realization.

There remain $N$ table weights per bottom. The unrestricted real parameter count is $S(N+km+2)+(N+km)+1$. Generator restriction does not reduce that count. Its actual savings are in checking a smaller table family and generating informative concrete examples, with only $4r$ programmable LUT bits and finitely bounded wiring selectors. The symbolic checker still constructs $N$ evaluations; it does not avoid exponential dependence on $k$. It can be slower than the independent raw-table checker because different descriptions alias the same table.

## Search implementation

`engine.py` is the main generic-description CEGIS engine. The unrestricted learner imports the preserved real-weight encoder in `mscore.py`. Initial concrete examples come from valid sampled generic descriptions. Each iteration synthesizes a rational candidate on concrete evaluated tables/raw addresses, fixes it, and existentially searches for a valid description and address violating the equation. SAT counterexamples include a decoded description; independent Python evaluation checks its entire table and target before deduplication and insertion. Batches contain up to 12 distinct evaluated input points. Learner models are exactly re-evaluated on accumulated examples. `latest.json` is explicitly an unproved intermediate candidate; only `verified_*.json` carries a certification result. Every generic-family certified candidate is submitted to the independent `smt_symbolic_check.py` arbitrary-table/raw-address miter. Its counterexamples are saved. They cannot be inserted into the active family unless representable there; a sound UNSAT family checker already rules that out. `r=-1` is an explicitly separate full-table diagnostic mode; it does not pretend to be a generator size.

There are three supplementary construction searches, clearly restricted:

1. **Fixed library CEGIS (`--mode pool`).** Bottom hyperplanes are fixed to inherited diagonal gates at $k=2$, inherited coarse-Fourier gates at $k=3$, or a new exact two-junta Fourier library at $k=4$. Top coefficients and threshold are unrestricted reals. Greedy bottom deletion is attempted with exact top refitting. These bottom gates are block symmetric. Failed/UNKNOWN refits establish no general lower bound. Temporary solver scopes are repaired by reinserting all accumulated examples after rollback.
2. **Complete-grid sparse LP (`lp_campaign.py`).** Enumerate every distinct table in the same generic family, and all block counts after proving block symmetry. Fit top coefficients with iterative reweighted $\ell_1$ objectives. Floating-point optimization is a proposal mechanism only: rational reconstruction is followed by Python arbitrary-precision integer verification of **every signed row**. Positive exact minimum is required. This certificate can prove correctness even when the redundant symbolic family checker is UNKNOWN. Raw-table symbolic checking is still run. With `MIXED=2`, add two independently even-complemented address versions of the library. This mode enumerates **all raw addresses**, uses separate top weights for every raw coordinate, and includes genuinely mixed signs within blocks. Its best witness may select the original coherent sublibrary; no mixed-sign improvement is inferred from the library alone.
3. **Bounded sparse support MILP (`sparse_milp.py`).** Binary selectors choose library support; initial real top/raw/threshold coefficients are bounded by 100 in absolute value, including bottom-output coefficients. After support selection an unrestricted top LP is refit, reconstructed rationally and checked exactly on the complete family grid. A generic symbolic checker and independent full-table checker are also called. MILP time limits retain feasible incumbents, never prove UNSAT. HiGHS numerical optimality/dual bounds are optimizer diagnostics, not exact mathematical lower-bound certificates.

The $k=4$ library is a feasible family construction rather than a known full-table upper bound. For each nonempty character $s$ of size at most two, $h_s=\sum_c(-1)^{s\cdot c}x_c$ lies in $(N/4)\mathbb Z\cap[-N/2,N/2]$ on any two-junta. Put $q=N/4$, take amplitude thresholds $r\in\{-N/2+1,-N/4+1,1,N/4+1\}$, and $H=[h_s\ge r]$. Then $h_s=q(\sum_rH-2)$. With $t_s$ the selected-block address sum, $L=N+1$ and $J=\lfloor |s|m/2\rfloor$,

$$(-1)^{t_s}(2H-1)=4\sum_{j=0}^J[Lt_s+h_s\ge2Lj+r]-2H-2t_s-1.$$

For even $t_s$ the ladder sum is $t_s/2+H$, and for odd $t_s$ it is $(t_s+1)/2$. Walsh inversion has no higher-degree terms on two-juntas, giving the top score $2\sum_c x_c+q\sum_{s,r}(-1)^{t_s}(2H_{s,r}-1)=2Nx_b$, threshold $N$. This explains the library and its coverage; the saved smaller supports are verified independently rather than inferred from this identity.

## Reproduction and environment

Run from this directory with Python 3 and `PYTHONPATH=/tmp/pydeps`; version details are in `environment.json`. Dependencies are Z3, NumPy and SciPy; they are not vendored. `constructions.py`, `mscore.py` and `smt_symbolic_check.py` are preserved local source copies, so reproduction does not depend on other experiment directories. Credit and provenance of the inherited constructions remain in their code and this report.

Examples:

```sh
PYTHONPATH=/tmp/pydeps python3 regression.py
PYTHONPATH=/tmp/pydeps python3 engine.py --k 3 --m 3 --r 1 --S 8 --budget 150 --timeout 15000 --out replay_free
PYTHONPATH=/tmp/pydeps python3 engine.py --k 3 --m 3 --r 1 --mode pool --budget 240 --timeout 8000 --out replay_pool
PYTHONPATH=/tmp/pydeps OPENBLAS_NUM_THREADS=1 python3 lp_campaign.py --k 3 --m 3 --r 1 --rounds 5 --out replay_lp
PYTHONPATH=/tmp/pydeps OPENBLAS_NUM_THREADS=1 python3 sparse_milp.py --k 3 --m 3 --r 1 --seconds 180 --out replay_milp
PYTHONPATH=/tmp/pydeps OPENBLAS_NUM_THREADS=1 MIXED=2 python3 lp_campaign.py --k 2 --m 6 --r -1 --rounds 8 --out replay_mixed
PYTHONPATH=/tmp/pydeps python3 audit.py
```

`batch.sh`, `free_batch.sh`, `milp_batch.sh` and `larger_milp_batch.sh` give the actual later campaign invocations. Earlier runs and their timeout/seed settings are listed in the final matrix. `WARM=path/to/examples.json` reloads examples from an identical or contained family; callers must ensure containment. Different solver versions/seeds may give different models. Exact witness checking is the reproducible result. Time budgets are bounded solver calls, with soft outer budgets checked between iterations; a final checker call may overrun the outer limit. UNKNOWN/timeout is never interpreted as UNSAT.

`regression_results.json` records known ten-bottom $A_{2,3}$/$A_{2,4}$ checks, larger inherited witnesses, generator-family coverage checks, Shannon full coverage, and rational tie semantics. `audit_results.json` independently enumerates the exact generic families and verifies block-symmetric witnesses with integer arithmetic on count grids. Counts cover every raw arrangement only after symmetry is checked for all bottom and top raw coefficients. For mixed-sign circuits the symbolic/raw-grid evidence is retained instead.

## A uniform one-LUT-family construction

A useful generalization from the searches is a simple sign-only reconstruction valid on **all two-juntas**, hence on every valid size-one generic LUT description. For nonempty $s$ with $|s|\le2$, let $h_s(x)=\sum_c(-1)^{s\cdot c}x_c$ and $\operatorname{sgn}(0)=0$. Then

$$F(x,b)=\frac4N\sum_c x_c-2+\sum_{1\le |s|\le2}\operatorname{sgn}(h_s(x))(-1)^{s\cdot b}$$

has $(2x_b-1)F(x,b)\ge1$ on this family. This follows by classifying the sixteen two-input functions, checked in 64 exact cases in `two_junta.py`: constants have no nonconstant Walsh terms; balanced nonconstant functions are a projection, its complement, parity or its complement and have one nonzero Walsh term; a singleton table has three signed Walsh terms whose sum is 3 at its selected point and $-1$ elsewhere, with mean term $-1$. Complements reverse the sign. Embedding into $k$ variables changes the Walsh magnitudes but not their signs, and introduces only zero other coefficients. This argument covers every two-junta, including one-input and constant functions.

Since $\operatorname{sgn}(h)=H_0+H_1-1$, use the ladder identity twice per character. The resulting block-symmetric circuit has

$$S_{r=1}(k,m)=2k\bigl(\lfloor m/2\rfloor+2\bigr)+2\binom{k}{2}(m+2)$$

bottoms plus one top for $k\ge2,m\ge1$. Its explicit integer construction is `two_junta.build(k,m)`, including all $N$ evaluated table coefficients in each bottom. At $k=2$ the family is all tables, but this formula is more expensive than the inherited diagonal construction. At growing $k$, this is only a polynomial-in-$k,m$ gate bound for the heavily restricted generator family, with exponentially many potential table wires; it is not an ordinary-Andreev bound. The optimized finite witnesses below can improve this uniform formula at particular parameters.

The independent generic checker also certifies the inherited 54-bottom $k=3,m=3$ witness for $r=5$ (16.8 seconds in `generic_budget_checks.json`). The explicit Shannon coverage regression proves that this family covers all 256 tables. This is an ordinary-Andreev certification through the requested generator semantics, matching the known baseline rather than improving it.

## Description symmetry and the fair comparison

The natural full-table comparison is **$N$ symbolic raw table bits**, not enumerating $2^N$ concrete tables. The supplied independent miter already uses that stronger baseline. A finite description has length $O(r\log(k+r))$; covering all $2^N$ truth tables requires at least $N$ description bits by counting. Thus genuine description compression of the universal family cannot bypass table information. Restricting $r$ can nevertheless be a useful CEGIS curriculum, exposing failures and generating construction hypotheses cheaply before the full-table test.

In response to the user's suggestion, `xag_encoding.py` implements a second family oracle: sources are false, the $k$ inputs, and earlier gates; literal $2i$ selects a source and $2i+1$ its complement. Each gate is AND or XOR, with sorted literal selectors $p\le q$ (commutative pin symmetry). The output is any signed literal. Inputs, constants and output selection are free. There are $r$ slots, allowing padding with identities. For $r\ge1$ this describes exactly the same function family as at-most-$r$ arbitrary binary LUTs. Every two-input Boolean function is constant, a literal, an AND of signed literals up to output complement, or XOR up to complement; output complements can be carried on outgoing edges. Conversely each XAG gate is a binary LUT, incoming complements can be absorbed into that gate's LUT, and an output complement into the last nontrivial LUT. A signed input output uses one unary LUT, permitted when $r\ge1$. The $r=0$ families differ, so the alternative explicitly refuses that case. Equality is independently regressed on $(k,r)=(2,1),(3,1),(3,2),(4,1)$.

This eliminates generic LUT pin-order symmetry while moving Boolean-function choice into a smaller basis with signed edges. It does not make the universal family smaller. `xag_benchmark.json` retains bounded timings, UNSAT and UNKNOWN separately; a faster/slower encoding is empirical, not implied by its shorter gate basis. Additional safe candidates are requiring output-last with identity padding, canonical treatment of repeated/constant inputs, and canonical ordering of independent nodes. Arbitrary ordering constraints on dependent DAG nodes would require a coverage proof. Canonicalizing by the **entire evaluated table** removes all description aliasing but reverts to the raw-table representation; it is appropriate for the learner's cache, not a new asymptotic compression.

## Main ordinary-Andreev improvement: six fewer bottoms for every m at k=3

The strongest result of the campaign is a uniform fixed-$k=3$ construction:

$$\boxed{S_3^{\mathrm{new}}(m)=6\lfloor m/2\rfloor+6m+\lfloor3m/2\rfloor+20,\qquad m\ge1.}$$

There is one additional top gate. This improves the inherited formula by **six bottoms for every $m$**, leaving slope $21/2$ unchanged. In particular $m=3,4,6$ use 48, 62, 83 bottoms, hence 49, 63, 84 total gates. All table bits are arbitrary. This is not a generator-family-only claim. It is not an optimum claim, a growing-$k$ construction, a subquadratic balanced result, or an improvement to the balanced leading constant $5/16$.

The 49-bottom finite $A_{3,3}$ MILP witness was the first discovery. Its five deleted gates were all table-only Walsh thresholds; none was a ladder gate. That suggested tying each ladder's coefficients together and optimizing the table-only correction instead. `uniform_cancellation.py` uses the inherited thirteen $(s,r)$ atoms, in exactly the order returned by `constructions.atoms3()`. Write $H_j=[h_{s_j}\ge r_j]$. It found one rational score

$$Q(x,b)=u\cdot x-\tau+\sum_j A_j\bigl(\chi_{s_j}(b)(2H_j-1)+2H_j\bigr)+\sum_j C_jH_j$$

with $(2x_b-1)Q(x,b)\ge1$ on all 2048 pairs, with **seven nonzero $C_j$** and all thirteen $A_j$ nonzero. `uniform_cancellation_results.json` contains the rational coefficients and exact proof; `uniform_integer_certificate.json` contains an independent integer certificate. With all coefficients multiplied by 16, they are:

```text
A   = [190,187,188,190,190,185,188,189,190,188,188,191,110]
C   = [-440,0,-220,-324,-344,0,-440,0,0,-444,0,-508,0]
u   = [-68,304,240,244,244,288,296,196]
tau = 1886
```

The minimum signed integer score is 16. Every table and every parity vector is checked using arbitrary-precision integers, with no solver or floating-point rounding required to accept this coefficient certificate.

For each channel the exact ladder identity from above, now with $L=6$ because $h_s\in[-4,4]$ and $r\in\{0,1\}$, gives

$$\chi_s(b)(2H-1)+2H=4\sum_{\ell=0}^{\lfloor|s|m/2\rfloor}[6t_s+h_s\ge12\ell+r]-2t_s-1.$$

Thus use ladder top coefficients $4A_j$, table-only coefficients $C_j$, direct address coefficient $-2\sum_{j:i\in s_j}A_j$ for every coordinate in block $i$, direct table coefficients $u$, and top threshold $\tau+\sum_jA_j$. Exactly six zero $C_j$ remove six table-only gates. This identity holds for every nonnegative integer $t_s\le|s|m$, proving the formula for all $m$, not just tested instances. No intermediate parities or Walsh amplitudes are additional circuit inputs or gates: substitute their affine forms directly into each bottom threshold. Gates are block symmetric, so the result is not a new mixed-sign architecture.

`uniform_cancellation_m3.json`, `_m4.json` and `_m6.json` are full explicit rational witnesses, with independent exact integer count-grid audits. `verify_uniform.py` separately checks the closed integer score and reruns the arbitrary-table/raw-address symbolic checker with longer budgets. Any UNKNOWN symbolic result is recorded as such; the all-$m$ identity and finite arbitrary-table coefficient certificate are independent exact correctness evidence.

## What the independent research bounce changed

At the user's explicit request, another GPT Sol agent inspected the method and ran a separate bounded amplitude-channel search. Its report and artifacts are under `bounce/`; no other agent was used before that request. The weighted-channel run retained cost 21 after 180 seconds, matching slope $21/2$, and produced no slope improvement. The agent discovered a simpler uniform coefficient model for the original thirteen channels: all amplitudes have weight 3 and the raw-table score is $4\sum_cx_c-16$, with exact margin at least 3. This has the inherited gate count, but simpler integer coefficients. The coefficient-cancellation extension above was then constructed and independently reviewed.

The main structural objection is precise. In a score $D(x)+\sum_s f_s(x)\chi_s(b)$ with correct strict signs on every table, **each nonempty character must occur**: substitute its parity table. If that character is absent, orthogonality gives $\mathbb E_b[F(x,b)\chi_s(b)]=0$, contradicting correct strict signs. Generic small-generator families omit most high-degree parity tables (and even some important low-size functions: at $k=3,r=2$, majority and the three-input multiplexer are absent). Channel deletion there does not predict full-table channel deletion.

Furthermore, realizing one separate full ladder for every character costs $\Theta(m\sum_s|s|)=\Theta(km2^k)$, already quadratic at balance $km=2^k$. This is a barrier for that specified **separable full-ladder architecture**, not a lower bound against unrestricted threshold circuits. Improving a few fixed-$k$ table-only coefficients is valuable but does not address this main cost. A general subquadratic route must share bottom hyperplanes across characters, share localized ladder windows, or use a different score representation. Sign-correct restricted-family circuits also do not automatically compose into a universal one: a decomposition needs exact values, controlled margins and ranges, or jointly gated shared features.

## Final matrix, negative results, and next steps

See `campaign_matrix.md` for every unrestricted CEGIS, library CEGIS, LP and MILP run, including attempted bottom budgets, feasible supports, solver statuses and family/full symbolic checks. `campaign_matrix.json` links exact witnesses. `twojunta_results.json`, `generic_budget_checks.json`, `xag_benchmark.json`, `canonical_benchmark.json` and `uniform_integer_certificate.json` record the additional construction and encoding regressions. Finite-grid exact certificates are independent of symbolic UNKNOWN.

The main unrestricted-real targets were $(k,m,r,S)=(3,3,1,8)$ (15-second learner calls, then a 60-second warm restart), $(2,6,1,18)$ and $(2,8,1,23)$ (30-second calls), plus $(2,6,0,6)$, $(2,8,0,8)$, $(3,4,0,8)$, $(4,2,1,12)$, $(4,3,1,16)$ and $(3,6,1,18)$ (20-second calls). A canonical-XAG repeat at $(3,3,1,8)$ also used 20-second calls. Each ended UNKNOWN without a certified witness; these runs do not exclude the requested sizes. The freely signed main learner thus remains implemented and exercised, but the successful circuits were discovered using a restricted Fourier bottom library. All main engine seeds were 1. Outer budgets were 100 seconds for `free_batch.sh`, 150 seconds for the first free $k=3,m=3$ and $k=2,m=6$ runs, 180 seconds for its warm restart, 120 seconds for free $k=2,m=8$, and 80 seconds for the canonical-XAG repeat.

Library-Cegis budgets were 180 seconds at $k=2$, 240 seconds at $k=3,4$ (300 seconds for the full-table $k=3,m=3$ run). Per-call timeouts were 5 seconds for `pool_k2m6r1`, 8 seconds for `pool_k2m8r1` and `pool_k3m3r1`, 20 seconds for `pool_k3m3r2`, 15 seconds for `pool_k4m2r1` and `pool_k3m3full`, and 30 seconds for `pool_k2m8r1_long`. Fixed-top/full-table attempts at $k=2,m=8$ reached UNKNOWN in the checker even with 30 seconds, illustrating that descriptions are not automatically an efficient miter. Full known-witness regression is still exactly correct by the independent count audit.

The strongest restricted-family MILP witnesses are 32 bottoms at $(3,3,r=1)$, 47 at $(3,3,r=2)$, 43 at $(3,4,r=1)$, 59 at $(3,6,r=1)$, 49 at $(4,2,r=1)$, and 60 at $(4,3,r=1)$. They have exact complete-family certificates, and each is refuted on arbitrary tables. Several symbolic family checks timed out, recorded separately. The full-table MILP obtained 49, 63 and 86 bottoms at $k=3,m=3,4,6$ before the uniform cancellation model improved these to 48, 62 and 83. The mixed-sign enriched $k=2,m=6$ pool retained the 19-bottom inherited count. No smaller full-table $k=2$ or full-table $k=4$ circuit was established. All MILP “optimal” labels concern numerical bounded/library optimizers only; no exact optimality theorem is asserted.

The LUT/XAG comparison found similar runtimes: on the inherited 54-bottom $k=3,m=3$ witness, LUT/XAG used about 11.6/11.5 seconds at $r=2$ and 13.9/14.4 seconds at $r=5$. On the new 49-bottom witness, XAG and canonical XAG used about 9.7 and 10.9 seconds in a separate paired run. These single bounded trials establish no stable performance ranking. Canonicalizing descriptions changes the checker and counterexample order; it does not remove any of the learner's table-weight parameters. The canonical-XAG learner run also timed out.

Next steps for **general** upper bounds:

- Use generic descriptions as a staged table curriculum, then certify or repair against arbitrary raw tables. Include parity tables of every degree, majority and multiplexer tables early; the small families here omit critical tests. Add exact whole-table deduplication and counterexample diversity so many equivalent descriptions do not dominate learning.
- Use the new uniform integer score as a simpler controlled-margin starting point. Optimize jointly the amplitude channels, localized ladder windows and table-only corrections. The six removed table-only gates prove that product-by-product implementations can have avoidable overhead, but alone do not improve the slope.
- To beat the balanced quadratic architecture cost, search for a common bottom gate serving several Walsh characters or jointly reconstructing several localized products. Investigate hyperplanes outside the individual $h_s+Lt_s$ forms, with independently mixed raw-address signs. Charge table coefficients and actual support wires as well as gates; a restricted-generator gate saving can retain exponentially many table wires.
- Pursue exact score identities or quantitative margin/range guarantees that allow composing useful generator-family modules. Separate sign correctness of modules is insufficient to combine them into arbitrary table correctness.

The campaign ran approximately 32 minutes on 2026-11-07 UTC, with a final archival/audit phase afterward. All experiment-owned solver jobs completed; no unrelated job was stopped. Files were staged into the private continuation archive, with checks and push status reported in the final response. No PR was created and no privacy setting changed.
