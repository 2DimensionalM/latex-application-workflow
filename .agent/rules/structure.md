# LaTeX 结构、版本与命名规范 (LaTeX Structure & Versioning Rules)

> 适用场景：新增或修改 LaTeX 入口（`versions/`）、正文片段（`src/sections/`）、公共样式与宏（`src/preamble*.tex`、`src/macros*.tex`）。

---

## 一、三层解耦架构

1. **样式与宏层（`src/preamble.tex`、`src/macros.tex`、`src/preamble-letter.tex`、`src/macros-letter.tex`）**：
   - 统一控制纸张边距、字体编码、段落间距与结构化排版命令：
     - `\cvexpblock{<Company>}{<Role Title>}{<Location>}{<Dates>}`：两栏对齐的经历标题块；
     - `\cveduhead{<School>}{<Dates>}`、`\cvedusub{<Degree>}{<Location>}`、`\cvedunote{<Notes>}`：教育背景块；
     - `\cvskillblock{<Category:>}{<Skill items>}`：技能分类块；
     - `\LetterSubject{<Subject line>}`：求职信主题行。
   - 修改共享样式或宏会影响多个目标，修改后须运行 `python3 scripts/workspace.py affected <path>` 评估影响范围。
2. **正文片段层（`src/sections/` 与 `src/sections/letters/`）**：
   - `src/sections/header.tex`：统一页眉入口，自动检测本地是否存在 `src/sections/header.private.tex`，不存在则回退到 `src/sections/header.template.tex`。
   - `src/sections/baseline-universal.tex`：唯一跨市场通用 CV 基线正文。
   - `src/sections/targeted-<short-slug>.tex`：单岗定制简历正文片段。
   - `src/sections/letters/targeted-<short-slug>-letter.tex`：单岗定制求职信正文片段。
3. **编译入口层（`versions/cv/{base,baseline,targeted}/` 与 `versions/letter/{baseline,targeted}/`）**：
   - 轻量级壳文件（设置 `\documentclass`、加载 `preamble` 与 `macros`、`\input` 对应 section）。
   - 编译时的 `JOBNAME` 与输出 PDF 文件名**自动由入口文件名 stem 派生**，绝不维护两套名字。

---

## 二、版本分类与命名铁律

| 版本层级 | 入口路径模式 | 标准输出 PDF 路径（`--publish` 时） | 说明 |
|---|---|---|---|
| **Base 演示模板** | `versions/cv/base/resume-base.tex` | `output/cv/base/resume-base.pdf` | 最小结构示例，非投递稿 |
| **Universal Baseline** | `versions/cv/baseline/resume-baseline.tex` | `output/cv/baseline/resume-baseline.pdf` | 唯一跨市场 CV 父本（见 `RESUME_BASELINE.md`） |
| **Targeted 简历** | `versions/cv/targeted/{id}-resume-<company>-<role>-<location>.tex` | `output/cv/targeted/{id}-resume-<company>-<role>-<location>.pdf` | 单岗定制简历，`{id}` 为三位 `internal_id` |
| **Targeted 求职信** | `versions/letter/targeted/{id}-cover-letter-<short-slug>.tex` | `output/cover-letters/pdf/targeted/{id}-cover-letter-<short-slug>.pdf` | 单岗定制求职信，`{id}` 为三位 `internal_id` |

### 命名一致性要求
- 所有入口文件名仅使用小写字母、数字和连字符（`[a-z0-9-]+.tex`）。
- 定向入口文件名必须以该岗 `metadata.yaml` 中的 `{internal_id}-resume-` 或 `{internal_id}-cover-letter-` 开头，`workspace.py check` 会强制校验前缀一致性。
- `src/sections/targeted-*.tex` 的内部短名可以比外部 PDF 文件名更简短，但入口文件中的 `\input{sections/...}` 必须真实存在且可被依赖分析器解析。
