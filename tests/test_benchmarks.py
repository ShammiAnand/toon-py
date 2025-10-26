import pytest
from toon_py import encode


def test_small_product_catalog():
    data = {
        "items": [
            {"sku": "A1", "name": "Widget", "qty": 2, "price": 9.99},
            {"sku": "B2", "name": "Gadget", "qty": 1, "price": 14.5},
            {"sku": "C3", "name": "Doohickey", "qty": 5, "price": 7.25},
        ]
    }
    result = encode(data)
    expected = "items[3]{sku,name,qty,price}:\n  A1,Widget,2,9.99\n  B2,Gadget,1,14.5\n  C3,Doohickey,5,7.25"
    assert result == expected


def test_api_response_with_users():
    data = {
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com", "active": True},
            {"id": 2, "name": "Bob", "email": "bob@example.com", "active": True},
            {
                "id": 3,
                "name": "Charlie",
                "email": "charlie@example.com",
                "active": False,
            },
        ],
        "total": 3,
        "page": 1,
    }
    result = encode(data)
    expected = "users[3]{id,name,email,active}:\n  1,Alice,alice@example.com,true\n  2,Bob,bob@example.com,true\n  3,Charlie,charlie@example.com,false\ntotal: 3\npage: 1"
    assert result == expected


def test_analytics_data():
    data = {
        "metrics": [
            {"date": "2025-01-01", "views": 1234, "clicks": 89, "conversions": 12},
            {"date": "2025-01-02", "views": 2345, "clicks": 156, "conversions": 23},
            {"date": "2025-01-03", "views": 1890, "clicks": 123, "conversions": 18},
            {"date": "2025-01-04", "views": 3456, "clicks": 234, "conversions": 34},
            {"date": "2025-01-05", "views": 2789, "clicks": 178, "conversions": 27},
        ]
    }
    result = encode(data)
    expected = """metrics[5]{date,views,clicks,conversions}:
  2025-01-01,1234,89,12
  2025-01-02,2345,156,23
  2025-01-03,1890,123,18
  2025-01-04,3456,234,34
  2025-01-05,2789,178,27"""
    assert result == expected


def test_simple_user_object():
    data = {"id": 1, "name": "Alice", "email": "alice@example.com", "active": True}
    result = encode(data)
    expected = "id: 1\nname: Alice\nemail: alice@example.com\nactive: true"
    assert result == expected


def test_user_with_tags():
    data = {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com",
        "tags": ["developer", "python", "ai"],
        "active": True,
    }
    result = encode(data)
    expected = "id: 1\nname: Alice\nemail: alice@example.com\ntags[3]: developer,python,ai\nactive: true"
    assert result == expected


def test_nested_configuration():
    data = {
        "app": {
            "name": "MyApp",
            "version": "1.0.0",
            "settings": {"debug": True, "timeout": 30, "retries": 3},
        }
    }
    result = encode(data)
    expected = "app:\n  name: MyApp\n  version: 1.0.0\n  settings:\n    debug: true\n    timeout: 30\n    retries: 3"
    assert result == expected


def test_ecommerce_order():
    data = {
        "order_id": "ORD-12345",
        "customer": {"id": 789, "name": "Jane Doe", "email": "jane@example.com"},
        "items": [
            {"sku": "WIDGET-A", "name": "Premium Widget", "qty": 2, "price": 29.99},
            {"sku": "GADGET-B", "name": "Deluxe Gadget", "qty": 1, "price": 49.99},
        ],
        "total": 109.97,
        "status": "shipped",
    }
    result = encode(data)
    expected = """order_id: ORD-12345
customer:
  id: 789
  name: Jane Doe
  email: jane@example.com
items[2]{sku,name,qty,price}:
  WIDGET-A,Premium Widget,2,29.99
  GADGET-B,Deluxe Gadget,1,49.99
total: 109.97
status: shipped"""
    assert result == expected
