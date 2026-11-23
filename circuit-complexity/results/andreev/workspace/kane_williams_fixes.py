#!/usr/bin/env python3
"""Apply the erratum to your own copy of the arXiv:1511.07860 LaTeX source.

Usage: kane_williams_fixes.py INPUT.tex OUTPUT.tex

Each entry is (erratum number, old text, new text, expected occurrences).
The script stops without writing if any count differs, so it cannot apply
silently to a different version of the source.
"""
import sys

R = [
 # E1: rank must count at-least-as-heavy weights, for both k_i and k'_i.
 (1, r"define $k_i$ to be the number of $j \in [n]$ such that $|a_i| \geq |a_j|$",
     r"define $k_i$ to be the number of $j \in [n]$ such that $|a_j| \geq |a_i|$", 1),
 (1, r"define $k'_i$ to be the number of $j \in [n]-B$ such that $|a_i|\geq |a_j|$",
     r"define $k'_i$ to be the number of $j \in [n]-B$ such that $|a_j|\geq |a_i|$", 1),
 # E2: forcing to 1 is non-strict; I must then be half-open.
 (2, r"\left(L'(x) > t+\sum_{i\in B : a_i < 0}|a_i|\right)",
     r"\left(L'(x) \geq t+\sum_{i\in B : a_i < 0}|a_i|\right)", 1),
 (2, r"~t+\sum_{i\in B : a_i < 0}|a_i|\right].$$",
     r"~t+\sum_{i\in B : a_i < 0}|a_i|\right).$$", 1),
 # E3: zero weights.
 (3, r"Let $I \subset \R$ be a finite interval,",
     r"Let $I \subset \R$ be a finite interval of positive length,", 1),
 (3, r"with threshold value $t \in \R$. For a set $B\subseteq [n]$,",
     r"with threshold value $t \in \R$. Variables with $a_i=0$ do not affect $f$ and give empty intervals below, so all sums over indices in this proof range only over $i$ with $a_i\neq 0$. For a set $B\subseteq [n]$,", 1),
 # E4: the bound is 1/2, which suffices because of the O(1).
 (4, r"\geq (k_i/2)/\sqrt{k_i} \gg 1$", r"\geq (k_i/2)/\sqrt{k_i} \geq 1/2$", 1),
 # E5: wire lemma works on the LTF restricted to S.
 (5, r"Define $k_i$ for $i\in S$ as in the proof of Lemma \ref{rr-LTF}.",
     r"Regard $f$ as an LTF on the variables in $S$, and define $k_i$ for $i\in S$ as in the proof of Lemma \ref{rr-LTF}.", 1),
 (5, r"by Equation \eqref{RestrictToBEqn}. Therefore,",
     r"by Equation \eqref{RestrictToBEqn} applied to that LTF with $B\cap S$ in place of $B$. Therefore,", 1),
 (5, r"& = \sum_{i\in S}\frac{O(1)}{\sqrt{k_i}}\cdot \min\left\{",
     r"& \leq \sum_{i\in S}\frac{O(1)}{\sqrt{k_i}}\cdot \min\left\{", 1),
 (5, r"& = \sum_{i\in S}\frac{O(1)}{\sqrt{k_i}} \cdot \min\left\{",
     r"& \leq \sum_{i\in S}\frac{O(1)}{\sqrt{k_i}} \cdot \min\left\{", 1),
 # E6: range of epsilon, counting bound, and direct input wires.
 (6, r"\epsilon\gg \sqrt{\log(n)/n}", r"\epsilon\gg \log(n)/\sqrt{n}", 1),
 (6, r"\epsilon \gg \sqrt{\log(n)/n}", r"\epsilon \gg \log(n)/\sqrt{n}", 2),
 (6, r"For all $\epsilon\gg \sqrt{n/2^n}$", r"For all $\epsilon\gg n/2^{n/2}$", 1),
 (6, r"circuits of $s \geq n$ gates and $n$ inputs", r"circuits of $s \geq 1$ gates and $n$ inputs", 1),
 (6, r"By Theorem~\ref{number-ckts}, the total number of functions computed by such size-$s$ depth-$2$ circuits is at most",
     r"By Theorem~\ref{number-ckts}, applied with the $n$ inputs as additional fixed functions for the output gate, and using $n^2 \ll \epsilon^2 2^n$, the total number of functions computed by such size-$s$ depth-$2$ circuits is at most", 1),
 # E7: survivors in the Andreev proof.
 (7, r"is at most most $c'\epsilon^3", r"is at most $c'\epsilon^3", 1),
 (7, r"the expected number of bottom level gates in $C$ not forced to constants by $\rho$",
     r"the expected number of bottom level gates in $C$ not forced to constants (for the gate bound) or to functions of a single input (for the wire bound) by $\rho$", 1),
 (7, r"In this case, $C$ is equivalent to a $\THR\circ\THR$ circuit with at most",
     r"In this case, replacing single-input gates by direct wires to the output gate, $C$ is equivalent to a $\THR\circ\THR$ circuit with at most", 1),
 # E8: typographical slips in formulas.
 (8, r"Dividing everything by $1/2$", r"Dividing everything by $2$", 1),
 (8, r"$g(z_i) = 0$ and $H(z_i)=1$", r"$g(z_i) = 0$ and $h(z_i)=1$", 1),
 (8, r"$2^{o(2^n)}/2^{n} = o(1)$", r"$2^{o(2^n)}/2^{2^n} = o(1)$", 1),
]

src = open(sys.argv[1], encoding="utf-8").read()
bad = [(e, o, src.count(o), c) for e, o, _, c in R if src.count(o) != c]
if bad:
    for e, o, got, want in bad:
        print(f"E{e}: found {got}, expected {want}: {o}", file=sys.stderr)
    sys.exit("No output written: the source does not match this erratum.")
for _, old, new, _ in R:
    src = src.replace(old, new)
open(sys.argv[2], "w", encoding="utf-8").write(src)
print(f"Applied {len(R)} replacements to {sys.argv[2]}")
