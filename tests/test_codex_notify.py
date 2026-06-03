import json

from codex_feishu_notifier.codex_notify import read_notification


def test_read_notification():
    payload = {"type": "agent-turn-complete", "last-assistant-message": "done"}
    assert read_notification(["cmd", json.dumps(payload)]) == payload


def test_read_notification_without_payload():
    assert read_notification(["cmd"]) is None
