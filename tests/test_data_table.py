"""Behavior and edge-case tests for the framework-agnostic data table."""

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
    """Object row used to verify attribute-based access."""

    name: str
    age: int


@pytest.fixture
def columns():
    return [
        ColumnDefinition("name", "Name"),
        ColumnDefinition("age", "Age"),
    ]


@pytest.fixture
def rows():
    return [
        {"name": "Charlie", "age": 35},
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
    ]


class TestDataTableValidation:
    def test_rows_per_page_must_be_positive(self, columns):
        with pytest.raises(ValueError, match="at least 1"):
            DataTable([], columns, rows_per_page=0)

    def test_sort_rejects_unknown_column(self, columns):
        table = DataTable([], columns)

        with pytest.raises(ValueError, match="not found"):
            table.sort("missing")

    def test_sort_rejects_non_sortable_column(self):
        table = DataTable([], [ColumnDefinition("name", "Name", sortable=False)])

        with pytest.raises(ValueError, match="not sortable"):
            table.sort("name")

    @pytest.mark.parametrize("page", [0, 3])
    def test_set_page_rejects_out_of_range_page(self, columns, page):
        table = DataTable([{"name": "Alice"}], columns)

        with pytest.raises(ValueError, match="between 1 and 1"):
            table.set_page(page)


class TestDataTableSearchAndSort:
    def test_search_is_trimmed_case_insensitive_and_cross_column(self, rows, columns):
        table = DataTable(rows, columns)

        table.search("  ALI ")
        assert table.get_current_page() == [{"name": "Alice", "age": 30}]
        assert table.get_search_query() == "ali"

        table.search("25")
        assert table.get_current_page() == [{"name": "Bob", "age": 25}]

    def test_search_supports_object_rows_and_missing_values(self, columns):
        data = [Person("Alice", 30), Person("Bob", 25), {"name": None}]
        table = DataTable(data, columns)

        table.search("bob")

        assert table.get_current_page() == [data[1]]

    def test_empty_search_restores_original_rows_and_first_page(self, rows, columns):
        table = DataTable(rows, columns, rows_per_page=1)
        table.set_page(2)

        table.search(" ")

        assert table.get_current_page() == [rows[0]]
        assert table.get_total_rows() == 3

    def test_sort_ascending_and_descending(self, rows, columns):
        table = DataTable(rows, columns)

        table.sort("age")
        assert [row["age"] for row in table.get_current_page()] == [25, 30, 35]
        assert table.get_sort_state() == {"column": "age", "ascending": True}

        table.sort("name", ascending=False)
        assert [row["name"] for row in table.get_current_page()] == ["Charlie", "Bob", "Alice"]
        assert table.get_sort_state() == {"column": "name", "ascending": False}


class TestDataTablePaginationAndState:
    def test_paginates_rows_and_reports_middle_page_metadata(self, rows, columns):
        table = DataTable(rows, columns, rows_per_page=1)
        table.set_page(2)

        assert table.get_current_page() == [rows[1]]
        assert table.get_total_pages() == 3
        assert table.get_page_info() == {
            "current_page": 2,
            "total_pages": 3,
            "total_rows": 3,
            "start_row": 2,
            "end_row": 2,
            "has_prev": True,
            "has_next": True,
        }

    def test_empty_table_has_one_empty_page(self, columns):
        table = DataTable([], columns)

        assert table.is_empty() is True
        assert table.get_total_pages() == 1
        assert table.get_current_page() == []
        assert table.get_page_info() == {
            "current_page": 1,
            "total_pages": 1,
            "total_rows": 0,
            "start_row": 0,
            "end_row": 0,
            "has_prev": False,
            "has_next": False,
        }

    def test_reset_clears_search_sort_and_page(self, rows, columns):
        table = DataTable(rows, columns, rows_per_page=1)
        table.search("a")
        table.sort("name")
        table.set_page(2)

        table.reset()

        assert table.get_current_page() == [rows[0]]
        assert table.get_search_query() == ""
        assert table.get_sort_state() == {"column": None, "ascending": True}
        assert table.get_columns() is columns


class TestCellFormatting:
    def test_uses_custom_formatter(self):
        column = ColumnDefinition("amount", "Amount", formatter=lambda value: f"${value:.2f}")
        table = DataTable([{"amount": 12.5}], [column])

        assert table.format_cell({"amount": 12.5}, column) == "$12.50"

    def test_formats_plain_object_value_and_missing_value(self):
        name_column = ColumnDefinition("name", "Name")
        missing_column = ColumnDefinition("missing", "Missing")
        table = DataTable([Person("Alice", 30)], [name_column, missing_column])

        assert table.format_cell(Person("Alice", 30), name_column) == "Alice"
        assert table.format_cell(Person("Alice", 30), missing_column) == ""


class TestPureHelpers:
    def test_apply_search_returns_original_for_blank_query(self, rows, columns):
        assert apply_search(rows, columns, "  ") is rows

    def test_apply_search_handles_objects_and_skips_none(self, columns):
        data = [Person("Alice", 30), Person("Bob", 25), {"name": None}]

        assert apply_search(data, columns, "25") == [data[1]]

    def test_sort_data_returns_new_list_in_requested_order(self, rows):
        result = sort_data(rows, "age", ascending=False)

        assert [row["age"] for row in result] == [35, 30, 25]
        assert result is not rows

    @pytest.mark.parametrize(
        "page, rows_per_page, message",
        [(0, 2, "Page must be at least 1"), (1, 0, "rows_per_page must be at least 1")],
    )
    def test_get_paginated_data_validates_arguments(self, page, rows_per_page, message):
        with pytest.raises(ValueError, match=message):
            get_paginated_data([1, 2], page, rows_per_page)

    def test_get_paginated_data_returns_page_or_empty_out_of_range(self):
        assert get_paginated_data([1, 2, 3], 2, 2) == [3]
        assert get_paginated_data([1, 2, 3], 5, 2) == []

    def test_process_table_data_combines_search_sort_and_pagination(self, rows, columns):
        result = process_table_data(
            rows,
            columns,
            search_query="a",
            sort_column="age",
            sort_ascending=False,
            page=2,
            rows_per_page=1,
        )

        assert result == {
            "rows": [{"name": "Alice", "age": 30}],
            "total_rows": 2,
            "total_pages": 2,
            "current_page": 2,
            "has_prev": True,
            "has_next": False,
            "start_row": 2,
            "end_row": 2,
        }

    @pytest.mark.parametrize("requested_page, expected_page", [(0, 1), (99, 2)])
    def test_process_table_data_clamps_page(self, rows, columns, requested_page, expected_page):
        result = process_table_data(rows, columns, page=requested_page, rows_per_page=2)

        assert result["current_page"] == expected_page

    def test_process_table_data_handles_empty_rows(self, columns):
        result = process_table_data([], columns)

        assert result["rows"] == []
        assert result["total_pages"] == 1
        assert result["start_row"] == 0
        assert result["end_row"] == 0

    def test_process_table_data_rejects_non_positive_page_size(self, columns):
        with pytest.raises(ValueError, match="rows_per_page must be at least 1"):
            process_table_data([{"name": "Alice"}], columns, rows_per_page=0)