"""Starter tests for BudgetCalculator."""

import pytest


def test_total_income(calculator, sample_transactions):
    """Calculate income for a happy-path transaction set."""
    assert calculator.total_income(sample_transactions) == 5000.0


def test_total_expenses(calculator, sample_transactions):
    """Calculate expenses for a happy-path transaction set."""
    assert calculator.total_expenses(sample_transactions) == 160.0


def test_remaining_budget(calculator, sample_transactions):
    """Calculate remaining budget for the sample month."""
    assert calculator.remaining_budget(1000.0, sample_transactions) == 840.0


class TestEmptyTransactions:
    """Calculations should return neutral values for an empty month."""

    def test_totals_and_cash_flow_are_zero(self, calculator):
        assert calculator.total_income([]) == 0.0
        assert calculator.total_expenses([]) == 0.0
        assert calculator.net_cash_flow([]) == 0.0

    def test_full_budget_remains(self, calculator):
        assert calculator.remaining_budget(1000.0, []) == 1000.0

    def test_average_expense_is_zero(self, calculator):
        assert calculator.average_expense([]) == 0.0


class TestZeroValues:
    """Percentage calculations should handle zero denominators safely."""

    def test_zero_income_has_zero_savings_rate(self, calculator):
        assert calculator.savings_rate(0.0, 250.0) == 0.0

    def test_zero_expenses_have_zero_category_percentage(self, calculator):
        assert calculator.category_percentage(0.0, 0.0) == 0.0

    def test_zero_expenses_preserve_all_income_as_savings(self, calculator):
        assert calculator.savings_rate(1000.0, 0.0) == 100.0


class TestErrorPaths:
    """Invalid transaction amounts should fail clearly."""

    def test_non_numeric_income_amount_raises_value_error(self, calculator):
        transactions = [{"amount": "not-a-number", "type": "income"}]

        with pytest.raises(ValueError):
            calculator.total_income(transactions)

        assert calculator.get_history() == []


class TestHistory:
    """Calculation history should be ordered and protected from mutation."""

    def test_composed_calculation_records_each_operation(self, calculator, sample_transactions):
        assert calculator.net_cash_flow(sample_transactions) == 4840.0
        assert calculator.get_history() == [
            "total_income = 5000.0",
            "total_expenses = 160.0",
            "net_cash_flow = 4840.0",
        ]

    def test_get_history_returns_a_copy(self, calculator):
        calculator.total_income([])

        returned_history = calculator.get_history()
        returned_history.append("external change")

        assert calculator.get_history() == ["total_income = 0"]


class TestForecastAndBudgetStatus:
    """Forecasting and budget checks should cover boundaries and invalid days."""

    def test_forecasts_month_end_spending(self, calculator, sample_transactions):
        assert calculator.forecast_month_end_spend(sample_transactions, 10, 30) == 480.0
        assert calculator.get_history()[-2:] == [
            "total_expenses = 160.0",
            "forecast_month_end_spend = 480.0",
        ]

    @pytest.mark.parametrize("days_elapsed, days_in_month", [(0, 30), (-1, 30), (10, 0), (31, 30)])
    def test_forecast_rejects_invalid_day_ranges(self, calculator, days_elapsed, days_in_month):
        with pytest.raises(ValueError, match="valid positive day range"):
            calculator.forecast_month_end_spend([], days_elapsed, days_in_month)

        assert calculator.get_history() == []

    def test_empty_month_forecast_is_zero(self, calculator):
        assert calculator.forecast_month_end_spend([], 15, 30) == 0.0

    @pytest.mark.parametrize(
        "budget, expected",
        [(159.99, True), (160.0, False), (200.0, False)],
    )
    def test_over_budget_uses_strict_boundary(self, calculator, sample_transactions, budget, expected):
        assert calculator.is_over_budget(budget, sample_transactions) is expected
        assert calculator.get_history()[-1] == f"is_over_budget({budget}) = {expected}"