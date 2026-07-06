"""Tests for the logger module."""

import logging

from logger import logger, setup_logger


def test_setup_logger_defaults():
    log = setup_logger("test_default")
    assert isinstance(log, logging.Logger)
    assert log.level == logging.INFO
    assert len(log.handlers) == 1


def test_setup_logger_custom_level():
    log = setup_logger("test_debug", level=logging.DEBUG)
    assert log.level == logging.DEBUG


def test_setup_logger_clears_existing_handlers():
    setup_logger("test_dupes")
    log = setup_logger("test_dupes")
    # Re-configuring must not accumulate duplicate handlers.
    assert len(log.handlers) == 1


def test_setup_logger_with_file_creates_directory(tmp_path):
    log_file = tmp_path / "logs" / "app.log"
    log = setup_logger("test_file", log_file=str(log_file))

    log.info("hello")
    for handler in log.handlers:
        handler.flush()

    assert log_file.exists()
    assert len(log.handlers) == 2


def test_module_logger_is_configured():
    assert logger.name == "github_copilot_demo"
    assert logger.handlers
