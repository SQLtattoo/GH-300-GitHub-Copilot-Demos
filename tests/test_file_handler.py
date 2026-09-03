import json

import pytest

from file_handler import BudgetFileHandler, FileHandler


pytestmark = pytest.mark.unit


def test_reads_csv_and_converts_amounts(tmp_path):
    csv_path = tmp_path / "transactions.csv"
    csv_path.write_text(
        "date,merchant,category,amount,type\n"
        "2026-06-01,Cafe,Dining,12.50,expense\n",
        encoding="utf-8",
    )
    handler = BudgetFileHandler(str(tmp_path))

    assert handler.read_transactions_csv("transactions.csv") == [
        {
            "date": "2026-06-01",
            "merchant": "Cafe",
            "category": "Dining",
            "amount": 12.5,
            "type": "expense",
        }
    ]
    assert handler.get_processed_files() == ["transactions.csv"]


def test_writes_transactions_csv_with_reader_compatible_headers(tmp_path):
    transactions = [
        {
            "date": "2026-06-01",
            "merchant": "Cafe, Corner",
            "category": "Dining",
            "amount": 12.5,
            "type": "expense",
        }
    ]
    handler = BudgetFileHandler(str(tmp_path))

    handler.write_transactions_csv("export.csv", transactions)

    assert handler.read_transactions_csv("export.csv") == transactions
    assert (tmp_path / "export.csv").read_text(encoding="utf-8").splitlines()[0] == (
        "date,merchant,category,amount,type"
    )
    assert handler.get_processed_files() == ["export.csv", "export.csv"]


@pytest.mark.parametrize(
    "contents",
    [
        "date,merchant,category,amount,type\n2026-06-01,Cafe,Dining,nope,expense\n",
        "date,merchant,category,amount\n2026-06-01,Cafe,Dining,10\n",
    ],
)
def test_rejects_malformed_csv_without_marking_it_processed(tmp_path, contents):
    (tmp_path / "bad.csv").write_text(contents, encoding="utf-8")
    handler = BudgetFileHandler(str(tmp_path))

    with pytest.raises((ValueError, KeyError)):
        handler.read_transactions_csv("bad.csv")

    assert handler.get_processed_files() == []


def test_reads_and_writes_json_and_tracks_successful_operations(tmp_path):
    transactions = [{"amount": 9.5, "type": "expense"}]
    (tmp_path / "input.json").write_text(json.dumps(transactions), encoding="utf-8")
    handler = BudgetFileHandler(str(tmp_path))

    assert handler.read_transactions_json("input.json") == transactions
    handler.write_report_json("report.json", {"total": 9.5})

    assert json.loads((tmp_path / "report.json").read_text(encoding="utf-8")) == {"total": 9.5}
    assert handler.get_processed_files() == ["input.json", "report.json"]


def test_invalid_json_and_missing_files_are_not_recorded(tmp_path):
    (tmp_path / "bad.json").write_text("not json", encoding="utf-8")
    handler = BudgetFileHandler(str(tmp_path))

    with pytest.raises(json.JSONDecodeError):
        handler.read_transactions_json("bad.json")
    with pytest.raises(FileNotFoundError):
        handler.read_transactions_csv("missing.csv")

    assert handler.get_processed_files() == []


def test_rejects_paths_outside_base_without_overwriting_files(tmp_path):
    base_path = tmp_path / "data"
    base_path.mkdir()
    outside_path = tmp_path / "outside.json"
    outside_path.write_text('{"secret": true}', encoding="utf-8")
    handler = BudgetFileHandler(str(base_path))

    with pytest.raises(ValueError):
        handler.read_transactions_json("../outside.json")
    with pytest.raises(ValueError):
        handler.write_report_json("../outside.json", {"overwritten": True})
    with pytest.raises(ValueError):
        handler.read_transactions_json(str(outside_path))

    assert outside_path.read_text(encoding="utf-8") == '{"secret": true}'
    assert handler.get_processed_files() == []


def test_processed_files_returns_a_copy(tmp_path):
    handler = BudgetFileHandler(str(tmp_path))
    handler.write_report_json("report.json", {})

    files = handler.get_processed_files()
    files.append("fake.json")

    assert handler.get_processed_files() == ["report.json"]


def test_legacy_alias_is_preserved():
    assert FileHandler is BudgetFileHandler