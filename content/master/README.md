# Candidate Master Fact Layer (`content/master/`)

This directory is the **Single Source of Truth (SoT)** for all candidate facts and supporting evidence.

## 1. Privacy & Version-Control Design

- Only this `README.md` and the six structured `*.example.md` templates are tracked in Git.
- Your real candidate files (`profile.md`, `education.md`, `experience.md`, `projects.md`, `skills.md`, `certifications.md`) are ignored by `.gitignore` and blocked by `scripts/privacy_check.py`, ensuring **personal data is never committed or uploaded to the remote repository**.

## 2. Quick Onboarding (`bootstrap`)

After cloning or forking this repository, run from the repository root:

```bash
python3 scripts/workspace.py bootstrap
```

This command copies each `*.example.md` file in `content/master/` to its corresponding untracked `*.md` file (skipping any file that already exists so your data is never overwritten) and initializes `src/sections/header.private.tex` from `src/sections/header.private.tex.example`.

## 3. File Inventory & Responsibilities

| Untracked Local File (Gitignored) | Tracked Template File (Committed) | What to Record |
|---|---|---|
| `profile.md` | `profile.example.md` | Core identity, target role families, availability/location/work-authorization/language logistics, and reusable 2–3 sentence `Profile` angles |
| `education.md` | `education.example.md` | Degrees, institutions, dates, coursework & grades, thesis/graduation project details, and reusable `\cvedunote` lines |
| `experience.md` | `experience.example.md` | Internships and full-time roles, including multi-stage progression, candidate ownership vs. upstream boundaries, deployment lifecycle states, internal codename mappings, `Need verification` items, and reusable candidate bullets |
| `projects.md` | `projects.example.md` | Academic, personal, and open-source projects, plus overlap notes where projects relate to `education.md` or `experience.md` |
| `skills.md` | `skills.example.md` | Evidence-backed skills across programming, data/backend engineering, BI delivery, AI-assisted engineering workflows, and languages |
| `certifications.md` | `certifications.example.md` | Strictly separated inventories of completed career/professional certifications, completed course credentials, and in-progress courses |

## 4. Golden Rules for Maintaining Master Data

1. **Record Facts Only — Never Editorial Omission Rules**:
   - Document *what happened*, *how it was built*, and *what evidence exists*.
   - Do not write rules like "omit tool X on 1-page resumes" or "drop Projects first" inside `content/master/*.md`. Repo-wide editorial rules belong in `.agent/rules/content.md`, and single-role trade-offs belong in `targets/<slug>/tailoring.md`.
2. **Never Delete Master Facts to Fit One Page**:
   - External resumes must fit on 1 page, but `content/master/` should retain full technical depth, historical stages, and candidate bullets so future applications across different role families can draw from the complete record.
3. **Mark Uncertain Items Explicitly (`Need verification`)**:
   - Tag any unconfirmed metric, library name, or legacy system with `Need verification`. Never expose `Need verification` items on external resumes or cover letters until verified.
4. **Explicit One-Way Synchronization**:
   - Updating `content/master/*.md` does not automatically rewrite `src/sections/baseline-universal.tex` or historical `targeted` resumes. Baseline refreshes happen only on explicit request.
