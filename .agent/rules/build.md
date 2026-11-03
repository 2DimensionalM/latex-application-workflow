# 构建、自动 QA 与发布规范 (Build, QA & Publishing Rules)

> 适用场景：编译简历/求职信、执行单页与篇幅高度 QA、增量回归测试、首次发布投递快照。详细命令参数见 `scripts/README.md`。

---

## 一、默认隔离构建（保护已发布快照）

- 所有常规构建命令（`./scripts/build.sh <target>` 或 `python3 scripts/workspace.py build <target>`）**默认只写入隔离审阅目录**：
  - `output/review/<JOBNAME>/<JOBNAME>.pdf`
  - `output/review/<JOBNAME>/build.log`
  - `output/review/<JOBNAME>/latex.log`
  - `output/review/<JOBNAME>/qa.json`
- 每次编译均在全新的临时目录生成 `.aux`/`.out` 中间件，并在编译前清理旧的 review 产物，杜绝“编译失败却误把上次旧 PDF 当成新结果”的隐患。
- 编译默认启用 `-no-shell-escape -interaction=nonstopmode -halt-on-error`。
- 支持 `--public-header` 参数：在临时工作树中强制使用公开占位页眉 `header.template.tex` 编译，用于 CI 测试或不含私有页眉的验证。

---

## 二、自动 QA 与人工视觉复核双闭环

每次构建完成后，`workspace.py` 会自动调用 `qa()` 分析生成的 PDF 与 `latex.log`，输出 `qa.json`：

1. **硬性错误（`errors`，导致退出码非 0 且禁止 `--publish`）**：
   - 页数不为 1 页（`expected 1 page, got N`）；
   - 求职信正文（`Dear ...` 至 `Sincerely,` / `Kind regards,` / `Best regards,` 之间）底端位置低于页面高度的 **60%**（`letter body ends above 60% page-height line`）；
   - `latex.log` 存在 LaTeX Error / Emergency stop。
2. **审阅警告（`warnings`，提示人工复核）**：
   - 简历正文末行低于页面高度的 **80%**（提示可能存在明显页底留白，需按 `.agent/rules/content.md` 执行回补）；
   - 求职信未能识别标准称呼/落款边界（需人工目视测量 60% 高度）；
   - `latex.log` 存在 `Overfull \hbox` / `Underfull \vbox` 警告。
3. **强制图片目视检查**：
   - 自动 QA 通过后，Agent 仍须使用 `pdftoppm -png -r 150` 将 PDF 渲染为 PNG 并用 Read 工具目视检查版面（确认无文字裁切、无异常间距、无页底大块留白）。

---

## 三、正式发布（`--publish`）与快照防覆盖保护

- 当材料通过自动 QA 与视觉检查、准备用于实际投递时，运行：
  ```bash
  ./scripts/build.sh resume:<id> --publish
  ./scripts/build.sh letter:<id> --publish
  ```
- **发布门禁**：
  - 若带有 `--public-header`、或 `qa.json` 存在任何 `errors`、或求职信边界未识别，脚本拒绝发布；
  - 对于所有 `targeted` 简历与求职信，若目标路径 `output/cv/targeted/<JOBNAME>.pdf` 或 `output/cover-letters/pdf/targeted/<JOBNAME>.pdf` **已存在**，脚本**拒绝覆盖**（保护历史投递快照）；
  - 仅 `baseline`（通用基线视图）在用户明确要求刷新时允许通过 `./scripts/build.sh baseline --publish` 原子替换。
