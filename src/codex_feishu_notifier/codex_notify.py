#!/usr/bin/env python3
import json
import os
import sys
from typing import Optional

if __package__ in (None, ""):
    sys.path.insert(0, str(__file__).split("/src/")[0] + "/src")

from codex_feishu_notifier.event import codex_event_from_notify
from codex_feishu_notifier.sender import send_codex_event
from codex_feishu_notifier.state import already_sent, log


def read_notification(argv) -> Optional[dict]:
    if len(argv) < 2:
        log("skip: no notification payload argument")
        return None

    try:
        return json.loads(argv[1])
    except json.JSONDecodeError as exc:
        log(f"skip: invalid notification json: {exc}")
        return None


def main(argv=None) -> int:
    argv = argv or sys.argv
    if os.getenv("CODEX_FEISHU_NOTIFY_ENABLED", "1") == "0":
        return 0

    notification = read_notification(argv)
    if not notification or notification.get("type") != "agent-turn-complete":
        return 0

    event = codex_event_from_notify(notification)
    if not event.assistant_result:
        log("skip: empty last-assistant-message")
        return 0

    key = event.turn_id or event.assistant_result
    if already_sent(key, event.assistant_result, "notify-sent.json"):
        log("skip: duplicate notification")
        return 0

    try:
        result = send_codex_event(event)
        if result.get("code") == 0:
            log(f"sent: {result.get('data', {}).get('message_id', 'unknown')}")
        else:
            log(f"send failed: {json.dumps(result, ensure_ascii=False)}")
    except Exception as exc:
        log(f"send exception: {exc}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
