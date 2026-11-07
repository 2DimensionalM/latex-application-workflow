---
name: application-pipeline
description: Turn a job URL or JD into a targeted resume and cover letter in one pass. Use when the user provides a posting and wants it registered and finished, or asks to intake a role and produce the CV and letter.
---

# Job URL to resume and cover letter

This is the only file to read for that task. Do not also open `README.md`, `STRUCTURE.md`, `.agent/README.md`, `RESUME_BASELINE.md`, other skills, or `.agent/rules/`. Those are reference docs for harness changes, not for producing an application.

## Do this in one pass

1. Fetch the posting. Keep only title, location, responsibilities, requirements, logistics, and employer job id. Do not invent requirements. Do not mark it closed from a banner alone; check JSON-LD or the ATS payload for a live description and apply URL.
2. Scaffold with `python3 scripts/workspace.py init --url URL --slug company-role-city --company '...' --role '...' --location '...' --write`. Write `jd.md` in English. Note a translation and the original language when the posting is not English. Put fit notes in `notes.md`. Set `status: open`, or `closed` when the posting is verified closed.
3. If the posting is open, immediately write a compact `tailoring.md`: profile angle, which sections stay, reverse-chronological bullet shortlist, skills to use, skills not to claim, and a five-paragraph letter plan. Do not turn this into a research memo.
4. Copy `src/sections/baseline-universal.tex` to `src/sections/targeted-<slug>.tex`. Add `versions/cv/targeted/{id}-resume-<company>-<role>-<location>.tex` using the same wrapper as `versions/cv/baseline/resume-baseline.tex`, pointed at the new section. Set `resume_version` in `metadata.yaml`.
5. Write `src/sections/letters/targeted-<slug>-letter.tex` and `versions/letter/targeted/{id}-cover-letter-<slug>.tex` using the wrapper in `versions/letter/targeted/cover-letter-placeholder.tex`. Set `cover_letter_version`.
6. Run `./scripts/build.sh resume:{id}` and `./scripts/build.sh letter:{id}`. Read `qa.json`. Fix the source and rebuild until the resume is one page and the letter is one page with `body_end_fraction >= 0.60`. Render a PNG with `pdftoppm` only if the QA numbers disagree with the layout you expect.
7. Move the `PROJECT_STATUS.md` row to the preparation group and set `Drafting Resume` or `Ready to Apply`. Run `python3 scripts/workspace.py check` once at the end.

Stop after intake only when the user asked to register the URL and nothing more, or the posting is closed.

## Hard constraints

- Never read, print, or commit `src/sections/header.private.tex`. Use facts from `content/master/` and the JD only.
- Keep Experience in reverse-chronological order. Do not add `\textbf` inside bullets or education notes.
- Resume bullets are action, tool, and outcome. If `qa.json` reports one page but `body_end_fraction < 0.80`, add verified detail and rebuild.
- The letter is five paragraphs: why this role, one or two proof points, a specific observation from the JD, what to do in the first weeks, and logistics. Do not retell the resume. Do not pad with spacing or margins.
- Do not `--publish` or mark the role `Applied` unless the user says the file was submitted.
- A failed build is diagnosed from `output/review/<JOBNAME>/build.log` only.
