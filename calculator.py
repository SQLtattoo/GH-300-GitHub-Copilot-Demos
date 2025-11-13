"""
Calculator module for demonstrating GitHub Copilot capabilities.
This module contains basic arithmetic operations and demonstrates:
- Inline suggestions
- Comment-driven development
- Function completion
"""

import math


class Calculator:
    """A simple calculator class with basic arithmetic operations."""
    
    def __init__(self):
        """Initialize the calculator with operation history."""
        self.history = []
    
    def add(self, a: float, b: float) -> float:
        """Add two numbers and return the result."""
        result = a + b
        self.history.append(f"add({a}, {b}) = {result}")
        return result
    
    def subtract(self, a: float, b: float) -> float:
        """Subtract b from a and return the result."""
        result = a - b
        self.history.append(f"subtract({a}, {b}) = {result}")
        return result
    
    # TODO: Implement multiply method that takes two numbers and returns their product
    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers and return the result."""
        result = a * b
        self.history.append(f"multiply({a}, {b}) = {result}")
        return result
    
    # This is intentionally left incomplete to demonstrate Copilot's code completion

    
    # TODO: Implement divide method that takes two numbers and returns their quotient
    def divide(self, a: float, b: float) -> float:
        """Divide a by b and return the result."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self.history.append(f"divide({a}, {b}) = {result}")
        return result
    # Should handle division by zero appropriately
    
    def power(self, base: float, exponent: float) -> float:
        """Calculate base raised to the power of exponent."""
        result = base ** exponent
        self.history.append(f"power({base}, {exponent}) = {result}")
        return result
    
    def percentage(self, value: float, total: float) -> float:
        """Calculate what percentage 'value' is of 'total'."""
        if total == 0:
            raise ValueError("Total cannot be zero")
        result = (value / total) * 100
        self.history.append(f"percentage({value}, {total}) = {result}%")
        return result
    
    # TODO: Create a method called 'square_root' that calculates the square root of a number
    def square_root(self, value: float) -> float:
        """Calculate the square root of a number."""
        if value < 0:
            raise ValueError("Cannot calculate square root of negative number")
        result = value ** 0.5
        self.history.append(f"square_root({value}) = {result}")
        return result
    # It should handle negative numbers by raising a ValueError
    
    def get_history(self) -> list:
        """Return the history of all operations performed."""
        return self.history.copy()
    
    def clear_history(self) -> None:
        """Clear the operation history."""
        self.history.clear()
    
    # BUG: This method doesn't handle empty list - will crash with ZeroDivisionError!
    
    def average(self, numbers: list) -> float:
        """Calculate the average of a list of numbers."""
        if not numbers:
            raise ValueError("Cannot calculate average of empty list")
        return sum(numbers) / len(numbers)
    
    def calculate_circle_area(self, radius: float) -> float:
        """Calculate the area of a circle using math.pi for precision."""
        result = math.pi * radius ** 2
        self.history.append(f"circle_area({radius}) = {result}")
        return result
    
    def calculate_circle_circumference(self, radius: float) -> float:
        """Calculate the circumference of a circle using math.pi for precision."""
        result = 2 * math.pi * radius
        self.history.append(f"circle_circumference({radius}) = {result}")
        return result
    
    # MISSING: Type hints, error handling, proper documentation

    def divide_numbers(self, a: float, b: float) -> float:
        """
        Divide two numbers and return the quotient.
        
        This method performs division operation between two floating-point numbers
        with proper error handling for division by zero.
        
        Args:
            a (float): The dividend (number to be divided)
            b (float): The divisor (number to divide by)
        
        Returns:
            float: The quotient of a divided by b
        
        Raises:
            ValueError: If b is zero (division by zero is undefined)
        
        Example:
            >>> calc = Calculator()
            >>> calc.divide_numbers(10, 2)
            5.0
            >>> calc.divide_numbers(7, 2)
            3.5
            >>> calc.divide_numbers(10, 0)
            ValueError: Cannot divide by zero
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def complex_calculation(self, x: float, y: float, z: float) -> float:
        """
        Perform a complex calculation: (x + y) * z - (x / y).
        
        Args:
            x (float): First operand
            y (float): Second operand (used as divisor)
            z (float): Third operand (multiplier)
        
        Returns:
            float: Result of the complex calculation
        """
        if y == 0:
            return (x + y) * z
        result = (x + y) * z - (x / y)
        self.history.append(f"complex_calculation({x}, {y}, {z}) = {result}")
        return result
    
    # UNTESTED: This method exists but has no tests - demonstrate test generation
    def modulo(self, a: float, b: float) -> float:
        """Calculate modulo operation."""
        if b == 0:
            raise ValueError("Modulo by zero is undefined")
        result = a % b
        self.history.append(f"modulo({a}, {b}) = {result}")
        return result
    
    # BUG: Doesn't handle edge cases properly
    def get_first_element(self, items: list):
        """Get the first element from a list."""
        if not items:
            raise ValueError("Cannot get first element of empty list")
        return items[0]
    
    def format_name(self, first_name: str, last_name: str) -> str:
        """
        Format a person's full name with proper validation.
        
        Args:
            first_name (str): Person's first name
            last_name (str): Person's last name
            
        Returns:
            str: Formatted full name with single space between names
            
        Raises:
            ValueError: If either name is None, empty, or contains only whitespace
        """
        # Validate inputs are not None
        if first_name is None or last_name is None:
            raise ValueError("First name and last name cannot be None")
        
        # Strip whitespace and validate not empty
        first_name = first_name.strip()
        last_name = last_name.strip()
        
        if not first_name or not last_name:
            raise ValueError("First name and last name cannot be empty or whitespace only")
        
        return f"{first_name} {last_name}"


# TODO: Create a function called 'factorial' that calculates the factorial of a non-negative integer
# It should raise ValueError for negative numbers


# TODO: Create a function called 'is_prime' that checks if a number is prime
# Return True if prime, False otherwise


# TODO: Create a function called 'fibonacci' that generates the first n Fibonacci numbers
# Return as a list


# TODO: Create a function that converts temperature from Celsius to Fahrenheit
# Formula: F = (C * 9/5) + 32
