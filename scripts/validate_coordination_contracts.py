#!/usr/bin/env python3
"""Read-only structural validation of coordination records; never executes evidence."""

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


def require_record(value, field):
    if not isinstance(value, dict):
        raise ValueError(f"{field} must be an object")
    return value


def require_enum(value, allowed, field):
    if not isinstance(value, str) or value not in allowed:
        raise ValueError(f"{field} must be one of {sorted(allowed)}")
    return value


def require_list(value, field):
    if not isinstance(value, list):
        raise ValueError(f"{field} must be an array")
    for index, item in enumerate(value):
        require_text(item, f"{field}[{index}]")
    if len(value) != len(set(value)):
        raise ValueError(f"{field} must contain unique entries")
    return value


def require_oid(value, field, sha256=False):
    require_text(value, field)
    pattern = r"[0-9a-fA-F]{64}" if sha256 else r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}"
    if not re.fullmatch(pattern, value):
        raise ValueError(f"{field} must be an exact {'SHA-256 digest' if sha256 else 'object id'}")
    return value


def require_header(value, kind):
    require_record(value, kind)
    if type(value.get("schemaVersion")) is not int or value["schemaVersion"] != 1:
        raise ValueError(f"{kind} schemaVersion must be the JSON integer 1")
    if value.get("contractKind") != kind:
        raise ValueError(f"contractKind must be {kind}")


def require_generation(value, field):
    if type(value) is not int or value < 1:
        raise ValueError(f"{field} must be a positive JSON integer")


def validate_state(value, field):
    require_record(value, field)
    for name in ("worktree", "branch"):
        require_text(value.get(name), f"{field}.{name}")
    require_oid(value.get("commit"), f"{field}.commit")
    require_list(value.get("dirtyPaths"), f"{field}.dirtyPaths")


def validate_portfolio(value):
    require_header(value, "project-coordinators")
    require_text(value.get("updatedAt"), "updatedAt")
    parent = require_record(value.get("parent"), "parent")
    for name in ("id", "repository", "coordinatorTask"):
        require_text(parent.get(name), f"parent.{name}")
    require_generation(parent.get("generation"), "parent.generation")
    projects = value.get("projects")
    if not isinstance(projects, list):
        raise ValueError("projects must be an array")
    ids, tasks, repositories, contexts = [parent["id"]], [parent["coordinatorTask"]], [parent["repository"]], []
    for index, project in enumerate(projects):
        field = f"projects[{index}]"
        require_record(project, field)
        for name in ("id", "projectContext", "repository", "coordinatorTask", "recoveryOwner"):
            require_text(project.get(name), f"{field}.{name}")
        require_generation(project.get("generation"), f"{field}.generation")
        require_enum(project.get("status"), {"active", "transitioning", "blocked", "retired"}, f"{field}.status")
        validate_state(project.get("state"), f"{field}.state")
        require_text(project["state"].get("sourcePacket"), f"{field}.state.sourcePacket")
        ledger = require_record(project.get("activeLanes"), f"{field}.activeLanes")
        for name in ("path", "checkedAt", "evidence"):
            require_text(ledger.get(name), f"{field}.activeLanes.{name}")
        ids.append(project["id"])
        tasks.append(project["coordinatorTask"])
        repositories.append(project["repository"])
        contexts.append(project["projectContext"])
    for name, entries in (("project ids", ids), ("coordinator tasks", tasks), ("repositories", repositories), ("project contexts", contexts)):
        if len(entries) != len(set(entries)):
            raise ValueError(f"{name} must be unique, including the parent where applicable")


