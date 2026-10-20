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


def project():
    return {
        "id": "child", "projectContext": "app-child", "repository": "/repos/child",
        "coordinatorTask": "old-task", "generation": 1, "status": "transitioning",
        "state": {"worktree": "/worktrees/child", "branch": "codex/work",
                  "commit": "a" * 40, "dirtyPaths": [], "sourcePacket": "docs/project/reset.md"},
        "activeLanes": {"path": "docs/project/active-lanes.json",
                        "checkedAt": "2026-10-20T10:00:00Z", "evidence": "owning task receipt"},
        "recoveryOwner": "parent-task",
    }


def portfolio_contract():
    return {
        "schemaVersion": 1, "contractKind": "project-coordinators",
        "updatedAt": "2026-10-20T10:00:00Z",
        "parent": {"id": "parent", "repository": "/repos/parent", "coordinatorTask": "parent-task", "generation": 1},
        "projects": [project()],
    }


def transfer_contract(status="prepared"):
    child = project()
    value = {
        "schemaVersion": 1, "contractKind": "coordinator-transfer", "projectId": "child",
        "fromGeneration": 1, "oldCoordinatorTask": "old-task", "newCoordinatorTask": None,
        "status": status, "authorization": "human approved named child rollover",
        "baseline": {key: val for key, val in child["state"].items() if key != "sourcePacket"},
        "lanes": lanes_contract(), "receipt": None, "retirement": None,
    }
    value["baseline"].update(packet="docs/project/reset.md", packetSha256="b" * 64)
    if status in {"receipt-verified", "promoted"}:
        value["newCoordinatorTask"] = "new-task"
        value["receipt"] = {
            "task": "new-task", "projectId": "child",
            **{key: value["baseline"][key] for key in ("worktree", "branch", "commit", "packetSha256")},
            "acceptedLaneIds": ["a"], "blockers": [], "evidence": "actual first-turn receipt",
            "sourceReconciliation": "current sources reread, decisions and dirty state reconciled",
            "nextSafeAction": "collect existing worker packet",
        }
    if status == "promoted":
        value["retirement"] = {"task": "old-task", "disposition": "renamed-stopped", "evidence": "stop acknowledgement"}
    return value


