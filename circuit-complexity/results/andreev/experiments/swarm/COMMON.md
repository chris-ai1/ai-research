Authors: Christian Reitwiessner

# Common brief for the four swarm agents (UP1, UP2, LOW1, LOW2)

Read this first, then your own task. The user wants **wildly creative, genuinely new ideas**, and cares **only about asymptotics**: exponents of $n$. Constants and polylog factors do not matter. Small-instance computation is only a sanity check or a way to test an asymptotic hypothesis on a growing family.

## The problem

- $N=2^k$ table bits $x_c$ ($c\in\{0,1\}^k$), and $k$ address blocks of $m$ bits $a_{i,1..m}$ with $s_i=|a_i|$.
- Address $b_i=s_i\bmod 2$, output $A(x,a)=x_b$. Input length $n=N+km$. Balanced case: $km=N$, so $n=2N$, $k\approx\log_2 n$, $m\approx n/(2\log n)$.
- Circuit: $S$ bottom threshold gates $[\alpha\cdot x+\gamma\cdot a\ge\theta]$ with arbitrary real weights, and one top threshold gate reading the bottom gates **and the raw inputs** (so any affine function of the inputs is free at the top).
- Size = number of gates. Exact computation on all inputs unless stated.

## State of the art (unrestricted model)

$$\Omega\bigl(n^{3/2}/\log^2 n\bigr)\ \le\ S\ \le\ \bigl(\tfrac5{16}+o(1)\bigr)n^2 .$$

**Goal: change an exponent.** Either an upper bound $n^{2-\varepsilon}$, or a lower bound $n^{3/2+\varepsilon}$, for the unrestricted model. A new exponent in a natural restricted model is a valid second prize if it is not already in the table below.

## What is known (do not rediscover)

Master summary: `/home/user/.t3/scratch/2026-11-02-improve-upper-bound-of-andreevs-93c6aee6/research_backup/docs/RESEARCH_STATE.md`. Reports are in `/home/user/.t3/scratch/2026-11-02-improve-upper-bound-of-andreevs-93c6aee6/research_backup/experiments/<name>/report.md` (below: `exp/<name>`). The paper is `/home/user/.t3/scratch/2026-11-02-improve-upper-bound-of-andreevs-93c6aee6/threshold_paper/paper.tex`; a short readable account of the two main results is `threshold_paper/explainer.md` in the same folder.

Upper bounds
- **$\tfrac5{16}n^2$ exact** (paper Thm 5; explainer §2). Fourier lookup $\sum_S X_S(-1)^{t_S}=N(-1)^{x_b}$ with $t_S=\sum_{i\in S}s_i$; each product becomes functions of single linear forms; functions of a linear form telescope into threshold gates ("staircases"); quadratic leftovers collapse when summed over $S$. Every gate sees a block only through $s_i$. Cost $\approx N$ characters $\times$ ($N/2$ table range + address range).
- **Average case**: agreement $1-\delta$ with $O(n^{3/2}\sqrt{\log(1/\delta)})$ gates; advantage $\varepsilon$ with $\tilde O(\varepsilon^2n^{3/2})$ gates (paper Thm 6). Staircases are truncated to a concentration window. The matching lower bound $\tilde\Omega(\varepsilon^2n^{3/2})$ holds. So **fixed error has exponent exactly $3/2$**; exact computation is where the gap is.
- **One-table-bit model** (each bottom gate reads at most one table bit): $O(n^{1+\log_2 3})$ via dominating kernels $K_c=(2k)^{|c|}[c\subseteq b]$ (`exp/one_table_bit`).

