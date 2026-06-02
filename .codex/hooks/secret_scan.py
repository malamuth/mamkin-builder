#!/usr/bin/env python3
import json
import re
import sys


PATTERNS = [
    ("database URL", re.compile(r"(?i)\bDATABASE_URL\b\s*=")),
    ("Postgres URL", re.compile(r"postgres(?:ql)?://[^\s\"']+")),
    ("OpenAI-style key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("GitHub token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{20,}\b")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{20,}\b")),
    ("generic key assignment", re.compile(r"(?i)\b(?:api[_-]?key|secret|token|password)\b\s*=\s*[^\s\"']{8,}")),
]


def walk_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from walk_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk_strings(item)


def main():
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0

    text = "\n".join(walk_strings(event))
    hits = sorted({label for label, pattern in PATTERNS if pattern.search(text)})
    if not hits:
        return 0

    message = (
        "Mamkin hook warning: secret-shaped text detected ("
        + ", ".join(hits)
        + "). Do not paste or store secret values in chat, docs, commits, or hook output. "
        + "Use a human-approved local/provider secret path instead."
    )

    name = event.get("hook_event_name")
    if name == "UserPromptSubmit":
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": message,
            }
        }))
    else:
        print(json.dumps({
            "systemMessage": message,
            "hookSpecificOutput": {
                "hookEventName": name or "PostToolUse",
                "additionalContext": message,
            },
        }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
