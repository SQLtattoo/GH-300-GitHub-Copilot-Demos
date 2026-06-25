"""
Financial calculation helpers for the Budget Buddy demo app.

This module is intentionally starter-quality for GitHub Copilot demos. Some
methods work on the happy path, while selected edge cases and TODOs are left for
learners to fix with Copilot.
"""

from typing import Dict, List


Transaction = Dict[str, object]


class BudgetCalculator:
    """Perform budget and expense calculations."""

    def __init__(self) -> None:
        """Initialize calculation history."""
        self.history: List[str] = []

    def total_income(self, transactions: List[Transaction]) -> float:
        """Return the sum of all income transactions."""
        total = sum(float(item["amount"]) for item in transactions if item.get("type") == "income")
        self.history.append(f"total_income = {total}")
        return total

    def total_expenses(self, transactions: List[Transaction]) -> float:
        """Return the sum of all expense transactions."""
        total = sum(float(item["amount"]) for item in transactions if item.get("type") == "expense")
        self.history.append(f"total_expenses = {total}")
        return total

    def net_cash_flow(self, transactions: List[Transaction]) -> float:
        """Return income minus expenses."""
        result = self.total_income(transactions) - self.total_expenses(transactions)
        self.history.append(f"net_cash_flow = {result}")
        return result

    def remaining_budget(self, monthly_budget: float, transactions: List[Transaction]) -> float:
        """Return the remaining budget after expenses."""
        result = monthly_budget - self.total_expenses(transactions)
        self.history.append(f"remaining_budget({monthly_budget}) = {result}")
        return result

    def average_expense(self, transactions: List[Transaction]) -> float:
        """Return the average amount for expense transactions."""
        expenses = [float(item["amount"]) for item in transactions if item.get("type") == "expense"]
        result = sum(expenses) / len(expenses)
        self.history.append(f"average_expense = {result}")
        return result

    def category_percentage(self, category_total: float, total_expenses: float) -> float:
        """Return a category's percentage of total expenses."""
        result = (category_total / total_expenses) * 100
        self.history.append(f"category_percentage = {result}")
        return result

    def savings_rate(self, income: float, expenses: float) -> float:
        """Return the savings rate as a percentage of income.

        Returns 0.0 when income is zero to avoid ZeroDivisionError.
        """
        if income == 0:
            self.history.append("savings_rate = 0.0 (income is zero)")
            return 0.0
        result = ((income - expenses) / income) * 100
        self.history.append(f"savings_rate = {result}")
        return result

    # TODO: Implement forecast_month_end_spend(transactions, days_elapsed, days_in_month)
    # It should estimate month-end spending from current month-to-date expenses.
    def forecast_month_end_spend(self, transactions: List[Transaction], days_elapsed: int, days_in_month: int) -> float:
        """Estimate month-end spending based on current expenses."""
        # Placeholder implementation
        current_expenses = self.total_expenses(transactions)
        if days_elapsed == 0:   
            self.history.append("forecast_month_end_spend = 0.0 (no days elapsed)")
            return 0.0  
        estimated_month_end_spend = (current_expenses / days_elapsed) * days_in_month
        self.history.append(f"forecast_month_end_spend = {estimated_month_end_spend}")
        return estimated_month_end_spend
    

    # TODO: Implement is_over_budget(monthly_budget, transactions)
    # It should return True when expenses exceed the monthly budget.
    def is_over_budget(self, monthly_budget: float, transactions: List[Transaction]) -> bool:
        """Check if expenses exceed the monthly budget."""
        total_expenses = self.total_expenses(transactions)
        over_budget = total_expenses > monthly_budget
        self.history.append(f"is_over_budget({monthly_budget}) = {over_budget}")
        return over_budget

    def get_history(self) -> List[str]:
        """Return a copy of calculation history."""
        return self.history.copy()


# Backward-compatible alias used by a few older demo prompts.
Calculator = BudgetCalculator
