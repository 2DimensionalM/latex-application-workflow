# Job URL & JD Intake Rules (`intake.md`)

> Applicable when the user provides one or more job posting URLs (or raw JD text) and asks to register them into the workspace. Associated skill: `.agent/skills/job-intake/SKILL.md`.

---

## 1. Trigger & Default Boundary

- **Trigger**: The user provides one or more job posting URLs or raw JD text to add to the project, without explicitly asking to draft a targeted resume or cover letter in the same turn.
- **Batch Intake Support**: When multiple URLs are provided in a single turn, each URL must receive its own `targets/<slug>/` directory, its own sequential `internal_id`, and its own row in `PROJECT_STATUS.md`.
- **Default Stopping Point**: Complete target quartet initialization, structured English `jd.md`, initial `notes.md`, and `PROJECT_STATUS.md` synchronization (`Status = Pending Pre-write`). Unless explicitly requested by the user, **do not skip pre-writing to generate LaTeX or compile PDFs**.

---

## 2. Mandatory Steps per Job Target

1. **Allocate Unique ID & Scaffold Target Directory**:
   - Run `python3 scripts/workspace.py init --url '<URL>' --slug <company-role-location> --company '<Company>' --role '<Role>' --location '<Location>' --write` (omit `--write` first to preview).
   - `internal_id` is automatically allocated as `max + 1` (`"001"` to `"999"`, zero-padded, monotonically increasing, never recycled).
2. **Fetch & Verify the Job Description**:
   - Extract from the live page: role title, company, location, responsibilities, required/preferred qualifications, internship/employment terms (start date, duration, days/week, thesis vs. non-thesis, enrollment rules), employer Job ID (if any), and `datePosted` / `validThrough`.
   - **Never invent** requirements or terms not present in the source posting.
3. **Cross-Verify Posting Status (Avoid False-Positive `closed`)**:
   - Do not mark a posting `closed` (`Closed`) based solely on an isolated banner or cached aggregator snippet. Cross-check whether embedded `application/ld+json` (`@type: JobPosting`) or ATS state objects (e.g., Workday or Phenom `phApp.ddo.jobDetail`) still expose a live description and `applyUrl`.
   - If verified closed: set `status: "closed"` in `metadata.yaml` and `Closed` in `PROJECT_STATUS.md` (placed in the bottom terminal group), keep the target package archived, and skip pre-writing/LaTeX.
   - If verified open: set `status: "open"` in `metadata.yaml` and `Pending Pre-write` in `PROJECT_STATUS.md`.
4. **Write Structured `targets/<slug>/jd.md`**:
   - Strip footer marketing copy, age-verification gates, cookie banners, and unrelated job recommendations.
   - Record metadata at the top of `jd.md`: `Internal ID`, `Employer Job ID`, `Company`, `Location`, `Source URL`, `Captured Date`, and `Original Posting Language`.
5. **Write `targets/<slug>/notes.md`**:
   - Record capture date, internal ID, employer Job ID, logistics items requiring verification (start window, language, visa/enrollment eligibility), and initial fit signals against `content/master/`.
6. **Leave `targets/<slug>/tailoring.md` Pending**:
   - Keep `tailoring.md` as a pending outline during intake-only runs, and leave `resume_version: ""` and `cover_letter_version: ""` in `metadata.yaml`.
7. **Synchronize `PROJECT_STATUS.md` & Validate**:
   - Ensure the new row is placed in Group 1 (active preparation group) with `[JD](targets/<slug>/jd.md)` and `—` for Resume and Cover Letter.
   - Run `python3 scripts/workspace.py check` and verify `0 errors`.

---

## 3. ATS & Career Site Extraction Patterns

| Site / ATS Type | Common Issue | Recommended Extraction Approach |
|---|---|---|
| **Structured Corporate Careers** | Heavy navigation chrome or client-side hydration | Parse embedded `application/ld+json` (`@type: JobPosting`) or the main article body |
| **Workday (`*.myworkdayjobs.com`)** | SPA shell returns empty body on basic fetch | Use `curl -sL` to extract `<meta property="og:title">`, `<meta property="og:description">`, or embedded JSON |
| **Greenhouse / Lever / Ashby** | Tracking query parameters on aggregator links | Extract main posting body or `og:description`; preserve the source URL |
| **Phenom People** | External feeds sometimes misreport "filled" | Inspect `application/ld+json` or `phApp.ddo.jobDetail` in the live HTML to confirm status and Workday `applyUrl` |
| **Age-Gated / Region-Gated Sites** | Standard fetch redirects to an age-gate form | Use `curl -sL` to inspect raw HTML metadata and embedded `JobPosting` JSON-LD |

---

## 4. `jd.md` Language Standard (Aligned with English Resume Workflow)

- **Write `jd.md` in English by default** so downstream pre-writing (`tailoring.md`), resume bullet mapping, and cover letter drafting align directly.
- **Non-English Postings (e.g., Dutch, German, French)**:
  - Faithfully translate the full JD into English in `jd.md` without adding or omitting requirements;
  - Note at the top of `jd.md`: `Original Posting Language: <Language>`, `Source URL`, and `Captured Date`;
  - Optionally record `posting_language: "nl"` (or relevant ISO code) and `jd_language: "en"` in `metadata.yaml`;
  - Preserve exact tool names (`SQL`, `Power BI`, `Python`), dates, currency amounts (`€`/`$`), and city names; explain local degree or administrative terms in parentheses on first mention (e.g., `WO degree (research-university level)`).
