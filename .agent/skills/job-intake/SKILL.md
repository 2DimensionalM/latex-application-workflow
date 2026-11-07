---
name: job-intake
description: Register a job URL or JD without writing a resume or cover letter. Use only when the user wants intake and explicitly does not want finished materials.
---

# Intake only

If the user wants the resume and cover letter too, follow `.agent/skills/application-pipeline/SKILL.md` instead. Do not open `.agent/rules/`.

Fetch the posting, then run `python3 scripts/workspace.py init --url URL --slug company-role-city --company '...' --role '...' --location '...' --write`. Write an English `jd.md`, short `notes.md`, and leave `tailoring.md` pending. Set `status: open` and the status row to `Pending Pre-write`, or `closed` / `Closed` only after JSON-LD or the ATS payload confirms the posting is gone. Run `python3 scripts/workspace.py check` once.
