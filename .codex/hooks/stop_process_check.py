#!/usr/bin/env python3
import json
import subprocess
import sys


def run(args):
    try:
        return subprocess.run(
            args,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except Exception:
        return None


def main():
    try:
        event = json.load(sys.stdin)
    except Exception:
        event = {}

    if event.get("stop_hook_active"):
        return 0

    status = run(["git", "status", "--short"])
    if not status or status.returncode != 0 or not status.stdout.strip():
        return 0

    changed = status.stdout
    reminders = []

    if ".env" in changed or "DATABASE_URL" in changed:
        reminders.append("verify no `.env` or secret-bearing file is staged or mentioned in the final answer")

    if ".codex/" in changed:
        reminders.append("mention that changed project-local Codex hooks/rules/config may need trust or a new session before active threads use them")

    last = event.get("last_assistant_message") or ""
    if changed and "git diff --check" not in last:
        reminders.append("report whether `git diff --check` or an equivalent validation was run")

    if not reminders:
        return 0

    message = "Mamkin closeout reminder: " + "; ".join(reminders) + "."
    print(json.dumps({"continue": True, "systemMessage": message}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
