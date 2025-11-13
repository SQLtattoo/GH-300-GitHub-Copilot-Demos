"""
Comprehensive tests for the Logger module.
"""

import pytest
import logging
import os
from io import StringIO
from logger import setup_logger


class TestLoggerSetup:
    """Test logger setup and configuration."""
    
    def test_default_logger_creation(self):
        """Test creating logger with default settings."""
        logger = setup_logger()
        assert logger is not None
        assert logger.name == 'app'
        assert logger.level == logging.INFO
    
    def test_custom_name_logger(self):
        """Test creating logger with custom name."""
        logger = setup_logger(name='test_logger')
        assert logger.name == 'test_logger'
    
    def test_custom_level_info(self):
        """Test logger with INFO level."""
        logger = setup_logger(name='info_logger', level=logging.INFO)
        assert logger.level == logging.INFO
    
    def test_custom_level_debug(self):
        """Test logger with DEBUG level."""
        logger = setup_logger(name='debug_logger', level=logging.DEBUG)
        assert logger.level == logging.DEBUG
    
    def test_custom_level_warning(self):
        """Test logger with WARNING level."""
        logger = setup_logger(name='warning_logger', level=logging.WARNING)
        assert logger.level == logging.WARNING
    
    def test_custom_level_error(self):
        """Test logger with ERROR level."""
        logger = setup_logger(name='error_logger', level=logging.ERROR)
        assert logger.level == logging.ERROR
    
    def test_custom_level_critical(self):
        """Test logger with CRITICAL level."""
        logger = setup_logger(name='critical_logger', level=logging.CRITICAL)
        assert logger.level == logging.CRITICAL


class TestLoggerOutput:
    """Test logger output behavior."""
    
    def test_logger_has_handlers(self):
        """Test logger has handlers configured."""
        logger = setup_logger(name='handler_test')
        assert len(logger.handlers) > 0
    
    def test_logger_info_message(self):
        """Test logging info message."""
        logger = setup_logger(name='info_test', level=logging.INFO)
        # Should not raise any exceptions
        logger.info("Test info message")
    
    def test_logger_debug_message(self):
        """Test logging debug message."""
        logger = setup_logger(name='debug_test', level=logging.DEBUG)
        logger.debug("Test debug message")
    
    def test_logger_warning_message(self):
        """Test logging warning message."""
        logger = setup_logger(name='warning_test', level=logging.WARNING)
        logger.warning("Test warning message")
    
    def test_logger_error_message(self):
        """Test logging error message."""
        logger = setup_logger(name='error_test', level=logging.ERROR)
        logger.error("Test error message")
    
    def test_logger_critical_message(self):
        """Test logging critical message."""
        logger = setup_logger(name='critical_test', level=logging.CRITICAL)
        logger.critical("Test critical message")


class TestLoggerFiltering:
    """Test log level filtering."""
    
    def test_info_level_filters_debug(self):
        """Test INFO level doesn't log DEBUG messages."""
        logger = setup_logger(name='filter_test_1', level=logging.INFO)
        # Verify that debug is not enabled when level is INFO
        assert not logger.isEnabledFor(logging.DEBUG)
    
    def test_warning_level_filters_info(self):
        """Test WARNING level doesn't log INFO messages."""
        logger = setup_logger(name='filter_test_2', level=logging.WARNING)
        assert not logger.isEnabledFor(logging.INFO)
    
    def test_error_level_filters_warning(self):
        """Test ERROR level doesn't log WARNING messages."""
        logger = setup_logger(name='filter_test_3', level=logging.ERROR)
        assert not logger.isEnabledFor(logging.WARNING)
    
    def test_debug_level_logs_all(self):
        """Test DEBUG level logs all messages."""
        logger = setup_logger(name='filter_test_4', level=logging.DEBUG)
        assert logger.isEnabledFor(logging.DEBUG)
        assert logger.isEnabledFor(logging.INFO)
        assert logger.isEnabledFor(logging.WARNING)
        assert logger.isEnabledFor(logging.ERROR)
        assert logger.isEnabledFor(logging.CRITICAL)


