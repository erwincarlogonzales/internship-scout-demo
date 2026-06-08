from agents.extractor import _parse_listings, _strip_code_fence


def test_strip_code_fence_removes_json_language_fence():
    text = '```json\n[{"role": "Intern"}]\n```'
    assert _strip_code_fence(text) == '[{"role": "Intern"}]'


def test_strip_code_fence_removes_bare_fence():
    text = '```\n[{"role": "Intern"}]\n```'
    assert _strip_code_fence(text) == '[{"role": "Intern"}]'


def test_strip_code_fence_leaves_unfenced_text_untouched():
    text = '[{"role": "Intern"}]'
    assert _strip_code_fence(text) == '[{"role": "Intern"}]'


def test_parse_listings_returns_list_for_valid_json():
    reply = '[{"role": "Intern", "company": "Acme"}]'
    assert _parse_listings(reply) == [{"role": "Intern", "company": "Acme"}]


def test_parse_listings_returns_empty_list_for_invalid_json(capsys):
    assert _parse_listings("this is not JSON") == []
