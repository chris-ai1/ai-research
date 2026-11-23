
## 6. Negative findings (and why)

1. **Mixed signs gave no improvement anywhere** [EVIDENCE + PROVED pieces].
   - $k=2$, periodic, best slope found in every class: 3 (two halves at period 4, block-symmetric at periods up to 8; §4.1). The optimal two-halves solutions used only block-symmetric directions $\beta=(2,2\,|\,\cdot)$.
   - $k=2$, finite pools: the mixed pool was never better than the block-symmetric pools (§4.2).
   - Explanation (Lemma 2.6): in the periodic world, mixing cannot make signal-carrying atoms cheaper. It only reshuffles the fluctuations of fluctuating atoms, and those were never used by any optimum.
2. **Fluctuating (long-period) atoms never helped** [EVIDENCE]. They are the only periodic mechanism that could beat pure parity. Every unrestricted solution found, at every $P$, used pure parity atoms only. When the pure $\{1,2\}$ atom was priced out, fluctuating $(1,-1)$ atoms were used, but three of them were needed (slope 3.5 instead of 3).
   - The reason is a mismatch between signal and noise. A fluctuating atom carries a parity signal of amplitude $g/2$ but varies by $p-g$ inside a parity class, and the pure-character tables (dictators, XOR) force strict amplitude dominances (proof of Theorem 2.4). A signal that small cannot tip them without its own fluctuation flipping a sign somewhere.
   - Exact cancellation of fluctuations across atoms is impossible, because distinct atoms fluctuate along distinct characters of $(\mathbb Z/P)^d$. Cancellation within one $(\beta,\alpha)$ family just rebuilds a pure parity atom at the same cost.
3. **One gadget per character fails** [PROVED for $k=2$ (any amplitudes) and for monomials at all $k$; VERIFIED for $k=3$, any amplitudes]. The obstruction is the pure-character tables: each forces its own character's amplitude to dominate the others.
4. **Minterm-style designs** (one gate detects one address on many cubes) are impossible: no hyperplane is parity-pure for two characters (Lemma 2.7).
5. **Bounded numbers of views** ($s_i$ plus $D_i$, two halves, $r$ parts) cannot reach $n^{2-\epsilon}$. This is class (c) of `mixed_sign` plus Lemma 2.6. In the periodic world they cannot even lower the pure-parity bound $n^2/16$.
6. **Generic pools are bad features.** $L_1$ over large mixed pools gives much worse supports than over block-symmetric pools ($m=3$: heuristic 37 vs 17), which matches `mixed_sign`'s random-feature finding. The finite-$m$ MILPs mostly recover Theorem G's counts, with one block-symmetric improvement (10 gates at $m=4$ against 12), and they miss the small-$m$ optima.

## 7. Most promising next steps

1. **Realise ternary parity-only patterns with threshold amplitudes.**
   - At $k=3$ the pattern with 2 gadgets per singleton and pair is feasible with arbitrary amplitudes (slope 10.5 against 13.5). Realisability is open (CP-SAT UNKNOWN).
   - More importantly: if $\bar n=O(1)$ gadgets per character with threshold amplitudes and linear $D$ works for all $k$, the balanced cost is about $\bar n\,n^2/16$. With $\bar n<5$ this beats $\frac5{16}n^2$ by a constant factor, **with no $Y$-range cost at all**.
   - Concrete sub-question: is every Boolean function on $k$ variables the sign of $\theta+\sum_{S\ne\emptyset}\tau_S\chi_S$ with $\tau_S\in\{-1,0,1\}$? If so, can the choice $\tau_S(x)$ be made a sum of two threshold functions of the table? True for $k\le3$ without the threshold condition. PLACEHOLDER-K4-NEXT
2. **Settle the $k=2$ periodic slope.**
   - Either prove slope $\ge3$ for all periodic constructions, including fluctuating and mixed atoms (a pointwise strengthening of Theorem 2.4), or find a counterexample.
   - The averaging lemma reduces this to showing that a fluctuating atom cannot supply the "second gadget" that Theorem 2.4 requires.
3. **For $o(n^2)$**, the analysis says exactly what is missing: heavily mixed atoms with $\gtrsim\epsilon\log n$ sign patterns per block and periods $n^{\Omega(\epsilon)}$, whose fluctuations cancel against partner atoms. Nothing in the bounded-view world can do this. The periodic LP is the right test bed: give each block $r\approx\log N$ parts and allow periods $p\approx\sqrt m$.

## 8. Files

| file | content |
|---|---|
| `report.md` | this report |
| `lpcore.py`, `exp_finite.py`, `batch_finite.sh`, `exp_k2.py` | finite-$m$ count-vector LP/MILP over gate pools (constraint generation, exact integer certificates) |
| `periodic_lp.py`, `run_periodic.py`, `run_periodic_k2.py`, `run_capped.py` | periodic (bulk) slope LP, dense version |
| `cg_periodic.py`, `cg2.py`, `run_cg2.py`, `run_cg_parity.py` | column-generation versions (vectorised pricing over all table forms) |
| `cpsat_periodic.py`, `cpsat_parity_only.py` | exact bounded-weight CP-SAT for the periodic and pure-parity models |
| `gadget_k2.py`, `parity_only_k2.py`, `lb_onegadget_k2.py`, `onegadget_any.py`, `onegadget_sym.py`, `gadget_thr.py` | gadget-configuration feasibility (monomial, arbitrary two-valued, threshold amplitudes; orbit reduction for $k=4$) |
| `build_periodic.py`, `realize.py`, `test_realize_k2.py`, `realize_k3_mono.py`, `verify_k3_big.py`, `k3_family.json` | turning atoms into explicit circuits; exact verification (count vectors and bit level) |
| **`subcube_family.py`**, `subcube_k.py` | **Theorem 3.1**: construction, gate-count formula, exact verification for $k\le4$ |
| `notes_theory.md` | working notes |
| `logs/` | all runs quoted above |
