"""Tests for the framework-agnostic data table helpers."""

from dataclasses import dataclass

import pytest

from data_table import (
    ColumnDefinition,
    DataTable,
    apply_search,
    get_paginated_data,
    process_table_data,
    sort_data,
)


@pytest.fixture
def columns():
    """Return representative table columns."""
    return [
        ColumnDefinition("name", "Name"),
        ColumnDefinition("amount", "Amount"),
        ColumnDefinition("secret", "Secret", sortable=False),
    ]


@pytest.fixture
def rows():
    """Return rows containing zero and missing sort values."""
    return [
        {"name": "Charlie", "amount": 10, "secret": "c"},
        {"name": "alice", "amount": 0, "secret": "a"},
        {"name": "Bob", "amount": None, "secret": "b"},
    ]


def test_data_table_rejects_invalid_page_size(columns):
    """Require at least one row per page."""
    with pytest.raises(ValueError, match="at least 1"):
        DataTable([], columns, rows_per_page=0)


def test_search_matches_case_insensitively_and_resets_page(columns, rows):
    """Search all columns and reset pagination to the first page."""
    table = DataTable(rows, columns, rows_per_page=1)
    table.set_page(2)

    table.search(" ALI ")

    assert table.get_current_page() == [rows[1]]
    assert table.get_search_query() == "ali"
    assert table.get_page_info()["current_page"] == 1


def test_empty_search_restores_original_rows(columns, rows):
    """Clearing search restores all rows."""
    table = DataTable(rows, columns)
    table.search("alice")

    table.search("  ")

    assert table.get_total_rows() == 3


def test_search_preserves_active_sort(columns, rows):
    """Keep filtered results in the selected sort order."""
    table = DataTable(rows, columns)
    table.sort("name", ascending=False)

    table.search("a")

    assert [row["name"] for row in table.get_current_page()] == ["Charlie", "alice"]


def test_sort_handles_zero_and_missing_values(columns, rows):
    """Sort zero numerically and leave missing values at the end."""
    table = DataTable(rows, columns)

    table.sort("amount")
    assert [row["amount"] for row in table.get_current_page()] == [0, 10, None]

    table.sort("amount", ascending=False)
    assert [row["amount"] for row in table.get_current_page()] == [10, 0, None]
    assert table.get_sort_state() == {"column": "amount", "ascending": False}


def test_sort_rejects_unknown_and_disabled_columns(columns, rows):
    """Reject missing columns and columns marked as not sortable."""
    table = DataTable(rows, columns)

    with pytest.raises(ValueError, match="not found"):
        table.sort("missing")
    with pytest.raises(ValueError, match="not sortable"):
        table.sort("secret")


def test_pagination_and_page_info(columns, rows):
    """Return correct page slices and navigation metadata."""
    table = DataTable(rows, columns, rows_per_page=2)
    table.set_page(2)

    assert table.get_current_page() == [rows[2]]
    assert table.get_page_info() == {
        "current_page": 2,
        "total_pages": 2,
        "total_rows": 3,
        "start_row": 3,
        "end_row": 3,
        "has_prev": True,
        "has_next": False,
    }


@pytest.mark.parametrize("page", [0, 3])
def test_set_page_rejects_out_of_range_values(columns, rows, page):
    """Reject pages outside the current result set."""
    table = DataTable(rows, columns, rows_per_page=2)

    with pytest.raises(ValueError, match="between 1 and 2"):
        table.set_page(page)


def test_empty_table_state(columns):
    """Represent empty tables as one empty page with zero row positions."""
    table = DataTable([], columns)

    assert table.is_empty() is True
    assert table.get_total_pages() == 1
    assert table.get_page_info() == {
        "current_page": 1,
        "total_pages": 1,
        "total_rows": 0,
        "start_row": 0,
        "end_row": 0,
        "has_prev": False,
        "has_next": False,
    }


