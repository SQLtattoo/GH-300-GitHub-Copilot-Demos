"""Tests for Budget Buddy logging configuration."""

import logging

from logger import setup_logger


def test_console_logs_only_the_message():
    """Keep interactive report output compact and readable."""
    configured_logger = setup_logger("test_console_output")

    console_formatter = configured_logger.handlers[0].formatter

    assert console_formatter is not None
    assert console_formatter._fmt == "%(message)s"


def test_file_logs_keep_diagnostic_context(tmp_path):
    """Retain timestamps, logger names, and levels in persisted logs."""
    log_path = tmp_path / "budget-buddy.log"
    configured_logger = setup_logger("test_file_output", log_file=str(log_path))

    file_handler = next(
        handler
        for handler in configured_logger.handlers
        if isinstance(handler, logging.FileHandler)
    )
    formatter = file_handler.formatter

    assert formatter is not None
    assert formatter._fmt == "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def test_file_logger_creates_parent_directory_and_writes_utf8(tmp_path):
    """Create missing log directories and persist Unicode messages."""
    log_path = tmp_path / "nested" / "budget-buddy.log"
    configured_logger = setup_logger("test_nested_log", log_file=str(log_path))

    configured_logger.info("Cafe total: 12.50 EUR")
    for handler in configured_logger.handlers:
        handler.flush()

    assert log_path.exists()
    assert "Cafe total: 12.50 EUR" in log_path.read_text(encoding="utf-8")
