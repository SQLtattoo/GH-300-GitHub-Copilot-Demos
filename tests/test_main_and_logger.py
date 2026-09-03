import logging

import pytest

import main
from logger import setup_logger


def test_format_currency_handles_numeric_values_and_grouping():
    assert main.format_currency("1234.5") == "$1,234.50"
    assert main.format_currency(-2) == "$-2.00"


def test_build_report_integrates_calculator_and_processor(transactions):
    report = main.build_report(1000.0, transactions)

    assert report == {
        "monthly_budget": 1000.0,
        "income": 5000.0,
        "expenses": 200.0,
        "remaining_budget": 800.0,
        "net_cash_flow": 4800.0,
        "savings_rate": 96.0,
        "largest_expense": transactions[1],
        "category_totals": {"Groceries": 175.5, "Dining": 24.5},
        "top_merchants": [
            {"merchant": "Market", "total": 175.5},
            {"merchant": "Cafe", "total": 24.5},
        ],
    }


def test_build_report_requires_nonzero_income():
    with pytest.raises(ZeroDivisionError):
        main.build_report(100.0, [{"type": "expense", "amount": 10.0}])


def test_build_report_reuses_precomputed_totals(monkeypatch, transactions):
    def fail_on_rescan(*args, **kwargs):
        pytest.fail("build_report should derive metrics from precomputed totals")

    monkeypatch.setattr(main.BudgetCalculator, "remaining_budget", fail_on_rescan)
    monkeypatch.setattr(main.BudgetCalculator, "net_cash_flow", fail_on_rescan)

    report = main.build_report(1000.0, transactions)

    assert report["remaining_budget"] == 800.0
    assert report["net_cash_flow"] == 4800.0


def test_show_transactions_logs_header_and_first_page(monkeypatch):
    messages = []
    monkeypatch.setattr(main.logger, "info", messages.append)
    transactions = [
        {
            "date": f"2026-06-{day:02d}",
            "merchant": "Cafe",
            "category": "Dining",
            "amount": day,
            "type": "expense",
        }
        for day in range(1, 8)
    ]

    main.show_transactions(transactions)

    assert messages[0] == "Recent transactions"
    assert len(messages) == 9
    assert "2026-06-01" in messages[3]
    assert "$1.00" in messages[3]
    assert all("2026-06-07" not in message for message in messages)


def test_show_top_merchants_logs_ranked_table_and_empty_state(monkeypatch):
    messages = []
    monkeypatch.setattr(main.logger, "info", messages.append)

    main.show_top_merchants(
        [
            {"merchant": "Market", "total": 175.5},
            {"merchant": "Cafe", "total": 24.5},
        ]
    )

    assert messages[0] == "Top merchants"
    assert "Market" in messages[3]
    assert "$175.50" in messages[3]
    assert "Cafe" in messages[4]

    messages.clear()
    main.show_top_merchants([])
    assert messages == ["Top merchants", "No expense transactions found."]


def test_main_loads_sample_data_and_logs_report(monkeypatch):
    messages = []
    monkeypatch.setattr(main.logger, "info", messages.append)

    main.main()

    assert "Budget Buddy - GitHub Copilot Demo App" in messages
    assert "Monthly budget: $3,200.00" in messages
    assert "Income: $5,200.00" in messages
    assert "Top merchants" in messages
    assert messages[-1] == "Demo-start app completed. Now use Copilot to harden it."


def test_setup_logger_replaces_handlers_and_writes_console_and_file(tmp_path, capsys):
    log_path = tmp_path / "logs" / "app.log"
    logger = setup_logger("test_budget_buddy_logger", logging.DEBUG, str(log_path))

    logger.info("first message")
    assert "first message" in capsys.readouterr().out
    assert "INFO - first message" in log_path.read_text(encoding="utf-8")
    assert len(logger.handlers) == 2

    original_handlers = list(logger.handlers)
    same_logger = setup_logger("test_budget_buddy_logger", logging.WARNING)
    assert same_logger is logger
    assert len(same_logger.handlers) == 1
    assert same_logger.level == logging.WARNING

    for handler in original_handlers + list(same_logger.handlers):
        handler.close()