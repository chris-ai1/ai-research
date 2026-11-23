<!-- Copyright (c) 2026 Christian Reitwiessner. All rights reserved. -->
Authors: Christian Reitwiessner

# Andreev threshold-circuit research — continuation archive

[Read the current threshold-circuit paper](workspace/eccc_draft/paper.pdf) or consult its [literature audit](workspace/eccc_draft/reviews/revision3/literature_audit.md). The [9 November update](docs/UPDATE_2026-11-09.md) records an earlier stage of the work.


This project directory preserves the research state, proofs, constructions, experiments, and paper sources needed to continue the Andreev research without the original chat or `/tmp` workspace. It is organized by mathematical content, not by timeline.

**Start with [RESEARCH_STATE.md](docs/RESEARCH_STATE.md), then [CONTINUE.md](docs/CONTINUE.md).** Archived reports contain conjectures, failed candidates, obsolete counts, and old formalization statuses; the curated summary points out important corrections. A solver timeout is never an impossibility proof.

The main open objective is an exact **subquadratic** depth-two threshold circuit for ordinary Andreev's function, with arbitrary independent table bits. The user wants clever upper-bound constructions, including SMT discoveries that generalize. Current focus: coarse Fourier information combined with genuinely mixed signs inside address blocks.

## Contents

- [`docs/RESEARCH_STATE.md`](docs/RESEARCH_STATE.md): definitions, strongest results, proof status, corrections, and open directions.
- [`docs/CONTINUE.md`](docs/CONTINUE.md): current work, precise generator-SMT specification, reproducibility, and user preferences.
- [`workspace/eccc_draft/paper.pdf`](workspace/eccc_draft/paper.pdf) and [`paper.tex`](workspace/eccc_draft/paper.tex): compact current paper, full proofs including appendices, explicit approximation construction, reviews and three checking scripts.
- [`workspace/threshold_paper/paper.pdf`](workspace/threshold_paper/paper.pdf) and [`paper.tex`](workspace/threshold_paper/paper.tex): longer earlier research paper, including the strongest general exact upper bound and improved average-case upper bounds, with corrected Lean coverage. Exploratory and finite-instance results remain in the research reports.
- [`workspace/`](workspace/): original explanatory notes, earlier PDFs, errata, and checking scripts.
- [`experiments/`](experiments/): preserved research directories, including construction code, exact witnesses, reports, reviews, and solver logs. Python caches and installed dependencies are excluded.
- [`formalization/`](formalization/): public Lean PR references, pinned commits, and a snapshot patch of the remaining open PR.
- [`tools/`](tools/): portable staging/runner and archive-integrity checker.
- [`SNAPSHOT.json`](SNAPSHOT.json), [`MANIFEST.json`](MANIFEST.json): environment/provenance and SHA-256 integrity records.

## Quick start

Run the following commands from `circuit-complexity/results/andreev/`. The manifest covers files in this topic directory. Its [pre-move version](https://github.com/chris-ai1/ai-research/blob/5fe941ddd800c5270959fc98bb5e60c1108883be/MANIFEST.json) preserves the earlier checksums.

```bash
python3 tools/verify_archive.py
python3 -m venv .venv
.venv/bin/pip install -r requirements-recorded.txt
.venv/bin/python tools/run_experiment.py --dry-run experiments/mixed_upper_sol/constructions.py
.venv/bin/python tools/run_experiment.py experiments/mixed_upper_sol/constructions.py
```

The runner stages a writable copy under `.work/` and rewrites the original machine-specific paths **in that copy**, preserving archived evidence. Some construction certificates use only the Python standard library; solver and numerical scripts need the recorded packages. A version unavailable on a fresh machine can be replaced deliberately, recording the change before interpreting numerical results.

This is a continuation snapshot, not an assertion that every archived claim is correct. Proofs, exact finite checks, heuristic evidence, and unsuccessful searches are distinguished in the reports. Preserve original contributor and source credit when extending them.

Completed 11 November Astra swarm: see RESEARCH_STATE.md section 21 and `experiments/swarm/` for restricted results, exact certificates and method barriers. No unrestricted exponent improvement.
