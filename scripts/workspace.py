#!/usr/bin/env python3
"""Validate and build the privacy-safe LaTeX skeleton."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent


def registry() -> dict[str, dict]:
    manifest = json.loads((ROOT / "scripts/build-targets.json").read_text())
    if manifest.get("schema_version") != 1:
        raise ValueError("unsupported manifest schema")
    result = {}
    for item in manifest.get("targets", []):
        alias = item.get("alias", "")
        entry = item.get("entry", "")
        kind = item.get("kind", "")
        if not re.fullmatch(r"[a-z0-9-]+", alias) or alias in result:
            raise ValueError(f"invalid or duplicate alias: {alias!r}")
        if kind not in {"resume", "letter"}:
            raise ValueError(f"invalid kind for {alias}")
        path = ROOT / entry
        if Path(entry).is_absolute() or ".." in Path(entry).parts:
            raise ValueError(f"unsafe entry path: {entry}")
        if not path.is_file() or path.suffix != ".tex":
            raise ValueError(f"missing LaTeX entry: {entry}")
        result[alias] = {"entry": entry, "kind": kind, "jobname": path.stem}
    return result


def check() -> int:
    errors = []
    try:
        records = registry()
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        errors.append(str(exc))
        records = {}
    for name in ("metadata.yaml", "jd.md", "notes.md", "tailoring.md"):
        if not (ROOT / "targets/example-company-role" / name).is_file():
            errors.append(f"missing example target file: {name}")
    print(f"{len(records)} build targets; {len(errors)} errors")
    for error in errors:
        print(f"ERROR: {error}")
    return bool(errors)


def build(alias: str) -> int:
    records = registry()
    if alias not in records:
        raise ValueError(f"unknown target: {alias}; choose from {', '.join(records)}")
    item = records[alias]
    review = ROOT / "output/review" / item["jobname"]
    review.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="latex-application-") as temp:
        aux = Path(temp)
        entry = ROOT / item["entry"]
        env = dict(__import__("os").environ)
        env["TEXINPUTS"] = str(ROOT / "src") + ":" + env.get("TEXINPUTS", "")
        run = subprocess.run(
            ["pdflatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error",
             f"-output-directory={aux}", f"-jobname={item['jobname']}", entry.name],
            cwd=entry.parent, env=env, capture_output=True, text=True,
        )
        (review / "build.log").write_text(run.stdout + run.stderr)
        if run.returncode:
            print(f"build failed; inspect {review / 'build.log'}", file=sys.stderr)
            return 1
        shutil.copy2(aux / f"{item['jobname']}.pdf", review / f"{item['jobname']}.pdf")
        print(review / f"{item['jobname']}.pdf")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check")
    build_parser = sub.add_parser("build")
    build_parser.add_argument("target")
    args = parser.parse_args()
    try:
        return check() if args.command == "check" else build(args.target)
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
