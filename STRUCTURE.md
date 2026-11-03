# Workspace 结构、数据流与命名边界

本文件定义项目的 Context Architecture 与目录职责边界。日常岗位清单见 `PROJECT_STATUS.md`，构建目标清单运行 `python3 scripts/workspace.py list`。

## 一、五层数据流（Context → Master → Baseline → Tailoring → Snapshot）

```
[外部输入: 个人经历证据 / 招聘页 URL / JD]
       │
       ▼
1. content/master/*.md          ← 唯一候选人事实源 (SoT)：完整经历、分阶段边界、成绩、待核实项、候选 bullet 池（只记事实，不写裁剪规则）
       │ (仅在用户明确要求刷新时策展)
       ▼
2. src/sections/baseline-universal.tex
   + versions/cv/baseline/resume-baseline.tex  ← 唯一跨市场通用一页 CV 基线（所有新岗定制的共同父本）
       │
       ├─── 岗位登记 (job-intake)  ──► targets/<slug>/{metadata.yaml, jd.md, notes.md, tailoring.md} + PROJECT_STATUS.md
       │
       ▼
3. targets/<slug>/tailoring.md  ← 岗位预写决策层 (job-prewrite)：JD 映射、板块取舍、经历 bullet 短名单、求职信五段大纲
       │
       ▼
4. 定向 LaTeX 源码 (targeted-resume / targeted-cover-letter)
   - 简历正文: src/sections/targeted-<short-slug>.tex
   - 简历入口: versions/cv/targeted/{id}-resume-<company>-<role>-<location>.tex
   - 信件正文: src/sections/letters/targeted-<short-slug>-letter.tex
   - 信件入口: versions/letter/targeted/{id}-cover-letter-<short-slug>.tex
       │
       ├─── 隔离构建与视觉 QA (`./scripts/build.sh`) ──► output/review/<JOBNAME>/{<JOBNAME>.pdf, qa.json, latex.log}
       │
       ▼
5. 正式发布快照 (`--publish` + status-and-publish)
   - output/cv/targeted/{id}-resume-<company>-<role>-<location>.pdf
   - output/cover-letters/pdf/targeted/{id}-cover-letter-<short-slug>.pdf
   (一旦投递，保留历史快照语义，不因后续母版或基线更新而重编译覆盖)
```

## 二、目录与文件职责

| 路径 | 职责与版本控制边界 |
|---|---|
| `AGENTS.md` / `.cursor/rules/project-memory.mdc` | 始终加载的安全边界、Git 策略与任务路由（保持两处一致） |
| `.cursor/skills/<skill-name>/SKILL.md` | 6 个标准化 Agentic Workflow 技能定义（按阶段触发或显式调用） |
| `docs/rules/` | 按任务按需加载的长期细则（`general.md`、`intake.md`、`tailoring.md`、`content.md`、`status.md`、`structure.md`、`build.md`） |
| `content/master/` | 候选人完整事实库 SoT。仓库仅跟踪 `README.md` 与 `*.example.md` 模板；本地真实 `*.md` 被 `.gitignore` 忽略 |
| `RESUME_BASELINE.md` | 唯一通用 CV 基线的定义、刷新边界与复用规范 |
| `targets/<slug>/` | 一岗一包四件套：`metadata.yaml`、`jd.md`、`notes.md`、`tailoring.md`。仓库仅跟踪 `targets/example-company-role/` |
| `PROJECT_STATUS.md` | 人类可编辑的 9 列岗位总表 + 4 列带日期历史动作表 |
| `src/preamble*.tex`、`src/macros*.tex` | 简历与求职信共享排版与宏定义（`\cvexpblock`、`\cveduhead`、`\cvskillblock`、`\LetterSubject`） |
| `src/sections/header.tex` | 页眉入口：若本地存在 `header.private.tex` 则自动加载，否则回退到公开占位 `header.template.tex` |
| `src/sections/header.private.tex` | 本地真实姓名与联系方式（Git 忽略，禁止 Agent 读取或打印） |
| `src/sections/baseline-universal.tex` | 通用一页 CV 基线正文片段 |
| `src/sections/targeted-*.tex` | 单岗定向简历正文片段（本地维护，Git 忽略） |
| `src/sections/letters/` | 求职信正文片段（含公开占位模板与本地 `targeted-*-letter.tex`） |
| `versions/cv/{base,baseline,targeted}/` | 简历编译入口（`JOBNAME` 自动取入口文件名 stem） |
| `versions/letter/{baseline,targeted}/` | 求职信编译入口 |
| `output/review/<JOBNAME>/` | 默认隔离构建输出（PDF、`build.log`、`latex.log`、`qa.json`），不会覆盖已发布快照 |
| `output/cv/`、`output/cover-letters/pdf/` | `--publish` 产出的正式投递快照目录 |
| `scripts/workspace.py` | 核心 Harness：支持 `bootstrap`、`init`、`check`、`list`、`build`、`qa`、`affected` |
| `scripts/build.sh`、`scripts/build_all.py` | 单目标构建包装器与批量隔离构建编排器 |
| `scripts/privacy_check.py` | 隐私与敏感文件门禁检查器（拦截私有路径、PDF 二进制与邮箱/电话/密钥） |
| `scripts/tests/test_workspace.py` | 无网络、临时夹具驱动的自动化回归测试 |

## 三、命名与编号不变量

1. **目标包目录**：`targets/<company-role-location>/`，全小写字母、数字与连字符。
2. **内部编号（`internal_id`）**：三位零填充数字字符串 `"001"`–`"999"`，按岗位入仓先后递增分配，**全局唯一、只增不改、缺号绝不回收**。`"000"` 仅留给 `example-company-role` 模板。
3. **定向简历入口与 PDF 名**：`versions/cv/targeted/{id}-resume-<company>-<role>-<location>.tex` → `output/cv/targeted/{id}-resume-<company>-<role>-<location>.pdf`。
4. **定向求职信入口与 PDF 名**：`versions/letter/targeted/{id}-cover-letter-<short-slug>.tex` → `output/cover-letters/pdf/targeted/{id}-cover-letter-<short-slug>.pdf`。
5. **自动注册**：在 `targets/<slug>/metadata.yaml` 填入真实存在的 `resume_version` 或 `cover_letter_version` 后，`workspace.py` 自动注册别名 `resume:<id>`、`resume:<slug>`、`letter:<id>`、`letter:<slug>` 及 `<JOBNAME>`，无需手改 `scripts/build.sh` 或 `scripts/build-targets.json`。
