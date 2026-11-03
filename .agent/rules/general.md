# Project Long-Term Memory & General Governance (`general.md`)

> This directory (`.agent/rules/`) stores the long-term engineering rules and reusable constraints for `latex-application-workflow`. Root entry points (`AGENTS.md`, `CLAUDE.md`, and the thin `.cursor/rules/project-memory.mdc` router) hold only safety boundaries and on-demand routing; detailed domain rules are maintained here in pure Markdown.

---

## 1. Project Purpose

1. **Decouple Facts from Typesetting**: Maintain structured candidate facts in `content/master/` and version-controlled LaTeX resumes and cover letters in `src/` and `versions/`.
2. **Standardize the 6-Stage Agentic Workflow**: Break the application lifecycle into six explicit stages—*Master & Baseline Maintenance -> Job Intake -> Role Pre-writing -> Targeted Resume -> Targeted Cover Letter -> Publish & Status Sync*—codified as reusable skills under `.agent/skills/`.
3. **Deterministic Harness & Anti-Drift QA**: Use `scripts/workspace.py` for deterministic 3-digit ID allocation, schema validation, LaTeX dependency resolution, automated single-page and density QA, and immutable snapshot protection.
4. **Privacy by Default**: Exclude personal contact headers (`src/sections/header.private.tex`), real master fact files (`content/master/*.md`), real job target packages (`targets/<slug>/`), local sub-workspaces (`cn-campus-2027/`), and generated PDFs via `.gitignore` and enforce pre-commit verification via `scripts/privacy_check.py`.

---

## 2. Core Principles

- **Understand Before Editing**: Follow the `AGENTS.md` routing table to read the relevant `.agent/skills/` file, `.agent/rules/` document, target quartet, and master facts before modifying files.
- **Master-First Single Source of Truth (SoT)**: `content/master/` is the sole source of truth for candidate facts and evidence. Never fabricate experiences, metrics, tools, grades, or application events.
- **Explicit One-Way Derivation**:
  - Updating `content/master/` **never automatically** rewrites `baseline`;
  - Refreshing `baseline` **never automatically** rewrites historical `targeted` resumes;
  - Submitted (`applied` and later) targeted LaTeX files and published PDFs are historical snapshots and **must never** be overwritten by subsequent builds.
- **Pre-write Before LaTeX**: Every targeted resume or cover letter must complete role-specific planning in `targets/<slug>/tailoring.md` before creating or editing LaTeX files.
- **Minimal Blast Radius**: Modify only the files required for the active stage and avoid unrelated refactoring.
- **Strict Header Privacy**: Never read, print, or stage `src/sections/header.private.tex`. If a local compilation fails, inspect only the public `output/review/<JOBNAME>/build.log` and guide the user to check their private header locally.

---

## 3. Four-Tier Information Ownership (Never Mix Layers)

| Tier | Location | What Belongs Here | What Is Forbidden Here |
|---|---|---|---|
| **Repo-Wide Rules & Skills** | `.agent/rules/*.md`, `.agent/skills/*/SKILL.md` | Cross-role workflow sequence, formatting guardrails, 1-page compression hierarchy, 5-paragraph cover letter standard, status table contract | Single-role temporary trade-offs or application progress |
| **Candidate Master Facts (SoT)** | `content/master/*.md` | Verified experiences, stage timelines, candidate ownership vs. upstream boundaries, grades, credential status, `Need verification` items, reusable bullet bank | Editorial omission rules such as "omit X on 1-page CV" or "drop Projects first" |
| **Single-Role Decisions** | `targets/<slug>/tailoring.md`, `notes.md` | JD keyword mapping, Profile angle, experience bullet shortlist, honest skill gaps, 5-paragraph cover letter outline for that specific role | Copying repo-wide workflow rules verbatim |
| **Application Status & History** | `PROJECT_STATUS.md`, `targets/<slug>/metadata.yaml` | 9-column current snapshot table + 4-column dated event history table | Long-form rule explanations, free-text notes columns, or batch edit logs |

---

## 4. Long-Term Memory Update Policy

### When to Update `.agent/rules/` or `.agent/skills/`
- Establishing new durable typesetting rules, LaTeX macro conventions, or naming invariants;
- Codifying reusable resume/cover letter writing rules or recurring QA lessons;
- Recording explicit, permanent user preferences (e.g., standard external phrasing for an employer stage or default skill categories);
- Extending status enumerations or validation checks in `scripts/workspace.py`.

### What Must NOT Be Added to Rule Files
- One-off JD keyword phrasing for a single application (belongs in `targets/<slug>/tailoring.md`);
- Temporary LaTeX compilation troubleshooting or environment hiccups;
- Individual application progress events (belongs in `PROJECT_STATUS.md` and `targets/<slug>/metadata.yaml`).
