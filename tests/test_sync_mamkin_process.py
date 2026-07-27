import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "sync_mamkin_process", ROOT / "scripts/sync_mamkin_process.py"
)
SYNC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SYNC)


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


class ProcessSyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base_dir = Path(self.temp.name)
        self.source = self.base_dir / "source"
        self.target = self.base_dir / "target"
        self.source.mkdir()
        self.manifest = {
            "schemaVersion": 1,
            "templateOwned": [
                "docs/process/*.md",
            ],
            "mixed": [
                "AGENTS.md",
                ".mamkin/process-manifest.json",
                ".mamkin/template-version.json",
            ],
            "projectOwned": ["docs/project/**"],
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
                    "templateCommit": "TBD",
                    "lastProcessSyncCommit": "TBD",
                }
            ),
        )
        write(self.source / "docs/process/example.md", "base\n")
        write(self.source / "AGENTS.md", "base mixed\n")
        write(self.source / "docs/project/brief.md", "template placeholder\n")
        self.init_repo(self.source)
        self.base_commit = run_git(self.source, "rev-parse", "HEAD")

        shutil.copytree(
            self.source,
            self.target,
            ignore=shutil.ignore_patterns(".git"),
        )
        metadata_path = self.target / ".mamkin/template-version.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        metadata["templateCommit"] = self.base_commit
        metadata["lastProcessSyncCommit"] = self.base_commit
        write(metadata_path, json.dumps(metadata))
        self.init_repo(self.target)

    def tearDown(self):
        self.temp.cleanup()

    def init_repo(self, root):
        run_git(root, "init", "-q")
        run_git(root, "config", "user.email", "tests@example.invalid")
        run_git(root, "config", "user.name", "Mamkin Tests")
        run_git(root, "add", ".")
        run_git(root, "commit", "-qm", "fixture")

    def commit_source(self, message="upstream"):
        run_git(self.source, "add", "-A")
        run_git(self.source, "commit", "-qm", message)
        return run_git(self.source, "rev-parse", "HEAD")

    def apply(self, source_head, *extra):
        return SYNC.main(
            [
                "--source",
                str(self.source),
                "--target",
                str(self.target),
                "--apply",
                "--expected-source-commit",
                source_head,
                *extra,
            ]
        )

    def test_review_is_non_mutating_and_marks_safe_update(self):
        write(self.source / "docs/process/example.md", "upstream\n")
        self.commit_source()
        plan = SYNC.plan_sync(
            self.source, self.target, self.manifest, self.base_commit
        )
        entry = next(item for item in plan if item["path"] == "docs/process/example.md")
        self.assertEqual(entry["action"], "safe-update")
        self.assertEqual(
            (self.target / "docs/process/example.md").read_text(encoding="utf-8"),
            "base\n",
        )

    def test_apply_requires_reviewed_commit_and_updates_safe_file(self):
        write(self.source / "docs/process/example.md", "upstream\n")
        source_head = self.commit_source()
        self.assertEqual(self.apply(source_head), 0)
        self.assertEqual(
            (self.target / "docs/process/example.md").read_text(encoding="utf-8"),
            "upstream\n",
        )
        metadata = json.loads(
            (self.target / ".mamkin/template-version.json").read_text(encoding="utf-8")
        )
        self.assertEqual(metadata["lastProcessSyncCommit"], source_head)

    def test_apply_rejects_unreviewed_source_commit(self):
        write(self.source / "docs/process/example.md", "upstream\n")
        self.commit_source()
        self.assertEqual(self.apply("0" * 40), 2)
        self.assertEqual(
            (self.target / "docs/process/example.md").read_text(encoding="utf-8"),
            "base\n",
        )

    def test_apply_rejects_dirty_source(self):
        write(self.source / "docs/process/example.md", "upstream\n")
        source_head = self.commit_source()
        write(self.source / "uncommitted.txt", "dirty\n")
        self.assertEqual(self.apply(source_head), 2)
        self.assertEqual(
            (self.target / "docs/process/example.md").read_text(encoding="utf-8"),
            "base\n",
        )

    def test_local_change_becomes_conflict_and_is_preserved(self):
        write(self.source / "docs/process/example.md", "upstream\n")
        source_head = self.commit_source()
        write(self.target / "docs/process/example.md", "local\n")
        run_git(self.target, "add", ".")
        run_git(self.target, "commit", "-qm", "local customization")
        self.assertEqual(self.apply(source_head), 1)
        self.assertEqual(
            (self.target / "docs/process/example.md").read_text(encoding="utf-8"),
            "local\n",
        )

    def test_project_owned_change_is_never_copied(self):
        write(self.source / "docs/project/brief.md", "upstream product data\n")
        source_head = self.commit_source()
        self.assertEqual(self.apply(source_head), 0)
        self.assertEqual(
            (self.target / "docs/project/brief.md").read_text(encoding="utf-8"),
            "template placeholder\n",
        )

    def test_upstream_manifest_expansion_requires_manual_merge(self):
        expanded = dict(self.manifest)
        expanded["templateOwned"] = [
            *self.manifest["templateOwned"],
            "scripts/new_process_tool.py",
        ]
        write(
            self.source / ".mamkin/process-manifest.json",
            json.dumps(expanded),
        )
        write(self.source / "scripts/new_process_tool.py", "print('new')\n")
        source_head = self.commit_source()
        self.assertEqual(self.apply(source_head), 1)
        self.assertFalse((self.target / "scripts/new_process_tool.py").exists())

    def test_project_only_mixed_change_is_preserved_without_blocking(self):
        write(self.target / "AGENTS.md", "project rules\n")
        run_git(self.target, "add", ".")
        run_git(self.target, "commit", "-qm", "adapt mixed file")
        write(self.source / "docs/process/example.md", "upstream\n")
        source_head = self.commit_source()
        self.assertEqual(self.apply(source_head), 0)
        self.assertEqual(
            (self.target / "AGENTS.md").read_text(encoding="utf-8"),
            "project rules\n",
        )

    def test_mixed_conflict_requires_exact_acknowledgement(self):
        write(self.target / "AGENTS.md", "project rules\n")
        run_git(self.target, "add", ".")
        run_git(self.target, "commit", "-qm", "adapt mixed file")
        write(self.source / "AGENTS.md", "upstream rules\n")
        source_head = self.commit_source()
        self.assertEqual(self.apply(source_head), 1)
        self.assertEqual(
            self.apply(source_head, "--acknowledge-mixed", "AGENTS.md"),
            0,
        )
        self.assertEqual(
            (self.target / "AGENTS.md").read_text(encoding="utf-8"),
            "project rules\n",
        )

    def test_first_sync_requires_explicit_two_way_acceptance(self):
        metadata_path = self.target / ".mamkin/template-version.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        metadata["templateCommit"] = "TBD"
        metadata["lastProcessSyncCommit"] = "TBD"
        write(metadata_path, json.dumps(metadata))
        run_git(self.target, "add", ".")
        run_git(self.target, "commit", "-qm", "unknown baseline")
        write(self.source / "docs/process/example.md", "upstream\n")
        source_head = self.commit_source()

        self.assertEqual(self.apply(source_head), 1)
        self.assertEqual(self.apply(source_head, "--accept-two-way"), 0)

    def test_deletion_requires_prune(self):
        (self.source / "docs/process/example.md").unlink()
        source_head = self.commit_source("remove process file")
        self.assertEqual(self.apply(source_head), 1)
        self.assertTrue((self.target / "docs/process/example.md").exists())
        self.assertEqual(self.apply(source_head, "--prune"), 0)
        self.assertFalse((self.target / "docs/process/example.md").exists())


if __name__ == "__main__":
    unittest.main()
