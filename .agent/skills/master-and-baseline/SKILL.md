---
name: master-and-baseline
description: Initialize and maintain the candidate Master Fact Layer (content/master/) and the single Universal CV Baseline (src/sections/baseline-universal.tex). Use when onboarding after forking the repo, adding or updating candidate experiences/education/projects/skills/certifications in master data, or when the user explicitly asks to refresh the universal baseline resume.
---

# Stage 0: Master Data & Universal Baseline Maintenance

## When to Use

- **Onboarding a fresh clone/fork**: Initializing local private files (`content/master/*.md` and `src/sections/header.private.tex`) from tracked `.example` templates.
- **Updating candidate facts**: Recording new internship/work stages, coursework/grades, projects, skills, or certifications into `content/master/`.
- **Refreshing the Universal CV Baseline**: Updating `src/sections/baseline-universal.tex` and `RESUME_BASELINE.md` **only** when the user explicitly requests a baseline refresh.

Read `content/master/README.md`, `RESUME_BASELINE.md`, and `.agent/rules/content.md` before making edits.

---

## Workflow Checklist

```markdown
Task Progress:
- [ ] Step 1: Identify mode (Bootstrap / Master Fact Update / Explicit Baseline Refresh)
- [ ] Step 2: Update or initialize `content/master/*.md` (facts only, no editorial omit rules)
- [ ] Step 3: (Only if requested) Curate `src/sections/baseline-universal.tex` & update `RESUME_BASELINE.md`
- [ ] Step 4: (Only if baseline changed) Run isolated build, 1-page + >=80% height QA, and visual check
- [ ] Step 5: Run `python3 scripts/workspace.py check` and `python3 scripts/privacy_check.py`
```

---

## Mode A: Fresh Repo Onboarding (`bootstrap`)

1. Run the bootstrap command to create untracked local files without overwriting existing ones:
   ```bash
   python3 scripts/workspace.py bootstrap
   ```
2. Ask the user to fill in their real contact details locally in `src/sections/header.private.tex` (**never** read, print, or commit `src/sections/header.private.tex`).
3. Guide the user (or take their provided resume/notes) to populate `content/master/{profile,education,experience,projects,skills,certifications}.md`.

---

## Mode B: Maintaining `content/master/*.md` (Single Source of Truth)

When the user provides new experiences, project details, grades, or screenshots:

1. **Extract verifiable facts only**:
   - **Stage & Timeline**: Separate multi-stage roles at the same employer (e.g., Phase 1 vs. Phase 2 after extension/promotion) with exact dates.
   - **Ownership vs. Upstream**: Clearly distinguish what the candidate built end-to-end vs. upstream pipelines/platforms maintained by other teams (consumed as sources).
   - **Deployment Lifecycle**: Explicitly record whether a system is `In development`, `Review passed / pre-production`, or `In production`, and distinguish `Intended audience` from `Active users`.
   - **Internal Codenames**: Record internal tool codenames alongside external-facing readable descriptions (e.g., `Internal codename: X -> External CV phrase: internal BI platform`).
   - **Unverified Details**: Tag any uncertain metric, library, or system name with `Need verification`. Never expose `Need verification` items on external resumes/letters.
2. **Maintain Reusable Candidate Bullets**:
   - Under each role/project in `content/master/`, keep a bank of verified, high-density candidate bullets (`Action + Method/Tool + Impact/Delivery Surface`) for downstream tailoring.
3. **Strict Separation Rule**:
   - **Do NOT** write editorial rules ("omit on 1-page CV", "do not list library X") inside `content/master/*.md`. Put repo-wide editorial rules in `.agent/rules/content.md` and single-role choices in `targets/<slug>/tailoring.md`.
   - Updating `content/master/` **does not** automatically trigger a baseline rebuild or rewrite historical targeted resumes.

---

## Mode C: Refreshing the Universal CV Baseline (Explicit Request Only)

Only execute when the user explicitly requests refreshing the universal baseline:

1. Cross-check `src/sections/baseline-universal.tex` against all files in `content/master/`.
2. Enforce formatting and content constraints from `.agent/rules/content.md`:
   - Strict reverse-chronological order in `Experience` (`\cvexpblock`).
   - Macro-only structural bolding (`\cvexpblock`, `\cveduhead`, `\cvskillblock`); no arbitrary `\textbf{...}` inside bullets or `\cvedunote{...}`.
   - Single-page target with balanced bottom density (last content line >= 80% page height).
3. Run isolated build and visual QA:
   ```bash
   ./scripts/build.sh baseline
   pdftoppm -png -r 150 output/review/resume-baseline/resume-baseline.pdf /tmp/resume-baseline-page
   ```
4. Inspect `/tmp/resume-baseline-page-1.png` with Read. If 2 pages, compress clauses; if `< 80%` height (bottom whitespace), backfill factual density from `content/master/` and recompile.
5. Update the refresh log in `RESUME_BASELINE.md`. When approved by the user, publish via `./scripts/build.sh baseline --publish`.
