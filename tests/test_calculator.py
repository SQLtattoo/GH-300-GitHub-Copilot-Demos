import pytest

from calculator import BudgetCalculator


def _sample_transactions() -> list[dict[str, object]]:
    return [
        {"date": "2026-06-01", "merchant": "Employer", "category": "Salary", "amount": 5000.0, "type": "income"},
        {"date": "2026-06-02", "merchant": "Store", "category": "Groceries", "amount": 200.0, "type": "expense"},
        {"date": "2026-06-03", "merchant": "Cafe", "category": "Dining", "amount": 50.0, "type": "expense"},
    ]


def test_calculator_core_metrics_and_history() -> None:
    calc = BudgetCalculator()
    transactions = _sample_transactions()

    assert calc.total_income(transactions) == 5000.0
    assert calc.total_expenses(transactions) == 250.0
    assert calc.net_cash_flow(transactions) == 4750.0
    assert calc.remaining_budget(1000.0, transactions) == 750.0
    assert calc.average_expense(transactions) == 125.0
    assert calc.category_percentage(50.0, 250.0) == 20.0
    assert calc.savings_rate(5000.0, 250.0) == 95.0
    assert calc.forecast_month_end_spend(transactions, days_elapsed=5, days_in_month=30) == 1500.0
    assert calc.is_over_budget(100.0, transactions) is True

    history = calc.get_history()
    assert history
    assert any("total_income" in entry for entry in history)
    assert any("forecast_month_end_spend" in entry for entry in history)


def test_calculator_zero_edge_cases() -> None:
    calc = BudgetCalculator()
    transactions: list[dict[str, object]] = []

    assert calc.savings_rate(0.0, 120.0) == 0.0
    assert calc.forecast_month_end_spend(transactions, days_elapsed=0, days_in_month=30) == 0.0


def test_calculator_alias_points_to_budget_calculator() -> None:
    from calculator import Calculator

    calc = Calculator()
    assert isinstance(calc, BudgetCalculator)


def test_total_income_and_expenses_ignore_unrelated_types() -> None:
    calc = BudgetCalculator()
    transactions: list[dict[str, object]] = [
        {"amount": "1200.50", "type": "income"},
        {"amount": 300.0, "type": "expense"},
        {"amount": 999.0, "type": "transfer"},
    ]

    assert calc.total_income(transactions) == 1200.5
    assert calc.total_expenses(transactions) == 300.0


def test_average_expense_raises_for_no_expense_transactions() -> None:
    calc = BudgetCalculator()
    transactions: list[dict[str, object]] = [{"amount": 1500.0, "type": "income"}]

    with pytest.raises(ZeroDivisionError):
        calc.average_expense(transactions)


def test_category_percentage_raises_when_total_expenses_is_zero() -> None:
    calc = BudgetCalculator()

    with pytest.raises(ZeroDivisionError):
        calc.category_percentage(10.0, 0.0)


def test_is_over_budget_false_when_expenses_equal_budget() -> None:
    calc = BudgetCalculator()
    transactions: list[dict[str, object]] = [{"amount": 250.0, "type": "expense"}]

    assert calc.is_over_budget(250.0, transactions) is False


def test_get_history_returns_copy_not_mutable_reference() -> None:
    calc = BudgetCalculator()
    transactions = _sample_transactions()
    calc.total_income(transactions)

    history = calc.get_history()
    history.append("tamper")

    assert "tamper" not in calc.get_history()
