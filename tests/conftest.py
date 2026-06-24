"""Starter pytest fixtures for the Budget Buddy demo app."""

import sys
from pathlib import Path

import pytest


sys.path.insert(0, str(Path(__file__).parent.parent))

from calculator import BudgetCalculator
from data_processor import TransactionProcessor
from file_handler import BudgetFileHandler


@pytest.fixture
def sample_transactions():
    """Return a small happy-path transaction set."""
    return [
        {"date": "2026-06-01", "merchant": "Payroll", "category": "Income", "amount": 5000.0, "type": "income"},
        {"date": "2026-06-02", "merchant": "Grocery", "category": "Groceries", "amount": 120.0, "type": "expense"},
        {"date": "2026-06-03", "merchant": "Transit", "category": "Transport", "amount": 40.0, "type": "expense"},
    ]


@pytest.fixture
def calculator():
    """Return a fresh calculator."""
    return BudgetCalculator()


@pytest.fixture
def processor():
    """Return a fresh transaction processor."""
    return TransactionProcessor()


@pytest.fixture
def file_handler(tmp_path):
    """Return a file handler rooted at a temporary path."""
    return BudgetFileHandler(str(tmp_path))