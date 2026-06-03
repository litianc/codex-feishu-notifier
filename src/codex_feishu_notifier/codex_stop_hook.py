#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(__file__).split("/src/")[0] + "/src")

from codex_feishu_notifier.event import CodexEvent, project_name_from_cwd
from codex_feishu_notifier.sender import send_codex_event
from codex_feishu_notifier.state import already_sent, log, mark_sent


def safe_string(value) -> str:
    return value if isinstance(value, str) else ""


def read_payload() -> dict:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        log(f"invalid hook payload json: {exc}", "stop-hook")
        return {}


def message_content_to_text(content) -> str:
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""

    parts = []
    for item in content:
        if isinstance(item, dict) and item.get("text"):
            parts.append(str(item["text"]))
    return "\n".join(parts).strip()


def extract_from_transcript(path: str) -> str:
    if not path:
        return ""

    transcript = Path(path)
    if not transcript.exists():
        log(f"transcript not found: {transcript}", "stop-hook")
        return ""

    latest_task_complete = ""
    latest_assistant = ""
    with transcript.open("r", encoding="utf-8") as file:
        for line in file:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            payload = event.get("payload")
            if not isinstance(payload, dict):
                continue

            if payload.get("type") == "task_complete":
                latest_task_complete = safe_string(payload.get("last_agent_message")).strip()
            elif (
                event.get("type") == "response_item"
                and payload.get("type") == "message"
                and payload.get("role") == "assistant"
            ):
                latest_assistant = message_content_to_text(payload.get("content"))

    return latest_task_complete or latest_assistant


def extract_message(payload: dict) -> str:
    keys = [
        "last_agent_message",
        "last-agent-message",
        "last_assistant_message",
        "last-assistant-message",
        "assistant_message",
        "assistant-message",
        "message",
        "response",
    ]
    for key in keys:
        value = safe_string(payload.get(key)).strip()
        if value:
            return value

    return extract_from_transcript(
        safe_string(payload.get("transcript_path") or payload.get("transcriptPath"))
    )


def extract_latest_prompt(payload: dict) -> str:
    value = payload.get("input_messages") or payload.get("input-messages")
    if isinstance(value, list):
        for item in reversed(value):
            text = safe_string(item).strip()
            if text:
                return text
    return safe_string(payload.get("prompt") or payload.get("user_prompt")).strip()


def event_from_stop_payload(payload: dict, message: str) -> CodexEvent:
    cwd = safe_string(payload.get("cwd") or payload.get("working_directory")).strip() or os.getcwd()
    return CodexEvent(
        event_type="stop",
        cwd=cwd,
        project=project_name_from_cwd(cwd),
        user_prompt=extract_latest_prompt(payload),
        assistant_result=message,
        thread_id=safe_string(payload.get("thread_id") or payload.get("thread-id")).strip(),
        turn_id=safe_string(payload.get("turn_id") or payload.get("turn-id")).strip(),
    )


def main() -> int:
    if os.getenv("CODEX_FEISHU_NOTIFY_ENABLED", "1") == "0":
        return 0

    payload = read_payload()
    event_name = safe_string(
        payload.get("hook_event_name")
        or payload.get("hookEventName")
        or payload.get("event")
        or payload.get("name")
    )
    if event_name and event_name != "Stop":
        return 0

    message = extract_message(payload).strip()
    if not message:
        log("skip: no final message found", "stop-hook")
        return 0

    key = safe_string(payload.get("session_id") or payload.get("sessionId")) or message
    if already_sent(key, message, "stop-hook-sent.json"):
        log("skip: duplicate final message", "stop-hook")
        return 0

    try:
        result = send_codex_event(event_from_stop_payload(payload, message))
        if result.get("code") == 0:
            mark_sent(key, message, "stop-hook-sent.json")
            log(f"sent: {result.get('data', {}).get('message_id', 'unknown')}", "stop-hook")
        else:
            log(f"send failed: {json.dumps(result, ensure_ascii=False)}", "stop-hook")
    except Exception as exc:
        log(f"send exception: {exc}", "stop-hook")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
