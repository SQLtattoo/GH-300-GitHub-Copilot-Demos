import main


def _sample_transactions() -> list[dict[str, object]]:
    return [
        {"date": "2026-06-01", "merchant": "Employer", "category": "Salary", "amount": 1000.0, "type": "income"},
        {"date": "2026-06-02", "merchant": "Store", "category": "Groceries", "amount": 150.0, "type": "expense"},
    ]


def test_format_currency() -> None:
    assert main.format_currency(1234.5) == "$1,234.50"


def test_build_report_contains_expected_metrics() -> None:
    report = main.build_report(500.0, _sample_transactions())

    assert report["monthly_budget"] == 500.0
    assert report["income"] == 1000.0
    assert report["expenses"] == 150.0
    assert report["remaining_budget"] == 350.0
    assert report["net_cash_flow"] == 850.0
    assert report["savings_rate"] == 85.0
    assert report["largest_expense"]["merchant"] == "Store"
    assert report["category_totals"] == {"Groceries": 150.0}


def test_show_transactions_logs_rows(monkeypatch) -> None:
    captured: list[str] = []

    def _capture(message: str) -> None:
        captured.append(message)

    monkeypatch.setattr(main.logger, "info", _capture)
    main.show_transactions(_sample_transactions())

    assert any("Recent transactions" in line for line in captured)
    assert any("Store" in line for line in captured)
