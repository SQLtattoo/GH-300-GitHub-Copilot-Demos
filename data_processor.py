"""
Data processor module for string and list operations.
Demonstrates Copilot's ability to work with data structures.
"""

import ast
import re


class DataProcessor:
    """Handles various data processing operations."""
    
    def __init__(self):
        """Initialize the data processor."""
        self.processed_count = 0
    
    def reverse_string(self, text: str) -> str:
        """Reverse a string."""
        self.processed_count += 1
        return text[::-1]
    
    # TODO: Create a method that checks if a string is a palindrome
    # Should ignore case and spaces
    
    # TODO: Create a method that counts the number of vowels in a string
    # Should handle both uppercase and lowercase
    
    def remove_duplicates(self, items: list) -> list:
        """Remove duplicate items from a list while preserving order."""
        self.processed_count += 1
        seen = set()
        result = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
    
    # TODO: Create a method called 'find_common_elements' that finds common elements between two lists
    
    # TODO: Create a method that sorts a list of dictionaries by a specified key
    
    def chunk_list(self, items: list, chunk_size: int) -> list:
        """Split a list into chunks of specified size."""
        if chunk_size <= 0:
            raise ValueError("Chunk size must be positive")
        self.processed_count += 1
        return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]
    
    # TODO: Create a method that flattens a nested list structure
    # Example: [[1, 2], [3, [4, 5]]] -> [1, 2, 3, 4, 5]
    
    def get_processed_count(self) -> int:
        """Return the number of operations processed."""
        return self.processed_count
    
    # BUG: Doesn't handle edge cases properly
    def count_words(self, text: str) -> int:
        """Count words in a text."""
        # BUG: Counts empty strings and multiple spaces incorrectly
        return len(text.split(' '))
    
    # PERFORMANCE ISSUE: O(n²) complexity - should use set for O(n)
    def find_duplicates_slow(self, items: list) -> list:
        """Find duplicate items in a list (inefficient version)."""
        # PERFORMANCE: This is O(n²) and could be much faster
        duplicates = []
        for i, item in enumerate(items):
            for j, other in enumerate(items):
                if i != j and item == other and item not in duplicates:
                    duplicates.append(item)
        return duplicates
    
    def process_data(self, data: list) -> list:
        """
        Process data by doubling each element.
        
        Args:
            data (list): List of numeric values to process
        
        Returns:
            list: New list with each element doubled
        
        Raises:
            TypeError: If data is not iterable or contains non-numeric values
        
        Example:
            >>> processor = DataProcessor()
            >>> processor.process_data([1, 2, 3])
            [2, 4, 6]
        """
        if not hasattr(data, '__iter__'):
            raise TypeError("Data must be iterable")
        result = []
        for x in data:
            try:
                result.append(x * 2)
            except TypeError:
                raise TypeError("All elements must support multiplication")
        return result
    
    def calculate_expression(self, expression: str) -> float:
        """
        Calculate a mathematical expression from string.
        
        Only supports basic arithmetic operations (+, -, *, /, parentheses).
        Uses safe parsing instead of eval to prevent code injection.
        
        Args:
            expression (str): Mathematical expression to evaluate
            
        Returns:
            float: Result of the calculation
            
        Raises:
            ValueError: If expression contains invalid characters or syntax
        """
        # Remove whitespace
        expression = expression.replace(' ', '')
        
        # Validate expression contains only safe characters
        if not re.match(r'^[0-9+\-*/().\s]+$', expression):
            raise ValueError("Expression contains invalid characters. Only numbers and +, -, *, /, () are allowed.")
        
        try:
            # Use ast.literal_eval for simple numeric literals, or compile and evaluate safely
            # For basic arithmetic, we parse the AST and evaluate only math operations
            tree = ast.parse(expression, mode='eval')
            return self._eval_expr(tree.body)
        except SyntaxError as e:
            raise ValueError(f"Invalid expression: {e}")
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Invalid expression: {e}")
    
    def _eval_expr(self, node):
        """
        Safely evaluate an AST node containing only arithmetic operations.
        
        Args:
            node: AST node to evaluate (ast.Num, ast.BinOp, ast.UnaryOp, or ast.Constant)
        
        Returns:
            float: The evaluated result of the expression
        
        Raises:
            ValueError: If node contains unsupported operations or expression types
        """
        if isinstance(node, ast.Num):  # <number>
            return node.n
        elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
            left = self._eval_expr(node.left)
            right = self._eval_expr(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            elif isinstance(node.op, ast.Sub):
                return left - right
            elif isinstance(node.op, ast.Mult):
                return left * right
            elif isinstance(node.op, ast.Div):
                if right == 0:
                    raise ValueError("Division by zero")
                return left / right
            else:
                raise ValueError(f"Unsupported operation: {type(node.op).__name__}")
        elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
            operand = self._eval_expr(node.operand)
            if isinstance(node.op, ast.USub):
                return -operand
            elif isinstance(node.op, ast.UAdd):
                return +operand
            else:
                raise ValueError(f"Unsupported unary operation: {type(node.op).__name__}")
        elif isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        else:
            raise ValueError(f"Unsupported expression type: {type(node).__name__}")
    
    # BUG: Edge case not handled
    def get_last_n_items(self, items: list, n: int) -> list:
        """Get the last n items from a list."""
        # BUG: Doesn't handle when n > len(items)
        # BUG: Doesn't handle negative n values
        return items[-n:]
    
    def merge_dictionaries(self, dict1: dict, dict2: dict) -> dict:
        """
        Merge two dictionaries, with dict2 values overwriting dict1 on key conflicts.
        
        Creates a new dictionary containing all keys from both input dictionaries.
        If a key exists in both dictionaries, the value from dict2 takes precedence.
        
        Args:
            dict1 (dict): First dictionary to merge
            dict2 (dict): Second dictionary to merge (takes precedence on conflicts)
        
        Returns:
            dict: New dictionary containing merged key-value pairs
        
        Example:
            >>> processor = DataProcessor()
            >>> d1 = {'a': 1, 'b': 2}
            >>> d2 = {'b': 3, 'c': 4}
            >>> processor.merge_dictionaries(d1, d2)
            {'a': 1, 'b': 3, 'c': 4}
        """
        result = dict1.copy()
        result.update(dict2)
        return result


def to_title_case(text: str) -> str:
    """
    Convert a string to title case.
    
    Capitalizes the first letter of each word and converts all other letters to lowercase.
    
    Args:
        text (str): The string to convert to title case
    
    Returns:
        str: The string converted to title case
    
    Example:
        >>> to_title_case("hello world")
        'Hello World'
        >>> to_title_case("HELLO world")
        'Hello World'
    """
    return text.title()


def find_most_frequent(items: list):
    """
    Find the most frequent element in a list.
    
    If there's a tie, returns the first one encountered.
    
    Args:
        items (list): List of items to analyze
    
    Returns:
        The most frequent element in the list
    
    Raises:
        ValueError: If the list is empty
    
    Example:
        >>> find_most_frequent([1, 2, 2, 3, 3, 3])
        3
        >>> find_most_frequent(['a', 'b', 'a', 'c'])
        'a'
    """
    if not items:
        raise ValueError("Cannot find most frequent element in empty list")
    
    frequency = {}
    for item in items:
        frequency[item] = frequency.get(item, 0) + 1
    
    max_count = 0
    most_frequent = None
    
    for item in items:
        if frequency[item] > max_count:
            max_count = frequency[item]
            most_frequent = item
    
    return most_frequent
