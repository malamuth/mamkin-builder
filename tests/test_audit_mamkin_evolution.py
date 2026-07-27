import importlib.util
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "audit_mamkin_evolution", ROOT / "scripts/audit_mamkin_evolution.py"
)
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class EvolutionAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.project = self.base / "project"
        self.template = self.base / "template"
        self.project.mkdir()
        self.template.mkdir()
        self.catalog = {
            "schemaVersion": 1,
            "capabilities": [
                {
                    "id": "present",
                    "title": "Present",
                    "category": "test",
                    "paths": ["one.txt"],
                    "benefitHypothesis": "Test present state."
                },
                {
                    "id": "inactive",
                    "title": "Inactive",
                    "category": "test",
                    "paths": ["config.json"],
                    "activation": {
                        "path": "config.json",
                        "jsonPath": ["mode"],
                        "equals": "enabled"
                    },
                    "benefitHypothesis": "Test activation state."
                },
                {
                    "id": "partial",
                    "title": "Partial",
                    "category": "test",
                    "paths": ["a.txt", "b.txt"],
                    "benefitHypothesis": "Test partial state."
                },
                {
                    "id": "missing",
                    "title": "Missing",
                    "category": "test",
                    "paths": ["missing.txt"],
                    "benefitHypothesis": "Test missing state."
                }
            ]
        }
        write(
            self.template / ".mamkin/evolution-capabilities.json",
            json.dumps(self.catalog),
        )
        for path in ["one.txt", "config.json", "a.txt", "b.txt", "missing.txt"]:
            write(self.template / path, "{}\n")
        write(self.project / "one.txt", "present\n")
        write(self.project / "config.json", json.dumps({"mode": "disabled"}))
        write(self.project / "a.txt", "partial\n")
        write(
            self.project / ".agents/skills/project-helper/SKILL.md",
            "---\nname: project-helper\ndescription: Legacy-only test helper.\n---\n",
        )
        write(
            self.project / ".agents/skills/project-helper/references/rules.md",
            "# Rules\n",
        )
        write(
            self.project / "docs/project/decision-log.md",
            "Manual workaround. Validation gap. Manual workaround.\n",
        )
        write(
            self.project / "docs/project/surprise-log.md",
            "# Agent Notes\n\n## Surprise Log\n\n- First repeated mistake.\n"
            "- Second repeated mistake.\n\n## Unrelated\n\n- Not a candidate.\n",
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_capability_states_and_customizations(self):
        inventory = AUDIT.build_inventory(
            self.project, self.template, self.catalog
        )
        states = {
            item["id"]: item["state"] for item in inventory["capabilities"]
        }
        self.assertEqual(
            states,
            {
                "present": "present",
                "inactive": "inactive",
                "partial": "partial",
                "missing": "missing",
            },
        )
        self.assertEqual(
            inventory["project"]["customizations"]["customSkills"],
            [".agents/skills/project-helper/SKILL.md"],
        )
        skill = inventory["project"]["customizations"]["customSkillDetails"][0]
        self.assertEqual(skill["name"], "project-helper")
        self.assertEqual(skill["referenceFiles"], 1)
        self.assertEqual(skill["statusSignals"], ["legacy"])
        learning = inventory["project"]["customizations"]["knowledgeSources"]
        self.assertIn(
            {
                "path": "docs/project/surprise-log.md",
                "kind": "learning-log",
                "matchedHeadings": ["Surprise Log"],
                "candidateItems": 2,
            },
            learning,
        )
        self.assertGreaterEqual(
            inventory["project"]["textSignals"]["signals"]["manual-workaround"][
                "occurrences"
            ],
            2,
        )

    def test_learning_section_count_stops_at_peer_heading(self):
        headings, count = AUDIT.learning_section_counts(
            "## Lessons\n- one\n### Detail\n- two\n## Current Plan\n- ignored\n"
        )
        self.assertEqual(headings, ["Lessons"])
        self.assertEqual(count, 2)

    def test_cli_is_read_only_and_emits_json(self):
        before = {
            path.relative_to(self.project).as_posix(): path.read_bytes()
            for path in self.project.rglob("*")
            if path.is_file()
        }
        output = StringIO()
        with redirect_stdout(output):
            result = AUDIT.main(
                [
                    "--project",
                    str(self.project),
                    "--template",
                    str(self.template),
                ]
            )
        after = {
            path.relative_to(self.project).as_posix(): path.read_bytes()
            for path in self.project.rglob("*")
            if path.is_file()
        }
        self.assertEqual(result, 0)
        self.assertEqual(before, after)
        self.assertEqual(json.loads(output.getvalue())["mode"], "read-only-inventory")

    def test_catalog_rejects_duplicate_ids(self):
        duplicate = {
            "schemaVersion": 1,
            "capabilities": [
                self.catalog["capabilities"][0],
                self.catalog["capabilities"][0],
            ],
        }
        with self.assertRaisesRegex(ValueError, "unique"):
            AUDIT.validate_catalog(duplicate)

    def test_catalog_rejects_paths_outside_the_project(self):
        unsafe = {
            "schemaVersion": 1,
            "capabilities": [
                {
                    "id": "unsafe",
                    "title": "Unsafe",
                    "category": "test",
                    "paths": ["../outside.txt"],
                    "benefitHypothesis": "Should never be inspected.",
                }
            ],
        }
        with self.assertRaisesRegex(ValueError, "relative"):
            AUDIT.validate_catalog(unsafe)


if __name__ == "__main__":
    unittest.main()
