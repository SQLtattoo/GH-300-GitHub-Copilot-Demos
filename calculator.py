from typing import Dict, List


Transaction = Dict[str, object]


class BudgetCalculator:
    def __init__(self) -> None:
        """Initialize calculator state and in-memory audit history."""
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
        """Return net cash flow as income minus expenses."""
        result = self.total_income(transactions) - self.total_expenses(transactions)
        self.history.append(f"net_cash_flow = {result}")
        return result

    def remaining_budget(self, monthly_budget: float, transactions: List[Transaction]) -> float:
        """Return remaining budget after subtracting total expenses."""
        result = monthly_budget - self.total_expenses(transactions)
        self.history.append(f"remaining_budget({monthly_budget}) = {result}")
        return result

    def average_expense(self, transactions: List[Transaction]) -> float:
        """Return the arithmetic mean of expense transaction amounts."""
        expenses = [float(item["amount"]) for item in transactions if item.get("type") == "expense"]
        result = sum(expenses) / len(expenses)
        self.history.append(f"average_expense = {result}")
        return result

    def category_percentage(self, category_total: float, total_expenses: float) -> float:
        """Return category spend as a percentage of total expenses."""
        result = (category_total / total_expenses) * 100
        self.history.append(f"category_percentage = {result}")
        return result

    def savings_rate(self, income: float, expenses: float) -> float:
        """Return savings rate percentage based on income and expenses."""
        if income == 0:
            self.history.append("savings_rate = 0.0 (income is zero)")
            return 0.0

        result = ((income - expenses) / income) * 100
        self.history.append(f"savings_rate = {result}")
        return result

    # TODO: Implement forecast_month_end_spend(transactions, days_elapsed, days_in_month)
    # It should estimate month-end spending from current month-to-date expenses.
    def forecast_month_end_spend(self, transactions: List[Transaction], days_elapsed: int, days_in_month: int) -> float:
        """Estimate month-end expense total from month-to-date spending pace."""
        total_expenses = self.total_expenses(transactions)
        if days_elapsed == 0:
            self.history.append("forecast_month_end_spend = 0.0 (no days elapsed)")
            return 0.0

        daily_average = total_expenses / days_elapsed
        forecasted_spend = daily_average * days_in_month
        self.history.append(f"forecast_month_end_spend = {forecasted_spend}")
        return forecasted_spend


    # TODO: Implement is_over_budget(monthly_budget, transactions)
    # It should return True when expenses exceed the monthly budget.
    def is_over_budget(self, monthly_budget: float, transactions: List[Transaction]) -> bool:
        """Return True when total expenses are greater than monthly budget."""
        total_expenses = self.total_expenses(transactions)
        over_budget = total_expenses > monthly_budget
        self.history.append(f"is_over_budget({monthly_budget}) = {over_budget}")
        return over_budget

    def get_history(self) -> List[str]:
        """Return a copy of recorded calculation history entries."""
        return self.history.copy()


# Backward-compatible alias used by a few older demo prompts.
Calculator = BudgetCalculator
