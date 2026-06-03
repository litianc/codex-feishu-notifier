from codex_feishu_notifier.text import last_non_empty_paragraph


def test_last_non_empty_paragraph():
    assert last_non_empty_paragraph("one\n\n two \n") == " two"


def test_last_non_empty_paragraph_falls_back_to_stripped_text():
    assert last_non_empty_paragraph("   ") == ""
