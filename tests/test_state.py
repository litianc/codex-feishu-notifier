from codex_feishu_notifier import state


def test_mark_sent_records_successful_delivery(tmp_path, monkeypatch):
    monkeypatch.setattr(state, "default_state_dir", lambda: tmp_path)

    assert not state.already_sent("turn-1", "done", "sent.json")

    state.mark_sent("turn-1", "done", "sent.json")

    assert state.already_sent("turn-1", "done", "sent.json")
    assert not state.already_sent("turn-1", "changed", "sent.json")
