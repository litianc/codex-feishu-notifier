from .event import CodexEvent


def last_non_empty_paragraph(text: str) -> str:
    paragraphs = []
    current = []

    for line in text.splitlines():
        if line.strip():
            current.append(line.rstrip())
        elif current:
            paragraphs.append("\n".join(current).strip())
            current = []

    if current:
        paragraphs.append("\n".join(current).strip())

    return paragraphs[-1] if paragraphs else text.strip()


def compact_whitespace(text: str) -> str:
    return " ".join(text.split())


def truncate_text(text: str, limit: int) -> str:
    text = compact_whitespace(text)
    if limit <= 0 or len(text) <= limit:
        return text
    return text[: max(0, limit - 1)].rstrip() + "..."


def compact_result(text: str, limit: int = 280) -> str:
    return truncate_text(last_non_empty_paragraph(text), limit)


def compose_codex_message(
    event: CodexEvent,
    *,
    prompt_limit: int = 120,
    result_limit: int = 280,
    include_cwd: bool = True,
) -> str:
    result = compact_result(event.assistant_result, result_limit)
    if not result:
        return ""

    lines = [f"Codex completed - {event.project}"]

    prompt = truncate_text(event.user_prompt, prompt_limit)
    if prompt:
        lines.append(f"Task: {prompt}")

    lines.append(f"Result: {result}")

    if include_cwd and event.cwd:
        lines.append(f"Dir: {event.cwd}")

    return "\n".join(lines)
