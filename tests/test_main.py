"""Tests for Budget Buddy report construction and application output."""

from unittest.mock import Mock

import pytest

import main as app


class TestFormattingAndReports:
    @pytest.mark.parametrize(
        "value, expected",
        [(0, "$0.00"), (1234.5, "$1,234.50"), (-12.5, "$-12.50"), ("2.5", "$2.50")],
    )
    def test_format_currency(self, value, expected):
        assert app.format_currency(value) == expected

    def test_format_currency_rejects_non_numeric_value(self):
        with pytest.raises(ValueError):
            app.format_currency("invalid")

    def test_build_report_calculates_all_metrics(self, sample_transactions):
        report = app.build_report(1000.0, sample_transactions)

        assert report == {
            "monthly_budget": 1000.0,
            "income": 5000.0,
            "expenses": 160.0,
            "remaining_budget": 840.0,
            "net_cash_flow": 4840.0,
            "savings_rate": 96.8,
            "largest_expense": sample_transactions[1],
            "category_totals": {"Groceries": 120.0, "Transport": 40.0},
        }

    def test_build_report_handles_empty_month(self):
        report = app.build_report(500.0, [])

        assert report["income"] == 0.0
        assert report["expenses"] == 0.0
        assert report["remaining_budget"] == 500.0
        assert report["net_cash_flow"] == 0.0
        assert report["savings_rate"] == 0.0
        assert report["largest_expense"] is None
        assert report["category_totals"] == {}


class TestApplicationOutput:
    def test_show_transactions_logs_header_and_each_visible_row(self, sample_transactions, monkeypatch):
        fake_logger = Mock()
        monkeypatch.setattr(app, "logger", fake_logger)

        app.show_transactions(sample_transactions)

        messages = [call.args[0] for call in fake_logger.info.call_args_list]
        assert messages[:3] == [
            "Recent transactions",
            "Date       | Merchant             | Category      | Amount     | Type",
            "-" * 72,
        ]
        assert len(messages) == 6
        assert any("Payroll" in message and "$5,000.00" in message for message in messages)

    def test_main_runs_sample_report_to_completion(self, monkeypatch):
        fake_logger = Mock()
        monkeypatch.setattr(app, "logger", fake_logger)

        app.main()

        messages = [call.args[0] for call in fake_logger.info.call_args_list]
        assert messages[0] == "Budget Buddy - GitHub Copilot Demo App"
        assert "Monthly budget: $3,200.00" in messages
        assert "Expenses: $2,484.76" in messages
        assert messages[-1] == "Demo-start app completed. Now use Copilot to harden it."