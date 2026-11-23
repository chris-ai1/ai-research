# LogCFL is unambiguous: Hoza's isolation for proof trees

[Read the paper (PDF)](paper.pdf) · [LaTeX source](paper.tex) · [Exhaustive checks](check.py) ([output](check-output.txt))

Hoza ([ECCC TR26-323](https://eccc.weizmann.ac.il/report/2026/323/)) proved NL = UL with a logspace weight generator that uses an O(log n)-bit seed and isolates minimum-weight paths in layered digraphs. This note shows that the same weights isolate minimum-weight **proof trees** in layered semi-unbounded circuits of logarithmic depth, once the 2-adic valuation of the layer is replaced by the AND-level of the gate. With van Melkebeek and Prakriya's unambiguous certificate machines, this gives

**LogCFL = UAuxPDA(log n, poly) = coUAuxPDA(log n, poly)**.

Before this, the result was known in space O(log^{3/2} n) (van Melkebeek–Prakriya) or with polynomial advice (Reinhardt–Allender).

| Pages | Question |
| --- | --- |
| 1 | What is claimed, and how does it relate to NL = UL? |
| 2 | Which circuits, and what is a proof tree? Why must the layer next to the leaves be AND? |
| 3–4 | Why do Hoza's derivative and collision arguments carry over to trees? |
| 4–5 | How does the seed search give an unambiguous AuxPDA? |
| 5 | Consequences, novelty and how the proof was checked |

**Status.** The note was written with AI assistance at the request of Christian Reitwiessner. The proof was produced by one AI agent and checked step by step by a second, independent AI review. That review found two fixes, both incorporated: the AND-first-layer condition, and "at most 2^m" in place of "exactly 2^m". No human expert has reviewed it. `check.py` enumerates every seed on small adversarial circuits. It finds no violation of the derivative and collision lemmas for base 6. It finds violations of the derivative bound for bases 2–5, and it shows that isolation fails for every seed when the layer next to the leaves is OR.

A formalization in Lean is proposed in [cslib-frontier#7920](https://github.com/cslib-community/cslib-frontier/issues/7920). It extends the formalized `NL_eq_UL`.

To rebuild the PDF, run `tectonic paper.tex` in this directory. To rerun the checks, run `python3 check.py`. It needs only the Python standard library and takes about a minute.
