"""
contact_page.py — Page object for the Contact Us page.

URL: https://automationexercise.com/contact_us
"""

import allure
from pages.base_page import BasePage


class ContactPage(BasePage):
    """Page object for the Contact Us form."""

    # ──────────────────────────────────────────
    # Selectors
    # ──────────────────────────────────────────

    PAGE_HEADER = "h2.title:has-text('Get In Touch')"

    NAME_INPUT = "input[data-qa='name']"
    EMAIL_INPUT = "input[data-qa='email']"
    SUBJECT_INPUT = "input[data-qa='subject']"
    MESSAGE_INPUT = "#message"
    FILE_UPLOAD = "input[name='upload_file']"
    SUBMIT_BUTTON = "input[data-qa='submit-button']"

    SUCCESS_MESSAGE = "div.alert-success"
    HOME_BUTTON = "a.btn-success:has-text('Home')"

    # ──────────────────────────────────────────
    # Actions
    # ──────────────────────────────────────────

    @allure.step("Open Contact Us page")
    def open(self):
        """Navigate to the Contact Us page."""
        self.navigate("/contact_us")
        return self

    @allure.step("Verify Contact Us page is loaded")
    def verify_page_loaded(self) -> bool:
        """Check that the Contact Us form is visible."""
        return self.is_visible(self.PAGE_HEADER)

    @allure.step("Fill contact form")
    def fill_contact_form(self, data: dict):
        """
        Fill out the contact form fields.

        Args:
            data: Dictionary with keys: name, email, subject, message.
        """
        self.fill(self.NAME_INPUT, data["name"])
        self.fill(self.EMAIL_INPUT, data["email"])
        self.fill(self.SUBJECT_INPUT, data["subject"])
        self.fill(self.MESSAGE_INPUT, data["message"])

    @allure.step("Upload file to contact form")
    def attach_file(self, file_path: str):
        """Attach a file to the contact form."""
        self.upload_file(self.FILE_UPLOAD, file_path)

    @allure.step("Submit contact form")
    def submit(self):
        """Click the Submit button and handle the confirmation dialog."""
        # The site shows a JavaScript alert on submit
        self.page.on("dialog", lambda dialog: dialog.accept())
        self.click(self.SUBMIT_BUTTON)

    @allure.step("Fill and submit contact form")
    def send_message(self, data: dict, file_path: str = None):
        """Fill the form, optionally attach a file, and submit."""
        self.fill_contact_form(data)
        if file_path:
            self.attach_file(file_path)
        self.submit()

    # ──────────────────────────────────────────
    # Verification
    # ──────────────────────────────────────────

    def is_success_message_visible(self) -> bool:
        """Check if the success message is displayed after submission."""
        return self.is_visible(self.SUCCESS_MESSAGE)

    def get_success_message(self) -> str:
        """Get the success message text."""
        return self.get_text(self.SUCCESS_MESSAGE)

    @allure.step("Click Home button after submission")
    def click_home(self):
        """Click the Home button on the success page."""
        self.click(self.HOME_BUTTON)

    def is_form_visible(self) -> bool:
        """Check if the contact form fields are visible."""
        return all([
            self.is_visible(self.NAME_INPUT),
            self.is_visible(self.EMAIL_INPUT),
            self.is_visible(self.SUBJECT_INPUT),
            self.is_visible(self.MESSAGE_INPUT),
            self.is_visible(self.SUBMIT_BUTTON),
        ])
