# 项目长期记忆与通用准则 (General Principles & Governance)

> 本目录存放 LaTeX Application Workflow 的长期规则与可复用约束。根路由 `AGENTS.md` 与 `.cursor/rules/project-memory.mdc` 仅保留安全红线与按需路由表；具体业务细则按主题维护在本目录对应文件中。

---

## 一、项目目标 (Project Purpose)

1. **事实与排版解耦**：使用 `content/master/` 维护结构化候选人事实资产，使用 `src/` 与 `versions/` 维护可版本控制的 LaTeX 简历与求职信。
2. **标准化 Agentic Workflow**：将求职全生命周期拆解为「母版与基线维护 → 岗位链接进项目 (Intake) → 岗位预写 (Pre-write) → 定向简历 (Targeted Resume) → 定向求职信 (Targeted Cover Letter) → 发布与状态追踪 (Publish & Status)」六个标准化阶段，并沉淀为独立 Skill。
3. **可审计与防漂移**：通过 `scripts/workspace.py` 提供确定性的编号分配、Schema 校验、LaTeX 依赖检查、单页/留白自动 QA 与快照防覆盖保护。
4. **默认隐私安全**：在公开或共享仓库中，个人联系方式（`header.private.tex`）、真实母版事实（`content/master/*.md`）、真实岗位包（`targets/<slug>/`）与生成的 PDF 默认被 `.gitignore` 忽略，并由 `scripts/privacy_check.py` 强制门禁拦截。

---

## 二、核心原则 (Core Principles)

- **先理解再修改**：修改前先按路由读取对应规则、目标包四件套与母版事实，明确当前文件依赖关系。
- **事实源唯一（Master-First）**：`content/master/` 是候选人事实与证据链的唯一事实源（SoT）。绝不虚构经历、指标、工具、成绩或申请进展。
- **单向显式派生**：
  - `content/master/` 更新**不自动**触发 `baseline` 重写；
  - `baseline` 刷新**不自动**回写任何历史 `targeted` 稿；
  - 已投递（`applied` 及后续阶段）的定向稿与已发布 PDF 属于历史交付快照，**严禁**被重编译覆盖。
- **先预写后落稿**：任何真实岗位的定向简历或求职信，必须先在 `targets/<slug>/tailoring.md` 完成岗位专属预写，再基于 `baseline-universal.tex` 创建或修改 LaTeX。
- **最小变更**：只修改完成当前阶段任务所必需的文件，避免无关重构。
- **信息安全红线**：严禁 Agent 读取、输出或提交 `src/sections/header.private.tex`；若本地编译报错，仅根据 `output/review/<JOBNAME>/build.log` 的公开信息指导用户自查私有页眉。

---

## 三、三层信息归属（严禁跨层混写）

| 层级 | 存放位置 | 应该写什么 | 严禁写什么 |
|---|---|---|---|
| **仓库级长期规则** | `docs/rules/*.md`、`.cursor/skills/*/SKILL.md` | 跨岗位通用的流程顺序、排版红线、一页压缩策略、五段求职信规范、状态表契约 | 某一个具体岗位的临时取舍或进度 |
| **候选人事实库 (SoT)** | `content/master/*.md` | 真实经历、时间线分期、本人 ownership 与上下游边界、成绩、证书状态、`Need verification` 待核实项、可复用 bullet 池 | “投递时默认省略 X”、“一页放不下先删 Y” 等对外裁剪规则 |
| **单岗定制决策** | `targets/<slug>/tailoring.md`、`notes.md` | 该岗 JD 关键词映射、Profile 角度、经历 bullet 短名单、诚实技能缺口、求职信五段切入点 | 大段复制仓库级通用规则 |
| **求职进展快照** | `PROJECT_STATUS.md`、`targets/<slug>/metadata.yaml` | 9 列当前岗位总表 + 4 列带日期历史动作时间线 | 冗长的规则说明、备注列或大段修改日志 |

---

## 四、规则与长期记忆更新策略 (Update Policy)

### 应更新 `docs/rules/` 或 `.cursor/skills/` 的情况
- 确立新的长期排版规范、LaTeX 宏约定或命名规则；
- 沉淀出跨岗位可复用的简历/求职信写作红线或踩坑结论；
- 用户明确提出新的长期偏好（例如某段经历的固定对外口径、某类技能标签的暴露方式）；
- 扩展 `workspace.py` 的状态枚举或校验逻辑。

### 不应写入规则文件的情况
- 单个岗位的一次性 JD 迎合措辞（写进该岗 `targets/<slug>/tailoring.md`）；
- 某次临时 LaTeX 编译错误或一次性环境排障；
- 具体岗位的投递/面试进展（写进 `PROJECT_STATUS.md` 与对应 `metadata.yaml`）。
