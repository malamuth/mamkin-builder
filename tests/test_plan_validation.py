import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "plan_validation", ROOT / "scripts/plan_validation.py"
)
PLAN_VALIDATION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PLAN_VALIDATION)


class ValidationPlannerTests(unittest.TestCase):
    def setUp(self):
        self.config = {
            "schemaVersion": 1,
            "always": ["diff"],
            "checks": {
                "diff": {"command": ["git", "diff", "--check"]},
                "prompt": {"command": ["python3", "prompt.py"]},
                "project": {"command": None},
            },
            "rules": [
                {
                    "patterns": ["docs/process/**", "AGENTS.md"],
                    "checks": ["prompt"],
                }
            ],
            "processOnlyPatterns": ["docs/**"],
            "unknownPathCheck": "project",
        }

    def test_prompt_change_selects_prompt_contracts(self):
        plan = PLAN_VALIDATION.build_plan(
            self.config, ["docs/process/agent-orchestration.md"]
        )
        self.assertEqual(set(plan), {"diff", "prompt"})

    def test_unmatched_docs_need_only_always_check(self):
        plan = PLAN_VALIDATION.build_plan(self.config, ["docs/project/brief.md"])
        self.assertEqual(set(plan), {"diff"})

    def test_unknown_product_path_selects_project_check(self):
        plan = PLAN_VALIDATION.build_plan(self.config, ["src/domain/order.py"])
        self.assertEqual(set(plan), {"diff", "project"})

    def test_rejects_shell_string_commands(self):
        self.config["checks"]["diff"]["command"] = "git diff --check"
        with self.assertRaisesRegex(ValueError, "argv array"):
            PLAN_VALIDATION.validate_config(self.config)

    def test_rejects_missing_unknown_path_check(self):
        self.config["unknownPathCheck"] = None
        with self.assertRaisesRegex(ValueError, "unknownPathCheck"):
            PLAN_VALIDATION.validate_config(self.config)

    def test_changed_paths_supports_repository_without_head(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            (root / "staged.txt").write_text("staged\n", encoding="utf-8")
            (root / "untracked.txt").write_text("untracked\n", encoding="utf-8")
            subprocess.run(["git", "add", "staged.txt"], cwd=root, check=True)
            self.assertEqual(
                PLAN_VALIDATION.changed_paths(root),
                ["staged.txt", "untracked.txt"],
            )


if __name__ == "__main__":
    unittest.main()
