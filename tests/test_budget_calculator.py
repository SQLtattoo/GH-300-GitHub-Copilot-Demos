"""Starter tests for BudgetCalculator."""


def test_total_income(calculator, sample_transactions):
    """Calculate income for a happy-path transaction set."""
    assert calculator.total_income(sample_transactions) == 5000.0


def test_total_expenses(calculator, sample_transactions):
    """Calculate expenses for a happy-path transaction set."""
    assert calculator.total_expenses(sample_transactions) == 160.0


def test_remaining_budget(calculator, sample_transactions):
    """Calculate remaining budget for the sample month."""
    assert calculator.remaining_budget(1000.0, sample_transactions) == 840.0