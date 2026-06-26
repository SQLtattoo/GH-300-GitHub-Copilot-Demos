import logging

from logger import setup_logger


def test_setup_logger_console_only() -> None:
    app_logger = setup_logger("test_console_logger", logging.DEBUG)

    assert app_logger.name == "test_console_logger"
    assert app_logger.level == logging.DEBUG
    assert len(app_logger.handlers) == 1


def test_setup_logger_with_file(tmp_path) -> None:
    log_file = tmp_path / "logs" / "app.log"
    app_logger = setup_logger("test_file_logger", logging.INFO, str(log_file))
    app_logger.info("hello log")

    assert log_file.exists()
    assert "hello log" in log_file.read_text(encoding="utf-8")
    assert len(app_logger.handlers) == 2
