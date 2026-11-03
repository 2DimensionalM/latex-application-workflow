# `.agent/` — 跨工具通用 Context Architecture 中心

本目录是 `latex-application-workflow` 的核心上下文架构（Context Architecture）中心。所有长期记忆、领域规则（Rules）与标准化阶段技能（Skills）均以纯 Markdown 维护在此处，不绑定任何单一编辑器或 Agent 的专有格式（如 `.mdc`）。

---

## 一、多 Agent 入口与路由设计

```
                   ┌──────────────────────────────┐
                   │   AGENTS.md (主安全边界与路由)  │
                   └──────────────┬───────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        ▲                         ▲                         ▲
┌───────┴────────┐      ┌─────────┴────────┐      ┌─────────┴────────────────────┐
│   CLAUDE.md    │      │ Codex / OpenCode │      │ .cursor/rules/*.mdc (薄路由) │
│ (Claude Code)  │      │   (原生读取)      │      │     (仅指向 AGENTS/.agent)    │
└────────────────┘      └──────────────────┘      └──────────────────────────────┘
                                  │
                                  ▼
             ┌─────────────────────────────────────────┐
             │                 .agent/                 │
             ├────────────────────┬────────────────────┤
             ▼                    ▼                    ▼
     .agent/skills/        .agent/rules/        .agent/README.md
  (6 个标准化阶段技能)    (7 个按需加载领域规则)   (上下文架构说明)
```

- **[`AGENTS.md`](../AGENTS.md)**：全仓库唯一的根级安全边界与任务路由表。
- **[`CLAUDE.md`](../CLAUDE.md)**：Claude Code 自动加载入口，直接路由至 `AGENTS.md` 与 `.agent/`。
- **[`.cursor/rules/project-memory.mdc`](../.cursor/rules/project-memory.mdc)**：Cursor 最小化适配壳（仅 10 行），只负责引导 Agent 读取 `AGENTS.md` 与 `.agent/`，自身不承载任何业务规则或长期记忆。

---

## 二、`.agent/skills/` — 6 个标准化阶段技能

每个子目录包含一份遵循渐进式披露（Progressive Disclosure）的 `SKILL.md`：

| 阶段 | 技能路径 | 职责 |
|---|---|---|
| **Stage 0** | [`.agent/skills/master-and-baseline/SKILL.md`](skills/master-and-baseline/SKILL.md) | Fork 后首次 `bootstrap` 初始化、`content/master/*.md` 事实源维护、显式刷新通用 CV 基线 |
| **Stage 1** | [`.agent/skills/job-intake/SKILL.md`](skills/job-intake/SKILL.md) | 招聘 URL / JD 进项目、ATS 正文提取、开放状态交叉核实、`workspace.py init` 分配编号 |
| **Stage 2** | [`.agent/skills/job-prewrite/SKILL.md`](skills/job-prewrite/SKILL.md) | 在动刀写 LaTeX 前完成 `targets/<slug>/tailoring.md` 六大模块预写与证据映射 |
| **Stage 3** | [`.agent/skills/targeted-resume/SKILL.md`](skills/targeted-resume/SKILL.md) | 从通用基线分叉定向简历、执行单页压缩与页底留白（≥80% 页高）自动 QA + 视觉复核闭环 |
| **Stage 4** | [`.agent/skills/targeted-cover-letter/SKILL.md`](skills/targeted-cover-letter/SKILL.md) | 撰写五段式定向求职信（含第 4 段前瞻切入计划）、执行 ≥60% 页面高度实测与视觉复核闭环 |
| **Stage 5** | [`.agent/skills/status-and-publish/SKILL.md`](skills/status-and-publish/SKILL.md) | `--publish` 发布防覆盖 PDF 快照、同步 `PROJECT_STATUS.md` 9 列总表分组排序与 4 列历史表 |

---

## 三、`.agent/rules/` — 7 个按需加载领域规则（长期记忆）

Agent 根据当前执行的任务阶段按需读取对应规则，避免上下文膨胀：

| 规则文件 | 维护主题 |
|---|---|
| [`.agent/rules/general.md`](rules/general.md) | 核心工程原则、四层信息归属边界与长期记忆更新策略 |
| [`.agent/rules/intake.md`](rules/intake.md) | 岗位 URL 登记、ATS 抓取策略、开放状态防误判与非英语 JD 英译规范 |
| [`.agent/rules/tailoring.md`](rules/tailoring.md) | 岗位定制六步顺序与 `tailoring.md` 六大必填模块规范 |
| [`.agent/rules/content.md`](rules/content.md) | 母版事实记录四维度、简历时间倒序与无损压缩十级优先级、页底留白回补、求职信五段结构与 ≥60% 高度铁律 |
| [`.agent/rules/status.md`](rules/status.md) | `PROJECT_STATUS.md` 9 列总表契约、状态枚举映射、3 级分组移动规则与 4 列历史动作表规范 |
| [`.agent/rules/structure.md`](rules/structure.md) | LaTeX 样式/宏/片段/入口三层解耦架构与文件命名不变量 |
| [`.agent/rules/build.md`](rules/build.md) | 隔离构建、自动 PDF/Log QA 门禁与 `--publish` 快照防覆盖机制 |
