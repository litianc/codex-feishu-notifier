import json

from codex_feishu_notifier.cli import main


def test_render_codex_payload_outputs_compact_message(tmp_path, capsys):
    payload_path = tmp_path / "payload.json"
    payload_path.write_text(
        json.dumps(
            {
                "type": "agent-turn-complete",
                "cwd": "/tmp/project",
                "input-messages": ["please finish the implementation"],
                "last-assistant-message": "Changed files\n\nImplementation complete.",
            }
        ),
        encoding="utf-8",
    )

    assert main(["--render-codex-payload", str(payload_path)]) == 0
    assert capsys.readouterr().out == (
        "Codex completed - project\n"
        "Task: please finish the implementation\n"
        "Result: Implementation complete.\n"
        "Dir: /tmp/project\n"
    )


def test_dry_run_codex_payload_alias(tmp_path, capsys):
    payload_path = tmp_path / "payload.json"
    payload_path.write_text(
        json.dumps(
            {
                "type": "agent-turn-complete",
                "cwd": "/tmp/project",
                "last-assistant-message": "Done.",
            }
        ),
        encoding="utf-8",
    )

    assert main(["--dry-run-codex-payload", str(payload_path)]) == 0
    assert "Result: Done." in capsys.readouterr().out
