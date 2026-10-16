import importlib.util
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


class CoordinationContractTests(unittest.TestCase):
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
