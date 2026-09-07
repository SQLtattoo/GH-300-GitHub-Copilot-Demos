"""
Financial calculation helpers for the Budget Buddy demo app.

This module provides the completed budget calculations used by the demo app.
"""

from typing import Dict, List


Transaction = Dict[str, object]


class BudgetCalculator:

    def __init__(self) -> None:
        """Initialize an empty calculation history."""
        self.history: List[str] = []

    def total_income(self, transactions: List[Transaction]) -> float:
        """Return the total amount of income transactions."""
        total = sum(float(item["amount"]) for item in transactions if item.get("type") == "income")
        self.history.append(f"total_income = {total}")
        return total

    def total_expenses(self, transactions: List[Transaction]) -> float:
        """Return the total amount of expense transactions."""
        total = sum(float(item["amount"]) for item in transactions if item.get("type") == "expense")
        self.history.append(f"total_expenses = {total}")
        return total

    def net_cash_flow(self, transactions: List[Transaction]) -> float:
        """Return income minus expenses for the transactions."""
        result = self.total_income(transactions) - self.total_expenses(transactions)
        self.history.append(f"net_cash_flow = {result}")
        return result

    def remaining_budget(self, monthly_budget: float, transactions: List[Transaction]) -> float:
        """Return the monthly budget remaining after expenses."""
        result = monthly_budget - self.total_expenses(transactions)
        self.history.append(f"remaining_budget({monthly_budget}) = {result}")
        return result

    def average_expense(self, transactions: List[Transaction]) -> float:
        """Return the average amount of the expense transactions."""
        expenses = [float(item["amount"]) for item in transactions if item.get("type") == "expense"]
        result = sum(expenses) / len(expenses) if expenses else 0.0
        self.history.append(f"average_expense = {result}")
        return result

    def category_percentage(self, category_total: float, total_expenses: float) -> float:
        """Return a category total as a percentage of all expenses."""
        result = (category_total / total_expenses) * 100 if total_expenses else 0.0
        self.history.append(f"category_percentage = {result}")
        return result

    def savings_rate(self, income: float, expenses: float) -> float:
        """Return savings as a percentage of income."""
        result = ((income - expenses) / income) * 100 if income else 0.0
        self.history.append(f"savings_rate = {result}")
        return result

    def forecast_month_end_spend(self, transactions: List[Transaction], days_elapsed: int, days_in_month: int) -> float:
        """Estimate month-end expenses from spending to date."""
        if days_elapsed < 1:
            raise ValueError("days_elapsed must be at least 1")
        if days_in_month < days_elapsed:
            raise ValueError("days_in_month must be at least days_elapsed")
        month_to_date_expenses = sum(float(item["amount"]) for item in transactions if item.get("type") == "expense")
        result = (month_to_date_expenses / days_elapsed) * days_in_month
        self.history.append(f"forecast_month_end_spend = {result}")
        return result

    def is_over_budget(self, monthly_budget: float, transactions: List[Transaction]) -> bool:
        """Return whether expenses exceed the monthly budget."""
        total_expenses = self.total_expenses(transactions)
        result = total_expenses > monthly_budget
        self.history.append(f"is_over_budget({monthly_budget}) = {result}")
        return result

    def get_history(self) -> List[str]:
        """Return a copy of the calculation history."""
        return self.history.copy()


# Backward-compatible alias used by a few older demo prompts.
Calculator = BudgetCalculator
