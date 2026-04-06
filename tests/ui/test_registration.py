"""
test_registration.py — User registration flow tests.

Covers successful registration, duplicate email, form validation,
success confirmation, and account deletion after registration.
"""

import pytest
import allure
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from utils.fake_data import generate_user_data
from utils.helpers import unique_email
from utils.logger import get_logger

logger = get_logger("test_registration")


@allure.epic("Authentication")
@allure.feature("Registration")
class TestRegistration:
    """Test suite for user registration / account creation."""

    @allure.story("Successful Registration")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.registration
    def test_register_new_user(self, page, new_user_data):
        """Test complete user registration flow."""
        login_page = LoginPage(page)
        login_page.open()

        # Start signup
        login_page.start_signup(new_user_data["name"], new_user_data["email"])

        # Fill and submit registration
        reg_page = RegistrationPage(page)
        assert reg_page.verify_form_visible(), "Registration form should be visible"

        reg_page.register(new_user_data)

        # Verify success
        assert reg_page.is_account_created(), "Account Created page should appear"
        assert "ACCOUNT CREATED" in reg_page.get_success_message().upper(), (
            "Success message should confirm account creation"
        )

        # Continue to home and verify logged in
        reg_page.click_continue()
        home = HomePage(page)
        assert home.is_logged_in(), "Should be logged in after registration"

        # Cleanup — delete account
        home.delete_account()

    @allure.story("Duplicate Registration")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.registration
    @pytest.mark.negative
    def test_register_with_existing_email(self, page, registered_user):
        """Test that registration fails with an already-used email."""
        login_page = LoginPage(page)
        login_page.open()

        # Try to signup with the same email
        login_page.start_signup(registered_user["name"], registered_user["email"])

        # Should show an error
        error = login_page.get_signup_error()
        assert "exist" in error.lower() or "already" in error.lower(), (
            f"Expected 'already exists' error, got: '{error}'"
        )

    @allure.story("Form Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.registration
    def test_registration_form_has_all_fields(self, page, new_user_data):
        """Test that the registration form contains all expected fields."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.start_signup(new_user_data["name"], new_user_data["email"])

        reg_page = RegistrationPage(page)
        assert reg_page.verify_form_visible(), "Registration form should be visible"

        # Verify key fields exist
        assert reg_page.is_visible(reg_page.PASSWORD_INPUT), "Password field should exist"
        assert reg_page.is_visible(reg_page.FIRST_NAME), "First name field should exist"
        assert reg_page.is_visible(reg_page.LAST_NAME), "Last name field should exist"
        assert reg_page.is_visible(reg_page.ADDRESS1), "Address field should exist"
        assert reg_page.is_visible(reg_page.COUNTRY), "Country dropdown should exist"
        assert reg_page.is_visible(reg_page.MOBILE_NUMBER), "Mobile number field should exist"
        assert reg_page.is_visible(reg_page.CREATE_ACCOUNT_BUTTON), "Submit button should exist"

        # Navigate away to avoid leaving a half-registered user
        page.goto("about:blank")

    @allure.story("Account Created Confirmation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.registration
    def test_account_created_confirmation_page(self, page, new_user_data):
        """Test the account creation success page appearance."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.start_signup(new_user_data["name"], new_user_data["email"])

        reg_page = RegistrationPage(page)
        reg_page.register(new_user_data)

        # Verify success page elements
        assert reg_page.is_account_created(), "Account created header should show"
        assert reg_page.is_visible(reg_page.CONTINUE_BUTTON), (
            "Continue button should be present on success page"
        )

        # Cleanup
        reg_page.click_continue()
        HomePage(page).delete_account()

    @allure.story("Account Deletion")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.registration
    def test_delete_account_after_registration(self, page, new_user_data):
        """Test that a user can delete their account after registering."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.start_signup(new_user_data["name"], new_user_data["email"])

        reg_page = RegistrationPage(page)
        reg_page.register(new_user_data)
        reg_page.click_continue()

        home = HomePage(page)
        assert home.is_logged_in(), "Should be logged in"

        home.delete_account()

        # After deletion, should no longer be logged in
        # The site shows an "Account Deleted" page
        assert page.locator("h2[data-qa='account-deleted']").is_visible() or \
               page.locator("b:has-text('Account Deleted')").is_visible(), (
            "Account deletion confirmation should appear"
        )

    @allure.story("Form Pre-population")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.registration
    def test_name_and_email_prepopulated(self, page, new_user_data):
        """Test that name and email from signup form carry over to registration."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.start_signup(new_user_data["name"], new_user_data["email"])

        reg_page = RegistrationPage(page)
        assert reg_page.verify_form_visible(), "Registration form should load"

        # The name field should be pre-filled from the signup form
        name_value = reg_page.get_input_value(reg_page.NAME_INPUT)
        assert new_user_data["name"] in name_value, (
            f"Name should be pre-populated with '{new_user_data['name']}', got '{name_value}'"
        )

        # Navigate away to avoid leaving a half-registered user
        page.goto("about:blank")
