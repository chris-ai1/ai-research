# Mixed-sign depth-two upper bounds for Andreev's function: pool LPs, periodic constructions, obstructions

Directory: `/tmp/andreev_gap/mixed_upper/`. All scripts run with `python3 -I` and add `/tmp/pydeps` themselves.
Logs are in `logs/`.

Notation follows the task:
- $N=2^k$ table bits $x_c$, and $k$ address blocks of $m$ bits, with $s_i=|a_i|$, $b=s\bmod 2$, $A=x_b$, $n=N+km$.
- The table index is $c=\sum_i b_i2^i$; for $k=2$ a table is written $(x_{00},x_{10},x_{01},x_{11})$.
- $e_S=t_S\bmod 2$ with $t_S=\sum_{i\in S}s_i$, and $\chi_S=(-1)^{t_S}=1-2e_S$.
- A *part-symmetric* gate has weights that are constant on each part of a fixed partition of every block; *block-symmetric* is the case of one part per block; *two halves* means two parts of sizes $\lceil m/2\rceil,\lfloor m/2\rfloor$ with counts $(u_i,w_i)$.
- The *slope* of a family at fixed $k$ is $\lim S(k,m)/m$.

Labels: **[PROVED]** complete proof here; **[VERIFIED]** exact computation (exact integer/rational arithmetic, or a CP-SAT/LP certificate with the stated bounds); **[EVIDENCE]** heuristic search only; **[CONJECTURE]**.

PLACEHOLDER-SUMMARY
