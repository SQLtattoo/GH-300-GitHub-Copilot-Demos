from collections import defaultdict
from typing import Dict, List, Optional


Transaction = Dict[str, object]


class TransactionProcessor:
    def __init__(self) -> None:
        """Initialize processor state used for demo metrics."""
        self.processed_count = 0

    def normalize_category(self, category: str) -> str:
        """Normalize a category label for consistent matching and grouping."""
        self.processed_count += 1
        return category.strip().title()

    def filter_by_month(self, transactions: List[Transaction], month: str) -> List[Transaction]:
        """Return transactions whose date starts with the provided YYYY-MM prefix."""
        self.processed_count += 1
        return [item for item in transactions if str(item.get("date", "")).startswith(month)]

    def expenses_only(self, transactions: List[Transaction]) -> List[Transaction]:
        """Return only transactions marked as expenses."""
        self.processed_count += 1
        return [item for item in transactions if item.get("type") == "expense"]

    def group_expenses_by_category(self, transactions: List[Transaction]) -> Dict[str, float]:
        """Return total expense amount grouped by normalized category."""
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
        """Return the highest-value expense transaction, if one exists."""
        expenses = self.expenses_only(transactions)
        if not expenses:
            return None
        return max(expenses, key=lambda item: float(item["amount"]))

    def find_duplicate_transactions(self, transactions: List[Transaction]) -> List[Transaction]:
        """Return unique transaction entries that appear more than once."""
        duplicates: List[Transaction] = []
        duplicate_counts: Dict[tuple, int] = defaultdict(int)
        seen_items = set()

        for item in transactions:
            key = (item.get("date"), item.get("amount"), item.get("merchant"))
            duplicate_counts[key] += 1

        for item in transactions:
            key = (item.get("date"), item.get("amount"), item.get("merchant"))
            if duplicate_counts[key] <= 1:
                continue

            signature = tuple(sorted(item.items()))
            if signature in seen_items:
                continue

            seen_items.add(signature)
            duplicates.append(item)

        return duplicates

    def validate_transaction(self, transaction: Transaction) -> bool:
        """Validate that a transaction contains all required fields."""
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
        """Return how many normalization/filter operations have been processed."""
        return self.processed_count


# Backward-compatible alias used by older demo prompts.
DataProcessor = TransactionProcessor