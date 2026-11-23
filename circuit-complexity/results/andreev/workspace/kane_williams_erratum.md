# Erratum for Kane–Williams, arXiv:1511.07860

This covers *Super-Linear Gate and Super-Quadratic Wire Lower Bounds for Depth-Two and Depth-Three Threshold Circuits*. Line numbers refer to `thr-thr-arxiv.tex` in the arXiv source. `kane_williams_fixes.py` applies every change below to your own copy of that file.

**Summary.** The main theorems survive. Only E6 changes a stated result: the range of $\varepsilon$ in the Andreev lower bound shrinks. E1–E5 and E7–E8 repair proofs or typos without changing any statement.

**Scope.** Checked: Sections 2 and 3, the PARITY section, the Andreev lower bound, and the Andreev upper-bound sketches. Not audited: the $B_n$ and $\mathrm{MAJ}\circ\mathrm{THR}\circ\mathrm{THR}$ material (line 400 onward), so errors may remain there.

## Proof repairs

**E1. Reversed rank definition (lines 274, 282; Lemma `rr-LTF`).** $k_i$ and $k'_i$ are defined by counting $j$ with $|a_i|\ge|a_j|$, that is, the lighter weights. Littlewood–Offord needs many weights at least as large as the interval, and the paper's next display also assumes larger $k_i$ means smaller $|a_i|$. Both must count $j$ with $|a_j|\ge|a_i|$.

**E2. Forcing condition (lines 268, 270).** With $f=[L\ge t]$, the restriction forces 1 exactly when $L'(x)\ge t+\sum_{i\in B,\,a_i<0}|a_i|$, not when it is strictly greater. So "not forced" means $L'(x)$ lies in the half-open interval $[\,t-\sum_{a_i>0}|a_i|,\ t+\sum_{a_i<0}|a_i|)$.

**E3. Zero weights (lines 165, 266).** The Littlewood–Offord form in Lemma `LOLem` is false for an interval of length 0: all-zero weights put probability 1 on a point. Require positive length and drop indices with $a_i=0$. They do not affect $f$, and with E2 they contribute empty intervals. If every free variable has weight 0, the interval is empty and $f$ is forced, as it should be.

**E4. Overstated estimate (line 286).** The first case gives $(k_i/2)/\sqrt{k_i}\ge1/2$, not $\gg1$. The argument still works, because the claimed bound has an unspecified constant.

**E5. Wire lemma (lines 314, 316, 319, 320; Lemma `wire-rr-Lem`).** The proof bounds the survival probability by a sum over $B\cap S$, but the cited equation sums over $B$. View $f$ as an LTF on the variables in $S$ and apply the equation with $B\cap S$ in place of $B$. Two displayed equalities are also only inequalities: $\Pr[i\in B,\ |B\cap S|\ge2]$ is at most the stated minimum.

**E7. Survivor counting in the Andreev proof (lines 353, 355).** The proof says "not forced to constants", but for the wire bound it means not forced to a constant or a single input. It then calls the restricted circuit one with few gates, but single-input gates remain. They become direct wires to the output gate, which the paper's model allows (line 86). Counting these needs the corrected Corollary in E6. Line 353 also has the typo "at most most".

**E8. Typos.**

- Line 173: "Dividing everything by $1/2$" should be by 2.
- Line 210: $H(z_i)$ should be $h(z_i)$.
- Line 226: the denominator $2^{n}$ should be $2^{2^n}$.

## Change to a stated result

**E6. Range of $\varepsilon$ (lines 68, 104, 192, 230, 233, 347).** Corollary `hardFunctionCor` claims the range $\varepsilon\gg\sqrt{n/2^n}$, but its proof needs fewer than $2^{o(\varepsilon^22^n)}$ candidate functions. Even with no bottom gates, the output gate can be any of the $2^{\Theta(n^2)}$ LTFs on the inputs, so the union bound requires $\varepsilon^22^n\gg n^2$.

The corrected statements are:

- Corollary `hardFunctionCor`: $\varepsilon\gg n/2^{n/2}$.
- Theorem `andreev-lb`, also in the abstract: $\varepsilon\gg\log(n)/\sqrt n$, in place of $\sqrt{\log(n)/n}$.
- Theorem `number-ckts`: the count $2^{O(n^2s)}$ holds for all $s\ge1$, so the hypothesis $s\ge n$ is unnecessary. With $n$ extra direct input wires, the count is $2^{O(n^2(s+1))}$.

**What this costs.** Nothing for gates: in the dropped range the stated gate bound is below one gate. The stated wire bound there, roughly $n/\log^2n$ up to $n/\sqrt{\log n}$, is no longer claimed.

This is a gap in the proof, not a disproof. A sharper bound on correlation with LTFs, for instance via VC-dimension chaining, might recover the original range, but I have not worked that out.

## Not included

The improvements in `andreev_depth_two_bounds.md` ($\varepsilon^3\to\varepsilon^2$ in the lower bounds, and the $O(n^2)$ upper bound) are new results, not corrections, so the script doesn't apply them. The paper's $O(n^3/\log n)$ upper bound is correct as stated.
