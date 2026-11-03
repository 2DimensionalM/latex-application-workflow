---
name: job-intake
description: Register one or more job posting URLs or raw job descriptions into the workspace (岗位链接/JD进项目). Use when the user provides job links or JDs and asks to add/intake/register them into the project ("进项目", "登记岗位", "加岗位").
---

# Step 1: Job URL & JD Intake (岗位链接与 JD 进项目)

## When to Use

Trigger this skill when the user shares one or more job posting URLs (or raw JD text) to register into the workspace.
- **Default boundary**: Unless the user explicitly asks to pre-write (`tailoring.md`) or draft LaTeX in the same turn, stop after completing the target package intake, `PROJECT_STATUS.md` update, and `workspace.py check`.

Read `.agent/rules/intake.md`, `targets/README.md`, and `.agent/rules/status.md` before starting.

---

## Workflow Checklist (Per Job URL)

```markdown
Task Progress:
- [ ] Step 1: Fetch & inspect the live job posting (or parse user-supplied JD text)
- [ ] Step 2: Cross-verify posting status (open vs. closed)
- [ ] Step 3: Run `python3 scripts/workspace.py init` to allocate `internal_id` and scaffold `targets/<slug>/`
- [ ] Step 4: Populate structured English `targets/<slug>/jd.md`
- [ ] Step 5: Populate `targets/<slug>/notes.md` and `targets/<slug>/metadata.yaml`
- [ ] Step 6: Sync `PROJECT_STATUS.md` row and run `python3 scripts/workspace.py check`
```

---

## Step-by-Step Instructions

### 1. Fetch & Parse the Job Posting
- Extract: **Company**, **Role Title**, **Location**, **Employer Job ID** (if any), **Responsibilities**, **Requirements**, **Logistics** (start date, duration, days/week, thesis vs. non-thesis, enrollment requirements), and `datePosted` / `validThrough`.
- **ATS Extraction Tips**:
  - **Workday (`*.myworkdayjobs.com`)**: Use `curl -sL '<URL>'` and extract `<meta property="og:title">`, `<meta property="og:description">`, or embedded JSON-LD (`application/ld+json`).
  - **Phenom / Corporate Careers**: Check `application/ld+json` (`@type: JobPosting`) or `phApp.ddo.jobDetail`.
  - **Age-gated sites**: Use `curl -sL` to read embedded metadata/JSON-LD directly.
- **Cross-check before marking `closed`**: Never mark a job `closed` (`已下架`) from an isolated banner alone; verify whether `JobPosting` JSON-LD / `jobDetail` still contains an active `applyUrl` and full description.

### 2. Initialize Target Package & Allocate `internal_id`
Choose a clean lowercase hyphenated slug `<company>-<role-keywords>-<city>` and run:
```bash
# Preview first
python3 scripts/workspace.py init --url '<URL>' --slug <company-role-city> --company '<Company>' --role '<Role>' --location '<City, Country>'

# Write target package + PROJECT_STATUS.md row
python3 scripts/workspace.py init --url '<URL>' --slug <company-role-city> --company '<Company>' --role '<Role>' --location '<City, Country>' --write
```
- `internal_id` is automatically assigned as `max + 1` (`001`, `002`, ...), zero-padded to 3 digits, and never recycled.

### 3. Write `targets/<slug>/jd.md` (English Standard)
- Always write `jd.md` body in **English** so downstream tailoring and English resume/letter drafting align directly.
- If the source posting is in another language (e.g., Dutch, German, French), translate faithfully into English without adding or dropping requirements, and record `Original posting language: <Language>` in the header.
- Strip cookie banners, age gates, and footer marketing boilerplate.

```markdown
# <Role Title> — <Company>

- **Internal ID:** `<id>`
- **Employer Job ID:** `<Job ID or N/A>`
- **Company:** <Company>
- **Location:** <City, Country>
- **Source URL:** <URL>
- **Captured Date:** YYYY-MM-DD
- **Original Posting Language:** English (or translated from Dutch/German/etc.)

---

## Role Overview
...

## Key Responsibilities
- ...

## Requirements & Qualifications
- ...

## Logistics & Terms
- ...
```

### 4. Write `targets/<slug>/notes.md` & Update `metadata.yaml`
- In `notes.md`, record: capture date, employer Job ID, logistics to verify (start window, thesis/non-thesis, language), and initial fit signals against `content/master/`.
- In `metadata.yaml`, set `status: "open"` (or `"closed"` if verified closed), keep `resume_version: ""` and `cover_letter_version: ""`.
- In `PROJECT_STATUS.md`, update the new row's status from `待核实` to `待预写` (if open) or `已下架` (if closed, moving the row to the bottom terminal group).

### 5. Validate
```bash
python3 scripts/workspace.py check
```
Ensure `0 errors` before finishing.
