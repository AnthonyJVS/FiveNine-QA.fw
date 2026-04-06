"""
test_login.py — Login flow tests.

Covers valid login, invalid credentials, empty fields, logout,
UI element verification, and session persistence.
"""

import pytest
import allure
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.fake_data import generate_user_data, generate_login_credentials
from utils.logger import get_logger

logger = get_logger("test_login")


@allure.epic("Authentication")
@allure.feature("Login")
class TestLogin:
    """Test suite for user login functionality."""

    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_with_valid_credentials(self, page, registered_user):
        """Test that a registered user can log in successfully."""
        login_page = LoginPage(page)
        login_page.open()

        login_page.login(registered_user["email"], registered_user["password"])

        home = HomePage(page)
        assert home.is_logged_in(), "User should be logged in after valid login"
        assert registered_user["name"] in home.get_logged_in_username(), (
            f"Username '{registered_user['name']}' should appear in nav bar"
        )

    @allure.story("Invalid Login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.negative
    def test_login_with_invalid_email(self, login_page):
        """Test that login fails with a non-existent email."""
        creds = generate_login_credentials(valid=False)
        login_page.login(creds["email"], creds["password"])

        error = login_page.get_login_error()
        assert "incorrect" in error.lower() or "not exist" in error.lower(), (
            f"Expected error message for invalid email, got: '{error}'"
        )

    @allure.story("Invalid Login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.negative
    def test_login_with_wrong_password(self, page, registered_user):
        """Test that login fails with a wrong password."""
        login_page = LoginPage(page)
        login_page.open()

        login_page.login(registered_user["email"], "completely_wrong_password")

        error = login_page.get_login_error()
        assert "incorrect" in error.lower() or "not exist" in error.lower(), (
            f"Expected error message for wrong password, got: '{error}'"
        )

    @allure.story("Invalid Login")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.login
    @pytest.mark.negative
    def test_login_with_empty_fields(self, login_page):
        """Test that login with empty fields does not proceed."""
        login_page.login("", "")

        # Should remain on the login page (browser validation prevents submit)
        assert login_page.verify_login_form_visible(), (
            "Login form should still be visible after empty submission"
        )

    @allure.story("Logout")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.login
    def test_logout_after_login(self, page, registered_user):
        """Test that a user can log out after logging in."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(registered_user["email"], registered_user["password"])

        home = HomePage(page)
        assert home.is_logged_in(), "Should be logged in"

        home.logout()

        # After logout, should be back on login page
        login_page_after = LoginPage(page)
        assert login_page_after.verify_login_form_visible(), (
            "Login form should be visible after logout"
        )

    @allure.story("Login UI")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    def test_login_page_elements_visible(self, login_page):
        """Test that all login page UI elements are present."""
        assert login_page.verify_login_form_visible(), (
            "Login form elements should be visible"
        )
        assert login_page.verify_signup_form_visible(), (
            "Signup form elements should be visible"
        )

        # Verify section headers
        assert "Login" in login_page.get_login_header_text(), (
            "Login header should contain 'Login'"
        )
        assert "Signup" in login_page.get_signup_header_text() or \
               "New User" in login_page.get_signup_header_text(), (
            "Signup header should contain 'Signup' or 'New User'"
        )

    @allure.story("Navigation")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.login
    def test_navigate_to_signup_from_login(self, login_page):
        """Test that the signup form is accessible from the login page."""
        assert login_page.verify_signup_form_visible(), (
            "Signup form should be visible on the login page"
        )

    @allure.story("Session Persistence")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    def test_login_preserves_session(self, page, registered_user):
        """Test that login session persists when navigating to other pages."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(registered_user["email"], registered_user["password"])

        home = HomePage(page)
        assert home.is_logged_in(), "Should be logged in"

        # Navigate to products and verify still logged in
        home.go_to_products()
        assert home.is_logged_in(), (
            "User should remain logged in after navigating to Products"
        )

        # Navigate to cart and verify still logged in
        home.go_to_cart()
        assert home.is_logged_in(), (
            "User should remain logged in after navigating to Cart"
        )
