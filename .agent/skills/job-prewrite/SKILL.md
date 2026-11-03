---
name: job-prewrite
description: Complete role-specific pre-writing and evidence mapping in targets/<slug>/tailoring.md before drafting any targeted resume or cover letter. Use when the user asks to pre-write a target role, populate tailoring.md, or as the mandatory planning phase before creating a targeted resume or cover letter.
---

# Stage 2: Role Pre-writing & Evidence Mapping (`tailoring.md`)

## When to Use

Trigger this skill when the user asks to pre-write a registered job target (`001`, `<slug>`, etc.) or before drafting a targeted LaTeX resume/cover letter if `targets/<slug>/tailoring.md` is still a placeholder.
- **Core rule**: Never skip pre-writing to directly edit LaTeX. `tailoring.md` is the decision layer connecting `jd.md` + `notes.md` to `content/master/` + `src/sections/baseline-universal.tex`.

Read `.agent/rules/tailoring.md`, `.agent/rules/content.md`, `targets/<slug>/jd.md`, `targets/<slug>/notes.md`, `src/sections/baseline-universal.tex`, and relevant `content/master/*.md` files.

---

## Workflow Checklist

```markdown
Task Progress:
- [ ] Step 1: Read `targets/<slug>/jd.md`, `notes.md`, `baseline-universal.tex`, and `content/master/*.md`
- [ ] Step 2: Analyze core JD signals, must-have keywords, and honest skill gaps
- [ ] Step 3: Write the 6 mandatory sections into `targets/<slug>/tailoring.md`
- [ ] Step 4: Verify no fabricated facts or `Need verification` items are included
- [ ] Step 5: Run `python3 scripts/workspace.py check`
```

---

## Mandatory 6-Section Template for `targets/<slug>/tailoring.md`

Write role-specific decisions only (do not copy repo-wide rules into `tailoring.md`):

```markdown
# Tailoring Plan — <Internal ID> <Company> — <Role>

## 1. Core JD Signals & Profile Direction
- **Core role problem:** What specific business/technical problem does this team need solved?
- **Profile positioning (2–3 sentences):** How the top `Profile` summary connects the candidate's degree, strongest experience, and core stack directly to this role.

## 2. Section Trade-offs & Layout Plan
- **Sections included:** `Profile`, `Education`, `Experience`, `Skills` (and whether `Projects` is included or folded into `Experience`/`Education`).
- **Education emphasis:** Which coursework, grades, or thesis/graduation project notes to surface for this JD.

## 3. Experience Bullet Shortlist (Strict Reverse-Chronological Order)
> Note: Employer blocks in `Experience` always stay in strict reverse-chronological order. Emphasize relevance via bullet selection and phrasing, never by reordering employers.

### <Latest / Current Employer> (<Dates>)
- **Candidate bullet 1:** ...
- **Candidate bullet 2:** ...
- **Candidate bullet 3:** ...
- **Compression / backfill notes:** Which detail to expand if bottom whitespace remains (<80% height), or tighten if over 1 page.

### <Previous Employer> (<Dates>)
- **Candidate bullet 1:** ...
- **Candidate bullet 2:** ...

### <Earlier Employer> (<Dates>)
- **Candidate bullet 1:** ...

## 4. Skills Alignment & Honest Gaps
- **Prioritized verified skills:** Exact categories and keywords backed by `content/master/skills.md` (including `AI-Assisted Engineering` items).
- **Honest gaps (DO NOT claim on CV):** Tools/methods mentioned in the JD that are unverified or absent from `content/master/`, and how to frame adjacent verified strengths instead.

## 5. Five-Paragraph Cover Letter Plan
1. **Paragraph 1 (Hook Opening):** Specific reason for targeting this company, team, product, or role design (no generic "I am writing to apply...").
2. **Paragraph 2 (Focused Resume Proof):** The 1–2 strongest verified delivery examples that prove readiness (do not recap the whole resume).
3. **Paragraph 3 (Company / Role Insight):** Concrete observation on the team's workflow, technical architecture, or business challenge from the JD.
4. **Paragraph 4 (Forward-Looking First-Weeks Plan — Mandatory):** Concrete, honest plan for how to ramp up in the first weeks and what specific problem to tackle first.
5. **Paragraph 5 (Logistics & Specific Closing):** Availability/start date/duration/location confirmation + a specific, non-template conversation starter.

## 6. Open Questions & Interview Risks
- Potential recruiter/hiring manager questions (e.g., timeline, tool gaps, domain transition) and defensible answers grounded in `content/master/`.
```
