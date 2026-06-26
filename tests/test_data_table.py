from dataclasses import dataclass

import pytest

from data_table import (
    ColumnDefinition,
    DataTable,
    _get_item_value,
    apply_search,
    get_paginated_data,
    process_table_data,
    sort_data,
)


@dataclass
class Person:
    name: str
    age: int


def _sample_rows() -> list[dict[str, object]]:
    return [
        {"name": "Alice", "age": 30, "city": "Athens"},
        {"name": "Bob", "age": 25, "city": "Berlin"},
        {"name": "Carol", "age": 35, "city": "Cairo"},
    ]


def _sample_columns() -> list[ColumnDefinition]:
    return [
        ColumnDefinition("name", "Name"),
        ColumnDefinition("age", "Age"),
        ColumnDefinition("city", "City"),
    ]


def test_datatable_constructor_and_basic_operations() -> None:
    with pytest.raises(ValueError):
        DataTable(_sample_rows(), _sample_columns(), rows_per_page=0)

    table = DataTable(_sample_rows(), _sample_columns(), rows_per_page=2)
    assert table.get_total_pages() == 2
    assert table.get_total_rows() == 3
    assert table.is_empty() is False

    table.search("ber")
    assert table.get_total_rows() == 1
    assert table.get_search_query() == "ber"

    table.search("  ")
    assert table.get_total_rows() == 3

    table.sort("age", ascending=False)
    assert table.get_current_page()[0]["name"] == "Carol"

    sort_state = table.get_sort_state()
    assert sort_state["column"] == "age"
    assert sort_state["ascending"] is False

    with pytest.raises(ValueError):
        table.sort("missing")

    not_sortable = [ColumnDefinition("name", "Name", sortable=False)]
    table2 = DataTable([{"name": "Alice"}], not_sortable)
    with pytest.raises(ValueError):
        table2.sort("name")


def test_datatable_pagination_and_page_info() -> None:
    table = DataTable(_sample_rows(), _sample_columns(), rows_per_page=2)

    with pytest.raises(ValueError):
        table.set_page(0)

    table.set_page(2)
    page_rows = table.get_current_page()
    assert len(page_rows) == 1
    assert page_rows[0]["name"] == "Carol"

    info = table.get_page_info()
    assert info["current_page"] == 2
    assert info["total_pages"] == 2
    assert info["start_row"] == 3
    assert info["end_row"] == 3
    assert info["has_prev"] is True
    assert info["has_next"] is False

    empty_table = DataTable([], _sample_columns())
    assert empty_table.get_total_pages() == 1
    assert empty_table.get_page_info()["start_row"] == 0


def test_datatable_format_columns_and_reset() -> None:
    cols = [
        ColumnDefinition("name", "Name"),
        ColumnDefinition("age", "Age", formatter=lambda value: f"{value} yrs"),
    ]
    row = {"name": "Alice", "age": 30}
    table = DataTable([row], cols)

    assert table.format_cell(row, cols[0]) == "Alice"
    assert table.format_cell(row, cols[1]) == "30 yrs"
    assert table.get_columns() == cols

    table.search("ali")
    table.sort("name")
    table.reset()

    assert table.get_search_query() == ""
    assert table.get_sort_state()["column"] is None


def test_pure_helper_functions() -> None:
    rows = _sample_rows()
    cols = _sample_columns()

    assert [row["name"] for row in apply_search(rows, cols, "ca")] == ["Carol"]
    assert apply_search(rows, cols, "") == rows

    sorted_rows = sort_data(rows, "age", ascending=True)
    assert [row["name"] for row in sorted_rows] == ["Bob", "Alice", "Carol"]

    assert get_paginated_data(rows, page=1, rows_per_page=2) == rows[:2]
    assert get_paginated_data(rows, page=2, rows_per_page=2) == rows[2:]

    with pytest.raises(ValueError):
        get_paginated_data(rows, page=0, rows_per_page=2)

    with pytest.raises(ValueError):
        get_paginated_data(rows, page=1, rows_per_page=0)


def test_process_table_data_and_get_item_value() -> None:
    rows = _sample_rows()
    cols = _sample_columns()

    result = process_table_data(
        rows,
        cols,
        search_query="a",
        sort_column="age",
        sort_ascending=False,
        page=10,
        rows_per_page=1,
    )

    assert result["total_rows"] == 2
    assert result["total_pages"] == 2
    assert result["current_page"] == 2
    assert result["rows"][0]["name"] == "Alice"
    assert result["has_prev"] is True
    assert result["has_next"] is False

    normalized = process_table_data(rows, cols, page=0, rows_per_page=2)
    assert normalized["current_page"] == 1
    assert normalized["start_row"] == 1

    person = Person(name="Dora", age=40)
    assert _get_item_value({"name": "Eve"}, "name") == "Eve"
    assert _get_item_value(person, "name") == "Dora"
    assert _get_item_value(person, "missing") is None
