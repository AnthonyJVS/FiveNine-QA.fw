"""
settings.py — Central configuration loader.

Loads environment-specific settings from .env files and provides
a typed Settings dataclass for use across the framework.

Usage:
    from config.settings import settings
    print(settings.base_url)
    print(settings.browser)
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv


# ──────────────────────────────────────────────
# Resolve environment file
# ──────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent.parent
ENV = os.getenv("ENV", "dev")

env_file = PROJECT_ROOT / "config" / "environments" / f".env.{ENV}"
if env_file.exists():
    load_dotenv(dotenv_path=env_file)
else:
    # Fallback: load from project root .env if it exists
    root_env = PROJECT_ROOT / ".env"
    if root_env.exists():
        load_dotenv(dotenv_path=root_env)


# ──────────────────────────────────────────────
# Settings dataclass
# ──────────────────────────────────────────────

@dataclass(frozen=True)
class Settings:
    """Immutable framework configuration."""

    # Environment
    env: str = field(default_factory=lambda: os.getenv("ENV", "dev"))

    # URLs
    base_url: str = field(
        default_factory=lambda: os.getenv("BASE_URL", "https://automationexercise.com")
    )
    api_base_url: str = field(
        default_factory=lambda: os.getenv("API_BASE_URL", "https://automationexercise.com/api")
    )

    # Browser configuration
    browser: str = field(
        default_factory=lambda: os.getenv("BROWSER", "chromium")
    )
    headless: bool = field(
        default_factory=lambda: os.getenv("HEADLESS", "true").lower() == "true"
    )
    slow_mo: int = field(
        default_factory=lambda: int(os.getenv("SLOW_MO", "0"))
    )
    viewport_width: int = field(
        default_factory=lambda: int(os.getenv("VIEWPORT_WIDTH", "1280"))
    )
    viewport_height: int = field(
        default_factory=lambda: int(os.getenv("VIEWPORT_HEIGHT", "720"))
    )

    # Timeouts (milliseconds)
    default_timeout: int = field(
        default_factory=lambda: int(os.getenv("DEFAULT_TIMEOUT", "30000"))
    )
    navigation_timeout: int = field(
        default_factory=lambda: int(os.getenv("NAVIGATION_TIMEOUT", "30000"))
    )

    # API settings
    api_timeout: int = field(
        default_factory=lambda: int(os.getenv("API_TIMEOUT", "30"))
    )

    # Artifacts
    screenshot_dir: str = field(
        default_factory=lambda: os.getenv("SCREENSHOT_DIR", "screenshots")
    )
    log_dir: str = field(
        default_factory=lambda: os.getenv("LOG_DIR", "logs")
    )
    report_dir: str = field(
        default_factory=lambda: os.getenv("REPORT_DIR", "reports")
    )

    # Test user (for login tests — dynamically created)
    test_user_email: str = field(
        default_factory=lambda: os.getenv("TEST_USER_EMAIL", "")
    )
    test_user_password: str = field(
        default_factory=lambda: os.getenv("TEST_USER_PASSWORD", "")
    )

    @property
    def project_root(self) -> Path:
        return PROJECT_ROOT

    @property
    def screenshots_path(self) -> Path:
        path = PROJECT_ROOT / self.screenshot_dir
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def logs_path(self) -> Path:
        path = PROJECT_ROOT / self.log_dir
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def reports_path(self) -> Path:
        path = PROJECT_ROOT / self.report_dir
        path.mkdir(parents=True, exist_ok=True)
        return path


# ──────────────────────────────────────────────
# Singleton instance
# ──────────────────────────────────────────────

settings = Settings()
