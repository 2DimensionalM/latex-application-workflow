---
name: status-and-publish
description: Publish verified resume and cover letter PDF snapshots and synchronize application status across metadata.yaml and PROJECT_STATUS.md (发布成品快照与更新求职进展). Use when the user approves materials for publishing ("发布PDF", "准备投递") or reports application progress such as applied, OA, interview, follow-up documents, offer, rejected, or closed ("已投递", "一面", "已拒", "已下架", "更新状态").
---

# Step 5: Publishing Snapshots & Synchronizing `PROJECT_STATUS.md`

## When to Use

Trigger this skill when:
1. **Publishing approved materials (`--publish`)**: Moving a visually verified resume and/or cover letter from `output/review/` into the snapshot directories `output/cv/targeted/` and `output/cover-letters/pdf/targeted/` and linking them in `PROJECT_STATUS.md`.
2. **Updating application progress**: Recording a real status transition (`已投递`, `一面`, `二面`, `补材料`, `已拿 offer`, `已拒`, `已下架`) in `targets/<slug>/metadata.yaml` and `PROJECT_STATUS.md`.

Read `docs/rules/status.md`, `docs/rules/build.md`, and `scripts/README.md`.

---

## Workflow Checklist

```markdown
Task Progress:
- [ ] Step 1: (If publishing) Run `./scripts/build.sh resume:<id> --publish` and/or `letter:<id> --publish`
- [ ] Step 2: Update `targets/<slug>/metadata.yaml` (`status`, `resume_version`, `cover_letter_version`)
- [ ] Step 3: Update the corresponding row in `PROJECT_STATUS.md` (links & `进展` column)
- [ ] Step 4: Move the row in `PROJECT_STATUS.md` to its correct 3-tier status group
- [ ] Step 5: (If a real application event occurred) Prepend a dated row (`YYYY-MM-DD`) at the top of `## 历史动作（带日期）`
- [ ] Step 6: Run `python3 scripts/workspace.py check --require-pdfs` and `python3 scripts/privacy_check.py`
```

---

## Mode A: Publishing Approved Materials (`--publish`)

1. Publish the verified targets (requires real/template header without `--public-header` and 0 QA errors):
   ```bash
   ./scripts/build.sh resume:<id> --publish
   ./scripts/build.sh letter:<id> --publish
   ```
   - Published PDFs are written to:
     - `output/cv/targeted/{id}-resume-<company>-<role>-<location>.pdf`
     - `output/cover-letters/pdf/targeted/{id}-cover-letter-<short-slug>.pdf`
   - **Snapshot protection**: `--publish` refuses to overwrite any existing targeted PDF snapshot.
2. In `PROJECT_STATUS.md`, update the row's `简历` and `求职信` cells:
   - `[简历](output/cv/targeted/{id}-resume-<company>-<role>-<location>.pdf)`
   - `[求职信](output/cover-letters/pdf/targeted/{id}-cover-letter-<short-slug>.pdf)`
3. Set `进展` to `待投递` (`Ready to Apply`). **Never** mark a role as `已投递` (`applied`) merely because its PDFs were built or published!

---

## Mode B: Recording Application Events & Status Transitions

When the user confirms a real event (e.g., submitted application, completed OA, interview invite, rejection, or job closed):

1. **Update `targets/<slug>/metadata.yaml` `status`**:
   - `draft` / `open` → `待核实` / `待预写` / `写简历` / `写求职信` / `审核简历` / `审核求职信` / `待投递`
   - `applied` → `已投递` / `补材料`
   - `interviewing` → `一面` / `二面` / `终面` / `补材料`
   - `offer` → `已拿 offer`
   - `rejected` → `已拒`
   - `closed` → `已下架`
2. **Update & Re-order the Main Table Row in `PROJECT_STATUS.md`**:
   - Update the `进展` cell to the new status label.
   - **Move the row into the matching group** (never change the status text while leaving the row stranded in its old group!):
     - **Group 1 (Top)**: Active preparation & material drafting (`待核实`, `待预写`, `写简历`, `写求职信`, `审核简历`, `审核求职信`, `待投递`)
     - **Group 2 (Middle)**: Submitted & active pipeline (`已投递`, `一面`, `二面`, `终面`, `补材料`)
     - **Group 3 (Bottom)**: Terminal states (`已拿 offer`, `已拒`, `已下架`)
3. **Prepend to the History Table (`## 历史动作（带日期）`)**:
   - Insert a new row **immediately below the History table header** (newest events at the top):
     ```markdown
     | YYYY-MM-DD | <Company> | <id>（<Employer Job ID if any>，<Role Title>） | <Event Label> |
     ```
4. **Verify**:
   ```bash
   python3 scripts/workspace.py check --require-pdfs
   ```
