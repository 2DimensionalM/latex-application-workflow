# Local web UI (`webui/`)

`.venv/bin/python webui/server.py` serves http://127.0.0.1:8765 (localhost only; Host/Origin checked).

- Board reads `targets/*/metadata.yaml` + `PROJECT_STATUS.md`; changing progress updates the status row, moves it to its group, adds a history row, and syncs `metadata.yaml` status. Only user-confirmed real events should be recorded.
- "New application" and cover-letter drafts run `claude -p` in the repo root with a restricted tool list and prompts that route through `.agent/skills/`. Cover letters from the UI are plain drafts in `targets/<slug>/cover_letter.md` (not LaTeX builds).
- HTML resume preview builds through `scripts/workspace.py build resume:<id>` (headless Chrome) and shows the review PDF.
- Fact library: the owner can view and edit the six `content/master/*.md` files in the UI (localhost only). Saves are refused if the file changed since it was opened, and the previous version is kept in `content/master/.history/` (Git-ignored). "Regenerate" rebuilds `content/master/resume.html` via `scripts/render_html.py` and runs the one-page QA. The UI never shows `src/sections/header.private.tex` or `content/master/resume.original.html`. Needs the `claude` CLI and Chrome installed.