Lower bounds
- **$\Omega(n^{3/2}/\log^2n)$, unrestricted**: Kane–Williams random restriction (one live bit per block), gate survival $O(k/\sqrt N)$ by Littlewood–Offord, then counting restricted circuits with fixed weights (paper §5).
- **Sign-coherent gates** (in-block weights of one sign): $\Omega(n^2/\log^3n)$ (paper App. B; explainer §3). Walk over all unit cubes of the block-count grid; entropy forces $\approx N/(3k)$ non-constant gates per cube; a coherent gate is non-constant on at most one cube per diagonal line.
- **One-table-bit model**: $\tilde\Omega(n^{32/19})$ for arbitrary real weights, by a *table-pair* reduction to hypercube edge slicing (Sauermann–Xu, arXiv:2510.16592): compare the top scores on two single-one tables whose indices differ in one address bit; gates reading neither table bit cancel; the survivors must slice every edge of an $m$-cube. With bounded integer address weights: $\Omega(n^2/\log n)$ (arXiv:2507.00773, Cor. 1.2). (`exp/review_coherence`, `exp/one_table_bit`.)
- **Structure**: a circuit with $n^{2-\varepsilon}$ gates contains $\tilde\Omega(n^{3/2})$ gates whose in-block weights nearly cancel (relative drift $n^{-\varepsilon+o(1)}$), under a weight-comparability hypothesis (`exp/coherence_fable`, corrected in `exp/review_coherence`).
- **Parity link**: fixing the table to $x_c=y\oplus|c|$ gives parity on $km+1$ bits. Depth-two parity with arbitrary gates: best known lower bound is polynomially below linear (it is the hypercube slicing problem); coherent gates need $\lfloor M/2\rfloor$.

Barriers
- **Survival barrier**: under any restriction leaving one live bit per block, a random $\pm1$ gate is non-constant with probability $\ge 1/(2\sqrt{2km})$, and a restricted circuit needs at most $N$ survivors. So per-gate survival counting stops at $n^{3/2}$ (`exp/push_lower` §5).
- **Communication**: $A$ has $O(k)$-bit protocols under every input partition, so plain discrepancy / sign-rank arguments over a bipartition give nothing near $n^2$.
- **Extractors**: no gain found (`exp/extractors_astra`).
- **Known false claims** (do not reuse): "staircases are sign-blind" as a general proposition (attainable values can have gaps); a pointwise $O(V/m)$ smoothness lemma for balanced $\pm1$ gates; "each table coefficient must concentrate on its own address class"; that the simultaneous-entropy barrier limits *all* per-gate methods.
- Dead ends already explored for the upper bound: sharing staircases across characters; lex-packing with large weights; sign-only Walsh reconstruction with equal weights (fails at $k=4$); translates of one middle-layer kernel; pure-parity constructions (need $\ge n^2/16$); pooling by table chunks (same $N^2/2$ count).

## Working rules

- Work only in your own folder under `/tmp/andreev_gap/swarm/`. Write `report.md` there **incrementally**, after each major idea, so progress survives an interruption (API rate limits have killed earlier runs).
- Label every claim **[PROVED]** (complete proof written), **[VERIFIED]** (computation), **[CONJECTURE]**, **[REFUTED]** or **[KNOWN, source]**. Be skeptical of your own proofs: a claimed exponent change is a major result and will be refereed adversarially. Check every bound against the table above; a lower bound may not exceed a known upper bound in the same model, and vice versa.
- **Use the board** `/tmp/andreev_gap/swarm/board.md` (rules at its top) to bounce ideas. Post candidates early, attack other agents' candidates, answer requests. The other agents' folders (`up1`, `up2`, `low1`, `low2`) are readable; read their `report.md` when the board points you there.
- Python: `python3 -I`, with `sys.path.insert(0,'/tmp/andreev_gap/coherence_fable/pydeps_local')` for numpy/scipy/ortools/pysat. z3 is in `/tmp/pydeps`. The disk is almost full (about 8 GB free): do **not** install packages or write large files.
- Do not kill processes you did not start. Post nothing online. Web search and reading papers are fine; cite only what you actually read.
- Use `$...$` for inline math and `$$...$$` for display math.
- Do the work yourself; do not start subagents.

## Final reply

State the strongest result with its exponent and status, the complete proof or construction (or where it is in your report), what you posted to and learned from the board, the dead ends with reasons, and the single most promising next step.
