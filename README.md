# LaTeX Application Workflow

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A **privacy-first, agent-agnostic (`.agent/` + `AGENTS.md` + `CLAUDE.md`), harness-driven** LaTeX workflow for engineering targeted English resumes (CVs) and cover letters.

This repository decouples **candidate master facts (`content/master/`)**, **a single cross-market Universal CV Baseline (`baseline-universal.tex`)**, **role-specific pre-writing plans (`targets/<slug>/tailoring.md`)**, and **isolated LaTeX compilation with automated PDF layout QA (`scripts/workspace.py`)**. Every phase—from job URL intake to snapshot publishing and status tracking—is codified into standardized, portable Agent Skills under `.agent/skills/` and domain rules under `.agent/rules/`, ready to fork and extend across Claude Code, Codex, Cursor, OpenCode, or any other coding agent.

---

## 1. Quick Start (3 Steps After Forking)

### Prerequisites
- Python 3.10+
- TeX Live or TinyTeX (`pdflatex`)
- Poppler (recommended; provides `pdftoppm` for visual PNG inspection)

### Onboarding Commands

```bash
# 1. Create a virtual environment and install validation/QA dependencies (PyYAML, pdfplumber)
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt

# 2. Bootstrap local untracked files (creates content/master/*.md and src/sections/header.private.tex from .example templates)
.venv/bin/python scripts/workspace.py bootstrap

# 3. Validate workspace invariants and compile the Universal CV Baseline & 5-paragraph cover letter template
.venv/bin/python scripts/workspace.py check
./scripts/build.sh baseline
./scripts/build.sh letter-placeholder
```

- Builds output to isolated review directories under `output/review/<JOBNAME>/` (`<JOBNAME>.pdf`, `build.log`, `latex.log`, and `qa.json`).
- Edit `src/sections/header.private.tex` with your real name and contact details (gitignored and strictly off-limits to agents).
- Edit `content/master/*.md` with your verified education, experience, projects, skills, and credentials (also gitignored and never uploaded).

---

## 2. Six-Stage Agentic Workflow & Standardized Skills (`.agent/skills/`)

The workflow is organized into **6 standardized stage skills** under `.agent/skills/`, routed on demand via `AGENTS.md`, `CLAUDE.md`, and `.cursor/rules/project-memory.mdc`:

```
[Stage 0: Master & Baseline Maintenance]  (.agent/skills/master-and-baseline/SKILL.md)
   content/master/*.md (Single Source of Truth) --(explicit refresh)--> src/sections/baseline-universal.tex (Single 1-Page Parent)
          |
          v
[Stage 1: Job URL & JD Intake]            (.agent/skills/job-intake/SKILL.md)
   `workspace.py init` allocates 3-digit ID (001..999) --> scaffolds targets/<slug>/{metadata.yaml, jd.md, notes.md, tailoring.md}
   and inserts a new row into PROJECT_STATUS.md (Status = Pending Pre-write)
          |
          v
[Stage 2: Role Pre-writing & Mapping]     (.agent/skills/job-prewrite/SKILL.md)
   Cross-maps jd.md + notes.md + content/master/ --> populates all 6 mandatory sections of targets/<slug>/tailoring.md
   (Never skip pre-writing to edit LaTeX directly)
          |
          +---------------------------------------------------+
          v                                                   v
[Stage 3: Targeted Resume & QA]                             [Stage 4: Targeted Cover Letter & QA]
(.agent/skills/targeted-resume/SKILL.md)                    (.agent/skills/targeted-cover-letter/SKILL.md)
 - Fork from baseline-universal.tex                          - Draft 5-paragraph letter from tailoring.md plan
 - Enforce strict reverse-chronological Experience order     - No prose recap of resume; mandatory Paragraph 4 execution plan
 - `./scripts/build.sh resume:<id>`                          - `./scripts/build.sh letter:<id>`
 - Enforce 1 page + >=80% height (bottom-whitespace loop)    - Enforce 1 page + >=60% body height (`Dear` to `Sincerely,`)
          |                                                   |
          +-------------------------+-------------------------+
                                    v
[Stage 5: Publish Snapshots & Sync Status] (.agent/skills/status-and-publish/SKILL.md)
   `./scripts/build.sh <target> --publish` writes immutable PDFs --> updates PROJECT_STATUS.md links, 3-tier row group order & history
```

