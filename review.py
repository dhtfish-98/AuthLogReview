"""Review repeated failed logins in owner-supplied normalized JSONL logs."""
from __future__ import annotations
from collections import defaultdict
from datetime import datetime, timezone
from strict_json import loads

WINDOW_SECONDS = 300
THRESHOLD = 5


def review_text(text: str) -> list[dict[str, str]]:
    groups = defaultdict(list)
    for line_number, raw in enumerate(text.splitlines(), 1):
        if not raw.strip():
            continue
        try:
            event = loads(raw)
        except ValueError as exc:
            raise ValueError(f"invalid JSON on line {line_number}") from exc
        if not isinstance(event, dict) or not all(isinstance(event.get(key), str) and event[key].strip() for key in ("time", "account", "source", "result")):
            raise ValueError(f"invalid event on line {line_number}")
        try:
            instant = datetime.fromisoformat(event["time"].replace("Z", "+00:00"))
            if instant.tzinfo is None:
                raise ValueError("missing timezone")
            stamp = instant.astimezone(timezone.utc).timestamp()
        except (ValueError, OverflowError, OSError) as exc:
            raise ValueError(f"invalid timezone-aware time on line {line_number}") from exc
        if event["result"] not in ("success", "failure"):
            raise ValueError(f"invalid result on line {line_number}")
        if event["result"] == "failure":
            groups[(event["account"], event["source"])].append((stamp, line_number))
    findings = []
    for events in groups.values():
        events.sort()
        left = 0
        for right, (stamp, line_number) in enumerate(events):
            while stamp - events[left][0] > WINDOW_SECONDS:
                left += 1
            if right - left + 1 >= THRESHOLD:
                lines = sorted(number for _, number in events[left:right + 1])
                findings.append({"rule": "failure-burst", "location": "lines " + ",".join(map(str, lines)), "note": f"At least {THRESHOLD} failures within {WINDOW_SECONDS} seconds; identifiers are not emitted"})
                break
    return sorted(findings, key=lambda item: item["location"])
