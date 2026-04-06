"""
base_page.py — Base page object with shared Playwright helpers.

All page objects inherit from BasePage to get common navigation,
interaction, waiting, and screenshot functionality.
"""

import allure
from playwright.sync_api import Page, expect, Locator
from playwright._impl._errors import TimeoutError as PlaywrightTimeout
from typing import Optional

from config.settings import settings
from utils.logger import get_logger

logger = get_logger("base_page")


class BasePage:
    """Base class for all page objects."""

    def __init__(self, page: Page):
        self.page = page
        self.page.set_default_timeout(settings.default_timeout)
        self.page.set_default_navigation_timeout(settings.navigation_timeout)

    # ──────────────────────────────────────────
    # Navigation
    # ──────────────────────────────────────────

    @allure.step("Navigate to {path}")
    def navigate(self, path: str = "/"):
        """Navigate to a path relative to base URL."""
        url = f"{settings.base_url.rstrip('/')}/{path.lstrip('/')}"
        logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until="domcontentloaded")
        self._dismiss_consent_overlay()

    @allure.step("Navigate to full URL: {url}")
    def navigate_to_url(self, url: str):
        """Navigate to an absolute URL."""
        logger.info(f"Navigating to URL: {url}")
        self.page.goto(url, wait_until="domcontentloaded")
        self._dismiss_consent_overlay()

    # ──────────────────────────────────────────
    # Element interactions
    # ──────────────────────────────────────────

    @allure.step("Click element: {selector}")
    def click(self, selector: str):
        """Click an element by selector (auto-dismisses consent overlay on block)."""
        logger.debug(f"Clicking: {selector}")
        try:
            self.page.click(selector)
        except PlaywrightTimeout as e:
            if "intercepts pointer events" in str(e) or "fc-consent" in str(e):
                logger.debug("Consent overlay blocked click — dismissing and retrying")
                self._dismiss_consent_overlay()
                self.page.click(selector)
            else:
                raise

    @allure.step("Fill '{selector}' with text")
    def fill(self, selector: str, text: str):
        """Fill a text input by selector (auto-dismisses consent overlay on block)."""
        logger.debug(f"Filling '{selector}' with '{text[:20]}...'")
        try:
            self.page.fill(selector, text)
        except PlaywrightTimeout as e:
            if "intercepts pointer events" in str(e) or "fc-consent" in str(e):
                logger.debug("Consent overlay blocked fill — dismissing and retrying")
                self._dismiss_consent_overlay()
                self.page.fill(selector, text)
            else:
                raise

    @allure.step("Type into '{selector}'")
    def type_text(self, selector: str, text: str, delay: int = 50):
        """Type text character by character (useful for search inputs)."""
        logger.debug(f"Typing into '{selector}'")
        self.page.type(selector, text, delay=delay)

    @allure.step("Select option in '{selector}'")
    def select_option(self, selector: str, value: str):
        """Select a dropdown option by value."""
        logger.debug(f"Selecting '{value}' in '{selector}'")
        self.page.select_option(selector, value)

    @allure.step("Check checkbox: {selector}")
    def check(self, selector: str):
        """Check a checkbox if not already checked."""
        logger.debug(f"Checking: {selector}")
        self.page.check(selector)

    def upload_file(self, selector: str, file_path: str):
        """Upload a file to a file input."""
        logger.debug(f"Uploading file to '{selector}': {file_path}")
        self.page.set_input_files(selector, file_path)

    # ──────────────────────────────────────────
    # Element state
    # ──────────────────────────────────────────

    def get_text(self, selector: str) -> str:
        """Get the text content of an element."""
        text = self.page.text_content(selector) or ""
        logger.debug(f"Text of '{selector}': '{text[:50]}'")
        return text.strip()

    def get_input_value(self, selector: str) -> str:
        """Get the value of an input element."""
        return self.page.input_value(selector)

    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """Check if an element is visible on the page."""
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def is_hidden(self, selector: str, timeout: int = 5000) -> bool:
        """Check if an element is hidden or absent."""
        try:
            self.page.wait_for_selector(selector, state="hidden", timeout=timeout)
            return True
        except Exception:
            return False

    def get_element_count(self, selector: str) -> int:
        """Count elements matching a selector."""
        return self.page.locator(selector).count()

    def get_all_texts(self, selector: str) -> list[str]:
        """Get text content of all elements matching a selector."""
        return self.page.locator(selector).all_text_contents()

    # ──────────────────────────────────────────
    # Waiting
    # ──────────────────────────────────────────

    @allure.step("Wait for element: {selector}")
    def wait_for_element(self, selector: str, state: str = "visible", timeout: int = None):
        """Wait for an element to reach a specific state."""
        timeout = timeout or settings.default_timeout
        logger.debug(f"Waiting for '{selector}' to be {state}")
        self.page.wait_for_selector(selector, state=state, timeout=timeout)

    def wait_for_url(self, url_pattern: str, timeout: int = None):
        """Wait for URL to match a pattern."""
        timeout = timeout or settings.navigation_timeout
        self.page.wait_for_url(url_pattern, timeout=timeout)

    def wait_for_load_state(self, state: str = "networkidle"):
        """Wait for a specific page load state."""
        self.page.wait_for_load_state(state)

    # ──────────────────────────────────────────
    # Assertions (using Playwright expect API)
    # ──────────────────────────────────────────

    def expect_visible(self, selector: str):
        """Assert element is visible."""
        expect(self.page.locator(selector)).to_be_visible()

    def expect_text(self, selector: str, expected_text: str):
        """Assert element contains expected text."""
        expect(self.page.locator(selector)).to_contain_text(expected_text)

    def expect_url_contains(self, path: str):
        """Assert current URL contains a path fragment."""
        expect(self.page).to_have_url(f"*{path}*")

    # ──────────────────────────────────────────
    # Page info
    # ──────────────────────────────────────────

    @property
    def current_url(self) -> str:
        """Return current page URL."""
        return self.page.url

    @property
    def title(self) -> str:
        """Return page title."""
        return self.page.title()

    # ──────────────────────────────────────────
    # Locator helper (for chaining)
    # ──────────────────────────────────────────

    def locator(self, selector: str) -> Locator:
        """Return a Playwright Locator for advanced operations."""
        return self.page.locator(selector)

    # ──────────────────────────────────────────
    # Screenshot
    # ──────────────────────────────────────────

    @allure.step("Take screenshot: {name}")
    def take_screenshot(self, name: str = "screenshot"):
        """Capture and attach a screenshot to the Allure report."""
        from utils.helpers import take_screenshot
        return take_screenshot(self.page, name)

    # ──────────────────────────────────────────
    # Internal helpers
    # ──────────────────────────────────────────

    def _dismiss_consent_overlay(self):
        """Dismiss cookie consent / ad overlays if present (FundingChoices / Google)."""
        # Fast path: forcibly remove ALL consent overlays via JS (most reliable)
        try:
            removed = self.page.evaluate("""
                const els = document.querySelectorAll(
                    '.fc-consent-root, .fc-dialog-overlay, .fc-dialog-container, '
                    + 'div[class*="consent"], div[id*="consent"]'
                );
                els.forEach(el => el.remove());
                els.length;
            """)
            if removed:
                logger.debug(f"Removed {removed} consent overlay element(s) via JS")
        except Exception:
            pass

        # Fallback: try clicking the consent button if overlay still exists
        try:
            consent_btn = self.page.locator("button.fc-cta-consent")
            if consent_btn.is_visible(timeout=500):
                consent_btn.click()
                logger.debug("Dismissed consent overlay via button click")
                self.page.wait_for_timeout(500)
        except Exception:
            pass

    def scroll_to_bottom(self):
        """Scroll to the bottom of the page."""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_to_element(self, selector: str):
        """Scroll an element into view."""
        self.page.locator(selector).scroll_into_view_if_needed()
