import math
from datetime import datetime, date
from decimal import Decimal
from typing import Any

from .types import EncodeOptions
from .quoting import quote_if_needed_key, quote_if_needed_value


def normalize_number(value: float | int) -> float | int | None:
    if isinstance(value, bool):
        return value

    if math.isnan(value) or math.isinf(value):
        return None

    if isinstance(value, float) and value == -0.0:
        return 0

    return value


def can_use_tabular(items: list) -> bool:
    if not items:
        return False

    if not all(isinstance(item, dict) for item in items):
        return False

    if not all(item for item in items):
        return False

    first_keys = set(items[0].keys())
    if not all(set(item.keys()) == first_keys for item in items):
        return False

    for item in items:
        for value in item.values():
            if isinstance(value, (dict, list)):
                return False

    return True


def format_primitive_value(value: Any, delimiter: str) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        normalized = normalize_number(value)
        if normalized is None:
            return "null"
        if isinstance(normalized, float):
            if normalized == int(normalized):
                return str(int(normalized))
            return str(normalized)
        return str(normalized)
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, (datetime, date)):
        return quote_if_needed_value(value.isoformat(), delimiter)
    if isinstance(value, str):
        return quote_if_needed_value(value, delimiter)
    return "null"


def format_primitive_array(items: list, delimiter: str, length_marker: str | bool, indent_level: int) -> str:
    length_prefix = f"#{len(items)}" if length_marker else str(len(items))

    if delimiter == "\t":
        delimiter_marker = "\t"
    elif delimiter == "|":
        delimiter_marker = "|"
    else:
        delimiter_marker = ""

    formatted_values = delimiter.join(format_primitive_value(item, delimiter) for item in items)
    return f"[{length_prefix}{delimiter_marker}]: {formatted_values}"


def format_tabular_array(key: str, items: list, delimiter: str, length_marker: str | bool, indent_level: int, options: EncodeOptions) -> list[str]:
    lines = []

    if not items:
        length_prefix = "#0" if length_marker else "0"
        if delimiter == "\t":
            delimiter_marker = "\t"
        elif delimiter == "|":
            delimiter_marker = "|"
        else:
            delimiter_marker = ""
        lines.append(f"{key}[{length_prefix}{delimiter_marker}]:")
        return lines

    first_item = items[0]
    keys = list(first_item.keys())

    length_prefix = f"#{len(items)}" if length_marker else str(len(items))

    if delimiter == "\t":
        delimiter_marker = "\t"
        header_keys = "\t".join(quote_if_needed_key(k) for k in keys)
    elif delimiter == "|":
        delimiter_marker = "|"
        header_keys = "|".join(quote_if_needed_key(k) for k in keys)
    else:
        delimiter_marker = ""
        header_keys = ",".join(quote_if_needed_key(k) for k in keys)

    lines.append(f"{key}[{length_prefix}{delimiter_marker}]{{{header_keys}}}:")

    indent = " " * (options.indent * (indent_level + 1))
    for item in items:
        row_values = delimiter.join(format_primitive_value(item[k], delimiter) for k in keys)
        lines.append(f"{indent}{row_values}")

    return lines


def format_list_array(items: list, indent_level: int, options: EncodeOptions) -> list[str]:
    lines = []
    indent = " " * (options.indent * indent_level)
    item_indent = " " * (options.indent * (indent_level + 1))

    for item in items:
        if isinstance(item, dict):
            dict_keys = list(item.keys())
            if not dict_keys:
                lines.append(f"{indent}- ")
            else:
                first_key = dict_keys[0]
                first_value = item[first_key]

                quoted_key = quote_if_needed_key(first_key)

                if isinstance(first_value, list):
                    if not first_value:
                        length_prefix = "#0" if options.length_marker else "0"
                        if options.delimiter == "\t":
                            delimiter_marker = "\t"
                        elif options.delimiter == "|":
                            delimiter_marker = "|"
                        else:
                            delimiter_marker = ""
                        lines.append(f"{indent}- {quoted_key}[{length_prefix}{delimiter_marker}]:")
                    elif all(not isinstance(v, (dict, list)) for v in first_value):
                        array_line = format_primitive_array(first_value, options.delimiter, options.length_marker, indent_level + 1)
                        lines.append(f"{indent}- {quoted_key}{array_line}")
                    elif can_use_tabular(first_value):
                        tabular_lines = format_tabular_array(quoted_key, first_value, options.delimiter, options.length_marker, indent_level, options)
                        lines.append(f"{indent}- {tabular_lines[0]}")
                        for i in range(1, len(tabular_lines)):
                            lines.append(tabular_lines[i])
                    else:
                        lines.append(f"{indent}- {quoted_key}:")
                        nested_lines = format_list_array(first_value, indent_level + 2, options)
                        lines.extend(nested_lines)

                    for k in dict_keys[1:]:
                        v = item[k]
                        encoded_lines = encode_value(v, indent_level + 1, options)
                        quoted_k = quote_if_needed_key(k)
                        if isinstance(v, (dict, list)):
                            lines.append(f"{item_indent}{quoted_k}:")
                            for line in encoded_lines:
                                lines.append(f"{item_indent}{line}")
                        else:
                            lines.append(f"{item_indent}{quoted_k}: {encoded_lines[0]}")
                else:
                    formatted_value = format_primitive_value(first_value, options.delimiter)
                    lines.append(f"{indent}- {quoted_key}: {formatted_value}")

                    for k in dict_keys[1:]:
                        v = item[k]
                        encoded_lines = encode_value(v, indent_level + 1, options)
                        quoted_k = quote_if_needed_key(k)
                        if isinstance(v, (dict, list)):
                            lines.append(f"{item_indent}{quoted_k}:")
                            for line in encoded_lines:
                                lines.append(f"{item_indent}{line}")
                        else:
                            lines.append(f"{item_indent}{quoted_k}: {encoded_lines[0]}")
        elif isinstance(item, list):
            if not item:
                length_prefix = "#0" if options.length_marker else "0"
                if options.delimiter == "\t":
                    delimiter_marker = "\t"
                elif options.delimiter == "|":
                    delimiter_marker = "|"
                else:
                    delimiter_marker = ""
                lines.append(f"{indent}- [{length_prefix}{delimiter_marker}]:")
            elif all(not isinstance(v, (dict, list)) for v in item):
                array_line = format_primitive_array(item, options.delimiter, options.length_marker, indent_level + 1)
                lines.append(f"{indent}- {array_line}")
            else:
                length_prefix = f"#{len(item)}" if options.length_marker else str(len(item))
                if options.delimiter == "\t":
                    delimiter_marker = "\t"
                elif options.delimiter == "|":
                    delimiter_marker = "|"
                else:
                    delimiter_marker = ""
                lines.append(f"{indent}- [{length_prefix}{delimiter_marker}]:")
                nested_lines = format_list_array(item, indent_level + 2, options)
                lines.extend(nested_lines)
        else:
            formatted = format_primitive_value(item, options.delimiter)
            lines.append(f"{indent}- {formatted}")

    return lines


