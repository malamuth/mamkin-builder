#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / ".mamkin/model-routing.json"


def load_config(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def select_profile(config, access, signals, requested_profile=None):
    order = config["profileOrder"]
    profiles = config["profiles"]
    signal_set = set(signals)
    unknown = signal_set - set(config["criticalSignals"]) - set(config["deepSignals"]) - set(config["economyRequirements"])
    if unknown:
        raise ValueError(f"unknown signals: {', '.join(sorted(unknown))}")

    critical = sorted(signal_set & set(config["criticalSignals"]))
    deep = sorted(signal_set & set(config["deepSignals"]))
    economy_ready = access == "read-only" and set(config["economyRequirements"]).issubset(signal_set)

    if critical:
        floor = "critical"
        reasons = critical
    elif deep:
        floor = "deep"
        reasons = deep
    elif economy_ready:
        floor = "economy"
        reasons = sorted(config["economyRequirements"])
    else:
        floor = "balanced"
        reasons = ["balanced-default"]

    selected = requested_profile or floor
    if selected not in profiles:
        raise ValueError(f"unknown requested profile: {selected}")
    if order.index(selected) < order.index(floor):
        raise ValueError(f"requested profile {selected} is below risk floor {floor}")

    profile = profiles[selected]
    return {
        "status": "selected",
        "riskFloor": floor,
        "selectedProfile": selected,
        "model": profile["model"],
        "reasoningEffort": profile["reasoningEffort"],
        "access": access,
        "agentPreset": profile["presets"][access],
        "reasons": reasons,
        "unavailableProfilePolicy": config["unavailableProfilePolicy"],
    }


def main():
    parser = argparse.ArgumentParser(description="Select a Mamkin reasoning profile from observable task signals.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--role", required=True)
    parser.add_argument("--access", required=True, choices=["read-only", "workspace-write"])
    parser.add_argument("--signal", action="append", default=[])
    parser.add_argument("--requested-profile")
    args = parser.parse_args()

    try:
        result = select_profile(load_config(args.config), args.access, args.signal, args.requested_profile)
    except (KeyError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "blocked", "error": str(error)}, sort_keys=True))
        return 2
    result["role"] = args.role
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
