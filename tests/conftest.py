# tests/conftest.py
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import logging
from core.api_client import APIClient

@pytest.fixture(scope="session")
def api_client():
    """
    Creates a single shared instance of the APIClient for all tests.
    :return: APIClient
    """
    return APIClient()

class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',    # blue
        'INFO': '\033[92m',     # green
        'WARNING': '\033[93m',   # yello
        'ERROR': '\033[91m',     # red
        'CRITICAL': '\033[95m'   # magenta
    }
    RESET = '\033[0m'

    def format(self, record):
        level_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{level_color}{record.levelname}{self.RESET}"
        return super().format(record)


@pytest.fixture(scope="session")
def logger():
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.DEBUG)

    log_level_str = os.getenv("LOG_LEVEL", "DEBUG").upper()
    log_level = getattr(logging, log_level_str, logging.DEBUG)

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s", "%H:%M:%S")
    color_formatter = ColorFormatter("[%(asctime)s] %(levelname)s - %(message)s", "%H:%M:%S")

    # print log to screen
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(color_formatter)

    # print log to file
    file_handler = logging.FileHandler("test_log.txt", mode="w", encoding="utf-8")
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    # do not add if exist
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    logger.propagate = False
    return logger
