from codex_feishu_notifier.event import codex_event_from_notify


def test_codex_event_from_notify_normalizes_payload():
    event = codex_event_from_notify(
        {
            "type": "agent-turn-complete",
            "cwd": "/tmp/example-repo",
            "input-messages": ["first", "finish the notifier"],
            "last-assistant-message": "Done\n\nFinal summary.",
            "thread-id": "thread-1",
            "turn-id": "turn-1",
        }
    )

    assert event.event_type == "agent-turn-complete"
    assert event.project == "example-repo"
    assert event.user_prompt == "finish the notifier"
    assert event.assistant_result == "Done\n\nFinal summary."
    assert event.thread_id == "thread-1"
    assert event.turn_id == "turn-1"
