from data_processor import DataProcessor, TransactionProcessor


def _sample_transactions() -> list[dict[str, object]]:
    return [
        {"date": "2026-06-01", "merchant": "Store", "category": "groceries", "amount": 100.0, "type": "expense"},
        {"date": "2026-06-01", "merchant": "Store", "category": "Groceries", "amount": 100.0, "type": "expense"},
        {"date": "2026-06-05", "merchant": "Cafe", "category": "dining", "amount": 25.0, "type": "expense"},
        {"date": "2026-06-10", "merchant": "Employer", "category": "Salary", "amount": 3000.0, "type": "income"},
    ]


def test_transaction_processor_core_functions() -> None:
    processor = TransactionProcessor()
    transactions = _sample_transactions()

    assert processor.normalize_category("  groceries ") == "Groceries"

    june_rows = processor.filter_by_month(transactions, "2026-06")
    assert len(june_rows) == 4

    expenses = processor.expenses_only(transactions)
    assert len(expenses) == 3

    grouped = processor.group_expenses_by_category(transactions)
    assert grouped == {"Groceries": 200.0, "Dining": 25.0}

    largest = processor.largest_expense(transactions)
    assert largest is not None
    assert largest["amount"] == 100.0

    duplicates = processor.find_duplicate_transactions(transactions)
    assert len(duplicates) == 2
    assert all(item["merchant"] == "Store" for item in duplicates)

    assert processor.validate_transaction(transactions[0]) is True
    assert processor.validate_transaction({"date": "2026-06-01"}) is False

    assert processor.get_processed_count() > 0


def test_largest_expense_none_when_no_expenses() -> None:
    processor = TransactionProcessor()
    rows = [{"date": "2026-06-01", "merchant": "Employer", "category": "Salary", "amount": 1000.0, "type": "income"}]

    assert processor.largest_expense(rows) is None


def test_largest_expense_ignores_income_with_higher_amount() -> None:
    processor = TransactionProcessor()
    rows = [
        {"date": "2026-06-01", "merchant": "Employer", "category": "Salary", "amount": 5000.0, "type": "income"},
        {"date": "2026-06-03", "merchant": "Airline", "category": "Travel", "amount": 1200.0, "type": "expense"},
        {"date": "2026-06-05", "merchant": "Hotel", "category": "Travel", "amount": 800.0, "type": "expense"},
    ]

    largest = processor.largest_expense(rows)

    assert largest is not None
    assert largest["merchant"] == "Airline"
    assert largest["amount"] == 1200.0


def test_largest_expense_supports_numeric_string_amounts() -> None:
    processor = TransactionProcessor()
    rows = [
        {"date": "2026-06-05", "merchant": "Cafe", "category": "Dining", "amount": "42.75", "type": "expense"},
        {"date": "2026-06-06", "merchant": "Grocer", "category": "Groceries", "amount": "100.25", "type": "expense"},
    ]

    largest = processor.largest_expense(rows)

    assert largest is not None
    assert largest["merchant"] == "Grocer"
    assert largest["amount"] == "100.25"


def test_data_processor_alias_points_to_transaction_processor() -> None:
    processor = DataProcessor()
    assert isinstance(processor, TransactionProcessor)
