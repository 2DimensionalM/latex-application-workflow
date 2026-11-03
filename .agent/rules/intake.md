# 岗位链接与 JD 进项目规范 (Job URL & JD Intake Rules)

> 适用场景：用户提供一条或多条招聘页 URL（或原始 JD 文本），要求「进项目」「登记岗位」「抓取 JD」。对应标准化 Skill：`.agent/skills/job-intake/SKILL.md`。

---

## 一、触发与默认边界

- **触发条件**：用户提供招聘链接或 JD 文本要求进项目，且**尚未**明确要求立即撰写定向简历或求职信。
- **支持单轮批量登记**：若用户一次提供多条 URL，每个 URL 必须建立**独立**的 `targets/<slug>/` 目标包、分配**独立**的递增 `internal_id`、并在 `PROJECT_STATUS.md` 主表插入**独立**的一行。
- **默认停止边界**：仅完成目标包四件套初始化、JD 结构化归档、`notes.md` 初步记录与 `PROJECT_STATUS.md` 同步（进展设为 `待预写`）。除非用户同轮明确要求，否则**不直接跳过预写去生成 LaTeX 或编译 PDF**。

---

## 二、每岗必做标准步骤

1. **分配唯一编号与初始化目录**：
   - 使用 `python3 scripts/workspace.py init --url '<URL>' --slug <company-role-location> --company '<Company>' --role '<Role>' --location '<Location>' --write` 初始化（或先不加 `--write` 预览）。
   - `internal_id` 自动取当前最大三位编号 `+1`（`"001"` 起，只增不改，缺号不回收）。
2. **抓取与核实 JD 正文**：
   - 从招聘页提取：职位名称、公司、地点、工作职责、硬性/加分要求、实习/全职条件（起止时间、每周天数、是否要求在读/毕业论文等）、雇主 Job ID（若有）、发布/截止日期。
   - **严禁虚构**页面上不存在的要求或福利。
3. **交叉核实岗位开放状态（防误判 `closed`）**：
   - 若页面明示下架/招满（`no longer available` / `job is closed`），还须检查页面内嵌 JSON-LD（`application/ld+json` 的 `JobPosting`）或 ATS 状态对象（如 Workday / Phenom 的 `jobDetail`）是否仍包含有效 `applyUrl` 与在招正文。
   - 确认已关闭时：`metadata.yaml` 设 `status: "closed"`，`PROJECT_STATUS.md` 进展设 `已下架`，仍保留目标包归档，不做后续预写与 LaTeX。
   - 确认开放时：`metadata.yaml` 设 `status: "open"`，`PROJECT_STATUS.md` 进展设 `待预写`。
4. **编写结构化 `targets/<slug>/jd.md`**：
   - 剔除页脚营销套话、年龄验证门、Cookie 横幅与无关推荐链接。
   - 文件顶部保留元信息（来源 URL、抓取日期、原始语言、雇主 Job ID）。
5. **编写 `targets/<slug>/notes.md`**：
   - 记录抓取日期、内部编号、雇主 Job ID、物流待核实项（如到岗时间、工作语言、签证/学籍要求）及初步匹配度信号（Fit Signals）。
6. **保持 `targets/<slug>/tailoring.md` 占位或待预写状态**：
   - 仅登记 URL 阶段保留结构化大纲占位，`resume_version` 与 `cover_letter_version` 在 `metadata.yaml` 中保持空字符串 `""`。
7. **同步 `PROJECT_STATUS.md` 并运行校验**：
   - 确认主表新增行位于第一组（进行中/待预写组），`JD` 列链接为 `[JD](targets/<slug>/jd.md)`，简历与求职信列为 `—`。
   - 运行 `python3 scripts/workspace.py check` 确保 0 错误。

---

## 三、常见招聘站点与 ATS 抓取策略

| 站点 / ATS 类型 | 常见问题 | 推荐提取方式 |
|---|---|---|
| **官方结构化 Careers** | 动态渲染或含大量导航噪音 | 优先读取页面内嵌 `application/ld+json`（`@type: JobPosting`）或主正文区域 |
| **Workday (`*.myworkdayjobs.com`)** | 纯前端渲染导致普通抓取正文为空 | 使用 `curl -sL` 提取 `<meta property="og:title">`、`<meta property="og:description">` 或内嵌 JSON 描述 |
| **Greenhouse / Lever / Ashby** | 聚合链接带追踪参数 | 抓取主帖正文或 `og:description`；保留原始 `source_url` |
| **Phenom People** | 外部缓存偶发误报 filled | 解析 HTML 内 `application/ld+json` 或 `phApp.ddo.jobDetail` 核实真实在招状态与 Workday `applyUrl` |
| **年龄门 / 地区门站点（如快消/酒企）** | 普通抓取被重定向至年龄验证页 | 使用 `curl` 获取原始 HTML 中的内嵌 JSON-LD 或职位描述元数据 |

---

## 四、`jd.md` 语言规范（与英文简历工作流对齐）

- **默认使用英文编写 `jd.md` 正文**：便于后续在 `tailoring.md` 预写、英文简历 bullet 映射和求职信撰写时直接对照。
- **非英语招聘帖（如荷兰语、德语、法语等）**：
  - 将 JD 正文**忠实翻译为英文**写入 `jd.md`，不增删硬性要求；
  - 在 `jd.md` 顶部注明：`Original posting language: <Language>`、`Source URL` 与 `Captured date`；
  - 可在 `metadata.yaml` 中补充 `posting_language: "nl"`（或对应语言代码）与 `jd_language: "en"`；
  - 保留专有工具名（SQL、Power BI、Python）、日期、金额（€/$）与地点原名；当地学制或法规专有词首次出现时可加英文括号释义（例如 `WO degree (research university level)`）。
