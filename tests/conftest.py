"""
tests/conftest.py — Root test fixtures for browser and page management.

Provides:
- Browser context creation with configurable options
- Page fixture with automatic screenshot on failure
- Logged-in page fixture for authenticated tests
"""

import pytest
import allure
from pathlib import Path
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

from config.settings import settings
from utils.logger import get_logger
from utils.helpers import screenshot_on_failure

logger = get_logger("conftest")


# ──────────────────────────────────────────────
# Browser fixtures
# ──────────────────────────────────────────────

@pytest.fixture(scope="session")
def browser():
    """
    Session-scoped browser instance.

    Launches the browser configured in settings (chromium/firefox/webkit).
    Shared across all tests in a session for efficiency.
    """
    with sync_playwright() as playwright:
        browser_type = getattr(playwright, settings.browser)
        browser_instance = browser_type.launch(
            headless=settings.headless,
            slow_mo=settings.slow_mo,
        )
        logger.info(
            f"Browser launched: {settings.browser} "
            f"(headless={settings.headless}, slow_mo={settings.slow_mo})"
        )
        yield browser_instance
        browser_instance.close()
        logger.info("Browser closed")


@pytest.fixture(scope="function")
def context(browser: Browser):
    """
    Function-scoped browser context.

    Creates a fresh context per test for isolation (separate cookies,
    storage, etc.). Configures viewport and other context options.
    Blocks cookie consent (FundingChoices) scripts to prevent overlay interference.
    """
    ctx = browser.new_context(
        viewport={
            "width": settings.viewport_width,
            "height": settings.viewport_height,
        },
        ignore_https_errors=True,
    )

    # Block ALL cookie consent / ad overlay scripts that interfere with UI tests
    consent_patterns = [
        "**/*fundingchoices*",
        "**/*fc.yahoo*",
        "**/*googletagmanager*",
        "**/*google*consent*",
        "**/*googlesyndication*",
        "**/*googleads*",
        "**/*doubleclick*",
        "**/*adservice*",
        "**/*pagead*",
        "**/*consent*",
    ]
    for pattern in consent_patterns:
        ctx.route(pattern, lambda route: route.abort())
    logger.debug("Blocked consent/ad overlay scripts via route")

    # Inject CSS + JS on every page to nuke consent overlays before they render
    ctx.add_init_script("""
        // Inject a style tag to hide consent overlays immediately
        const style = document.createElement('style');
        style.textContent = `
            .fc-consent-root, .fc-dialog-overlay, .fc-dialog-container,
            div[class*="consent"], div[id*="consent"],
            .fc-dialog, .fc-footer { display: none !important; visibility: hidden !important; }
        `;
        (document.head || document.documentElement).appendChild(style);

        // Observe DOM and remove consent elements as they appear
        const observer = new MutationObserver((mutations) => {
            document.querySelectorAll(
                '.fc-consent-root, .fc-dialog-overlay, .fc-dialog-container'
            ).forEach(el => el.remove());
        });
        observer.observe(document.documentElement, { childList: true, subtree: true });
    """)
    logger.debug("Injected consent-blocking CSS/JS")

    logger.debug("New browser context created")
    yield ctx
    ctx.close()
    logger.debug("Browser context closed")


@pytest.fixture(scope="function")
def page(context: BrowserContext, request):
    """
    Function-scoped page with automatic screenshot on failure.

    Yields a fresh page for each test. If the test fails,
    captures a screenshot and attaches it to the Allure report.
    """
    pg = context.new_page()
    logger.info(f"New page opened for test: {request.node.name}")

    yield pg

    # Screenshot on failure (use getattr to avoid AttributeError when setup fails)
    rep_call = getattr(request.node, "rep_call", None)
    rep_setup = getattr(request.node, "rep_setup", None)
    if (rep_call and rep_call.failed) or (rep_setup and rep_setup.failed):
        logger.warning(f"Test FAILED: {request.node.name} — capturing screenshot")
        screenshot_on_failure(pg, request.node.name)

    pg.close()
    logger.debug("Page closed")


# ──────────────────────────────────────────────
# Pytest hooks for failure detection
# ──────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test result on the item for use in fixtures."""
    import pluggy

    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
