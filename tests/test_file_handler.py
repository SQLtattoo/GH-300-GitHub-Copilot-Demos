"""Starter tests for BudgetFileHandler."""

import json

import pytest


def test_read_transactions_csv(file_handler, tmp_path):
    """Read transactions from a simple CSV file."""
    csv_file = tmp_path / "transactions.csv"
    csv_file.write_text(
        "date,merchant,category,amount,type\n"
        "2026-06-01,Payroll,Income,5000.00,income\n"
        "2026-06-02,Grocery,Groceries,120.00,expense\n",
        encoding="utf-8",
    )

    transactions = file_handler.read_transactions_csv("transactions.csv")

    assert len(transactions) == 2
    assert transactions[1]["amount"] == 120.0


def test_processed_files_are_tracked(file_handler, tmp_path):
    """Track files read by the handler."""
    csv_file = tmp_path / "transactions.csv"
    csv_file.write_text(
        "date,merchant,category,amount,type\n"
        "2026-06-02,Grocery,Groceries,120.00,expense\n",
        encoding="utf-8",
    )

    file_handler.read_transactions_csv("transactions.csv")

    assert file_handler.get_processed_files() == ["transactions.csv"]


@pytest.mark.security
def test_read_transactions_json_blocks_path_traversal(file_handler, tmp_path):
    """Reject JSON reads that traverse outside the configured base directory."""
    outside_file = tmp_path.parent / "outside-transactions.json"
    outside_file.write_text(
        json.dumps([{"date": "2026-06-01", "merchant": "Outside", "category": "Misc", "amount": 10.0, "type": "expense"}]),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="outside the base directory"):
        file_handler.read_transactions_json("../outside-transactions.json")