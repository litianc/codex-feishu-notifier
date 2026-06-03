from codex_feishu_notifier.codex_stop_hook import event_from_stop_payload
from codex_feishu_notifier.text import compose_codex_message


def test_event_from_stop_payload_uses_compact_message_fields():
    event = event_from_stop_payload(
        {
            "cwd": "/tmp/project",
            "input_messages": ["older", "finish hooks"],
            "thread_id": "thread-1",
            "turn_id": "turn-1",
        },
        "Changed files\n\nStop hook ready.",
    )

    assert compose_codex_message(event) == (
        "Codex completed - project\n"
        "Task: finish hooks\n"
        "Result: Stop hook ready.\n"
        "Dir: /tmp/project"
    )
