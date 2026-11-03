#!/usr/bin/env python3
"""Fail if staged or tracked files contain private candidate data, regional sub-workspaces, PDFs, or secrets."""
from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent

BLOCKED_EXACT = {
    "src/sections/header.private.tex",
}

BLOCKED_PREFIXES = (
    "cn-campus-2027/",
    "_inbox/",
    "nuffic/",
    "content/tailored/",
    "src/sections/targeted-",
    "src/sections/letters/targeted-",
    "versions/cv/targeted/",
)

ALLOWED_MASTER_FILES = {
    "content/master/README.md",
}

ALLOWED_TARGET_PREFIXES = (
    "targets/README.md",
    "targets/example-company-role/",
)

SECRET_PATTERNS = {
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "phone number": re.compile(r"(?<!\d)(?:\+?\d[\s().-]*){9,}(?!\d)"),
    "GitHub token": re.compile(
        r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"
    ),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def tracked_and_staged_files(root: Path = ROOT) -> list[str]:
    tracked = subprocess.run(
        ["git", "ls-files", "-z"], cwd=root, check=True, capture_output=True
    ).stdout.split(b"\0")
    staged = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    ).stdout.split(b"\0")
    files = {part.decode("utf-8") for part in tracked + staged if part}
    return sorted(files)


def is_blocked_path(relative: str) -> str | None:
    if relative in BLOCKED_EXACT:
        return f"blocked private file: {relative}"
    if relative.startswith("output/") and relative != "output/.gitkeep":
        return f"blocked output artifact: {relative}"
    if relative.endswith(".pdf"):
        return f"blocked PDF artifact: {relative}"
    if any(
        relative == prefix.rstrip("/") or relative.startswith(prefix)
        for prefix in BLOCKED_PREFIXES
    ):
        if relative != "versions/cv/targeted/.gitkeep":
            return f"blocked private/regional path: {relative}"
    if relative.startswith("versions/letter/targeted/") and relative not in {
        "versions/letter/targeted/cover-letter-placeholder.tex",
        "versions/letter/targeted/.gitkeep",
    }:
        return f"blocked targeted letter path: {relative}"
    if relative.startswith("content/master/"):
        if (
            relative not in ALLOWED_MASTER_FILES
            and not relative.endswith(".example.md")
        ):
            return f"blocked private master fact file: {relative}"
    if relative.startswith("targets/"):
        if not any(
            relative == allowed.rstrip("/") or relative.startswith(allowed)
            for allowed in ALLOWED_TARGET_PREFIXES
        ):
            return f"blocked real job target package: {relative}"
    return None


def check_repo(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for relative in tracked_and_staged_files(root):
        reason = is_blocked_path(relative)
        if reason:
            errors.append(reason)
            continue
        path = root / relative
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
    return errors


def main() -> int:
    errors = check_repo(ROOT)
    if errors:
        print("Privacy check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Privacy check passed: {len(tracked_and_staged_files(ROOT))} tracked/staged text files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
