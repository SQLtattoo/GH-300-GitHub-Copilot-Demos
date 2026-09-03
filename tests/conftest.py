import pytest


@pytest.fixture
def transactions() -> list[dict[str, object]]:
    return [
        {
            "date": "2026-06-01",
            "merchant": "Payroll",
            "category": "Income",
            "amount": 5000.0,
            "type": "income",
        },
        {
            "date": "2026-06-02",
            "merchant": "Market",
            "category": " groceries ",
            "amount": 125.5,
            "type": "expense",
        },
        {
            "date": "2026-06-03",
            "merchant": "Cafe",
            "category": "DINING",
            "amount": 24.5,
            "type": "expense",
        },
        {
            "date": "2026-07-01",
            "merchant": "Market",
            "category": "Groceries",
            "amount": 50.0,
            "type": "expense",
        },
    ]