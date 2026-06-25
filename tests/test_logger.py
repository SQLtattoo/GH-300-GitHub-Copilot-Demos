"""Tests for the centralized logger setup."""

import logging

from logger import setup_logger


def test_setup_logger_defaults():
    """A default logger has the right name, level, and a single handler."""
    log = setup_logger("test_default_logger")
    assert log.name == "test_default_logger"
    assert log.level == logging.INFO
    assert len(log.handlers) == 1


def test_setup_logger_clears_existing_handlers():
    """Calling setup twice does not accumulate duplicate handlers."""
    setup_logger("test_no_dupes")
    log = setup_logger("test_no_dupes")
    assert len(log.handlers) == 1


def test_setup_logger_custom_level():
    """A custom level is applied to the logger."""
    log = setup_logger("test_debug_logger", level=logging.DEBUG)
    assert log.level == logging.DEBUG


def test_setup_logger_writes_to_file(tmp_path):
    """When a log file is given, a file handler is added and writes are persisted."""
    log_path = tmp_path / "logs" / "app.log"
    log = setup_logger("test_file_logger", log_file=str(log_path))

    assert any(isinstance(h, logging.FileHandler) for h in log.handlers)

    log.info("hello file")
    for handler in log.handlers:
        handler.flush()
        handler.close()

    assert log_path.exists()
    assert "hello file" in log_path.read_text(encoding="utf-8")
