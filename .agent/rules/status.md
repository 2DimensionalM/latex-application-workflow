# `PROJECT_STATUS.md` Standardization & Synchronization Rules (`status.md`)

> Applicable when adding a new job target, linking published resume/cover letter PDFs, or updating application progress (applied, OA, interview, offer, rejected, closed). Associated skill: `.agent/skills/status-and-publish/SKILL.md`.

---

## 1. Role & Cleanliness Guardrails for `PROJECT_STATUS.md`

1. **Scope**: Root `PROJECT_STATUS.md` maintains exactly two human-editable tables:
   - **Application Pipeline (`## Application Pipeline (Current Snapshot)`)**: Strict **1-to-1** mapping with real target packages under `targets/<slug>/` (excluding the `example-company-role` template).
   - **Activity History (`## Activity History (Dated Events)`)**: Reverse-chronological log of verified application events (applied, OA, interviews, follow-up docs, offer, rejection, job closed).
2. **Forbidden in `PROJECT_STATUS.md`**:
   - Do not add a free-text `Notes` or `Remarks` column (put role nuances, logistics checks, and re-opening notes inside `targets/<slug>/notes.md` or `tailoring.md`).
   - Do not paste long rule explanations or batch change logs above the table.
   - Use clean link labels `Resume` and `Cover Letter` without appending `"PDF"` to column headers or link text.

---

## 2. Main Table Schema (9 Columns)

```markdown
| ID | Company | Role | Location | Posting | JD | Status | Resume | Cover Letter |
|---|---|---|---|---|---|---|---|---|
```

| Col # | Column Header | Contract & Validation Rule |
|---|---|---|
| 1 | `ID` | 3-digit zero-padded string (`001`–`999`), matching `internal_id` in `targets/<slug>/metadata.yaml` and targeted filename prefixes. Allocated sequentially (`max + 1`); **never renumbered or recycled**. |
| 2 | `Company` | Matches `company` in `metadata.yaml` (human-readable abbreviations allowed). |
| 3 | `Role` | Matches `role` in `metadata.yaml` (may append employer Job ID in parentheses, e.g., `(REQ-1001)`; escape literal pipes as `\|`). |
| 4 | `Location` | Matches `location` or `location.display` in `metadata.yaml`. |
| 5 | `Posting` | External link `[Link](https://...)` pointing to `source_url` or `source` in `metadata.yaml`. |
| 6 | `JD` | Workspace-relative link `[JD](targets/<slug>/jd.md)` opening the local structured English JD. |
| 7 | `Status` | Must belong to the allowed status label set for the target's `metadata.yaml` `status` value (see mapping table below). |
| 8 | `Resume` | After `--publish`, link `[Resume](output/cv/targeted/{id}-resume-....pdf)`; before publishing, use `—`. |
| 9 | `Cover Letter` | After `--publish`, link `[Cover Letter](output/cover-letters/pdf/targeted/{id}-cover-letter-....pdf)`; if none or unpublished, use `—`. |

---

## 3. `metadata.yaml` Status Enum & Main Table Status Mapping

`scripts/workspace.py check` enforces consistency between `metadata.yaml` `status` and the `Status` column in `PROJECT_STATUS.md`:

| `metadata.yaml` `status` | Allowed `PROJECT_STATUS.md` `Status` Labels | Row Sorting Group |
|---|---|---|
| `draft` | `Pending Verification`, `Pending Pre-write`, `Drafting Resume`, `Drafting Letter`, `Reviewing Resume`, `Reviewing Letter`, `Ready to Apply` | **Group 1 (Preparation & Drafting)** |
| `open` | `Pending Pre-write`, `Drafting Resume`, `Drafting Letter`, `Reviewing Resume`, `Reviewing Letter`, `Ready to Apply` | **Group 1 (Preparation & Drafting)** |
| `applied` | `Applied`, `Follow-up Docs` | **Group 2 (Submitted & Active Pipeline)** |
| `interviewing` | `OA`, `Interview`, `Round 1`, `Round 2`, `Final Round`, `Follow-up Docs` | **Group 2 (Submitted & Active Pipeline)** |
| `offer` | `Offer` | **Group 3 (Terminal Outcomes)** |
| `rejected` | `Rejected` | **Group 3 (Terminal Outcomes)** |
| `closed` | `Closed` | **Group 3 (Terminal Outcomes)** |

*(Bilingual compatibility: `workspace.py` also accepts the equivalent Chinese status labels when validating existing workspaces.)*

---

## 4. Three-Tier Row Grouping Order (Move Rows on Status Change)

Rows in the main table are **ordered by status group**, not by numerical `ID`:
1. **Group 1 (Top of table)**: Active preparation and material drafting (`Pending Verification`, `Pending Pre-write`, `Drafting Resume`, `Drafting Letter`, `Reviewing Resume`, `Reviewing Letter`, `Ready to Apply`);
2. **Group 2 (Middle of table)**: Submitted applications and active interviews (`Applied`, `OA`, `Interview`, `Round 1`, `Round 2`, `Final Round`, `Follow-up Docs`), with most recently submitted/updated rows near the top of the group;
3. **Group 3 (Bottom of table)**: Terminal states (`Offer`, `Rejected`, `Closed`) grouped together at the bottom, never mixed into Groups 1 or 2.

> **Mandatory Rule**: Whenever a target's status transitions across groups (e.g., from `Ready to Apply` to `Applied`, or from `Applied` to `Rejected`), **move the entire row to the target group in the same edit**. Never update the `Status` cell text while leaving the row in its old group position.

---

## 5. Activity History Table (4-Column Schema & Ordering)

```markdown
| Date | Company | Role (or ID) | Event |
|---|---|---|---|
| 2026-11-03 | Example Corp | 001 (REQ-1001, Data & AI Engineer Intern) | Applied |
```

- **What to record**: Only verified real-world application events (`Applied`, `Completed OA`, `Round 1 Interview`, `Round 2 Interview`, `Follow-up Docs Sent`, `Offer`, `Rejected`, `Closed`). Local LaTeX builds or pre-writing edits are not recorded in the history table.
- **Ordering**: **Prepend new events immediately below the table header** (strict reverse-chronological order, `YYYY-MM-DD`).
- **Consistency**: The latest event for a target in the history table must match its current `Status` in the main pipeline table above.
