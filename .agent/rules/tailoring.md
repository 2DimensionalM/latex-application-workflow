# Role Pre-writing & Tailoring Rules (`tailoring.md`)

> Applicable when preparing a role-specific pre-writing plan (`targets/<slug>/tailoring.md`) or before drafting a targeted resume and cover letter. Associated skill: `.agent/skills/job-prewrite/SKILL.md`.

---

## 1. Standard 6-Step Customization Sequence (Never Skip Steps)

1. **Master Facts First (`content/master/`)**: Verify that candidate facts and reusable candidate bullets are up to date in `content/master/`.
2. **Target Package Ready (`targets/<slug>/`)**: Confirm `jd.md`, `notes.md`, and `metadata.yaml` are registered per `.agent/rules/intake.md`.
3. **Role Pre-writing (`targets/<slug>/tailoring.md` — Mandatory Default)**: Before creating or editing any targeted LaTeX files, complete the role-specific evidence mapping, section trade-offs, and 5-paragraph cover letter plan in `tailoring.md`.
4. **Targeted Resume (`targeted-resume`)**: Fork from the single universal baseline `src/sections/baseline-universal.tex` to create `src/sections/targeted-<short-slug>.tex` and `versions/cv/targeted/{id}-resume-<company>-<role>-<location>.tex`, then run isolated build and 1-page / bottom-whitespace visual QA.
5. **Targeted Cover Letter (`targeted-cover-letter`)**: Using `tailoring.md`, `content/master/`, and the target resume, create `src/sections/letters/targeted-<short-slug>-letter.tex` and `versions/letter/targeted/{id}-cover-letter-<short-slug>.tex`, then verify the 5-paragraph structure and >=60% body-height QA.
6. **Publish & Status Sync (`status-and-publish`)**: After visual verification, run `--publish`, link the published PDFs in `PROJECT_STATUS.md`, update the status group order, and run `workspace.py check`.

---

## 2. Division of Responsibility: `tailoring.md` vs. `content/master/` vs. `.agent/rules/`

| Location | Sole Responsibility | Forbidden Content |
|---|---|---|
| `.agent/rules/*.md` | Cross-role workflow sequence, formatting guardrails, compression hierarchy, 5-paragraph cover letter standard | Single-role temporary trade-offs |
| `content/master/*.md` | Pure candidate fact inventory (stage timelines, grades, skill evidence, project details, `Need verification` items) | Editorial omission rules ("omit X on CV") |
| `targets/<slug>/tailoring.md` | **This role only**: JD requirement breakdown -> master evidence mapping, Profile/Skills/Bullet selection, 5-paragraph cover letter outline, interview risks | Copying repo-wide rules verbatim; writing one-off JD keywords back into `baseline` or `master` |

---

## 3. Six Mandatory Sections in `targets/<slug>/tailoring.md`

Every real target's `tailoring.md` must address the following six areas before LaTeX drafting begins:

### 1. Core JD Signals & Profile Direction
- What are the 2–3 core business or technical problems this role is hired to solve?
- How should the 2–3 sentence `Profile` summary connect the candidate's degree, strongest delivery experience, and core stack directly to this role?

### 2. Section Trade-offs & Single-Page Layout Plan
- Which sections are included on the 1-page resume (`Profile`, `Education`, `Experience`, `Projects`, `Skills`)?
- Should `Projects` be a standalone section or folded into `Experience` / `Education` to preserve 1-page density?
- Which coursework, grades, or thesis/graduation project notes should be highlighted in `Education`?

### 3. Experience Bullet Shortlist (Strict Reverse-Chronological Order)
- **Ordering guardrail**: Employer blocks in `Experience` **always remain in strict reverse-chronological order** (newest/current role at the top). Never reorder employers by JD relevance.
- For each employer block, list the shortlisted candidate bullets, the methods/tools/deliverables to emphasize, and secondary details that can be expanded (for bottom-whitespace backfill) or tightened (if over 1 page).

### 4. Skills Alignment & Honest Gaps
- **Prioritized verified skills**: Keywords requested by the JD that are backed by verified evidence in `content/master/skills.md` (including default `AI-assisted engineering` items).
- **Honest gaps (never claim on CV)**: Tools or qualifications mentioned in the JD that the candidate has not verified or used. Explicitly note how to position adjacent verified strengths in the cover letter or interview instead of fabricating keywords.

### 5. Five-Paragraph Cover Letter Plan
- **Paragraph 1 (Hook Opening)**: Why this specific company, team, product, or role design?
- **Paragraph 2 (Focused Resume Proof)**: Which 1–2 strongest verified delivery examples prove readiness without recapping the entire resume?
- **Paragraph 3 (Company / Role Insight)**: Concrete observation on the workflow, architecture, or operational challenge described in the JD.
- **Paragraph 4 (Forward-Looking First-Weeks Plan — Mandatory)**: Concrete, honest plan for how to ramp up in the first weeks and what specific problem to investigate or solve first.
- **Paragraph 5 (Logistics & Specific Closing)**: Start window, duration, days/week, location/language confirmation + a specific, non-template interview discussion topic.

### 6. Open Questions & Interview Risks
- Which eligibility, timeline, or technical depth questions are likely to come up in screening, and what are the defensible answers grounded in `content/master/`?
