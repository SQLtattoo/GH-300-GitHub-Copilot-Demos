"""Starter tests for TransactionProcessor."""

import pytest


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


class TestFilteringAndNormalization:
    def test_normalize_category_strips_and_title_cases(self, processor):
        assert processor.normalize_category("  HOME utilities ") == "Home Utilities"
        assert processor.get_processed_count() == 1

    def test_filter_by_month_ignores_missing_and_nonmatching_dates(self, processor):
        transactions = [
            {"date": "2026-06-01"},
            {"date": "2026-07-01"},
            {},
            {"date": None},
        ]

        assert processor.filter_by_month(transactions, "2026-06") == [transactions[0]]

    def test_expenses_only_handles_empty_and_mixed_transactions(self, processor):
        transactions = [{"type": "income"}, {"type": "expense"}, {}]

        assert processor.expenses_only(transactions) == [transactions[1]]
        assert processor.expenses_only([]) == []
        assert processor.get_processed_count() == 2


class TestSummaries:
    def test_group_expenses_handles_empty_category_and_default_amount(self, processor):
        transactions = [
            {"type": "expense"},
            {"type": "expense", "category": " food ", "amount": 2.5},
            {"type": "income", "category": "ignored", "amount": "invalid"},
        ]

        assert processor.group_expenses_by_category(transactions) == {"": 0.0, "Food": 2.5}
        assert processor.get_processed_count() == 3

    def test_group_expenses_rejects_non_numeric_expense(self, processor):
        with pytest.raises(ValueError):
            processor.group_expenses_by_category(
                [{"type": "expense", "category": "food", "amount": "invalid"}]
            )

    def test_largest_expense_returns_none_without_expenses(self, processor):
        assert processor.largest_expense([{"type": "income", "amount": 100}]) is None
        assert processor.get_processed_count() == 1

    def test_largest_expense_supports_negative_amounts(self, processor):
        transactions = [
            {"type": "expense", "amount": -10},
            {"type": "expense", "amount": -2},
        ]

        assert processor.largest_expense(transactions) is transactions[1]


class TestDuplicateDetection:
    def test_unique_transactions_have_no_duplicates(self, processor, sample_transactions):
        assert processor.find_duplicate_transactions(sample_transactions) == []

    def test_returns_each_distinct_record_sharing_duplicate_identity(self, processor):
        first = {"date": "2026-06-01", "merchant": "Cafe", "amount": 10, "category": "Food"}
        second = {"date": "2026-06-01", "merchant": "Cafe", "amount": 10, "category": "Dining"}

        assert processor.find_duplicate_transactions([first, second]) == [first, second]

    def test_identical_records_are_reported_once(self, processor):
        transaction = {"date": "2026-06-01", "merchant": "Cafe", "amount": 10}

        assert processor.find_duplicate_transactions([transaction, transaction.copy()]) == [transaction]


class TestValidation:
    @pytest.mark.parametrize("missing_field", ["date", "merchant", "category", "amount", "type"])
    def test_validate_transaction_rejects_each_missing_field(
        self, processor, sample_transactions, missing_field
    ):
        transaction = sample_transactions[0].copy()
        del transaction[missing_field]

        assert processor.validate_transaction(transaction) is False