def closeout_contract(action="retain"):
    return {
        "schemaVersion": 1, "contractKind": "lane-closeout", "task": "old-task",
        "coordinatorTask": "new-task", "worktree": "/worktrees/child", "branchOrCommit": "a" * 40,
        "action": action, "reason": "explicit resource disposition", "authorization": "human approved exact cleanup",
        "dirtyPaths": [], "liveDependents": [], "pendingPackets": [],
        "integration": {"status": "verified", "evidence": "accepted tip reachable from verified base"},
        "preservation": {"status": "verified", "evidence": "packets saved outside removed copy", "ignoredFiles": "none needed"},
        "checkedAt": "2026-10-20T10:00:00Z", "evidence": "fresh owning-task preflight",
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

    def test_portfolio_is_optional_and_child_count_is_not_lane_cap(self):
        inventory = portfolio_contract()
        inventory["projects"] = []
        CONTRACTS.validate_portfolio(inventory)
        for index in range(4):
            child = project()
            for name in ("id", "projectContext", "repository", "coordinatorTask"):
                child[name] += str(index)
            inventory["projects"].append(child)
        CONTRACTS.validate_portfolio(inventory)
        CONTRACTS.validate_lanes({**lanes_contract(), "lanes": []})

    def test_portfolio_rejects_duplicate_authorities_and_bad_state(self):
        for field in ("id", "projectContext", "repository", "coordinatorTask"):
            inventory = portfolio_contract()
            second = project()
            for name in ("id", "projectContext", "repository", "coordinatorTask"):
                if name != field:
                    second[name] += "-other"
            inventory["projects"].append(second)
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "unique"):
                CONTRACTS.validate_portfolio(inventory)
        for field in ("id", "repository", "coordinatorTask"):
            inventory = portfolio_contract()
            inventory["projects"][0][field] = inventory["parent"][field]
            with self.subTest(parent_collision=field), self.assertRaisesRegex(ValueError, "unique"):
                CONTRACTS.validate_portfolio(inventory)
        for generation in (True, 0, 1.0, "1", [], {}):
            inventory = portfolio_contract()
            inventory["projects"][0]["generation"] = generation
            with self.subTest(generation=generation), self.assertRaisesRegex(ValueError, "generation"):
                CONTRACTS.validate_portfolio(inventory)
        for field, value in (("commit", "short"), ("worktree", "TBD"), ("dirtyPaths", None)):
            inventory = portfolio_contract()
            inventory["projects"][0]["state"][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                CONTRACTS.validate_portfolio(inventory)

    def test_prepared_transfer_preserves_old_authority_and_all_lane_statuses(self):
        value = transfer_contract()
        value["lanes"]["lanes"] = [lane("a", "blocked"), lane("b", "parked"), lane("old", "complete")]
        CONTRACTS.validate_transfer(value, portfolio_contract())
        value["status"] = "blocked"
        CONTRACTS.validate_transfer(value, portfolio_contract())
        value["newCoordinatorTask"] = "old-task"
        with self.assertRaisesRegex(ValueError, "must differ"):
            CONTRACTS.validate_transfer(value)

    def test_receipt_requires_exact_identity_checkout_and_packet(self):
        CONTRACTS.validate_transfer(transfer_contract("receipt-verified"), portfolio_contract())
        for field in ("task", "projectId", "worktree", "branch", "commit", "packetSha256"):
            value = transfer_contract("receipt-verified")
            value["receipt"][field] = "wrong"
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, f"receipt.{field}"):
                CONTRACTS.validate_transfer(value)
        for field, bad in (("receipt", None), ("newCoordinatorTask", None)):
            value = transfer_contract("receipt-verified")
            value[field] = bad
            with self.subTest(field=field), self.assertRaises(ValueError):
                CONTRACTS.validate_transfer(value)

    def test_pre_promotion_registry_must_keep_transfer_paused(self):
        with tempfile.TemporaryDirectory() as directory:
            transfer_path = Path(directory) / "transfer.json"
            registry_path = Path(directory) / "registry.json"
            for status in ("prepared", "receipt-verified", "blocked"):
                transfer = transfer_contract(status)
                for registry_status in ("active", "retired", "transitioning", "blocked"):
                    registry = portfolio_contract()
                    registry["projects"][0]["status"] = registry_status
                    allowed = registry_status == "transitioning" or status == registry_status == "blocked"
                    with self.subTest(status=status, registry_status=registry_status):
                        if allowed:
                            CONTRACTS.validate_transfer(transfer, registry)
                        else:
                            with self.assertRaisesRegex(ValueError, "paused transfer authority"):
                                CONTRACTS.validate_transfer(transfer, registry)
                        transfer_path.write_text(json.dumps(transfer))
                        registry_path.write_text(json.dumps(registry))
                        result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/validate_coordination_contracts.py"), "transfer", str(transfer_path), "--registry", str(registry_path)], capture_output=True, text=True)
                        self.assertEqual(result.returncode, 0 if allowed else 1, result.stderr)
                        self.assertNotIn("Traceback", result.stderr)
    def test_receipt_requires_every_unresolved_lane_and_no_blocker(self):
        for accepted in ([], ["a", "unknown"], ["a", "a"]):
            value = transfer_contract("receipt-verified")
            value["receipt"]["acceptedLaneIds"] = accepted
            with self.subTest(accepted=accepted), self.assertRaisesRegex(ValueError, "acceptedLaneIds"):
                CONTRACTS.validate_transfer(value)
        value = transfer_contract("receipt-verified")
        value["lanes"]["lanes"] += [lane("b", "parked"), lane("history", "superseded")]
        with self.assertRaisesRegex(ValueError, "every unresolved"):
            CONTRACTS.validate_transfer(value)
        value["receipt"]["acceptedLaneIds"].append("b")
        CONTRACTS.validate_transfer(value)
        value["receipt"]["blockers"] = ["missing source"]
        with self.assertRaisesRegex(ValueError, "blockers"):
            CONTRACTS.validate_transfer(value)

    def test_dirty_baseline_requires_preservation_and_successor_reconciliation(self):
        value = transfer_contract("receipt-verified")
        value["baseline"]["dirtyPaths"] = ["docs/current.md", "untracked.json"]
        with self.assertRaisesRegex(ValueError, "dirtyPreservation"):
            CONTRACTS.validate_transfer(value)
        value["baseline"]["dirtyPreservation"] = "saved snapshot with tracked and untracked bytes"
        with self.assertRaisesRegex(ValueError, "dirtyStateEvidence"):
            CONTRACTS.validate_transfer(value)
        value["receipt"]["dirtyStateEvidence"] = "read snapshot and confirmed current dirty bytes"
        CONTRACTS.validate_transfer(value)

    def test_promotion_requires_retirement_and_matching_registry_generation(self):
        value = transfer_contract("promoted")
        with self.assertRaisesRegex(ValueError, "requires --registry"):
            CONTRACTS.validate_transfer(value)
        registry = portfolio_contract()
        with self.assertRaisesRegex(ValueError, "registry coordinatorTask"):
            CONTRACTS.validate_transfer(value, registry)
        child = registry["projects"][0]
        child.update(coordinatorTask="new-task", generation=2, status="active")
        CONTRACTS.validate_transfer(value, registry)
        mutations = [("generation", 3), ("coordinatorTask", "old-task"), ("status", "blocked")]
        for field, bad in mutations:
            changed = copy.deepcopy(registry)
            changed["projects"][0][field] = bad
            with self.subTest(field=field), self.assertRaises(ValueError):
                CONTRACTS.validate_transfer(value, changed)
        for field, bad in (("worktree", "/wrong"), ("commit", "c" * 40), ("sourcePacket", "old.md"), ("dirtyPaths", ["new.md"])):
            changed = copy.deepcopy(registry)
            changed["projects"][0]["state"][field] = bad
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "registry state"):
                CONTRACTS.validate_transfer(value, changed)
        value["retirement"] = None
        with self.assertRaisesRegex(ValueError, "retirement"):
            CONTRACTS.validate_transfer(value, registry)

    def test_cleanup_rejects_dirty_shared_or_uncollected_state(self):
        for action in ("archive-chat", "remove-worktree"):
            CONTRACTS.validate_closeout(closeout_contract(action))
            for field in ("dirtyPaths", "liveDependents", "pendingPackets"):
                value = closeout_contract(action)
                value[field] = ["successor-or-unfinished-work"]
                with self.subTest(action=action, field=field), self.assertRaisesRegex(ValueError, field):
                    CONTRACTS.validate_closeout(value)
            for field, value in (("authorization", None), ("integration", {"status": "pending", "evidence": "unknown"}), ("preservation", {"status": "pending", "evidence": "unknown", "ignoredFiles": "not copied"})):
                record = closeout_contract(action)
                record[field] = value
                with self.subTest(action=action, field=field), self.assertRaises(ValueError):
                    CONTRACTS.validate_closeout(record)

    def test_retention_does_not_require_cleanup_authority_or_clean_state(self):
        value = closeout_contract()
        value.update(authorization=None, dirtyPaths=["user.md"], liveDependents=["successor"], pendingPackets=["worker"])
        value["integration"]["status"] = "pending"
        value["preservation"]["status"] = "pending"
        CONTRACTS.validate_closeout(value)

    def test_new_records_cli_are_read_only_and_malformed_inputs_fail_cleanly(self):
        cases = [("portfolio", portfolio_contract(), CONTRACTS.validate_portfolio),
                 ("transfer", transfer_contract(), CONTRACTS.validate_transfer),
                 ("closeout", closeout_contract(), CONTRACTS.validate_closeout)]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.json"
            for kind, value, validate in cases:
                original = copy.deepcopy(value)
                validate(value)
                self.assertEqual(value, original)
                payload = json.dumps(value).encode()
                path.write_bytes(payload)
                self.assert_cli_result(kind, path, 0)
                self.assertEqual(path.read_bytes(), payload)
                for version in (True, 1.0, "1", None, 2, []):
                    bad = copy.deepcopy(value)
                    bad["schemaVersion"] = version
                    path.write_text(json.dumps(bad))
                    self.assert_cli_result(kind, path, 1, "schemaVersion")
                for bad in (b"{", b"[]", b"\xff"):
                    path.write_bytes(bad)
                    self.assert_cli_result(kind, path, 1, "ERROR:")
                self.assert_cli_result(kind, Path(directory) / "missing.json", 1, "missing.json")

    def test_transfer_cli_checks_the_explicit_registry_without_writing_it(self):
        with tempfile.TemporaryDirectory() as directory:
            transfer = Path(directory) / "transfer.json"
            registry = Path(directory) / "registry.json"
            transfer.write_text(json.dumps(transfer_contract("promoted")))
            value = portfolio_contract()
            value["projects"][0].update(coordinatorTask="new-task", generation=2, status="active")
            registry.write_text(json.dumps(value))
            original = registry.read_bytes()
            result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/validate_coordination_contracts.py"), "transfer", str(transfer), "--registry", str(registry)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(registry.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
