"""
logger.py — Structured logging configuration for the QA framework.

Provides a configured logger with both console and file handlers.
Log files are written to the logs/ directory with timestamped names.

Usage:
    from utils.logger import logger
    logger.info("Test started")
    logger.error("Assertion failed", exc_info=True)
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

from config.settings import settings


# ──────────────────────────────────────────────
# Log directory & file setup
# ──────────────────────────────────────────────

LOG_DIR = settings.logs_path
LOG_FILE = LOG_DIR / f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"


# ──────────────────────────────────────────────
# Formatter
# ──────────────────────────────────────────────

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)


# ──────────────────────────────────────────────
# Logger factory
# ──────────────────────────────────────────────

def get_logger(name: str = "qa_framework") -> logging.Logger:
    """
    Create or retrieve a named logger with console + file handlers.

    Args:
        name: Logger name (typically module name).

    Returns:
        Configured Logger instance.
    """
    log = logging.getLogger(name)

    # Prevent duplicate handlers on repeated calls
    if log.handlers:
        return log

    log.setLevel(logging.DEBUG)

    # Console handler — INFO and above
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # File handler — DEBUG and above (captures everything)
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    log.addHandler(console_handler)
    log.addHandler(file_handler)

    return log


# ──────────────────────────────────────────────
# Default logger instance
# ──────────────────────────────────────────────

logger = get_logger()
