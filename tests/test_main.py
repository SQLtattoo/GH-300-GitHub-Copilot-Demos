"""Tests for Budget Buddy report construction and application orchestration."""

import main as budget_app


def test_format_currency():
    """Format numeric values with currency punctuation and two decimals."""
    assert budget_app.format_currency("1234.5") == "$1,234.50"


def test_build_report_contains_complete_budget_summary(sample_transactions):
    """Build all report metrics from a representative transaction set."""
    report = budget_app.build_report(1000.0, sample_transactions)

    assert report == {
        "monthly_budget": 1000.0,
        "income": 5000.0,
        "expenses": 160.0,
        "remaining_budget": 840.0,
        "net_cash_flow": 4840.0,
        "savings_rate": 96.8,
        "largest_expense": sample_transactions[1],
        "category_totals": {"Groceries": 120.0, "Transport": 40.0},
        "top_merchants": [("Grocery", 120.0), ("Transit", 40.0)],
    }


def test_build_report_handles_empty_transactions():
    """Build a neutral report for a month without transactions."""
    report = budget_app.build_report(500.0, [])

    assert report["income"] == 0.0
    assert report["expenses"] == 0.0
    assert report["savings_rate"] == 0.0
    assert report["largest_expense"] is None
    assert report["category_totals"] == {}
    assert report["top_merchants"] == []


def test_show_transactions_logs_headers_and_formatted_rows(monkeypatch, sample_transactions):
    """Log the table heading and each formatted transaction row."""
    messages = []
    monkeypatch.setattr(budget_app.logger, "info", messages.append)

    budget_app.show_transactions(sample_transactions[:1])

    assert messages[0] == "Recent transactions"
    assert "Merchant" in messages[1]
    assert "$5,000.00" in messages[3]
    assert "Payroll" in messages[3]


def test_main_runs_complete_report_flow(monkeypatch, sample_transactions):
    """Load and export transactions, then log every report section."""
    messages = []
    exported = []

    class StubFileHandler:
        def __init__(self, base_path):
            assert base_path == "data"

        def read_transactions_csv(self, filename):
            assert filename == "sample_transactions.csv"
            return sample_transactions

        def write_transactions_csv(self, filename, transactions):
            exported.append((filename, transactions))

    monkeypatch.setattr(budget_app, "BudgetFileHandler", StubFileHandler)
    monkeypatch.setattr(budget_app.logger, "info", messages.append)

    budget_app.main()

    assert exported == [("exported_transactions.csv", sample_transactions)]
    assert messages[0] == "Budget Buddy - GitHub Copilot Demo App"
    assert "Monthly budget: $3,200.00" in messages
    assert "Savings rate: 96.8%" in messages
    assert "Top merchants:" in messages
    assert "  1. Grocery: $120.00" in messages
    assert "  2. Transit: $40.00" in messages
    assert "Transactions exported to data/exported_transactions.csv" in messages
    assert messages[-1] == "Budget Buddy report completed."