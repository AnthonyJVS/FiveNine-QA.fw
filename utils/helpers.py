"""
helpers.py — Common utility functions for the QA framework.

Provides screenshot capture, timestamp generation, retry logic,
and other shared helpers.
"""

import time
import functools
from datetime import datetime
from pathlib import Path
from typing import Callable, Any

import allure
from playwright.sync_api import Page

from config.settings import settings
from utils.logger import get_logger

logger = get_logger("helpers")


# ──────────────────────────────────────────────
# Screenshot helpers
# ──────────────────────────────────────────────

def take_screenshot(page: Page, name: str = "screenshot") -> Path:
    """
    Capture a browser screenshot and attach it to the Allure report.

    Args:
        page: Playwright page instance.
        name: Descriptive name for the screenshot.

    Returns:
        Path to the saved screenshot file.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{name}_{timestamp}.png"
    filepath = settings.screenshots_path / filename

    page.screenshot(path=str(filepath), full_page=True)
    logger.info(f"Screenshot saved: {filepath}")

    # Attach to Allure report
    allure.attach.file(
        str(filepath),
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )

    return filepath


def screenshot_on_failure(page: Page, test_name: str):
    """
    Capture a screenshot specifically for a failed test.

    Args:
        page: Playwright page instance.
        test_name: Name of the failing test for the filename.
    """
    safe_name = test_name.replace("/", "_").replace("\\", "_").replace(":", "_")
    take_screenshot(page, name=f"FAIL_{safe_name}")


# ──────────────────────────────────────────────
# Timestamp helpers
# ──────────────────────────────────────────────

def timestamp() -> str:
    """Return current timestamp string for unique identifiers."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def unique_email(prefix: str = "testuser") -> str:
    """Generate a unique email address for test registration."""
    ts = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"{prefix}_{ts}@testqa.com"


# ──────────────────────────────────────────────
# Retry decorator
# ──────────────────────────────────────────────

def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """
    Retry decorator for flaky operations.

    Use sparingly — only where external factors cause intermittent failures
    (e.g., network requests, element timing).

    Args:
        max_attempts: Maximum number of retry attempts.
        delay: Seconds to wait between retries.
        exceptions: Tuple of exception types to catch and retry.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed for "
                        f"{func.__name__}: {e}"
                    )
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_exception

        return wrapper

    return decorator


# ──────────────────────────────────────────────
# Allure step helpers
# ──────────────────────────────────────────────

def allure_step(description: str):
    """Shorthand for Allure step context manager."""
    return allure.step(description)
