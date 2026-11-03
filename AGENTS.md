# LaTeX Application Workflow: Safety Boundaries & Context Architecture Router (`AGENTS.md`)

This file is the primary, agent-agnostic entry point for the repository (compatible with Codex, Claude Code, Cursor, Windsurf, OpenCode, and other agents). All long-term memory, domain rules, and standardized workflow skills are maintained in pure Markdown under **`.agent/`**, decoupled from any single IDE's proprietary format.

## 1. Core Safety & Engineering Guardrails

- **Privacy & Security Boundaries**:
  - Never read, print, stage, or commit `src/sections/header.private.tex` (even if a LaTeX build fails, diagnose only from public logs and ask the user to inspect their private header locally).
  - Never stage or commit real candidate master facts (`content/master/*.md`; keep only `README.md` and `*.example.md` templates tracked), real job target packages (`targets/<slug>/`; keep only `example-company-role/`), generated PDFs, or local sub-workspaces (`cn-campus-2027/`).
  - Run `python3 scripts/privacy_check.py` and `python3 scripts/workspace.py check` before every `git commit` and `git push`.
- **Fact & Snapshot Integrity**:
  - Never fabricate candidate facts, skills, metrics, job requirements, or application status; `content/master/` is the Single Source of Truth (SoT).
  - Preserve the semantics and published PDF snapshots of submitted (`applied` and later) applications; updating `content/master/` does not automatically refresh `baseline` or back-write historical targeted materials.
  - Never submit applications automatically, access employer portals with write actions, or run destructive Git commands.
- **Git Commit & Push Policy**:
  - Once local checks (`workspace.py check`, unit tests, and `privacy_check.py`) pass, commit and push directly to `origin/main` (`git commit` + `git push origin main`) without opening a pull request.
- **On-Demand Context Loading**: Load only the `.agent/skills/` and `.agent/rules/` files required for the active task stage. Do not eagerly read unrelated files.

## 2. Stage-by-Stage Task Router (`.agent/skills/` + `.agent/rules/`)

| Workflow Stage / Task | Standardized Skill (`.agent/skills/`) | On-Demand Rules & Reference Docs (`.agent/rules/`, etc.) |
|---|---|---|
| **0. Onboarding / Maintaining `content/master/` / Refreshing Universal Baseline** | `.agent/skills/master-and-baseline/SKILL.md` | `content/master/README.md`, `RESUME_BASELINE.md`, `.agent/rules/content.md` |
| **1. Job URL & JD Intake** | `.agent/skills/job-intake/SKILL.md` | `.agent/rules/intake.md`, `targets/README.md`, `.agent/rules/status.md` |
| **2. Role Pre-writing & Evidence Mapping (`tailoring.md`)** | `.agent/skills/job-prewrite/SKILL.md` | `.agent/rules/tailoring.md`, `.agent/rules/content.md`, target `jd.md` / `notes.md` |
| **3. Targeted Resume Drafting & 1-Page Visual QA** | `.agent/skills/targeted-resume/SKILL.md` | `.agent/rules/content.md`, `.agent/rules/tailoring.md`, `RESUME_BASELINE.md`, target quartet |
| **4. Targeted Cover Letter Drafting & >=60% Height QA** | `.agent/skills/targeted-cover-letter/SKILL.md` | `.agent/rules/content.md`, `.agent/rules/tailoring.md`, target quartet & resume |
| **5. Publishing PDF Snapshots & Updating `PROJECT_STATUS.md`** | `.agent/skills/status-and-publish/SKILL.md` | `.agent/rules/status.md`, `scripts/README.md`, target `metadata.yaml` |
| **Build / QA / Harness Scripts & Context Architecture Maintenance** | — | `.agent/README.md`, `scripts/README.md`, `.agent/rules/build.md`, `.agent/rules/structure.md`, `STRUCTURE.md`, `.agent/rules/general.md` |
