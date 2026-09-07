"""
File loading helpers for the Budget Buddy demo app.

This module provides file handling constrained to a configured base directory.
"""

import csv
import json
import math
from pathlib import Path
from typing import Dict, List


Transaction = Dict[str, object]
CSV_FIELDS = ["date", "merchant", "category", "amount", "type"]


class BudgetFileHandler:
    """Read and write budget tracker data files."""

    def __init__(self, base_path: str = ".") -> None:
        """Initialize the handler with a base path."""
        self.base_path = base_path
        self.files_processed: List[str] = []

    def _resolve_safe_path(self, filename: str) -> Path:
        """Resolve a relative filename contained by the configured base path."""
        requested_path = Path(filename)
        if requested_path.is_absolute() or requested_path.drive:
            raise ValueError("Absolute paths are not allowed")

        base_path = Path(self.base_path).resolve()
        resolved_path = (base_path / requested_path).resolve()
        try:
            resolved_path.relative_to(base_path)
        except ValueError as error:
            raise ValueError("Path resolves outside the base path") from error
        return resolved_path

    def read_transactions_csv(self, filename: str) -> List[Transaction]:
        """Read transactions from a CSV file."""
        filepath = self._resolve_safe_path(filename)
        transactions: List[Transaction] = []

        with open(filepath, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file, strict=True)
            missing_columns = [field for field in CSV_FIELDS if field not in (reader.fieldnames or [])]
            if missing_columns:
                raise ValueError(f"CSV is missing required columns: {', '.join(missing_columns)}")

            try:
                for row_number, row in enumerate(reader, start=2):
                    if None in row:
                        raise ValueError(f"Malformed CSV row {row_number}: unexpected extra values")
                    transactions.append(self._validate_transaction(row, f"CSV row {row_number}"))
            except csv.Error as error:
                raise ValueError(f"Malformed CSV: {error}") from error

        self.files_processed.append(filename)
        return transactions

    def read_transactions_json(self, filename: str) -> List[Transaction]:
        """Read transactions from a JSON file."""
        filepath = self._resolve_safe_path(filename)
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError("JSON transaction data must be a list")

        transactions = []
        for index, item in enumerate(data, start=1):
            if not isinstance(item, dict):
                raise ValueError(f"JSON transaction {index} must be an object")
            transactions.append(self._validate_transaction(item, f"JSON transaction {index}"))
        self.files_processed.append(filename)
        return transactions

    def write_report_json(self, filename: str, report: Dict[str, object]) -> None:
        """Write a summary report as JSON."""
        filepath = self._resolve_safe_path(filename)
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=2)
        self.files_processed.append(filename)

    def get_processed_files(self) -> List[str]:
        """Return processed files."""
        return self.files_processed.copy()

    def write_transactions_csv(self, filename: str, transactions: List[Transaction]) -> None:
        """Write transactions using the CSV format accepted by the reader."""
        validated = [
            self._validate_transaction(transaction, f"Transaction {index}")
            for index, transaction in enumerate(transactions, start=1)
        ]
        filepath = self._resolve_safe_path(filename)
        with open(filepath, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerows(validated)
        self.files_processed.append(filename)

    @staticmethod
    def _validate_transaction(transaction: Transaction, context: str) -> Transaction:
        """Validate and normalize a transaction loaded from a file."""
        missing_fields = [
            field
            for field in CSV_FIELDS
            if field not in transaction or transaction[field] is None or not str(transaction[field]).strip()
        ]
        if missing_fields:
            raise ValueError(f"{context} has missing fields: {', '.join(missing_fields)}")

        raw_amount = transaction["amount"]
        if isinstance(raw_amount, bool):
            raise ValueError(f"{context} has an invalid amount: {raw_amount}")
        try:
            amount = float(raw_amount)
        except (TypeError, ValueError) as error:
            raise ValueError(f"{context} has an invalid amount: {raw_amount}") from error
        if not math.isfinite(amount) or amount < 0:
            raise ValueError(f"{context} has an invalid amount: {raw_amount}")

        transaction_type = str(transaction["type"]).strip()
        if transaction_type not in {"income", "expense"}:
            raise ValueError(f"{context} has an invalid type: {transaction_type}")

        return {
            "date": str(transaction["date"]).strip(),
            "merchant": str(transaction["merchant"]).strip(),
            "category": str(transaction["category"]).strip(),
            "amount": amount,
            "type": transaction_type,
        }


# Backward-compatible alias used by older demo prompts.
FileHandler = BudgetFileHandler