# toon-py

**Token-Oriented Object Notation (TOON) for Python**

A compact, human-readable format for passing structured data to LLMs with **30-60% fewer tokens** than JSON.

Python port of [@byjohann/toon](https://github.com/johannschopplich/toon).

## Why TOON?

LLM tokens cost money. TOON reduces token usage by:
- Removing redundant punctuation (braces, brackets, most quotes)
- Using indentation for structure
- Tabularizing arrays of objects
- Writing inline primitive arrays without spaces

## Installation

### As a CLI tool

For standalone CLI usage:

```bash
# Using pip
pip install toon-py

# Using uv (recommended)
uv tool install toon-py
```

### As a Python library

To use in your Python project:

```bash
# Using pip
pip install toon-py

# Using uv
uv add toon-py
```

## Quick Start

### Python API

```python
from toon_py import encode

data = {
    "user": {
        "id": 123,
        "name": "Ada",
        "tags": ["reading", "gaming"],
        "active": True
    }
}

print(encode(data))
```

**Output:**

```
user:
  id: 123
  name: Ada
  tags[2]: reading,gaming
  active: true
```

### CLI

```bash
# From file
toon data.json

# From stdin
cat data.json | toon

# From string
toon '{"tags": ["foo", "bar"]}'

# With options
toon data.json --delimiter tab --length-marker -o output.toon
```

## Token Savings

| Example | JSON Tokens | TOON Tokens | Saved | Reduction |
|---------|-------------|-------------|-------|-----------|
| Simple user | 31 | 18 | 13 | **41.9%** |
| User with tags | 48 | 28 | 20 | **41.7%** |
| Product catalog | 117 | 49 | 68 | **58.1%** |
| API response | 123 | 53 | 70 | **56.9%** |
| Analytics data | 209 | 94 | 115 | **55.0%** |
| Large dataset (50 records) | 2159 | 762 | 1397 | **64.7%** |

## Features

### Objects

```python
encode({"id": 1, "name": "Ada"})
```

```
id: 1
name: Ada
```

### Primitive Arrays (Inline)

```python
encode({"tags": ["admin", "ops", "dev"]})
```

```
tags[3]: admin,ops,dev
```

### Arrays of Objects (Tabular)

```python
encode({
    "items": [
        {"sku": "A1", "qty": 2, "price": 9.99},
        {"sku": "B2", "qty": 1, "price": 14.5}
    ]
})
```

```
items[2]{sku,qty,price}:
  A1,2,9.99
  B2,1,14.5
```

### Encoding Options

```python
from toon_py import encode, EncodeOptions

data = {"items": [{"id": 1, "name": "Widget"}]}

# Tab delimiter
options = EncodeOptions(delimiter="\t")
print(encode(data, options))

# Pipe delimiter
options = EncodeOptions(delimiter="|")
print(encode(data, options))

# Length marker
options = EncodeOptions(length_marker="#")
print(encode(data, options))
# Output: items[#1]{id,name}: ...

# Custom indent
options = EncodeOptions(indent=4)
print(encode(data, options))
```

## CLI Options

```
toon [INPUT] [OPTIONS]

Arguments:
  INPUT                 JSON file, JSON string, or stdin

Options:
  -i, --indent INT      Spaces per indent level (default: 2)
  -d, --delimiter TEXT  Delimiter: comma, tab, or pipe (default: comma)
  -l, --length-marker   Add '#' prefix to array lengths
  -o, --output PATH     Output file (default: stdout)
  --help                Show help message
```

## Format Rules

### Quoting

Keys and values are quoted only when necessary:

```python
# Unquoted
{"name": "hello world"}  # -> name: hello world

# Quoted (contains comma)
{"note": "hello, world"}  # -> note: "hello, world"

# Quoted (looks like number)
{"code": "123"}  # -> code: "123"

# Quoted (key with space)
{"full name": "Ada"}  # -> "full name": Ada
```

### Tabular Format

Arrays of objects use tabular format when:
- All elements are objects
- All objects have identical keys
- All values are primitives (no nested arrays/objects)

```python
encode({
    "users": [
        {"id": 1, "name": "Alice", "active": True},
        {"id": 2, "name": "Bob", "active": False}
    ]
})
```

```
users[2]{id,name,active}:
  1,Alice,true
  2,Bob,false
```

### Empty Containers

```python
encode({})            # -> (empty output)
encode({"items": []}) # -> items[0]:
encode({"config": {}})# -> config:
```

## Type Conversions

| Python Type | TOON Output |
|-------------|-------------|
| `None` | `null` |
| `True`/`False` | `true`/`false` |
| `123` | `123` |
| `-0.0` | `0` |
| `float('nan')` | `null` |
| `float('inf')` | `null` |
| `datetime(...)` | `"2025-01-01T00:00:00Z"` |

## Use in LLM Prompts

Wrap TOON data in code blocks:

````markdown
Here's the data in TOON format:

```
user:
  id: 123
  tags[2]: reading,gaming
  active: true
```

Please analyze this data...
````

## Development

```bash
# Clone and setup
git clone https://github.com/shammianand/toon-py.git
cd toon-py
uv sync --all-extras

# Run tests
uv run pytest

# Format code
uv run black src/
uv run ruff check src/
```

## License

MIT License - see [LICENSE](LICENSE)

## Credits

Python port of [@byjohann/toon](https://github.com/johannschopplich/toon) by [Johann Schopplich](https://github.com/johannschopplich)
