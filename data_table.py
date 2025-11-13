"""
DataTable module for displaying tabular data in web frameworks.

A generic helper component to display, sort, search, and paginate tabular data.
Compatible with Flask, Django, FastAPI, and other web frameworks.
"""

from typing import TypeVar, Generic, List, Dict, Any, Callable, Optional
from dataclasses import dataclass
import math


T = TypeVar('T')


@dataclass
class ColumnDefinition:
    """
    Definition of a table column.
    
    Attributes:
        key (str): The field name or key to access the data
        label (str): Display label for the column header
        sortable (bool): Whether the column can be sorted
        formatter (Optional[Callable]): Optional function to format the cell value
    """
    key: str
    label: str
    sortable: bool = True
    formatter: Optional[Callable[[Any], str]] = None


class DataTable(Generic[T]):
    """
    Generic data table component for displaying tabular data.
    
    Features:
    - Accepts a list of objects or dictionaries
    - Column definitions to map object fields
    - Sorting on any column (ascending/descending)
    - Pagination (configurable rows per page, default 10)
    - Text search across all columns
    - Error and empty states handling
    - Designed to plug into Flask, Django, or FastAPI templates
    
    Type Parameters:
        T: The type of data objects in the table
    
    Example:
        >>> columns = [
        ...     ColumnDefinition(key='name', label='Name'),
        ...     ColumnDefinition(key='age', label='Age')
        ... ]
        >>> data = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
        >>> table = DataTable(data, columns)
        >>> table.set_page(1)
        >>> rows = table.get_current_page()
    """
    
    def __init__(
        self,
        data: List[T],
        columns: List[ColumnDefinition],
        rows_per_page: int = 10
    ):
        """
        Initialize the DataTable.
        
        Args:
            data (List[T]): List of data objects or dictionaries
            columns (List[ColumnDefinition]): Column definitions for the table
            rows_per_page (int): Number of rows to display per page (default: 10)
        
        Raises:
            ValueError: If rows_per_page is less than 1
        """
        if rows_per_page < 1:
            raise ValueError("rows_per_page must be at least 1")
        
        self._original_data = data
        self._filtered_data = data
        self._columns = columns
        self._rows_per_page = rows_per_page
        self._current_page = 1
        self._sort_column: Optional[str] = None
        self._sort_ascending = True
        self._search_query = ""
    
    def _get_value(self, item: T, key: str) -> Any:
        """
        Extract value from an item by key.
        
        Supports both dictionary access and object attribute access.
        
        Args:
            item (T): The data item
            key (str): The key or attribute name
        
        Returns:
            Any: The extracted value, or None if not found
        """
        if isinstance(item, dict):
            return item.get(key)
        else:
            return getattr(item, key, None)
    
    def search(self, query: str) -> None:
        """
        Filter data based on search query across all columns.
        
        The search is case-insensitive and matches partial strings.
        Resets to page 1 after searching.
        
        Args:
            query (str): Search query string
        """
        self._search_query = query.lower().strip()
        
        if not self._search_query:
            self._filtered_data = self._original_data
        else:
            self._filtered_data = []
            for item in self._original_data:
                # Search across all columns
                for column in self._columns:
                    value = self._get_value(item, column.key)
                    if value is not None and self._search_query in str(value).lower():
                        self._filtered_data.append(item)
                        break
        
        self._current_page = 1
    
    def sort(self, column_key: str, ascending: bool = True) -> None:
        """
        Sort the filtered data by a column.
        
        Args:
            column_key (str): The column key to sort by
            ascending (bool): Sort in ascending order if True, descending if False
        
        Raises:
            ValueError: If column_key is not found or not sortable
        """
        # Validate column exists and is sortable
        column = next((col for col in self._columns if col.key == column_key), None)
        if not column:
            raise ValueError(f"Column '{column_key}' not found")
        if not column.sortable:
            raise ValueError(f"Column '{column_key}' is not sortable")
        
        self._sort_column = column_key
        self._sort_ascending = ascending
        
        # Sort the filtered data
        self._filtered_data = sorted(
            self._filtered_data,
            key=lambda item: self._get_value(item, column_key) or "",
            reverse=not ascending
        )
        
        self._current_page = 1
    
    def set_page(self, page: int) -> None:
        """
        Set the current page number.
        
        Args:
            page (int): Page number (1-indexed)
        
        Raises:
            ValueError: If page number is invalid
        """
        total_pages = self.get_total_pages()
        if page < 1 or page > total_pages:
            raise ValueError(f"Page must be between 1 and {total_pages}")
        self._current_page = page
    
    def get_current_page(self) -> List[T]:
        """
        Get the data for the current page.
        
        Returns:
            List[T]: List of data items for the current page
        """
        start_idx = (self._current_page - 1) * self._rows_per_page
        end_idx = start_idx + self._rows_per_page
        return self._filtered_data[start_idx:end_idx]
    
    def get_total_pages(self) -> int:
        """
        Get the total number of pages.
        
        Returns:
            int: Total number of pages
        """
        if not self._filtered_data:
            return 1
        return math.ceil(len(self._filtered_data) / self._rows_per_page)
    
    def get_total_rows(self) -> int:
        """
        Get the total number of rows in filtered data.
        
        Returns:
            int: Total number of rows
        """
        return len(self._filtered_data)
    
    def is_empty(self) -> bool:
        """
        Check if the table has no data.
        
        Returns:
            bool: True if no data is available
        """
        return len(self._filtered_data) == 0
    
    def get_page_info(self) -> Dict[str, Any]:
        """
        Get pagination information.
        
        Returns:
            Dict[str, Any]: Dictionary containing pagination details
                - current_page: Current page number
                - total_pages: Total number of pages
                - total_rows: Total number of rows
                - start_row: Starting row number (1-indexed)
                - end_row: Ending row number (1-indexed)
                - has_prev: Whether there's a previous page
                - has_next: Whether there's a next page
        """
        total_rows = self.get_total_rows()
        start_row = (self._current_page - 1) * self._rows_per_page + 1
        end_row = min(self._current_page * self._rows_per_page, total_rows)
        
        return {
            'current_page': self._current_page,
            'total_pages': self.get_total_pages(),
            'total_rows': total_rows,
            'start_row': start_row if total_rows > 0 else 0,
            'end_row': end_row,
            'has_prev': self._current_page > 1,
            'has_next': self._current_page < self.get_total_pages()
        }
    
    def format_cell(self, item: T, column: ColumnDefinition) -> str:
        """
        Format a cell value using the column's formatter if available.
        
        Args:
            item (T): The data item
            column (ColumnDefinition): The column definition
        
        Returns:
            str: Formatted cell value
        """
        value = self._get_value(item, column.key)
        
        if column.formatter:
            return column.formatter(value)
        
        return str(value) if value is not None else ""
    
    def get_columns(self) -> List[ColumnDefinition]:
        """
        Get the column definitions.
        
        Returns:
            List[ColumnDefinition]: List of column definitions
        """
        return self._columns
    
    def get_sort_state(self) -> Dict[str, Any]:
        """
        Get the current sort state.
        
        Returns:
            Dict[str, Any]: Dictionary with 'column' and 'ascending' keys
        """
        return {
            'column': self._sort_column,
            'ascending': self._sort_ascending
        }
    
    def get_search_query(self) -> str:
        """
        Get the current search query.
        
        Returns:
            str: Current search query
        """
        return self._search_query
    
    def reset(self) -> None:
        """
        Reset the table to its initial state.
        
        Clears search, sorting, and resets to page 1.
        """
        self._filtered_data = self._original_data
        self._current_page = 1
        self._sort_column = None
        self._sort_ascending = True
        self._search_query = ""


