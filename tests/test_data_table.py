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


pytestmark = pytest.mark.unit


@dataclass
class Person:
    name: str
    age: int


@pytest.fixture
def columns():
    return [ColumnDefinition("name", "Name"), ColumnDefinition("age", "Age")]


@pytest.fixture
def people():
    return [
        {"name": "Charlie", "age": 35},
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
    ]


def test_rejects_non_positive_page_size(columns):
    with pytest.raises(ValueError, match="at least 1"):
        DataTable([], columns, rows_per_page=0)


def test_search_is_case_insensitive_resets_page_and_can_be_cleared(people, columns):
    table = DataTable(people, columns, rows_per_page=1)
    table.set_page(2)

    table.search("  ALI ")
    assert table.get_current_page() == [people[1]]
    assert table.get_search_query() == "ali"
    assert table.get_page_info()["current_page"] == 1

    table.search(" ")
    assert table.get_total_rows() == 3


def test_search_matches_object_attributes_and_ignores_missing_values(columns):
    data = [Person("Ada", 36), Person("Grace", 40), object()]

    assert apply_search(data, columns, "ace") == [data[1]]
    assert apply_search(data, columns, "") is data


def test_sort_tracks_direction_resets_page_and_does_not_mutate_original(people, columns):
    table = DataTable(people, columns, rows_per_page=1)
    table.set_page(2)
    table.sort("age", ascending=False)

    assert table.get_current_page() == [people[0]]
    assert table.get_sort_state() == {"column": "age", "ascending": False}
    assert people[0]["name"] == "Charlie"


def test_sort_rejects_unknown_and_disabled_columns(people):
    columns = [ColumnDefinition("name", "Name", sortable=False)]
    table = DataTable(people, columns)

    with pytest.raises(ValueError, match="not found"):
        table.sort("missing")
    with pytest.raises(ValueError, match="not sortable"):
        table.sort("name")


def test_sort_data_supports_objects_and_missing_values():
    data = [Person("Bob", 20), object(), Person("Ada", 30)]

    result = sort_data(data, "name")

    assert result[0] is data[1]
    assert [person.name for person in result[1:]] == ["Ada", "Bob"]


def test_pagination_boundaries_and_metadata(people, columns):
    table = DataTable(people, columns, rows_per_page=2)
    table.set_page(2)

    assert table.get_current_page() == [people[2]]
    assert table.get_page_info() == {
        "current_page": 2,
        "total_pages": 2,
        "total_rows": 3,
        "start_row": 3,
        "end_row": 3,
        "has_prev": True,
        "has_next": False,
    }
    with pytest.raises(ValueError, match="between 1 and 2"):
        table.set_page(0)
    with pytest.raises(ValueError, match="between 1 and 2"):
        table.set_page(3)


def test_empty_table_has_one_empty_page(columns):
    table = DataTable([], columns)

    assert table.is_empty() is True
    assert table.get_total_pages() == 1
    assert table.get_page_info()["start_row"] == 0
    assert table.get_page_info()["end_row"] == 0


def test_cell_formatting_columns_and_reset(people):
    column = ColumnDefinition("age", "Age", formatter=lambda value: f"{value} years")
    table = DataTable(people, [column])

    assert table.format_cell(people[0], column) == "35 years"
    assert table.format_cell(Person("Ada", 30), column) == "30 years"
    assert table.format_cell({}, ColumnDefinition("age", "Age")) == ""
    assert table.get_columns() == [column]

    table.search("35")
    table.sort("age", ascending=False)
    table.reset()
    assert table.get_total_rows() == 3
    assert table.get_search_query() == ""
    assert table.get_sort_state() == {"column": None, "ascending": True}


@pytest.mark.parametrize(("page", "size"), [(0, 2), (1, 0)])
def test_paginated_helper_rejects_invalid_arguments(page, size):
    with pytest.raises(ValueError):
        get_paginated_data([1, 2], page, size)


def test_process_table_data_combines_operations_and_clamps_page(people, columns):
    result = process_table_data(
        people,
        columns,
        search_query="a",
        sort_column="age",
        sort_ascending=False,
        page=99,
        rows_per_page=1,
    )

    assert result == {
        "rows": [people[1]],
        "total_rows": 2,
        "total_pages": 2,
        "current_page": 2,
        "has_prev": True,
        "has_next": False,
        "start_row": 2,
        "end_row": 2,
    }


def test_process_empty_data_clamps_page_to_one(columns):
    result = process_table_data([], columns, page=-5, rows_per_page=2)

    assert result["rows"] == []
    assert result["current_page"] == 1
    assert result["total_pages"] == 1