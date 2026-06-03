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
