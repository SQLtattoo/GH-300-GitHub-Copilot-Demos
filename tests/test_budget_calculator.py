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


def test_empty_transactions_have_zero_totals(calculator):
    """Return zero totals when there are no transactions."""
    assert calculator.total_income([]) == 0.0
    assert calculator.total_expenses([]) == 0.0
    assert calculator.net_cash_flow([]) == 0.0


def test_average_expense_is_zero_for_empty_transactions(calculator):
    """Return a neutral average when there are no expenses."""
    assert calculator.average_expense([]) == 0.0


def test_savings_rate_is_zero_when_income_is_zero(calculator):
    """Avoid division by zero when no income was earned."""
    assert calculator.savings_rate(0.0, 125.0) == 0.0


def test_category_percentage_is_zero_when_expenses_are_zero(calculator):
    """Avoid division by zero when there are no expenses."""
    assert calculator.category_percentage(0.0, 0.0) == 0.0


def test_history_records_calculations_in_order(calculator):
    """Record each calculation in the order it was performed."""
    calculator.total_income([])
    calculator.remaining_budget(500.0, [])

    assert calculator.get_history() == [
        "total_income = 0",
        "total_expenses = 0",
        "remaining_budget(500.0) = 500.0",
    ]


def test_get_history_returns_a_copy(calculator):
    """Prevent callers from mutating the calculator's history."""
    calculator.total_income([])

    history = calculator.get_history()
    history.append("changed externally")

    assert calculator.get_history() == ["total_income = 0"]


def test_average_and_percentage_calculations(calculator, sample_transactions):
    """Calculate nonzero averages, category percentages, and savings rates."""
    assert calculator.average_expense(sample_transactions) == 80.0
    assert calculator.category_percentage(40.0, 160.0) == 25.0
    assert calculator.savings_rate(5000.0, 1000.0) == 80.0


def test_forecast_month_end_spend(calculator, sample_transactions):
    """Project month-to-date expenses across the full month."""
    assert calculator.forecast_month_end_spend(sample_transactions, 16, 30) == 300.0


@pytest.mark.parametrize(
    ("days_elapsed", "days_in_month", "message"),
    [
        (0, 30, "days_elapsed must be at least 1"),
        (31, 30, "days_in_month must be at least days_elapsed"),
    ],
)
def test_forecast_month_end_spend_rejects_invalid_days(
    calculator,
    days_elapsed,
    days_in_month,
    message,
):
    """Reject day ranges that would be undefined or impossible."""
    with pytest.raises(ValueError, match=message):
        calculator.forecast_month_end_spend([], days_elapsed, days_in_month)


def test_is_over_budget_uses_strict_boundary(calculator, sample_transactions):
    """Treat expenses equal to the budget as within budget."""
    assert calculator.is_over_budget(159.99, sample_transactions) is True
    assert calculator.is_over_budget(160.0, sample_transactions) is False