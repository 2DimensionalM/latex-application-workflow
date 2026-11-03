# Universal CV Baseline (`RESUME_BASELINE.md`)

## 1. Definition & Role

The **Universal CV Baseline** is the single cross-market parent resume for this workspace. It represents a curated, balanced 1-page view of the candidate's profile and serves as the shared starting point before reading a specific job description (`jd.md`), completing role pre-writing (`tailoring.md`), and producing a targeted resume.

Boundaries across the data layers:

- **`content/master/` (Single Source of Truth)**: Stores the complete, verifiable inventory of candidate experiences, stage timelines, grades, credentials, and reusable candidate bullets. Never delete facts from `content/master/` to fit a 1-page resume.
- **`baseline` (Curated 1-Page Parent View)**: A balanced 1-page resume curated from `content/master/` without single-company or single-posting bias.
- **`targets/<slug>/tailoring.md` (Role Decision Layer)**: Defines how to select, prioritize, and compress evidence from `baseline` and `content/master/` for one specific job target.
- **`targeted` (Role-Specific Deliverable)**: Carries the final JD alignment; one-off company keywords or role-specific edits are never written back into `baseline`.

## 2. Why Only One Universal Baseline Is Maintained

1. **Zero Multi-Branch Drift**: Avoids maintaining parallel `baseline-<company>` or `baseline-<industry>` files that quickly fall out of sync.
2. **Fast Surgical Forking**: Every new targeted resume forks from the same verified 1-page layout after `tailoring.md` is completed, rather than starting from scratch.
3. **Explicit One-Way Updates**: Updating `content/master/`, refreshing `baseline`, and drafting a `targeted` resume are three distinct actions that never implicitly overwrite one another.

## 3. Source & Output Paths

| Role | Path |
|---|---|
| Complete Fact Source (SoT) | `content/master/*.md` (initialized locally from `*.example.md` via `python3 scripts/workspace.py bootstrap`) |
| Baseline Section Body | `src/sections/baseline-universal.tex` |
| Baseline Build Entry | `versions/cv/baseline/resume-baseline.tex` |
| Isolated Review Output | `output/review/resume-baseline/resume-baseline.pdf` |
| Published Baseline Snapshot | `output/cv/baseline/resume-baseline.pdf` |

## 4. Building, Verifying & Refreshing the Baseline

```bash
# 1. Build in isolated review directory and run 1-page / density / log QA
./scripts/build.sh baseline

# 2. Build with the tracked placeholder header (CI / template verification)
./scripts/build.sh baseline --public-header

# 3. After visual verification, publish/refresh the universal baseline snapshot
./scripts/build.sh baseline --publish
```

### When to Refresh the Baseline

- **Refresh only when the user explicitly requests a universal baseline update.**
- Refresh procedure:
  1. Cross-check `src/sections/baseline-universal.tex` against the latest verified facts and timeline states in `content/master/*.md`.
  2. Update `src/sections/baseline-universal.tex` following `.agent/rules/content.md` (1-page limit, strict reverse-chronological order, macro-only bolding).
  3. Run `./scripts/build.sh baseline` and render PNGs with `pdftoppm` to verify 1-page density (last content line >= 80% page height, no obvious bottom whitespace).
  4. Update the refresh log at the bottom of this file.
- **No Historical Back-Writes**: Refreshing `baseline` never triggers automatic rebuilds of existing `targeted` resumes or overwrites published application snapshots.

## 5. How Every Job Target Forks from the Baseline

1. Complete job intake per `.agent/skills/job-intake/SKILL.md` (`jd.md`, `notes.md`, `metadata.yaml`).
2. Complete role pre-writing per `.agent/skills/job-prewrite/SKILL.md` (`targets/<slug>/tailoring.md`).
3. Follow `.agent/skills/targeted-resume/SKILL.md`:
   - Copy `src/sections/baseline-universal.tex` to `src/sections/targeted-<short-slug>.tex`;
   - Create entry `versions/cv/targeted/{id}-resume-<company>-<role>-<location>.tex`;
   - Register `resume_version` in `targets/<slug>/metadata.yaml`;
   - Tailor `Profile`, `Skills`, `Experience` bullets, and `Education` notes per `tailoring.md`.

## 6. Cover Letters

Cover letters must articulate specific motivation and a concrete first-weeks execution plan for the target company and role (see the 5-paragraph standard in `.agent/rules/content.md`). Therefore, **there is no universal cover letter baseline**. Each cover letter is drafted per role under `src/sections/letters/targeted-<short-slug>-letter.tex` and `versions/letter/targeted/{id}-cover-letter-<short-slug>.tex`.

## 7. Current Baseline Refresh Log

- **Last refreshed:** YYYY-MM-DD (Update when configuring your personal baseline after forking)
- **Included context:** Summarize the core experience stages, coursework/projects, and skill categories included in `baseline-universal.tex`.
- **Boundary notes:** Record items intentionally excluded from the 1-page baseline or marked `Need verification` in `content/master/`.
