from codex_feishu_notifier.event import CodexEvent
from codex_feishu_notifier.text import compose_codex_message, last_non_empty_paragraph


def test_last_non_empty_paragraph():
    assert last_non_empty_paragraph("one\n\n two \n") == "two"


def test_last_non_empty_paragraph_falls_back_to_stripped_text():
    assert last_non_empty_paragraph("   ") == ""


def test_compose_codex_message_is_compact_and_contextual():
    message = compose_codex_message(
        CodexEvent(
            event_type="agent-turn-complete",
            cwd="/Users/me/project",
            project="project",
            user_prompt="Please implement the compact IM notification renderer.",
            assistant_result="Changed files\n\nImplemented renderer and tests.",
            thread_id="thread-1",
            turn_id="turn-1",
        )
    )

    assert message == (
        "Codex completed - project\n"
        "Task: Please implement the compact IM notification renderer.\n"
        "Result: Implemented renderer and tests.\n"
        "Dir: /Users/me/project"
    )
