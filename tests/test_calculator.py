import pytest

from calculator import BudgetCalculator, Calculator


pytestmark = pytest.mark.unit


def test_calculates_totals_cash_flow_and_remaining_budget(transactions):
    calculator = BudgetCalculator()

    assert calculator.total_income(transactions) == pytest.approx(5000.0)
    assert calculator.total_expenses(transactions) == pytest.approx(200.0)
    assert calculator.net_cash_flow(transactions) == pytest.approx(4800.0)
    assert calculator.remaining_budget(1000.0, transactions) == pytest.approx(800.0)


def test_supports_numeric_strings_and_ignores_unrecognized_types():
    transactions = [
        {"type": "income", "amount": "10.25"},
        {"type": "expense", "amount": "2.75"},
        {"type": "refund", "amount": "1000"},
        {"amount": "999"},
    ]
    calculator = BudgetCalculator()

    assert calculator.total_income(transactions) == pytest.approx(10.25)
    assert calculator.total_expenses(transactions) == pytest.approx(2.75)


def test_empty_totals_are_zero_and_negative_budget_is_supported():
    calculator = BudgetCalculator()

    assert calculator.total_income([]) == 0
    assert calculator.total_expenses([]) == 0
    assert calculator.remaining_budget(-10.0, []) == -10.0


def test_average_percentage_savings_and_forecast(transactions):
    calculator = BudgetCalculator()

    assert calculator.average_expense(transactions) == pytest.approx(200.0 / 3)
    assert calculator.category_percentage(50.0, 200.0) == pytest.approx(25.0)
    assert calculator.savings_rate(5000.0, 200.0) == pytest.approx(96.0)
    assert calculator.forecast_month_end_spend(transactions, 10, 30) == pytest.approx(600.0)


@pytest.mark.parametrize(
    ("operation", "args"),
    [
        ("average_expense", ([],)),
        ("category_percentage", (10.0, 0.0)),
        ("savings_rate", (0.0, 10.0)),
        ("forecast_month_end_spend", ([], 0, 30)),
    ],
)
def test_undefined_zero_denominator_operations_raise(operation, args):
    calculator = BudgetCalculator()

    with pytest.raises(ZeroDivisionError):
        getattr(calculator, operation)(*args)


def test_over_budget_uses_strict_boundary(transactions):
    calculator = BudgetCalculator()

    assert calculator.is_over_budget(199.99, transactions) is True
    assert calculator.is_over_budget(200.0, transactions) is False


def test_history_records_nested_operations_and_returns_a_copy(transactions):
    calculator = BudgetCalculator()
    calculator.net_cash_flow(transactions)

    history = calculator.get_history()
    assert history == [
        "total_income = 5000.0",
        "total_expenses = 200.0",
        "net_cash_flow = 4800.0",
    ]

    history.append("tampered")
    assert "tampered" not in calculator.get_history()


def test_legacy_alias_is_preserved():
    assert Calculator is BudgetCalculator