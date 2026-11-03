#!/usr/bin/env python3
"""Build all registered targets once per unique entry in isolated review directories."""
from __future__ import annotations

import argparse
import sys
from workspace import ROOT, build, registry


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true")
    group = p.add_mutually_exclusive_group()
    group.add_argument("--resumes-only", action="store_true")
    group.add_argument("--letters-only", action="store_true")
    p.add_argument("--public-header", action="store_true")
    args = p.parse_args()
    try:
        records, _ = registry(ROOT)
        records = [
            r
            for r in records
            if not (args.resumes_only and r["kind"] == "letter")
            and not (args.letters_only and r["kind"] == "resume")
        ]
        for r in records:
            print(f'{r["kind"]}\t{r["aliases"][0]}', flush=True)
            if not args.dry_run and build(ROOT, r, args.public_header):
                return 1
        print(f"# total: {len(records)}")
        return 0
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