def validate_transfer(value, registry=None):
    require_header(value, "coordinator-transfer")
    for name in ("projectId", "oldCoordinatorTask", "authorization"):
        require_text(value.get(name), name)
    require_generation(value.get("fromGeneration"), "fromGeneration")
    status = require_enum(value.get("status"), {"prepared", "receipt-verified", "promoted", "blocked"}, "status")
    new_task = value.get("newCoordinatorTask")
    if new_task is not None:
        require_text(new_task, "newCoordinatorTask")
        if new_task == value["oldCoordinatorTask"]:
            raise ValueError("newCoordinatorTask must differ from oldCoordinatorTask")
    baseline = value.get("baseline")
    validate_state(baseline, "baseline")
    require_text(baseline.get("packet"), "baseline.packet")
    require_oid(baseline.get("packetSha256"), "baseline.packetSha256", sha256=True)
    if baseline["dirtyPaths"]:
        require_text(baseline.get("dirtyPreservation"), "baseline.dirtyPreservation")
    lanes = require_record(value.get("lanes"), "lanes")
    validate_lanes(lanes)
    unresolved = {lane["id"] for lane in lanes["lanes"] if lane["status"] in UNRESOLVED_LANE_STATUSES}

    receipt = value.get("receipt")
    if status in {"receipt-verified", "promoted"}:
        require_text(new_task, "newCoordinatorTask")
        require_record(receipt, "receipt")
        expected = {"task": new_task, "projectId": value["projectId"], **{name: baseline[name] for name in ("worktree", "branch", "commit", "packetSha256")}}
        for name, expected_value in expected.items():
            if receipt.get(name) != expected_value:
                raise ValueError(f"receipt.{name} must match the transfer baseline/identity")
        accepted = require_list(receipt.get("acceptedLaneIds"), "receipt.acceptedLaneIds")
        if set(accepted) != unresolved:
            raise ValueError("receipt.acceptedLaneIds must match every unresolved lane exactly")
        if require_list(receipt.get("blockers"), "receipt.blockers"):
            raise ValueError("receipt.blockers must be empty before verification/promotion")
        for name in ("evidence", "sourceReconciliation", "nextSafeAction"):
            require_text(receipt.get(name), f"receipt.{name}")
        if baseline["dirtyPaths"]:
            require_text(receipt.get("dirtyStateEvidence"), "receipt.dirtyStateEvidence")

    if status == "promoted":
        retirement = require_record(value.get("retirement"), "retirement")
        if retirement.get("task") != value["oldCoordinatorTask"]:
            raise ValueError("retirement.task must match oldCoordinatorTask")
        require_enum(retirement.get("disposition"), {"renamed-stopped", "archived"}, "retirement.disposition")
        require_text(retirement.get("evidence"), "retirement.evidence")
        if registry is None:
            raise ValueError("promoted transfer requires --registry")
    if registry is not None:
        validate_portfolio(registry)
        project = next((p for p in registry["projects"] if p["id"] == value["projectId"]), None)
        if project is None:
            raise ValueError("projectId must exist in registry")
        promoted = status == "promoted"
        if project["coordinatorTask"] != (new_task if promoted else value["oldCoordinatorTask"]):
            raise ValueError("registry coordinatorTask does not match transfer authority")
        if project["generation"] != value["fromGeneration"] + int(promoted):
            raise ValueError("registry generation does not match transfer authority")
        if not promoted:
            allowed = {"transitioning", "blocked"} if status == "blocked" else {"transitioning"}
            if project["status"] not in allowed:
                raise ValueError("registry status must preserve paused transfer authority")
        if promoted:
            if project["status"] != "active":
                raise ValueError("promoted registry project must be active")
            for name in ("worktree", "branch", "commit", "dirtyPaths"):
                if project["state"][name] != baseline[name]:
                    raise ValueError(f"registry state.{name} must match promoted baseline")
            if project["state"]["sourcePacket"] != baseline["packet"]:
                raise ValueError("registry state.sourcePacket must match promoted baseline")


def validate_closeout(value):
    require_header(value, "lane-closeout")
    for name in ("task", "coordinatorTask", "worktree", "branchOrCommit", "reason", "checkedAt", "evidence"):
        require_text(value.get(name), name)
    action = require_enum(value.get("action"), {"retain", "archive-chat", "remove-worktree"}, "action")
    for name in ("dirtyPaths", "liveDependents", "pendingPackets"):
        entries = require_list(value.get(name), name)
        if action != "retain" and entries:
            raise ValueError(f"{name} must be empty before cleanup")
    integration = require_record(value.get("integration"), "integration")
    require_enum(integration.get("status"), {"pending", "verified", "not-required"}, "integration.status")
    require_text(integration.get("evidence"), "integration.evidence")
    preservation = require_record(value.get("preservation"), "preservation")
    require_enum(preservation.get("status"), {"pending", "verified"}, "preservation.status")
    for name in ("evidence", "ignoredFiles"):
        require_text(preservation.get(name), f"preservation.{name}")
    if action != "retain":
        require_text(value.get("authorization"), "authorization")
        if integration["status"] == "pending":
            raise ValueError("integration must be resolved before cleanup")
        if preservation["status"] != "verified":
            raise ValueError("preservation must be verified before cleanup")


def main(argv=None):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="kind", required=True)
    for kind in ("cross-repo", "lanes", "portfolio", "transfer", "closeout"):
        child = subparsers.add_parser(kind)
        child.add_argument("path")
        if kind == "transfer":
            child.add_argument("--registry")
    args = parser.parse_args(argv)

    try:
        value = load_object(args.path)
        if args.kind == "cross-repo":
            validate_cross_repo(value)
        elif args.kind == "lanes":
            validate_lanes(value)
        elif args.kind == "portfolio":
            validate_portfolio(value)
        elif args.kind == "transfer":
            registry = load_object(args.registry) if args.registry else None
            validate_transfer(value, registry)
        else:
            validate_closeout(value)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Validated {args.kind} contract: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
