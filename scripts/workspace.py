#!/usr/bin/env python3
"""Metadata-driven LaTeX application workflow harness: bootstrap, init, check, list, build, qa, affected."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
PRIVATE = "src/sections/header.private.tex"
PRIVATE_EXAMPLE = "src/sections/header.private.tex.example"
BASELINE_ENTRY = "versions/cv/baseline/resume-baseline.tex"
PLACEHOLDER_LETTER_ENTRY = "versions/letter/targeted/cover-letter-placeholder.tex"
VERSION_FIELDS = {"resume": "resume_version", "letter": "cover_letter_version"}

GROUP_0_LABELS = {
    "待核实", "待预写", "写简历", "写求职信", "审核简历", "审核求职信", "待投递",
    "Pending Verification", "Pending Pre-write", "Drafting Resume", "Drafting Letter",
    "Reviewing Resume", "Reviewing Letter", "Ready to Apply",
}
GROUP_1_LABELS = {
    "已投递", "一面", "二面", "终面", "补材料",
    "Applied", "Interview", "Round 1", "Round 2", "Final Round", "Follow-up Docs",
}
GROUP_2_LABELS = {
    "已拿 offer", "已拒", "已下架",
    "Offer", "Rejected", "Closed",
}

STATUS = {
    "draft": GROUP_0_LABELS,
    "open": GROUP_0_LABELS - {"待核实", "Pending Verification"},
    "applied": {"已投递", "补材料", "Applied", "Follow-up Docs"},
    "interviewing": {"一面", "二面", "终面", "补材料", "Interview", "Round 1", "Round 2", "Final Round", "Follow-up Docs"},
    "offer": {"已拿 offer", "Offer"},
    "rejected": {"已拒", "Rejected"},
    "closed": {"已下架", "Closed"},
}


def yaml_load(path: Path) -> dict:
    try:
        import yaml
    except ImportError as exc:
        raise ValueError(
            "Missing PyYAML: run `.venv/bin/python -m pip install -r requirements.txt`"
        ) from exc

    class UniqueLoader(yaml.SafeLoader):
        pass

    def mapping(loader, node, deep=False):
        result = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise ValueError(f"{path}: YAML keys must be strings")
            if key in result:
                raise ValueError(f"{path}: duplicate YAML key {key}")
            result[key] = loader.construct_object(value_node, deep=deep)
        return result

    UniqueLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping
    )
    try:
        data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)
    except yaml.YAMLError as exc:
        raise ValueError(f"{path}: invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected mapping")
    return data


def safe_path(root: Path, value: str) -> Path:
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValueError(f"invalid relative path: {value!r}")
    p = root / value
    if ".." in Path(value).parts or not p.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"path escapes workspace: {value}")
    if p.resolve() == (root / PRIVATE).resolve():
        raise ValueError("private header cannot be inspected")
    return p


def packages(root: Path) -> list[tuple[Path, dict]]:
    targets_dir = root / "targets"
    if not targets_dir.is_dir():
        return []
    return [
        (
            p,
            yaml_load(
                safe_path(root, (p / "metadata.yaml").relative_to(root).as_posix())
            ),
        )
        for p in sorted(targets_dir.iterdir())
        if p.is_dir() and p.name != "example-company-role"
    ]


def rows(root: Path) -> list[list[str]]:
    text = (root / "PROJECT_STATUS.md").read_text(encoding="utf-8")
    if "## 岗位总表" not in text:
        raise ValueError("PROJECT_STATUS.md missing '## 岗位总表' section")
    table = text.split("## 岗位总表", 1)[1].split("\n## ", 1)[0]
    result = []
    for line in table.splitlines():
        if not line.startswith("|") or re.match(r"^\|\s*(编号|ID|[-:])", line):
            continue
        cells = re.split(r"(?<!\\)\s+\|\s+", line.strip().strip("|").strip())
        if len(cells) != 9:
            raise ValueError(f"expected nine cells in status row: {line[:70]}")
        result.append(cells)
    return result


def history_rows(root: Path) -> list[list[str]]:
    text = (root / "PROJECT_STATUS.md").read_text(encoding="utf-8")
    if "## 历史动作" not in text:
        return []
    table = text.split("## 历史动作", 1)[1].split("\n## ", 1)[0]
    result = []
    for line in table.splitlines():
        if not line.startswith("|") or re.match(r"^\|\s*(日期|Date|[-:])", line):
            continue
        cells = re.split(r"(?<!\\)\s+\|\s+", line.strip().strip("|").strip())
        if len(cells) != 4:
            raise ValueError(f"expected four cells in history row: {line[:70]}")
        result.append(cells)
    return result


def link(cell: str) -> str | None:
    m = re.search(r"\]\((.+)\)", cell)
    return m.group(1) if m else None


def record(entry: str, aliases: list[str], engine: str = "pdflatex") -> dict:
    p = Path(entry)
    if (
        len(p.parts) != 4
        or p.parts[0] != "versions"
        or p.parts[1] not in ("cv", "letter")
        or p.parts[2] not in ("base", "baseline", "targeted")
        or p.suffix not in (".tex", ".html")
    ):
        raise ValueError(f"invalid entry: {entry}")
    if p.suffix == ".html":
        engine = "chrome"
    if engine not in ("pdflatex", "xelatex", "chrome"):
        raise ValueError(f"invalid engine for {entry}: {engine}")
    kind = "resume" if p.parts[1] == "cv" else "letter"
    sub = p.parts[2]
    if not re.fullmatch(r"[a-z0-9-]+", p.stem):
        raise ValueError(f"invalid JOBNAME: {p.stem}")
    prefix = "output/cv" if kind == "resume" else "output/cover-letters/pdf"
    return {
        "entry": entry,
        "aliases": list(aliases),
        "kind": kind,
        "engine": engine,
        "jobname": p.stem,
        "pdf": f"{prefix}/{sub}/{p.stem}.pdf",
    }


def registry(root: Path) -> tuple[list[dict], dict[str, dict]]:
    manifest = json.loads((root / "scripts/build-targets.json").read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1:
        raise ValueError("unsupported build manifest version")
    by_entry: dict[str, dict] = {}
    for item in manifest["targets"]:
        entry = item["entry"]
        if entry in by_entry:
            raise ValueError(f"duplicate manifest entry: {entry}")
        raw_aliases = item.get("aliases")
        if raw_aliases is None and "alias" in item:
            raw_aliases = [item["alias"]]
        if not isinstance(raw_aliases, list) or not raw_aliases:
            raise ValueError(f"missing aliases for {entry}")
        by_entry[entry] = record(entry, raw_aliases, item.get("engine", "pdflatex"))

    for folder, meta in packages(root):
        for kind, field in VERSION_FIELDS.items():
            entry = meta.get(field)
            if entry:
                safe_path(root, entry)
                item = by_entry.setdefault(entry, record(entry, []))
                if item["kind"] != kind:
                    raise ValueError(f"{folder.name}: wrong kind in {field}")
                if item["kind"] == "resume" and Path(item["entry"]).parts[2] == "baseline":
                    raise ValueError(
                        f"{folder.name}: target metadata must not claim the universal baseline; "
                        f"leave {field} empty until a targeted entry exists"
                    )
                item["aliases"].extend(
                    [f"{kind}:{meta['internal_id']}", f"{kind}:{folder.name}"]
                )

    cv_baselines = [
        item
        for item in by_entry.values()
        if item["kind"] == "resume" and Path(item["entry"]).parts[2] == "baseline"
    ]
    if (root / "RESUME_BASELINE.md").is_file():
        if len(cv_baselines) != 1:
            raise ValueError("workspace must register exactly one universal CV baseline")
        baseline = cv_baselines[0]
        if baseline["entry"] != BASELINE_ENTRY:
            raise ValueError(f"universal CV baseline must use {BASELINE_ENTRY}")
        if "baseline" not in baseline["aliases"]:
            raise ValueError("universal CV baseline requires 'baseline' alias")

    aliases: dict[str, dict] = {}
    for item in by_entry.values():
        safe_path(root, item["entry"])
        if item["jobname"] not in item["aliases"]:
            item["aliases"].append(item["jobname"])
        for alias in item["aliases"]:
            if not re.fullmatch(r"[a-z0-9:-]+", alias) or alias in aliases:
                raise ValueError(f"invalid/duplicate alias: {alias}")
            aliases[alias] = item
    return list(by_entry.values()), aliases


def dependencies(root: Path, entry: str) -> set[str]:
    """Read only public literal TeX inputs. Private input is an opaque dependency."""
    root = root.resolve()
    found: set[str] = set()
    if entry.endswith(".html"):
        safe_path(root, entry)
        if not (root / entry).is_file():
            raise ValueError(f"missing input: {entry}")
        return {entry}

    def visit(p: Path) -> None:
        rel = p.relative_to(root).as_posix()
        if rel in found:
            return
        found.add(rel)
        if rel == PRIVATE:
            return
        safe_path(root, rel)
        if not p.is_file():
            raise ValueError(f"missing input: {rel}")
        text = re.sub(r"(?<!\\)%[^\n]*", "", p.read_text(encoding="utf-8"))
        for value in re.findall(r"\\(?:input|include)\{([^{}]+)\}", text):
            name = value if value.endswith(".tex") else value + ".tex"
            options = [(p.parent / name).resolve(), (root / "src" / name).resolve()]
            child = next(
                (
                    q
                    for q in options
                    if q == (root / PRIVATE).resolve() or q.is_file()
                ),
                options[-1],
            )
            if not child.is_relative_to(root):
                raise ValueError(f"input escapes workspace: {value}")
            visit(child)

    visit((root / entry).resolve())
    return found


def validate(root: Path, require_pdfs: bool = False) -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    def error(msg: str) -> None:
        errors.append(msg)

    example_dir = root / "targets/example-company-role"
    if example_dir.is_dir():
        for name in ("metadata.yaml", "jd.md", "notes.md", "tailoring.md"):
            if not (example_dir / name).is_file():
                error(f"example-company-role: missing {name}")

    ps = packages(root)
    try:
        rs = rows(root)
    except ValueError as exc:
        error(str(exc))
        rs = []
    try:
        history_rows(root)
    except ValueError as exc:
        error(str(exc))

    ids: set[str] = set()
    entries: set[str] = set()
    for folder, m in ps:
        ident = m.get("internal_id")
        if (
            not isinstance(ident, str)
            or not re.fullmatch(r"[0-9]{3}", ident)
            or ident == "000"
        ):
            error(
                f"{folder.name}: internal_id must be a quoted three-digit string (001–999)"
            )
            ident = str(ident)
        if ident in ids:
            error(f"duplicate internal_id: {ident}")
        ids.add(ident)
        for name in ("jd.md", "notes.md", "tailoring.md", "metadata.yaml"):
            if not (folder / name).is_file():
                error(f"{folder.name}: missing {name}")
        for field in ("company", "role", "status"):
            if not isinstance(m.get(field), str) or not m[field].strip():
                error(f"{ident}: missing string {field}")
        if not all(isinstance(m.get(field), str) for field in ("company", "role", "status")):
            continue
        loc = m.get("location")
        if not isinstance(loc, (str, dict)) or (
            isinstance(loc, dict) and not isinstance(loc.get("display"), str)
        ):
            error(f"{ident}: location must be string or mapping with display")
        source = m.get("source_url") or m.get("source")
        if not isinstance(source, str) or not re.match(r"https?://[^\s]+$", source):
            error(f"{ident}: invalid source URL")
        if m.get("status") not in STATUS:
            error(f"{ident}: unknown status; explicitly extend STATUS mapping before use")
        matches = [r for r in rs if r[0] == ident]
        if len(matches) != 1:
            error(f"{ident}: expected exactly one PROJECT_STATUS row, got {len(matches)}")
            continue
        row = matches[0]
        if link(row[5]) != f"targets/{folder.name}/jd.md":
            error(f"{ident}: wrong JD link")
        if row[6] not in STATUS.get(m.get("status"), set()):
            error(f"{ident}: metadata/status mismatch")
        if link(row[4]) != source:
            warnings.append(f"{ident}: source URL presentation differs; review manually")
        for field, actual in [("company", row[1]), ("role", row[2]), ("location", row[3])]:
            expected = (
                loc.get("display")
                if field == "location" and isinstance(loc, dict)
                else m.get(field)
            )
            if expected != actual:
                warnings.append(f"{ident}: {field} display differs (human abbreviation allowed)")
        for kind, field in VERSION_FIELDS.items():
            value = m.get(field)
            pdf_link = link(row[7 if kind == "resume" else 8])
            if field not in m:
                error(f"{ident}: missing {field}; use empty string when not created")
            if value is None or not isinstance(value, str):
                error(f"{ident}: {field} must be string")
                continue
            if not value:
                if pdf_link:
                    error(f"{ident}: PDF linked but {field} empty")
                continue
            p = safe_path(root, value)
            rec = record(value, [])
            if rec["kind"] != kind:
                error(f"{ident}: wrong {field} kind")
            if "/targeted/" in value and not p.name.startswith(
                f"{ident}-" + ("resume-" if kind == "resume" else "cover-letter-")
            ):
                error(f"{ident}: filename prefix mismatch: {value}")
            if not p.is_file():
                error(f"{ident}: missing version {value}")
            entries.add(value)
            if pdf_link and pdf_link != rec["pdf"]:
                error(f"{ident}: output PDF link/name mismatch")
            if pdf_link or require_pdfs:
                if not (root / rec["pdf"]).is_file():
                    error(f"{ident}: missing PDF {rec['pdf']}")
            if not pdf_link:
                warnings.append(f"{ident}: {kind} exists but status PDF not linked (draft is allowed)")

    for r in rs:
        if r[0] not in ids:
            error(f"PROJECT_STATUS orphan ID: {r[0]}")

    records, _ = registry(root)
    registered = {r["entry"] for r in records}
    for rec in records:
        if (
            "/targeted/" in rec["entry"]
            and rec["entry"] != PLACEHOLDER_LETTER_ENTRY
            and rec["entry"] not in entries
        ):
            error(f"unowned targeted entry: {rec['entry']}")
        try:
            dependencies(root, rec["entry"])
        except ValueError as exc:
            error(str(exc))

    if (root / "versions").is_dir():
        for p in [*(root / "versions").rglob("*.tex"), *(root / "versions").rglob("*.html")]:
            rel = p.relative_to(root).as_posix()
            if rel not in registered:
                error(f"unregistered entry: {rel}")

    expected_pdfs = {r["pdf"] for r in records}
    for base in ("output/cv/targeted", "output/cover-letters/pdf/targeted"):
        if (root / base).is_dir():
            for p in (root / base).glob("*.pdf"):
                rel = p.relative_to(root).as_posix()
                if rel not in expected_pdfs:
                    error(f"orphan PDF: {rel}")

    groups = [
        2 if r[6] in GROUP_2_LABELS else 1 if r[6] in GROUP_1_LABELS else 0
        for r in rs
    ]
    if groups != sorted(groups):
        warnings.append(
            "PROJECT_STATUS group order differs; move rows to match status group order"
        )
    return {
        "targets": len(ps),
        "builds": len(records),
        "errors": errors,
        "warnings": warnings,
    }


def qa(pdf: Path, kind: str, log: Path | None = None) -> dict:
    try:
        import pdfplumber
    except ImportError as exc:
        raise ValueError(
            "Missing pdfplumber: install requirements.txt in .venv"
        ) from exc

    with pdfplumber.open(pdf) as document:
        pages = len(document.pages)
        page = document.pages[-1]
        height = page.height
        words = page.extract_words()
        lines: list[dict] = []
        for word in sorted(words, key=lambda w: (round(w["top"], 1), w["x0"])):
            if lines and abs(lines[-1]["top"] - word["top"]) < 3:
                lines[-1]["text"] += " " + word["text"]
                lines[-1]["bottom"] = max(lines[-1]["bottom"], word["bottom"])
            else:
                lines.append(
                    {
                        "top": word["top"],
                        "bottom": word["bottom"],
                        "text": word["text"],
                    }
                )

    warnings: list[str] = []
    errors: list[str] = []
    if pages != 1:
        errors.append(f"expected 1 page, got {pages}")
    ratio = None
    if kind == "letter":
        active = False
        body = []
        closed = False
        for line_el in lines:
            text_line = line_el["text"]
            if re.match(r"Dear\b", text_line):
                active = True
                continue
            if active and re.match(
                r"(Sincerely|Yours sincerely|Kind regards|Best regards)\b", text_line
            ):
                closed = True
                break
            if active:
                body.append(line_el)
        if body and closed:
            ratio = max(l["bottom"] for l in body) / height
            if ratio < 0.60:
                errors.append("letter body ends above 60% page-height line")
        else:
            warnings.append("REVIEW: letter body boundaries not recognized; measure visually")
    elif lines:
        content = [l for l in lines if l["top"] / height < 0.94]
        ratio = max((l["bottom"] for l in content), default=0) / height
        if ratio < 0.80:
            warnings.append(
                "REVIEW: resume content ends above 80% line; possible bottom whitespace"
            )
    else:
        warnings.append("REVIEW: no extractable text")

    counts = {}
    if log is not None:
        if not log.is_file():
            errors.append("missing build log")
        else:
            text = log.read_text(encoding="utf-8", errors="replace")
            counts = {
                name: len(re.findall(pattern, text, re.M))
                for name, pattern in {
                    "latex_errors": r"^!|LaTeX Error|Emergency stop|Fatal error",
                    "overfull": r"Overfull \\[hv]box",
                    "underfull": r"Underfull \\[hv]box",
                }.items()
            }
            if counts["latex_errors"]:
                errors.append("LaTeX errors found in log")
            if counts["overfull"] or counts["underfull"]:
                warnings.append("REVIEW: TeX box warnings; see local log")
    return {
        "pdf": str(pdf),
        "pages": pages,
        "body_end_fraction": round(ratio, 4) if ratio is not None else None,
        "log_counts": counts,
        "errors": errors,
        "warnings": warnings,
        "visual_review": "required for delivery",
    }


def chrome_binary() -> str:
    candidates = [
        os.environ.get("CHROME_BIN", ""),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        shutil.which("google-chrome") or "",
        shutil.which("chromium") or "",
    ]
    found = next((c for c in candidates if c and Path(c).is_file()), None)
    if not found:
        raise ValueError("Chrome not found; install Chrome or set CHROME_BIN")
    return found


def build_html(root: Path, rec: dict, publish: bool = False) -> int:
    """Render an HTML resume to PDF with headless Chrome, then run the same PDF QA."""
    review = root / "output/review" / rec["jobname"]
    review.mkdir(parents=True, exist_ok=True)
    destination = root / rec["pdf"] if publish else review / (rec["jobname"] + ".pdf")
    if publish and destination.exists():
        raise ValueError("refusing to overwrite an existing PDF snapshot; use review build")
    for name in (rec["jobname"] + ".pdf", "qa.json", "latex.log"):
        (review / name).unlink(missing_ok=True)
    source = (root / rec["entry"]).resolve()
    review_pdf = review / (rec["jobname"] + ".pdf")
    with tempfile.TemporaryDirectory(prefix="cv-html-") as temp:
        run = subprocess.run(
            [
                chrome_binary(),
                "--headless=new",
                "--disable-gpu",
                "--no-pdf-header-footer",
                "--virtual-time-budget=8000",
                f"--user-data-dir={temp}",
                f"--print-to-pdf={review_pdf}",
                source.as_uri(),
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )
    (review / "build.log").write_text(run.stdout + run.stderr, encoding="utf-8")
    if run.returncode or not review_pdf.is_file():
        raise ValueError(f"Chrome PDF export failed; inspect {review / 'build.log'}")
    report = qa(review_pdf, rec["kind"], None)
    if publish:
        if report["errors"]:
            raise ValueError("cannot publish failing QA; review build only")
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("xb") as out, review_pdf.open("rb") as inp:
            shutil.copyfileobj(inp, out)
    report["pdf"] = str(destination)
    (review / "qa.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 1 if report["errors"] else 0


def build(
    root: Path, rec: dict, public_header: bool = False, publish: bool = False
) -> int:
    if rec["engine"] == "chrome":
        return build_html(root, rec, publish)
    review = root / "output/review" / rec["jobname"]
    review.mkdir(parents=True, exist_ok=True)
    destination = root / rec["pdf"] if publish else review / (rec["jobname"] + ".pdf")
    refreshable_baseline = rec["entry"] == BASELINE_ENTRY
    if publish and destination.exists() and not refreshable_baseline:
        raise ValueError(
            "refusing to overwrite an existing PDF snapshot; use review build"
        )
    for name in (rec["jobname"] + ".pdf", "qa.json", "latex.log"):
        (review / name).unlink(missing_ok=True)

    with tempfile.TemporaryDirectory(prefix="cv-build-") as temp:
        stage = Path(temp)
        workroot = root
        if public_header:
            workroot = stage / "workspace"
            shutil.copytree(
                root / "src",
                workroot / "src",
                ignore=shutil.ignore_patterns("header.private.tex"),
            )
            shutil.copytree(root / "versions", workroot / "versions")
            (workroot / "src/sections/header.tex").write_text(
                "\\input{sections/header.template}\n", encoding="utf-8"
            )
        aux = stage / "aux"
        aux.mkdir()
        entry = workroot / rec["entry"]
        env = dict(
            os.environ,
            TEXINPUTS=str(workroot / "src") + ":" + os.environ.get("TEXINPUTS", ""),
        )
        runlog = review / "build.log"
        with runlog.open("w", encoding="utf-8") as out:
            run = subprocess.run(
                [
                    rec["engine"],
                    "-no-shell-escape",
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    "-recorder",
                    "-output-directory=" + str(aux),
                    "-jobname=" + rec["jobname"],
                    entry.name,
                ],
                cwd=entry.parent,
                env=env,
                stdout=out,
                stderr=subprocess.STDOUT,
            )
        log = aux / (rec["jobname"] + ".log")
        if log.exists():
            shutil.copy2(log, review / "latex.log")
        if run.returncode:
            raise ValueError(
                f"{rec['engine']} failed; inspect local log {runlog}; do not read private header"
            )
        pdf = aux / (rec["jobname"] + ".pdf")
        review_pdf = review / (rec["jobname"] + ".pdf")
        shutil.copy2(pdf, review_pdf)
        report = qa(review_pdf, rec["kind"], review / "latex.log")
        destination.parent.mkdir(parents=True, exist_ok=True)
        if publish and (
            report["errors"]
            or public_header
            or any("boundaries not recognized" in x for x in report["warnings"])
        ):
            raise ValueError(
                "cannot publish failing QA or placeholder header; review build only"
            )
        if publish:
            if refreshable_baseline:
                staged = destination.with_suffix(destination.suffix + ".tmp")
                staged.unlink(missing_ok=True)
                shutil.copy2(pdf, staged)
                os.replace(staged, destination)
            else:
                with destination.open("xb") as out, pdf.open("rb") as inp:
                    shutil.copyfileobj(inp, out)
        else:
            shutil.copy2(pdf, destination)
        report["pdf"] = str(destination)
        (review / "qa.json").write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps(report, indent=2))
        return 1 if report["errors"] else 0


def init_target(root: Path, args: argparse.Namespace) -> None:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.slug):
        raise ValueError("invalid slug")
    if not re.fullmatch(r"https?://[^\s|]+", args.url):
        raise ValueError("invalid URL")
    folder = root / "targets" / args.slug
    if folder.exists():
        raise ValueError("target already exists")
    ps = packages(root)
    if any(args.url == (m.get("source_url") or m.get("source")) for _, m in ps):
        raise ValueError("URL already registered")
    identifiers = [m["internal_id"] for _, m in ps]
    if (
        any(not isinstance(i, str) or not re.fullmatch(r"[0-9]{3}", i) for i in identifiers)
        or len(set(identifiers)) != len(identifiers)
    ):
        raise ValueError("fix invalid/duplicate IDs before initialization")
    ident = f"{max(map(int, identifiers), default=0) + 1:03}"
    if len(ident) != 3:
        raise ValueError("ID space exhausted; do not recycle IDs")
    statusfile = root / "PROJECT_STATUS.md"
    old = statusfile.read_text(encoding="utf-8")
    anchor = "|------|------|------|--------|--------|-----|------|----------|------------|"
    if old.count(anchor) != 1:
        raise ValueError("status table header changed; review insertion anchor")
    meta = {
        "internal_id": ident,
        "company": args.company or "待核实",
        "role": args.role or "待核实",
        "location": args.location or "待核实",
        "source_url": args.url,
        "date_saved": dt.date.today().isoformat(),
        "status": "draft",
        "resume_version": "",
        "cover_letter_version": "",
    }

    def cell(s: str) -> str:
        return s.replace("|", r"\|").replace("\n", " ")

    row = (
        f'| {ident} | {cell(meta["company"])} | {cell(meta["role"])} | '
        f'{cell(meta["location"])} | [链接]({args.url}) | '
        f'[JD](targets/{args.slug}/jd.md) | 待核实 | — | — |'
    )
    if not args.write:
        print(json.dumps(meta, ensure_ascii=False, indent=2))
        print(row)
        return
    folder.mkdir(parents=True)
    try:
        (folder / "metadata.yaml").write_text(
            "".join(
                f"{k}: {json.dumps(v, ensure_ascii=False)}\n" for k, v in meta.items()
            ),
            encoding="utf-8",
        )
        (folder / "jd.md").write_text(
            f"# JD capture pending\n\n"
            f"- **Internal ID:** `{ident}`\n"
            f"- **Source URL:** {args.url}\n"
            f"- **Captured Date:** {meta['date_saved']}\n\n"
            f"The posting has not been retrieved or verified yet. Follow `.agent/skills/job-intake/SKILL.md` to populate the verified English JD.\n",
            encoding="utf-8",
        )
        (folder / "notes.md").write_text(
            f"# Notes — {ident} {meta['company']} — {meta['role']}\n\n"
            f"URL registered locally on {meta['date_saved']}. Verify company, role, location, logistics, and posting status before tailoring.\n",
            encoding="utf-8",
        )
        (folder / "tailoring.md").write_text(
            f"# Tailoring — pending\n\n"
            f"No tailoring or application action performed yet. Follow `.agent/skills/job-prewrite/SKILL.md` before creating targeted LaTeX files.\n",
            encoding="utf-8",
        )
        statusfile.write_text(old.replace(anchor, anchor + "\n" + row, 1), encoding="utf-8")
    except Exception:
        statusfile.write_text(old, encoding="utf-8")
        shutil.rmtree(folder)
        raise
    print(f"Created {ident}: {folder}; JD and posting status await verification")


def bootstrap_workspace(root: Path, dry_run: bool = False) -> int:
    created: list[str] = []
    skipped: list[str] = []

    master_dir = root / "content/master"
    if master_dir.is_dir():
        for example_path in sorted(master_dir.glob("*.example.md")):
            target_name = example_path.name.replace(".example.md", ".md")
            target_path = master_dir / target_name
            rel = target_path.relative_to(root).as_posix()
            if target_path.exists():
                skipped.append(rel)
            else:
                if not dry_run:
                    shutil.copy2(example_path, target_path)
                created.append(rel)

    private_example = root / PRIVATE_EXAMPLE
    private_target = root / PRIVATE
    if private_example.is_file():
        if private_target.exists():
            skipped.append(PRIVATE)
        else:
            if not dry_run:
                shutil.copy2(private_example, private_target)
            created.append(PRIVATE)

    mode = "DRY-RUN" if dry_run else "BOOTSTRAP"
    for item in created:
        print(f"{mode} CREATED: {item}")
    for item in skipped:
        print(f"{mode} SKIPPED (already exists): {item}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("bootstrap", help="Initialize local untracked master files and private header from .example templates")
    p.add_argument("--dry-run", action="store_true")

    p = sub.add_parser("check", help="Validate metadata, PROJECT_STATUS.md, LaTeX dependencies, and PDF links")
    p.add_argument("--require-pdfs", action="store_true")
    p.add_argument("--json", action="store_true")

    sub.add_parser("list", help="List all registered build targets")

    p = sub.add_parser("build", help="Compile a target in an isolated directory and run PDF/log QA")
    p.add_argument("target")
    p.add_argument("--public-header", action="store_true")
    p.add_argument("--publish", action="store_true")

    p = sub.add_parser("affected", help="List or build targets affected by modified file paths")
    p.add_argument("paths", nargs="+")
    p.add_argument("--build", action="store_true")
    p.add_argument("--public-header", action="store_true")

    p = sub.add_parser("qa", help="Run standalone PDF page/density and LaTeX log QA")
    p.add_argument("pdf", type=Path)
    p.add_argument("--kind", choices=VERSION_FIELDS, required=True)
    p.add_argument("--log", type=Path)

    p = sub.add_parser("init", help="Allocate internal_id and scaffold a new job target package")
    p.add_argument("--url", required=True)
    p.add_argument("--slug", required=True)
    p.add_argument("--company")
    p.add_argument("--role")
    p.add_argument("--location")
    p.add_argument("--write", action="store_true")

    args = parser.parse_args()
    try:
        if args.command == "bootstrap":
            return bootstrap_workspace(ROOT, args.dry_run)
        if args.command == "check":
            report = validate(ROOT, args.require_pdfs)
            if args.json:
                print(json.dumps(report, ensure_ascii=False, indent=2))
            else:
                lines = [
                    f'{report["targets"]} targets; {report["builds"]} builds',
                    *[f"ERROR: {e}" for e in report["errors"]],
                    *[f"WARN: {w}" for w in report["warnings"]],
                    f'{len(report["errors"])} errors; {len(report["warnings"])} warnings',
                ]
                print("\n".join(lines))
            return bool(report["errors"])
        if args.command == "init":
            init_target(ROOT, args)
            return 0
        if args.command == "qa":
            report = qa(args.pdf, args.kind, args.log)
            print(json.dumps(report, indent=2))
            return bool(report["errors"])
        records, aliases = registry(ROOT)
        if args.command == "list":
            for rec in records:
                print(f'{rec["kind"]}\t{rec["aliases"][0]}\t{rec["entry"]}')
            return 0
        if args.command == "build":
            if args.target not in aliases:
                raise ValueError(f"unknown target: {args.target}; use list")
            return build(ROOT, aliases[args.target], args.public_header, args.publish)
        if args.command == "affected":
            changes = set()
            for p_str in args.paths:
                q = Path(p_str)
                q = q if q.is_absolute() else ROOT / q
                if not q.resolve().is_relative_to(ROOT.resolve()):
                    raise ValueError("changed path outside workspace")
                changes.add(q.resolve().relative_to(ROOT.resolve()).as_posix())
            global_change = any(
                p_rel.startswith("scripts/") or p_rel == "requirements.txt"
                for p_rel in changes
            )
            selected = []
            for rec in records:
                package_hit = any(
                    p_rel.startswith("targets/")
                    and any(
                        p_rel.startswith(f"targets/{a.split(':', 1)[1]}/")
                        for a in rec["aliases"]
                        if ":" in a
                    )
                    for p_rel in changes
                )
                if (
                    global_change
                    or package_hit
                    or changes & dependencies(ROOT, rec["entry"])
                ):
                    selected.append(rec)
            for rec in selected:
                print(rec["aliases"][0])
            if args.build:
                return max(
                    (build(ROOT, r, args.public_header) for r in selected), default=0
                )
            return 0
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
