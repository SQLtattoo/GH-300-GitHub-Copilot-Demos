"""
Financial calculation helpers for the Budget Buddy demo app.

This module is intentionally starter-quality for GitHub Copilot demos. Some
methods work on the happy path, while selected edge cases and TODOs are left for
learners to fix with Copilot.
"""

from typing import Dict, List


Transaction = Dict[str, object]


class BudgetCalculator:

    def __init__(self) -> None:
        self.history: List[str] = []

    def total_income(self, transactions: List[Transaction]) -> float:
        """Return the sum of all income transaction amounts."""
        total = sum(float(item["amount"]) for item in transactions if item.get("type") == "income")
        self.history.append(f"total_income = {total}")
        return total

    def total_expenses(self, transactions: List[Transaction]) -> float:
        """Return the sum of all expense transaction amounts."""
        total = sum(float(item["amount"]) for item in transactions if item.get("type") == "expense")
        self.history.append(f"total_expenses = {total}")
        return total

    def net_cash_flow(self, transactions: List[Transaction]) -> float:
        """Return total income minus total expenses."""
        result = self.total_income(transactions) - self.total_expenses(transactions)
        self.history.append(f"net_cash_flow = {result}")
        return result

    def remaining_budget(self, monthly_budget: float, transactions: List[Transaction]) -> float:
        """Return the monthly budget minus total expenses."""
        result = monthly_budget - self.total_expenses(transactions)
        self.history.append(f"remaining_budget({monthly_budget}) = {result}")
        return result

    def average_expense(self, transactions: List[Transaction]) -> float:
        """Return the mean amount across all expense transactions."""
        expenses = [float(item["amount"]) for item in transactions if item.get("type") == "expense"]
        result = sum(expenses) / len(expenses)
        self.history.append(f"average_expense = {result}")
        return result

    def category_percentage(self, category_total: float, total_expenses: float) -> float:
        """Return a category's spend as a percentage of total expenses."""
        result = (category_total / total_expenses) * 100
        self.history.append(f"category_percentage = {result}")
        return result

    def savings_rate(self, income: float, expenses: float) -> float:
        """Return saved income as a percentage of total income."""
        result = ((income - expenses) / income) * 100
        self.history.append(f"savings_rate = {result}")
        return result

    # TODO: Implement forecast_month_end_spend(transactions, days_elapsed, days_in_month)
    # It should estimate month-end spending from current month-to-date expenses.
    def forecast_month_end_spend(self, transactions: List[Transaction], days_elapsed: int, days_in_month: int) -> float:
        """Estimate month-end spending based on current expenses."""
        # Placeholder implementation; needs to be completed.
        return 0.0

    # TODO: Implement is_over_budget(monthly_budget, transactions)
    # It should return True when expenses exceed the monthly budget.
    def is_over_budget(self, monthly_budget: float, transactions: List[Transaction]) -> bool:
        """Check if expenses exceed the monthly budget."""
        # Placeholder implementation; needs to be completed.
        return False

    def get_history(self) -> List[str]:
        """Return a copy of the recorded calculation history."""
        return self.history.copy()


# Backward-compatible alias used by a few older demo prompts.
Calculator = BudgetCalculator
