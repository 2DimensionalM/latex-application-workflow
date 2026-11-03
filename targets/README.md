# Job Target Packages (`targets/`)

Every real job application lives in its own `targets/<slug>/` directory containing a standard **four-file quartet**:

| File | Responsibility |
|---|---|
| `metadata.yaml` | Machine-readable contract (`internal_id`, company, role, location, source URL, status, and resume/cover letter entry paths) |
| `jd.md` | Verified, structured English job description (if the original posting is in another language, translate faithfully into English and note the source language in the header) |
| `notes.md` | Company/team research, employer Job ID, logistics (start window, duration, days/week, thesis requirement), and initial fit signals |
| `tailoring.md` | Role-specific pre-writing plan covering the 6 mandatory modules (core JD signals & Profile angle, section trade-offs, experience bullet shortlist, skills alignment & honest gaps, 5-paragraph cover letter outline, open questions & interview risks) |

> **Privacy Boundary**: Only `targets/example-company-role/` and this `README.md` are tracked in Git. All real target packages (`targets/<slug>/`) are ignored by `.gitignore` and blocked by `scripts/privacy_check.py`.

---

## 1. `metadata.yaml` Schema Contract

Validated automatically by `python3 scripts/workspace.py check`:

| Field | Type & Validation Rule |
|---|---|
| `internal_id` | Quoted 3-digit string `"001"`–`"999"`, globally unique, allocated sequentially as `max + 1`, never recycled (`"000"` is reserved for `example-company-role`) |
| `company` | Non-empty string; defaults to `"Pending Verification"` during URL-only initialization |
| `role` | Non-empty string; defaults to `"Pending Verification"` during URL-only initialization |
| `location` | Non-empty string, or a mapping containing a non-empty string `display` |
| `source_url` (or `source`) | Valid `http://` or `https://` job posting URL |
| `date_saved` (optional) | ISO date `YYYY-MM-DD` when the target was first registered |
| `status` | Enum: `draft` / `open` / `applied` / `interviewing` / `offer` / `rejected` / `closed`; must match the row's `Status` cell in `PROJECT_STATUS.md` |
| `resume_version` | Required key; `""` before creation, or `versions/cv/targeted/{id}-resume-<company>-<role>-<location>.tex` |
| `cover_letter_version` | Required key; `""` before creation, or `versions/letter/targeted/{id}-cover-letter-<short-slug>.tex` |

---

## 2. Initializing a New Job Target

```bash
# 1. Preview allocated internal_id, metadata.yaml, and PROJECT_STATUS.md row (no disk writes)
python3 scripts/workspace.py init \
  --url 'https://example.com/jobs/12345' \
  --slug example-corp-data-scientist-amsterdam \
  --company 'Example Corp' \
  --role 'Data Scientist Intern' \
  --location 'Amsterdam, Netherlands'

# 2. Write the target quartet and insert the row into PROJECT_STATUS.md
python3 scripts/workspace.py init \
  --url 'https://example.com/jobs/12345' \
  --slug example-corp-data-scientist-amsterdam \
  --company 'Example Corp' \
  --role 'Data Scientist Intern' \
  --location 'Amsterdam, Netherlands' \
  --write
```

---

## 3. Associated Skills & Rules

- **Stage 1 (Job URL & JD Intake)**: `.agent/skills/job-intake/SKILL.md`, `.agent/rules/intake.md`
- **Stage 2 (Role Pre-writing `tailoring.md`)**: `.agent/skills/job-prewrite/SKILL.md`, `.agent/rules/tailoring.md`
- **Stage 3 (Targeted Resume Drafting & QA)**: `.agent/skills/targeted-resume/SKILL.md`, `.agent/rules/content.md`
- **Stage 4 (Targeted Cover Letter Drafting & QA)**: `.agent/skills/targeted-cover-letter/SKILL.md`, `.agent/rules/content.md`
- **Stage 5 (Publishing Snapshots & Updating Status)**: `.agent/skills/status-and-publish/SKILL.md`, `.agent/rules/status.md`
