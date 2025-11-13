"""
Comprehensive tests for the FileHandler module.
"""

import pytest
import os
import json


class TestInitialization:
    """Test FileHandler initialization."""
    
    def test_init_default_path(self):
        """Test initialization with default path."""
        from file_handler import FileHandler
        handler = FileHandler()
        assert handler.base_path == "."
    
    def test_init_custom_path(self, tmp_path):
        """Test initialization with custom path."""
        from file_handler import FileHandler
        handler = FileHandler(str(tmp_path))
        assert handler.base_path == str(tmp_path)
    
    def test_init_empty_processed_files(self, file_handler):
        """Test that processed files list is empty on init."""
        assert file_handler.get_processed_files() == []


class TestTextFileOperations:
    """Test reading and writing text files."""
    
    def test_read_text_file_basic(self, file_handler, tmp_path):
        """Test reading a text file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello World", encoding='utf-8')
        
        content = file_handler.read_text_file("test.txt")
        assert content == "Hello World"
    
    def test_read_text_file_multiline(self, file_handler, tmp_path):
        """Test reading multiline text file."""
        test_file = tmp_path / "multiline.txt"
        test_file.write_text("Line 1\nLine 2\nLine 3", encoding='utf-8')
        
        content = file_handler.read_text_file("multiline.txt")
        assert "Line 1" in content
        assert "Line 2" in content
        assert "Line 3" in content
    
    def test_read_text_file_not_found(self, file_handler):
        """Test reading non-existent file."""
        with pytest.raises(FileNotFoundError, match="File not found"):
            file_handler.read_text_file("nonexistent.txt")
    
    def test_read_text_file_tracks_processed(self, file_handler, tmp_path):
        """Test that reading file adds to processed list."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content", encoding='utf-8')
        
        file_handler.read_text_file("test.txt")
        assert "test.txt" in file_handler.get_processed_files()


class TestJSONFileOperations:
    """Test JSON file operations."""
    
    def test_read_json_file_basic(self, file_handler, tmp_path):
        """Test reading JSON file."""
        test_file = tmp_path / "data.json"
        test_data = {"name": "John", "age": 30}
        test_file.write_text(json.dumps(test_data), encoding='utf-8')
        
        data = file_handler.read_json_file("data.json")
        assert data == test_data
    
    def test_read_json_file_complex(self, file_handler, tmp_path):
        """Test reading complex JSON structure."""
        test_file = tmp_path / "complex.json"
        test_data = {
            "users": [
                {"name": "Alice", "role": "admin"},
                {"name": "Bob", "role": "user"}
            ],
            "settings": {"theme": "dark"}
        }
        test_file.write_text(json.dumps(test_data), encoding='utf-8')
        
        data = file_handler.read_json_file("complex.json")
        assert len(data["users"]) == 2
        assert data["settings"]["theme"] == "dark"
    
    def test_read_json_file_not_found(self, file_handler):
        """Test reading non-existent JSON file."""
        with pytest.raises(FileNotFoundError, match="File not found"):
            file_handler.read_json_file("missing.json")
    
    def test_read_json_file_invalid_json(self, file_handler, tmp_path):
        """Test reading file with invalid JSON."""
        test_file = tmp_path / "invalid.json"
        test_file.write_text("{ invalid json }", encoding='utf-8')
        
        with pytest.raises(ValueError, match="Invalid JSON"):
            file_handler.read_json_file("invalid.json")


class TestFileInfo:
    """Test file information methods."""
    
    def test_get_file_size_basic(self, file_handler, tmp_path):
        """Test getting file size."""
        test_file = tmp_path / "sizeme.txt"
        content = "12345"  # 5 bytes
        test_file.write_text(content, encoding='utf-8')
        
        size = file_handler.get_file_size("sizeme.txt")
        assert size == 5
    
    def test_get_file_size_empty_file(self, file_handler, tmp_path):
        """Test getting size of empty file."""
        test_file = tmp_path / "empty.txt"
        test_file.write_text("", encoding='utf-8')
        
        size = file_handler.get_file_size("empty.txt")
        assert size == 0
    
    def test_get_file_size_not_found(self, file_handler):
        """Test getting size of non-existent file."""
        with pytest.raises(FileNotFoundError, match="File not found"):
            file_handler.get_file_size("missing.txt")


class TestSecureFileOperations:
    """Test secure file reading with path validation."""
    
    def test_read_file_safe_basic(self, file_handler, tmp_path):
        """Test safe file reading."""
        test_file = tmp_path / "safe.txt"
        test_file.write_text("Safe content", encoding='utf-8')
        
        content = file_handler.read_file_safe("safe.txt")
        assert content == "Safe content"
    
    def test_read_file_safe_path_traversal_blocked(self, file_handler):
        """Test that path traversal is blocked."""
        with pytest.raises(ValueError, match="Access denied: Path traversal detected"):
            file_handler.read_file_safe("../../../etc/passwd")
    
    def test_read_file_safe_absolute_path_blocked(self, file_handler):
        """Test that absolute paths outside base_path are blocked."""
        with pytest.raises(ValueError, match="Access denied"):
            file_handler.read_file_safe("/etc/passwd")
    
    def test_read_file_safe_not_found(self, file_handler):
        """Test safe reading of non-existent file."""
        with pytest.raises(FileNotFoundError, match="File not found"):
            file_handler.read_file_safe("missing.txt")


