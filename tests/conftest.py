"""
Pytest configuration and shared fixtures.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from calculator import Calculator
from data_processor import DataProcessor
from file_handler import FileHandler
from data_table import DataTable, ColumnDefinition


@pytest.fixture
def calculator():
    """Fixture providing a fresh Calculator instance for each test."""
    return Calculator()


@pytest.fixture
def data_processor():
    """Fixture providing a fresh DataProcessor instance for each test."""
    return DataProcessor()


@pytest.fixture
def file_handler(tmp_path):
    """Fixture providing a FileHandler instance with a temporary directory."""
    return FileHandler(str(tmp_path))


@pytest.fixture
def sample_employees():
    """Fixture providing sample employee data for DataTable tests."""
    return [
        {'name': 'Alice', 'department': 'Engineering', 'salary': 95000, 'age': 32},
        {'name': 'Bob', 'department': 'Marketing', 'salary': 75000, 'age': 28},
        {'name': 'Charlie', 'department': 'Engineering', 'salary': 105000, 'age': 35},
        {'name': 'Diana', 'department': 'Sales', 'salary': 85000, 'age': 30},
    ]


@pytest.fixture
def employee_columns():
    """Fixture providing column definitions for employee data."""
    return [
        ColumnDefinition(key='name', label='Name'),
        ColumnDefinition(key='department', label='Department'),
        ColumnDefinition(key='salary', label='Salary'),
        ColumnDefinition(key='age', label='Age'),
    ]
