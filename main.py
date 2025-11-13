"""
Main application entry point.
Demonstrates how all modules work together.
"""

from calculator import Calculator
from data_processor import DataProcessor
from file_handler import FileHandler
from data_table import DataTable, ColumnDefinition, process_table_data
from logger import logger


def main():
    """Main function to demonstrate the application."""
    logger.info("=" * 50)
    logger.info("GitHub Copilot Demo Project")
    logger.info("=" * 50)
    
    # Calculator demonstration
    logger.info("--- Calculator Demo ---")
    calc = Calculator()
    logger.info(f"5 + 3 = {calc.add(5, 3)}")
    logger.info(f"10 - 4 = {calc.subtract(10, 4)}")
    logger.info(f"2 ^ 3 = {calc.power(2, 3)}")
    logger.info(f"Percentage: 25 of 200 = {calc.percentage(25, 200)}%")
    logger.info(f"Operation history: {calc.get_history()}")
    
    # Data processor demonstration
    logger.info("--- Data Processor Demo ---")
    processor = DataProcessor()
    logger.info(f"Reverse 'Hello': {processor.reverse_string('Hello')}")
    numbers = [1, 2, 2, 3, 4, 4, 5]
    logger.info(f"Remove duplicates from {numbers}: {processor.remove_duplicates(numbers)}")
    logger.info(f"Chunk [1,2,3,4,5,6] into size 2: {processor.chunk_list([1,2,3,4,5,6], 2)}")
    logger.info(f"Operations processed: {processor.get_processed_count()}")
    
    # File handler demonstration
    logger.info("--- File Handler Demo ---")
    file_handler = FileHandler()
    logger.info(f"Processed files: {file_handler.get_processed_files()}")
    
    # DataTable demonstration
    logger.info("--- DataTable Demo ---")
    
    # Sample data: employees
    employees = [
        {'name': 'Alice Johnson', 'department': 'Engineering', 'salary': 95000, 'age': 32},
        {'name': 'Bob Smith', 'department': 'Marketing', 'salary': 75000, 'age': 28},
        {'name': 'Charlie Brown', 'department': 'Engineering', 'salary': 105000, 'age': 35},
        {'name': 'Diana Prince', 'department': 'Sales', 'salary': 85000, 'age': 30},
        {'name': 'Eve Davis', 'department': 'Engineering', 'salary': 98000, 'age': 29},
        {'name': 'Frank Miller', 'department': 'Marketing', 'salary': 72000, 'age': 26},
        {'name': 'Grace Lee', 'department': 'Sales', 'salary': 88000, 'age': 31},
        {'name': 'Henry Wilson', 'department': 'Engineering', 'salary': 110000, 'age': 38},
        {'name': 'Iris Chen', 'department': 'Marketing', 'salary': 79000, 'age': 27},
        {'name': 'Jack Turner', 'department': 'Sales', 'salary': 92000, 'age': 33},
    ]
    
    # Define columns with custom formatter for salary
    def format_currency(value):
        return f"${value:,.2f}"
    
    columns = [
        ColumnDefinition(key='name', label='Employee Name'),
        ColumnDefinition(key='department', label='Department'),
        ColumnDefinition(key='salary', label='Salary', formatter=format_currency),
        ColumnDefinition(key='age', label='Age'),
    ]
    
    # Test 1: Basic table creation and pagination
    logger.info("Test 1: Creating DataTable with 10 employees, 5 per page")
    table = DataTable(employees, columns, rows_per_page=5)
    logger.info(f"Total rows: {table.get_total_rows()}")
    logger.info(f"Total pages: {table.get_total_pages()}")
    
    # Get first page
    page_1 = table.get_current_page()
    logger.info(f"Page 1 employees: {[emp['name'] for emp in page_1]}")
    
    # Test 2: Sorting
    logger.info("Test 2: Sorting by salary (descending)")
    table.sort('salary', ascending=False)
    sorted_page = table.get_current_page()
    logger.info(f"Top 5 earners: {[(emp['name'], emp['salary']) for emp in sorted_page]}")
    
    # Test 3: Search functionality
    logger.info("Test 3: Searching for 'Engineering' department")
    table.search('Engineering')
    search_results = table.get_current_page()
    logger.info(f"Found {table.get_total_rows()} engineers")
    logger.info(f"Engineering employees: {[emp['name'] for emp in search_results]}")
    
    # Test 4: Pagination info
    logger.info("Test 4: Getting pagination info")
    table.reset()  # Reset to show all data
    table.set_page(2)
    page_info = table.get_page_info()
    logger.info(f"Page info: Page {page_info['current_page']} of {page_info['total_pages']}")
    logger.info(f"Showing rows {page_info['start_row']}-{page_info['end_row']} of {page_info['total_rows']}")
    logger.info(f"Has previous: {page_info['has_prev']}, Has next: {page_info['has_next']}")
    
    # Test 5: Using pure helper functions
    logger.info("Test 5: Using process_table_data (pure function)")
    result = process_table_data(
        data=employees,
        columns=columns,
        search_query='sales',
        sort_column='salary',
        sort_ascending=False,
        page=1,
        rows_per_page=3
    )
    logger.info(f"Sales employees (sorted by salary, top 3):")
    for emp in result['rows']:
        logger.info(f"  - {emp['name']}: {format_currency(emp['salary'])}")
    logger.info(f"Total sales employees: {result['total_rows']}")
    
    # Test 6: Cell formatting
    logger.info("Test 6: Testing cell formatting")
    table.reset()
    first_employee = table.get_current_page()[0]
    salary_column = next(col for col in columns if col.key == 'salary')
    formatted_salary = table.format_cell(first_employee, salary_column)
    logger.info(f"{first_employee['name']}'s formatted salary: {formatted_salary}")
    
    # Test 7: Empty state
    logger.info("Test 7: Testing empty state")
    table.search('NonExistentDepartment')
    logger.info(f"Is table empty after invalid search: {table.is_empty()}")
    
    logger.info("=" * 50)
    logger.info("Demo completed successfully!")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
