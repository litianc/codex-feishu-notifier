import argparse
import json
import sys
from pathlib import Path

from .config import get_feishu_config
from .feishu import FeishuBot
from .sender import send_text


DEFAULT_MESSAGE_TEXT = (
    "Codex task report\n"
    "Status: Success\n"
    "Details: codex-feishu-notifier manual test."
)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Send a Feishu text notification.")
    parser.add_argument("--text", default=DEFAULT_MESSAGE_TEXT)
    parser.add_argument("--text-file", help="Read message content from a UTF-8 file.")
    parser.add_argument("--stdin", action="store_true", help="Read message content from stdin.")
    parser.add_argument("--last-paragraph", action="store_true")
    parser.add_argument("--check", action="store_true", help="Verify Feishu credentials only.")
    return parser.parse_args(argv)


def resolve_text(args) -> str:
    if args.stdin:
        return sys.stdin.read()
    if args.text_file:
        return Path(args.text_file).read_text(encoding="utf-8")
    return args.text


def main(argv=None) -> int:
    args = parse_args(argv)

    try:
        if args.check:
            config = get_feishu_config()
            bot = FeishuBot(config["app_id"], config["app_secret"])
            bot.check_credentials()
            print("Feishu credentials are valid.")
            return 0

        result = send_text(resolve_text(args), last_paragraph=args.last_paragraph)
        if result.get("code") == 0:
            print("Message sent.")
            print(json.dumps(result.get("data", result), ensure_ascii=False, indent=2))
            return 0

        print(f"Feishu API returned: {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
