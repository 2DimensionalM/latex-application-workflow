# 通用 CV Baseline（Universal Baseline）规范

## 一、定义与定位

**通用基线简历（Universal CV Baseline）** 是本工作区唯一的跨市场 CV 父本。它面向候选人当前主力目标方向，是在读取具体岗位 JD、完成 `tailoring.md` 预写并制作定向稿（Targeted Resume）之前的共同一页起点。

它与各层的边界如下：

- **`content/master/`（完整事实源 SoT）**：保存完整、可核实的候选人经历、分阶段技术细节、成绩、证书状态与候选 bullet 池；不因“一页限制”删减事实。
- **`baseline`（人工策展一页视图）**：从 `content/master/` 中筛选出的均衡、无特定公司偏向的一页简历父本。
- **`targets/<slug>/tailoring.md`（单岗决策层）**：决定针对某一具体 JD 如何从 `baseline` 与 `content/master/` 中取舍、重排 bullet 和对齐关键词。
- **`targeted`（单岗交付稿）**：承担最终 JD 对齐；一次性岗位关键词或定制改写绝不回写 `baseline`。

## 二、为什么只维护唯一一份通用 Baseline

1. **避免多分支同步灾难**：不为每家公司或细分行业新建 `baseline-<company>` 或 `baseline-<industry>`。
2. **极速定向分叉**：所有新岗位在完成 `tailoring.md` 预写后，直接以同一个稳定的一页结构为父本做手术式微调，而非从零排版。
3. **单向显式触发**：修改 `content/master/` 事实、刷新 `baseline`、制作单岗 `targeted` 稿是三种彼此独立的动作，互不隐式覆盖。

## 三、关联文件路径

| 角色 | 路径 |
|---|---|
| 完整事实源 | `content/master/*.md`（首次上手通过 `python3 scripts/workspace.py bootstrap` 从 `*.example.md` 生成） |
| 基线正文片段 | `src/sections/baseline-universal.tex` |
| 基线编译入口 | `versions/cv/baseline/resume-baseline.tex` |
| 隔离审阅产物 | `output/review/resume-baseline/resume-baseline.pdf` |
| 正式发布基线 | `output/cv/baseline/resume-baseline.pdf` |

## 四、构建、验证与刷新流程

```bash
# 1. 隔离构建并运行一页 / 留白 / 日志 QA
./scripts/build.sh baseline

# 2. 使用公开占位页眉测试构建（CI / 模板验证）
./scripts/build.sh baseline --public-header

# 3. 人工目视确认版面无误后，发布/刷新当前通用基线快照
./scripts/build.sh baseline --publish
```

### 何时刷新 Baseline

- **仅在用户明确提出“刷新 / 更新通用 baseline”时执行**。
- 刷新步骤：
  1. 完整对照 `content/master/*.md` 最新事实与时间线状态（如在职阶段、在读课程、项目状态）。
  2. 更新 `src/sections/baseline-universal.tex`，遵循 `docs/rules/content.md` 的一页规则、倒序时间线与宏排版约束。
  3. 运行 `./scripts/build.sh baseline` 并用 `pdftoppm` 渲染图片检查单页填充度（正文底端 ≥ 80% 页高，无明显页底留白）。
  4. 更新本文件下方的刷新记录。
- **不回写历史**：刷新 `baseline` 不会自动重编译任何 `targeted` 简历，也不会修改已投递岗位的历史快照。

## 五、所有新岗位如何从 Baseline 分叉

1. 先按 `.cursor/skills/job-intake/SKILL.md` 完成岗位登记（`jd.md`、`notes.md`、`metadata.yaml`）。
2. 按 `.cursor/skills/job-prewrite/SKILL.md` 完成 `targets/<slug>/tailoring.md` 预写。
3. 按 `.cursor/skills/targeted-resume/SKILL.md`：
   - 将 `src/sections/baseline-universal.tex` 复制为 `src/sections/targeted-<short-slug>.tex`；
   - 创建入口 `versions/cv/targeted/{id}-resume-<company>-<role>-<location>.tex`；
   - 在 `targets/<slug>/metadata.yaml` 登记 `resume_version`；
   - 根据 `tailoring.md` 调整 Profile、Skills、各段经历 bullet 及 Education 详略。

## 六、关于求职信（Cover Letter）

求职信必须阐述具体公司、具体团队与具体岗位的申请动机及入职切入计划（见 `docs/rules/content.md` 五段式结构），因此**不设立跨公司通用的 Cover Letter Baseline**。每封求职信均在完成 `tailoring.md` 预写后，直接创建 `src/sections/letters/targeted-<short-slug>-letter.tex` 与 `versions/letter/targeted/{id}-cover-letter-<short-slug>.tex`。

## 七、当前 Baseline 刷新记录

- **Last refreshed:** YYYY-MM-DD（Fork 后首次配置个人基线时更新此处）
- **Included context:** 记录本次纳入 `baseline-universal.tex` 的核心经历阶段、最新课程/项目与技能基线。
- **Boundary notes:** 记录明确排除在通用一页视图之外或待核实（`Need verification`）的边界事项。
