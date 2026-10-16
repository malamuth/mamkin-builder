import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_coordination_contracts", ROOT / "scripts/validate_coordination_contracts.py"
)
CONTRACTS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONTRACTS)


def cross_repo_contract():
    return {
        "schemaVersion": 1,
        "contractKind": "cross-repo-compatibility",
        "producer": {
            "repository": "producer",
            "commit": "a" * 40,
            "sourceClosure": ["schemas/palette.json", "src/palette.py"],
        },
        "envelope": {
            "type": "palette-preview",
            "version": "1",
            "artifact": "out.json",
            "sha256": "b" * 64,
        },
        "consumer": {
            "repository": "consumer",
            "acceptedTypes": ["palette-preview"],
            "acceptedVersions": ["1"],
            "validatorCommand": ["python3", "scripts/validate_preview.py", "out.json"],
        },
        "preflight": {
            "status": "passed",
            "checkedAt": "2026-10-16T10:00:00Z",
            "evidence": "validator exited 0 against the exact producer commit",
        },
    }


def lane(lane_id, status="active"):
    return {
        "id": lane_id,
        "owner": f"owner-{lane_id}",
        "task": f"task-{lane_id}",
        "status": status,
        "worktree": f"/worktrees/{lane_id}",
        "branchOrCommit": f"codex/{lane_id}",
        "currentPacket": f"docs/packets/{lane_id}.md",
        "recoveryOwner": "coordinator",
    }


def lanes_contract():
    return {
        "schemaVersion": 1,
        "contractKind": "active-lanes",
        "updatedAt": "2026-10-16T10:00:00Z",
        "lanes": [lane("a")],
    }


class CoordinationContractTests(unittest.TestCase):
    def assert_cli_result(self, kind, path, expected_code, diagnostic=None):
        result = subprocess.run(
            [
                sys.executable, "-B",
                str(ROOT / "scripts/validate_coordination_contracts.py"),
                kind, str(path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, expected_code, result.stderr)
        if diagnostic is not None:
            self.assertTrue(result.stderr.startswith("ERROR:"), result.stderr)
            self.assertIn(diagnostic, result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertEqual(result.stdout, "")
        else:
            self.assertEqual(result.stderr, "")

    def test_rejects_invalid_schema_versions_without_mutation(self):
        for kind, factory, validate in (
            ("cross-repo", cross_repo_contract, CONTRACTS.validate_cross_repo),
            ("lanes", lanes_contract, CONTRACTS.validate_lanes),
        ):
            for version in (None, True, False, 1.0, 0.0, "1", 0, 2, [], {}):
                with self.subTest(kind=kind, version=version):
                    contract = factory()
                    contract["schemaVersion"] = version
                    original = copy.deepcopy(contract)
                    with self.assertRaisesRegex(ValueError, "schemaVersion"):
                        validate(contract)
                    self.assertEqual(contract, original)
                    with tempfile.TemporaryDirectory() as directory:
                        path = Path(directory) / "contract.json"
                        path.write_text(json.dumps(contract), encoding="utf-8")
                        self.assert_cli_result(kind, path, 1, "schemaVersion")
            with self.subTest(kind=kind, version="missing"):
                contract = factory()
                del contract["schemaVersion"]
                with self.assertRaisesRegex(ValueError, "schemaVersion"):
                    validate(contract)
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "contract.json"
                    path.write_text(json.dumps(contract), encoding="utf-8")
                    self.assert_cli_result(kind, path, 1, "schemaVersion")

    def test_rejects_invalid_lane_statuses_without_mutation(self):
        invalid_statuses = (
            None, True, False, 1, 1.0, [], ["active"], {},
            {"status": "active"}, "unknown",
        )
        for status in invalid_statuses:
            with self.subTest(status=status):
                contract = lanes_contract()
                contract["lanes"][0]["status"] = status
                original = copy.deepcopy(contract)
                with self.assertRaisesRegex(ValueError, r"lanes\[0\]\.status"):
                    CONTRACTS.validate_lanes(contract)
                self.assertEqual(contract, original)
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "contract.json"
                    path.write_text(json.dumps(contract), encoding="utf-8")
                    self.assert_cli_result("lanes", path, 1, "lanes[0].status")

    def test_valid_contracts_preserved_and_consumer_command_not_executed(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "executed"
            contract = cross_repo_contract()
            contract["consumer"]["validatorCommand"] = [
                sys.executable, "-c",
                f"from pathlib import Path; Path({str(marker)!r}).touch()",
            ]
            cases = [("cross-repo", contract, CONTRACTS.validate_cross_repo)]
            for status in sorted(CONTRACTS.LANE_STATUSES):
                inventory = lanes_contract()
                inventory["lanes"][0]["status"] = status
                cases.append(("lanes", inventory, CONTRACTS.validate_lanes))
            for kind, value, validate in cases:
                with self.subTest(kind=kind, contract=value):
                    original = copy.deepcopy(value)
                    validate(value)
                    self.assertEqual(value, original)
                    path = Path(directory) / f"{kind}.json"
                    path.write_text(json.dumps(value), encoding="utf-8")
                    self.assert_cli_result(kind, path, 0)
            self.assertFalse(marker.exists())

    def test_cli_reports_file_and_json_errors_without_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "contract.json"
            for kind in ("cross-repo", "lanes"):
                for payload, diagnostic in (
                    (b"{", "ERROR:"),
                    (b"\xff", "utf-8"),
                    (b"[]", "root must be an object"),
                ):
                    with self.subTest(kind=kind, payload=payload):
                        path.write_bytes(payload)
                        self.assert_cli_result(kind, path, 1, diagnostic)
                self.assert_cli_result(
                    kind, Path(directory) / "missing.json", 1, "missing.json"
                )

    def test_accepts_compatible_cross_repo_contract(self):
        CONTRACTS.validate_cross_repo(cross_repo_contract())

    def test_rejects_unaccepted_envelope_version(self):
        contract = cross_repo_contract()
        contract["consumer"]["acceptedVersions"] = ["2"]
        with self.assertRaisesRegex(ValueError, "version is not accepted"):
            CONTRACTS.validate_cross_repo(contract)

    def test_rejects_unpassed_preflight(self):
        contract = cross_repo_contract()
        contract["preflight"]["status"] = "blocked"
        with self.assertRaisesRegex(ValueError, "must be passed"):
            CONTRACTS.validate_cross_repo(contract)

    def test_accepts_two_unresolved_lanes_and_history(self):
        CONTRACTS.validate_lanes(
            {
                "schemaVersion": 1,
                "contractKind": "active-lanes",
                "updatedAt": "2026-10-16T10:00:00Z",
                "lanes": [lane("a"), lane("b", "blocked"), lane("old", "superseded")],
            }
        )

    def test_rejects_third_unresolved_lane(self):
        inventory = {
            "schemaVersion": 1,
            "contractKind": "active-lanes",
            "updatedAt": "2026-10-16T10:00:00Z",
            "lanes": [lane("a"), lane("b", "blocked"), lane("c", "parked")],
        }
        with self.assertRaisesRegex(ValueError, "at most two unresolved"):
            CONTRACTS.validate_lanes(inventory)


if __name__ == "__main__":
    unittest.main()
