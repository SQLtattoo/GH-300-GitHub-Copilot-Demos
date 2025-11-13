"""
File handler module for file I/O operations.
Demonstrates Copilot's ability with file handling and error management.
"""

import json
import os
from typing import List, Dict, Any


class FileHandler:
    """Handles file reading and writing operations."""
    
    def __init__(self, base_path: str = "."):
        """Initialize with a base path for file operations."""
        self.base_path = base_path
        self.files_processed = []
    
    def read_text_file(self, filename: str) -> str:
        """Read and return contents of a text file."""
        filepath = os.path.join(self.base_path, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            self.files_processed.append(filename)
            return content
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filepath}")
    
    # TODO: Create a method that writes text to a file
    # Should create parent directories if they don't exist
    
    def read_json_file(self, filename: str) -> Dict[str, Any]:
        """Read and parse a JSON file."""
        filepath = os.path.join(self.base_path, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.files_processed.append(filename)
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filepath}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in file: {filepath}")
    
    # TODO: Create a method that writes data to a JSON file
    # Should format it nicely with indentation
    
    # TODO: Create a method that counts the number of lines in a text file
    
    # TODO: Create a method that searches for a specific string in a file
    # Return line numbers where the string appears
    
    def get_file_size(self, filename: str) -> int:
        """Return the size of a file in bytes."""
        filepath = os.path.join(self.base_path, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        return os.path.getsize(filepath)
    
    # TODO: Create a method that lists all files in a directory with a specific extension
    
    def get_processed_files(self) -> List[str]:
        """Return list of files that have been processed."""
        return self.files_processed.copy()
    
    def read_file_safe(self, filename: str) -> str:
        """
        Read a file with proper path validation.
        
        Validates that the requested file is within the base_path directory
        to prevent directory traversal attacks.
        
        Args:
            filename (str): Name of the file to read (relative to base_path)
            
        Returns:
            str: Contents of the file
            
        Raises:
            ValueError: If path traversal is attempted
            FileNotFoundError: If file doesn't exist
        """
        # Use os.path.join for cross-platform compatibility
        filepath = os.path.join(self.base_path, filename)
        
        # Resolve to absolute path and validate it's within base_path
        abs_base = os.path.abspath(self.base_path)
        abs_filepath = os.path.abspath(filepath)
        
        # Check if the resolved path is within base_path
        if not abs_filepath.startswith(abs_base + os.sep) and abs_filepath != abs_base:
            raise ValueError(f"Access denied: Path traversal detected. File must be within {abs_base}")
        
        # Check file exists
        if not os.path.exists(abs_filepath):
            raise FileNotFoundError(f"File not found: {filename}")
        
        try:
            with open(abs_filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            self.files_processed.append(filename)
            return content
        except Exception as e:
            raise IOError(f"Error reading file {filename}: {e}")
    
    # BUG: Doesn't handle binary files properly
    def count_lines(self, filename: str) -> int:
        """Count lines in a file."""
        # BUG: Doesn't specify encoding, may fail on some files
        # TODO: Add error handling
        filepath = os.path.join(self.base_path, filename)
        with open(filepath, 'r') as f:
            return len(f.readlines())
    
    def append_to_file(self, filename: str, content: str) -> None:
        """
        Append content to a file.
        
        Args:
            filename (str): Name of the file to append to (relative to base_path)
            content (str): Content to append to the file
        
        Raises:
            FileNotFoundError: If the file doesn't exist
            IOError: If there's an error writing to the file
        
        Example:
            >>> handler = FileHandler()
            >>> handler.append_to_file('log.txt', 'New log entry\n')
        """
        filepath = os.path.join(self.base_path, filename)
        try:
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(content)
            self.files_processed.append(filename)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filepath}")
        except Exception as e:
            raise IOError(f"Error appending to file {filename}: {e}")
    
    def delete_file(self, filename: str) -> bool:
        """
        Delete a file safely within the base path.
        
        Args:
            filename (str): Name of the file to delete (relative to base_path)
        
        Returns:
            bool: True if file was successfully deleted, False otherwise
        
        Raises:
            ValueError: If path traversal is attempted
            FileNotFoundError: If the file doesn't exist
        
        Example:
            >>> handler = FileHandler()
            >>> handler.delete_file('temp.txt')
            True
        """
        filepath = os.path.join(self.base_path, filename)
        
        # Validate path is within base_path (prevent path traversal)
        abs_base = os.path.abspath(self.base_path)
        abs_filepath = os.path.abspath(filepath)
        
        if not abs_filepath.startswith(abs_base + os.sep) and abs_filepath != abs_base:
            raise ValueError(f"Access denied: Cannot delete files outside base path {abs_base}")
        
        if not os.path.exists(abs_filepath):
            raise FileNotFoundError(f"File not found: {filename}")
        
        try:
            os.remove(abs_filepath)
            self.files_processed.append(filename)
            return True
        except OSError as e:
            raise IOError(f"Error deleting file {filename}: {e}")


# TODO: Create a function that copies a file from source to destination
# Should handle errors appropriately


# TODO: Create a function that reads a CSV file and returns data as a list of dictionaries