# Pure helper functions - framework-agnostic utilities


def apply_search(data: List[T], columns: List[ColumnDefinition], query: str) -> List[T]:
    """
    Apply search filter to data across all columns.
    
    Pure function that doesn't modify the original data.
    Case-insensitive partial string matching.
    
    Args:
        data (List[T]): List of data items to search
        columns (List[ColumnDefinition]): Column definitions for accessing data fields
        query (str): Search query string
    
    Returns:
        List[T]: Filtered list of items matching the search query
    
    Example:
        >>> data = [{'name': 'Alice'}, {'name': 'Bob'}]
        >>> columns = [ColumnDefinition(key='name', label='Name')]
        >>> apply_search(data, columns, 'ali')
        [{'name': 'Alice'}]
    """
    query = query.lower().strip()
    
    if not query:
        return data
    
    filtered = []
    for item in data:
        for column in columns:
            value = _get_item_value(item, column.key)
            if value is not None and query in str(value).lower():
                filtered.append(item)
                break
    
    return filtered


def sort_data(
    data: List[T],
    column_key: str,
    ascending: bool = True
) -> List[T]:
    """
    Sort data by a column key.
    
    Pure function that returns a new sorted list without modifying the original.
    
    Args:
        data (List[T]): List of data items to sort
        column_key (str): The key/field name to sort by
        ascending (bool): Sort in ascending order if True, descending if False
    
    Returns:
        List[T]: New sorted list
    
    Example:
        >>> data = [{'age': 30}, {'age': 25}]
        >>> sort_data(data, 'age', ascending=True)
        [{'age': 25}, {'age': 30}]
    """
    return sorted(
        data,
        key=lambda item: _get_item_value(item, column_key) or "",
        reverse=not ascending
    )


