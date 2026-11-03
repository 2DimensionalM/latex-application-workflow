# `.agent/` — Agent-Agnostic Context Architecture Hub

This directory is the central Context Architecture hub for `latex-application-workflow`. All long-term memory, domain rules (`rules/`), and standardized workflow skills (`skills/`) are maintained here in pure Markdown, independent of any single editor or agent's proprietary format (such as `.mdc`).

---

## 1. Multi-Agent Entry & Routing Design

```
                   +------------------------------------------+
                   | AGENTS.md (Primary Boundaries & Router)  |
                   +--------------------+---------------------+
                                        |
        +-------------------------------+-------------------------------+
        ^                               ^                               ^
+-------+--------+            +---------+--------+            +---------+--------------------+
|   CLAUDE.md    |            | Codex / OpenCode |            | .cursor/rules/*.mdc (Router) |
| (Claude Code)  |            |  (Native Read)   |            |  (Points to AGENTS/.agent)   |
+----------------+            +------------------+            +------------------------------+
                                        |
                                        v
                   +-----------------------------------------+
                   |                 .agent/                 |
                   +--------------------+--------------------+
                   v                    v                    v
           .agent/skills/        .agent/rules/        .agent/README.md
        (6 Stage Workflow)     (7 On-Demand Rules)   (Architecture Guide)
```

- **[`AGENTS.md`](../AGENTS.md)**: The single root-level source of safety boundaries and the 6-stage task routing table.
- **[`CLAUDE.md`](../CLAUDE.md)**: Automatic entry point for Claude Code, routing directly to `AGENTS.md` and `.agent/`.
- **[`.cursor/rules/project-memory.mdc`](../.cursor/rules/project-memory.mdc)**: Minimal 10-line adapter for Cursor that delegates to `AGENTS.md` and `.agent/` without storing domain rules itself.

---

## 2. `.agent/skills/` — 6 Standardized Workflow Skills

Each subdirectory contains a `SKILL.md` designed for progressive disclosure:

| Stage | Skill Path | Responsibility |
|---|---|---|
| **Stage 0** | [`.agent/skills/master-and-baseline/SKILL.md`](skills/master-and-baseline/SKILL.md) | First-time `bootstrap` onboarding, maintaining `content/master/*.md` (SoT), and explicitly refreshing the Universal CV Baseline |
| **Stage 1** | [`.agent/skills/job-intake/SKILL.md`](skills/job-intake/SKILL.md) | Job URL / JD intake, ATS text extraction, open/closed cross-verification, and `workspace.py init` ID allocation |
| **Stage 2** | [`.agent/skills/job-prewrite/SKILL.md`](skills/job-prewrite/SKILL.md) | Completing the 6-section pre-writing plan and evidence mapping in `targets/<slug>/tailoring.md` before editing LaTeX |
| **Stage 3** | [`.agent/skills/targeted-resume/SKILL.md`](skills/targeted-resume/SKILL.md) | Forking a targeted resume from the universal baseline, enforcing 1-page compression, and running the >=80% density / bottom-whitespace visual QA loop |
| **Stage 4** | [`.agent/skills/targeted-cover-letter/SKILL.md`](skills/targeted-cover-letter/SKILL.md) | Drafting a 5-paragraph targeted cover letter (with mandatory forward-looking execution plan) and verifying the >=60% body-height threshold |
| **Stage 5** | [`.agent/skills/status-and-publish/SKILL.md`](skills/status-and-publish/SKILL.md) | Publishing immutable PDF snapshots via `--publish` and synchronizing `PROJECT_STATUS.md` (9-column main table + 4-column history table) |

---

## 3. `.agent/rules/` — 7 On-Demand Domain Rules (Long-Term Memory)

Agents load only the rule files needed for the current task to keep context windows lean and focused:

| Rule File | Domain Topic |
|---|---|
| [`.agent/rules/general.md`](rules/general.md) | Core engineering principles, 4-tier information ownership, and long-term memory update policy |
| [`.agent/rules/intake.md`](rules/intake.md) | Job URL intake, ATS extraction patterns, open/closed verification, and non-English JD translation rules |
| [`.agent/rules/tailoring.md`](rules/tailoring.md) | The 6-step customization sequence and the mandatory 6-section specification for `tailoring.md` |
| [`.agent/rules/content.md`](rules/content.md) | Master fact recording dimensions, 1-page resume compression & bottom-whitespace backfill loop, and 5-paragraph cover letter >=60% height rules |
| [`.agent/rules/status.md`](rules/status.md) | `PROJECT_STATUS.md` 9-column schema, `metadata.yaml` status mapping, 3-tier row grouping order, and 4-column history log rules |
| [`.agent/rules/structure.md`](rules/structure.md) | 3-tier LaTeX decoupling (`src/` macros & sections vs. `versions/` entries) and file naming invariants |
| [`.agent/rules/build.md`](rules/build.md) | Isolated review builds, automated PDF/Log QA gates, and `--publish` snapshot overwrite protection |
