# Application Workflow（`feature/html-engine-webui` 分支）

一套**隐私优先、Agent 驱动**的求职材料工作流：用一份结构化的个人事实库，按岗位生成**一页英文简历**，自动做版面质检，并在一个**本地网页工作台**里管理投递进度。

这个分支在原有的 LaTeX 工作流之上，增加了两样东西：

1. **HTML 简历引擎**：事实库 `content/master/*.md` → HTML 母版简历 → 每个岗位一份定制 HTML 简历 → 用无头 Chrome 转成 PDF，并沿用原来的 PDF 质检（必须一页、内容填满 ≥80% 页高）。不需要安装 LaTeX。
2. **本地网页工作台 `webui/`**：投递看板、事实库编辑、简历预览，以及在网页里直接调用 Claude Code（`claude -p`）完成"贴链接 → 生成定制简历 / 求职信"。

原来的 LaTeX 路径（`src/*.tex`、`versions/**/*.tex`、`./scripts/build.sh baseline` 等）完全保留，两条路径共用同一套编号、状态表和质检规则。

---

## 一、整体逻辑：五层数据流

```
① 事实库（唯一事实来源，本地私有）
   content/master/{profile,education,experience,projects,skills,certifications}.md
   + src/sections/header.private.tex（姓名与联系方式）
        │  scripts/render_html.py（套用 src/html/resume.template.html 版式）
        ▼
② HTML 母版简历（本地私有，自动生成，不要手改）
   content/master/resume.html
        │
        │  ③ 岗位登记：workspace.py init → targets/<slug>/{metadata.yaml, jd.md, notes.md, tailoring.md}
        │     并在 PROJECT_STATUS.md 新增一行（三位编号 001、002…，只增不回收）
        ▼
④ 定制简历（本地私有，每个岗位一份）
   versions/cv/targeted/{id}-resume-<company>-<role>-<location>.html
   只允许对母版里已有的事实做挑选、排序、改写，不能新增事实
        │  workspace.py build resume:<id>（无头 Chrome → PDF → 一页/留白质检）
        ▼
⑤ 审阅与发布
   output/review/<JOBNAME>/{<JOBNAME>.pdf, qa.json}      ← 每次构建，可反复覆盖
   output/cv/targeted/<JOBNAME>.pdf                       ← --publish 正式快照，防覆盖
```

几条核心原则（详见 `AGENTS.md` 与 `.agent/rules/`）：

- **事实只改一处**：经历、项目、技能等一律改 `content/master/*.md`，再重新生成母版。不要直接改 `resume.html`。
- **不编造**：定制简历和求职信只能使用事实库里已有的内容；事实库里标了 `Need verification` 的内容，核实前不得写进对外材料。
- **投递过的版本不被覆盖**：母版更新不会改动已有的定制简历；`--publish` 拒绝覆盖已存在的快照。
- **状态只记真实事件**：`PROJECT_STATUS.md` 的历史表只记录投递、面试、结果等真实发生的事，不记录"写了简历""编译了 PDF"。

---

## 二、快速上手

### 环境要求

