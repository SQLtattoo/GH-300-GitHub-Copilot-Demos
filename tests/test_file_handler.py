"""Starter tests for BudgetFileHandler."""


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


def test_read_transactions_json(file_handler, tmp_path):
    """Read transactions back from a JSON file and track the read."""
    json_file = tmp_path / "transactions.json"
    json_file.write_text(
        '[{"date": "2026-06-02", "merchant": "Grocery", "category": "Groceries", '
        '"amount": 120.0, "type": "expense"}]',
        encoding="utf-8",
    )

    transactions = file_handler.read_transactions_json("transactions.json")

    assert transactions[0]["amount"] == 120.0
    assert file_handler.get_processed_files() == ["transactions.json"]


def test_write_report_json_roundtrip(file_handler, tmp_path):
    """Writing a report produces JSON that can be read back unchanged."""
    import json

    report = {"income": 5000.0, "expenses": 160.0, "remaining_budget": 840.0}
    file_handler.write_report_json("report.json", report)

    written = tmp_path / "report.json"
    assert written.exists()
    assert json.loads(written.read_text(encoding="utf-8")) == report
    assert file_handler.get_processed_files() == ["report.json"]


def test_write_transactions_csv_roundtrip(file_handler, sample_transactions):
    """Exported transactions can be read back unchanged."""
    file_handler.write_transactions_csv("export.csv", sample_transactions)

    read_back = file_handler.read_transactions_csv("export.csv")

    assert read_back == sample_transactions
    assert file_handler.get_processed_files() == ["export.csv", "export.csv"]


def test_write_transactions_csv_headers(file_handler, tmp_path, sample_transactions):
    """Exported CSV uses the headers consumed by read_transactions_csv."""
    file_handler.write_transactions_csv("export.csv", sample_transactions)

    written = tmp_path / "export.csv"
    first_line = written.read_text(encoding="utf-8").splitlines()[0]
    assert first_line == "date,merchant,category,amount,type"


def test_write_transactions_csv_empty(file_handler, tmp_path):
    """Exporting an empty list writes only the header row."""
    file_handler.write_transactions_csv("export.csv", [])

    written = tmp_path / "export.csv"
    assert written.read_text(encoding="utf-8").splitlines() == [
        "date,merchant,category,amount,type"
    ]
    assert file_handler.read_transactions_csv("export.csv") == []