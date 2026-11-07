---
name: targeted-cover-letter
description: Draft and build one targeted cover letter. Use when the user asks for a cover letter for an existing target.
---

# Cover letter only

Read `targets/<slug>/tailoring.md` and `jd.md`. Do not open `.agent/rules/`.

Write five paragraphs: why this role, one or two proof points, a specific JD observation, a first-weeks plan, and logistics. Do not retell the resume. Use the wrapper in `versions/letter/targeted/cover-letter-placeholder.tex`, set `cover_letter_version`, and run `./scripts/build.sh letter:{id}` until `qa.json` shows one page and `body_end_fraction >= 0.60`.
