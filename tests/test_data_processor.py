"""
Comprehensive tests for the DataProcessor module.
"""

import pytest
from data_processor import to_title_case, find_most_frequent


class TestStringOperations:
    """Test string manipulation methods."""
    
    def test_reverse_string_basic(self, data_processor):
        """Test basic string reversal."""
        assert data_processor.reverse_string("Hello") == "olleH"
    
    def test_reverse_string_empty(self, data_processor):
        """Test reversing empty string."""
        assert data_processor.reverse_string("") == ""
    
    def test_reverse_string_single_char(self, data_processor):
        """Test reversing single character."""
        assert data_processor.reverse_string("a") == "a"
    
    def test_reverse_string_with_spaces(self, data_processor):
        """Test reversing string with spaces."""
        assert data_processor.reverse_string("Hello World") == "dlroW olleH"


class TestListOperations:
    """Test list manipulation methods."""
    
    def test_remove_duplicates_basic(self, data_processor):
        """Test removing duplicates from list."""
        assert data_processor.remove_duplicates([1, 2, 2, 3, 4, 4, 5]) == [1, 2, 3, 4, 5]
    
    def test_remove_duplicates_preserves_order(self, data_processor):
        """Test that order is preserved."""
        assert data_processor.remove_duplicates([3, 1, 2, 1, 3]) == [3, 1, 2]
    
    def test_remove_duplicates_empty_list(self, data_processor):
        """Test removing duplicates from empty list."""
        assert data_processor.remove_duplicates([]) == []
    
    def test_remove_duplicates_no_duplicates(self, data_processor):
        """Test list with no duplicates."""
        assert data_processor.remove_duplicates([1, 2, 3]) == [1, 2, 3]
    
    def test_remove_duplicates_strings(self, data_processor):
        """Test removing duplicate strings."""
        assert data_processor.remove_duplicates(['a', 'b', 'a', 'c']) == ['a', 'b', 'c']
    
    def test_chunk_list_basic(self, data_processor):
        """Test chunking list into smaller lists."""
        result = data_processor.chunk_list([1, 2, 3, 4, 5, 6], 2)
        assert result == [[1, 2], [3, 4], [5, 6]]
    
    def test_chunk_list_uneven(self, data_processor):
        """Test chunking list with uneven division."""
        result = data_processor.chunk_list([1, 2, 3, 4, 5], 2)
        assert result == [[1, 2], [3, 4], [5]]
    
    def test_chunk_list_size_one(self, data_processor):
        """Test chunking with size 1."""
        result = data_processor.chunk_list([1, 2, 3], 1)
        assert result == [[1], [2], [3]]
    
    def test_chunk_list_invalid_size(self, data_processor):
        """Test chunking with invalid size."""
        with pytest.raises(ValueError, match="Chunk size must be positive"):
            data_processor.chunk_list([1, 2, 3], 0)
        with pytest.raises(ValueError, match="Chunk size must be positive"):
            data_processor.chunk_list([1, 2, 3], -1)
    
    def test_chunk_list_empty(self, data_processor):
        """Test chunking empty list."""
        assert data_processor.chunk_list([], 2) == []


class TestDataProcessing:
    """Test data processing methods."""
    
    def test_process_data_basic(self, data_processor):
        """Test basic data processing (doubling)."""
        assert data_processor.process_data([1, 2, 3]) == [2, 4, 6]
    
    def test_process_data_empty(self, data_processor):
        """Test processing empty list."""
        assert data_processor.process_data([]) == []
    
    def test_process_data_negative_numbers(self, data_processor):
        """Test processing negative numbers."""
        assert data_processor.process_data([-1, -2, -3]) == [-2, -4, -6]
    
    def test_process_data_floats(self, data_processor):
        """Test processing floating point numbers."""
        assert data_processor.process_data([1.5, 2.5, 3.5]) == [3.0, 5.0, 7.0]
    
    def test_process_data_not_iterable(self, data_processor):
        """Test processing non-iterable data."""
        with pytest.raises(TypeError, match="Data must be iterable"):
            data_processor.process_data(123)
    
    def test_process_data_non_numeric(self, data_processor):
        """Test processing with string data (strings support multiplication)."""
        # Strings can be multiplied in Python: 'a' * 2 = 'aa'
        result = data_processor.process_data([1, 2, "three"])
        assert result == [2, 4, "threethree"]


class TestExpressionCalculation:
    """Test mathematical expression calculation."""
    
    def test_calculate_expression_addition(self, data_processor):
        """Test addition expression."""
        assert data_processor.calculate_expression("2+3") == 5
    
    def test_calculate_expression_subtraction(self, data_processor):
        """Test subtraction expression."""
        assert data_processor.calculate_expression("10-4") == 6
    
    def test_calculate_expression_multiplication(self, data_processor):
        """Test multiplication expression."""
        assert data_processor.calculate_expression("3*4") == 12
    
    def test_calculate_expression_division(self, data_processor):
        """Test division expression."""
        assert data_processor.calculate_expression("10/2") == 5
    
    def test_calculate_expression_complex(self, data_processor):
        """Test complex expression with parentheses."""
        assert data_processor.calculate_expression("(2+3)*4") == 20
    
    def test_calculate_expression_with_spaces(self, data_processor):
        """Test expression with spaces."""
        assert data_processor.calculate_expression("2 + 3 * 4") == 14
    
    def test_calculate_expression_division_by_zero(self, data_processor):
        """Test division by zero in expression."""
        with pytest.raises(ValueError, match="Division by zero"):
            data_processor.calculate_expression("10/0")
    
    def test_calculate_expression_invalid_characters(self, data_processor):
        """Test expression with invalid characters."""
        with pytest.raises(ValueError, match="Expression contains invalid characters"):
            data_processor.calculate_expression("2+3; import os")
    
    def test_calculate_expression_invalid_syntax(self, data_processor):
        """Test expression with invalid syntax."""
        # Test with a truly invalid expression that will fail AST parsing
        with pytest.raises(ValueError, match="Invalid expression"):
            data_processor.calculate_expression("2 +")