def test_format_cell_supports_formatters_objects_and_missing_values(columns):
    """Format dictionary or object values and render missing values as empty."""
    amount = ColumnDefinition("amount", "Amount", formatter=lambda value: f"${value:.2f}")

    assert DataTable([], columns).format_cell({"amount": 12.5}, amount) == "$12.50"
    assert DataTable([], columns).format_cell(Record("Alice", 12), columns[0]) == "Alice"
    assert DataTable([], columns).format_cell({}, columns[0]) == ""


def test_columns_and_input_data_are_defensively_copied(columns, rows):
    """Keep external list mutation from changing table configuration or data."""
    table = DataTable(rows, columns)
    rows.append({"name": "Later", "amount": 20})
    returned_columns = table.get_columns()
    returned_columns.clear()

    assert table.get_total_rows() == 3
    assert len(table.get_columns()) == 3


def test_reset_clears_search_sort_and_page(columns, rows):
    """Restore the table's initial rows and interaction state."""
    table = DataTable(rows, columns, rows_per_page=1)
    table.sort("name")
    table.search("alice")
    table.reset()

    assert table.get_current_page() == [rows[0]]
    assert table.get_search_query() == ""
    assert table.get_sort_state() == {"column": None, "ascending": True}


@dataclass
class Record:
    """Simple object row used to verify attribute access."""

    name: str
    amount: int


def test_apply_search_supports_objects_and_blank_queries():
    """Search object attributes and return a new list for blank searches."""
    data = [Record("Alice", 10), Record("Bob", 20)]

    assert apply_search(data, [ColumnDefinition("name", "Name")], "LIC") == [data[0]]
    assert apply_search(data, [], "") == data
    assert apply_search(data, [], "") is not data


def test_sort_data_orders_numbers_text_and_missing_values():
    """Provide stable ordering across supported value types."""
    numeric = [{"value": 10}, {"value": 2}, {"value": None}]
    text = [Record("charlie", 1), Record("Alice", 2)]

    assert [item["value"] for item in sort_data(numeric, "value")] == [2, 10, None]
    assert [item.name for item in sort_data(text, "name", ascending=False)] == [
        "charlie",
        "Alice",
    ]


def test_get_paginated_data_validates_and_slices():
    """Validate helper arguments and return the requested page."""
    assert get_paginated_data([1, 2, 3], page=2, rows_per_page=2) == [3]
    with pytest.raises(ValueError, match="Page must be at least 1"):
        get_paginated_data([], page=0, rows_per_page=1)
    with pytest.raises(ValueError, match="rows_per_page must be at least 1"):
        get_paginated_data([], page=1, rows_per_page=0)


def test_process_table_data_combines_search_sort_and_pagination(columns, rows):
    """Apply all table transformations and return complete metadata."""
    result = process_table_data(
        rows,
        columns,
        search_query="a",
        sort_column="name",
        sort_ascending=False,
        page=2,
        rows_per_page=1,
    )

    assert result == {
        "rows": [rows[1]],
        "total_rows": 2,
        "total_pages": 2,
        "current_page": 2,
        "has_prev": True,
        "has_next": False,
        "start_row": 2,
        "end_row": 2,
    }


@pytest.mark.parametrize(("requested", "expected"), [(0, 1), (99, 2)])
def test_process_table_data_clamps_page(columns, rows, requested, expected):
    """Clamp requested pages to the available range."""
    result = process_table_data(rows, columns, page=requested, rows_per_page=2)

    assert result["current_page"] == expected


def test_process_table_data_handles_empty_rows(columns):
    """Return coherent metadata for an empty result set."""
    result = process_table_data([], columns)

    assert result["rows"] == []
    assert result["total_pages"] == 1
    assert result["start_row"] == 0


def test_process_table_data_validates_page_size_and_sort_column(columns, rows):
    """Reject invalid page sizes and sort definitions before processing."""
    with pytest.raises(ValueError, match="rows_per_page"):
        process_table_data(rows, columns, rows_per_page=0)
    with pytest.raises(ValueError, match="not found"):
        process_table_data(rows, columns, sort_column="missing")
    with pytest.raises(ValueError, match="not sortable"):
        process_table_data(rows, columns, sort_column="secret")