---
name: targeted-resume
description: Draft, compile, and visually QA a single-page targeted LaTeX resume from the universal baseline and role tailoring plan (制作定向简历与单页留白QA). Use when the user asks to write, customize, or build a targeted resume/CV ("写简历", "制作定向简历", "编译简历") for a specific job target.
---

# Step 3: Targeted Resume Drafting & 1-Page Visual QA (定向简历制作与单页留白 QA)

## When to Use

Trigger this skill when drafting or updating a targeted resume for a specific job package `targets/<slug>/` (internal ID `<id>`).
- **Prerequisite**: `targets/<slug>/tailoring.md` must be completed first. If `tailoring.md` is still a placeholder, execute `.cursor/skills/job-prewrite/SKILL.md` first!

Read `docs/rules/content.md`, `docs/rules/tailoring.md`, `RESUME_BASELINE.md`, `targets/<slug>/tailoring.md`, `targets/<slug>/jd.md`, and `src/sections/baseline-universal.tex`.

---

## Workflow Checklist

```markdown
Task Progress:
- [ ] Step 1: Verify `targets/<slug>/tailoring.md` is complete
- [ ] Step 2: Create `src/sections/targeted-<short-slug>.tex` from `src/sections/baseline-universal.tex`
- [ ] Step 3: Create `versions/cv/targeted/{id}-resume-<company>-<role>-<location>.tex` & update `metadata.yaml`
- [ ] Step 4: Tailor Profile, Education, Experience bullets, and Skills per `tailoring.md` and `docs/rules/content.md`
- [ ] Step 5: Run `./scripts/build.sh resume:<id>` and inspect `qa.json` (must be 1 page, 0 LaTeX errors)
- [ ] Step 6: Render PNG via `pdftoppm` and visually verify page density (if <80% height / bottom whitespace, backfill & recompile)
- [ ] Step 7: Update `PROJECT_STATUS.md` stage (`写简历` / `审核简历` / `待投递`) and run `python3 scripts/workspace.py check`
```

---

## Step-by-Step Instructions

### 1. Fork from the Universal Baseline
- Copy `src/sections/baseline-universal.tex` to `src/sections/targeted-<short-slug>.tex`.
- Create the entry file `versions/cv/targeted/{id}-resume-<company>-<role>-<location>.tex`:
  ```latex
  \documentclass[10pt,a4paper]{article}
  \input{preamble}
  \input{macros}
  \begin{document}
  \small
  \setlength{\parskip}{0.22em}
  \newgeometry{margin=1.62cm}
  \input{sections/targeted-<short-slug>}
  \restoregeometry
  \end{document}
  ```
- Set `resume_version: "versions/cv/targeted/{id}-resume-<company>-<role>-<location>.tex"` in `targets/<slug>/metadata.yaml`.

### 2. Apply Content & Formatting Rules (`docs/rules/content.md`)
- **Strict Reverse-Chronological Experience Order**: Never reorder `\cvexpblock` employer blocks by JD relevance. Keep newest/current roles at the top; emphasize relevance via bullet selection and phrasing.
- **No Random `\textbf{...}`**: Only rely on structural bolding inside `\cvexpblock`, `\cveduhead`, and `\cvskillblock`. Never put `\textbf{...}` inside `\item` bullets or `\cvedunote{...}` (use plain `Coursework:` and `\textit{...}` for course names).
- **Bullet Construction & Line Width**: Write `Action + Method/Tool + Impact/Stakeholder` bullets. Aim to fill each bullet's final line cleanly—avoid orphan 1–3 word line wraps that waste vertical space.
- **Never Back-Write One-Off Keywords**: Do not write company-specific tailoring back into `src/sections/baseline-universal.tex` or `content/master/`.

### 3. Isolated Build & Mandatory 1-Page + Bottom-Whitespace QA Loop
Run the isolated build:
```bash
./scripts/build.sh resume:<id>
pdftoppm -png -r 150 output/review/{id}-resume-<company>-<role>-<location>/{id}-resume-<company>-<role>-<location>.pdf /tmp/cv-review-<id>
```
Read `/tmp/cv-review-<id>-1.png` using the Read tool to inspect the visual layout:

- **Case A — Spills onto 2 pages (`pages > 1`)**:
  Follow the compression hierarchy in `docs/rules/content.md`:
  1. Tighten long technical clauses and remove redundant phrasing first;
  2. Eliminate 1–3 word orphan line wraps;
  3. Tighten `Profile`, `Skills`, and `Education` notes;
  4. Merge two closely related bullets while preserving core facts.
  *(Never delete an entire employer `\cvexpblock` or drop whole bullets without explicit authorization in `tailoring.md` or from the user.)*
- **Case B — 1 page, but visible bottom whitespace (`body_end_fraction < 0.80` or bottom looks empty)**:
  **Do not deliver a top-heavy page with a blank bottom!** Immediately backfill from `targets/<slug>/tailoring.md` → `content/master/` → `jd.md`:
  1. Restore or expand factual density in existing experience bullets (tools, delivery surface, verified outcomes);
  2. Expand `Education` coursework/thesis notes or `Profile` / `Skills` lines;
  3. Recompile and re-inspect the PNG until the page is 1 page and visually balanced.
