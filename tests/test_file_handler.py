"""Tests for the BudgetFileHandler module."""

import json

import pytest

from file_handler import BudgetFileHandler, FileHandler


def test_read_transactions_csv_from_data_dir():
    handler = BudgetFileHandler("data")
    transactions = handler.read_transactions_csv("sample_transactions.csv")

    assert len(transactions) > 0
    assert set(transactions[0].keys()) == {"date", "merchant", "category", "amount", "type"}
    assert isinstance(transactions[0]["amount"], float)
    assert handler.get_processed_files() == ["sample_transactions.csv"]


def test_read_transactions_json(tmp_path):
    records = [{"date": "2024-01-01", "merchant": "A", "amount": 1.0}]
    (tmp_path / "txns.json").write_text(json.dumps(records), encoding="utf-8")

    handler = BudgetFileHandler(str(tmp_path))
    assert handler.read_transactions_json("txns.json") == records
    assert handler.get_processed_files() == ["txns.json"]


def test_init_stores_absolute_base_path(tmp_path):
    handler = BudgetFileHandler(str(tmp_path))
    assert handler.base_path == str(tmp_path.resolve())


def test_write_report_json_round_trip(tmp_path):
    handler = BudgetFileHandler(str(tmp_path))
    report = {"income": 100.0, "expenses": 40.0}

    handler.write_report_json("report.json", report)

    written = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    assert written == report
    assert "report.json" in handler.get_processed_files()


def test_resolve_safe_path_rejects_absolute(tmp_path):
    handler = BudgetFileHandler(str(tmp_path))
    with pytest.raises(ValueError, match="relative"):
        handler.read_transactions_json("C:/Windows/system.ini")


def test_resolve_safe_path_rejects_traversal(tmp_path):
    handler = BudgetFileHandler(str(tmp_path))
    with pytest.raises(ValueError, match="outside"):
        handler.read_transactions_json("../secret.json")


def test_resolve_safe_path_allows_nested_relative_path(tmp_path):
    nested = tmp_path / "nested"
    nested.mkdir()
    payload = [{"date": "2024-02-01", "merchant": "Nested", "amount": 7.5}]
    (nested / "records.json").write_text(json.dumps(payload), encoding="utf-8")

    handler = BudgetFileHandler(str(tmp_path))
    assert handler.read_transactions_json("nested/records.json") == payload


def test_read_transactions_csv_raises_on_invalid_amount(tmp_path):
    csv_data = (
        "date,merchant,category,amount,type\n"
        "2024-01-01,Store,Food,invalid,debit\n"
    )
    (tmp_path / "bad.csv").write_text(csv_data, encoding="utf-8")

    handler = BudgetFileHandler(str(tmp_path))
    with pytest.raises(ValueError):
        handler.read_transactions_csv("bad.csv")

    # Failed reads should not be tracked as processed.
    assert handler.get_processed_files() == []


def test_get_processed_files_returns_copy(tmp_path):
    handler = BudgetFileHandler(str(tmp_path))
    files = handler.get_processed_files()
    files.append("tampered")
    assert handler.get_processed_files() == []


def test_backward_compatible_alias():
    assert FileHandler is BudgetFileHandler
