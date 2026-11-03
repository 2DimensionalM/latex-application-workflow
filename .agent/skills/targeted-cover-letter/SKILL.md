---
name: targeted-cover-letter
description: Draft, compile, and visually QA a targeted 5-paragraph LaTeX cover letter that meets the mandatory >=60% page-height threshold. Use when the user asks to write, revise, or build a cover letter for a job target.
---

# Stage 4: Targeted Cover Letter Drafting & >=60% Height QA

## When to Use

Trigger this skill when drafting or updating a targeted cover letter for a job package `targets/<slug>/` (internal ID `<id>`).
- **Prerequisite**: `targets/<slug>/tailoring.md` must be completed first. Do not use a generic "universal cover letter"; every cover letter must be written specifically for the target company and role.

Read `.agent/rules/content.md`, `.agent/rules/tailoring.md`, `targets/<slug>/tailoring.md`, `targets/<slug>/jd.md`, `targets/<slug>/notes.md`, and the target's resume section (`src/sections/targeted-<short-slug>.tex`).

---

## Workflow Checklist

```markdown
Task Progress:
- [ ] Step 1: Verify `targets/<slug>/tailoring.md` has the 5-paragraph cover letter plan
- [ ] Step 2: Create `src/sections/letters/targeted-<short-slug>-letter.tex`
- [ ] Step 3: Create `versions/letter/targeted/{id}-cover-letter-<short-slug>.tex` & update `metadata.yaml`
- [ ] Step 4: Draft the 5-paragraph body (anti-prose-resume check + forward-looking execution paragraph)
- [ ] Step 5: Run `./scripts/build.sh letter:<id>` and check `qa.json` (`pages == 1` and `body_end_fraction >= 0.60`)
- [ ] Step 6: Render PNG via `pdftoppm -png -r 100` and visually verify layout & >=60% body height
- [ ] Step 7: Update `PROJECT_STATUS.md` stage and run `python3 scripts/workspace.py check`
```

---

## Step-by-Step Instructions

### 1. Create the Cover Letter Entry & Section Files
- Entry file `versions/letter/targeted/{id}-cover-letter-<short-slug>.tex`:
  ```latex
  \documentclass[10pt,a4paper]{article}
  \input{preamble-letter}
  \input{macros-letter}
  \begin{document}
  \input{sections/header}
  \input{sections/letters/targeted-<short-slug>-letter}
  \end{document}
  ```
- Section file `src/sections/letters/targeted-<short-slug>-letter.tex`:
  ```latex
  \vspace{0.4em}
  \today

  \vspace{0.4em}
  \noindent
  Hiring Team\\
  <Company Name>\\
  <City, Country>

  \vspace{0.3em}
  \LetterSubject{Application for <Role Title> (<Employer Job ID if any>)}

  Dear Hiring Team,

  % Paragraph 1: Hook Opening
  ...

  % Paragraph 2: Focused Resume Proof (1-2 anchors only)
  ...

  % Paragraph 3: Company / Role Understanding & Motivation
  ...

  % Paragraph 4: Forward-Looking First-Weeks Execution Plan (Mandatory)
  ...

  % Paragraph 5: Logistics & Specific Closing
  ...

  \vspace{0.6em}
  Sincerely,\\[0.8em]
  <Full Name or Sign-off>
  ```
- Set `cover_letter_version: "versions/letter/targeted/{id}-cover-letter-<short-slug>.tex"` in `targets/<slug>/metadata.yaml`.

### 2. Enforce the Mandatory 5-Paragraph Structure & Anti-Prose-Resume Rule
- **Anti-Prose-Resume Rule**: Never restate the resume bullet-by-bullet in prose. Any paragraph that merely paraphrases resume bullets without adding role-specific context or forward-looking reasoning must be rewritten.
- **5 Mandatory Paragraphs**:
  1. **Hook Opening**: Lead directly with why this company, product, engineering culture, or role design matters—never start with `"I am writing to apply for..."`.
  2. **Focused Resume Proof**: Cite only 1–2 concrete delivery anchors from `content/master/` that prove the candidate can handle the core technical/operational demand of this role.
  3. **Company / Role Insight**: Share a specific observation or judgment about how this role fits into the team's workflow, architecture, or business model based on `jd.md` and `notes.md`.
  4. **Forward-Looking Execution Plan (Mandatory)**: Detail how the candidate plans to ramp up in the first weeks, what concrete problem or pipeline they want to investigate/solve first, and how they will bridge any honest gaps.
  5. **Logistics & Closing**: State availability (start date, duration, days per week, location/language) and close with a concrete, non-template question or discussion topic for the interview.

### 3. Isolated Build & Mandatory >= 60% Page-Height QA Loop
Run the isolated build and render the page image:
```bash
./scripts/build.sh letter:<id>
pdftoppm -png -r 100 output/review/{id}-cover-letter-<short-slug>/{id}-cover-letter-<short-slug>.pdf /tmp/letter-review-<id>
```
1. Check `qa.json` output:
   - `pages` must be `1`;
   - `body_end_fraction` (measured from top of page to the last line of body text before `Sincerely,`) **must be >= 0.60**.
2. Inspect `/tmp/letter-review-<id>-1.png` using the Read tool.
3. **If `body_end_fraction < 0.60`**:
   - Expand substantive content in Paragraph 4 (forward-looking plan) or deepen the role/company analysis in Paragraphs 2–3;
   - **Never** inflate font size, line spacing (`\baselinestretch`), or margins to fake the 60% threshold;
   - Recompile and re-verify until `body_end_fraction >= 0.60` and the visual layout is clean on 1 page.
