import pytest
from pytoon import encode


def test_quote_string_with_comma():
    data = {"note": "hello, world"}
    result = encode(data)
    assert result == 'note: "hello, world"'


def test_quote_boolean_looking_string():
    data = {"items": ["true", "false", "null"]}
    result = encode(data)
    assert result == 'items[3]: "true","false","null"'


def test_quote_number_looking_string():
    data = {"values": ["42", "3.14", "-5", "1e6"]}
    result = encode(data)
    assert result == 'values[4]: "42","3.14","-5","1e6"'


def test_quote_leading_zero_string():
    data = {"code": "007"}
    result = encode(data)
    assert result == 'code: "007"'


def test_quote_empty_string():
    data = {"text": ""}
    result = encode(data)
    assert result == 'text: ""'


def test_quote_string_with_leading_space():
    data = {"text": " padded"}
    result = encode(data)
    assert result == 'text: " padded"'


def test_quote_string_with_trailing_space():
    data = {"text": "padded "}
    result = encode(data)
    assert result == 'text: "padded "'


def test_quote_string_with_list_prefix():
    data = {"text": "- item"}
    result = encode(data)
    assert result == 'text: "- item"'


def test_quote_string_with_structural_tokens():
    data = {"values": ["[5]", "{key}", "[3]: x,y"]}
    result = encode(data)
    assert result == 'values[3]: "[5]","{key}","[3]: x,y"'


def test_quote_key_with_space():
    data = {"full name": "Ada"}
    result = encode(data)
    assert result == '"full name": Ada'


def test_quote_numeric_key():
    data = {"123": "value"}
    result = encode(data)
    assert result == '"123": value'


def test_quote_key_with_hyphen():
    data = {"-key": "value"}
    result = encode(data)
    assert result == '"-key": value'


def test_quote_key_with_colon():
    data = {"order:id": "123"}
    result = encode(data)
    assert result == '"order:id": "123"'


def test_quote_key_with_brackets():
    data = {"[index]": "value"}
    result = encode(data)
    assert result == '"[index]": value'


def test_unquoted_unicode():
    data = {"greeting": "hello 👋 world"}
    result = encode(data)
    assert result == "greeting: hello 👋 world"


def test_escape_quotes_in_string():
    data = {"text": 'say "hi"'}
    result = encode(data)
    assert result == 'text: "say \\"hi\\""'


def test_escape_newline():
    data = {"text": "line1\nline2"}
    result = encode(data)
    assert result == 'text: "line1\\nline2"'


def test_escape_tab():
    data = {"text": "a\tb"}
    result = encode(data)
    assert result == 'text: "a\\tb"'


def test_escape_backslash():
    data = {"path": "C:\\Users"}
    result = encode(data)
    assert result == 'path: "C:\\\\Users"'
