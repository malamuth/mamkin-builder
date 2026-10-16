#!/usr/bin/env python3
"""Fixed independent acceptance checks; pass the completed snapshot with --root."""

import argparse
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


def contract():
    return {
        "schemaVersion": 1,
        "contractKind": "cross-repo-compatibility",
        "producer": {"repository": "producer", "commit": "a" * 40, "sourceClosure": ["src.py"]},
        "envelope": {"type": "preview", "version": "1", "artifact": "out.json", "sha256": "b" * 64},
        "consumer": {
            "repository": "consumer", "acceptedTypes": ["preview"], "acceptedVersions": ["1"],
            "validatorCommand": ["python3", "validate.py"],
        },
        "preflight": {"status": "passed", "checkedAt": "2026-10-16T18:00:00Z", "evidence": "check passed"},
    }


def lanes():
    return {
        "schemaVersion": 1, "contractKind": "active-lanes", "updatedAt": "2026-10-16T18:00:00Z",
        "lanes": [{"id": "one", "owner": "worker", "task": "task-one", "status": "active",
                   "worktree": "/worktree", "branchOrCommit": "codex/fixture",
                   "currentPacket": "packet.md", "recoveryOwner": "parent"}],
    }


class Acceptance(unittest.TestCase):
    root = None
    target = None

    @classmethod
    def setUpClass(cls):
        script = cls.root / "scripts/validate_coordination_contracts.py"
        spec = importlib.util.spec_from_file_location("acceptance_target", script)
        cls.target = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.target)

    def run_cli(self, kind, contents):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "contract.json"
            path.write_bytes(contents)
            result = subprocess.run(
                [sys.executable, "-B", str(self.root / "scripts/validate_coordination_contracts.py"), kind, str(path)],
                capture_output=True, text=True, cwd=self.root,
            )
            self.assertEqual(path.read_bytes(), contents)
            return result

    def assert_cli_rejected(self, result, field=None):
        self.assertEqual(result.returncode, 1)
        self.assertIn("ERROR:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(result.stdout, "")
        if field:
            self.assertIn(field, result.stderr)

    def test_cross_repo_schema_types(self):
        for version in (True, False, 1.0, "1", None, [], {}, 0, 2):
            with self.subTest(version=repr(version)):
                value = contract()
                value["schemaVersion"] = version
                with self.assertRaisesRegex(ValueError, "schemaVersion"):
                    self.target.validate_cross_repo(value)

    def test_lane_schema_types(self):
        for version in (True, False, 1.0, "1", None, [], {}, 0, 2):
            with self.subTest(version=repr(version)):
                value = lanes()
                value["schemaVersion"] = version
                with self.assertRaisesRegex(ValueError, "schemaVersion"):
                    self.target.validate_lanes(value)

    def test_missing_schema_versions(self):
        for make, validate in ((contract, self.target.validate_cross_repo), (lanes, self.target.validate_lanes)):
            value = make()
            del value["schemaVersion"]
            with self.assertRaisesRegex(ValueError, "schemaVersion"):
                validate(value)

    def test_lane_status_types(self):
        for status in ([], {}, None, True, False, 1, 1.5, "unknown", "", " "):
            with self.subTest(status=repr(status)):
                value = lanes()
                value["lanes"][0]["status"] = status
                with self.assertRaisesRegex(ValueError, "status"):
                    self.target.validate_lanes(value)

    def test_all_existing_statuses_and_preservation(self):
        for status in ("active", "blocked", "parked", "superseded", "complete"):
            value = lanes()
            value["lanes"][0]["status"] = status
            original = copy.deepcopy(value)
            self.target.validate_lanes(value)
            self.assertEqual(value, original)

    def test_cross_repo_valid_and_preserved(self):
        value = contract()
        original = copy.deepcopy(value)
        self.target.validate_cross_repo(value)
        self.assertEqual(value, original)

    def test_empty_lanes_remain_valid(self):
        value = lanes()
        value["lanes"] = []
        self.target.validate_lanes(value)

    def test_unresolved_lane_cap_remains(self):
        value = lanes()
        for index, status in enumerate(("blocked", "parked"), 2):
            row = copy.deepcopy(value["lanes"][0])
            row.update(id=str(index), status=status)
            value["lanes"].append(row)
        with self.assertRaisesRegex(ValueError, "at most two"):
            self.target.validate_lanes(value)
        value["lanes"][2]["status"] = "superseded"
        self.target.validate_lanes(value)

    def test_cli_array_status(self):
        value = lanes()
        value["lanes"][0]["status"] = []
        self.assert_cli_rejected(self.run_cli("lanes", json.dumps(value).encode()), "status")

    def test_cli_object_status(self):
        value = lanes()
        value["lanes"][0]["status"] = {}
        self.assert_cli_rejected(self.run_cli("lanes", json.dumps(value).encode()), "status")

    def test_cli_boolean_schema(self):
        for kind, value in (("lanes", lanes()), ("cross-repo", contract())):
            value["schemaVersion"] = True
            self.assert_cli_rejected(self.run_cli(kind, json.dumps(value).encode()), "schemaVersion")

    def test_cli_float_schema(self):
        for kind, value in (("lanes", lanes()), ("cross-repo", contract())):
            value["schemaVersion"] = 1.0
            self.assert_cli_rejected(self.run_cli(kind, json.dumps(value).encode()), "schemaVersion")

    def test_cli_invalid_utf8_control(self):
        self.assert_cli_rejected(self.run_cli("lanes", b"\xff"))

    def test_cli_malformed_json_control(self):
        self.assert_cli_rejected(self.run_cli("lanes", b"{"))

    def test_cli_non_object_roots_control(self):
        for value in ([], None, "hello", 1, True):
            self.assert_cli_rejected(self.run_cli("lanes", json.dumps(value).encode()), "root")

    def test_cli_missing_file_control(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, "-B", str(self.root / "scripts/validate_coordination_contracts.py"),
                 "lanes", str(Path(directory) / "missing.json")], capture_output=True, text=True, cwd=self.root,
            )
        self.assert_cli_rejected(result)

    def test_cli_valid_contracts_control(self):
        for kind, value in (("lanes", lanes()), ("cross-repo", contract())):
            result = self.run_cli(kind, json.dumps(value).encode())
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stderr, "")
            self.assertIn("Validated", result.stdout)

    def test_validator_does_not_execute_declared_command(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "not-authorized"
            value = contract()
            value["consumer"]["validatorCommand"] = [sys.executable, "-c", f"open({str(marker)!r}, 'w').close()"]
            self.target.validate_cross_repo(value)
            result = self.run_cli("cross-repo", json.dumps(value).encode())
            self.assertEqual(result.returncode, 0)
            self.assertFalse(marker.exists())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    args, remaining = parser.parse_known_args()
    Acceptance.root = args.root.resolve()
    unittest.main(argv=[sys.argv[0]] + remaining)
