#!/usr/bin/env python3
"""Run one explicitly enabled, local, argv-only formatter after write-capable tools."""

import json
import subprocess
from pathlib import Path


def main():
    root_result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=False,
        capture_output=True,
        text=True,
    )
    root = (
        Path(root_result.stdout.strip())
        if root_result.returncode == 0 and root_result.stdout.strip()
        else Path.cwd()
    )
    config_path = root / ".mamkin/validation-map.json"
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return 0

    post_edit = config.get("postEdit") or {}
    command = post_edit.get("command")
    if post_edit.get("mode") != "enabled" or not command:
        return 0
    if not isinstance(command, list) or not all(
        isinstance(part, str) and part for part in command
    ):
        print(json.dumps({"systemMessage": "Mamkin post-edit formatter has an invalid argv command."}))
        return 0

    result = subprocess.run(
        command,
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()
        if len(detail) > 500:
            detail = detail[:500] + "..."
        message = f"Mamkin post-edit formatter exited {result.returncode}."
        if detail:
            message += f" {detail}"
        print(json.dumps({"systemMessage": message}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
