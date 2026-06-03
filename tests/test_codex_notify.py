import json

from codex_feishu_notifier import codex_notify
from codex_feishu_notifier.codex_notify import read_notification


def test_read_notification():
    payload = {"type": "agent-turn-complete", "last-assistant-message": "done"}
    assert read_notification(["cmd", json.dumps(payload)]) == payload


def test_read_notification_without_payload():
    assert read_notification(["cmd"]) is None


def test_main_sends_composed_codex_event(monkeypatch, tmp_path):
    sent = []

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(codex_notify, "already_sent", lambda *args: False)
    monkeypatch.setattr(
        codex_notify,
        "send_codex_event",
        lambda event: sent.append(event) or {"code": 0},
    )

    payload = {
        "type": "agent-turn-complete",
        "cwd": "/tmp/project",
        "input-messages": ["finish this"],
        "last-assistant-message": "All done.",
        "turn-id": "turn-1",
    }

    assert codex_notify.main(["cmd", json.dumps(payload)]) == 0
    assert sent[0].project == "project"
    assert sent[0].user_prompt == "finish this"
