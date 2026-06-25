"""Tests for the DataTable component and its pure helper functions."""

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


@dataclass
class Person:
    """Simple object used to exercise attribute-based access."""

    name: str
    age: int


@pytest.fixture
def columns():
    """Column definitions covering a sortable and a non-sortable column."""
    return [
        ColumnDefinition(key="name", label="Name"),
        ColumnDefinition(key="age", label="Age"),
        ColumnDefinition(key="city", label="City", sortable=False),
    ]


@pytest.fixture
def people():
    """A small dataset of dictionaries."""
    return [
        {"name": "Alice", "age": 30, "city": "Paris"},
        {"name": "Bob", "age": 25, "city": "London"},
        {"name": "Charlie", "age": 35, "city": "Paris"},
    ]


# --- Construction ------------------------------------------------------------------


def test_init_rejects_invalid_rows_per_page(columns):
    """rows_per_page below 1 raises ValueError."""
    with pytest.raises(ValueError):
        DataTable([], columns, rows_per_page=0)


def test_get_columns_returns_definitions(columns, people):
    """get_columns returns the original column definitions."""
    table = DataTable(people, columns)
    assert table.get_columns() == columns


# --- Value extraction --------------------------------------------------------------


def test_get_value_supports_objects(columns):
    """_get_value reads attributes from non-dict items."""
    table = DataTable([Person("Dana", 40)], columns)
    assert table._get_value(Person("Dana", 40), "name") == "Dana"
    assert table._get_value(Person("Dana", 40), "missing") is None


# --- Search ------------------------------------------------------------------------


def test_search_filters_case_insensitively(columns, people):
    """Search matches partial, case-insensitive strings across columns."""
    table = DataTable(people, columns)
    table.search("PAR")
    assert table.get_total_rows() == 2
    assert table.get_search_query() == "par"


def test_search_empty_query_restores_all(columns, people):
    """An empty query resets the filtered data to the full set."""
    table = DataTable(people, columns)
    table.search("alice")
    table.search("")
    assert table.get_total_rows() == 3


# --- Sorting -----------------------------------------------------------------------


def test_sort_ascending_and_descending(columns, people):
    """Sorting reorders rows and records the sort state."""
    table = DataTable(people, columns)
    table.sort("age", ascending=True)
    assert [row["age"] for row in table.get_current_page()] == [25, 30, 35]
    assert table.get_sort_state() == {"column": "age", "ascending": True}

    table.sort("age", ascending=False)
    assert [row["age"] for row in table.get_current_page()] == [35, 30, 25]


def test_sort_unknown_column_raises(columns, people):
    """Sorting by an unknown column raises ValueError."""
    table = DataTable(people, columns)
    with pytest.raises(ValueError):
        table.sort("unknown")


def test_sort_non_sortable_column_raises(columns, people):
    """Sorting by a non-sortable column raises ValueError."""
    table = DataTable(people, columns)
    with pytest.raises(ValueError):
        table.sort("city")


# --- Pagination --------------------------------------------------------------------


def test_pagination_pages_and_bounds(columns, people):
    """Pages slice the data and reject out-of-range page numbers."""
    table = DataTable(people, columns, rows_per_page=2)
    assert table.get_total_pages() == 2
    assert table.get_current_page() == people[:2]

    table.set_page(2)
    assert table.get_current_page() == people[2:]

    with pytest.raises(ValueError):
        table.set_page(3)
    with pytest.raises(ValueError):
        table.set_page(0)


def test_empty_table_reports_single_page(columns):
    """An empty table has one page and is flagged empty."""
    table = DataTable([], columns)
    assert table.is_empty() is True
    assert table.get_total_pages() == 1
    assert table.get_total_rows() == 0


