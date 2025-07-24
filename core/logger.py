"""
Professional logging configuration for API testing framework.
Provides structured logging with different levels and outputs.
"""

import logging
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Optional


class ColorFormatter(logging.Formatter):
    """Custom formatter that adds colors to log levels for console output."""
    
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m'   # Magenta
    }
    RESET = '\033[0m'

    def format(self, record):
        level_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{level_color}{record.levelname}{self.RESET}"
        return super().format(record)


class APITestLogger:
    """
    Singleton logger class for API testing framework.
    Provides centralized logging configuration and management.
    """
    
    _instance: Optional['APITestLogger'] = None
    _logger: Optional[logging.Logger] = None

    def __new__(cls) -> 'APITestLogger':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._logger is None:
            self._setup_logger()

    def _setup_logger(self) -> None:
        """Initialize and configure the logger with console and file handlers."""
        self._logger = logging.getLogger("api_test_framework")
        self._logger.setLevel(logging.DEBUG)
        
        # Clear any existing handlers to avoid duplicates
        self._logger.handlers.clear()
        
        # Get log level from environment or default to INFO
        log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
        log_level = getattr(logging, log_level_str, logging.INFO)
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            "[%(asctime)s] %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        console_formatter = ColorFormatter(
            "[%(asctime)s] %(levelname)s - %(message)s",
            datefmt="%H:%M:%S"
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(console_formatter)
        
        # File handler
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        log_filename = f"api_tests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(
            log_dir / log_filename, 
            mode="w", 
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        
        # Add handlers
        self._logger.addHandler(console_handler)
        self._logger.addHandler(file_handler)
        
        # Prevent propagation to root logger
        self._logger.propagate = False
        
        self._logger.info(f"Logger initialized. Log file: {log_filename}")

    @property
    def logger(self) -> logging.Logger:
        """Get the configured logger instance."""
        return self._logger

    def info(self, message: str) -> None:
        """Log an info message."""
        self._logger.info(message)

    def debug(self, message: str) -> None:
        """Log a debug message."""
        self._logger.debug(message)

    def warning(self, message: str) -> None:
        """Log a warning message."""
        self._logger.warning(message)

    def error(self, message: str) -> None:
        """Log an error message."""
        self._logger.error(message)

    def critical(self, message: str) -> None:
        """Log a critical message."""
        self._logger.critical(message)

    def log_api_request(self, method: str, url: str, payload: dict = None) -> None:
        """Log API request details."""
        message = f"API Request: {method.upper()} {url}"
        if payload:
            message += f" | Payload: {payload}"
        self._logger.info(message)

    def log_api_response(self, status_code: int, response_time: float = None) -> None:
        """Log API response details."""
        message = f"API Response: {status_code}"
        if response_time:
            message += f" | Response Time: {response_time:.3f}s"
        
        if 200 <= status_code < 300:
            self._logger.info(message)
        elif 400 <= status_code < 500:
            self._logger.warning(message)
        else:
            self._logger.error(message)

    def log_test_start(self, test_name: str) -> None:
        """Log the start of a test."""
        self._logger.info(f"Starting test: {test_name}")

    def log_test_end(self, test_name: str, status: str = "PASSED") -> None:
        """Log the end of a test."""
        self._logger.info(f"Test completed: {test_name} - {status}")


# Convenience functions for easy access
def get_logger() -> APITestLogger:
    """Get the singleton logger instance."""
    return APITestLogger()


def setup_test_logging() -> logging.Logger:
    """Setup logging for tests and return the logger instance."""
    logger_instance = get_logger()
    return logger_instance.logger
