---
name: targeted-resume-html
description: Draft and QA a single-page targeted HTML resume from the owner's HTML master (制作 HTML 定向简历). Use instead of targeted-resume when the resume format is HTML.
---

# Step 3 (HTML variant): Targeted HTML Resume

Prerequisite: `targets/<slug>/tailoring.md` is complete (`.agent/skills/job-prewrite/SKILL.md`). Read `.agent/rules/content.md`, `tailoring.md`, `jd.md`.

1. **Parent**: `content/master/resume.html` (Git-ignored), generated from `content/master/*.md` + the private header by `.venv/bin/python scripts/render_html.py`. Facts are edited in the `.md` files, never in the HTML; re-render after a fact change. Never print, stage or commit the parent.
2. **Create** the tailored resume as a Markdown spec `versions/cv/targeted/{id}-resume-<company>-<role>-<location>.md` (Git-ignored). Start from `.venv/bin/python -c "import sys; sys.path.insert(0,'scripts'); import render_html; print(render_html.baseline_markdown())"` and change only: Tagline, Profile, which Experience/Projects entries appear (### headings must match fact-file names; entries marked `On baseline CV: no` may be added), bullet wording, Coursework lines and Skills lines. Employers, titles, dates, locations, tech stacks, links, name, contact and photo come from the fact files; Experience is printed newest first and every employer must stay. The build renders the spec into the `.html` entry next to it. Older targets without a `.md` keep their hand-edited `.html`.
3. Set `resume_version` in `targets/<slug>/metadata.yaml` to that path.
4. **Build + QA**: `.venv/bin/python scripts/workspace.py build resume:<id>` renders with headless Chrome and runs the same PDF QA (1 page, body ends >= 80% page height). Fix and rebuild until `qa.json` has no errors. For the visual check, Read the page-1 PNG the build writes (`png` in `qa.json`); no poppler/pdftoppm is needed.
5. Publish only with `--publish` after the user has reviewed the PDF; then follow `.agent/skills/status-and-publish/SKILL.md`.

Never claim skills the master does not support; list them as gaps in `tailoring.md`.
