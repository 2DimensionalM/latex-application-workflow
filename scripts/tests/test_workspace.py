"""Unit tests for the LaTeX application workflow harness (disposable fixtures only)."""
from __future__ import annotations

import argparse
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import privacy_check
import workspace as w

HEADER = (
    "| 编号 | 公司 | 岗位 | 地点 | 招聘页 | JD | 进展 | 简历 | 求职信 |\n"
    "|------|------|------|--------|--------|-----|------|----------|------------|"
)
HISTORY_HEADER = (
    "| 日期 | 公司 | 岗位（或编号） | 动作 |\n"
    "|------|------|----------------|------|"
)


class WorkspaceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "targets").mkdir()
        (self.root / "scripts").mkdir()
        (self.root / "scripts/build-targets.json").write_text(
            '{"schema_version":1,"targets":[]}', encoding="utf-8"
        )
        (self.root / "PROJECT_STATUS.md").write_text(
            "# Test\n\n## 岗位总表（当前快照）\n\n"
            + HEADER
            + "\n\n## 历史动作（带日期）\n\n"
            + HISTORY_HEADER
            + "\n",
            encoding="utf-8",
        )

    def init(self, slug: str = "fixture-role", write: bool = True) -> Path:
        args = argparse.Namespace(
            slug=slug,
            url="https://example.com/jobs/" + slug,
            company=None,
            role=None,
            location=None,
            write=write,
        )
        with contextlib.redirect_stdout(io.StringIO()):
            w.init_target(self.root, args)
        return self.root / "targets" / slug

    def version(self, folder: Path) -> str:
        entry = "versions/cv/targeted/001-resume-fixture-role.tex"
        p = self.root / entry
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("\\documentclass{article}\n", encoding="utf-8")
        m = folder / "metadata.yaml"
        m.write_text(
            m.read_text(encoding="utf-8").replace(
                'resume_version: ""', "resume_version: " + json.dumps(entry)
            ),
            encoding="utf-8",
        )
        return entry

    def test_live_repository_checks_and_manifest(self) -> None:
        report = w.validate(w.ROOT)
        self.assertEqual(report["errors"], [])
        records, aliases = w.registry(w.ROOT)
        self.assertEqual(len(records), 3)
        self.assertIn("baseline", aliases)
        self.assertIn("resume-base", aliases)
        self.assertIn("letter-placeholder", aliases)

    def test_agent_agnostic_context_architecture(self) -> None:
        self.assertTrue((w.ROOT / "AGENTS.md").is_file())
        self.assertTrue((w.ROOT / "CLAUDE.md").is_file())
        self.assertTrue((w.ROOT / ".agent/README.md").is_file())
        self.assertTrue((w.ROOT / ".cursor/rules/project-memory.mdc").is_file())
        self.assertFalse((w.ROOT / ".cursor/skills").exists())
        expected_skills = {
            "master-and-baseline",
            "job-intake",
            "job-prewrite",
            "targeted-resume",
            "targeted-cover-letter",
            "status-and-publish",
        }
        for skill in expected_skills:
            self.assertTrue((w.ROOT / ".agent/skills" / skill / "SKILL.md").is_file())
        expected_rules = {
            "general.md",
            "intake.md",
            "tailoring.md",
            "content.md",
            "status.md",
            "structure.md",
            "build.md",
        }
        for rule in expected_rules:
            self.assertTrue((w.ROOT / ".agent/rules" / rule).is_file())

    def test_bootstrap_creates_untracked_files_without_overwriting(self) -> None:
        master = self.root / "content/master"
        master.mkdir(parents=True)
        (master / "profile.example.md").write_text("# Template Profile\n", encoding="utf-8")
        sec = self.root / "src/sections"
        sec.mkdir(parents=True)
        (sec / "header.private.tex.example").write_text("% Header Example\n", encoding="utf-8")

        with contextlib.redirect_stdout(io.StringIO()):
            w.bootstrap_workspace(self.root)
        self.assertTrue((master / "profile.md").is_file())
        self.assertTrue((sec / "header.private.tex").is_file())

        (master / "profile.md").write_text("# Custom User Data\n", encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            w.bootstrap_workspace(self.root)
        self.assertEqual(
            (master / "profile.md").read_text(encoding="utf-8"), "# Custom User Data\n"
        )

    def test_url_preview_has_no_writes(self) -> None:
        before = (self.root / "PROJECT_STATUS.md").read_bytes()
        self.init(write=False)
        self.assertEqual(list((self.root / "targets").iterdir()), [])
        self.assertEqual(before, (self.root / "PROJECT_STATUS.md").read_bytes())

    def test_init_quartet_status_history_and_next_id(self) -> None:
        p = self.init()
        self.init("fixture-two")
        self.assertEqual(len(list(p.iterdir())), 4)
        self.assertEqual(w.validate(self.root)["errors"], [])
        self.assertEqual(w.packages(self.root)[1][1]["internal_id"], "002")
        with self.assertRaises(ValueError):
            self.init()

    def test_duplicate_yaml_key_rejected(self) -> None:
        p = self.init() / "metadata.yaml"
        p.write_text(p.read_text(encoding="utf-8") + 'internal_id: "009"\n', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate YAML"):
            w.packages(self.root)

    def test_invalid_id_and_missing_quartet(self) -> None:
        p = self.init()
        m = p / "metadata.yaml"
        m.write_text(m.read_text(encoding="utf-8").replace('"001"', "1"), encoding="utf-8")
        (p / "notes.md").unlink()
        errors = w.validate(self.root)["errors"]
        self.assertTrue(any("three-digit" in e for e in errors))
        self.assertTrue(any("notes.md" in e for e in errors))

    def test_metadata_alone_registers_new_version(self) -> None:
        p = self.init()
        entry = self.version(p)
        records, aliases = w.registry(self.root)
        self.assertEqual(aliases["resume:001"]["entry"], entry)
        self.assertEqual(len(records), 1)
        self.assertEqual(w.validate(self.root)["errors"], [])

    def test_missing_version_and_wrong_pdf_fail(self) -> None:
        p = self.init()
        entry = self.version(p)
        f = self.root / "PROJECT_STATUS.md"
        f.write_text(
            f.read_text(encoding="utf-8").replace(
                "| — | — |", "| [简历](output/cv/targeted/wrong.pdf) | — |"
            ),
            encoding="utf-8",
        )
        (self.root / entry).unlink()
        errors = w.validate(self.root)["errors"]
        self.assertTrue(any("missing version" in e for e in errors))
        self.assertTrue(any("link/name mismatch" in e for e in errors))

    def test_html_entry_uses_chrome_engine(self) -> None:
        rec = w.record("versions/cv/targeted/001-resume-acme-intern-nl.html", ["resume:001"])
        self.assertEqual(rec["engine"], "chrome")
        self.assertEqual(rec["kind"], "resume")
        self.assertEqual(rec["pdf"], "output/cv/targeted/001-resume-acme-intern-nl.pdf")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "versions/cv/targeted").mkdir(parents=True)
            (root / rec["entry"]).write_text("<html></html>", encoding="utf-8")
            self.assertEqual(w.dependencies(root, rec["entry"]), {rec["entry"]})

    def test_render_html_parsers(self) -> None:
        import render_html as r
        self.assertEqual(r.compact_dates("Mar 2025 – Sep 2025"), "Mar – Sep 2025")
        self.assertEqual(r.compact_dates("Dec 2025 – Mar 2026"), "Dec 2025 – Mar 2026")
        body = "- **Dates:** Jan 2023 – Mar 2023\n- **Reusable Candidate Bullets:**\n  - `Did A`\n  - `Did B`\n"
        self.assertEqual(r.field(body, "Dates"), "Jan 2023 – Mar 2023")
        self.assertEqual(r.bullets(body), ["Did A", "Did B"])
        name, contact = r.render_header(
            "{\\Large \\textbf{Jane Doe}}\n{\\normalsize City \\quad\\textbar\\quad "
            "\\href{mailto:jd-mail}{jd-mail} \\quad\\textbar\\quad \\href{https://github.com/jd}{GitHub}}"
        )
        self.assertEqual(name, "Jane Doe")
        self.assertIn("City · jd-mail", contact)
        self.assertIn('href="https://github.com/jd"', contact)

    def test_path_escape_rejected(self) -> None:
        p = self.init()
        m = p / "metadata.yaml"
        m.write_text(
            m.read_text(encoding="utf-8").replace(
                'resume_version: ""', 'resume_version: "../escape.tex"'
            ),
            encoding="utf-8",
        )
        with self.assertRaises(ValueError):
            w.validate(self.root)

    def test_status_conflict_and_duplicate_row(self) -> None:
        self.init()
        f = self.root / "PROJECT_STATUS.md"
        f.write_text(
            f.read_text(encoding="utf-8").replace("| 待核实 |", "| 已投递 |"),
            encoding="utf-8",
        )
        self.assertTrue(any("status mismatch" in e for e in w.validate(self.root)["errors"]))
        row = next(
            l for l in f.read_text(encoding="utf-8").splitlines() if l.startswith("| 001")
        )
        f.write_text(
            f.read_text(encoding="utf-8").replace(row, row + "\n" + row), encoding="utf-8"
        )
        self.assertTrue(any("exactly one" in e for e in w.validate(self.root)["errors"]))

    def test_private_input_is_opaque(self) -> None:
        p = self.init()
        entry = self.version(p)
        (self.root / entry).write_text("\\input{sections/header.private}\n", encoding="utf-8")
        self.assertIn(w.PRIVATE, w.dependencies(self.root, entry))

    def test_single_universal_baseline_enforced(self) -> None:
        (self.root / "RESUME_BASELINE.md").write_text("# Baseline\n", encoding="utf-8")
        (self.root / "scripts/build-targets.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "targets": [
                        {
                            "entry": w.BASELINE_ENTRY,
                            "aliases": ["baseline", "resume-baseline"],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        records, aliases = w.registry(self.root)
        self.assertEqual(len(records), 1)
        self.assertEqual(aliases["baseline"]["entry"], w.BASELINE_ENTRY)

    def test_publish_refuses_existing_snapshot(self) -> None:
        p = self.init()
        entry = self.version(p)
        rec = w.record(entry, [])
        pdf = self.root / rec["pdf"]
        pdf.parent.mkdir(parents=True)
        pdf.write_bytes(b"SNAPSHOT")
        with patch("workspace.subprocess.run") as run:
            with self.assertRaisesRegex(ValueError, "overwrite"):
                w.build(self.root, rec, publish=True)
            run.assert_not_called()
        self.assertEqual(pdf.read_bytes(), b"SNAPSHOT")

    def test_letter_boundary_and_page_failure(self) -> None:
        def word(text: str, y: int) -> dict:
            return {"text": text, "top": y, "bottom": y + 10, "x0": 10}

        class Page:
            height = 1000

            def extract_words(self):
                return [
                    word("HEADER", 20),
                    word("Dear Hiring Team,", 100),
                    word("Body", 500),
                    word("Sincerely,", 700),
                    word("SIGNATURE", 800),
                ]

        class Doc:
            pages = [Page(), Page()]

            def __enter__(self):
                return self

            def __exit__(self, *a):
                pass

        with patch("pdfplumber.open", return_value=Doc()):
            report = w.qa(Path("fixture.pdf"), "letter")
        self.assertEqual(report["body_end_fraction"], 0.51)
        self.assertEqual(len(report["errors"]), 2)

    def test_privacy_path_blocks(self) -> None:
        self.assertIsNone(privacy_check.is_blocked_path("content/master/README.md"))
        self.assertIsNone(privacy_check.is_blocked_path("content/master/skills.example.md"))
        self.assertIsNotNone(privacy_check.is_blocked_path("content/master/skills.md"))
        self.assertIsNotNone(privacy_check.is_blocked_path("cn-campus-2027/README.md"))
        self.assertIsNotNone(privacy_check.is_blocked_path("src/sections/header.private.tex"))
        self.assertIsNone(privacy_check.is_blocked_path("src/sections/header.private.tex.example"))
        self.assertIsNotNone(privacy_check.is_blocked_path("targets/real-company/jd.md"))
        self.assertIsNone(privacy_check.is_blocked_path("targets/example-company-role/jd.md"))


if __name__ == "__main__":
    unittest.main()
