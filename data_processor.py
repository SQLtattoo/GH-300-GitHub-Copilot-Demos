"""
Transaction processing helpers for the Budget Buddy demo app.

This module provides validated, single-pass transaction processing helpers.
"""

from collections import defaultdict
from typing import Dict, FrozenSet, List, Optional, Tuple


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
        for expense in self.expenses_only(transactions):
            category = self.normalize_category(str(expense.get("category", "")))
            totals[category] += float(expense.get("amount", 0))

        return dict(totals)

    def largest_expense(self, transactions: List[Transaction]) -> Optional[Transaction]:
        """Return the largest expense transaction, if one exists."""
        expenses = self.expenses_only(transactions)
        if not expenses:
            return None
        return max(expenses, key=lambda item: float(item["amount"]))

    def find_duplicate_transactions(self, transactions: List[Transaction]) -> List[Transaction]:
        """Find probable duplicate transactions."""
        key_counts: Dict[Tuple[object, object, object], int] = defaultdict(int)
        for item in transactions:
            key = (item.get("date"), item.get("amount"), item.get("merchant"))
            key_counts[key] += 1

        duplicates: List[Transaction] = []
        emitted: set[FrozenSet[Tuple[str, object]]] = set()
        for item in transactions:
            key = (item.get("date"), item.get("amount"), item.get("merchant"))
            marker = frozenset(item.items())
            if key_counts[key] > 1 and marker not in emitted:
                duplicates.append(item)
                emitted.add(marker)

        return duplicates

    def validate_transaction(self, transaction: Transaction) -> bool:
        """Return True when a transaction has valid required fields."""
        required_fields = ["date", "merchant", "category", "amount", "type"]
        if any(field not in transaction for field in required_fields):
            return False
        if any(not str(transaction[field]).strip() for field in ["date", "merchant", "category"]):
            return False
        if transaction["type"] not in {"income", "expense"}:
            return False
        if isinstance(transaction["amount"], bool):
            return False

        try:
            amount = float(transaction["amount"])
        except (TypeError, ValueError):
            return False

        return amount >= 0

    def sort_transactions(
        self,
        transactions: List[Transaction],
        field: str,
        descending: bool = False,
    ) -> List[Transaction]:
        """Return transactions sorted by a supported field."""
        supported_fields = {"date", "merchant", "category", "amount"}
        if field not in supported_fields:
            raise ValueError(f"Unsupported sort field: {field}")

        self.processed_count += 1
        if field == "amount":
            key = lambda item: float(item.get(field, 0))
        else:
            key = lambda item: str(item.get(field, "")).casefold()
        return sorted(transactions, key=key, reverse=descending)

    def spending_alerts(
        self,
        transactions: List[Transaction],
        category_limits: Dict[str, float],
    ) -> Dict[str, float]:
        """Return category totals that exceed configured spending limits."""
        normalized_limits = {
            self.normalize_category(category): float(limit)
            for category, limit in category_limits.items()
        }
        if any(limit < 0 for limit in normalized_limits.values()):
            raise ValueError("Category limits must be non-negative")

        self.processed_count += 1
        totals = self.group_expenses_by_category(transactions)
        return {
            category: total
            for category, total in totals.items()
            if category in normalized_limits and total > normalized_limits[category]
        }

    def summarize_by_merchant(self, transactions: List[Transaction]) -> Dict[str, float]:
        """Return expense totals grouped by merchant."""
        self.processed_count += 1
        totals: Dict[str, float] = defaultdict(float)
        for transaction in self.expenses_only(transactions):
            merchant = str(transaction.get("merchant", "")).strip()
            totals[merchant] += float(transaction.get("amount", 0))
        return dict(totals)

    def top_merchants(
        self,
        transactions: List[Transaction],
        limit: int = 3,
    ) -> List[Tuple[str, float]]:
        """Return the highest-spend merchants, ranked by expense total."""
        if limit <= 0:
            return []

        merchant_totals = self.summarize_by_merchant(transactions)
        # Merchant name provides deterministic ordering when totals are tied.
        ranked_merchants = sorted(
            merchant_totals.items(),
            key=lambda item: (-item[1], item[0].casefold()),
        )
        return ranked_merchants[:limit]

    def get_processed_count(self) -> int:
        """Return the number of processing operations performed."""
        return self.processed_count


# Backward-compatible alias used by older demo prompts.
DataProcessor = TransactionProcessor