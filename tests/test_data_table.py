"""Tests for the DataTable module and its pure helper functions."""

import pytest

from data_table import (
    ColumnDefinition,
    DataTable,
    apply_search,
    get_paginated_data,
    process_table_data,
    sort_data,
)


class Row:
    """Simple object to exercise attribute-based access."""

    def __init__(self, name, age):
        self.name = name
        self.age = age


@pytest.fixture
def columns():
    return [
        ColumnDefinition(key="name", label="Name"),
        ColumnDefinition(key="age", label="Age"),
    ]


@pytest.fixture
def people():
    return [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
        {"name": "Charlie", "age": 35},
    ]


def test_init_rejects_invalid_rows_per_page(columns):
    with pytest.raises(ValueError):
        DataTable([], columns, rows_per_page=0)


def test_get_value_dict_and_object(columns):
    table = DataTable([], columns)
    assert table._get_value({"name": "Alice"}, "name") == "Alice"
    assert table._get_value(Row("Bob", 25), "name") == "Bob"
    assert table._get_value({"name": "Alice"}, "missing") is None


def test_search_filters_and_resets_page(people, columns):
    table = DataTable(people, columns, rows_per_page=1)
    table.set_page(2)

    table.search("ali")
    assert table.get_total_rows() == 1
    assert table.get_current_page() == [{"name": "Alice", "age": 30}]
    assert table.get_search_query() == "ali"


def test_search_empty_query_restores_all(people, columns):
    table = DataTable(people, columns)
    table.search("ali")
    table.search("")
    assert table.get_total_rows() == 3


def test_sort_ascending_and_descending(people, columns):
    table = DataTable(people, columns)

    table.sort("age", ascending=True)
    assert [row["age"] for row in table.get_current_page()] == [25, 30, 35]

    table.sort("age", ascending=False)
    assert [row["age"] for row in table.get_current_page()] == [35, 30, 25]

    assert table.get_sort_state() == {"column": "age", "ascending": False}


def test_sort_unknown_column_raises(people, columns):
    table = DataTable(people, columns)
    with pytest.raises(ValueError, match="not found"):
        table.sort("unknown")


def test_sort_non_sortable_column_raises(people):
    columns = [ColumnDefinition(key="name", label="Name", sortable=False)]
    table = DataTable(people, columns)
    with pytest.raises(ValueError, match="not sortable"):
        table.sort("name")


def test_pagination(people, columns):
    table = DataTable(people, columns, rows_per_page=2)
    assert table.get_total_pages() == 2

    table.set_page(2)
    assert table.get_current_page() == [{"name": "Charlie", "age": 35}]


def test_set_page_invalid_raises(people, columns):
    table = DataTable(people, columns, rows_per_page=2)
    with pytest.raises(ValueError):
        table.set_page(99)


def test_total_pages_empty(columns):
    table = DataTable([], columns)
    assert table.get_total_pages() == 1
    assert table.is_empty() is True


def test_get_page_info(people, columns):
    table = DataTable(people, columns, rows_per_page=2)
    info = table.get_page_info()
    assert info["current_page"] == 1
    assert info["total_pages"] == 2
    assert info["total_rows"] == 3
    assert info["start_row"] == 1
    assert info["end_row"] == 2
    assert info["has_prev"] is False
    assert info["has_next"] is True


def test_get_page_info_empty(columns):
    table = DataTable([], columns)
    info = table.get_page_info()
    assert info["total_rows"] == 0
    assert info["start_row"] == 0


def test_format_cell_with_and_without_formatter():
    columns = [
        ColumnDefinition(key="amount", label="Amount", formatter=lambda v: f"${v:.2f}"),
        ColumnDefinition(key="name", label="Name"),
    ]
    table = DataTable([], columns)
    item = {"amount": 5, "name": None}

    assert table.format_cell(item, columns[0]) == "$5.00"
    assert table.format_cell(item, columns[1]) == ""


def test_get_columns(columns):
    table = DataTable([], columns)
    assert table.get_columns() == columns


def test_reset(people, columns):
    table = DataTable(people, columns)
    table.search("ali")
    table.sort("age")
    table.reset()

    assert table.get_total_rows() == 3
    assert table.get_search_query() == ""
    assert table.get_sort_state() == {"column": None, "ascending": True}


# --- Pure helper functions ---


def test_apply_search(people, columns):
    assert apply_search(people, columns, "bob") == [{"name": "Bob", "age": 25}]
    assert apply_search(people, columns, "") == people


def test_apply_search_object_rows(columns):
    rows = [Row("Alice", 30), Row("Bob", 25)]
    result = apply_search(rows, columns, "bob")
    assert result[0].name == "Bob"


def test_sort_data(people):
    result = sort_data(people, "age", ascending=True)
    assert [row["age"] for row in result] == [25, 30, 35]


def test_get_paginated_data():
    assert get_paginated_data([1, 2, 3, 4, 5], page=2, rows_per_page=2) == [3, 4]


def test_get_paginated_data_invalid():
    with pytest.raises(ValueError):
        get_paginated_data([1, 2], page=0, rows_per_page=2)
    with pytest.raises(ValueError):
        get_paginated_data([1, 2], page=1, rows_per_page=0)


def test_process_table_data(people, columns):
    result = process_table_data(
        people,
        columns,
        search_query="a",
        sort_column="age",
        sort_ascending=True,
        page=1,
        rows_per_page=10,
    )
    assert result["total_rows"] == 2
    assert result["current_page"] == 1
    assert [row["name"] for row in result["rows"]] == ["Alice", "Charlie"]


def test_process_table_data_page_clamped(people, columns):
    result = process_table_data(people, columns, page=99, rows_per_page=2)
    assert result["current_page"] == result["total_pages"]


def test_process_table_data_empty(columns):
    result = process_table_data([], columns)
    assert result["total_rows"] == 0
    assert result["total_pages"] == 1
    assert result["start_row"] == 0
    assert result["rows"] == []
