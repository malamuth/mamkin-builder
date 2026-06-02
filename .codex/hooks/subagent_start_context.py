#!/usr/bin/env python3
import json
import sys


def main():
    try:
        event = json.load(sys.stdin)
    except Exception:
        event = {}

    agent_type = event.get("agent_type") or "subagent"
    message = (
        f"Mamkin subagent context for `{agent_type}`: read AGENTS.md, your assigned role card, "
        "the relevant feature/walkthrough docs, and the packet template. Return work to the "
        "coordinator using the delegated physical return path. If direct delivery is unavailable, "
        "start the local final packet with `Coordinator handoff - manual relay required for "
        "coordinator thread <id>`. Do not continue after emitting the packet."
    )

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SubagentStart",
            "additionalContext": message,
        }
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
