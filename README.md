# LaTeX Application Workflow

一套**隐私优先（Privacy-First）、基于 Context Architecture 与自动化 Harness 驱动**的 LaTeX 英文简历与求职信（CV & Cover Letter）工程化工作流。

本项目将**候选人事实资产（`content/master/`）**、**唯一跨市场通用基线（`baseline-universal.tex`）**、**单岗预写决策（`targets/<slug>/tailoring.md`）**与**定向 LaTeX 编译及 PDF 视觉/版面自动 QA（`scripts/workspace.py`）**解耦，并将从「岗位链接进项目」到「发布投递与状态追踪」的每一步沉淀为标准化 Agent Skills（`.cursor/skills/`），支持任何用户 Fork 后直接上手与扩展。

---

## 一、快速上手（Fork 后 3 步初始化）

### 环境要求
- Python 3.10+
- TeX Live 或 TinyTeX（提供 `pdflatex`）
- Poppler（推荐，提供 `pdftoppm` 供 Agent 渲染 PDF 页面进行目视 QA）

### 初始化命令

```bash
# 1. 创建虚拟环境并安装校验/QA依赖（PyYAML, pdfplumber）
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt

# 2. 一键生成本地私有文件（从 *.example.md 生成 content/master/*.md，并生成 src/sections/header.private.tex）
.venv/bin/python scripts/workspace.py bootstrap

# 3. 校验工作区一致性并编译通用 CV 基线与五段式求职信模板
.venv/bin/python scripts/workspace.py check
./scripts/build.sh baseline
./scripts/build.sh letter-placeholder
```

- 构建默认输出至隔离目录 `output/review/<JOBNAME>/`（包含 `<JOBNAME>.pdf`、`build.log`、`latex.log` 与自动版面检测报告 `qa.json`）。
- 编辑 `src/sections/header.private.tex` 填入真实姓名与联系方式（该文件已被 `.gitignore` 忽略且禁止 Agent 读取）。
- 编辑 `content/master/*.md` 填入你的真实教育、经历、项目、技能与证书事实（同样被 `.gitignore` 忽略，永不上传）。

---

## 二、Agentic Workflow 全流程与标准化 Skills

本仓库在 `.cursor/skills/` 下沉淀了 **6 个标准化阶段技能**，并在 `AGENTS.md` 与 `.cursor/rules/project-memory.mdc` 中建立了按需路由：

```
[Stage 0: 母版与通用基线维护]  (.cursor/skills/master-and-baseline/SKILL.md)
   content/master/*.md (唯一事实源 SoT) ──(显式刷新)──► src/sections/baseline-universal.tex (唯一一页父本)
          │
          ▼
[Stage 1: 岗位链接/JD进项目]   (.cursor/skills/job-intake/SKILL.md)
   `workspace.py init` 分配三位编号 001..999 ──► 建立 targets/<slug>/{metadata.yaml, jd.md, notes.md, tailoring.md}
   并同步 PROJECT_STATUS.md 主表新行（进展 = 待预写）
          │
          ▼
[Stage 2: 岗位预写与证据映射]  (.cursor/skills/job-prewrite/SKILL.md)
   对照 jd.md + notes.md + content/master/ ──► 撰写 targets/<slug>/tailoring.md 六大模块（严禁跳过预写直接改 LaTeX）
          │
          ├───────────────────────────────────────────────────┐
          ▼                                                   ▼
[Stage 3: 定向简历制作与 QA]                                [Stage 4: 定向求职信制作与 QA]
(.cursor/skills/targeted-resume/SKILL.md)                  (.cursor/skills/targeted-cover-letter/SKILL.md)
 - 从 baseline-universal.tex 分叉                           - 基于 tailoring.md 五段提纲创建信件正文
 - 严格保持 Experience 时间倒序                              - 拒绝“简历散文复述”，强制包含第 4 段前瞻切入计划
 - `./scripts/build.sh resume:<id>`                        - `./scripts/build.sh letter:<id>`
 - 强制单页 + 正文底端 ≥80% 页高（留白自动回补闭环）          - 强制单页 + 正文底端 ≥60% 页高实测闭环
          │                                                   │
          └─────────────────────────┬─────────────────────────┘
                                    ▼
[Stage 5: 成品发布与状态追踪]  (.cursor/skills/status-and-publish/SKILL.md)
   `./scripts/build.sh <target> --publish` 发布防覆盖快照 ──► 更新 PROJECT_STATUS.md 产物链接、分组行序与历史动作时间线
```

