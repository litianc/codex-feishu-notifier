import os
from pathlib import Path


ENV_FILE_NAMES = (".env",)


def load_env_file(path: Path) -> None:
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def load_default_env() -> None:
    search_roots = [Path.cwd(), Path(__file__).resolve().parents[2]]
    for root in search_roots:
        for name in ENV_FILE_NAMES:
            load_env_file(root / name)


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def get_feishu_config() -> dict:
    load_default_env()
    return {
        "app_id": get_required_env("FEISHU_APP_ID"),
        "app_secret": get_required_env("FEISHU_APP_SECRET"),
        "receive_id": get_required_env("FEISHU_RECEIVE_ID"),
        "receive_id_type": os.getenv("FEISHU_RECEIVE_ID_TYPE", "open_id"),
    }
