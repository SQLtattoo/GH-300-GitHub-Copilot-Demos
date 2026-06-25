"""Starter tests for TransactionProcessor."""


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


def test_find_duplicate_transactions_no_duplicates(processor, sample_transactions):
    """Return an empty list when there are no duplicates."""
    assert processor.find_duplicate_transactions(sample_transactions) == []


def test_find_duplicate_transactions_returns_matches_in_order(processor):
    """Return each duplicated transaction once, in order of first appearance."""
    transactions = [
        {"date": "2026-06-02", "merchant": "Grocery", "category": "Groceries", "amount": 120.0, "type": "expense"},
        {"date": "2026-06-03", "merchant": "Transit", "category": "Transport", "amount": 40.0, "type": "expense"},
        {"date": "2026-06-02", "merchant": "Grocery", "category": "Groceries", "amount": 120.0, "type": "expense"},
        {"date": "2026-06-03", "merchant": "Transit", "category": "Transport", "amount": 40.0, "type": "expense"},
    ]

    duplicates = processor.find_duplicate_transactions(transactions)

    assert duplicates == [
        {"date": "2026-06-02", "merchant": "Grocery", "category": "Groceries", "amount": 120.0, "type": "expense"},
        {"date": "2026-06-03", "merchant": "Transit", "category": "Transport", "amount": 40.0, "type": "expense"},
    ]


def test_find_duplicate_transactions_matches_on_date_amount_merchant(processor):
    """Match duplicates on date, amount, and merchant even when other fields differ."""
    transactions = [
        {"date": "2026-06-02", "merchant": "Grocery", "category": "Groceries", "amount": 120.0, "type": "expense"},
        {"date": "2026-06-02", "merchant": "Grocery", "category": "Food", "amount": 120.0, "type": "expense"},
    ]

    duplicates = processor.find_duplicate_transactions(transactions)

    assert duplicates == transactions


# --- Remaining processor behavior --------------------------------------------------


def test_normalize_category_trims_and_titlecases(processor):
    """Categories are stripped and title-cased, and the op count increments."""
    assert processor.normalize_category("  groceries ") == "Groceries"
    assert processor.get_processed_count() == 1


def test_expenses_only_filters_income(processor, sample_transactions):
    """expenses_only drops non-expense rows."""
    expenses = processor.expenses_only(sample_transactions)
    assert len(expenses) == 2
    assert all(item["type"] == "expense" for item in expenses)


def test_group_expenses_by_category(processor):
    """Expenses are summed per normalized category."""
    transactions = [
        {"category": "Groceries", "amount": 120.0, "type": "expense"},
        {"category": "groceries", "amount": 30.0, "type": "expense"},
        {"category": "Transport", "amount": 40.0, "type": "expense"},
        {"category": "Income", "amount": 5000.0, "type": "income"},
    ]
    totals = processor.group_expenses_by_category(transactions)
    assert totals == {"Groceries": 150.0, "Transport": 40.0}


def test_largest_expense_returns_none_when_empty(processor):
    """largest_expense returns None when there are no expenses."""
    assert processor.largest_expense([]) is None


def test_validate_transaction_rejects_missing_fields(processor):
    """Transactions missing a required field fail validation."""
    incomplete = {"date": "2026-06-02", "merchant": "Grocery", "amount": 10.0, "type": "expense"}
    assert processor.validate_transaction(incomplete) is False


def test_top_merchants_ranks_expense_spending(processor):
    """Merchants are ranked by total expense spending, descending."""
    transactions = [
        {"merchant": "Grocery", "amount": 120.0, "type": "expense"},
        {"merchant": "Transit", "amount": 40.0, "type": "expense"},
        {"merchant": "Grocery", "amount": 30.0, "type": "expense"},
        {"merchant": "Payroll", "amount": 5000.0, "type": "income"},
    ]

    assert processor.top_merchants(transactions) == [
        ("Grocery", 150.0),
        ("Transit", 40.0),
    ]


def test_top_merchants_respects_limit(processor):
    """Only the top N merchants are returned."""
    transactions = [
        {"merchant": "A", "amount": 30.0, "type": "expense"},
        {"merchant": "B", "amount": 20.0, "type": "expense"},
        {"merchant": "C", "amount": 10.0, "type": "expense"},
    ]

    assert processor.top_merchants(transactions, limit=2) == [("A", 30.0), ("B", 20.0)]


def test_top_merchants_empty_when_no_expenses(processor):
    """An empty list is returned when there are no expenses."""
    assert processor.top_merchants([]) == []
    assert processor.top_merchants([{"merchant": "P", "amount": 5000.0, "type": "income"}]) == []


def test_top_merchants_non_positive_limit(processor, sample_transactions):
    """A non-positive limit returns an empty list."""
    assert processor.top_merchants(sample_transactions, limit=0) == []