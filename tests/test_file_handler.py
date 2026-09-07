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


def test_write_transactions_csv_round_trips(file_handler, sample_transactions):
    """Write transactions with headers that the CSV reader accepts."""
    file_handler.write_transactions_csv("round-trip.csv", sample_transactions)

    assert file_handler.read_transactions_csv("round-trip.csv") == sample_transactions
    assert file_handler.get_processed_files() == ["round-trip.csv", "round-trip.csv"]


@pytest.mark.parametrize(
    ("contents", "message"),
    [
        ("date,merchant,amount,type\n", "missing required columns: category"),
        (
            "date,merchant,category,amount,type\n2026-06-01,Cafe,Food,10,expense,extra\n",
            "unexpected extra values",
        ),
        (
            "date,merchant,category,amount,type\n2026-06-01,Cafe,Food,nope,expense\n",
            "CSV row 2 has an invalid amount",
        ),
        (
            "date,merchant,category,amount,type\n2026-06-01,Cafe,,10,expense\n",
            "CSV row 2 has missing fields: category",
        ),
        (
            "date,merchant,category,amount,type\n2026-06-01,Cafe,Food,10,transfer\n",
            "CSV row 2 has an invalid type",
        ),
    ],
)
def test_read_transactions_csv_rejects_malformed_rows(file_handler, tmp_path, contents, message):
    """Raise contextual errors for malformed CSV input."""
    (tmp_path / "bad.csv").write_text(contents, encoding="utf-8")

    with pytest.raises(ValueError, match=message):
        file_handler.read_transactions_csv("bad.csv")

    assert file_handler.get_processed_files() == []


def test_read_transactions_json_validates_and_normalizes(file_handler, tmp_path):
    """Load a valid JSON transaction list and normalize numeric amounts."""
    payload = [
        {
            "date": "2026-06-01",
            "merchant": "Cafe",
            "category": "Food",
            "amount": "12.50",
            "type": "expense",
        }
    ]
    (tmp_path / "transactions.json").write_text(json.dumps(payload), encoding="utf-8")

    transactions = file_handler.read_transactions_json("transactions.json")

    assert transactions[0]["amount"] == 12.5
    assert file_handler.get_processed_files() == ["transactions.json"]


@pytest.mark.parametrize("payload", [{"amount": 10}, ["not an object"]])
def test_read_transactions_json_rejects_invalid_structure(file_handler, tmp_path, payload):
    """Reject JSON roots and entries that cannot represent transactions."""
    (tmp_path / "bad.json").write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="must be"):
        file_handler.read_transactions_json("bad.json")


def test_write_report_json_round_trips(file_handler, tmp_path):
    """Write JSON reports and track successful output files."""
    report = {"income": 100.0, "expenses": 25.0}

    file_handler.write_report_json("report.json", report)

    assert json.loads((tmp_path / "report.json").read_text(encoding="utf-8")) == report
    assert file_handler.get_processed_files() == ["report.json"]


@pytest.mark.parametrize("operation", ["read_csv", "read_json", "write_json", "write_csv"])
def test_file_operations_reject_paths_outside_base(file_handler, operation):
    """Apply base-path confinement consistently to every file operation."""
    with pytest.raises(ValueError, match="outside the base path"):
        if operation == "read_csv":
            file_handler.read_transactions_csv("../outside.csv")
        elif operation == "read_json":
            file_handler.read_transactions_json("../outside.json")
        elif operation == "write_json":
            file_handler.write_report_json("../outside.json", {})
        else:
            file_handler.write_transactions_csv("../outside.csv", [])


def test_file_operations_reject_absolute_paths(file_handler, tmp_path):
    """Reject absolute paths even when they point inside the base directory."""
    with pytest.raises(ValueError, match="Absolute paths are not allowed"):
        file_handler.read_transactions_csv(str(tmp_path / "transactions.csv"))


def test_get_processed_files_returns_a_copy(file_handler):
    """Prevent callers from changing internal processed-file history."""
    files = file_handler.get_processed_files()
    files.append("external.csv")

    assert file_handler.get_processed_files() == []


def test_read_transactions_csv_wraps_parser_errors(file_handler, tmp_path):
    """Translate low-level CSV parser failures into a clear value error."""
    (tmp_path / "bad.csv").write_text(
        "date,merchant,category,amount,type\n\"unterminated",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Malformed CSV"):
        file_handler.read_transactions_csv("bad.csv")


@pytest.mark.parametrize("amount", [True, -1, float("inf"), float("nan")])
def test_write_transactions_csv_rejects_invalid_amounts(file_handler, sample_transactions, amount):
    """Reject boolean, negative, and non-finite transaction amounts."""
    transaction = {**sample_transactions[0], "amount": amount}

    with pytest.raises(ValueError, match="invalid amount"):
        file_handler.write_transactions_csv("invalid.csv", [transaction])