import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "adopt_mamkin_process", ROOT / "scripts/adopt_mamkin_process.py"
)
ADOPT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ADOPT)


def run_git(root, *args):
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class AdoptMamkinProcessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base_dir = Path(self.temp.name)
        self.source = self.base_dir / "source"
        self.target = self.base_dir / "target"
        self.source.mkdir()
        self.target.mkdir()
        self.manifest = {
            "schemaVersion": 1,
            "templateOwned": [
                ".agents/skills/mamkin-*/**",
                "docs/process/*.md",
                "scripts/adopt_mamkin_process.py",
            ],
            "mixed": [
                "AGENTS.md",
                "README.md",
                ".mamkin/process-manifest.json",
                ".mamkin/template-version.json",
                "docs/process/naming-conventions.md",
            ],
            "projectOwned": ["docs/project/**", "features/**"],
            "neverSync": [".git/**", ".env", ".env.*"],
        }
        write(
            self.source / ".mamkin/process-manifest.json",
            json.dumps(self.manifest),
        )
        write(
            self.source / ".mamkin/template-version.json",
            json.dumps(
                {
                    "schemaVersion": 1,
                    "templateName": "mamkin-builder",
                    "templateRepo": "https://example.invalid/mamkin.git",
                    "initializedProject": False,
                }
            ),
        )
        write(self.source / "docs/process/example.md", "process\n")
        write(self.source / "docs/process/naming-conventions.md", "prefix TBD\n")
        write(self.source / "docs/project/brief.md", "placeholder\n")
        write(self.source / "AGENTS.md", "template instructions\n")
        write(self.source / "README.md", "template readme\n")
        write(self.source / "scripts/adopt_mamkin_process.py", "# process tool\n")
        write(self.source / ".env.example", "NAME=not-a-secret\n")
        self.init_repo(self.source)
        write(self.target / "product.txt", "existing product\n")
        write(self.target / "AGENTS.md", "existing project instructions\n")
        self.init_repo(self.target)

    def tearDown(self):
        self.temp.cleanup()

    def init_repo(self, root):
        run_git(root, "init", "-q")
        run_git(root, "config", "user.email", "tests@example.invalid")
        run_git(root, "config", "user.name", "Mamkin Tests")
        run_git(root, "add", ".")
        run_git(root, "commit", "-qm", "fixture")

    def review_values(self):
        source_head = ADOPT.git_head(self.source)
        target_head = ADOPT.git_head(self.target)
        entries = ADOPT.plan_adoption(self.source, self.target, self.manifest)
        digest = ADOPT.plan_digest(
            source_head,
            target_head,
            ADOPT.classify_repository(self.target),
            ADOPT.git_clean(self.source),
            ADOPT.git_clean(self.target),
            entries,
        )
        return source_head, target_head, digest

    def apply(self, source_head, target_head, digest):
        return ADOPT.main(
            [
                "--source",
                str(self.source),
                "--target",
                str(self.target),
                "--apply",
                "--expected-source-commit",
                source_head,
                "--expected-target-commit",
                target_head,
                "--expected-plan-digest",
                digest,
            ]
        )

    def test_review_is_non_mutating(self):
        before = set(ADOPT.inventory(self.target))
        self.assertEqual(
            ADOPT.main(["--source", str(self.source), "--target", str(self.target)]),
            0,
        )
        self.assertEqual(ADOPT.inventory(self.target), before)
        self.assertTrue(ADOPT.git_clean(self.target))

    def test_plan_seeds_only_missing_template_owned_files(self):
        entries = ADOPT.plan_adoption(self.source, self.target, self.manifest)
        actions = {entry["path"]: entry["action"] for entry in entries}
        self.assertEqual(actions["docs/process/example.md"], "seed")
        self.assertEqual(actions["AGENTS.md"], "manual-merge")
        self.assertEqual(actions["docs/process/naming-conventions.md"], "manual-create")
        self.assertEqual(actions["docs/project/brief.md"], "create-project-context")
        self.assertNotIn(".env.example", actions)

    def test_untracked_or_ignored_source_file_is_not_planned(self):
        write(self.source / "docs/process/untracked.md", "untracked\n")
        entries = ADOPT.plan_adoption(self.source, self.target, self.manifest)
        self.assertNotIn(
            "docs/process/untracked.md",
            {entry["path"] for entry in entries},
        )

    def test_existing_target_directory_is_protected_as_a_collision(self):
        (self.target / "docs/process/example.md").mkdir(parents=True)
        entries = ADOPT.plan_adoption(self.source, self.target, self.manifest)
        action = next(
            entry["action"]
            for entry in entries
            if entry["path"] == "docs/process/example.md"
        )
        self.assertEqual(action, "protect-existing")

    def test_existing_template_owned_path_is_protected_without_reading_or_overwrite(self):
        write(self.target / "docs/process/example.md", "project process\n")
        run_git(self.target, "add", ".")
        run_git(self.target, "commit", "-qm", "existing collision")
        source_head, target_head, digest = self.review_values()
        self.assertEqual(self.apply(source_head, target_head, digest), 0)
        self.assertEqual(
            (self.target / "docs/process/example.md").read_text(encoding="utf-8"),
            "project process\n",
        )
        target_manifest = ADOPT.load_json(self.target / ADOPT.MANIFEST_PATH)
        self.assertIn("docs/process/example.md", target_manifest["projectOwned"])

    def test_apply_seeds_process_and_metadata_but_preserves_mixed_files(self):
        source_head, target_head, digest = self.review_values()
        self.assertEqual(self.apply(source_head, target_head, digest), 0)
        self.assertEqual(
            (self.target / "AGENTS.md").read_text(encoding="utf-8"),
            "existing project instructions\n",
        )
        self.assertEqual(
            (self.target / "docs/process/example.md").read_text(encoding="utf-8"),
            "process\n",
        )
        self.assertFalse((self.target / "docs/project/brief.md").exists())
        metadata = ADOPT.load_json(self.target / ADOPT.VERSION_PATH)
        self.assertTrue(metadata["initializedProject"])
        self.assertEqual(metadata["adoptionMode"], "brownfield")
        self.assertEqual(metadata["templateCommit"], source_head)
        self.assertEqual(metadata["lastProcessSyncCommit"], source_head)
        self.assertEqual(metadata["adoptedFromProjectCommit"], target_head)

    def test_dirty_target_blocks_apply(self):
        source_head, target_head, digest = self.review_values()
        write(self.target / "uncommitted.txt", "dirty\n")
        self.assertEqual(self.apply(source_head, target_head, digest), 1)
        self.assertFalse((self.target / ADOPT.VERSION_PATH).exists())

    def test_changed_target_commit_invalidates_review(self):
        source_head, target_head, digest = self.review_values()
        write(self.target / "later.txt", "later\n")
        run_git(self.target, "add", ".")
        run_git(self.target, "commit", "-qm", "later target")
        self.assertEqual(self.apply(source_head, target_head, digest), 2)
        self.assertFalse((self.target / ADOPT.VERSION_PATH).exists())

    def test_changed_source_commit_invalidates_review(self):
        source_head, target_head, digest = self.review_values()
        write(self.source / "docs/process/later.md", "later\n")
        run_git(self.source, "add", ".")
        run_git(self.source, "commit", "-qm", "later source")
        self.assertEqual(self.apply(source_head, target_head, digest), 2)
        self.assertFalse((self.target / ADOPT.VERSION_PATH).exists())

    def test_dirty_source_blocks_apply(self):
        source_head, target_head, digest = self.review_values()
        write(self.source / "uncommitted.txt", "dirty\n")
        self.assertEqual(self.apply(source_head, target_head, digest), 1)
        self.assertFalse((self.target / ADOPT.VERSION_PATH).exists())

    def test_changed_plan_digest_is_rejected(self):
        source_head, target_head, _ = self.review_values()
        self.assertEqual(self.apply(source_head, target_head, "0" * 64), 2)
        self.assertFalse((self.target / ADOPT.VERSION_PATH).exists())

    def test_already_initialized_repository_routes_to_sync(self):
        write(
            self.target / ADOPT.VERSION_PATH,
            json.dumps({"schemaVersion": 1, "initializedProject": True}),
        )
        write(self.target / ADOPT.MANIFEST_PATH, json.dumps(self.manifest))
        self.assertEqual(ADOPT.classify_repository(self.target), "already-initialized")
        self.assertEqual(
            ADOPT.main(["--source", str(self.source), "--target", str(self.target)]),
            0,
        )

    def test_partial_adoption_is_detected_and_not_applied(self):
        write(self.target / "docs/process/agent-orchestration.md", "partial\n")
        run_git(self.target, "add", ".")
        run_git(self.target, "commit", "-qm", "partial adoption")
        source_head, target_head, digest = self.review_values()
        self.assertEqual(ADOPT.classify_repository(self.target), "partial-adoption")
        self.assertEqual(self.apply(source_head, target_head, digest), 1)

    def test_empty_repository_routes_to_init(self):
        empty = self.base_dir / "empty"
        empty.mkdir()
        run_git(empty, "init", "-q")
        run_git(empty, "config", "user.email", "tests@example.invalid")
        run_git(empty, "config", "user.name", "Mamkin Tests")
        run_git(empty, "commit", "--allow-empty", "-qm", "empty fixture")
        self.assertEqual(ADOPT.classify_repository(empty), "new-or-empty")
        self.assertEqual(
            ADOPT.main(["--source", str(self.source), "--target", str(empty)]),
            0,
        )

    def test_non_git_target_is_reviewable_but_not_applicable(self):
        non_git = self.base_dir / "non-git"
        non_git.mkdir()
        write(non_git / "product.txt", "product\n")
        self.assertEqual(
            ADOPT.main(["--source", str(self.source), "--target", str(non_git)]),
            0,
        )
        self.assertFalse((non_git / ADOPT.VERSION_PATH).exists())

    def test_nested_monorepo_directory_is_reviewable_but_not_applicable(self):
        nested = self.target / "packages" / "app"
        nested.mkdir(parents=True)
        write(nested / "product.txt", "nested product\n")
        run_git(self.target, "add", ".")
        run_git(self.target, "commit", "-qm", "nested app")
        source_head = ADOPT.git_head(self.source)
        target_head = ADOPT.git_head(self.target)
        entries = ADOPT.plan_adoption(self.source, nested, self.manifest)
        digest = ADOPT.plan_digest(
            source_head,
            target_head,
            ADOPT.classify_repository(nested),
            ADOPT.git_clean(self.source),
            ADOPT.git_clean(nested),
            entries,
        )
        self.assertEqual(
            ADOPT.main(
                [
                    "--source",
                    str(self.source),
                    "--target",
                    str(nested),
                    "--apply",
                    "--expected-source-commit",
                    source_head,
                    "--expected-target-commit",
                    target_head,
                    "--expected-plan-digest",
                    digest,
                ]
            ),
            1,
        )
        self.assertFalse((nested / ADOPT.VERSION_PATH).exists())

    def test_symlinked_source_process_path_blocks_apply(self):
        link = self.source / "docs/process/symlink.md"
        link.symlink_to("example.md")
        run_git(self.source, "add", ".")
        run_git(self.source, "commit", "-qm", "tracked process symlink")
        source_head, target_head, digest = self.review_values()
        entries = ADOPT.plan_adoption(self.source, self.target, self.manifest)
        action = next(entry["action"] for entry in entries if entry["path"].endswith("symlink.md"))
        self.assertEqual(action, "blocked-source")
        self.assertEqual(self.apply(source_head, target_head, digest), 1)
        self.assertFalse((self.target / ADOPT.VERSION_PATH).exists())

    def test_apply_rolls_back_created_files_after_write_failure(self):
        entries = ADOPT.plan_adoption(self.source, self.target, self.manifest)
        source_head = ADOPT.git_head(self.source)
        target_head = ADOPT.git_head(self.target)
        original_write = ADOPT.write_new_file
        calls = 0

        def failing_write(path, content):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("fixture failure")
            original_write(path, content)

        with mock.patch.object(ADOPT, "write_new_file", side_effect=failing_write):
            with self.assertRaises(OSError):
                ADOPT.apply_adoption(
                    self.source,
                    self.target,
                    self.manifest,
                    ADOPT.load_json(self.source / ADOPT.VERSION_PATH),
                    entries,
                    source_head,
                    target_head,
                )
        self.assertFalse((self.target / "docs/process/example.md").exists())
        self.assertFalse((self.target / ADOPT.MANIFEST_PATH).exists())
        self.assertFalse((self.target / ADOPT.VERSION_PATH).exists())


if __name__ == "__main__":
    unittest.main()
