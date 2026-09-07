"""Starter tests for TransactionProcessor."""

import pytest


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


def test_find_duplicate_transactions_returns_each_matching_value_once(processor):
    """Return duplicate transaction values once, preserving first-seen order."""
    grocery = {
        "date": "2026-06-01",
        "merchant": "Grocery",
        "category": "food",
        "amount": 42.50,
        "type": "expense",
    }
    reclassified_grocery = {**grocery, "category": "household"}
    transactions = [grocery, dict(grocery), reclassified_grocery]

    assert processor.find_duplicate_transactions(transactions) == [
        grocery,
        reclassified_grocery,
    ]


def test_find_duplicate_transactions_ignores_unique_transactions(processor):
    """Return no duplicates when each comparison key occurs only once."""
    transactions = [
        {"date": "2026-06-01", "merchant": "Grocery", "amount": 42.50},
        {"date": "2026-06-02", "merchant": "Grocery", "amount": 42.50},
        {"date": "2026-06-01", "merchant": "Cafe", "amount": 8.25},
    ]

    assert processor.find_duplicate_transactions(transactions) == []


def test_group_expenses_by_category_normalizes_and_totals(processor):
    """Group only expenses and normalize equivalent category names."""
    transactions = [
        {"category": " groceries ", "amount": 10.0, "type": "expense"},
        {"category": "GROCERIES", "amount": 15.5, "type": "expense"},
        {"category": "groceries", "amount": 100.0, "type": "income"},
    ]

    assert processor.group_expenses_by_category(transactions) == {"Groceries": 25.5}


@pytest.mark.parametrize(
    "changes",
    [
        {"amount": -1},
        {"amount": "not-a-number"},
        {"amount": True},
        {"type": "transfer"},
        {"merchant": ""},
    ],
)
def test_validate_transaction_rejects_invalid_values(processor, sample_transactions, changes):
    """Reject invalid values even when all required fields are present."""
    transaction = {**sample_transactions[0], **changes}

    assert processor.validate_transaction(transaction) is False


def test_validate_transaction_rejects_missing_fields(processor):
    """Reject transactions that omit required fields."""
    assert processor.validate_transaction({"amount": 10.0}) is False


def test_sort_transactions_supports_amount_and_text(processor, sample_transactions):
    """Sort numeric and text fields without mutating the input list."""
    original = sample_transactions.copy()

    by_amount = processor.sort_transactions(sample_transactions, "amount", descending=True)
    by_merchant = processor.sort_transactions(sample_transactions, "merchant")

    assert [item["amount"] for item in by_amount] == [5000.0, 120.0, 40.0]
    assert [item["merchant"] for item in by_merchant] == ["Grocery", "Payroll", "Transit"]
    assert sample_transactions == original


def test_sort_transactions_rejects_unknown_field(processor):
    """Reject sort fields outside the supported contract."""
    with pytest.raises(ValueError, match="Unsupported sort field"):
        processor.sort_transactions([], "type")


def test_spending_alerts_returns_only_exceeded_limits(processor, sample_transactions):
    """Return normalized category totals strictly above their limits."""
    limits = {" groceries ": 100.0, "Transport": 40.0}

    assert processor.spending_alerts(sample_transactions, limits) == {"Groceries": 120.0}


def test_spending_alerts_rejects_negative_limits(processor):
    """Reject nonsensical negative category limits."""
    with pytest.raises(ValueError, match="non-negative"):
        processor.spending_alerts([], {"Groceries": -1.0})


def test_summarize_by_merchant_totals_expenses_only(processor, sample_transactions):
    """Summarize repeated expense merchants without including income."""
    transactions = sample_transactions + [
        {"merchant": "Grocery", "amount": 5.0, "type": "expense"},
    ]

    assert processor.summarize_by_merchant(transactions) == {
        "Grocery": 125.0,
        "Transit": 40.0,
    }


def test_top_merchants_ranks_expense_totals_with_a_limit(processor):
    """Rank merchants by total expense and use names to break ties."""
    transactions = [
        {"merchant": "Cafe", "amount": 20.0, "type": "expense"},
        {"merchant": "Market", "amount": 30.0, "type": "expense"},
        {"merchant": "Cafe", "amount": 15.0, "type": "expense"},
        {"merchant": "Bakery", "amount": 35.0, "type": "expense"},
        {"merchant": "Payroll", "amount": 5000.0, "type": "income"},
    ]

    assert processor.top_merchants(transactions, limit=2) == [
        ("Bakery", 35.0),
        ("Cafe", 35.0),
    ]


def test_top_merchants_handles_empty_transactions(processor):
    """Return an empty ranking when there are no expenses."""
    assert processor.top_merchants([]) == []


def test_largest_expense_returns_none_without_expenses(processor):
    """Return None when no expense transaction exists."""
    assert processor.largest_expense([]) is None


def test_processed_count_tracks_public_processing(processor):
    """Expose that processing operations occurred without prescribing internals."""
    processor.normalize_category(" food ")
    processor.filter_by_month([], "2026-06")

    assert processor.get_processed_count() == 2