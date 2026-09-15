#!/usr/bin/env python3
"""Fail if staged or tracked files contain private artifacts or obvious secrets."""
from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
BLOCKED_PATHS = (
    "content/master/",
    "src/sections/header.private.tex",
)
SECRET_PATTERNS = {
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "phone number": re.compile(r"(?<!\d)(?:\+?\d[\s().-]*){9,}(?!\d)"),
    "GitHub token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def tracked_files() -> list[str]:
    run = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True)
    return [part.decode() for part in run.stdout.split(b"\0") if part]


def main() -> int:
    errors = []
    for relative in tracked_files():
        if relative.startswith("output/") and relative != "output/.gitkeep":
            errors.append(f"blocked tracked path: {relative}")
            continue
        if any(relative == prefix.rstrip("/") or relative.startswith(prefix) for prefix in BLOCKED_PATHS):
            errors.append(f"blocked tracked path: {relative}")
            continue
        path = ROOT / relative
        if not path.is_file() or path.is_symlink():
            continue
        data = path.read_bytes()
        if b"\0" in data:
            errors.append(f"binary file is not allowed in skeleton: {relative}")
            continue
        text = data.decode("utf-8", errors="replace")
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"possible {label}: {relative}")
    if errors:
        print("Privacy check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Privacy check passed: {len(tracked_files())} tracked text files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
