from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class CodexEvent:
    event_type: str
    cwd: str
    project: str
    user_prompt: str
    assistant_result: str
    thread_id: str
    turn_id: str


def first_present(payload: Mapping[str, Any], *keys: str) -> Any:
    for key in keys:
        value = payload.get(key)
        if value not in (None, ""):
            return value
    return None


def as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def latest_input_message(payload: Mapping[str, Any]) -> str:
    value = first_present(payload, "input-messages", "input_messages", "inputMessages")
    if isinstance(value, list):
        for item in reversed(value):
            text = as_text(item)
            if text:
                return text
        return ""
    return as_text(value)


def project_name_from_cwd(cwd: str) -> str:
    if not cwd:
        return "workspace"
    return Path(cwd).name or "workspace"


def codex_event_from_notify(payload: Mapping[str, Any]) -> CodexEvent:
    cwd = as_text(first_present(payload, "cwd", "working_directory", "workingDirectory"))
    return CodexEvent(
        event_type=as_text(first_present(payload, "type", "event_type", "eventType")),
        cwd=cwd,
        project=project_name_from_cwd(cwd),
        user_prompt=latest_input_message(payload),
        assistant_result=as_text(
            first_present(
                payload,
                "last-assistant-message",
                "last_assistant_message",
                "lastAssistantMessage",
                "last-agent-message",
                "last_agent_message",
                "lastAgentMessage",
                "message",
                "status_message",
                "statusMessage",
            )
        ),
        thread_id=as_text(first_present(payload, "thread-id", "thread_id", "threadId")),
        turn_id=as_text(first_present(payload, "turn-id", "turn_id", "turnId")),
    )
