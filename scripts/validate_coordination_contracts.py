#!/usr/bin/env python3
"""Validate cross-repository preflight packets and active-lane inventories."""

import argparse
import json
import re
import sys
from pathlib import Path


UNRESOLVED_LANE_STATUSES = {"active", "blocked", "parked"}
LANE_STATUSES = UNRESOLVED_LANE_STATUSES | {"superseded", "complete"}


def load_object(path):
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be an object")
    return value


def require_text(value, field):
    if not isinstance(value, str) or not value.strip() or value.strip() == "TBD":
        raise ValueError(f"{field} must be a resolved non-empty string")
    return value


def require_string_list(value, field):
    if not isinstance(value, list) or not value:
        raise ValueError(f"{field} must be a non-empty array")
    for index, item in enumerate(value):
        require_text(item, f"{field}[{index}]")
    return value


def validate_cross_repo(value):
    if type(value.get("schemaVersion")) is not int or value.get("schemaVersion") != 1:
        raise ValueError("cross-repo schemaVersion must be the JSON integer 1")
    if value.get("contractKind") != "cross-repo-compatibility":
        raise ValueError("contractKind must be cross-repo-compatibility")

    producer = value.get("producer")
    envelope = value.get("envelope")
    consumer = value.get("consumer")
    preflight = value.get("preflight")
    for name, section in (
        ("producer", producer),
        ("envelope", envelope),
        ("consumer", consumer),
        ("preflight", preflight),
    ):
        if not isinstance(section, dict):
            raise ValueError(f"{name} must be an object")

    require_text(producer.get("repository"), "producer.repository")
    producer_commit = require_text(producer.get("commit"), "producer.commit")
    if not re.fullmatch(r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}", producer_commit):
        raise ValueError("producer.commit must be an exact 40- or 64-character object id")
    require_string_list(producer.get("sourceClosure"), "producer.sourceClosure")

    envelope_type = require_text(envelope.get("type"), "envelope.type")
    envelope_version = require_text(envelope.get("version"), "envelope.version")
    require_text(envelope.get("artifact"), "envelope.artifact")
    artifact_sha256 = require_text(envelope.get("sha256"), "envelope.sha256")
    if not re.fullmatch(r"[0-9a-fA-F]{64}", artifact_sha256):
        raise ValueError("envelope.sha256 must be an exact SHA-256 digest")

    require_text(consumer.get("repository"), "consumer.repository")
    accepted_types = require_string_list(consumer.get("acceptedTypes"), "consumer.acceptedTypes")
    accepted_versions = require_string_list(
        consumer.get("acceptedVersions"), "consumer.acceptedVersions"
    )
    command = consumer.get("validatorCommand")
    if not isinstance(command, list) or not command or not all(
        isinstance(part, str) and part for part in command
    ):
        raise ValueError("consumer.validatorCommand must be a non-empty argv array")
    if envelope_type not in accepted_types:
        raise ValueError("envelope.type is not accepted by the consumer")
    if envelope_version not in accepted_versions:
        raise ValueError("envelope.version is not accepted by the consumer")

    if preflight.get("status") != "passed":
        raise ValueError("preflight.status must be passed before dispatch")
    require_text(preflight.get("checkedAt"), "preflight.checkedAt")
    require_text(preflight.get("evidence"), "preflight.evidence")


def validate_lanes(value):
    if type(value.get("schemaVersion")) is not int or value.get("schemaVersion") != 1:
        raise ValueError("active-lanes schemaVersion must be the JSON integer 1")
    if value.get("contractKind") != "active-lanes":
        raise ValueError("contractKind must be active-lanes")
    require_text(value.get("updatedAt"), "updatedAt")
    lanes = value.get("lanes")
    if not isinstance(lanes, list):
        raise ValueError("lanes must be an array")

    ids = []
    unresolved = []
    for index, lane in enumerate(lanes):
        if not isinstance(lane, dict):
            raise ValueError(f"lanes[{index}] must be an object")
        lane_id = require_text(lane.get("id"), f"lanes[{index}].id")
        ids.append(lane_id)
        require_text(lane.get("owner"), f"lanes[{index}].owner")
        require_text(lane.get("task"), f"lanes[{index}].task")
        status = lane.get("status")
        if not isinstance(status, str) or status not in LANE_STATUSES:
            raise ValueError(f"lanes[{index}].status must be one of {sorted(LANE_STATUSES)}")
        require_text(lane.get("worktree"), f"lanes[{index}].worktree")
        require_text(lane.get("branchOrCommit"), f"lanes[{index}].branchOrCommit")
        require_text(lane.get("currentPacket"), f"lanes[{index}].currentPacket")
        require_text(lane.get("recoveryOwner"), f"lanes[{index}].recoveryOwner")
        if status in UNRESOLVED_LANE_STATUSES:
            unresolved.append(lane_id)

    if len(ids) != len(set(ids)):
        raise ValueError("lane ids must be unique")
    if len(unresolved) > 2:
        raise ValueError(f"at most two unresolved independent lanes are allowed: {unresolved}")


def main(argv=None):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="kind", required=True)
    for kind in ("cross-repo", "lanes"):
        child = subparsers.add_parser(kind)
        child.add_argument("path")
    args = parser.parse_args(argv)

    try:
        value = load_object(args.path)
        if args.kind == "cross-repo":
            validate_cross_repo(value)
        else:
            validate_lanes(value)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Validated {args.kind} contract: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
