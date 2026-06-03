# codex-feishu-notifier

Send Codex completion summaries to Feishu.

The recommended Codex integration is `notify`, because Codex passes an
`agent-turn-complete` JSON payload containing `last-assistant-message`.
The package also includes a `Stop` hook adapter for environments where hook
payloads include final-message fields or transcript paths.

## Install

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

## Configure

Copy the example file and fill in your own Feishu app credentials:

```bash
cp .env.example .env
```

Required variables:

```text
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=your_app_secret
FEISHU_RECEIVE_ID=ou_xxx
FEISHU_RECEIVE_ID_TYPE=open_id
```

Never commit `.env`.

## Send A Manual Test

```bash
codex-feishu-notifier --check
codex-feishu-notifier --text "hello from codex-feishu-notifier"
```

Send only the last paragraph from stdin:

```bash
printf 'Work done\n\nFinal summary only' \
  | codex-feishu-notifier --stdin --last-paragraph
```

## Codex Notify Integration

Add this to a Codex profile or config:

```toml
notify = ["codex-feishu-notify"]
```

This repository also includes `.codex/config.toml` with that project-local
setting. The file contains no secrets; `.env` still holds your Feishu app
credentials.

For a local editable checkout without installing scripts, use:

```toml
notify = ["python3", "/absolute/path/to/codex-feishu-notifier/src/codex_feishu_notifier/codex_notify.py"]
```

Codex calls the notify command with one JSON argument. This tool normalizes the
payload and sends a compact IM message containing:

- workspace name
- the latest user prompt, shortened for scanability
- the final non-empty assistant result paragraph
- working directory

Preview the message without sending it:

```bash
codex-feishu-notifier --render-codex-payload payload.json
# Equivalent:
codex-feishu-notifier --dry-run-codex-payload payload.json
```

## Codex Stop Hook Integration

Example `hooks.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "codex-feishu-stop-hook",
            "timeout": 15,
            "statusMessage": "Sending Feishu completion notice"
          }
        ]
      }
    ]
  }
}
```

Use Codex's `/hooks` UI to review and trust project-local hooks.

## Disable Temporarily

```bash
CODEX_FEISHU_NOTIFY_ENABLED=0 codex
```
