import pytest
from pytoon import encode, EncodeOptions


def test_simple_object():
    data = {"id": 1, "name": "Ada", "active": True}
    result = encode(data)
    assert result == "id: 1\nname: Ada\nactive: true"


def test_nested_object():
    data = {"user": {"id": 123, "name": "Ada"}}
    result = encode(data)
    assert result == "user:\n  id: 123\n  name: Ada"


def test_primitive_array():
    data = {"tags": ["foo", "bar", "baz"]}
    result = encode(data)
    assert result == "tags[3]: foo,bar,baz"


def test_tabular_array():
    data = {
        "items": [
            {"sku": "A1", "qty": 2, "price": 9.99},
            {"sku": "B2", "qty": 1, "price": 14.5},
        ]
    }
    result = encode(data)
    expected = "items[2]{sku,qty,price}:\n  A1,2,9.99\n  B2,1,14.5"
    assert result == expected


def test_mixed_array():
    data = {"items": [1, {"a": 1}, "text"]}
    result = encode(data)
    expected = "items[3]:\n  - 1\n  - a: 1\n  - text"
    assert result == expected


def test_empty_object():
    data = {}
    result = encode(data)
    assert result == ""


def test_empty_array():
    data = {"items": []}
    result = encode(data)
    assert result == "items[0]:"


def test_root_array():
    data = ["x", "y", "z"]
    result = encode(data)
    assert result == "[3]: x,y,z"


def test_array_of_arrays():
    data = {"pairs": [[1, 2], [3, 4]]}
    result = encode(data)
    expected = "pairs[2]:\n  - [2]: 1,2\n  - [2]: 3,4"
    assert result == expected


def test_null_value():
    data = {"value": None}
    result = encode(data)
    assert result == "value: null"


def test_boolean_values():
    data = {"active": True, "deleted": False}
    result = encode(data)
    assert result == "active: true\ndeleted: false"


def test_number_normalization():
    data = {"zero": -0.0, "int": 1.0, "float": 1.5}
    result = encode(data)
    assert result == "zero: 0\nint: 1\nfloat: 1.5"


def test_tab_delimiter():
    data = {"tags": ["a", "b", "c"]}
    options = EncodeOptions(delimiter="\t")
    result = encode(data, options)
    assert result == "tags[3\t]: a\tb\tc"


def test_pipe_delimiter():
    data = {"tags": ["a", "b", "c"]}
    options = EncodeOptions(delimiter="|")
    result = encode(data, options)
    assert result == "tags[3|]: a|b|c"


def test_length_marker():
    data = {"tags": ["a", "b"]}
    options = EncodeOptions(length_marker="#")
    result = encode(data, options)
    assert result == "tags[#2]: a,b"


def test_custom_indent():
    data = {"user": {"id": 1}}
    options = EncodeOptions(indent=4)
    result = encode(data, options)
    assert result == "user:\n    id: 1"


def test_user_with_tags():
    data = {
        "user": {
            "id": 123,
            "name": "Ada",
            "tags": ["reading", "gaming"],
            "active": True,
        }
    }
    result = encode(data)
    expected = "user:\n  id: 123\n  name: Ada\n  tags[2]: reading,gaming\n  active: true"
    assert result == expected


def test_nested_config():
    data = {
        "config": {
            "server": {"host": "localhost", "port": 8080},
            "debug": True,
        }
    }
    result = encode(data)
    expected = "config:\n  server:\n    host: localhost\n    port: 8080\n  debug: true"
    assert result == expected


def test_list_with_objects():
    data = {
        "items": [
            {"id": 1, "name": "First"},
            {"id": 2, "name": "Second", "extra": True},
        ]
    }
    result = encode(data)
    expected = "items[2]:\n  - id: 1\n    name: First\n  - id: 2\n    name: Second\n    extra: true"
    assert result == expected


def test_string_with_spaces():
    data = {"note": "hello world"}
    result = encode(data)
    assert result == "note: hello world"


def test_nested_array_in_object():
    data = {
        "items": [
            {
                "users": [{"id": 1, "name": "Ada"}, {"id": 2, "name": "Bob"}],
                "status": "active",
            }
        ]
    }
    result = encode(data)
    expected = "items[1]:\n  - users[2]{id,name}:\n    1,Ada\n    2,Bob\n    status: active"
    assert result == expected
