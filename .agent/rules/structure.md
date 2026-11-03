# LaTeX Structure, Versioning & Naming Rules (`structure.md`)

> Applicable when adding or modifying LaTeX entry files (`versions/`), section fragments (`src/sections/`), or shared preambles and macros (`src/preamble*.tex`, `src/macros*.tex`).

---

## 1. Three-Tier LaTeX Decoupling

1. **Preamble & Macro Layer (`src/preamble.tex`, `src/macros.tex`, `src/preamble-letter.tex`, `src/macros-letter.tex`)**:
   - Controls page geometry, font encoding, paragraph rhythm, and structural layout macros:
     - `\cvexpblock{<Company>}{<Role Title>}{<Location>}{<Dates>}`: two-column aligned experience header;
     - `\cveduhead{<School>}{<Dates>}`, `\cvedusub{<Degree>}{<Location>}`, `\cvedunote{<Notes>}`: education block macros;
     - `\cvskillblock{<Category:>}{<Skill items>}`: categorized skill block;
     - `\LetterSubject{<Subject line>}`: cover letter `Re:` subject line.
   - Because shared preambles and macros affect multiple targets, run `python3 scripts/workspace.py affected <path>` after any edit to inspect the blast radius.
2. **Section Content Layer (`src/sections/` & `src/sections/letters/`)**:
   - `src/sections/header.tex`: unified header router that automatically loads `src/sections/header.private.tex` if present locally, or falls back to `src/sections/header.template.tex`.
   - `src/sections/baseline-universal.tex`: the single cross-market Universal CV Baseline body.
   - `src/sections/targeted-<short-slug>.tex`: role-specific targeted resume body fragments.
   - `src/sections/letters/targeted-<short-slug>-letter.tex`: role-specific targeted cover letter body fragments.
3. **Build Entry Layer (`versions/cv/{base,baseline,targeted}/` & `versions/letter/{baseline,targeted}/`)**:
   - Thin wrapper files that set `\documentclass`, `\input` the shared preamble/macros, and `\input` the target section fragment.
   - `JOBNAME` and output PDF filenames are **automatically derived from the entry filename stem**, eliminating duplicate name maintenance.

---

## 2. Version Tiers & Naming Invariants

| Tier | Entry Path Pattern | Published PDF Path (`--publish`) | Purpose |
|---|---|---|---|
| **Base Demo** | `versions/cv/base/resume-base.tex` | `output/cv/base/resume-base.pdf` | Minimal structural demo, not for applications |
| **Universal Baseline** | `versions/cv/baseline/resume-baseline.tex` | `output/cv/baseline/resume-baseline.pdf` | Single cross-market CV parent (see `RESUME_BASELINE.md`) |
| **Targeted Resume** | `versions/cv/targeted/{id}-resume-<company>-<role>-<location>.tex` | `output/cv/targeted/{id}-resume-<company>-<role>-<location>.pdf` | Role-specific resume (`{id}` = 3-digit `internal_id`) |
| **Targeted Cover Letter** | `versions/letter/targeted/{id}-cover-letter-<short-slug>.tex` | `output/cover-letters/pdf/targeted/{id}-cover-letter-<short-slug>.pdf` | Role-specific cover letter (`{id}` = 3-digit `internal_id`) |

### Naming Consistency Rules
- Entry filenames use only lowercase ASCII letters, digits, and hyphens (`[a-z0-9-]+.tex`).
- Targeted entry filenames must start with `{internal_id}-resume-` or `{internal_id}-cover-letter-` matching `targets/<slug>/metadata.yaml`; `workspace.py check` validates this prefix invariant.
- Internal section fragments (`src/sections/targeted-*.tex`) may use a shorter slug than the full entry filename, provided all literal `\input{...}` paths resolve cleanly.
