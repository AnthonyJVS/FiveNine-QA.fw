"""
dashboard/app.py — Streamlit QA Dashboard.

A lightweight dashboard for running tests, viewing results,
and inspecting test artifacts.

Run with: streamlit run dashboard/app.py
"""

import subprocess
import os
import sys
from pathlib import Path
from datetime import datetime

import streamlit as st

# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
LOGS_DIR = PROJECT_ROOT / "logs"
ALLURE_RESULTS_DIR = PROJECT_ROOT / "allure-results"

# ──────────────────────────────────────────────
# Page setup
# ──────────────────────────────────────────────

st.set_page_config(
    page_title="QA Automation Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title(" QA Automation Dashboard")
st.markdown("---")

# ──────────────────────────────────────────────
# Sidebar — Test Execution
# ──────────────────────────────────────────────

with st.sidebar:
    st.header(" Run Tests")

    test_suite = st.selectbox(
        "Select test suite",
        ["smoke", "api", "ui", "all"],
        index=0,
    )

    browser = st.selectbox(
        "Browser",
        ["chromium", "firefox", "webkit"],
        index=0,
    )

    headless = st.checkbox("Headless mode", value=True)

    if st.button(" Run Tests", type="primary", use_container_width=True):
        # Build the pytest command
        cmd = [sys.executable, "-m", "pytest"]

        if test_suite == "smoke":
            cmd.extend(["-m", "smoke"])
        elif test_suite == "api":
            cmd.extend(["tests/api/"])
        elif test_suite == "ui":
            cmd.extend(["tests/ui/"])
        else:
            cmd.extend(["tests/"])

        cmd.extend([
            "-v",
            "--html=reports/report.html",
            "--self-contained-html",
            "--alluredir=allure-results",
            "--tb=short",
        ])

        env = os.environ.copy()
        env["BROWSER"] = browser
        env["HEADLESS"] = str(headless).lower()

        with st.spinner(f"Running {test_suite} tests..."):
            result = subprocess.run(
                cmd,
                cwd=str(PROJECT_ROOT),
                capture_output=True,
                text=True,
                env=env,
            )

        if result.returncode == 0:
            st.success("✅ All tests passed!")
        else:
            st.error(f"❌ Tests failed (exit code: {result.returncode})")

        st.session_state["last_run_output"] = result.stdout + result.stderr
        st.session_state["last_run_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    st.markdown("---")
    st.header("📋 Quick Info")
    st.markdown(f"**Project Root:** `{PROJECT_ROOT}`")

    # Count test files
    ui_tests = len(list((PROJECT_ROOT / "tests" / "ui").glob("test_*.py")))
    api_tests = len(list((PROJECT_ROOT / "tests" / "api").glob("test_*.py")))
    st.metric("UI Test Files", ui_tests)
    st.metric("API Test Files", api_tests)

# ──────────────────────────────────────────────
# Main content — Tabs
# ──────────────────────────────────────────────

tab_output, tab_reports, tab_screenshots, tab_logs = st.tabs([
    " Test Output",
    " Reports",
    " Screenshots",
    " Logs",
])

# ── Test Output Tab ──
with tab_output:
    if "last_run_output" in st.session_state:
        st.markdown(f"**Last run:** {st.session_state.get('last_run_time', 'N/A')}")
        st.code(st.session_state["last_run_output"], language="text")
    else:
        st.info("No test output yet. Run a test suite from the sidebar.")

# ── Reports Tab ──
with tab_reports:
    st.subheader("Available Reports")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_files = sorted(REPORTS_DIR.glob("*.html"), reverse=True)

    if report_files:
        for report in report_files:
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f"📄 **{report.name}**")
            with col2:
                mod_time = datetime.fromtimestamp(report.stat().st_mtime)
                st.text(mod_time.strftime("%Y-%m-%d %H:%M:%S"))
            with col3:
                size_kb = report.stat().st_size / 1024
                st.text(f"{size_kb:.1f} KB")
    else:
        st.info("No reports generated yet. Run tests to generate reports.")

    st.markdown("---")
    st.markdown(
        "💡 **Tip:** Open the HTML report files directly in your browser "
        "for the full interactive experience."
    )

# ── Screenshots Tab ──
with tab_screenshots:
    st.subheader("Failure Screenshots")

    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    screenshots = sorted(
        SCREENSHOTS_DIR.glob("*.png"),
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )

    if screenshots:
        # Show screenshots in a grid
        cols = st.columns(3)
        for i, screenshot in enumerate(screenshots[:12]):  # Show last 12
            with cols[i % 3]:
                st.image(str(screenshot), caption=screenshot.name, use_container_width=True)
    else:
        st.info("No screenshots captured yet. Screenshots are taken on test failures.")

# ── Logs Tab ──
with tab_logs:
    st.subheader("Test Execution Logs")

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_files = sorted(LOGS_DIR.glob("*.log"), reverse=True)

    if log_files:
        selected_log = st.selectbox(
            "Select log file",
            log_files,
            format_func=lambda f: f.name,
        )

        if selected_log:
            content = selected_log.read_text(encoding="utf-8", errors="replace")
            # Show last 200 lines to avoid performance issues
            lines = content.split("\n")
            if len(lines) > 200:
                st.warning(f"Showing last 200 of {len(lines)} lines")
                content = "\n".join(lines[-200:])
            st.code(content, language="text")
    else:
        st.info("No logs available yet. Run tests to generate log files.")

# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "QA Automation Framework Dashboard • Built with Streamlit"
    "</div>",
    unsafe_allow_html=True,
)
