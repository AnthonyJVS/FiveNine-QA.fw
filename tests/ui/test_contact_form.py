"""
test_contact_form.py — Contact Us form tests.

Covers valid submission, form validation, success message,
and form element verification.
"""

import pytest
import allure
from pages.contact_page import ContactPage
from utils.fake_data import generate_contact_data
from utils.logger import get_logger

logger = get_logger("test_contact_form")


@allure.epic("User Experience")
@allure.feature("Contact Form")
class TestContactForm:
    """Test suite for the Contact Us form."""

    @allure.story("Valid Submission")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.contact
    def test_submit_contact_form_with_valid_data(self, contact_page):
        """Test submitting the contact form with all valid fields."""
        data = generate_contact_data()

        contact_page.send_message(data)

        assert contact_page.is_success_message_visible(), (
            "Success message should appear after valid submission"
        )
        success_text = contact_page.get_success_message()
        logger.info(f"Contact form success message: {success_text}")

    @allure.story("Form Elements")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.contact
    def test_contact_form_elements_visible(self, contact_page):
        """Test that all contact form fields are present."""
        assert contact_page.verify_page_loaded(), "Contact page should load"
        assert contact_page.is_form_visible(), (
            "All contact form fields should be visible"
        )

    @allure.story("Page Header")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.contact
    def test_contact_page_header(self, contact_page):
        """Test that the 'Get In Touch' header is displayed."""
        assert contact_page.is_visible(contact_page.PAGE_HEADER), (
            "'Get In Touch' header should be visible"
        )

    @allure.story("Success Message Content")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.contact
    def test_success_message_content(self, contact_page):
        """Test that the success message contains appropriate text."""
        data = generate_contact_data()
        contact_page.send_message(data)

        assert contact_page.is_success_message_visible(), (
            "Success message should appear"
        )

        success_text = contact_page.get_success_message()
        # The site typically shows something like "Success! Your details have been submitted successfully."
        assert "success" in success_text.lower() or "submitted" in success_text.lower(), (
            f"Success message should confirm submission, got: '{success_text}'"
        )

    @allure.story("Navigation After Submission")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.contact
    def test_navigate_home_after_submission(self, contact_page):
        """Test navigating home after successful contact form submission."""
        data = generate_contact_data()
        contact_page.send_message(data)

        assert contact_page.is_success_message_visible(), (
            "Success message should appear"
        )

        contact_page.click_home()

        # Should be on the home page
        from pages.home_page import HomePage
        home = HomePage(contact_page.page)
        assert home.verify_page_loaded(), "Should navigate to home page"