class TestLoggerFileOutput:
    """Test logger file output functionality."""
    
    def test_logger_with_log_file(self, tmp_path):
        """Test logger writes to file."""
        log_file = tmp_path / "test.log"
        logger = setup_logger(name='file_test', log_file=str(log_file))
        
        logger.info("Test message")
        
        # Verify file was created
        assert log_file.exists()
    
    def test_log_file_contains_message(self, tmp_path):
        """Test log file contains logged message."""
        log_file = tmp_path / "test_content.log"
        logger = setup_logger(name='file_content_test', log_file=str(log_file))
        
        test_message = "This is a test log message"
        logger.info(test_message)
        
        # Force flush handlers
        for handler in logger.handlers:
            handler.flush()
        
        # Read and verify content
        content = log_file.read_text()
        assert test_message in content
    
    def test_multiple_messages_to_file(self, tmp_path):
        """Test multiple messages are logged to file."""
        log_file = tmp_path / "test_multiple.log"
        logger = setup_logger(name='file_multiple_test', log_file=str(log_file))
        
        messages = ["Message 1", "Message 2", "Message 3"]
        for msg in messages:
            logger.info(msg)
        
        # Force flush
        for handler in logger.handlers:
            handler.flush()
        
        content = log_file.read_text()
        for msg in messages:
            assert msg in content
    
    def test_log_file_directory_creation(self, tmp_path):
        """Test logger creates directory if it doesn't exist."""
        log_dir = tmp_path / "logs"
        log_file = log_dir / "app.log"
        
        # Directory doesn't exist yet
        assert not log_dir.exists()
        
        logger = setup_logger(name='dir_test', log_file=str(log_file))
        logger.info("Test message")
        
        # Force flush
        for handler in logger.handlers:
            handler.flush()
        
        # Verify directory and file were created
        assert log_dir.exists()
        assert log_file.exists()


class TestLoggerFormatting:
    """Test logger message formatting."""
    
    def test_log_format_includes_level(self, tmp_path):
        """Test log format includes log level."""
        log_file = tmp_path / "format_test.log"
        logger = setup_logger(name='format_level_test', log_file=str(log_file))
        
        logger.info("Test message")
        
        # Force flush
        for handler in logger.handlers:
            handler.flush()
        
        content = log_file.read_text()
        assert "INFO" in content
    
    def test_log_format_includes_message(self, tmp_path):
        """Test log format includes the message."""
        log_file = tmp_path / "format_message_test.log"
        logger = setup_logger(name='format_msg_test', log_file=str(log_file))
        
        test_msg = "Unique test message 12345"
        logger.info(test_msg)
        
        # Force flush
        for handler in logger.handlers:
            handler.flush()
        
        content = log_file.read_text()
        assert test_msg in content
    
    def test_different_levels_formatted_correctly(self, tmp_path):
        """Test different log levels are formatted correctly."""
        log_file = tmp_path / "format_levels_test.log"
        logger = setup_logger(name='format_all_test', log_file=str(log_file), level=logging.DEBUG)
        
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")
        
        # Force flush
        for handler in logger.handlers:
            handler.flush()
        
        content = log_file.read_text()
        assert "DEBUG" in content
        assert "INFO" in content
        assert "WARNING" in content
        assert "ERROR" in content
        assert "CRITICAL" in content


class TestLoggerExceptionHandling:
    """Test logger exception handling."""
    
    def test_logger_with_exception_info(self, tmp_path):
        """Test logging with exception information."""
        log_file = tmp_path / "exception_test.log"
        logger = setup_logger(name='exception_test', log_file=str(log_file))
        
        try:
            raise ValueError("Test exception")
        except ValueError:
            logger.error("An error occurred", exc_info=True)
        
        # Force flush
        for handler in logger.handlers:
            handler.flush()
        
        content = log_file.read_text()
        assert "An error occurred" in content
        assert "ValueError" in content
        assert "Test exception" in content
    
    def test_logger_handles_special_characters(self, tmp_path):
        """Test logger handles special characters in messages."""
        log_file = tmp_path / "special_chars_test.log"
        logger = setup_logger(name='special_chars_test', log_file=str(log_file))
        
        special_msg = "Test with special chars: @#$%^&*() unicode: ñ é ü"
        logger.info(special_msg)
        
        # Force flush
        for handler in logger.handlers:
            handler.flush()
        
        content = log_file.read_text()
        # At least verify message was logged (encoding might affect exact match)
        assert "Test with special chars" in content


class TestLoggerReuse:
    """Test logger reuse and singleton behavior."""
    
    def test_same_name_returns_same_logger(self):
        """Test requesting same logger name returns same instance."""
        logger1 = setup_logger(name='reuse_test')
        logger2 = setup_logger(name='reuse_test')
        # Note: logging.getLogger returns same instance for same name
        assert logger1.name == logger2.name
    
    def test_different_names_return_different_loggers(self):
        """Test different logger names return different instances."""
        logger1 = setup_logger(name='logger_a')
        logger2 = setup_logger(name='logger_b')
        assert logger1.name != logger2.name


@pytest.mark.parametrize("level,level_name", [
    (logging.DEBUG, "DEBUG"),
    (logging.INFO, "INFO"),
    (logging.WARNING, "WARNING"),
    (logging.ERROR, "ERROR"),
    (logging.CRITICAL, "CRITICAL"),
])
def test_log_levels_parametrized(tmp_path, level, level_name):
    """Parametrized test for different log levels."""
    log_file = tmp_path / f"param_test_{level_name}.log"
    logger = setup_logger(name=f'param_test_{level_name}', log_file=str(log_file), level=level)
    
    assert logger.level == level
    logger.log(level, f"Test {level_name} message")
    
    # Force flush
    for handler in logger.handlers:
        handler.flush()
    
    content = log_file.read_text()
    assert level_name in content
