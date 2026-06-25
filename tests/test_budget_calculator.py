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


# --- Edge case: empty transactions -------------------------------------------------


def test_total_income_empty(calculator):
    """Income of an empty transaction list is zero."""
    assert calculator.total_income([]) == 0.0


def test_total_expenses_empty(calculator):
    """Expenses of an empty transaction list is zero."""
    assert calculator.total_expenses([]) == 0.0


def test_net_cash_flow_empty(calculator):
    """Net cash flow of an empty transaction list is zero."""
    assert calculator.net_cash_flow([]) == 0.0


def test_remaining_budget_empty(calculator):
    """With no expenses the full budget remains."""
    assert calculator.remaining_budget(1000.0, []) == 1000.0


def test_average_expense_empty_raises(calculator):
    """Averaging with no expenses divides by zero (documents current behavior)."""
    with pytest.raises(ZeroDivisionError):
        calculator.average_expense([])


# --- Edge case: zero income --------------------------------------------------------


def test_savings_rate_zero_income(calculator):
    """Zero income returns a 0.0 savings rate instead of raising."""
    assert calculator.savings_rate(0, 500.0) == 0.0


def test_total_income_zero_income_transactions(calculator):
    """Only-expense transactions produce zero income."""
    transactions = [
        {"category": "Groceries", "amount": 120.0, "type": "expense"},
        {"category": "Transport", "amount": 40.0, "type": "expense"},
    ]
    assert calculator.total_income(transactions) == 0.0


# --- Edge case: zero expenses ------------------------------------------------------


def test_total_expenses_zero_when_only_income(calculator):
    """Only-income transactions produce zero expenses."""
    transactions = [
        {"category": "Income", "amount": 5000.0, "type": "income"},
    ]
    assert calculator.total_expenses(transactions) == 0.0


def test_savings_rate_zero_expenses_is_full(calculator):
    """No expenses means the entire income is saved (100%)."""
    assert calculator.savings_rate(5000.0, 0.0) == 100.0


def test_net_cash_flow_zero_expenses(calculator):
    """Net cash flow equals income when there are no expenses."""
    transactions = [
        {"category": "Income", "amount": 5000.0, "type": "income"},
    ]
    assert calculator.net_cash_flow(transactions) == 5000.0


# --- History behavior --------------------------------------------------------------


def test_history_starts_empty(calculator):
    """A fresh calculator has no history."""
    assert calculator.get_history() == []


def test_history_records_each_calculation(calculator, sample_transactions):
    """Each calculation appends an entry to the history."""
    calculator.total_income(sample_transactions)
    calculator.total_expenses(sample_transactions)
    history = calculator.get_history()
    assert len(history) == 2
    assert history[0] == "total_income = 5000.0"
    assert history[1] == "total_expenses = 160.0"


def test_net_cash_flow_records_nested_history(calculator, sample_transactions):
    """net_cash_flow records its own entry plus the nested totals it calls."""
    calculator.net_cash_flow(sample_transactions)
    history = calculator.get_history()
    assert history == [
        "total_income = 5000.0",
        "total_expenses = 160.0",
        "net_cash_flow = 4840.0",
    ]


def test_get_history_returns_copy(calculator, sample_transactions):
    """Mutating the returned history must not affect the calculator's state."""
    calculator.total_income(sample_transactions)
    snapshot = calculator.get_history()
    snapshot.append("tampered")
    assert calculator.get_history() == ["total_income = 5000.0"]


# --- Remaining methods -------------------------------------------------------------


def test_average_expense_happy_path(calculator, sample_transactions):
    """Average expense divides total expenses by the expense count."""
    assert calculator.average_expense(sample_transactions) == 80.0


def test_category_percentage(calculator):
    """A category's share is expressed as a percentage of total expenses."""
    assert calculator.category_percentage(40.0, 160.0) == 25.0


def test_savings_rate_negative_when_expenses_exceed_income(calculator):
    """Spending more than income yields a negative savings rate."""
    assert calculator.savings_rate(1000.0, 1500.0) == -50.0


def test_forecast_month_end_spend_projects_linearly(calculator, sample_transactions):
    """Spending is projected linearly from days elapsed to month length."""
    # 160 expenses over 10 days -> 16/day -> 480 over 30 days.
    assert calculator.forecast_month_end_spend(sample_transactions, 10, 30) == 480.0


def test_forecast_month_end_spend_zero_days(calculator, sample_transactions):
    """With no days elapsed the forecast is zero (avoids divide-by-zero)."""
    assert calculator.forecast_month_end_spend(sample_transactions, 0, 30) == 0.0


def test_is_over_budget_true_and_false(calculator, sample_transactions):
    """is_over_budget compares total expenses against the monthly budget."""
    assert calculator.is_over_budget(100.0, sample_transactions) is True
    assert calculator.is_over_budget(1000.0, sample_transactions) is False