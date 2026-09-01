"""Starter tests for BudgetFileHandler."""

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
@pytest.mark.parametrize(
    "operation, outside_name, contents",
    [
        ("read_transactions_csv", "outside.csv", "date,merchant,category,amount,type\n"),
        ("read_transactions_json", "outside.json", "[]"),
        ("write_report_json", "outside.json", "do not overwrite"),
    ],
)
def test_file_operations_reject_parent_traversal(
    file_handler, tmp_path, operation, outside_name, contents
):
    """Block reads and writes that escape the configured base directory."""
    outside_file = tmp_path.parent / outside_name
    outside_file.write_text(contents, encoding="utf-8")

    with pytest.raises(ValueError, match="outside the base path"):
        method = getattr(file_handler, operation)
        if operation == "write_report_json":
            method(f"../{outside_name}", {"status": "unsafe"})
        else:
            method(f"../{outside_name}")

    assert outside_file.read_text(encoding="utf-8") == contents


@pytest.mark.security
@pytest.mark.parametrize(
    "operation, outside_name, contents",
    [
        ("read_transactions_csv", "absolute.csv", "date,merchant,category,amount,type\n"),
        ("read_transactions_json", "absolute.json", "[]"),
        ("write_report_json", "absolute.json", "do not overwrite"),
    ],
)
def test_file_operations_reject_absolute_paths(
    file_handler, tmp_path, operation, outside_name, contents
):
    """Block absolute paths even when they point to accessible files."""
    outside_file = tmp_path.parent / outside_name
    outside_file.write_text(contents, encoding="utf-8")

    with pytest.raises(ValueError, match="Absolute paths are not allowed"):
        method = getattr(file_handler, operation)
        if operation == "write_report_json":
            method(str(outside_file), {"status": "unsafe"})
        else:
            method(str(outside_file))

    assert outside_file.read_text(encoding="utf-8") == contents