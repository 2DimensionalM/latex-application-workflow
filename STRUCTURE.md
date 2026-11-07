# Workspace Structure, Data Flow & Naming Boundaries (`STRUCTURE.md`)

This document defines the repository's Context Architecture and directory boundaries. For the live application table, see `PROJECT_STATUS.md`; to list registered build targets, run `python3 scripts/workspace.py list`.

## 1. Five-Layer Data Flow (Context -> Master -> Baseline -> Tailoring -> Snapshot)

```
[External Input: Candidate Evidence / Job Posting URL / JD]
       |
       v
1. content/master/*.md          <- Single Source of Truth (SoT): complete experiences, stage boundaries, grades, Need verification items, reusable candidate bullets (facts only, no editorial omit rules)
       | (Curated only upon explicit user request)
       v
2. src/sections/baseline-universal.tex
   + versions/cv/baseline/resume-baseline.tex  <- Single cross-market 1-page Universal CV Baseline (shared parent for all targeted forks)
       |
       +--- Job Intake (job-intake)  --> targets/<slug>/{metadata.yaml, jd.md, notes.md, tailoring.md} + PROJECT_STATUS.md
       |
       v
3. targets/<slug>/tailoring.md  <- Role Pre-writing Decision Layer (job-prewrite): JD mapping, section trade-offs, experience bullet shortlist, 5-paragraph cover letter plan
       |
       v
4. Targeted LaTeX Sources (targeted-resume / targeted-cover-letter)
   - Resume body:   src/sections/targeted-<short-slug>.tex
   - Resume entry:  versions/cv/targeted/{id}-resume-<company>-<role>-<location>.tex
   - Letter body:   src/sections/letters/targeted-<short-slug>-letter.tex
   - Letter entry:  versions/letter/targeted/{id}-cover-letter-<short-slug>.tex
       |
       +--- Isolated Build & Visual QA (`./scripts/build.sh`) --> output/review/<JOBNAME>/{<JOBNAME>.pdf, qa.json, latex.log}
       |
       v
5. Published Immutable Snapshots (`--publish` + status-and-publish)
   - output/cv/targeted/{id}-resume-<company>-<role>-<location>.pdf
   - output/cover-letters/pdf/targeted/{id}-cover-letter-<short-slug>.pdf
   (Once submitted, historical snapshots are preserved and never overwritten by subsequent master or baseline updates)
```

## 2. Directory & File Responsibilities

| Path | Responsibility & Version-Control Boundary |
|---|---|
| `AGENTS.md` | Safety boundaries and the one file to read for the current task |
| `CLAUDE.md` | Claude Code router to `AGENTS.md` and the application pipeline skill |
| `.cursor/rules/project-memory.mdc` | Cursor router to `AGENTS.md` and the application pipeline skill |
| `.agent/README.md` | Index of skills; not part of resume or letter production |
| `.agent/skills/application-pipeline/SKILL.md` | Job URL through resume and cover letter |
| `.agent/skills/<stage>/SKILL.md` | One stage when the user asked for that stage only |
| `.agent/rules/<topic>.md` | Reference for harness or rule changes (`general.md`, `intake.md`, `tailoring.md`, `content.md`, `status.md`, `structure.md`, `build.md`) |
| `content/master/` | Candidate Master Fact Layer (SoT). Only `README.md` and `*.example.md` templates are tracked; real local `*.md` files are gitignored |
| `RESUME_BASELINE.md` | Definition, refresh policy, and forking rules for the single Universal CV Baseline |
| `targets/<slug>/` | One quartet per job role (`metadata.yaml`, `jd.md`, `notes.md`, `tailoring.md`). Only `targets/example-company-role/` is tracked |
| `PROJECT_STATUS.md` | Human-editable 9-column Application Pipeline table + 4-column dated Activity History table |
| `src/preamble*.tex`, `src/macros*.tex` | Shared resume and cover letter typography and layout macros (`\cvexpblock`, `\cveduhead`, `\cvskillblock`, `\LetterSubject`) |
| `src/sections/header.tex` | Header router: automatically loads `header.private.tex` if present locally, or falls back to `header.template.tex` |
| `src/sections/header.private.tex` | Local real name and contact details (gitignored; strictly off-limits to agents) |
| `src/sections/baseline-universal.tex` | Universal 1-page CV baseline section body |
| `src/sections/targeted-*.tex` | Role-specific targeted resume section fragments (gitignored) |
| `src/sections/letters/` | Cover letter section fragments (includes tracked placeholder and gitignored `targeted-*-letter.tex`) |
| `versions/cv/{base,baseline,targeted}/` | Resume LaTeX build entry points (`JOBNAME` is automatically derived from entry stem) |
| `versions/letter/{baseline,targeted}/` | Cover letter LaTeX build entry points |
| `output/review/<JOBNAME>/` | Default isolated build outputs (PDF, `build.log`, `latex.log`, `qa.json`); never overwrites published snapshots |
| `output/cv/`, `output/cover-letters/pdf/` | Published application PDF snapshots created via `--publish` |
| `scripts/workspace.py` | Core harness supporting `bootstrap`, `init`, `check`, `list`, `build`, `qa`, and `affected` |
| `scripts/build.sh`, `scripts/build_all.py` | Single-target build wrapper and batch isolated build orchestrator |
| `scripts/privacy_check.py` | Pre-commit privacy gate blocking private paths, binary PDFs, emails, phone numbers, and secrets |
| `scripts/tests/test_workspace.py` | Offline unit test suite using disposable temporary fixtures |
| `LICENSE` | MIT open-source license |

## 3. Naming & ID Invariants

1. **Target Package Directory**: `targets/<company-role-location>/`, lowercase ASCII letters, digits, and hyphens.
2. **Internal ID (`internal_id`)**: 3-digit zero-padded string `"001"`–`"999"`, allocated sequentially (`max + 1`) as targets enter the workspace. **Globally unique, monotonically increasing, never recycled.** `"000"` is reserved for the `example-company-role` template.
3. **Targeted Resume Entry & PDF Name**: `versions/cv/targeted/{id}-resume-<company>-<role>-<location>.tex` -> `output/cv/targeted/{id}-resume-<company>-<role>-<location>.pdf`.
4. **Targeted Cover Letter Entry & PDF Name**: `versions/letter/targeted/{id}-cover-letter-<short-slug>.tex` -> `output/cover-letters/pdf/targeted/{id}-cover-letter-<short-slug>.pdf`.
5. **Automatic Build Registration**: Setting a valid `resume_version` or `cover_letter_version` path in `targets/<slug>/metadata.yaml` automatically registers `resume:<id>`, `resume:<slug>`, `letter:<id>`, `letter:<slug>`, and `<JOBNAME>` in `workspace.py` without editing `scripts/build.sh` or `scripts/build-targets.json`.
