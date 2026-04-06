"""
Root conftest.py — Project-level pytest configuration and hooks.

This file is auto-discovered by pytest and runs before any test collection.
It registers custom markers and sets up environment properties for reporting.
"""

import os
import pytest
from pathlib import Path


# ──────────────────────────────────────────────
# Directory setup — ensure artifact directories exist
# ──────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent

ARTIFACT_DIRS = [
    PROJECT_ROOT / "reports",
    PROJECT_ROOT / "screenshots",
    PROJECT_ROOT / "logs",
    PROJECT_ROOT / "allure-results",
]

for directory in ARTIFACT_DIRS:
    directory.mkdir(parents=True, exist_ok=True)


# ──────────────────────────────────────────────
# Allure environment properties
# ──────────────────────────────────────────────

def pytest_configure(config):
    """Write Allure environment properties for report context."""
    allure_dir = PROJECT_ROOT / "allure-results"
    allure_dir.mkdir(parents=True, exist_ok=True)

    env_file = allure_dir / "environment.properties"
    env_file.write_text(
        f"Browser=chromium\n"
        f"Environment={os.getenv('ENV', 'dev')}\n"
        f"Base.URL=https://automationexercise.com\n"
        f"Python={os.sys.version}\n"
        f"OS={os.name}\n"
    )


# ──────────────────────────────────────────────
# Session-level hooks
# ──────────────────────────────────────────────

def pytest_collection_modifyitems(config, items):
    """Auto-add markers based on test location."""
    for item in items:
        test_path = str(item.fspath)
        if "/ui/" in test_path or "\\ui\\" in test_path:
            item.add_marker(pytest.mark.ui)
        elif "/api/" in test_path or "\\api\\" in test_path:
            item.add_marker(pytest.mark.api)
