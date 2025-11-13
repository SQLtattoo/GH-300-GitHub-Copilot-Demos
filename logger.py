"""
Logger module for centralized logging across the application.
Provides consistent logging configuration and formatting.
"""

import logging
import sys
from typing import Optional


def setup_logger(
    name: str = "app",
    level: int = logging.INFO,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Configure and return a logger instance with consistent formatting.
    
    Args:
        name (str): Name of the logger (default: "app")
        level (int): Logging level (default: logging.INFO)
        log_file (Optional[str]): Path to log file. If None, logs only to console.
    
    Returns:
        logging.Logger: Configured logger instance
    
    Example:
        >>> logger = setup_logger("my_app", logging.DEBUG)
        >>> logger.info("Application started")
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        import os
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Create default application logger
logger = setup_logger("github_copilot_demo", logging.INFO)
