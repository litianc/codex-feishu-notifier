from .config import get_feishu_config
from .event import CodexEvent
from .feishu import FeishuBot
from .text import compose_codex_message, last_non_empty_paragraph


def send_text(text: str, last_paragraph: bool = False) -> dict:
    text = last_non_empty_paragraph(text) if last_paragraph else text.strip()
    if not text:
        raise RuntimeError("Message text is empty")

    config = get_feishu_config()
    bot = FeishuBot(config["app_id"], config["app_secret"])
    return bot.send_text(
        receive_id=config["receive_id"],
        receive_id_type=config["receive_id_type"],
        text=text,
    )


def send_codex_event(event: CodexEvent) -> dict:
    text = compose_codex_message(event)
    if not text:
        raise RuntimeError("Message text is empty")

    config = get_feishu_config()
    bot = FeishuBot(config["app_id"], config["app_secret"])
    return bot.send_text(
        receive_id=config["receive_id"],
        receive_id_type=config["receive_id_type"],
        text=text,
    )