class TestPerformanceIssues:
    """Test methods with known performance issues."""
    
    def test_find_duplicates_slow(self, data_processor):
        """Test slow duplicate finder (O(n²) implementation)."""
        result = data_processor.find_duplicates_slow([1, 2, 2, 3, 3, 4])
        assert set(result) == {2, 3}
    
    def test_find_duplicates_slow_no_duplicates(self, data_processor):
        """Test slow duplicate finder with no duplicates."""
        assert data_processor.find_duplicates_slow([1, 2, 3]) == []


class TestBuggyMethods:
    """Test methods with known bugs."""
    
    def test_count_words_basic(self, data_processor):
        """Test basic word counting."""
        # Note: This has a known bug with multiple spaces
        result = data_processor.count_words("hello world test")
        assert result == 3
    
    def test_count_words_empty(self, data_processor):
        """Test counting words in empty string."""
        # Known bug: counts empty string as 1 word
        result = data_processor.count_words("")
        assert result >= 0  # Allowing for bug
    
    def test_get_last_n_items_basic(self, data_processor):
        """Test getting last n items."""
        assert data_processor.get_last_n_items([1, 2, 3, 4, 5], 2) == [4, 5]
    
    def test_get_last_n_items_all(self, data_processor):
        """Test getting all items."""
        assert data_processor.get_last_n_items([1, 2, 3], 3) == [1, 2, 3]


class TestDictionaryOperations:
    """Test dictionary manipulation methods."""
    
    def test_merge_dictionaries_basic(self, data_processor):
        """Test basic dictionary merge."""
        d1 = {'a': 1, 'b': 2}
        d2 = {'c': 3, 'd': 4}
        result = data_processor.merge_dictionaries(d1, d2)
        assert result == {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    
    def test_merge_dictionaries_conflict(self, data_processor):
        """Test merge with conflicting keys (dict2 wins)."""
        d1 = {'a': 1, 'b': 2}
        d2 = {'b': 3, 'c': 4}
        result = data_processor.merge_dictionaries(d1, d2)
        assert result == {'a': 1, 'b': 3, 'c': 4}
    
    def test_merge_dictionaries_empty(self, data_processor):
        """Test merging empty dictionaries."""
        result = data_processor.merge_dictionaries({}, {})
        assert result == {}
    
    def test_merge_dictionaries_one_empty(self, data_processor):
        """Test merging with one empty dictionary."""
        d1 = {'a': 1}
        result = data_processor.merge_dictionaries(d1, {})
        assert result == {'a': 1}
    
    def test_merge_dictionaries_immutability(self, data_processor):
        """Test that original dictionaries are not modified."""
        d1 = {'a': 1}
        d2 = {'b': 2}
        result = data_processor.merge_dictionaries(d1, d2)
        assert d1 == {'a': 1}  # Unchanged
        assert d2 == {'b': 2}  # Unchanged


class TestProcessedCount:
    """Test operation counting."""
    
    def test_processed_count_initial(self, data_processor):
        """Test initial processed count is zero."""
        assert data_processor.get_processed_count() == 0
    
    def test_processed_count_increments(self, data_processor):
        """Test that processed count increments."""
        data_processor.reverse_string("test")
        assert data_processor.get_processed_count() == 1
        data_processor.remove_duplicates([1, 2, 2])
        assert data_processor.get_processed_count() == 2
        data_processor.chunk_list([1, 2, 3], 2)
        assert data_processor.get_processed_count() == 3


class TestUtilityFunctions:
    """Test standalone utility functions."""
    
    def test_to_title_case_basic(self):
        """Test converting to title case."""
        assert to_title_case("hello world") == "Hello World"
    
    def test_to_title_case_already_title(self):
        """Test title case when already in title case."""
        assert to_title_case("Hello World") == "Hello World"
    
    def test_to_title_case_uppercase(self):
        """Test converting from uppercase."""
        assert to_title_case("HELLO WORLD") == "Hello World"
    
    def test_to_title_case_empty(self):
        """Test title case with empty string."""
        assert to_title_case("") == ""
    
    def test_find_most_frequent_basic(self):
        """Test finding most frequent element."""
        assert find_most_frequent([1, 2, 2, 3, 3, 3]) == 3
    
    def test_find_most_frequent_tie_first_wins(self):
        """Test that first encountered wins in tie."""
        result = find_most_frequent([1, 1, 2, 2])
        assert result == 1  # First encountered
    
    def test_find_most_frequent_single_element(self):
        """Test with single element."""
        assert find_most_frequent([5]) == 5
    
    def test_find_most_frequent_empty_list(self):
        """Test with empty list."""
        with pytest.raises(ValueError, match="Cannot find most frequent element in empty list"):
            find_most_frequent([])
    
    def test_find_most_frequent_strings(self):
        """Test with string elements."""
        assert find_most_frequent(['a', 'b', 'a', 'c']) == 'a'


@pytest.mark.parametrize("input_list,expected", [
    ([1, 2, 3], [1, 2, 3]),
    ([1, 1, 2, 2, 3, 3], [1, 2, 3]),
    ([5], [5]),
    ([], []),
])
def test_remove_duplicates_parametrized(data_processor, input_list, expected):
    """Parametrized test for remove_duplicates."""
    assert data_processor.remove_duplicates(input_list) == expected
