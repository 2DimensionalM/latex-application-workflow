#!/usr/bin/env python3
"""Render HTML resumes from the content/master/*.md fact files.

Two inputs:
- the master itself (all `On baseline CV` entries) -> content/master/resume.html
- a tailored resume Markdown spec (versions/cv/targeted/*.md) that only chooses and words content:
  tagline, profile, which experience/project entries and bullets, coursework lines, skills lines.

Employers, titles, dates, locations, tech stacks and links always come from the fact files, and the
name, contact block and photo from the private header, so a tailored spec cannot change them.
Prints only the output path.
"""
from __future__ import annotations

import argparse
import base64
import html
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "content/master"
TEMPLATE = ROOT / "src/html/resume.template.html"
HEADER = ROOT / "src/sections/header.private.tex"
OUTPUT = MASTER / "resume.html"
PHOTOS = {"photo.jpg": "image/jpeg", "photo.jpeg": "image/jpeg", "photo.png": "image/png"}
DATE_RANGE = re.compile(r"([A-Z][a-z]{2}) (\d{4}) – ([A-Z][a-z]{2}) (\d{4})")

e = html.escape


# ---------- fact-file parsing ----------

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


# ---------- the master model ----------

def experience_model(text: str) -> list[dict]:
    out = []
    for heading, body in sections(text):
        org, _, title = heading_name(heading).partition(" — ")
        title = field(body, "CV Title") or title
        out.append({
            "name": org.strip(),
            "date": compact_dates(field(body, "Dates") or field(body, "Overall Dates")),
            "role": e(" · ".join(x for x in (title, field(body, "Location")) if x)),
            "bullets": bullets(body),
            "baseline": on_baseline(body),
        })
    return out


def project_model(text: str) -> list[dict]:
    out = []
    for heading, body in sections(text):
        context = field(body, "Context & Dates")
        # Prefer the dates in parentheses (project period) over data ranges in the text.
        m = re.search(r"\(([A-Z][a-z]{2} \d{4}(?: – [A-Z][a-z]{2} \d{4})?)\)", context) or DATE_RANGE.search(context)
        role = e(field(body, "Tech Stack"))
        repo = field(body, "Repository")
        if repo.startswith("http"):  # notes like 'private; do not link' are not links
            role += f' · <a href="{e(repo)}">GitHub</a>'
        out.append({
            "name": heading_name(heading),
            "date": compact_dates(m[1] if m.re is not DATE_RANGE else m[0]) if m else "",
            "role": role,
            "bullets": bullets(body),
            "baseline": on_baseline(body),
        })
    return out


def education_model(text: str) -> list[dict]:
    out = []
    for _heading, body in sections(text):
        institution = field(body, "Institution")
        if not institution:
            continue
        courses = field(body, "Coursework listed on CV") or "; ".join(sub_items(body, "Coursework listed on CV"))
        out.append({
            "name": institution,
            "degree": field(body, "Degree"),
            "meta": " · ".join(x for x in (field(body, "Location"), field(body, "Dates")) if x),
            "course": plain(courses),
        })
    return out


def skills_model(text: str) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    skills, langs = [], []
    for heading, body in sections(text):
        name = heading_name(heading)
        rows = table_rows(body)
        if name == "Languages":
            langs = [(r[0], r[1]) for r in rows]
        elif rows and not name.startswith("Not Held"):
            skills.append((name, ", ".join(r[0] for r in rows)))
    return skills, langs


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


def render_photo(master: Path) -> str:
    """Photo box: the private content/master/photo.* embedded as a data URI, or the empty placeholder."""
    for name, mime in PHOTOS.items():
        file = master / name
        if file.is_file():
            data = base64.b64encode(file.read_bytes()).decode("ascii")
            return f'<div class="photo has-photo"><img src="data:{mime};base64,{data}" alt="Photo"></div>'
    return '<div class="photo">Photo</div>'


