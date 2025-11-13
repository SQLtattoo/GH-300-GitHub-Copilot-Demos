"""
Comprehensive tests for the DataTable module.
"""

import pytest
from data_table import (
    DataTable, ColumnDefinition, 
    apply_search, sort_data, get_paginated_data, process_table_data
)


class TestColumnDefinition:
    """Test ColumnDefinition dataclass."""
    
    def test_column_definition_basic(self):
        """Test basic column definition creation."""
        col = ColumnDefinition(key='name', label='Name')
        assert col.key == 'name'
        assert col.label == 'Name'
        assert col.sortable == True
        assert col.formatter is None
    
    def test_column_definition_with_formatter(self):
        """Test column definition with custom formatter."""
        def formatter(value):
            return f"${value}"
        
        col = ColumnDefinition(key='price', label='Price', formatter=formatter)
        assert col.formatter is not None
        assert col.formatter(100) == "$100"
    
    def test_column_definition_not_sortable(self):
        """Test column definition with sortable=False."""
        col = ColumnDefinition(key='actions', label='Actions', sortable=False)
        assert col.sortable == False


class TestDataTableInitialization:
    """Test DataTable initialization."""
    
    def test_init_basic(self, sample_employees, employee_columns):
        """Test basic initialization."""
        table = DataTable(sample_employees, employee_columns)
        assert table.get_total_rows() == 4
        assert table.get_total_pages() == 1
    
    def test_init_custom_rows_per_page(self, sample_employees, employee_columns):
        """Test initialization with custom rows per page."""
        table = DataTable(sample_employees, employee_columns, rows_per_page=2)
        assert table.get_total_pages() == 2
    
    def test_init_invalid_rows_per_page(self, sample_employees, employee_columns):
        """Test initialization with invalid rows_per_page."""
        with pytest.raises(ValueError, match="rows_per_page must be at least 1"):
            DataTable(sample_employees, employee_columns, rows_per_page=0)


class TestPagination:
    """Test pagination functionality."""
    
    def test_get_current_page_first_page(self, sample_employees, employee_columns):
        """Test getting first page."""
        table = DataTable(sample_employees, employee_columns, rows_per_page=2)
        page = table.get_current_page()
        assert len(page) == 2
        assert page[0]['name'] == 'Alice'
        assert page[1]['name'] == 'Bob'
    
    def test_set_page_valid(self, sample_employees, employee_columns):
        """Test setting valid page number."""
        table = DataTable(sample_employees, employee_columns, rows_per_page=2)
        table.set_page(2)
        page = table.get_current_page()
        assert len(page) == 2
        assert page[0]['name'] == 'Charlie'
    
    def test_set_page_invalid(self, sample_employees, employee_columns):
        """Test setting invalid page number."""
        table = DataTable(sample_employees, employee_columns)
        with pytest.raises(ValueError, match="Page must be between 1 and"):
            table.set_page(0)
        with pytest.raises(ValueError, match="Page must be between 1 and"):
            table.set_page(10)
    
    def test_get_total_pages_empty_data(self, employee_columns):
        """Test total pages with empty data."""
        table = DataTable([], employee_columns)
        assert table.get_total_pages() == 1
    
    def test_get_total_pages_exact_division(self, sample_employees, employee_columns):
        """Test total pages with exact division."""
        table = DataTable(sample_employees, employee_columns, rows_per_page=2)
        assert table.get_total_pages() == 2  # 4 items / 2 per page
    
    def test_get_total_pages_with_remainder(self, sample_employees, employee_columns):
        """Test total pages with remainder."""
        table = DataTable(sample_employees, employee_columns, rows_per_page=3)
        assert table.get_total_pages() == 2  # 4 items / 3 per page = 2 pages
    
    def test_get_page_info(self, sample_employees, employee_columns):
        """Test getting page information."""
        table = DataTable(sample_employees, employee_columns, rows_per_page=2)
        table.set_page(2)
        info = table.get_page_info()
        
        assert info['current_page'] == 2
        assert info['total_pages'] == 2
        assert info['total_rows'] == 4
        assert info['start_row'] == 3
        assert info['end_row'] == 4
        assert info['has_prev'] == True
        assert info['has_next'] == False


