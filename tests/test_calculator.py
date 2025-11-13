"""
Comprehensive tests for the Calculator module.
"""

import pytest
import math


class TestBasicOperations:
    """Test basic arithmetic operations."""
    
    def test_add_positive_numbers(self, calculator):
        """Test adding two positive numbers."""
        assert calculator.add(5, 3) == 8
    
    def test_add_negative_numbers(self, calculator):
        """Test adding negative numbers."""
        assert calculator.add(-5, -3) == -8
    
    def test_add_mixed_signs(self, calculator):
        """Test adding numbers with different signs."""
        assert calculator.add(5, -3) == 2
        assert calculator.add(-5, 3) == -2
    
    def test_add_with_zero(self, calculator):
        """Test adding with zero."""
        assert calculator.add(5, 0) == 5
        assert calculator.add(0, 5) == 5
    
    def test_add_floats(self, calculator):
        """Test adding floating point numbers."""
        assert calculator.add(1.5, 2.5) == 4.0
    
    def test_subtract_positive_numbers(self, calculator):
        """Test subtracting positive numbers."""
        assert calculator.subtract(10, 4) == 6
    
    def test_subtract_negative_result(self, calculator):
        """Test subtraction resulting in negative number."""
        assert calculator.subtract(3, 5) == -2
    
    def test_subtract_with_zero(self, calculator):
        """Test subtraction with zero."""
        assert calculator.subtract(5, 0) == 5
        assert calculator.subtract(0, 5) == -5
    
    def test_multiply_positive_numbers(self, calculator):
        """Test multiplying positive numbers."""
        assert calculator.multiply(3, 4) == 12
    
    def test_multiply_by_zero(self, calculator):
        """Test multiplication by zero."""
        assert calculator.multiply(5, 0) == 0
        assert calculator.multiply(0, 5) == 0
    
    def test_multiply_negative_numbers(self, calculator):
        """Test multiplying negative numbers."""
        assert calculator.multiply(-3, -4) == 12
        assert calculator.multiply(-3, 4) == -12
    
    def test_divide_positive_numbers(self, calculator):
        """Test dividing positive numbers."""
        assert calculator.divide(10, 2) == 5
    
    def test_divide_by_zero(self, calculator):
        """Test that dividing by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calculator.divide(10, 0)
    
    def test_divide_floats(self, calculator):
        """Test division with floating point numbers."""
        assert calculator.divide(7, 2) == 3.5
    
    def test_divide_numbers_method(self, calculator):
        """Test the divide_numbers method."""
        assert calculator.divide_numbers(10, 2) == 5.0
    
    def test_divide_numbers_by_zero(self, calculator):
        """Test divide_numbers with zero divisor."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calculator.divide_numbers(10, 0)


class TestAdvancedOperations:
    """Test advanced mathematical operations."""
    
    def test_power_positive_exponent(self, calculator):
        """Test power with positive exponent."""
        assert calculator.power(2, 3) == 8
    
    def test_power_zero_exponent(self, calculator):
        """Test power with zero exponent."""
        assert calculator.power(5, 0) == 1
    
    def test_power_negative_exponent(self, calculator):
        """Test power with negative exponent."""
        assert calculator.power(2, -2) == 0.25
    
    def test_power_fractional_exponent(self, calculator):
        """Test power with fractional exponent."""
        assert calculator.power(4, 0.5) == 2.0
    
    def test_percentage_basic(self, calculator):
        """Test basic percentage calculation."""
        assert calculator.percentage(25, 200) == 12.5
    
    def test_percentage_100_percent(self, calculator):
        """Test 100% calculation."""
        assert calculator.percentage(50, 50) == 100.0
    
    def test_percentage_zero_total(self, calculator):
        """Test percentage with zero total."""
        with pytest.raises(ValueError, match="Total cannot be zero"):
            calculator.percentage(10, 0)
    
    def test_square_root_positive(self, calculator):
        """Test square root of positive number."""
        assert calculator.square_root(16) == 4.0
    
    def test_square_root_zero(self, calculator):
        """Test square root of zero."""
        assert calculator.square_root(0) == 0.0
    
    def test_square_root_negative(self, calculator):
        """Test square root of negative number raises error."""
        with pytest.raises(ValueError, match="Cannot calculate square root of negative number"):
            calculator.square_root(-4)
    
    def test_modulo_basic(self, calculator):
        """Test modulo operation."""
        assert calculator.modulo(10, 3) == 1
    
    def test_modulo_by_zero(self, calculator):
        """Test modulo by zero raises error."""
        with pytest.raises(ValueError, match="Modulo by zero is undefined"):
            calculator.modulo(10, 0)