def test_get_page_info_for_populated_table(columns, people):
    """Page info exposes navigation flags and row numbers."""
    table = DataTable(people, columns, rows_per_page=2)
    info = table.get_page_info()
    assert info["current_page"] == 1
    assert info["total_pages"] == 2
    assert info["total_rows"] == 3
    assert info["start_row"] == 1
    assert info["end_row"] == 2
    assert info["has_prev"] is False
    assert info["has_next"] is True


def test_get_page_info_for_empty_table(columns):
    """Empty tables report zeroed row numbers."""
    table = DataTable([], columns)
    info = table.get_page_info()
    assert info["start_row"] == 0
    assert info["end_row"] == 0
    assert info["has_next"] is False


# --- Formatting --------------------------------------------------------------------


def test_format_cell_uses_formatter_and_handles_none():
    """format_cell applies the formatter when present, else stringifies."""
    cols = [
        ColumnDefinition(key="amount", label="Amount", formatter=lambda v: f"${v:.2f}"),
        ColumnDefinition(key="note", label="Note"),
    ]
    table = DataTable([{"amount": 5, "note": None}], cols)
    item = {"amount": 5, "note": None}
    assert table.format_cell(item, cols[0]) == "$5.00"
    assert table.format_cell(item, cols[1]) == ""


# --- Reset -------------------------------------------------------------------------


def test_reset_clears_search_and_sort(columns, people):
    """reset returns the table to its initial state."""
    table = DataTable(people, columns, rows_per_page=2)
    table.search("paris")
    table.sort("age")
    table.set_page(1)
    table.reset()

    assert table.get_search_query() == ""
    assert table.get_sort_state() == {"column": None, "ascending": True}
    assert table.get_total_rows() == 3


# --- Pure helpers ------------------------------------------------------------------


def test_apply_search_pure(columns, people):
    """apply_search filters without mutating the input and returns all on empty."""
    matched = apply_search(people, columns, "london")
    assert matched == [people[1]]
    assert apply_search(people, columns, "  ") == people


def test_sort_data_pure(columns, people):
    """sort_data returns a new sorted list."""
    result = sort_data(people, "name", ascending=False)
    assert [row["name"] for row in result] == ["Charlie", "Bob", "Alice"]


def test_get_paginated_data_and_errors():
    """get_paginated_data slices pages and validates arguments."""
    data = [1, 2, 3, 4, 5]
    assert get_paginated_data(data, page=1, rows_per_page=2) == [1, 2]
    assert get_paginated_data(data, page=3, rows_per_page=2) == [5]
    with pytest.raises(ValueError):
        get_paginated_data(data, page=0, rows_per_page=2)
    with pytest.raises(ValueError):
        get_paginated_data(data, page=1, rows_per_page=0)


def test_process_table_data_full_pipeline(columns, people):
    """process_table_data applies search, sort, and pagination together."""
    result = process_table_data(
        people,
        columns,
        search_query="paris",
        sort_column="age",
        sort_ascending=True,
        page=1,
        rows_per_page=1,
    )
    assert result["total_rows"] == 2
    assert result["total_pages"] == 2
    assert result["rows"] == [{"name": "Alice", "age": 30, "city": "Paris"}]
    assert result["has_next"] is True
    assert result["start_row"] == 1
    assert result["end_row"] == 1


def test_process_table_data_clamps_page_and_handles_empty(columns, people):
    """Out-of-range pages are clamped and empty results report sane metadata."""
    clamped = process_table_data(people, columns, page=99, rows_per_page=2)
    assert clamped["current_page"] == clamped["total_pages"]

    empty = process_table_data([], columns, page=1, rows_per_page=10)
    assert empty["total_rows"] == 0
    assert empty["total_pages"] == 1
    assert empty["start_row"] == 0
    assert empty["end_row"] == 0


def test_process_table_data_supports_objects(columns):
    """The pure pipeline also works with attribute-based objects."""
    data = [Person("Alice", 30), Person("Bob", 25)]
    result = process_table_data(data, columns, sort_column="age")
    assert result["rows"][0].name == "Bob"
