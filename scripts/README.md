# Scripts & Automation Harness (`scripts/`)

本目录包含 `latex-application-workflow` 的核心自动化校验、岗位初始化、隔离构建、PDF 质量门禁（QA）与隐私检查脚本。

---

## 一、环境准备与首次初始化（Onboarding）

需要 Python 3.10+ 与 TeX Live / TinyTeX（含 `pdflatex`；推荐安装 `poppler` 以使用 `pdftoppm` 渲染图片复核）。

```bash
# 1. 创建虚拟环境并安装依赖
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt

# 2. 初始化本地私有文件（从 *.example.md 和 header.private.tex.example 生成，不覆盖已有文件）
.venv/bin/python scripts/workspace.py bootstrap

# 3. 运行静态一致性检查与回归测试
.venv/bin/python scripts/workspace.py check
.venv/bin/python -m unittest discover -s scripts/tests -v
```

---

## 二、核心命令速查

### 1. 登记新岗位 URL（Step 1 — Intake）

```bash
# 预览分配的 internal_id、metadata.yaml 与 PROJECT_STATUS.md 新行（无写入）
.venv/bin/python scripts/workspace.py init \
  --url 'https://example.com/jobs/12345' \
  --slug example-corp-data-scientist-amsterdam \
  --company 'Example Corp' \
  --role 'Data Scientist Intern' \
  --location 'Amsterdam, Netherlands'

# 确认无误后加 --write 写入磁盘
.venv/bin/python scripts/workspace.py init \
  --url 'https://example.com/jobs/12345' \
  --slug example-corp-data-scientist-amsterdam \
  --company 'Example Corp' \
  --role 'Data Scientist Intern' \
  --location 'Amsterdam, Netherlands' \
  --write
```

### 2. 查看所有已注册构建目标

```bash
./scripts/build.sh --list
# 或
.venv/bin/python scripts/workspace.py list
```

### 3. 单目标隔离构建与自动 QA（Step 3 & Step 4）

```bash
# 构建通用 CV 基线
./scripts/build.sh baseline

# 使用公开占位页眉构建（CI / 模板测试）
./scripts/build.sh baseline --public-header
./scripts/build.sh letter-placeholder --public-header

# 构建指定岗位的定向简历或求职信（通过三位编号或 slug）
./scripts/build.sh resume:001
./scripts/build.sh letter:001
```

默认输出到 `output/review/<JOBNAME>/`（含 `<JOBNAME>.pdf`、`build.log`、`latex.log`、`qa.json`），**绝不覆盖**已发布的投递快照。

### 4. 独立运行 PDF 与日志 QA

```bash
.venv/bin/python scripts/workspace.py qa \
  output/review/resume-baseline/resume-baseline.pdf \
  --kind resume \
  --log output/review/resume-baseline/latex.log
```

- **Resume QA**：强制单页（1 Page），且当正文底端低于页面高度 80% 时发出留白提示（`warnings`）。
- **Cover Letter QA**：强制单页（1 Page），且自动识别 `Dear ...` 与 `Sincerely,` / `Kind regards,` / `Best regards,` 之间的正文，强制要求正文底端达到页面高度 **≥ 60%**（未达标记入 `errors`）。

### 5. 正式发布投递快照（Step 5 — Publish）

```bash
./scripts/build.sh resume:001 --publish
./scripts/build.sh letter:001 --publish
```

- 仅当未使用 `--public-header` 且 `qa.json` 无任何错误时才可发布。
- 定向简历发布至 `output/cv/targeted/`，定向求职信发布至 `output/cover-letters/pdf/targeted/`。
- **防覆盖保护**：若目标定向 PDF 已存在，`--publish` 会拒绝覆盖以保护历史投递快照；仅 `baseline` 支持原子刷新。

### 6. 依赖感知的增量构建（`affected`）

```bash
# 查看修改某文件会影响哪些构建目标
.venv/bin/python scripts/workspace.py affected src/macros.tex

# 直接构建受影响的目标
.venv/bin/python scripts/workspace.py affected src/sections/baseline-universal.tex --build --public-header
```

### 7. 隐私与安全门禁检查（每次 Commit / Push 前必跑）

```bash
.venv/bin/python scripts/privacy_check.py
```

自动拦截任何已跟踪或已暂存的私有母版文件（`content/master/*.md`）、私有页眉（`src/sections/header.private.tex`）、真实岗位目录（`targets/<slug>/`）、`cn-campus-2027/`、PDF 二进制产物，以及正文中的邮箱、电话号码、GitHub Token 或私钥。
