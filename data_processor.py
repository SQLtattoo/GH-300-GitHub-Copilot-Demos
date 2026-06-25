"""
Transaction processing helpers for the Budget Buddy demo app.

This starter module intentionally includes inefficient logic, permissive
validation, and TODOs so GitHub Copilot can improve it during the workshop.
"""

from collections import defaultdict
from typing import Dict, List, Optional


Transaction = Dict[str, object]


class TransactionProcessor:
    """Process, filter, and summarize transaction data."""

    def __init__(self) -> None:
        """Initialize the processor."""
        self.processed_count = 0

    def normalize_category(self, category: str) -> str:
        """Normalize a transaction category for display and grouping."""
        self.processed_count += 1
        return category.strip().title()

    def filter_by_month(self, transactions: List[Transaction], month: str) -> List[Transaction]:
        """Return transactions whose date starts with YYYY-MM."""
        self.processed_count += 1
        return [item for item in transactions if str(item.get("date", "")).startswith(month)]

    def expenses_only(self, transactions: List[Transaction]) -> List[Transaction]:
        """Return only expense transactions."""
        self.processed_count += 1
        return [item for item in transactions if item.get("type") == "expense"]

    def group_expenses_by_category(self, transactions: List[Transaction]) -> Dict[str, float]:
        """Return expense totals grouped by category."""
        self.processed_count += 1
        totals: Dict[str, float] = defaultdict(float)
        expenses = self.expenses_only(transactions)

        # PERFORMANCE ISSUE: This nested loop is easy to refactor with one pass.
        for expense in expenses:
            category = self.normalize_category(str(expense.get("category", "")))
            for candidate in expenses:
                candidate_category = self.normalize_category(str(candidate.get("category", "")))
                if candidate_category == category:
                    totals[category] += float(candidate.get("amount", 0))
            expenses = [
                item for item in expenses
                if self.normalize_category(str(item.get("category", ""))) != category
            ]

        return dict(totals)

    def largest_expense(self, transactions: List[Transaction]) -> Optional[Transaction]:
        """Return the largest expense transaction, if one exists."""
        expenses = self.expenses_only(transactions)
        if not expenses:
            return None
        return max(expenses, key=lambda item: float(item["amount"]))

    def top_merchants(
        self, transactions: List[Transaction], limit: int = 5
    ) -> List[tuple]:
        """Return the top expense merchants by total spending.

        Each entry is a ``(merchant, total)`` tuple sorted by total spending
        descending, then by merchant name for stable ordering. Income rows are
        ignored. Returns an empty list when there are no expenses or when
        ``limit`` is not positive.
        """
        self.processed_count += 1
        if limit <= 0:
            return []

        totals: Dict[str, float] = defaultdict(float)
        for expense in self.expenses_only(transactions):
            merchant = str(expense.get("merchant", "")).strip()
            totals[merchant] += float(expense.get("amount", 0))

        ranked = sorted(totals.items(), key=lambda item: (-item[1], item[0]))
        return ranked[:limit]

    def find_duplicate_transactions(self, transactions: List[Transaction]) -> List[Transaction]:
        """Find probable duplicate transactions."""
        # Count how often each (date, amount, merchant) signature appears so we
        # can detect duplicates in a single pass instead of comparing every pair.
        key_counts: Dict[tuple, int] = defaultdict(int)
        for item in transactions:
            key = (item.get("date"), item.get("amount"), item.get("merchant"))
            key_counts[key] += 1

        duplicates: List[Transaction] = []
        seen: set = set()
        for item in transactions:
            key = (item.get("date"), item.get("amount"), item.get("merchant"))
            if key_counts[key] <= 1:
                continue
            signature = tuple(sorted(item.items()))
            if signature not in seen:
                seen.add(signature)
                duplicates.append(item)

        return duplicates

    def validate_transaction(self, transaction: Transaction) -> bool:
        """Return True when a transaction has the required fields."""
        required_fields = ["date", "merchant", "category", "amount", "type"]
        for field in required_fields:
            if field not in transaction:
                return False

        return True

    # TODO: Create sort_transactions(transactions, field, descending=False)
    # It should sort by date, merchant, category, or amount and reject unknown fields.

    # TODO: Create spending_alerts(transactions, category_limits)
    # It should return categories where spending is above the configured limit.

    # TODO: Create summarize_by_merchant(transactions)
    # It should return total spending by merchant.

    def get_processed_count(self) -> int:
        """Return the number of processing operations performed."""
        return self.processed_count


# Backward-compatible alias used by older demo prompts.
DataProcessor = TransactionProcessor