class TestSorting:
    """Test sorting functionality."""
    
    def test_sort_ascending(self, sample_employees, employee_columns):
        """Test sorting in ascending order."""
        table = DataTable(sample_employees, employee_columns)
        table.sort('salary', ascending=True)
        page = table.get_current_page()
        assert page[0]['salary'] == 75000  # Bob - lowest
        assert page[-1]['salary'] == 105000  # Charlie - highest
    
    def test_sort_descending(self, sample_employees, employee_columns):
        """Test sorting in descending order."""
        table = DataTable(sample_employees, employee_columns)
        table.sort('salary', ascending=False)
        page = table.get_current_page()
        assert page[0]['salary'] == 105000  # Charlie - highest
        assert page[-1]['salary'] == 75000  # Bob - lowest
    
    def test_sort_by_string(self, sample_employees, employee_columns):
        """Test sorting by string column."""
        table = DataTable(sample_employees, employee_columns)
        table.sort('name', ascending=True)
        page = table.get_current_page()
        assert page[0]['name'] == 'Alice'
        assert page[-1]['name'] == 'Diana'
    
    def test_sort_invalid_column(self, sample_employees, employee_columns):
        """Test sorting by invalid column."""
        table = DataTable(sample_employees, employee_columns)
        with pytest.raises(ValueError, match="Column 'invalid' not found"):
            table.sort('invalid')
    
    def test_sort_non_sortable_column(self, sample_employees):
        """Test sorting by non-sortable column."""
        columns = [
            ColumnDefinition(key='name', label='Name', sortable=False),
        ]
        table = DataTable(sample_employees, columns)
        with pytest.raises(ValueError, match="Column 'name' is not sortable"):
            table.sort('name')
    
    def test_sort_resets_to_page_one(self, sample_employees, employee_columns):
        """Test that sorting resets to page 1."""
        table = DataTable(sample_employees, employee_columns, rows_per_page=2)
        table.set_page(2)
        table.sort('name')
        info = table.get_page_info()
        assert info['current_page'] == 1
    
    def test_get_sort_state(self, sample_employees, employee_columns):
        """Test getting current sort state."""
        table = DataTable(sample_employees, employee_columns)
        table.sort('salary', ascending=False)
        state = table.get_sort_state()
        assert state['column'] == 'salary'
        assert state['ascending'] == False


class TestSearch:
    """Test search functionality."""
    
    def test_search_basic(self, sample_employees, employee_columns):
        """Test basic search."""
        table = DataTable(sample_employees, employee_columns)
        table.search('Engineering')
        assert table.get_total_rows() == 2  # Alice and Charlie
    
    def test_search_case_insensitive(self, sample_employees, employee_columns):
        """Test case-insensitive search."""
        table = DataTable(sample_employees, employee_columns)
        table.search('engineering')  # lowercase
        assert table.get_total_rows() == 2
    
    def test_search_partial_match(self, sample_employees, employee_columns):
        """Test partial string matching."""
        table = DataTable(sample_employees, employee_columns)
        table.search('ali')  # matches "Alice"
        assert table.get_total_rows() == 1
        page = table.get_current_page()
        assert page[0]['name'] == 'Alice'
    
    def test_search_no_results(self, sample_employees, employee_columns):
        """Test search with no results."""
        table = DataTable(sample_employees, employee_columns)
        table.search('NonExistent')
        assert table.get_total_rows() == 0
        assert table.is_empty() == True
    
    def test_search_empty_query(self, sample_employees, employee_columns):
        """Test search with empty query shows all data."""
        table = DataTable(sample_employees, employee_columns)
        table.search('Engineering')
        table.search('')  # Clear search
        assert table.get_total_rows() == 4
    
    def test_search_resets_to_page_one(self, sample_employees, employee_columns):
        """Test that search resets to page 1."""
        table = DataTable(sample_employees, employee_columns, rows_per_page=2)
        table.set_page(2)
        table.search('Alice')
        info = table.get_page_info()
        assert info['current_page'] == 1
    
    def test_get_search_query(self, sample_employees, employee_columns):
        """Test getting current search query."""
        table = DataTable(sample_employees, employee_columns)
        table.search('Engineering')
        assert table.get_search_query() == 'engineering'  # Lowercased


class TestFormatting:
    """Test cell formatting functionality."""
    
    def test_format_cell_without_formatter(self, sample_employees, employee_columns):
        """Test formatting cell without custom formatter."""
        table = DataTable(sample_employees, employee_columns)
        item = sample_employees[0]
        column = employee_columns[0]  # name column
        formatted = table.format_cell(item, column)
        assert formatted == 'Alice'
    
    def test_format_cell_with_formatter(self, sample_employees):
        """Test formatting cell with custom formatter."""
        def currency_formatter(value):
            return f"${value:,.2f}"
        
        columns = [
            ColumnDefinition(key='salary', label='Salary', formatter=currency_formatter)
        ]
        table = DataTable(sample_employees, columns)
        item = sample_employees[0]
        column = columns[0]
        formatted = table.format_cell(item, column)
        assert formatted == "$95,000.00"
    
    def test_format_cell_none_value(self, employee_columns):
        """Test formatting cell with None value."""
        data = [{'name': None}]
        table = DataTable(data, [employee_columns[0]])
        formatted = table.format_cell(data[0], employee_columns[0])
        assert formatted == ""


class TestEmptyState:
    """Test empty state handling."""
    
    def test_is_empty_with_data(self, sample_employees, employee_columns):
        """Test is_empty returns False when data exists."""
        table = DataTable(sample_employees, employee_columns)
        assert table.is_empty() == False
    
    def test_is_empty_without_data(self, employee_columns):
        """Test is_empty returns True when no data."""
        table = DataTable([], employee_columns)
        assert table.is_empty() == True
    
    def test_is_empty_after_search(self, sample_employees, employee_columns):
        """Test is_empty after search with no results."""
        table = DataTable(sample_employees, employee_columns)
        table.search('NonExistent')
        assert table.is_empty() == True


