# 母版维护与简历/求职信内容排版规范 (Master Data, Resume & Cover Letter Rules)

> 适用场景：维护 `content/master/` 事实库、刷新通用 `baseline`、撰写或修改定向简历（`src/sections/*.tex`）与求职信（`src/sections/letters/*.tex`）。对应标准化 Skills：`.agent/skills/master-and-baseline`、`.agent/skills/targeted-resume`、`.agent/skills/targeted-cover-letter`。

---

## 一、母版事实库（`content/master/`）维护准则

### 1. `content/master/` 的唯一定位：可辩护事实与证据链 SoT
- **只存事实，不存裁剪规则**：`content/master/` 记录候选人完整、真实的经历细节、时间线分期、课程与总评/分项成绩、脚本/系统真名、项目架构、证书编号及可复用的候选 bullet 池。
- **不要因“一页简历放不下”而删减母版事实**：对外简历需要精炼，但母版应保留完整技术上下文与演进历史，以便后续针对不同类型岗位随时提取证据。
- **不要在母版中写对外省略指令**：诸如“投递简历时默认不写某库名”、“一页放不下时先删 Projects”属于仓库级内容规则（维护在本文件 `.agent/rules/content.md`）或单岗决策（维护在 `targets/<slug>/tailoring.md`），严禁混入 `content/master/*.md`。

### 2. 结构化事实记录的四个关键维度
在维护 `content/master/experience.md`、`projects.md`、`education.md`、`skills.md`、`certifications.md` 时，必须写清以下边界：
1. **阶段与时间线边界（Stage & Timeline）**：若同一雇主有岗位晋升、续签或项目阶段演进（如 Phase 1 报表自动化 → Phase 2 生产级应用开发），必须明确区分各阶段的时间区间与职责，不得将早期静态产物混同于当前架构，也不得抹掉职位升级信号。
2. **所有权与上下游边界（Ownership vs. Upstream Context）**：明确区分“本人端到端设计/实现/交付的部分”与“上游数据工程/平台团队维护的基础设施（仅作为数据源消费）”。对外简历严禁将消费上游平台写成拥有上游管线。
3. **生命周期与上线状态（Lifecycle & Deployment State）**：严格区分 `In development`（开发中）、`Architecture/Security review passed, pre-production`（评审通过/待上线）、`In production`（已上线生产）以及 `Intended audience`（预计受众人数）与 `Active users`（实际活跃用户）。严禁将待上线系统写成已正式投产或夸大活跃用户数。
4. **内部代号与待核实项（Internal Codenames & `Need verification`）**：
   - 雇主内部平台代号可在母版中记录以便检索，但须注明对应的外部可读类别描述（如 `internal BI platform`、`internal collaboration site`）。
   - 尚未完全确认的指标、具体库名或历史系统名，在母版中显式标记 `Need verification`；在未核实前**严禁**写入对外简历或求职信。

---

## 二、对外简历（Resume / CV）写作与版式铁律

### 1. 叙事与措辞准则
- **能力与交付优先（Capability-First）**：每条 bullet 遵循 **「做了什么动作 + 用了什么方法/工具 + 交付给谁/产生了什么业务影响」**。不堆砌仅对内部有意义的 `.py` 脚本文件名或底层琐碎 plumbing。
- **内部工具名可读化**：外部招聘方无法理解前雇主的内部系统代号，对外正文统一使用行业可读表述（如 `internal BI platform`、`linked audit workbook`）。
- **技能与证书证据链**：
  - `Skills` 板块的每一项主张都必须在 `Education`、`Experience` 或 `Projects` 中有据可查；不把泛化职位头衔词当作独立技术技能堆砌。
  - 若稳定使用 AI 辅助工程工作流（如 `Cursor`、`Claude Code CLI`、`AI-native thinking`、`Agentic workflow`），可在 `Skills` 的 `AI-assisted engineering:` 类别中清晰呈现，并在经历中配以具体交付事实支撑，避免空泛 hype（不使用 `vibe coding` 等口语化表述）。
  - 证书严格区分**行业/职业认证（Professional/Career Credentials）**与**课程结业证书（Course Credentials）**；在读/未结业课程严禁写成已获证。

### 2. Experience 板块顺序铁律（强制时间倒序）
- `\cvexpblock` 各段经历**永远按时间倒序排列**（最新/在职经历在最上，早期经历在下）。
- **严禁**因为某段早期经历与当前 JD 更相关，就将其调到更晚近的经历前面。针对 JD 突出某段经历，只能通过**该段内 bullet 的数量、措辞与详略**实现，绝不能打乱时间线。

### 3. 正文字重与宏规范（禁止乱加粗）
- 除 `src/macros.tex` 预留的结构性加粗外（`\cvexpblock` 的职位名、`\cveduhead` 的学校名、`\cvskillblock` 的技能类别名），**严禁**在经历 bullet 正文、`\cvedunote{...}` 教育附注或括号说明中随意使用 `\textbf{...}` 做局部强调或伪小标题。
- 教育附注前缀使用普通正文字重（如 `Coursework:`、`Thesis:`），课程名称使用 `\textit{...}`。