class TestCircleOperations:
    """Test circle-related calculations."""
    
    def test_circle_area(self, calculator):
        """Test circle area calculation."""
        result = calculator.calculate_circle_area(5)
        expected = math.pi * 25
        assert abs(result - expected) < 0.0001
    
    def test_circle_circumference(self, calculator):
        """Test circle circumference calculation."""
        result = calculator.calculate_circle_circumference(5)
        expected = 2 * math.pi * 5
        assert abs(result - expected) < 0.0001
    
    def test_circle_area_zero_radius(self, calculator):
        """Test circle area with zero radius."""
        assert calculator.calculate_circle_area(0) == 0


class TestDataOperations:
    """Test operations on collections."""
    
    def test_average_positive_numbers(self, calculator):
        """Test average of positive numbers."""
        assert calculator.average([1, 2, 3, 4, 5]) == 3.0
    
    def test_average_single_number(self, calculator):
        """Test average of single number."""
        assert calculator.average([5]) == 5.0
    
    def test_average_empty_list(self, calculator):
        """Test average of empty list raises error."""
        with pytest.raises(ValueError, match="Cannot calculate average of empty list"):
            calculator.average([])
    
    def test_average_negative_numbers(self, calculator):
        """Test average with negative numbers."""
        assert calculator.average([-1, -2, -3]) == -2.0
    
    def test_get_first_element_valid(self, calculator):
        """Test getting first element from list."""
        assert calculator.get_first_element([1, 2, 3]) == 1
    
    def test_get_first_element_empty_list(self, calculator):
        """Test getting first element from empty list."""
        with pytest.raises(ValueError, match="Cannot get first element of empty list"):
            calculator.get_first_element([])


class TestStringOperations:
    """Test string formatting operations."""
    
    def test_format_name_valid(self, calculator):
        """Test formatting valid names."""
        assert calculator.format_name("John", "Doe") == "John Doe"
    
    def test_format_name_with_whitespace(self, calculator):
        """Test formatting names with extra whitespace."""
        assert calculator.format_name("  John  ", "  Doe  ") == "John Doe"
    
    def test_format_name_none_first_name(self, calculator):
        """Test formatting with None first name."""
        with pytest.raises(ValueError, match="First name and last name cannot be None"):
            calculator.format_name(None, "Doe")
    
    def test_format_name_none_last_name(self, calculator):
        """Test formatting with None last name."""
        with pytest.raises(ValueError, match="First name and last name cannot be None"):
            calculator.format_name("John", None)
    
    def test_format_name_empty_string(self, calculator):
        """Test formatting with empty strings."""
        with pytest.raises(ValueError, match="First name and last name cannot be empty or whitespace only"):
            calculator.format_name("", "Doe")
    
    def test_format_name_whitespace_only(self, calculator):
        """Test formatting with whitespace-only strings."""
        with pytest.raises(ValueError, match="First name and last name cannot be empty or whitespace only"):
            calculator.format_name("   ", "Doe")


class TestComplexCalculations:
    """Test complex calculation methods."""
    
    def test_complex_calculation_basic(self, calculator):
        """Test basic complex calculation."""
        result = calculator.complex_calculation(2, 4, 3)
        # (2 + 4) * 3 - (2 / 4) = 6 * 3 - 0.5 = 17.5
        assert result == 17.5
    
    def test_complex_calculation_zero_y(self, calculator):
        """Test complex calculation with y=0."""
        result = calculator.complex_calculation(2, 0, 3)
        # (2 + 0) * 3 = 6 (division skipped)
        assert result == 6


class TestHistory:
    """Test operation history tracking."""
    
    def test_history_empty_on_init(self, calculator):
        """Test that history is empty on initialization."""
        assert calculator.get_history() == []
    
    def test_history_records_operations(self, calculator):
        """Test that history records operations."""
        calculator.add(5, 3)
        calculator.multiply(2, 4)
        history = calculator.get_history()
        assert len(history) == 2
        assert "add(5, 3) = 8" in history[0]
        assert "multiply(2, 4) = 8" in history[1]
    
    def test_clear_history(self, calculator):
        """Test clearing history."""
        calculator.add(5, 3)
        calculator.clear_history()
        assert calculator.get_history() == []
    
    def test_history_returns_copy(self, calculator):
        """Test that get_history returns a copy."""
        calculator.add(5, 3)
        history = calculator.get_history()
        history.append("fake entry")
        # Original history should be unchanged
        assert len(calculator.get_history()) == 1


@pytest.mark.parametrize("a,b,expected", [
    (0, 0, 0),
    (1, 1, 2),
    (-1, -1, -2),
    (100, 200, 300),
    (0.1, 0.2, 0.3),
])
def test_add_parametrized(calculator, a, b, expected):
    """Parametrized test for addition with various inputs."""
    result = calculator.add(a, b)
    assert abs(result - expected) < 0.0001  # Handle floating point precision
