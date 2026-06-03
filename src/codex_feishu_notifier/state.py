import hashlib
import json
from pathlib import Path


def default_state_dir() -> Path:
    return Path.home() / ".codex" / "codex-feishu-notifier"


def log(message: str, name: str = "notify") -> None:
    import time

    state_dir = default_state_dir()
    state_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with (state_dir / f"{name}.log").open("a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")


def already_sent(key: str, message: str, state_name: str = "sent.json") -> bool:
    digest = hashlib.sha256(message.encode("utf-8")).hexdigest()
    state_file = default_state_dir() / state_name

    try:
        state = json.loads(state_file.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        state = {}

    if state.get(key) == digest:
        return True

    state_file.parent.mkdir(parents=True, exist_ok=True)
    state[key] = digest
    state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    return False
