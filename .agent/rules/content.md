# Master Data, Resume & Cover Letter Content Rules (`content.md`)

> Applicable when maintaining `content/master/`, refreshing the universal `baseline`, or drafting/editing targeted resumes (`src/sections/*.tex`) and cover letters (`src/sections/letters/*.tex`). Associated skills: `.agent/skills/master-and-baseline`, `.agent/skills/targeted-resume`, `.agent/skills/targeted-cover-letter`.

---

## 1. Candidate Master Fact Layer (`content/master/`) Maintenance Rules

### 1.1 Sole Purpose of `content/master/`: Defensible Fact & Evidence SoT
- **Facts only, no editorial omission rules**: `content/master/` stores complete, verifiable candidate facts—dates, role stages, coursework and grades, internal/external tool names, project architectures, credential IDs, and a bank of reusable candidate bullets.
- **Never delete master facts to fit a 1-page resume**: External resumes are curated 1-page views, whereas `content/master/` retains full technical context and historical stages so future applications across different role families can draw from the complete evidence pool.
- **Keep omission rules out of `content/master/`**: Directives like "omit library X on external resumes" or "drop Projects when tight on space" belong in `.agent/rules/content.md` (repo-wide) or `targets/<slug>/tailoring.md` (role-specific), never inside `content/master/*.md`.

### 1.2 Four Required Dimensions of Structured Master Facts
When updating `content/master/{profile,education,experience,projects,skills,certifications}.md`, explicitly document:
1. **Stage & Timeline Boundaries**: If a role at an employer evolved across multiple contracts, promotions, or phases (e.g., Phase 1 reporting automation -> Phase 2 containerized web application), record exact date ranges and responsibilities for each stage so earlier static deliverables are never conflated with current architecture.
2. **Candidate Ownership vs. Upstream Context**: Clearly separate what the candidate designed, built, and delivered end-to-end from upstream data warehouses or orchestration pipelines maintained by other engineering teams (which may only be cited as consumed data sources).
3. **Deployment Lifecycle & Audience State**: Distinguish `In development`, `Architecture/Security review passed (pre-production)`, and `In production`, as well as `Intended audience (~N stakeholders)` vs. `Active users`. Never describe a pre-production system as already live in production.
4. **Internal Codenames & `Need verification` Markers**:
   - Record employer-internal tool codenames alongside external human-readable descriptions (e.g., `internal BI platform`, `internal collaboration site`).
   - Mark any unconfirmed metric, library name, or historical system with `Need verification`; never include `Need verification` items in external resumes or cover letters until verified.

---

## 2. External Resume (CV) Writing & Typesetting Guardrails

### 2.1 Narrative & Phrasing Standards
- **Capability & Delivery First**: Construct every bullet around **Action + Method/Tool + Delivery Surface / Business Impact**. Avoid listing internal `.py` script filenames or low-signal plumbing details.
- **Readable External Terminology**: Replace opaque employer-internal codenames with clear industry terms (`internal BI platform`, `linked audit workbook`).
- **Evidence-Backed Skills & Credentials**:
  - Every claim in `Skills` must trace to verified evidence in `Education`, `Experience`, or `Projects`.
  - Expose AI-assisted engineering capabilities clearly (e.g., `\cvskillblock{AI-Assisted Engineering:}{Cursor, Claude Code CLI, AI-native thinking, Agentic workflow}`), backed by concrete delivery bullets rather than vague hype (never use phrases like `vibe coding`).
  - Strictly separate **Professional / Career Credentials** from **Course / Skill Credentials**, and never list in-progress courses as earned certificates.

### 2.2 Experience Section Ordering Rule (Strict Reverse-Chronological Order)
- `\cvexpblock` employer entries **must always appear in strict reverse-chronological order** (most recent / current role at the top, earliest role at the bottom).
- **Never** reorder employer blocks to put an older role above a newer role because of JD relevance. Emphasize a specific role through **bullet count, phrasing, and technical detail within its chronological position**.

### 2.3 Typography & Macro Discipline (No Arbitrary `\textbf{...}`)
- Rely only on the structural bolding built into `src/macros.tex` (`\cvexpblock` role title, `\cveduhead` institution name, `\cvskillblock` category header).
- **Never** add ad-hoc `\textbf{...}` inside experience `\item` bullets, `\cvedunote{...}` education notes, or parenthetical remarks. Use plain `Coursework:` / `Graduation Project:` prefixes and `\textit{...}` for course titles.

