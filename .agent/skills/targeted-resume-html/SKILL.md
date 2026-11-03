---
name: targeted-resume-html
description: Draft and QA a single-page targeted HTML resume from the owner's HTML master (制作 HTML 定向简历). Use instead of targeted-resume when the resume format is HTML.
---

# Step 3 (HTML variant): Targeted HTML Resume

Prerequisite: `targets/<slug>/tailoring.md` is complete (`.agent/skills/job-prewrite/SKILL.md`). Read `.agent/rules/content.md`, `tailoring.md`, `jd.md`.

1. **Parent**: `content/master/resume.html` (owner's HTML master, Git-ignored). Read-only: never modify, print, stage or commit it.
2. **Create** `versions/cv/targeted/{id}-resume-<company>-<role>-<location>.html` (Git-ignored) by copying the master and changing only selection, order and wording of facts already present. Keep CSS/structure; keep experience in reverse-chronological order; never alter dates, titles, employers, numbers or credentials.
3. Set `resume_version` in `targets/<slug>/metadata.yaml` to that path.
4. **Build + QA**: `.venv/bin/python scripts/workspace.py build resume:<id>` renders with headless Chrome and runs the same PDF QA (1 page, body ends >= 80% page height). Fix and rebuild until `qa.json` has no errors.
5. Publish only with `--publish` after the user has reviewed the PDF; then follow `.agent/skills/status-and-publish/SKILL.md`.

Never claim skills the master does not support; list them as gaps in `tailoring.md`.
