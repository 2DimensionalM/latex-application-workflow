# Candidate Master Fact Layer (`content/master/`)

本目录是候选人事实与证据链的**唯一事实源（Single Source of Truth, SoT）**。

## 一、隐私与版本控制设计

- 仓库中**仅跟踪**本说明文件 `README.md` 与六个结构化示例模板 `*.example.md`。
- 你的真实个人信息文件（`profile.md`、`education.md`、`experience.md`、`projects.md`、`skills.md`、`certifications.md`）已被 `.gitignore` 忽略，并受 `scripts/privacy_check.py` 保护，**绝不会被提交或上传到远程 Git 仓库**。

## 二、快速初始化（Onboarding）

Fork 或克隆本仓库后，在仓库根目录运行：

```bash
python3 scripts/workspace.py bootstrap
```

该命令会自动将本目录下的 `*.example.md` 复制为对应的本地 `*.md` 文件（若本地已存在同名文件则自动跳过，不会覆盖你的数据），同时根据 `src/sections/header.private.tex.example` 创建本地私有页眉 `src/sections/header.private.tex`。

## 三、文件清单与职责

| 本地私有文件（Git 忽略） | 跟踪模板文件（Git 跟踪） | 维护内容 |
|---|---|---|
| `profile.md` | `profile.example.md` | 候选人基本定位、核心求职方向、可入职时间/地点/签证/语言等物流事实、不同投递方向的 Profile 候选句 |
| `education.md` | `education.example.md` | 学位、院校、时间线、GPA/核心课程成绩、毕业论文/Capstone 详情与可复用教育附注 |
| `experience.md` | `experience.example.md` | 实习与全职经历完整事实（含多阶段演进、本人 ownership 与上下游团队边界、系统上线生命周期、内部代号映射、`Need verification` 待核实项、候选 bullet 池） |
| `projects.md` | `projects.example.md` | 学术、个人或开源项目事实，以及与 `experience.md` / `education.md` 的重叠关系说明 |
| `skills.md` | `skills.example.md` | 有据可查的技能分类清单（编程语言、数据与工程栈、AI 辅助与 Agentic 工作流、领域与自然语言）及每项技能的证据来源 |
| `certifications.md` | `certifications.example.md` | 严格区分「已完成职业/行业认证」、「已完成课程/技能证书」与「在读未结业课程」 |

## 四、维护黄金法则（Agent 与人类共同遵守）

1. **只记事实，不写裁剪规则**：
   - 本目录只记录**真实发生过什么**、**做到什么程度**、**有哪些证据**。
   - 不要在本目录写“投递简历时省略某工具”、“一页放不下先删某段”等裁剪指令——跨岗通用裁剪规则维护在 `.agent/rules/content.md`，单岗取舍维护在 `targets/<slug>/tailoring.md`。
2. **不要因一页简历限制而删减母版事实**：
   - 对外简历只有一页，但 `content/master/` 应当保留完整的技术背景、历史阶段与候选 bullet，供不同方向的岗位随时提取。
3. **显式标注待核实项（`Need verification`）**：
   - 任何记不清的量化指标、历史系统名或算法库，在母版中标明 `Need verification`，核实前严禁写入对外简历或求职信。
4. **单向显式同步**：
   - 更新 `content/master/*.md` 不会自动改写 `src/sections/baseline-universal.tex` 或历史 `targeted` 简历；仅在明确需要刷新通用基线或撰写新岗位材料时读取本目录。