def model(root: Path = ROOT) -> dict:
    master = root / "content/master"
    read = lambda name: (master / name).read_text(encoding="utf-8")
    profile = read("profile.md")
    summary_section = dict((heading_name(h), b) for h, b in sections(profile)).get("Profile Summary Candidates", "")
    summary = re.search(r"`([^`]+)`", summary_section)
    header = root / "src/sections/header.private.tex"
    name, contact = render_header(header.read_text(encoding="utf-8") if header.is_file() else "")
    skills, langs = skills_model(read("skills.md"))
    return {
        "root": root, "name": name, "contact": contact,
        "tagline": field(profile, "CV tagline (current master)"),
        "profile": summary[1] if summary else "",
        "experience": experience_model(read("experience.md")),
        "projects": project_model(read("projects.md")),
        "education": education_model(read("education.md")),
        "skills": skills, "langs": langs,
    }


def baseline_selection(m: dict) -> dict:
    return {
        "tagline": m["tagline"], "profile": m["profile"],
        "experience": [(x["name"], x["bullets"]) for x in m["experience"] if x["baseline"]],
        "projects": [(x["name"], x["bullets"]) for x in m["projects"] if x["baseline"]],
        "education": [(x["name"], x["course"]) for x in m["education"]],
        "skills": list(m["skills"]),
    }


# ---------- HTML ----------

def entry(org: str, date: str, role: str, items: list[str]) -> str:
    lis = "".join(f"\n            <li>{e(b)}</li>" for b in items)
    return (
        f'        <div class="entry">\n'
        f'          <div class="row"><span class="org">{e(org)}</span><span class="date">{e(date)}</span></div>\n'
        f'          <div class="role">{role}</div>\n'
        f"          <ul>{lis}\n          </ul>\n        </div>\n"
    )


def page(m: dict, sel: dict) -> str:
    by = lambda kind: {x["name"]: x for x in m[kind]}
    exp, proj, edu = by("experience"), by("projects"), by("education")
    experience = "".join(entry(n, exp[n]["date"], exp[n]["role"], b) for n, b in sel["experience"])
    projects = "".join(entry(n, proj[n]["date"], proj[n]["role"], b) for n, b in sel["projects"])
    education = "".join(
        f'        <div class="entry">\n'
        f'          <span class="org">{e(n)}</span>\n'
        f"          <div>{e(edu[n]['degree'])}</div>\n"
        f'          <div class="meta">{e(edu[n]["meta"])}</div>\n'
        + (f'          <div class="course">{e(course)}</div>\n' if course else "")
        + "        </div>\n"
        for n, course in sel["education"]
    )
    skills = "".join(f'        <div class="skill"><b>{e(c)}</b><span>{e(items)}</span></div>\n' for c, items in sel["skills"])
    langs = "".join(f'        <div class="lang"><span>{e(a)}</span><span>{e(b)}</span></div>\n' for a, b in m["langs"])
    body = f"""
  <header>
    {render_photo(m["root"] / "content/master")}
    <div class="id">
      <h1>{e(m["name"])}</h1>
      <div class="tagline">{e(sel["tagline"])}</div>
      <div class="contact">
        {m["contact"]}
      </div>
      <div class="profile">
    {e(sel["profile"])}
      </div>
    </div>
  </header>

  <div class="cols">
    <div class="main">

      <section>
        <h2>Experience</h2>
{experience}      </section>

      <section>
        <h2>Projects</h2>
{projects}      </section>

    </div>

    <aside class="side">

      <section>
        <h2>Education</h2>
{education}      </section>

      <section>
        <h2>Skills</h2>
{skills}      </section>

      <section>
        <h2>Languages</h2>
{langs}      </section>

    </aside>
  </div>
"""
    template = (m["root"] / "src/html/resume.template.html").read_text(encoding="utf-8")
    return template.replace("{{TITLE}}", e(f"{m['name']} – CV")).replace("{{PAGE}}", body)


def render(root: Path = ROOT) -> str:
    """The master resume: every entry marked for the baseline CV."""
    m = model(root)
    return page(m, baseline_selection(m))


# ---------- tailored resume Markdown spec ----------

SPEC_NOTE = """<!--
Tailored resume spec. Choose and word content here; the renderer adds everything else.
- Headings under Experience, Projects and Education must match names in content/master/*.md exactly.
  Entries marked "On baseline CV: no" in the fact files may be added by name.
- Dates, titles, employers, locations, tech stacks, links, name, contact and photo come from the
  fact files and cannot be changed here.
- Experience is printed newest first whatever the order here, and every employer must stay.
- Bullets are plain text (no bold). Never add facts, numbers or skills that are not in content/master.
-->
"""


