"""Summarize repeated failed logins in owner-supplied normalized JSONL logs."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
import json

WINDOW_SECONDS = 300
THRESHOLD = 5


def review_text(text: str) -> list[dict[str, str]]:
    groups = defaultdict(list)
    for line_number, raw in enumerate(text.splitlines(), 1):
        if not raw.strip():
            continue
        try:
            event = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON on line {line_number}") from exc
        if not isinstance(event, dict) or not all(isinstance(event.get(k), str) for k in ("time", "account", "source", "result")):
            raise ValueError(f"invalid event on line {line_number}")
        try:
            instant = datetime.fromisoformat(event["time"].replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(f"invalid time on line {line_number}") from exc
        if instant.tzinfo is None:
            raise ValueError(f"time needs timezone on line {line_number}")
        if event["result"] not in ("success", "failure"):
            raise ValueError(f"invalid result on line {line_number}")
        if event["result"] == "failure":
            groups[(event["account"], event["source"])].append(instant.astimezone(timezone.utc).timestamp())
    findings = []
    for group_number, ((account, source), stamps) in enumerate(sorted(groups.items()), 1):
        stamps.sort()
        left = 0
        for right, stamp in enumerate(stamps):
            while stamp - stamps[left] > WINDOW_SECONDS:
                left += 1
            if right - left + 1 >= THRESHOLD:
                findings.append({"rule": "failure-burst", "location": f"group[{group_number}]", "note": f"At least {THRESHOLD} failures within {WINDOW_SECONDS} seconds; identifiers are not emitted"})
                break
    return findings
