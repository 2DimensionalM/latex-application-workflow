---
name: targeted-resume
description: Draft and build one targeted resume. Use when the user asks for a resume for an existing target.
---

# Resume only

Read `targets/<slug>/tailoring.md`, `jd.md`, and `src/sections/baseline-universal.tex`. If tailoring is still a placeholder, write that compact plan first. Do not open `.agent/rules/`.

Copy the baseline section to `src/sections/targeted-<slug>.tex`, add `versions/cv/targeted/{id}-resume-<company>-<role>-<location>.tex` with the baseline wrapper, and set `resume_version`. Keep Experience reverse-chronological and do not add `\textbf` inside bullets. Run `./scripts/build.sh resume:{id}` until `qa.json` shows one page and no errors. If `body_end_fraction < 0.80`, add verified detail and rebuild.
