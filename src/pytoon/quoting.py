import re


def needs_quoting_key(key: str) -> bool:
    if not key:
        return True

    if key.isdigit():
        return True

    if key.startswith("-"):
        return True

    if any(char in key for char in [" ", ",", ":", '"', "{", "}", "[", "]"]) or any(ord(c) < 32 for c in key):
        return True

    return False


def needs_quoting_value(value: str, delimiter: str) -> bool:
    if not value:
        return True

    if value.startswith(" ") or value.endswith(" "):
        return True

    if any(char in value for char in [delimiter, ":", '"', "\\"]) or any(ord(c) < 32 for c in value):
        return True

    if value.startswith("- "):
        return True

    if value in ["true", "false", "null"]:
        return True

    if re.match(r'^-?\d+(\.\d+)?([eE][+-]?\d+)?$', value):
        return True

    if value.startswith("0") and len(value) > 1 and value[1].isdigit():
        return True

    if re.match(r'^\[\d+\]', value) or re.match(r'^\{.+\}', value) or re.match(r'^\[\d+\]:.*', value):
        return True

    return False


def escape_string(s: str) -> str:
    result = []
    for char in s:
        if char == '"':
            result.append('\\"')
        elif char == "\\":
            result.append("\\\\")
        elif char == "\n":
            result.append("\\n")
        elif char == "\r":
            result.append("\\r")
        elif char == "\t":
            result.append("\\t")
        elif ord(char) < 32:
            result.append(f"\\u{ord(char):04x}")
        else:
            result.append(char)
    return "".join(result)


def quote_if_needed_key(key: str) -> str:
    if needs_quoting_key(key):
        return f'"{escape_string(key)}"'
    return key


def quote_if_needed_value(value: str, delimiter: str) -> str:
    if needs_quoting_value(value, delimiter):
        return f'"{escape_string(value)}"'
    return value
