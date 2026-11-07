# LaTeX Application Workflow

Load only the file for the current task. Do not preload `README.md`, `STRUCTURE.md`, `.agent/README.md`, or `.agent/rules/`.

- Never read, print, or commit `src/sections/header.private.tex`. Diagnose build failures from `output/review/<JOBNAME>/build.log`.
- Never invent candidate facts, skills, metrics, job requirements, or application status. `content/master/` is the fact source.
- Do not commit real `content/master/*.md`, real `targets/<slug>/`, PDFs, or `cn-campus-2027/`.
- A compiled PDF is not an application. Do not overwrite an already published targeted PDF.
- For repository maintenance, run `python3 scripts/privacy_check.py` and `python3 scripts/workspace.py check` before committing to `main`.

| Task | Read only |
|---|---|
| Job URL through resume and cover letter | `.agent/skills/application-pipeline/SKILL.md` |
| Intake only, pre-write only, resume only, or letter only | The matching file in `.agent/skills/`; do not also open `.agent/rules/` |
| Publish a snapshot or record applied, interview, offer, rejected, closed | `.agent/skills/status-and-publish/SKILL.md` |
| Edit master facts or refresh the universal baseline | `.agent/skills/master-and-baseline/SKILL.md` |
| Change the harness, layout, or these instructions | The one matching file under `.agent/rules/` or `scripts/README.md` |
