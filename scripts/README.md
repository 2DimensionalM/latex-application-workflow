# Scripts & Automation Harness (`scripts/`)

This directory contains the validation, target initialization, isolated build, automated PDF/log QA, and privacy gate scripts for `latex-application-workflow`.

---

## 1. Environment Setup & First-Time Onboarding

Requires Python 3.10+ and TeX Live or TinyTeX (`pdflatex`). Installing `poppler` (`pdftoppm`) is recommended for visual PNG inspection.

```bash
# 1. Create a virtual environment and install dependencies
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt

# 2. Bootstrap local untracked files (from *.example.md and header.private.tex.example, without overwriting existing files)
.venv/bin/python scripts/workspace.py bootstrap

# 3. Run static consistency checks and the unit test suite
.venv/bin/python scripts/workspace.py check
.venv/bin/python -m unittest discover -s scripts/tests -v
```

---

## 2. Core CLI Reference

### 2.1 Initialize a New Job Target (Stage 1 — Intake)

```bash
# Preview the allocated internal_id, metadata.yaml, and PROJECT_STATUS.md row (no disk writes)
.venv/bin/python scripts/workspace.py init \
  --url 'https://example.com/jobs/12345' \
  --slug example-corp-data-scientist-amsterdam \
  --company 'Example Corp' \
  --role 'Data Scientist Intern' \
  --location 'Amsterdam, Netherlands'

# Add --write to create targets/<slug>/ and insert the row into PROJECT_STATUS.md
.venv/bin/python scripts/workspace.py init \
  --url 'https://example.com/jobs/12345' \
  --slug example-corp-data-scientist-amsterdam \
  --company 'Example Corp' \
  --role 'Data Scientist Intern' \
  --location 'Amsterdam, Netherlands' \
  --write
```

### 2.2 List Registered Build Targets

```bash
./scripts/build.sh --list
# or
.venv/bin/python scripts/workspace.py list
```

### 2.3 Isolated Target Build & Automated QA (Stage 3 & Stage 4)

```bash
# Build the single Universal CV Baseline
./scripts/build.sh baseline

# Build with the tracked placeholder header (CI / template testing)
./scripts/build.sh baseline --public-header
./scripts/build.sh letter-placeholder --public-header

# Build a targeted resume or cover letter by 3-digit ID or slug
./scripts/build.sh resume:001
./scripts/build.sh letter:001
```

By default, builds write to `output/review/<JOBNAME>/` (`<JOBNAME>.pdf`, `build.log`, `latex.log`, `qa.json`) and **never overwrite** published application snapshots.

### 2.4 Standalone PDF & Log QA

```bash
.venv/bin/python scripts/workspace.py qa \
  output/review/resume-baseline/resume-baseline.pdf \
  --kind resume \
  --log output/review/resume-baseline/latex.log
```

- **Resume QA**: Enforces `1 page` and emits a review warning if the last content line ends above `80%` of page height (indicating potential bottom whitespace).
- **Cover Letter QA**: Enforces `1 page` and measures the body between `Dear ...` and `Sincerely,` / `Kind regards,` / `Best regards,`, requiring `body_end_fraction >= 0.60` (hard error if `< 0.60`).

### 2.5 Publish Immutable Snapshots (Stage 5 — Publish)

```bash
./scripts/build.sh resume:001 --publish
./scripts/build.sh letter:001 --publish
```

- Requires a clean QA report (`errors == []`) and cannot be used with `--public-header`.
- Publishes targeted resumes to `output/cv/targeted/` and targeted cover letters to `output/cover-letters/pdf/targeted/`.
- **Overwrite Protection**: Refuses to overwrite any existing targeted PDF snapshot. Only `baseline` supports atomic replacement via `./scripts/build.sh baseline --publish`.

### 2.6 Dependency-Aware Incremental Builds (`affected`)

```bash
# List targets affected by modifying a shared file
.venv/bin/python scripts/workspace.py affected src/macros.tex

# Build all affected targets in isolated review directories
.venv/bin/python scripts/workspace.py affected src/sections/baseline-universal.tex --build --public-header
```

### 2.7 Pre-Commit Privacy & Secret Gate

```bash
.venv/bin/python scripts/privacy_check.py
```

Blocks any tracked or staged private master files (`content/master/*.md`), private headers (`src/sections/header.private.tex`), real job target directories (`targets/<slug>/`), local sub-workspaces (`cn-campus-2027/`), PDF/binary artifacts, and plain-text emails, phone numbers, GitHub tokens, or private keys.