| 阶段 | Skill 路径 | 触发场景示例 | 核心产出与门禁 |
|---|---|---|---|
| **0. 母版与基线** | [`.cursor/skills/master-and-baseline/SKILL.md`](.cursor/skills/master-and-baseline/SKILL.md) | “初始化项目”、“把这段新实习加进 master”、“刷新通用 baseline” | 更新 `content/master/*.md` 或 `baseline-universal.tex` |
| **1. 链接进项目** | [`.cursor/skills/job-intake/SKILL.md`](.cursor/skills/job-intake/SKILL.md) | “把这个招聘链接进项目”、“登记这三条岗位 URL” | 分配 `internal_id`、生成结构化英文 `jd.md` 与 `notes.md`、更新 `PROJECT_STATUS.md` |
| **2. 岗位预写** | [`.cursor/skills/job-prewrite/SKILL.md`](.cursor/skills/job-prewrite/SKILL.md) | “帮我预写 001 岗位”、“做 001 的 tailoring 规划” | 完成 `targets/<slug>/tailoring.md` 六大模块映射 |
| **3. 定向简历** | [`.cursor/skills/targeted-resume/SKILL.md`](.cursor/skills/targeted-resume/SKILL.md) | “写 001 的定向简历”、“编译并检查 001 简历留白” | 生成 `{id}-resume-....tex`、通过 1 页 + ≥80% 页面填充度 QA |
| **4. 定向求职信** | [`.cursor/skills/targeted-cover-letter/SKILL.md`](.cursor/skills/targeted-cover-letter/SKILL.md) | “写 001 的求职信 / cover letter” | 生成 `{id}-cover-letter-....tex`、五段式结构、通过 ≥60% 正文高度 QA |
| **5. 发布与状态** | [`.cursor/skills/status-and-publish/SKILL.md`](.cursor/skills/status-and-publish/SKILL.md) | “发布 001 的 PDF”、“001 已投递 / 收到一面 / 已拒” | `--publish` 写入正式目录、更新 `PROJECT_STATUS.md` 分组排序与历史表 |

---

## 三、Context Architecture 与长期记忆规范

项目采用**「薄根路由 + 按需领域规则 + 阶段化 Skills」**架构，避免将数万字历史经验无条件塞入每次对话上下文：

| 文档路径 | 职责说明 |
|---|---|
| [`AGENTS.md`](AGENTS.md) / [`.cursor/rules/project-memory.mdc`](.cursor/rules/project-memory.mdc) | 始终加载的安全红线与任务路由表（保持两处同步） |
| [`STRUCTURE.md`](STRUCTURE.md) | 目录职责、五层数据流与文件命名/编号不变量 |
| [`RESUME_BASELINE.md`](RESUME_BASELINE.md) | 唯一跨市场 CV 基线的定义、刷新边界与分叉规范 |
| [`PROJECT_STATUS.md`](PROJECT_STATUS.md) | 标准化的 9 列岗位总表 + 4 列带日期历史动作时间线 |
| [`content/master/README.md`](content/master/README.md) | 候选人事实库（SoT）维护规范与 6 个 `*.example.md` 模板说明 |
| [`targets/README.md`](targets/README.md) | 岗位目标包四件套契约与 `metadata.yaml` Schema |
| [`scripts/README.md`](scripts/README.md) | `workspace.py`、`build.sh`、`build_all.py`、`privacy_check.py` 完整命令手册 |
| [`docs/rules/general.md`](docs/rules/general.md) | 核心工程原则、三层信息归属与长期记忆更新策略 |
| [`docs/rules/intake.md`](docs/rules/intake.md) | 招聘 URL 抓取、ATS 解析技巧、开放状态交叉验证与非英语 JD 翻译规范 |
| [`docs/rules/tailoring.md`](docs/rules/tailoring.md) | 定制六步顺序与 `tailoring.md` 六大模块标准 |
| [`docs/rules/content.md`](docs/rules/content.md) | 母版事实记录规范、简历单页压缩与留白回补闭环、求职信五段结构与 ≥60% 高度铁律 |
| [`docs/rules/status.md`](docs/rules/status.md) | `PROJECT_STATUS.md` 9 列总表、3 级状态分组移动规则与 4 列历史表规范 |
| [`docs/rules/structure.md`](docs/rules/structure.md) | LaTeX 宏与三层分离架构（`src/` vs `versions/`） |
| [`docs/rules/build.md`](docs/rules/build.md) | 隔离构建、自动 PDF/Log QA 与快照防覆盖发布机制 |

---

## 四、隐私安全模型（Privacy by Design）

1. **私有文件默认隔离**：
   - `src/sections/header.private.tex`（真实姓名、地址、电话、邮箱、个人主页链接）
   - `content/master/*.md`（真实个人履历事实库，仅跟踪 `README.md` 与 `*.example.md`）
   - `targets/<slug>/`（真实申请岗位包，仅跟踪 `targets/example-company-role/`）
   - `versions/cv/targeted/*.tex`、`src/sections/targeted-*.tex`、`src/sections/letters/targeted-*.tex`
   - `output/**`（所有编译生成的 PDF 与日志）
   - 本地特定目录（如 `cn-campus-2027/`、`_inbox/`、`nuffic/`）
2. **提交前强制门禁**：
   每次 `git commit` / `git push` 前运行：
   ```bash
   .venv/bin/python scripts/privacy_check.py
   .venv/bin/python scripts/workspace.py check
   .venv/bin/python -m unittest discover -s scripts/tests -v
   ```
   `privacy_check.py` 会扫描所有已跟踪和已暂存文件，一旦发现被禁止的私有路径、二进制/PDF 文件、邮箱地址、电话号码或密钥即刻报错阻断。
