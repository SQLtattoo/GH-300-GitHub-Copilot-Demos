import pytest

from data_processor import DataProcessor, TransactionProcessor


pytestmark = pytest.mark.unit


def test_normalizes_category_and_counts_processing():
    processor = TransactionProcessor()

    assert processor.normalize_category("  hOME office ") == "Home Office"
    assert processor.get_processed_count() == 1


def test_filters_by_month_without_mutating_input(transactions):
    processor = TransactionProcessor()
    original = list(transactions)

    result = processor.filter_by_month(transactions, "2026-06")

    assert len(result) == 3
    assert result is not transactions
    assert transactions == original
    assert processor.get_processed_count() == 1


def test_month_filter_tolerates_missing_and_non_string_dates():
    processor = TransactionProcessor()
    records = [{"date": 20260601}, {}, {"date": "2026-06-02"}]

    assert processor.filter_by_month(records, "2026-06") == [records[2]]


def test_expenses_grouping_and_largest_expense(transactions):
    processor = TransactionProcessor()

    assert processor.expenses_only(transactions) == transactions[1:]
    assert processor.group_expenses_by_category(transactions) == {
        "Groceries": 175.5,
        "Dining": 24.5,
    }
    assert processor.largest_expense(transactions) == transactions[1]
    assert processor.get_processed_count() == 6


def test_grouping_defaults_missing_category_and_amount():
    processor = TransactionProcessor()

    assert processor.group_expenses_by_category([{"type": "expense"}]) == {"": 0.0}


def test_summarize_by_merchant_returns_top_three_expense_totals(transactions):
    processor = TransactionProcessor()
    records = transactions + [
        {"merchant": "Cafe", "amount": 100.0, "type": "expense"},
        {"merchant": "Bookshop", "amount": 75.0, "type": "expense"},
        {"merchant": "Pharmacy", "amount": 25.0, "type": "expense"},
    ]

    assert processor.summarize_by_merchant(records) == [
        {"merchant": "Market", "total": 175.5},
        {"merchant": "Cafe", "total": 124.5},
        {"merchant": "Bookshop", "total": 75.0},
    ]


def test_summarize_by_merchant_returns_empty_list_without_expenses():
    processor = TransactionProcessor()

    assert processor.summarize_by_merchant([]) == []
    assert processor.summarize_by_merchant(
        [{"merchant": "Payroll", "amount": 5000.0, "type": "income"}]
    ) == []


def test_largest_expense_returns_none_when_no_expenses():
    processor = TransactionProcessor()

    assert processor.largest_expense([{"type": "income", "amount": 1}]) is None


def test_duplicate_detection_returns_each_distinct_matching_record_once():
    first = {"date": "2026-06-01", "amount": 10.0, "merchant": "Cafe", "type": "expense"}
    equivalent = dict(first)
    variant = {**first, "category": "Dining"}
    unique = {"date": "2026-06-02", "amount": 10.0, "merchant": "Cafe"}
    processor = TransactionProcessor()

    assert processor.find_duplicate_transactions([first, equivalent, variant, unique]) == [first, variant]


def test_duplicate_detection_handles_missing_key_fields():
    first = {"type": "expense"}
    second = {"type": "income"}
    processor = TransactionProcessor()

    assert processor.find_duplicate_transactions([first, first.copy(), second]) == [first, second]


@pytest.mark.parametrize("missing_field", ["date", "merchant", "category", "amount", "type"])
def test_validation_rejects_each_missing_required_field(missing_field):
    transaction = {
        "date": "2026-06-01",
        "merchant": "Cafe",
        "category": "Dining",
        "amount": 10.0,
        "type": "expense",
    }
    transaction.pop(missing_field)

    assert TransactionProcessor().validate_transaction(transaction) is False


def test_validation_accepts_required_fields_even_when_values_are_none():
    transaction = {field: None for field in ["date", "merchant", "category", "amount", "type"]}

    assert TransactionProcessor().validate_transaction(transaction) is True


def test_legacy_alias_is_preserved():
    assert DataProcessor is TransactionProcessor