### 4. 单页限制与十级无损压缩优先级
所有投递用英文简历（`baseline` 与 `targeted`）**必须严格控制在单页（1 Page）**。当内容超出 1 页时，按以下优先级收紧，**能不删事实尽量不删**：
1. **收紧长技术从句（首选）**：压缩单条 bullet 内的冗余从句与重复技术枚举，保留「核心动作 + 关键工具 + 交付面/结果」。
2. **消除半行孤词（Widow/Orphan Words）**：收紧只多出两三个词就换行的句子，直接省出整行高度。
3. **全局去冗余词**：精简 `Profile`、经历 bullet 与 `Education` 附注中的套话形容词。
4. **收紧 `Skills` 行**：合并同类技能标签，移除与当前岗位无关的次要细项。
5. **合并近义 Bullet（保留实质信息）**：将同一经历下两条较短或高度相关的 `\item` 合并重写为一条饱满的句子。**未经用户明确同意或 `tailoring.md` 明确授权，Agent 不得擅自整条删除核心经历 bullet**。
6. **收紧 `Education` 附注**：合并课程与论文附注行，不删学位主行。
7. **调整 `Projects` 板块**：当核心项目已在 `Experience` 或 `Education` 充分体现且 `tailoring.md` 允许时，可省略独立 `Projects` 板块。
8. **红线：严禁擅自删除整段雇主经历（`\cvexpblock`）**：除非用户书面确认，绝不以“与 JD 距离远”为由删掉任何一段正式雇主/管培经历。

### 5. 页底留白强制检查与回补闭环（每次编译必做）
- **任何一次编译产出简历 PDF 后**（无论是第一次编译即单页，还是从两页压回单页），都必须检查末页填充度（`qa.json` 的 `body_end_fraction` 及 `pdftoppm` 渲染图）。
- 若正文结束位置偏高（例如低于页面高度 **80%**，页底出现明显大块空白、版面头重脚轻），**必须当场执行回补，不得直接交付**。
- **回补来源优先级**：`targets/<slug>/tailoring.md` 预写候选池 → `content/master/` 事实细节 → `jd.md` 关注点。
- **回补方式**：优先恢复或扩充已有 bullet 的事实密度（补充工具链、干系人或可辩护结果），其次扩充 `Education` 附注、`Profile` 或 `Skills`；回补后重新编译并再次目视确认仍为单页且版面饱满。
- **Bullet 行宽**：单条 `\item` 尽量写满可用行宽，避免半行短句断行导致右侧大面积留白。

---

## 三、求职信（Cover Letter）写作与 60% 篇幅铁律

### 1. 核心质量标准：绝不做“简历的散文复述版”
- 如果求职信只是把简历上的 bullet 加上连接词换个说法抄一遍，没有提供简历之外的新信息，视为**不合格，必须重写**。
- 求职信必须补充简历无法承载的信息：**为什么是这家公司/这个具体岗位**、**为什么是现在申请**、**对该团队业务挑战或工作流的具体理解**、以及**入职后头几周打算如何切入并解决什么具体问题**。

### 2. 强制五段式标准结构
1. **第 1 段 — 钩子开头（Hook Opening）**：开门见山用一句话点明为什么申请这家公司的这个具体岗位（具体到业务、产品、技术方向或岗位设计本身），**禁用** `"I am writing to apply for..."` 等模板套话。
2. **第 2 段 — 精选简历证明（Focused Proof）**：仅点睛式引用 1–2 处最契合的硬核交付事实，证明“我有能力接住这份工作”，**严禁**按时间线把所有经历逐段复述一遍。
3. **第 3 段 — 公司/岗位理解与动机（Role & Company Insight）**：针对该公司商业模式、该岗位在组织中的位置或 JD 中的具体细节提出观察与思考，展示真正读懂了 JD 并研究过公司。
4. **第 4 段 — 前瞻切入计划（Forward-Looking Plan，强制段）**：具体、诚实地说明**入职后打算如何快速上手、最想弄清楚或解决的具体问题、头几周会先做什么**。必须基于 `jd.md` 与 `tailoring.md` 中已核实的事实与边界，不写“我会努力学习”式空话。这是支撑求职信深度与篇幅的关键段落。
5. **第 5 段 — Logistics 与具体收尾（Logistics & Specific Closing）**：交代可入职时间、持续时长、每周可用天数、地点/语言等实用信息 + 一句具体、非模板化的面谈交流点。

### 3. 篇幅硬性下限（≥ 60% 页面高度，强制实测）
- **硬性指标**：求职信正文（从 `Dear ...` 到 `Sincerely,` 之间，不含页眉、日期与底部签名）在单页 A4 上，**最后一行文字的底部位置必须达到整页高度的 60%（3/5）或更靠下**，且总页数严格为 **1 页**。
- **强制验证闭环**：
  1. 运行 `./scripts/build.sh letter:<id>`，检查 `qa.json` 中的 `body_end_fraction` 是否 `>= 0.60` 且无 `errors`；
  2. 运行 `pdftoppm -png -r 100 <pdf_path> <out_prefix>` 并读取生成的 PNG 图片进行**目视复核**；
  3. 若未达到 60% 线，**必须**通过扩充实质内容（优先深化第 4 段前瞻计划或第 2、3 段业务分析）重新编译并重新测量，直到达标。**严禁**通过调大字号、拉大行距或修改页边距来凑页面高度。