def encode_array(items: list, indent_level: int, options: EncodeOptions) -> list[str]:
    if not items:
        length_prefix = "#0" if options.length_marker else "0"
        if options.delimiter == "\t":
            delimiter_marker = "\t"
        elif options.delimiter == "|":
            delimiter_marker = "|"
        else:
            delimiter_marker = ""
        return [f"[{length_prefix}{delimiter_marker}]:"]

    if all(not isinstance(item, (dict, list)) for item in items):
        return [format_primitive_array(items, options.delimiter, options.length_marker, indent_level)]

    if can_use_tabular(items):
        return format_tabular_array("", items, options.delimiter, options.length_marker, indent_level - 1, options)

    length_prefix = f"#{len(items)}" if options.length_marker else str(len(items))
    if options.delimiter == "\t":
        delimiter_marker = "\t"
    elif options.delimiter == "|":
        delimiter_marker = "|"
    else:
        delimiter_marker = ""

    lines = [f"[{length_prefix}{delimiter_marker}]:"]
    lines.extend(format_list_array(items, indent_level + 1, options))
    return lines


def encode_object(obj: dict, indent_level: int, options: EncodeOptions) -> list[str]:
    lines = []
    indent = " " * (options.indent * indent_level)

    for key, value in obj.items():
        quoted_key = quote_if_needed_key(key)

        if isinstance(value, dict):
            if not value:
                lines.append(f"{indent}{quoted_key}:")
            else:
                lines.append(f"{indent}{quoted_key}:")
                nested_lines = encode_object(value, indent_level + 1, options)
                lines.extend(nested_lines)
        elif isinstance(value, list):
            if not value:
                length_prefix = "#0" if options.length_marker else "0"
                if options.delimiter == "\t":
                    delimiter_marker = "\t"
                elif options.delimiter == "|":
                    delimiter_marker = "|"
                else:
                    delimiter_marker = ""
                lines.append(f"{indent}{quoted_key}[{length_prefix}{delimiter_marker}]:")
            elif all(not isinstance(item, (dict, list)) for item in value):
                array_line = format_primitive_array(value, options.delimiter, options.length_marker, indent_level)
                lines.append(f"{indent}{quoted_key}{array_line}")
            elif can_use_tabular(value):
                tabular_lines = format_tabular_array(quoted_key, value, options.delimiter, options.length_marker, indent_level, options)
                for i, line in enumerate(tabular_lines):
                    if i == 0:
                        lines.append(f"{indent}{line}")
                    else:
                        lines.append(f"{indent}{line}")
            else:
                length_prefix = f"#{len(value)}" if options.length_marker else str(len(value))
                if options.delimiter == "\t":
                    delimiter_marker = "\t"
                elif options.delimiter == "|":
                    delimiter_marker = "|"
                else:
                    delimiter_marker = ""
                lines.append(f"{indent}{quoted_key}[{length_prefix}{delimiter_marker}]:")
                list_lines = format_list_array(value, indent_level + 1, options)
                lines.extend(list_lines)
        else:
            formatted = format_primitive_value(value, options.delimiter)
            lines.append(f"{indent}{quoted_key}: {formatted}")

    return lines


def encode_value(value: Any, indent_level: int, options: EncodeOptions) -> list[str]:
    if isinstance(value, dict):
        return encode_object(value, indent_level, options)
    elif isinstance(value, list):
        return encode_array(value, indent_level, options)
    else:
        return [format_primitive_value(value, options.delimiter)]


def encode(value: Any, options: EncodeOptions | None = None) -> str:
    if options is None:
        options = EncodeOptions()

    if isinstance(value, dict):
        if not value:
            return ""
        lines = encode_object(value, 0, options)
    elif isinstance(value, list):
        lines = encode_array(value, 0, options)
    else:
        lines = [format_primitive_value(value, options.delimiter)]

    return "\n".join(lines)