| 依赖 | 用途 | 是否必需 |
|---|---|---|
| Python 3.10+ | 脚本与网页服务 | 必需 |
| Google Chrome | HTML → PDF 渲染与质检 | HTML 路径必需（也可用 `CHROME_BIN` 指定 Chromium） |
| [Claude Code](https://claude.com/claude-code) CLI（`claude`，已登录） | 网页里的"生成定制简历""生成求职信" | 只在用 AI 功能时需要 |
| TeX Live / TinyTeX（`pdflatex`） | 原 LaTeX 路径 | 只走 HTML 路径可以不装 |

### 初始化

```bash
# 1. 虚拟环境与依赖（PyYAML、pdfplumber）
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt

# 2. 从模板生成本地私有文件：content/master/*.md 与 src/sections/header.private.tex（已存在的不会覆盖）
.venv/bin/python scripts/workspace.py bootstrap

# 3. 填写你自己的事实与联系方式（这些文件被 .gitignore 忽略）
#    content/master/*.md            参照同目录 *.example.md 的结构
#    src/sections/header.private.tex  姓名、城市、邮箱、电话、GitHub

# 4. 生成 HTML 母版简历，并检查工作区
.venv/bin/python scripts/render_html.py
.venv/bin/python scripts/workspace.py check

# 5. 启动网页工作台，打开 http://127.0.0.1:8765
.venv/bin/python webui/server.py
```

> 启动时报 `Address already in use`：说明已有一个服务占着 8765 端口，先关掉它（在它的终端按 Ctrl+C）。改了 `webui/` 或 `scripts/` 的代码后，需要重启服务才会生效。

### 事实库文件怎么写

`render_html.py` 按固定字段解析 md，字段名要和 `*.example.md` 保持一致。常用约定：

| 写法 | 作用 |
|---|---|
| `## 1. 公司 — 职位` | 一段经历或一个项目的标题 |
| `- **Dates:** Mar 2025 – Sep 2025` | 经历日期（同年会自动缩写成 `Mar – Sep 2025`） |
| `- **Context & Dates:** … (Jul 2025)` | 项目日期，括号里的日期优先 |
| `- **CV Title:** …` | 母版简历上显示的职位名（有多个写法时指定一个） |
| `- **Reusable Candidate Bullets:**` 下的 `` - `…` `` | 放进简历的 bullet |
| `- **On baseline CV:** no` | 只留在事实库，不放进母版简历（用来控制一页） |
| `Need verification` | 待核实标记，网页里会高亮并计数 |
| `skills.md` 里的表格 | 每个 `##` 小节是一组技能，第一列是显示在简历上的文字 |

---

## 三、网页工作台（`webui/`）

只监听 `127.0.0.1`，会拒绝来自其他网站的请求。

| 区块 | 功能 |
|---|---|
| 统计卡片 | 岗位总数、已投递、准备中、流程中、已结束 |
| Claude 模型 | 页面右上角选择：跟随 Claude Code 默认、Opus（质量最好）或 Sonnet（更快、更省）。选择保存在浏览器里，对之后的生成、修改和求职信都生效；进度面板会显示实际使用的模型 |
| 新建申请 | 粘贴职位链接或 JD 文本 → 后台运行 `claude -p`，按 `.agent/skills/` 的阶段流程登记岗位、预写、生成定制 HTML 简历并质检。页面逐步显示 Claude 在做什么（读取、抓取、写入、构建），最后单独显示结果；原始日志折叠在"原始日志"里。服务器会先用 Python 直接抓取 JD（支持 LinkedIn、Workday 和带 JobPosting 结构化数据的招聘页），抓不到时才让 Claude 自己抓 |
| 投递看板 | 编号、公司、职位、地点、登记日期、投递日期，按"准备中 / 已投递·流程中 / 已结束"分组。改"状态"会同步 `metadata.yaml` 与 `PROJECT_STATUS.md`（移动到对应分组；只有投递及之后的状态写入历史表） |
| 简历预览 | 生成并显示该岗位的 PDF。预览使用系统字体以提速，源文件没变时直接复用上次的 PDF；`--publish` 正式发布时才加载网页字体 |
| 求职信 | 调用 `claude -p` 按五段式规则起草，保存为 `targets/<slug>/cover_letter.md`（纯文本草稿，不走 LaTeX 构建） |
| 修改简历 / 求职信 | 在"简历预览 / 修改"或"求职信 / 修改"下方输入修改要求，Claude 只改这一份文件，只用事实库里已有的内容；需要事实库没有的内容时会拒绝并说明。修改前当前版本自动备份到 `targets/<slug>/.history/`，简历改完会重新构建并质检。下方"历史版本"可一键恢复任意旧版（恢复前也会先备份当前版本，所以恢复本身可以撤销） |
| 事实库 | 查看和编辑 6 个 `content/master/*.md`：预览 / 编辑切换，保存前检查文件是否被别处改过，旧版本自动备份到 `content/master/.history/`；一键"重新生成母版简历"并显示质检结果；查看母版 PDF |

网页不会显示 `src/sections/header.private.tex`。

---

## 四、命令速查

| 命令 | 作用 |
|---|---|
| `.venv/bin/python scripts/render_html.py` | 由事实库生成 `content/master/resume.html` |
| `.venv/bin/python scripts/workspace.py init --url … --slug … --company … --role … --location … --write` | 登记岗位（不加 `--write` 只预览） |
| `.venv/bin/python scripts/workspace.py list` | 列出所有构建目标 |
| `.venv/bin/python scripts/workspace.py build resume:<id>` | 构建某岗位的简历（`.html` 入口走 Chrome，`.tex` 入口走 LaTeX） |
| `.venv/bin/python scripts/workspace.py build resume:<id> --publish` | 质检通过后发布防覆盖快照 |
| `.venv/bin/python scripts/workspace.py check` | 校验 `metadata.yaml`、`PROJECT_STATUS.md`、构建入口的一致性 |
| `.venv/bin/python scripts/privacy_check.py` | 扫描已跟踪文件中的私有路径、邮箱、电话、密钥 |
| `.venv/bin/python -m unittest discover -s scripts/tests -v` | 回归测试 |
| `CV_ONLINE_FONTS=1 .venv/bin/python webui/server.py` | 预览也加载网页字体（更接近设计稿，但更慢） |

更多 LaTeX 路径的命令见 [`scripts/README.md`](scripts/README.md)。

---

## 五、这个分支新增或改动的文件

| 路径 | 说明 |
|---|---|
| [`scripts/render_html.py`](scripts/render_html.py) | 事实库 → HTML 母版简历的生成器（只打印输出路径，不打印内容） |
| [`src/html/resume.template.html`](src/html/resume.template.html) | HTML 简历版式模板（只有样式与结构，不含个人内容） |
| [`scripts/workspace.py`](scripts/workspace.py) | 新增 `.html` 构建入口：无头 Chrome 渲染、预览缓存、复用原 PDF 质检与防覆盖发布 |
| [`webui/server.py`](webui/server.py)、[`webui/index.html`](webui/index.html) | 本地网页工作台 |
| [`.agent/skills/targeted-resume-html/SKILL.md`](.agent/skills/targeted-resume-html/SKILL.md) | HTML 定制简历的阶段技能（替代 `targeted-resume` 的 LaTeX 步骤） |
| [`.agent/rules/webui.md`](.agent/rules/webui.md) | 网页工作台的行为与安全边界 |
| `.gitignore` | 新增忽略 `versions/cv/targeted/*.html`、`versions/letter/targeted/*.html` |

---

## 六、Agent 工作流（`.agent/skills/`）

`AGENTS.md`（以及 `CLAUDE.md`、`.cursor/rules/project-memory.mdc`）是所有 Agent 的入口，按任务阶段路由到对应技能与规则：

| 阶段 | Skill | 触发示例 | 产出与门禁 |
|---|---|---|---|
| 0. 母版与基线 | [`master-and-baseline`](.agent/skills/master-and-baseline/SKILL.md) | "把这段新实习加进 master" | 更新 `content/master/*.md` |
| 1. 岗位登记 | [`job-intake`](.agent/skills/job-intake/SKILL.md) | "把这个招聘链接进项目" | 分配编号，写英文 `jd.md` 与 `notes.md`，更新 `PROJECT_STATUS.md` |
| 2. 岗位预写 | [`job-prewrite`](.agent/skills/job-prewrite/SKILL.md) | "帮我预写 001" | `tailoring.md` 六大模块（含诚实缺口） |
| 3. 定制简历（LaTeX） | [`targeted-resume`](.agent/skills/targeted-resume/SKILL.md) | "写 001 的简历" | `.tex` 入口，1 页 + ≥80% 填充 |
| 3b. 定制简历（HTML） | [`targeted-resume-html`](.agent/skills/targeted-resume-html/SKILL.md) | 母版为 HTML 时 | `.html` 入口，同样的质检 |
| 4. 求职信 | [`targeted-cover-letter`](.agent/skills/targeted-cover-letter/SKILL.md) | "写 001 的求职信" | 五段式，≥60% 正文高度 |
| 5. 发布与状态 | [`status-and-publish`](.agent/skills/status-and-publish/SKILL.md) | "001 已投递 / 收到一面" | `--publish` 快照，更新状态表与历史表 |

规则文档（按需加载）：[`general`](.agent/rules/general.md)、[`intake`](.agent/rules/intake.md)、[`tailoring`](.agent/rules/tailoring.md)、[`content`](.agent/rules/content.md)、[`status`](.agent/rules/status.md)、[`structure`](.agent/rules/structure.md)、[`build`](.agent/rules/build.md)、[`webui`](.agent/rules/webui.md)。目录职责与命名规则见 [`STRUCTURE.md`](STRUCTURE.md)。

---

## 七、隐私模型

以下内容被 `.gitignore` 忽略，**永远不应提交**：

- `content/master/*`（事实库、生成的 `resume.html`、`.history/` 备份；只跟踪 `README.md` 与 `*.example.md`）
- `src/sections/header.private.tex`（真实联系方式）
- `targets/<slug>/`（真实岗位包；只跟踪 `targets/example-company-role/`）
- `versions/cv/targeted/*.{tex,html}`、`versions/letter/targeted/*.{tex,html}`、`src/sections/targeted-*.tex` 等定制稿
- `output/**`（所有 PDF 与日志）

**特别注意 `PROJECT_STATUS.md`**：它是被 Git 跟踪的文件（仓库里只放空白表头），但你本地使用时会写入真实岗位记录。提交时请**不要勾选它**。如果不小心提交并推送了，需要从分支历史里移除，单纯再提交一次删除并不能清掉历史里的内容。

提交或推送前建议运行：

```bash
.venv/bin/python scripts/privacy_check.py
.venv/bin/python scripts/workspace.py check
.venv/bin/python -m unittest discover -s scripts/tests -v
```

---

## 八、已知限制

- `test_live_repository_checks_and_manifest` 假定仓库里没有真实岗位；本地登记了岗位后这条测试会失败，在干净克隆里是通过的。
- `privacy_check.py` 会把链接里较长的数字（如 LinkedIn 职位编号）误报为电话号码。
- HTML 构建除了页数和留白，还会检查内容是否被页面框裁掉（页面样式会隐藏溢出部分，PDF 看起来仍是一页），并生成第 1 页 PNG 供目视检查。
- 预览使用系统字体，字形与设计稿略有不同；正式发布时使用网页字体。
- 网页里生成的求职信是 Markdown 草稿，不经过 LaTeX 版面质检。
- 本分支基于较早的 `main`，与最新 `main`（文档英文化、MIT 许可证）尚未合并。
