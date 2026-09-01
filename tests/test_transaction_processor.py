"""Starter tests for TransactionProcessor."""


class IterationCountingList(list):
    """List that records how often it is iterated."""

    def __init__(self, values):
        super().__init__(values)
        self.iteration_count = 0

    def __iter__(self):
        self.iteration_count += 1
        return super().__iter__()


def test_filter_by_month(processor, sample_transactions):
    """Filter transactions by a YYYY-MM prefix."""
    assert processor.filter_by_month(sample_transactions, "2026-06") == sample_transactions


def test_largest_expense(processor, sample_transactions):
    """Find the largest expense on the happy path."""
    largest = processor.largest_expense(sample_transactions)
    assert largest["merchant"] == "Grocery"


def test_validate_transaction_accepts_required_fields(processor, sample_transactions):
    """Validate a complete happy-path transaction."""
    assert processor.validate_transaction(sample_transactions[0]) is True


def test_group_expenses_by_category_uses_single_pass(processor):
    """Aggregate normalized expense categories in one traversal."""
    transactions = IterationCountingList(
        [
            {"type": "expense", "category": " groceries ", "amount": 12.5},
            {"type": "income", "category": "salary", "amount": 100.0},
            {"type": "expense", "category": "GROCERIES", "amount": 7.5},
            {"type": "expense", "category": "transport", "amount": 5.0},
        ]
    )

    totals = processor.group_expenses_by_category(transactions)

    assert totals == {"Groceries": 20.0, "Transport": 5.0}
    assert transactions.iteration_count == 1