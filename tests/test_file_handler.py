"""Starter tests for BudgetFileHandler."""

import json

import pytest

import file_handler as file_handler_module


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


class TestJsonOperations:
    def test_reads_json_and_tracks_file(self, file_handler, tmp_path):
        transactions = [{"merchant": "Cafe", "amount": 12.5, "type": "expense"}]
        (tmp_path / "transactions.json").write_text(json.dumps(transactions), encoding="utf-8")

        assert file_handler.read_transactions_json("transactions.json") == transactions
        assert file_handler.get_processed_files() == ["transactions.json"]

    def test_writes_indented_report_and_tracks_file(self, file_handler, tmp_path):
        report = {"income": 1000.0, "categories": {"Food": 25.0}}

        file_handler.write_report_json("report.json", report)

        report_path = tmp_path / "report.json"
        assert json.loads(report_path.read_text(encoding="utf-8")) == report
        assert "\n  \"income\"" in report_path.read_text(encoding="utf-8")
        assert file_handler.get_processed_files() == ["report.json"]

    def test_invalid_json_propagates_error_without_tracking_file(self, file_handler, tmp_path):
        (tmp_path / "invalid.json").write_text("{invalid", encoding="utf-8")

        with pytest.raises(json.JSONDecodeError):
            file_handler.read_transactions_json("invalid.json")

        assert file_handler.get_processed_files() == []


class TestFileErrorsAndHistory:
    def test_missing_file_propagates_file_not_found(self, file_handler):
        with pytest.raises(FileNotFoundError):
            file_handler.read_transactions_csv("missing.csv")

        assert file_handler.get_processed_files() == []

    def test_non_numeric_csv_amount_raises_value_error(self, file_handler, tmp_path):
        (tmp_path / "invalid.csv").write_text(
            "date,merchant,category,amount,type\n"
            "2026-06-01,Cafe,Food,not-a-number,expense\n",
            encoding="utf-8",
        )

        with pytest.raises(ValueError):
            file_handler.read_transactions_csv("invalid.csv")

        assert file_handler.get_processed_files() == []

    def test_processed_files_returns_defensive_copy(self, file_handler, tmp_path):
        (tmp_path / "transactions.json").write_text("[]", encoding="utf-8")
        file_handler.read_transactions_json("transactions.json")

        processed = file_handler.get_processed_files()
        processed.append("external.json")

        assert file_handler.get_processed_files() == ["transactions.json"]

    def test_commonpath_value_error_is_treated_as_unsafe(self, file_handler, monkeypatch):
        def raise_cross_volume_error(paths):
            raise ValueError("Paths are on different drives")

        monkeypatch.setattr(file_handler_module.os.path, "commonpath", raise_cross_volume_error)

        with pytest.raises(ValueError, match="outside the base path"):
            file_handler._resolve_safe_path("transactions.csv")