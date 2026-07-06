"""Tests for the TransactionProcessor module."""

from data_processor import DataProcessor, TransactionProcessor


def test_normalize_category():
    processor = TransactionProcessor()
    assert processor.normalize_category("  groceries ") == "Groceries"


def test_filter_by_month(sample_transactions):
    processor = TransactionProcessor()
    filtered = processor.filter_by_month(sample_transactions, "2024-01")
    assert len(filtered) == 4
    assert processor.filter_by_month(sample_transactions, "2024-02") == []


def test_expenses_only(sample_transactions):
    processor = TransactionProcessor()
    expenses = processor.expenses_only(sample_transactions)
    assert len(expenses) == 3
    assert all(item["type"] == "expense" for item in expenses)


def test_group_expenses_by_category(sample_transactions):
    processor = TransactionProcessor()
    totals = processor.group_expenses_by_category(sample_transactions)
    assert totals == {"Groceries": 200.0, "Dining": 50.0, "Utilities": 150.0}


def test_largest_expense(sample_transactions):
    processor = TransactionProcessor()
    largest = processor.largest_expense(sample_transactions)
    assert largest is not None
    assert largest["amount"] == 200.0


def test_largest_expense_empty():
    processor = TransactionProcessor()
    assert processor.largest_expense([]) is None


def test_top_merchants(sample_transactions):
    processor = TransactionProcessor()
    top = processor.top_merchants(sample_transactions)
    assert top == [("Grocer", 200.0), ("Utility Co", 150.0), ("Cafe", 50.0)]


def test_top_merchants_aggregates_and_limits():
    processor = TransactionProcessor()
    txns = [
        {"merchant": "Cafe", "category": "Dining", "amount": 5.0, "type": "expense"},
        {"merchant": "Cafe", "category": "Dining", "amount": 7.0, "type": "expense"},
        {"merchant": "Grocer", "category": "Groceries", "amount": 30.0, "type": "expense"},
        {"merchant": "Boss", "category": "Salary", "amount": 999.0, "type": "income"},
    ]
    assert processor.top_merchants(txns, limit=1) == [("Grocer", 30.0)]
    assert processor.top_merchants(txns) == [("Grocer", 30.0), ("Cafe", 12.0)]


def test_top_merchants_empty():
    processor = TransactionProcessor()
    assert processor.top_merchants([]) == []


def test_find_duplicate_transactions():
    processor = TransactionProcessor()
    txns = [
        {"date": "2024-01-01", "amount": 10.0, "merchant": "A"},
        {"date": "2024-01-01", "amount": 10.0, "merchant": "A"},
        {"date": "2024-01-02", "amount": 20.0, "merchant": "B"},
    ]
    duplicates = processor.find_duplicate_transactions(txns)
    # The starter implementation reports each duplicated transaction once.
    assert len(duplicates) == 1
    assert duplicates[0]["merchant"] == "A"


def test_find_duplicate_transactions_none():
    processor = TransactionProcessor()
    txns = [
        {"date": "2024-01-01", "amount": 10.0, "merchant": "A"},
        {"date": "2024-01-02", "amount": 20.0, "merchant": "B"},
    ]
    assert processor.find_duplicate_transactions(txns) == []


def test_validate_transaction_valid():
    processor = TransactionProcessor()
    txn = {"date": "2024-01-01", "merchant": "A", "category": "Food", "amount": 1.0, "type": "expense"}
    assert processor.validate_transaction(txn) is True


def test_validate_transaction_missing_field():
    processor = TransactionProcessor()
    assert processor.validate_transaction({"date": "2024-01-01"}) is False


def test_get_processed_count(sample_transactions):
    processor = TransactionProcessor()
    processor.expenses_only(sample_transactions)
    processor.normalize_category("food")
    assert processor.get_processed_count() == 2


def test_backward_compatible_alias():
    assert DataProcessor is TransactionProcessor
