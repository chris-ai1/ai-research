#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Stage archived experiments, translate legacy paths, and run a Python script."""
import argparse
import json
from pathlib import Path
import re
import shutil
import site
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--dry-run", action="store_true")
parser.add_argument("script", help="Repository-relative Python script under experiments/ or workspace/")
parser.add_argument("args", nargs=argparse.REMAINDER)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
source = (root / args.script).resolve()
try:
    relative = source.relative_to(root)
except ValueError:
    parser.error("Script must be inside this repository")
if relative.parts[0] not in {"experiments", "workspace"} or source.suffix != ".py" or not source.is_file():
    parser.error("Choose an existing Python script under experiments/ or workspace/")
stage = root / ".work" / "staged"
target = stage / relative
command = [sys.executable, str(target), *args.args]
if args.dry_run:
    print("Will refresh a staged copy in", stage)
    print("Command:", repr(command))
    raise SystemExit(0)
snapshot = json.loads((root / "SNAPSHOT.json").read_text())
packages = site.getsitepackages()[0]
replacements = {
    snapshot["original_experiments"]: str(stage / "experiments"),
    snapshot["original_workspace"]: str(stage / "workspace"),
    "/tmp/andreev-pdf-tools/python": packages,
    "/tmp/pydeps": packages,
}
legacy_paths = re.compile("|".join(re.escape(old) for old in replacements))
for directory in ("experiments", "workspace"):
    destination = stage / directory
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(root / directory, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
for path in stage.rglob("*"):
    if path.suffix not in {".py", ".sh"} or not path.is_file():
        continue
    original = path.read_text()
    rewritten = legacy_paths.sub(lambda match: replacements[match.group()], original)
    if rewritten != original:
        path.write_text(rewritten)
print("Running staged copy:", target, flush=True)
raise SystemExit(subprocess.call(command, cwd=target.parent))
