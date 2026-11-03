# Application Status & Activity Tracker (`PROJECT_STATUS.md`)

This file maintains two human-editable tables:
1. **Application Pipeline (Current Snapshot)**: One row per real target package under `targets/<slug>/`.
2. **Activity History (Dated Events)**: Reverse-chronological log of verified application events (applied, OA, interviews, follow-up documents, offer, rejection, or job closed), with the newest event placed at the top.

For synchronization rules with `targets/<slug>/metadata.yaml`, the 3-tier status grouping order, ID allocation invariants, and update procedures, see **[`.agent/rules/status.md`](.agent/rules/status.md)** and **[`.agent/skills/status-and-publish/SKILL.md`](.agent/skills/status-and-publish/SKILL.md)**.

---

## Standard `Status` Labels (Mapped to `metadata.yaml` `status`)

| Preparation (`draft` / `open`) | Material Drafting (`draft` / `open`) | Review & Ready (`draft` / `open`) | Active Pipeline (`applied` / `interviewing`) | Terminal Outcomes (`offer` / `rejected` / `closed`) |
|---|---|---|---|---|
| `Pending Verification` | `Drafting Resume` | `Reviewing Resume` | `Applied` | `Offer` |
| `Pending Pre-write` | `Drafting Letter` | `Reviewing Letter` | `OA` / `Interview` / `Round 1` / `Round 2` / `Final Round` | `Rejected` |
| | | `Ready to Apply` | `Follow-up Docs` | `Closed` |

---

## Application Pipeline (Current Snapshot)

| ID | Company | Role | Location | Posting | JD | Status | Resume | Cover Letter |
|------|------|------|--------|--------|-----|------|----------|------------|

---

## Activity History (Dated Events)

| Date | Company | Role (or ID) | Event |
|------|------|----------------|------|

---

## Row Templates (Inserted via `workspace.py init` or Manual Edit)

**Application Pipeline (9 Columns):**

```markdown
| 001 | Example Corp | Data & AI Engineer Intern (REQ-1001) | Amsterdam, Netherlands | [Link](https://example.com/jobs/1001) | [JD](targets/example-corp-data-ai-intern-amsterdam/jd.md) | Pending Pre-write | — | — |
```

**Activity History (4 Columns — insert immediately below the Activity History header):**

```markdown
| 2026-11-03 | Example Corp | 001 (REQ-1001, Data & AI Engineer Intern) | Applied |
```
