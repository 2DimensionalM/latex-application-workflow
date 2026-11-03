# 岗位预写与定制流程规范 (Role Pre-writing & Tailoring Rules)

> 适用场景：为已登记岗位做投递前规划（预写 `tailoring.md`），或准备撰写定向简历与求职信。对应标准化 Skill：`.agent/skills/job-prewrite/SKILL.md`。

---

## 一、岗位定制标准六步顺序（严禁跳步）

1. **母版事实优先（`content/master/`）**：确认候选人事实与可复用 bullet 已在 `content/master/` 核实完备。
2. **目标包就绪（`targets/<slug>/`）**：确认 `jd.md`、`notes.md`、`metadata.yaml` 已按 `.agent/rules/intake.md` 登记完毕。
3. **岗位预写（`targets/<slug>/tailoring.md`，默认必做、不可跳过）**：在动刀写任何定向 LaTeX 之前，先在 `tailoring.md` 完成该岗专属的证据映射、板块取舍与求职信五段规划。
4. **定向简历（`targeted-resume`）**：以唯一通用父本 `src/sections/baseline-universal.tex` 为起点，创建 `src/sections/targeted-<short-slug>.tex` 与 `versions/cv/targeted/{id}-resume-<company>-<role>-<location>.tex`，完成隔离构建与单页/留白视觉 QA。
5. **定向求职信（`targeted-cover-letter`）**：基于 `tailoring.md`、`content/master/` 与该岗定向简历，创建 `src/sections/letters/targeted-<short-slug>-letter.tex` 与 `versions/letter/targeted/{id}-cover-letter-<short-slug>.tex`，完成五段式结构与 ≥60% 页面高度视觉 QA。
6. **发布与状态联动（`status-and-publish`）**：人工确认成品后执行 `--publish`，更新 `PROJECT_STATUS.md` 的产物链接与进展阶段，并运行 `workspace.py check`。

---

## 二、`tailoring.md`、`content/master/` 与 `.agent/rules/` 的职责分工

| 文件位置 | 唯一职责 | 禁止事项 |
|---|---|---|
| `.agent/rules/*.md` | 跨岗位通用的流程、红线、排版规则、压缩优先级、五段求职信标准 | 不记录单岗临时取舍 |
| `content/master/*.md` | 候选人纯事实库存（经历分期、成绩、技能证据、项目细节、`Need verification`） | 不写“投递时省略 X”等裁剪规则 |
| `targets/<slug>/tailoring.md` | **仅限本岗**：JD 核心要求拆解 → 母版证据映射、Profile/Skills/Bullets 取舍、求职信五段提纲、面试风险点 | 不要大段复制仓库级通用规则；不要把一次性 JD 关键词写回 `baseline` 或 `master` |

---

## 三、`targets/<slug>/tailoring.md` 必备六大模块（预写标准结构）

每份真实岗位的 `tailoring.md` 必须清晰回答以下六个问题（标题可微调，但实质内容不可或缺）：

### 1. 岗位核心信号与 Profile 方向 (Role Positioning & Profile Angle)
- 该岗位真正解决的业务/技术问题是什么（2–3 条核心痛点）？
- 简历顶部 `Profile` 应如何用 2–3 句话建立候选人与该岗位的直接连接？

### 2. 板块结构与详略取舍 (Section Trade-offs)
- 单页简历保留哪些板块（`Profile`、`Education`、`Experience`、`Projects`、`Skills`）？
- `Projects` 板块是否开启，还是将核心项目信号合入 `Experience` / `Education` 以保证单页密度？
- `Education` 附注（课程、论文/毕业设计、GPA）重点突出哪些与本岗相关的科目？

### 3. 经历 Bullet 候选短名单 (Experience Bullet Shortlist)
- **顺序红线**：`Experience` 各段雇主顺序**严格保持时间倒序**（最新/在职在最上），绝不按相关性颠倒时间线。
- 针对每段经历，列出拟选入本岗简历的 bullet 短名单、重点放大的方法/工具/交付物，以及可压缩的次要细节。

### 4. Skills 对齐与诚实边界 (Skills Alignment & Honest Gaps)
- **保留/前置的关键词**：JD 点名且 `content/master/skills.md` 有扎实证据支撑的工具、语言与工作流（含默认保留的 AI 辅助工程能力项）。
- **明确不写的诚实缺口（Honest Gaps）**：JD 提到但候选人未验证或未掌握的工具/技术，明确标注“不写入简历 Skills，若求职信或面试涉及则以相邻能力切入”，严禁硬蹭关键词。

### 5. 求职信五段式规划 (Five-Paragraph Cover Letter Plan)
- **第 1 段（钩子开头）**：为什么是这家公司、这个团队或这个具体业务场景？
- **第 2 段（精选简历证明）**：挑哪 1–2 个最硬核的交付事实证明能接住工作（避免复述整份简历）？
- **第 3 段（公司/岗位洞察与动机）**：对 JD 中具体工作方式、上下游协作或技术挑战的观察与判断。
- **第 4 段（前瞻执行计划，必填）**：入职头几周打算如何切入、优先摸清或解决什么具体问题？
- **第 5 段（Logistics 与结尾）**：可入职时间、持续时长、地点/语言等确认项 + 非套话的交流邀约。

### 6. 开放问题与面试风险 (Open Questions & Interview Risks)
- 哪些资质/时间线/技术深度可能在筛简历或一面时被追问？如何基于 `content/master/` 准备可辩护的回答？
