# LaTeX Application Workflow：安全边界与 Context Architecture 路由 (`AGENTS.md`)

本文件是仓库跨 Agent 通用（Codex、Claude Code、Cursor、Windsurf、OpenCode 等）的主入口。所有长期记忆、领域规则与标准化阶段技能统一维护在 **`.agent/`** 目录下，不绑定任何单一 IDE 专有格式。

## 一、核心安全与工程红线

- **隐私与安全红线**：
  - 禁止读取、打印、暂存或提交 `src/sections/header.private.tex`（即使 LaTeX 编译失败也只根据公开日志提示用户本地自查）。
  - 禁止提交候选人真实母版事实（`content/master/*.md`，仅保留 `README.md` 与 `*.example.md` 模板）、真实岗位目录（`targets/<slug>/`，仅保留 `example-company-role/`）、生成的 PDF，或 `cn-campus-2027/` 等本地专有目录。
  - 每次 `git commit` / `git push` 前必须运行 `python3 scripts/privacy_check.py` 与 `python3 scripts/workspace.py check`。
- **事实与快照红线**：
  - 不虚构候选人事实、技能、指标、JD 要求或申请状态；`content/master/` 是唯一事实源（SoT）。
  - 保留已投递及后续流程的定向稿语义和已发布 PDF 快照；母版更新不自动刷新 `baseline` 或回写历史 targeted 稿。
  - 不自动提交申请、不访问雇主受控系统或执行外部写操作；不使用破坏性 Git 命令。
- **Git 提交策略**：
  - 在本地校验（`workspace.py check`、单元测试、`privacy_check.py`）通过后，可直接 `git commit` 并 `git push origin main`，无需走 PR 流程。
- **按需加载上下文**：只读取当前任务所需的 `.agent/skills/` 与 `.agent/rules/` 文档，不无条件遍历无关文件。

## 二、按阶段路由表（`.agent/skills/` + `.agent/rules/`）

| 任务阶段 / 动作 | 对应标准化 Skill (`.agent/skills/`) | 按需读取规则与文档 (`.agent/rules/` 等) |
|---|---|---|
| **0. 首次上手 / 维护 `content/master/` 事实库 / 刷新通用 Baseline** | `.agent/skills/master-and-baseline/SKILL.md` | `content/master/README.md`、`RESUME_BASELINE.md`、`.agent/rules/content.md` |
| **1. 岗位链接 / JD 进项目（Intake）** | `.agent/skills/job-intake/SKILL.md` | `.agent/rules/intake.md`、`targets/README.md`、`.agent/rules/status.md` |
| **2. 岗位预写与证据映射（Pre-write `tailoring.md`）** | `.agent/skills/job-prewrite/SKILL.md` | `.agent/rules/tailoring.md`、`.agent/rules/content.md`、该岗 `jd.md` / `notes.md` |
| **3. 定向简历制作与一页留白 QA（Targeted Resume）** | `.agent/skills/targeted-resume/SKILL.md` | `.agent/rules/content.md`、`.agent/rules/tailoring.md`、`RESUME_BASELINE.md`、该岗四件套 |
| **4. 定向求职信制作与 60% 篇幅 QA（Targeted Cover Letter）** | `.agent/skills/targeted-cover-letter/SKILL.md` | `.agent/rules/content.md`、`.agent/rules/tailoring.md`、该岗四件套与对应简历 |
| **5. 成品发布、状态更新与 `PROJECT_STATUS.md` 联动** | `.agent/skills/status-and-publish/SKILL.md` | `.agent/rules/status.md`、`scripts/README.md`、对应 `metadata.yaml` |
| **构建 / QA / 脚本与 Context Architecture 维护** | — | `.agent/README.md`、`scripts/README.md`、`.agent/rules/build.md`、`.agent/rules/structure.md`、`STRUCTURE.md`、`.agent/rules/general.md` |
