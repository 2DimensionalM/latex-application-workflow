#!/usr/bin/env python3
"""Render the HTML master resume from the content/master/*.md fact files.

Reads profile/education/experience/projects/skills.md plus the private header
(src/sections/header.private.tex) and fills src/html/resume.template.html.
Writes content/master/resume.html (Git-ignored). Prints only the output path.
"""
from __future__ import annotations

import argparse
import html
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "content/master"
TEMPLATE = ROOT / "src/html/resume.template.html"
HEADER = ROOT / "src/sections/header.private.tex"
OUTPUT = MASTER / "resume.html"
DATE_RANGE = re.compile(r"([A-Z][a-z]{2}) (\d{4}) – ([A-Z][a-z]{2}) (\d{4})")

e = html.escape


def sections(text: str) -> list[tuple[str, str]]:
    """Split a master file into (heading, body) pairs at '## ' headings."""
    parts = re.split(r"^## +(.+)$", text, flags=re.M)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)]


def heading_name(heading: str) -> str:
    return re.sub(r"^\d+\.\s*", "", heading).strip()


def field(body: str, name: str) -> str:
    m = re.search(rf"^- \*\*{re.escape(name)}:\*\*[ \t]*(.*)$", body, re.M)
    return m.group(1).strip() if m else ""


def sub_items(body: str, name: str) -> list[str]:
    """Indented '  - ' items under a '- **name:**' field."""
    m = re.search(rf"^- \*\*{re.escape(name)}:\*\*.*\n((?:  +- .*\n?)*)", body, re.M)
    if not m:
        return []
    return [re.sub(r"^\s+- ", "", line).strip() for line in m.group(1).splitlines() if line.strip()]


def bullets(body: str) -> list[str]:
    return [re.sub(r"^`|`$", "", item) for item in sub_items(body, "Reusable Candidate Bullets")]


def compact_dates(value: str) -> str:
    """'Mar 2025 – Sep 2025' -> 'Mar – Sep 2025'; other ranges unchanged."""
    return DATE_RANGE.sub(
        lambda m: f"{m[1]} – {m[3]} {m[4]}" if m[2] == m[4] else m[0], value
    )


def plain(md: str) -> str:
    return re.sub(r"\*([^*]+)\*", r"\1", md)


def on_baseline(body: str) -> bool:
    return field(body, "On baseline CV").lower() not in ("no", "false")


def table_rows(body: str) -> list[list[str]]:
    rows = []
    for line in body.splitlines():
        if line.startswith("|") and not re.match(r"^\|\s*-", line):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows[1:]  # drop the header row


def entry(org: str, date: str, role: str, items: list[str]) -> str:
    lis = "".join(f"\n            <li>{e(b)}</li>" for b in items)
    return (
        f'        <div class="entry">\n'
        f'          <div class="row"><span class="org">{e(org)}</span><span class="date">{e(date)}</span></div>\n'
        f'          <div class="role">{role}</div>\n'
        f"          <ul>{lis}\n          </ul>\n        </div>\n"
    )


def render_experience(text: str) -> str:
    out = []
    for heading, body in sections(text):
        if not on_baseline(body):
            continue
        org, _, title = heading_name(heading).partition(" — ")
        title = field(body, "CV Title") or title
        role = e(" · ".join(x for x in (title, field(body, "Location")) if x))
        out.append(entry(org, compact_dates(field(body, "Dates") or field(body, "Overall Dates")), role, bullets(body)))
    return "".join(out)


def render_projects(text: str) -> str:
    out = []
    for heading, body in sections(text):
        if not on_baseline(body):
            continue
        context = field(body, "Context & Dates")
        # Prefer the dates in parentheses (project period) over data ranges in the text.
        m = re.search(r"\(([A-Z][a-z]{2} \d{4}(?: – [A-Z][a-z]{2} \d{4})?)\)", context) or DATE_RANGE.search(context)
        role = e(field(body, "Tech Stack"))
        repo = field(body, "Repository")
        if repo:
            role += f' · <a href="{e(repo)}">GitHub</a>'
        out.append(entry(heading_name(heading), compact_dates(m[1] if m.re is not DATE_RANGE else m[0]) if m else "", role, bullets(body)))
    return "".join(out)