def get_paginated_data(
    data: List[T],
    page: int,
    rows_per_page: int
) -> List[T]:
    """
    Get a specific page of data.
    
    Pure function for pagination without modifying the original data.
    
    Args:
        data (List[T]): List of data items to paginate
        page (int): Page number (1-indexed)
        rows_per_page (int): Number of rows per page
    
    Returns:
        List[T]: Slice of data for the requested page
    
    Raises:
        ValueError: If page < 1 or rows_per_page < 1
    
    Example:
        >>> data = [1, 2, 3, 4, 5]
        >>> get_paginated_data(data, page=1, rows_per_page=2)
        [1, 2]
        >>> get_paginated_data(data, page=2, rows_per_page=2)
        [3, 4]
    """
    if page < 1:
        raise ValueError("Page must be at least 1")
    if rows_per_page < 1:
        raise ValueError("rows_per_page must be at least 1")
    
    start_idx = (page - 1) * rows_per_page
    end_idx = start_idx + rows_per_page
    return data[start_idx:end_idx]


def process_table_data(
    data: List[T],
    columns: List[ColumnDefinition],
    search_query: Optional[str] = None,
    sort_column: Optional[str] = None,
    sort_ascending: bool = True,
    page: int = 1,
    rows_per_page: int = 10
) -> Dict[str, Any]:
    """
    Process table data with search, sort, and pagination in one call.
    
    Pure, framework-agnostic function that applies all transformations
    and returns paginated results with metadata.
    
    Args:
        data (List[T]): Original data list
        columns (List[ColumnDefinition]): Column definitions
        search_query (Optional[str]): Search query to filter data
        sort_column (Optional[str]): Column key to sort by
        sort_ascending (bool): Sort direction (default: True)
        page (int): Page number (1-indexed, default: 1)
        rows_per_page (int): Rows per page (default: 10)
    
    Returns:
        Dict[str, Any]: Dictionary containing:
            - rows: List of data items for the current page
            - total_rows: Total number of filtered rows
            - total_pages: Total number of pages
            - current_page: Current page number
            - has_prev: Whether there's a previous page
            - has_next: Whether there's a next page
            - start_row: Starting row number (1-indexed)
            - end_row: Ending row number (1-indexed)
    
    Example:
        >>> data = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
        >>> columns = [ColumnDefinition(key='name', label='Name')]
        >>> result = process_table_data(data, columns, page=1, rows_per_page=10)
        >>> result['rows']
        [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
    """
    # Apply search filter
    filtered_data = data
    if search_query:
        filtered_data = apply_search(filtered_data, columns, search_query)
    
    # Apply sorting
    if sort_column:
        filtered_data = sort_data(filtered_data, sort_column, sort_ascending)
    
    # Calculate pagination metadata
    total_rows = len(filtered_data)
    total_pages = math.ceil(total_rows / rows_per_page) if total_rows > 0 else 1
    
    # Validate page number
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages
    
    # Get paginated data
    rows = get_paginated_data(filtered_data, page, rows_per_page)
    
    # Calculate row numbers
    start_row = (page - 1) * rows_per_page + 1 if total_rows > 0 else 0
    end_row = min(page * rows_per_page, total_rows)
    
    return {
        'rows': rows,
        'total_rows': total_rows,
        'total_pages': total_pages,
        'current_page': page,
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'start_row': start_row,
        'end_row': end_row
    }


def _get_item_value(item: T, key: str) -> Any:
    """
    Internal helper to extract value from an item by key.
    
    Supports both dictionary access and object attribute access.
    
    Args:
        item (T): The data item
        key (str): The key or attribute name
    
    Returns:
        Any: The extracted value, or None if not found
    """
    if isinstance(item, dict):
        return item.get(key)
    else:
        return getattr(item, key, None)