def to_markdown(sel: dict, title: str = "Resume") -> str:
    out = [f"# {title}", "", SPEC_NOTE, "## Tagline", "", sel["tagline"], "", "## Profile", "", sel["profile"], ""]
    for section, key in (("Experience", "experience"), ("Projects", "projects")):
        out += [f"## {section}", ""]
        for name, items in sel[key]:
            out += [f"### {name}", "", *[f"- {b}" for b in items], ""]
    out += ["## Education", ""]
    for name, course in sel["education"]:
        out += [f"### {name}", "", *([f"Coursework: {course}"] if course else []), ""]
    out += ["## Skills", "", *[f"- {c}: {items}" for c, items in sel["skills"]], ""]
    return "\n".join(out)


def baseline_markdown(root: Path = ROOT, title: str = "Resume") -> str:
    return to_markdown(baseline_selection(model(root)), title)


def _clean(text: str) -> str:
    return re.sub(r"\*\*([^*]+)\*\*|`([^`]+)`", lambda m: m[1] or m[2], text).strip()


def parse_markdown(text: str) -> dict:
    """Raw selection from a spec, before validation against the fact files."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    raw = {"tagline": "", "profile": "", "experience": [], "projects": [], "education": [], "skills": []}
    for heading, body in sections(text):
        key = heading.strip().lower()
        if key in ("tagline", "profile"):
            raw[key] = " ".join(l.strip() for l in body.strip().splitlines() if l.strip())
        elif key in ("experience", "projects", "education"):
            parts = re.split(r"^### +(.+)$", body, flags=re.M)
            for i in range(1, len(parts), 2):
                name, block = parts[i].strip(), parts[i + 1]
                if key == "education":
                    course = re.search(r"^Coursework:\s*(.+)$", block, re.M)
                    raw[key].append((name, _clean(course[1]) if course else ""))
                else:
                    raw[key].append((name, [_clean(l[2:]) for l in block.splitlines() if l.startswith("- ") and l[2:].strip()]))
        elif key == "skills":
            for line in body.splitlines():
                if line.startswith("- ") and ":" in line:
                    cat, items = line[2:].split(":", 1)
                    if items.strip():
                        raw[key].append((_clean(cat), _clean(items)))
    return raw


def resolve(m: dict, raw: dict) -> dict:
    """Validate a raw selection against the fact files; raise ValueError listing every problem."""
    problems = []

    def match(kind: str, label: str) -> list:
        known = {x["name"].lower(): x["name"] for x in m[kind]}
        out = []
        for name, value in raw[kind]:
            if name.lower() in known:
                out.append((known[name.lower()], value))
            else:
                problems.append(f"{label} '{name}' is not in content/master (use the exact name)")
        return out

    experience = dict(match("experience", "experience entry"))
    for x in m["experience"]:
        if x["baseline"] and x["name"] not in experience:
            problems.append(f"employer '{x['name']}' was dropped; every employer must stay")
    projects = match("projects", "project")
    education = dict(match("education", "education entry"))
    if problems:
        raise ValueError("resume spec: " + "; ".join(problems))
    return {
        "tagline": raw["tagline"] or m["tagline"],
        "profile": raw["profile"] or m["profile"],
        # Fact-file order is newest first; keep it whatever order the spec used.
        "experience": [(x["name"], experience[x["name"]]) for x in m["experience"] if x["name"] in experience],
        "projects": projects,
        "education": [(x["name"], education[x["name"]]) for x in m["education"] if x["name"] in education],
        "skills": raw["skills"] or list(m["skills"]),
    }


def render_markdown(text: str, root: Path = ROOT) -> str:
    m = model(root)
    return page(m, resolve(m, parse_markdown(text)))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=OUTPUT)
    parser.add_argument("--from-md", type=Path, help="render a tailored resume spec instead of the master")
    args = parser.parse_args()
    try:
        out = args.out if args.out.is_absolute() else ROOT / args.out
        if args.from_md:
            spec = args.from_md if args.from_md.is_absolute() else ROOT / args.from_md
            out.write_text(render_markdown(spec.read_text(encoding="utf-8")), encoding="utf-8")
        else:
            out.write_text(render(), encoding="utf-8")
    except (OSError, IndexError, KeyError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(out.relative_to(ROOT) if out.is_relative_to(ROOT) else out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
