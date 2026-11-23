#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Verify archived files against the committed SHA-256 manifest."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "MANIFEST.json").read_text())
errors = []
for name, expected in manifest["sha256"].items():
    path = root / name
    if not path.is_file():
        errors.append(f"Missing: {name}")
    elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        errors.append(f"Changed: {name}")
if errors:
    raise SystemExit("\n".join(errors))
print(f"Verified {len(manifest['sha256'])} archived files.")
