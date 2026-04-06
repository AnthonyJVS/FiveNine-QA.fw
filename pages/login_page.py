"""
login_page.py — Page object for the Login / Signup page.

URL: https://automationexercise.com/login
"""

import allure
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for the Login and Signup page."""

    # ──────────────────────────────────────────
    # Selectors — Login form
    # ──────────────────────────────────────────

    LOGIN_HEADER = "div.login-form h2"
    LOGIN_EMAIL = "input[data-qa='login-email']"
    LOGIN_PASSWORD = "input[data-qa='login-password']"
    LOGIN_BUTTON = "button[data-qa='login-button']"
    LOGIN_ERROR = "p[style*='color: red']"

    # ──────────────────────────────────────────
    # Selectors — Signup form
    # ──────────────────────────────────────────

    SIGNUP_HEADER = "div.signup-form h2"
    SIGNUP_NAME = "input[data-qa='signup-name']"
    SIGNUP_EMAIL = "input[data-qa='signup-email']"
    SIGNUP_BUTTON = "button[data-qa='signup-button']"
    SIGNUP_ERROR = "p[style*='color: red']"

    # ──────────────────────────────────────────
    # Actions — Login
    # ──────────────────────────────────────────

    @allure.step("Open login page")
    def open(self):
        """Navigate to the login/signup page."""
        self.navigate("/login")
        return self

    @allure.step("Login with email: {email}")
    def login(self, email: str, password: str):
        """
        Perform login with the given credentials.

        Args:
            email: User email address.
            password: User password.
        """
        self.fill(self.LOGIN_EMAIL, email)
        self.fill(self.LOGIN_PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    @allure.step("Verify login form is visible")
    def verify_login_form_visible(self) -> bool:
        """Check that the login form elements are present."""
        return all([
            self.is_visible(self.LOGIN_EMAIL),
            self.is_visible(self.LOGIN_PASSWORD),
            self.is_visible(self.LOGIN_BUTTON),
        ])

    def get_login_error(self) -> str:
        """Get the login error message text."""
        if self.is_visible(self.LOGIN_ERROR):
            return self.get_text(self.LOGIN_ERROR)
        return ""

    def get_login_header_text(self) -> str:
        """Get the login section header text."""
        return self.get_text(self.LOGIN_HEADER)

    # ──────────────────────────────────────────
    # Actions — Signup
    # ──────────────────────────────────────────

    @allure.step("Start signup with name: {name}, email: {email}")
    def start_signup(self, name: str, email: str):
        """
        Fill in the signup form and submit to proceed to registration.

        Args:
            name: User display name.
            email: User email address.
        """
        self.fill(self.SIGNUP_NAME, name)
        self.fill(self.SIGNUP_EMAIL, email)
        self.click(self.SIGNUP_BUTTON)

    @allure.step("Verify signup form is visible")
    def verify_signup_form_visible(self) -> bool:
        """Check that the signup form elements are present."""
        return all([
            self.is_visible(self.SIGNUP_NAME),
            self.is_visible(self.SIGNUP_EMAIL),
            self.is_visible(self.SIGNUP_BUTTON),
        ])

    def get_signup_error(self) -> str:
        """Get the signup error message text."""
        if self.is_visible(self.SIGNUP_ERROR):
            return self.get_text(self.SIGNUP_ERROR)
        return ""

    def get_signup_header_text(self) -> str:
        """Get the signup section header text."""
        return self.get_text(self.SIGNUP_HEADER)
