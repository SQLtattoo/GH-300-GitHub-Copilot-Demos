import json

import pytest

from file_handler import BudgetFileHandler, FileHandler


def test_file_handler_reads_csv_json_and_writes_report(tmp_path) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    csv_path = data_dir / "transactions.csv"
    csv_path.write_text(
        "date,merchant,category,amount,type\n"
        "2026-06-01,Store,Groceries,10.5,expense\n",
        encoding="utf-8",
    )

    json_path = data_dir / "transactions.json"
    json_payload = [
        {
            "date": "2026-06-02",
            "merchant": "Cafe",
            "category": "Dining",
            "amount": 20.0,
            "type": "expense",
        }
    ]
    json_path.write_text(json.dumps(json_payload), encoding="utf-8")

    handler = BudgetFileHandler(str(data_dir))
    csv_rows = handler.read_transactions_csv("transactions.csv")
    json_rows = handler.read_transactions_json("transactions.json")

    assert csv_rows[0]["amount"] == 10.5
    assert json_rows == json_payload

    report = {"total": 30.5}
    handler.write_report_json("report.json", report)
    assert json.loads((data_dir / "report.json").read_text(encoding="utf-8")) == report

    processed_files = handler.get_processed_files()
    assert processed_files == ["transactions.csv", "transactions.json", "report.json"]


def test_file_handler_blocks_absolute_and_traversal_paths(tmp_path) -> None:
    handler = BudgetFileHandler(str(tmp_path))

    with pytest.raises(ValueError):
        handler.read_transactions_json("../outside.json")

    with pytest.raises(ValueError):
        handler.read_transactions_json("C:/outside.json")


def test_file_handler_alias_points_to_budget_file_handler() -> None:
    handler = FileHandler(".")
    assert isinstance(handler, BudgetFileHandler)