def render_education(text: str) -> str:
    out = []
    for _heading, body in sections(text):
        institution = field(body, "Institution")
        if not institution:
            continue
        courses = field(body, "Coursework listed on CV") or "; ".join(sub_items(body, "Coursework listed on CV"))
        meta = " · ".join(x for x in (field(body, "Location"), field(body, "Dates")) if x)
        out.append(
            f'        <div class="entry">\n'
            f'          <span class="org">{e(institution)}</span>\n'
            f"          <div>{e(field(body, 'Degree'))}</div>\n"
            f'          <div class="meta">{e(meta)}</div>\n'
            + (f'          <div class="course">{e(plain(courses))}</div>\n' if courses else "")
            + "        </div>\n"
        )
    return "".join(out)


def render_skills(text: str) -> tuple[str, str]:
    skills, langs = [], []
    for heading, body in sections(text):
        name = heading_name(heading)
        rows = table_rows(body)
        if name == "Languages":
            langs = [f'        <div class="lang"><span>{e(r[0])}</span><span>{e(r[1])}</span></div>\n' for r in rows]
        elif rows and not name.startswith("Not Held"):
            items = ", ".join(r[0] for r in rows)
            skills.append(f'        <div class="skill"><b>{e(name)}</b><span>{e(items)}</span></div>\n')
    return "".join(skills), "".join(langs)


def render_header(tex: str) -> tuple[str, str]:
    """Name and contact HTML from the private LaTeX header (never printed)."""
    name = re.search(r"\\textbf\{([^{}]+)\}", tex)
    body = tex.split("\\normalsize", 1)[1].rsplit("}", 1)[0] if "\\normalsize" in tex else ""
    plain_items, link_items = [], []
    for part in re.split(r"\\quad\\textbar\\quad", body):
        part = part.strip()
        link = re.search(r"\\href\{([^{}]+)\}\{([^{}]+)\}", part)
        if link and link[1].startswith("mailto:"):
            plain_items.append(e(link[2]))
        elif link:
            url = link[1]
            link_items.append(f'<a href="{e(url)}">{e(re.sub(r"^https?://", "", url))}</a>')
        elif part:
            plain_items.append(e(part))
    contact = " · ".join(plain_items) + ("<br>\n        " + " · ".join(link_items) if link_items else "")
    return (name[1] if name else "[Full Name]"), contact


def render(root: Path = ROOT) -> str:
    master = root / "content/master"
    read = lambda name: (master / name).read_text(encoding="utf-8")
    profile = read("profile.md")
    tagline = field(profile, "CV tagline (current master)")
    summary_section = dict((heading_name(h), b) for h, b in sections(profile)).get("Profile Summary Candidates", "")
    summary = re.search(r"`([^`]+)`", summary_section)
    header = root / "src/sections/header.private.tex"
    name, contact = render_header(header.read_text(encoding="utf-8") if header.is_file() else "")
    skills, langs = render_skills(read("skills.md"))
    page = f"""
  <header>
    <div class="id">
      <h1>{e(name)}</h1>
      <div class="tagline">{e(tagline)}</div>
      <div class="contact">
        {contact}
      </div>
      <div class="profile">
    {e(summary[1] if summary else "")}
      </div>
    </div>
    <div class="photo">Photo</div>
  </header>

  <div class="cols">
    <div class="main">

      <section>
        <h2>Experience</h2>
{render_experience(read("experience.md"))}      </section>

      <section>
        <h2>Projects</h2>
{render_projects(read("projects.md"))}      </section>

    </div>

    <aside class="side">

      <section>
        <h2>Education</h2>
{render_education(read("education.md"))}      </section>

      <section>
        <h2>Skills</h2>
{skills}      </section>

      <section>
        <h2>Languages</h2>
{langs}      </section>

    </aside>
  </div>
"""
    template = (root / "src/html/resume.template.html").read_text(encoding="utf-8")
    return template.replace("{{TITLE}}", e(f"{name} – CV")).replace("{{PAGE}}", page)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        out = args.out if args.out.is_absolute() else ROOT / args.out
        out.write_text(render(), encoding="utf-8")
    except (OSError, IndexError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(out.relative_to(ROOT) if out.is_relative_to(ROOT) else out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
