# Job Target Packages (`targets/`)

每个真实申请岗位对应 `targets/<slug>/` 下一个独立目录，包含标准**四件套**：

| 文件 | 职责 |
|---|---|
| `metadata.yaml` | 机器可读契约（唯一编号 `internal_id`、公司、岗位、地点、招聘链接、状态、简历/求职信入口路径） |
| `jd.md` | 已核实的结构化英文 JD（若原帖为非英语，忠实翻译为英文并在头部标注原始语言） |
| `notes.md` | 岗位调研、雇主 Job ID、物流条件（起止时间/每周天数/论文要求）与初步匹配信号 |
| `tailoring.md` | 该岗位的专属预写方案（6 大模块：核心痛点与 Profile 方向、板块取舍、经历 bullet 短名单、Skills 对齐与诚实缺口、求职信五段提纲、开放问题与面试风险） |

> **隐私边界**：仓库中仅提交 `targets/example-company-role/` 作为 Schema 与结构模板；所有真实岗位目录 `targets/<slug>/` 均被 `.gitignore` 忽略，不会上传到远程 Git 仓库。

---

## 一、`metadata.yaml` 字段契约

由 `python3 scripts/workspace.py check` 自动校验：

| 字段 | 类型与约束 |
|---|---|
| `internal_id` | 引号包裹的三位数字字符串 `"001"`–`"999"`，全局唯一，按入仓先后取当前最大编号 `+1`，缺号绝不回收（`"000"` 仅限 `example-company-role` 模板） |
| `company` | 非空字符串；仅登记 URL 尚未核实时写 `"待核实"` |
| `role` | 非空字符串；仅登记 URL 尚未核实时写 `"待核实"` |
| `location` | 非空字符串，或包含非空字符串 `display` 的字典 |
| `source_url`（或 `source`） | 合法的 `http://` 或 `https://` 招聘来源链接 |
| `date_saved`（可选） | 首次入仓日期 `YYYY-MM-DD` |
| `status` | 枚举值：`draft` / `open` / `applied` / `interviewing` / `offer` / `rejected` / `closed`，必须与 `PROJECT_STATUS.md` 该行的「进展」列匹配 |
| `resume_version` | 必须存在；未创建定向简历时填 `""`，创建后填 `versions/cv/targeted/{id}-resume-<company>-<role>-<location>.tex` |
| `cover_letter_version` | 必须存在；未创建定向求职信时填 `""`，创建后填 `versions/letter/targeted/{id}-cover-letter-<short-slug>.tex` |

---

## 二、快速登记新岗位命令

```bash
# 1. 预览将要分配的 internal_id、metadata.yaml 与 PROJECT_STATUS.md 新增行（不写盘）
python3 scripts/workspace.py init --url 'https://example.com/jobs/12345' --slug example-corp-data-scientist-amsterdam --company 'Example Corp' --role 'Data Scientist Intern' --location 'Amsterdam, Netherlands'

# 2. 确认无误后加 --write 正式创建四件套并插入 PROJECT_STATUS.md
python3 scripts/workspace.py init --url 'https://example.com/jobs/12345' --slug example-corp-data-scientist-amsterdam --company 'Example Corp' --role 'Data Scientist Intern' --location 'Amsterdam, Netherlands' --write
```

---

## 三、关联标准化 Skills 与规则

- **Step 1（岗位链接 / JD 进项目）**：`.agent/skills/job-intake/SKILL.md`、`.agent/rules/intake.md`
- **Step 2（岗位预写 `tailoring.md`）**：`.agent/skills/job-prewrite/SKILL.md`、`.agent/rules/tailoring.md`
- **Step 3（定向简历制作与 QA）**：`.agent/skills/targeted-resume/SKILL.md`、`.agent/rules/content.md`
- **Step 4（定向求职信制作与 QA）**：`.agent/skills/targeted-cover-letter/SKILL.md`、`.agent/rules/content.md`
- **Step 5（发布快照与更新进展）**：`.agent/skills/status-and-publish/SKILL.md`、`.agent/rules/status.md`
