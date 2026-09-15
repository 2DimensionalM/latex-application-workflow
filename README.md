# LaTeX Application Workflow

A privacy-first skeleton for maintaining LaTeX resumes, cover letters, job-target metadata, and local QA automation.

This repository contains only generic placeholders. It intentionally excludes candidate history, real application records, job descriptions, contact details, generated PDFs, and private master data.

## Quick start

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/workspace.py check
./scripts/build.sh resume-base
```

Builds go to `output/review/`, which is ignored by Git. Replace placeholders only in untracked private files or in a separate private data layer.

## Layout

| Path | Purpose |
|---|---|
| `AGENTS.md` | Short safety boundary and task router |
| `docs/rules/` | Workflow details loaded only when relevant |
| `targets/` | One metadata package per role; only the empty example is committed |
| `versions/` | LaTeX entry points |
| `src/` | Shared layout and placeholder sections |
| `scripts/` | Registry, validation, build, and QA commands |
| `PROJECT_STATUS.md` | Empty human-editable tracking table |

## Privacy model

- `src/sections/header.private.tex`, `content/master/`, real `targets/*`, and all PDFs are ignored.
- The committed header contains placeholders only.
- Builds use `-no-shell-escape` and write to an ignored review directory.
- Before every push, run `scripts/privacy_check.py`.

