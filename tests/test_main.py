"""Tests for the main application module."""

import main
from main import build_report, format_currency, show_transactions


def test_format_currency():
    assert format_currency(1234.5) == "$1,234.50"
    assert format_currency("0") == "$0.00"


def test_build_report(sample_transactions):
    report = build_report(1000.0, sample_transactions)

    assert report["monthly_budget"] == 1000.0
    assert report["income"] == 3000.0
    assert report["expenses"] == 400.0
    assert report["remaining_budget"] == 600.0
    assert report["net_cash_flow"] == 2600.0
    assert report["largest_expense"]["amount"] == 200.0
    assert report["category_totals"] == {"Groceries": 200.0, "Dining": 50.0, "Utilities": 150.0}
    assert report["top_merchants"] == [("Grocer", 200.0), ("Utility Co", 150.0), ("Cafe", 50.0)]


def test_show_transactions_runs(sample_transactions):
    # Should log without raising.
    show_transactions(sample_transactions)


def test_main_runs():
    # Reads data/sample_transactions.csv and logs a full report.
    main.main()