| Stage | Skill Path | Typical Trigger | Core Deliverable & Quality Gate |
|---|---|---|---|
| **0. Master & Baseline** | [`.agent/skills/master-and-baseline/SKILL.md`](.agent/skills/master-and-baseline/SKILL.md) | Onboarding repo, adding new experience/grades to master, refreshing universal baseline | Updated `content/master/*.md` or `baseline-universal.tex` |
| **1. Job Intake** | [`.agent/skills/job-intake/SKILL.md`](.agent/skills/job-intake/SKILL.md) | Adding one or more job posting URLs or JDs into the project | Allocated `internal_id`, structured English `jd.md` & `notes.md`, synced `PROJECT_STATUS.md` |
| **2. Role Pre-writing** | [`.agent/skills/job-prewrite/SKILL.md`](.agent/skills/job-prewrite/SKILL.md) | Pre-writing `tailoring.md` and mapping evidence for a target role | Completed 6-section `targets/<slug>/tailoring.md` |
| **3. Targeted Resume** | [`.agent/skills/targeted-resume/SKILL.md`](.agent/skills/targeted-resume/SKILL.md) | Drafting, compressing, or backfilling a targeted resume for a role | `{id}-resume-....tex` passing 1-page + >=80% density visual QA |
| **4. Targeted Cover Letter** | [`.agent/skills/targeted-cover-letter/SKILL.md`](.agent/skills/targeted-cover-letter/SKILL.md) | Drafting or revising a role-specific cover letter | `{id}-cover-letter-....tex` with 5 paragraphs passing >=60% body-height QA |
| **5. Publish & Status** | [`.agent/skills/status-and-publish/SKILL.md`](.agent/skills/status-and-publish/SKILL.md) | Publishing final PDFs or recording applied/interview/rejected/closed events | Immutable PDFs via `--publish`, updated `PROJECT_STATUS.md` group order & dated history |

---

## 3. Agent-Agnostic Context Architecture (`.agent/` + `AGENTS.md` + `CLAUDE.md`)

All long-term memory, domain rules, and workflow skills are written in standard Markdown under **`.agent/`**, avoiding lock-in to any single editor's rule format:

| Path | Purpose |
|---|---|
| [`AGENTS.md`](AGENTS.md) | Universal root entry point: safety guardrails, Git policy, and the 6-stage routing table |
| [`CLAUDE.md`](CLAUDE.md) | Claude Code entry router pointing to `AGENTS.md` and `.agent/` |
| [`.cursor/rules/project-memory.mdc`](.cursor/rules/project-memory.mdc) | Thin 10-line Cursor router pointing to `AGENTS.md` and `.agent/` |
| [`.agent/README.md`](.agent/README.md) | Overview of the `.agent/` Context Architecture hub |
| [`.agent/rules/general.md`](.agent/rules/general.md) | Core engineering principles, 4-tier information ownership, and long-term memory update policy |
| [`.agent/rules/intake.md`](.agent/rules/intake.md) | Job URL intake, ATS extraction patterns, open/closed verification, and non-English JD translation rules |
| [`.agent/rules/tailoring.md`](.agent/rules/tailoring.md) | The 6-step customization sequence and mandatory 6-section `tailoring.md` specification |
| [`.agent/rules/content.md`](.agent/rules/content.md) | Master fact dimensions, 1-page resume compression & bottom-whitespace backfill loop, and 5-paragraph cover letter >=60% height rules |
| [`.agent/rules/status.md`](.agent/rules/status.md) | `PROJECT_STATUS.md` 9-column schema, `metadata.yaml` status mapping, 3-tier row grouping order, and 4-column history table rules |
| [`.agent/rules/structure.md`](.agent/rules/structure.md) | LaTeX macro & 3-tier file decoupling (`src/` vs. `versions/`) |
| [`.agent/rules/build.md`](.agent/rules/build.md) | Isolated review builds, automated PDF/Log QA gates, and `--publish` snapshot overwrite protection |
| [`STRUCTURE.md`](STRUCTURE.md) | Directory layout, 5-layer data flow, and naming/ID invariants |
| [`RESUME_BASELINE.md`](RESUME_BASELINE.md) | Definition, refresh policy, and forking guide for the single Universal CV Baseline |
| [`PROJECT_STATUS.md`](PROJECT_STATUS.md) | Standardized 9-column Application Pipeline table + 4-column dated Activity History table |
| [`content/master/README.md`](content/master/README.md) | Candidate Master Fact Layer (SoT) guide and inventory of the 6 `*.example.md` templates |
| [`targets/README.md`](targets/README.md) | Target quartet contract and `metadata.yaml` schema |
| [`scripts/README.md`](scripts/README.md) | Full CLI reference for `workspace.py`, `build.sh`, `build_all.py`, and `privacy_check.py` |

---

## 4. Privacy Model (Privacy by Design)

1. **Untracked Private & Local Paths**:
   - `src/sections/header.private.tex` (real name, address, phone, email, personal profile links)
   - `content/master/*.md` (real candidate master facts; only `README.md` and `*.example.md` are tracked)
   - `targets/<slug>/` (real job target packages; only `targets/example-company-role/` is tracked)
   - `versions/cv/targeted/*.tex`, `src/sections/targeted-*.tex`, `src/sections/letters/targeted-*.tex`
   - `output/**` (all compiled PDFs and logs)
   - Local sub-workspaces (`cn-campus-2027/`, `_inbox/`, `nuffic/`)
2. **Mandatory Pre-Commit Gate**:
   Run before every `git commit` / `git push`:
   ```bash
   .venv/bin/python scripts/privacy_check.py
   .venv/bin/python scripts/workspace.py check
   .venv/bin/python -m unittest discover -s scripts/tests -v
   ```
   `privacy_check.py` inspects all tracked and staged files and fails immediately if any private path, binary/PDF artifact, email address, phone number, GitHub token, or private key is detected.

---

## 5. License

Released under the [MIT License](LICENSE).
