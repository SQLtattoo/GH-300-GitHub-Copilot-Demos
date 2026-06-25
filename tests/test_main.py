"""Tests for the main application entry point and report building."""

import pytest

import main


@pytest.fixture
def transactions():
    """A transaction set with income and multiple expense categories."""
    return [
        {"date": "2026-06-01", "merchant": "Payroll", "category": "Income", "amount": 5000.0, "type": "income"},
        {"date": "2026-06-02", "merchant": "Grocery", "category": "Groceries", "amount": 120.0, "type": "expense"},
        {"date": "2026-06-03", "merchant": "Transit", "category": "Transport", "amount": 40.0, "type": "expense"},
        {"date": "2026-06-04", "merchant": "Market", "category": "Groceries", "amount": 60.0, "type": "expense"},
    ]


def test_format_currency():
    """Numeric values are formatted as currency with thousands separators."""
    assert main.format_currency(1234.5) == "$1,234.50"
    assert main.format_currency("0") == "$0.00"


def test_build_report_structure_and_values(transactions):
    """build_report aggregates income, expenses, and derived metrics."""
    report = main.build_report(3200.0, transactions)

    assert report["monthly_budget"] == 3200.0
    assert report["income"] == 5000.0
    assert report["expenses"] == 220.0
    assert report["remaining_budget"] == 2980.0
    assert report["net_cash_flow"] == 4780.0
    assert report["savings_rate"] == pytest.approx(95.6)
    assert report["largest_expense"]["merchant"] == "Grocery"
    assert report["category_totals"]["Groceries"] == 180.0
    assert report["category_totals"]["Transport"] == 40.0
    assert report["top_merchants"] == [
        ("Grocery", 120.0),
        ("Market", 60.0),
        ("Transit", 40.0),
    ]


def test_show_transactions_logs_rows(transactions, caplog):
    """show_transactions emits header and per-row log lines."""
    with caplog.at_level("INFO"):
        main.show_transactions(transactions)

    assert "Recent transactions" in caplog.text
    assert "Grocery" in caplog.text


def test_main_runs_end_to_end(monkeypatch, transactions, caplog):
    """main wires the handler, report, and logging together."""
    monkeypatch.setattr(
        main.BudgetFileHandler,
        "read_transactions_csv",
        lambda self, filename: transactions,
    )

    with caplog.at_level("INFO"):
        main.main()

    assert "Budget Buddy - GitHub Copilot Demo App" in caplog.text
    assert "Top merchants:" in caplog.text
    assert "Demo-start app completed" in caplog.text
