---
name: status-and-publish
description: Publish verified resume and cover letter PDF snapshots and synchronize application status across metadata.yaml and PROJECT_STATUS.md. Use when the user approves materials for publishing or reports application progress such as applied, OA, interview, follow-up documents, offer, rejected, or closed.
---

# Stage 5: Publishing Snapshots & Synchronizing `PROJECT_STATUS.md`

## When to Use

Trigger this skill when:
1. **Publishing approved materials (`--publish`)**: Moving a visually verified resume and/or cover letter from `output/review/` into the snapshot directories `output/cv/targeted/` and `output/cover-letters/pdf/targeted/` and linking them in `PROJECT_STATUS.md`.
2. **Updating application progress**: Recording a real status transition (`Applied`, `OA`, `Round 1`, `Round 2`, `Follow-up Docs`, `Offer`, `Rejected`, `Closed`) in `targets/<slug>/metadata.yaml` and `PROJECT_STATUS.md`.

Read `.agent/rules/status.md`, `.agent/rules/build.md`, and `scripts/README.md`.

---

## Workflow Checklist

```markdown
Task Progress:
- [ ] Step 1: (If publishing) Run `./scripts/build.sh resume:<id> --publish` and/or `letter:<id> --publish`
- [ ] Step 2: Update `targets/<slug>/metadata.yaml` (`status`, `resume_version`, `cover_letter_version`)
- [ ] Step 3: Update the corresponding row in `PROJECT_STATUS.md` (links & `Status` column)
- [ ] Step 4: Move the row in `PROJECT_STATUS.md` to its correct 3-tier status group
- [ ] Step 5: (If a real application event occurred) Prepend a dated row (`YYYY-MM-DD`) at the top of `## Activity History`
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
2. In `PROJECT_STATUS.md`, update the row's `Resume` and `Cover Letter` cells:
   - `[Resume](output/cv/targeted/{id}-resume-<company>-<role>-<location>.pdf)`
   - `[Cover Letter](output/cover-letters/pdf/targeted/{id}-cover-letter-<short-slug>.pdf)`
3. Set `Status` to `Ready to Apply`. **Never** mark a role as `Applied` (`applied`) merely because its PDFs were built or published!

---

## Mode B: Recording Application Events & Status Transitions

When the user confirms a real event (e.g., submitted application, completed OA, interview invite, rejection, or job closed):

1. **Update `targets/<slug>/metadata.yaml` `status`**:
   - `draft` / `open` -> `Pending Verification` / `Pending Pre-write` / `Drafting Resume` / `Drafting Letter` / `Reviewing Resume` / `Reviewing Letter` / `Ready to Apply`
   - `applied` -> `Applied` / `Follow-up Docs`
   - `interviewing` -> `OA` / `Interview` / `Round 1` / `Round 2` / `Final Round` / `Follow-up Docs`
   - `offer` -> `Offer`
   - `rejected` -> `Rejected`
   - `closed` -> `Closed`
2. **Update & Re-order the Main Table Row in `PROJECT_STATUS.md`**:
   - Update the `Status` cell to the new status label.
   - **Move the row into the matching group** (never change the status text while leaving the row stranded in its old group!):
     - **Group 1 (Top)**: Active preparation & material drafting (`Pending Verification`, `Pending Pre-write`, `Drafting Resume`, `Drafting Letter`, `Reviewing Resume`, `Reviewing Letter`, `Ready to Apply`)
     - **Group 2 (Middle)**: Submitted & active pipeline (`Applied`, `OA`, `Interview`, `Round 1`, `Round 2`, `Final Round`, `Follow-up Docs`)
     - **Group 3 (Bottom)**: Terminal states (`Offer`, `Rejected`, `Closed`)
3. **Prepend to the Activity History Table (`## Activity History (Dated Events)`)**:
   - Insert a new row **immediately below the History table header** (newest events at the top):
     ```markdown
     | YYYY-MM-DD | <Company> | <id> (<Employer Job ID if any>, <Role Title>) | <Event Label> |
     ```
4. **Verify**:
   ```bash
   python3 scripts/workspace.py check --require-pdfs
   ```
