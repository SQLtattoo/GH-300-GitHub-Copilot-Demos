"""Tests for the BudgetCalculator module."""

import pytest

from calculator import BudgetCalculator, Calculator


def test_total_income(sample_transactions):
    assert BudgetCalculator().total_income(sample_transactions) == 3000.0


def test_total_income_empty():
    assert BudgetCalculator().total_income([]) == 0.0


def test_total_expenses(sample_transactions):
    assert BudgetCalculator().total_expenses(sample_transactions) == 400.0


def test_net_cash_flow(sample_transactions):
    assert BudgetCalculator().net_cash_flow(sample_transactions) == 2600.0


def test_remaining_budget(sample_transactions):
    assert BudgetCalculator().remaining_budget(1000.0, sample_transactions) == 600.0


def test_average_expense(sample_transactions):
    assert BudgetCalculator().average_expense(sample_transactions) == pytest.approx(133.3333, rel=1e-3)


def test_category_percentage():
    assert BudgetCalculator().category_percentage(200.0, 400.0) == 50.0


def test_savings_rate():
    assert BudgetCalculator().savings_rate(3000.0, 400.0) == pytest.approx(86.6667, rel=1e-3)


def test_forecast_month_end_spend_placeholder(sample_transactions):
    # TODO placeholder currently returns 0.0.
    assert BudgetCalculator().forecast_month_end_spend(sample_transactions, 10, 30) == 0.0


def test_is_over_budget_placeholder(sample_transactions):
    # TODO placeholder currently returns False.
    assert BudgetCalculator().is_over_budget(100.0, sample_transactions) is False


def test_history_records_calculations(sample_transactions):
    calculator = BudgetCalculator()
    calculator.total_income(sample_transactions)
    calculator.total_expenses(sample_transactions)

    history = calculator.get_history()
    assert len(history) == 2
    assert history[0].startswith("total_income")


def test_history_is_a_copy(sample_transactions):
    calculator = BudgetCalculator()
    calculator.total_income(sample_transactions)

    history = calculator.get_history()
    history.append("tampered")
    assert calculator.get_history() == ["total_income = 3000.0"]


def test_backward_compatible_alias():
    assert Calculator is BudgetCalculator
