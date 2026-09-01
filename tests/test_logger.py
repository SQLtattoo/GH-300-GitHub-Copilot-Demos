"""Tests for centralized logger configuration."""

import logging

from logger import setup_logger


def _close_handlers(configured_logger):
    """Close test handlers so temporary files can be cleaned up on Windows."""
    for handler in configured_logger.handlers:
        handler.close()
    configured_logger.handlers.clear()


def test_setup_logger_writes_formatted_console_message(capsys):
    configured_logger = setup_logger("test.console", logging.DEBUG)
    configured_logger.propagate = False

    configured_logger.debug("calculated total")

    output = capsys.readouterr().out
    assert "test.console - DEBUG - calculated total" in output
    assert len(configured_logger.handlers) == 1
    _close_handlers(configured_logger)


def test_setup_logger_creates_parent_directory_and_file(tmp_path):
    log_path = tmp_path / "nested" / "budget.log"
    configured_logger = setup_logger("test.file", logging.WARNING, str(log_path))
    configured_logger.propagate = False

    configured_logger.warning("budget exceeded")
    for handler in configured_logger.handlers:
        handler.flush()

    assert log_path.exists()
    assert "test.file - WARNING - budget exceeded" in log_path.read_text(encoding="utf-8")
    assert len(configured_logger.handlers) == 2
    _close_handlers(configured_logger)


def test_setup_logger_replaces_existing_handlers():
    configured_logger = logging.getLogger("test.reconfigure")
    old_handler = logging.NullHandler()
    configured_logger.addHandler(old_handler)

    result = setup_logger("test.reconfigure", logging.ERROR)

    assert result is configured_logger
    assert old_handler not in result.handlers
    assert len(result.handlers) == 1
    assert result.level == logging.ERROR
    _close_handlers(result)