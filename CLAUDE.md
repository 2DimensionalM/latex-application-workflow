# Claude Code Entry Router (`CLAUDE.md`)

本仓库采用跨工具通用的 **`.agent/` + `AGENTS.md`** Context Architecture。

1. **首先读取 [`AGENTS.md`](AGENTS.md)**：获取仓库级隐私红线、事实与快照边界、Git 直接推送策略以及 6 阶段任务路由表。
2. **按任务阶段按需读取 `.agent/`**：
   - **标准化工作流 Skills**：位于 [`.agent/skills/`](.agent/skills/)（`master-and-baseline`、`job-intake`、`job-prewrite`、`targeted-resume`、`targeted-cover-letter`、`status-and-publish`）。
   - **长期记忆与领域规则**：位于 [`.agent/rules/`](.agent/rules/)（`general.md`、`intake.md`、`tailoring.md`、`content.md`、`status.md`、`structure.md`、`build.md`）。
   - **架构说明**：见 [`.agent/README.md`](.agent/README.md) 与 [`STRUCTURE.md`](STRUCTURE.md)。

> 严禁读取或提交 `src/sections/header.private.tex`。长期记忆和领域规则统一维护在 `AGENTS.md` 与 `.agent/rules/` 中，不在工具专属配置文件中重复维护。
