import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import workspace


class WorkspaceTests(unittest.TestCase):
    def test_registry_contains_only_generic_targets(self):
        records = workspace.registry()
        self.assertEqual(set(records), {"resume-base", "letter-placeholder"})

    def test_jobname_comes_from_entry_stem(self):
        for item in workspace.registry().values():
            self.assertEqual(item["jobname"], Path(item["entry"]).stem)

    def test_manifest_is_versioned(self):
        manifest = json.loads((workspace.ROOT / "scripts/build-targets.json").read_text())
        self.assertEqual(manifest["schema_version"], 1)


if __name__ == "__main__":
    unittest.main()