class TestAppendOperations:
    """Test appending to files."""
    
    def test_append_to_file_new_file(self, file_handler, tmp_path):
        """Test appending creates new file if not exists."""
        # Note: append mode creates file if it doesn't exist
        file_handler.append_to_file("newfile.txt", "First line\n")
        
        test_file = tmp_path / "newfile.txt"
        assert test_file.exists()
        assert "First line" in test_file.read_text(encoding='utf-8')
    
    def test_append_to_file_existing(self, file_handler, tmp_path):
        """Test appending to existing file."""
        test_file = tmp_path / "append.txt"
        test_file.write_text("Line 1\n", encoding='utf-8')
        
        file_handler.append_to_file("append.txt", "Line 2\n")
        
        content = test_file.read_text(encoding='utf-8')
        assert "Line 1" in content
        assert "Line 2" in content
    
    def test_append_to_file_tracks_processed(self, file_handler, tmp_path):
        """Test that appending tracks in processed files."""
        test_file = tmp_path / "track.txt"
        test_file.write_text("", encoding='utf-8')
        
        file_handler.append_to_file("track.txt", "content")
        assert "track.txt" in file_handler.get_processed_files()


class TestDeleteOperations:
    """Test file deletion."""
    
    def test_delete_file_basic(self, file_handler, tmp_path):
        """Test deleting a file."""
        test_file = tmp_path / "delete_me.txt"
        test_file.write_text("Delete this", encoding='utf-8')
        
        result = file_handler.delete_file("delete_me.txt")
        assert result == True
        assert not test_file.exists()
    
    def test_delete_file_not_found(self, file_handler):
        """Test deleting non-existent file."""
        with pytest.raises(FileNotFoundError, match="File not found"):
            file_handler.delete_file("nonexistent.txt")
    
    def test_delete_file_path_traversal_blocked(self, file_handler):
        """Test that path traversal is blocked in delete."""
        with pytest.raises(ValueError, match="Access denied"):
            file_handler.delete_file("../../../etc/passwd")
    
    def test_delete_file_tracks_processed(self, file_handler, tmp_path):
        """Test that deleting tracks in processed files."""
        test_file = tmp_path / "track_delete.txt"
        test_file.write_text("", encoding='utf-8')
        
        file_handler.delete_file("track_delete.txt")
        assert "track_delete.txt" in file_handler.get_processed_files()


class TestProcessedFilesList:
    """Test processed files tracking."""
    
    def test_get_processed_files_returns_copy(self, file_handler, tmp_path):
        """Test that get_processed_files returns a copy."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content", encoding='utf-8')
        
        file_handler.read_text_file("test.txt")
        processed = file_handler.get_processed_files()
        processed.append("fake.txt")
        
        # Original list should be unchanged
        assert "fake.txt" not in file_handler.get_processed_files()
    
    def test_multiple_operations_tracked(self, file_handler, tmp_path):
        """Test that multiple operations are tracked."""
        # Create test files
        file1 = tmp_path / "file1.txt"
        file1.write_text("content1", encoding='utf-8')
        file2 = tmp_path / "file2.txt"
        file2.write_text("content2", encoding='utf-8')
        
        file_handler.read_text_file("file1.txt")
        file_handler.read_text_file("file2.txt")
        
        processed = file_handler.get_processed_files()
        assert len(processed) == 2
        assert "file1.txt" in processed
        assert "file2.txt" in processed


class TestCountLines:
    """Test line counting functionality."""
    
    def test_count_lines_single_line(self, file_handler, tmp_path):
        """Test counting lines in single-line file."""
        test_file = tmp_path / "single.txt"
        test_file.write_text("One line", encoding='utf-8')
        
        count = file_handler.count_lines("single.txt")
        assert count == 1
    
    def test_count_lines_multiple_lines(self, file_handler, tmp_path):
        """Test counting multiple lines."""
        test_file = tmp_path / "multi.txt"
        test_file.write_text("Line 1\nLine 2\nLine 3\n", encoding='utf-8')
        
        count = file_handler.count_lines("multi.txt")
        assert count == 3
    
    def test_count_lines_empty_file(self, file_handler, tmp_path):
        """Test counting lines in empty file."""
        test_file = tmp_path / "empty.txt"
        test_file.write_text("", encoding='utf-8')
        
        count = file_handler.count_lines("empty.txt")
        assert count == 0


@pytest.mark.parametrize("filename,content,expected_size", [
    ("small.txt", "Hi", 2),
    ("medium.txt", "Hello World", 11),
    ("empty.txt", "", 0),
])
def test_file_size_parametrized(file_handler, tmp_path, filename, content, expected_size):
    """Parametrized test for file sizes."""
    test_file = tmp_path / filename
    test_file.write_text(content, encoding='utf-8')
    
    size = file_handler.get_file_size(filename)
    assert size == expected_size
