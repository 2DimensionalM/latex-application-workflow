# Build, Automated QA & Publishing Rules (`build.md`)

> Applicable when compiling resumes or cover letters, running single-page and density QA, performing incremental dependency builds, or publishing final PDF snapshots. For full CLI reference, see `scripts/README.md`.

---

## 1. Isolated Review Builds by Default (Snapshot Protection)

- All standard build commands (`./scripts/build.sh <target>` or `python3 scripts/workspace.py build <target>`) write **exclusively to isolated review directories**:
  - `output/review/<JOBNAME>/<JOBNAME>.pdf`
  - `output/review/<JOBNAME>/build.log`
  - `output/review/<JOBNAME>/latex.log`
  - `output/review/<JOBNAME>/qa.json`
- Every compilation uses a fresh temporary directory for `.aux`/`.out` intermediates and clears stale review outputs beforehand, ensuring a failed compile can never leave behind a stale PDF.
- Compilations run with `-no-shell-escape -interaction=nonstopmode -halt-on-error`.
- Pass `--public-header` to compile inside a temporary staging tree using `src/sections/header.template.tex` (for CI or template verification without `header.private.tex`).

---

## 2. Automated PDF/Log QA + Visual Inspection Loop

After every build, `workspace.py` runs `qa()` on the generated PDF and `latex.log` and writes `qa.json`:

1. **Hard Errors (`errors` -> non-zero exit code & blocks `--publish`)**:
   - Page count is not equal to 1 (`expected 1 page, got N`);
   - Cover letter body (between `Dear ...` and `Sincerely,` / `Kind regards,` / `Best regards,`) ends above **60% of page height** (`letter body ends above 60% page-height line`);
   - `latex.log` contains a LaTeX Error or Emergency stop.
2. **Review Warnings (`warnings` -> requires human/visual check)**:
   - Resume content ends above **80% of page height** (signals likely bottom whitespace; backfill per `.agent/rules/content.md`);
   - Cover letter greeting/sign-off boundaries could not be parsed automatically;
   - `latex.log` reports `Overfull \hbox` or `Underfull \vbox` warnings.
3. **Mandatory Visual Inspection**:
   - Even when `qa.json` reports 0 errors, render the PDF to PNG via `pdftoppm -png -r 150` and inspect the image with the Read tool to verify visual balance, margins, and line wraps.

---

## 3. Publishing Snapshots (`--publish`) & Overwrite Protection

- Once a targeted document passes both automated QA and visual inspection, publish it via:
  ```bash
  ./scripts/build.sh resume:<id> --publish
  ./scripts/build.sh letter:<id> --publish
  ```
- **Publishing Guardrails**:
  - `--publish` is rejected if `--public-header` is active, if `qa.json` contains any `errors`, or if cover letter boundaries are unrecognized.
  - For all `targeted` resumes and cover letters, if the destination file (`output/cv/targeted/<JOBNAME>.pdf` or `output/cover-letters/pdf/targeted/<JOBNAME>.pdf`) **already exists**, `--publish` **refuses to overwrite it** to protect historical application snapshots.
  - Only `baseline` (`versions/cv/baseline/resume-baseline.tex`) supports atomic replacement via `./scripts/build.sh baseline --publish` when explicitly refreshing the universal baseline.