### 2.4 Single-Page Constraint & 8-Step Lossless Compression Hierarchy
All external resumes (`baseline` and `targeted`) **must fit on exactly 1 page**. When a build spills onto 2 pages, compress in the following order to preserve factual density:
1. **Tighten long technical clauses first**: Condense verbose subordinate clauses and repetitive tool enumerations inside individual bullets while keeping `Action + Key Tool + Outcome`.
2. **Eliminate 1–3 word orphan line wraps**: Trim bullets whose final line contains only a few trailing words to reclaim full vertical lines.
3. **Trim filler adjectives**: Tighten `Profile`, experience bullets, and `Education` notes.
4. **Consolidate `Skills` lines**: Merge overlapping skill labels and drop minor tools irrelevant to the target JD.
5. **Merge closely related bullets (preserving substance)**: Combine two short or adjacent `\item` entries under the same role into one high-density sentence. **Never delete an entire core experience bullet without explicit authorization in `tailoring.md` or from the user.**
6. **Compact `Education` notes**: Merge coursework and thesis notes onto fewer lines without removing degree headers.
7. **Fold standalone `Projects`**: When project signals are already covered under `Experience` or `Education` and `tailoring.md` permits, omit a separate `Projects` section.
8. **Hard Guardrail — Never drop an entire employer `\cvexpblock`**: Never remove a formal internship or trainee role unless explicitly instructed by the user.

### 2.5 Mandatory Bottom-Whitespace Check & Backfill Loop (Every Build)
- **After every resume compilation** (whether it compiled to 1 page immediately or after compression), inspect `body_end_fraction` in `qa.json` and visually inspect the rendered PNG via `pdftoppm`.
- If the last content line ends too high on the page (e.g., `< 80%` page height, leaving a visibly blank bottom section), **you must backfill content before delivering**.
- **Backfill priority**: `targets/<slug>/tailoring.md` candidate pool -> `content/master/` verified details -> `jd.md` focus areas.
- **How to backfill**: Expand factual density in existing experience bullets (tools, stakeholders, verified outcomes), or expand `Education` notes / `Profile` / `Skills`, then recompile and re-verify that the resume remains 1 page with balanced visual density.
- **Bullet line width**: Aim to fill each bullet's available line width cleanly rather than leaving half-empty lines.

---

## 3. Cover Letter Writing & >=60% Page-Height Guardrails

### 3.1 Core Quality Standard: Never Write a Prose Recap of the Resume
- A cover letter that merely paraphrases resume bullets in paragraph form with transition words is **unacceptable and must be rewritten**.
- The cover letter must add context that the resume cannot carry: **why this specific company and role**, **why now**, **concrete understanding of the team's workflow or technical challenge**, and **a concrete forward-looking plan for the first weeks on the job**.

### 3.2 Mandatory Five-Paragraph Structure
1. **Paragraph 1 — Hook Opening**: State directly why this company, product, team, or role design stands out—never open with generic templates like `"I am writing to apply for..."`.
2. **Paragraph 2 — Focused Resume Proof**: Cite only 1–2 high-signal delivery examples from `content/master/` that prove readiness for the role's core demand (do not walk through every job on the resume).
3. **Paragraph 3 — Company & Role Insight**: Share a specific observation or judgment on the company's business model, where this role sits in the engineering/operations workflow, or a concrete challenge in the JD.
4. **Paragraph 4 — Forward-Looking Execution Plan (Mandatory)**: Explain concretely and honestly **how the candidate plans to ramp up in the first weeks, what specific pipeline or problem they want to investigate/solve first, and how they will approach it**. Ground this in `jd.md` and `tailoring.md` without empty cliches ("I am a fast learner") or fabricated experience.
5. **Paragraph 5 — Logistics & Specific Closing**: Confirm availability (start date, duration, days/week, location/language) and close with a specific, non-template question or topic for the interview conversation.

### 3.3 Hard Minimum Length Threshold (>= 60% Page Height, Verified Visually)
- **Hard requirement**: The cover letter body (from `Dear ...` to the last body line before `Sincerely,`, excluding header, date, and signature) on a single A4 page **must end at or below 60% (3/5) of total page height** (`body_end_fraction >= 0.60`), and total page count must be **1 page**.
- **Mandatory verification loop**:
  1. Run `./scripts/build.sh letter:<id>` and check `qa.json` (`pages == 1`, `body_end_fraction >= 0.60`, `errors == []`);
  2. Render the PDF to PNG via `pdftoppm -png -r 100` and inspect the image with the Read tool;
  3. If `body_end_fraction < 0.60`, expand substantive content (primarily Paragraph 4's forward-looking plan or Paragraphs 2–3's technical/operational analysis), recompile, and re-measure until `>= 0.60`. **Never** inflate font size, line spacing, or margins to fake the height threshold.