class TestReset:
    """Test reset functionality."""
    
    def test_reset_clears_search(self, sample_employees, employee_columns):
        """Test reset clears search."""
        table = DataTable(sample_employees, employee_columns)
        table.search('Engineering')
        table.reset()
        assert table.get_search_query() == ''
        assert table.get_total_rows() == 4
    
    def test_reset_clears_sort(self, sample_employees, employee_columns):
        """Test reset clears sort."""
        table = DataTable(sample_employees, employee_columns)
        table.sort('salary', ascending=False)
        table.reset()
        state = table.get_sort_state()
        assert state['column'] is None
    
    def test_reset_to_page_one(self, sample_employees, employee_columns):
        """Test reset returns to page 1."""
        table = DataTable(sample_employees, employee_columns, rows_per_page=2)
        table.set_page(2)
        table.reset()
        info = table.get_page_info()
        assert info['current_page'] == 1


class TestPureHelperFunctions:
    """Test pure helper functions."""
    
    def test_apply_search(self, sample_employees, employee_columns):
        """Test apply_search helper function."""
        result = apply_search(sample_employees, employee_columns, 'engineering')
        assert len(result) == 2
    
    def test_apply_search_empty_query(self, sample_employees, employee_columns):
        """Test apply_search with empty query returns all."""
        result = apply_search(sample_employees, employee_columns, '')
        assert len(result) == 4
    
    def test_sort_data(self, sample_employees):
        """Test sort_data helper function."""
        result = sort_data(sample_employees, 'salary', ascending=True)
        assert result[0]['salary'] == 75000
        assert result[-1]['salary'] == 105000
    
    def test_sort_data_descending(self, sample_employees):
        """Test sort_data in descending order."""
        result = sort_data(sample_employees, 'salary', ascending=False)
        assert result[0]['salary'] == 105000
        assert result[-1]['salary'] == 75000
    
    def test_get_paginated_data(self, sample_employees):
        """Test get_paginated_data helper function."""
        result = get_paginated_data(sample_employees, page=1, rows_per_page=2)
        assert len(result) == 2
        assert result[0]['name'] == 'Alice'
    
    def test_get_paginated_data_second_page(self, sample_employees):
        """Test getting second page."""
        result = get_paginated_data(sample_employees, page=2, rows_per_page=2)
        assert len(result) == 2
        assert result[0]['name'] == 'Charlie'
    
    def test_get_paginated_data_invalid_page(self, sample_employees):
        """Test get_paginated_data with invalid page."""
        with pytest.raises(ValueError, match="Page must be at least 1"):
            get_paginated_data(sample_employees, page=0, rows_per_page=2)
    
    def test_get_paginated_data_invalid_rows_per_page(self, sample_employees):
        """Test get_paginated_data with invalid rows_per_page."""
        with pytest.raises(ValueError, match="rows_per_page must be at least 1"):
            get_paginated_data(sample_employees, page=1, rows_per_page=0)
    
    def test_process_table_data_basic(self, sample_employees, employee_columns):
        """Test process_table_data all-in-one function."""
        result = process_table_data(
            data=sample_employees,
            columns=employee_columns,
            page=1,
            rows_per_page=2
        )
        assert len(result['rows']) == 2
        assert result['total_rows'] == 4
        assert result['total_pages'] == 2
        assert result['current_page'] == 1
    
    def test_process_table_data_with_search(self, sample_employees, employee_columns):
        """Test process_table_data with search."""
        result = process_table_data(
            data=sample_employees,
            columns=employee_columns,
            search_query='engineering',
            page=1,
            rows_per_page=10
        )
        assert len(result['rows']) == 2
        assert result['total_rows'] == 2
    
    def test_process_table_data_with_sort(self, sample_employees, employee_columns):
        """Test process_table_data with sorting."""
        result = process_table_data(
            data=sample_employees,
            columns=employee_columns,
            sort_column='salary',
            sort_ascending=False,
            page=1,
            rows_per_page=10
        )
        assert result['rows'][0]['salary'] == 105000  # Highest first
    
    def test_process_table_data_combined(self, sample_employees, employee_columns):
        """Test process_table_data with search, sort, and pagination."""
        result = process_table_data(
            data=sample_employees,
            columns=employee_columns,
            search_query='engineering',
            sort_column='salary',
            sort_ascending=True,
            page=1,
            rows_per_page=1
        )
        assert len(result['rows']) == 1
        assert result['rows'][0]['name'] == 'Alice'  # Lower salary
        assert result['total_rows'] == 2
        assert result['has_next'] == True


@pytest.mark.parametrize("page,rows_per_page,expected_count", [
    (1, 2, 2),
    (2, 2, 2),
    (1, 4, 4),
    (1, 10, 4),
])
def test_pagination_parametrized(sample_employees, employee_columns, page, rows_per_page, expected_count):
    """Parametrized test for pagination."""
    table = DataTable(sample_employees, employee_columns, rows_per_page=rows_per_page)
    table.set_page(page)
    result = table.get_current_page()
    assert len(result) <= expected_count
