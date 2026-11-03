# Claude Code Entry Router (`CLAUDE.md`)

This repository uses an agent-agnostic **`.agent/` + `AGENTS.md`** Context Architecture.

1. **Read [`AGENTS.md`](AGENTS.md) first**: It defines the repository-wide privacy guardrails, fact/snapshot boundaries, direct-to-`main` Git policy, and the 6-stage task routing table.
2. **Load `.agent/` modules on demand based on the active task stage**:
   - **Standardized Workflow Skills**: Located in [`.agent/skills/`](.agent/skills/) (`master-and-baseline`, `job-intake`, `job-prewrite`, `targeted-resume`, `targeted-cover-letter`, `status-and-publish`).
   - **Long-Term Memory & Domain Rules**: Located in [`.agent/rules/`](.agent/rules/) (`general.md`, `intake.md`, `tailoring.md`, `content.md`, `status.md`, `structure.md`, `build.md`).
   - **Architecture Overview**: See [`.agent/README.md`](.agent/README.md) and [`STRUCTURE.md`](STRUCTURE.md).

> Never read, print, or commit `src/sections/header.private.tex`. Maintain all long-term memory and domain rules inside `AGENTS.md` and `.agent/rules/`, rather than in tool-specific configuration files.
