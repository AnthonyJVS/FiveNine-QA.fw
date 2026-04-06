"""
registration_page.py — Page object for the Account Registration form.

URL: https://automationexercise.com/signup
(Reached after submitting the signup form on the login page)
"""

import allure
from pages.base_page import BasePage


class RegistrationPage(BasePage):
    """Page object for the user registration / account information form."""

    # ──────────────────────────────────────────
    # Selectors
    # ──────────────────────────────────────────

    # Page header
    PAGE_HEADER = "h2.title:has-text('Enter Account Information')"

    # Title / Gender
    TITLE_MR = "#id_gender1"
    TITLE_MRS = "#id_gender2"

    # Account info
    NAME_INPUT = "input[data-qa='name']"
    PASSWORD_INPUT = "input[data-qa='password']"
    EMAIL_INPUT = "input[data-qa='email']"

    # Date of birth
    DOB_DAY = "select[data-qa='days']"
    DOB_MONTH = "select[data-qa='months']"
    DOB_YEAR = "select[data-qa='years']"

    # Checkboxes
    NEWSLETTER_CHECKBOX = "#newsletter"
    SPECIAL_OFFERS_CHECKBOX = "#optin"

    # Address info
    FIRST_NAME = "input[data-qa='first_name']"
    LAST_NAME = "input[data-qa='last_name']"
    COMPANY = "input[data-qa='company']"
    ADDRESS1 = "input[data-qa='address']"
    ADDRESS2 = "input[data-qa='address2']"
    COUNTRY = "select[data-qa='country']"
    STATE = "input[data-qa='state']"
    CITY = "input[data-qa='city']"
    ZIPCODE = "input[data-qa='zipcode']"
    MOBILE_NUMBER = "input[data-qa='mobile_number']"

    # Submit
    CREATE_ACCOUNT_BUTTON = "button[data-qa='create-account']"

    # Success page
    ACCOUNT_CREATED_HEADER = "h2[data-qa='account-created']"
    CONTINUE_BUTTON = "a[data-qa='continue-button']"

    # ──────────────────────────────────────────
    # Actions
    # ──────────────────────────────────────────

    @allure.step("Verify registration form is visible")
    def verify_form_visible(self) -> bool:
        """Check that the registration form loaded."""
        return self.is_visible(self.PAGE_HEADER)

    @allure.step("Fill registration form with user data")
    def fill_registration_form(self, data: dict):
        """
        Fill out the complete registration form.

        Args:
            data: Dictionary containing user registration fields.
                  Expected keys: title, password, birth_date, birth_month,
                  birth_year, firstname, lastname, company, address1,
                  address2, country, state, city, zipcode, mobile_number.
        """
        # Title / Gender
        if data.get("title") == "Mrs":
            self.click(self.TITLE_MRS)
        else:
            self.click(self.TITLE_MR)

        # Password
        self.fill(self.PASSWORD_INPUT, data["password"])

        # Date of birth
        self.select_option(self.DOB_DAY, data["birth_date"])
        self.select_option(self.DOB_MONTH, data["birth_month"])
        self.select_option(self.DOB_YEAR, data["birth_year"])

        # Newsletter & offers
        self.check(self.NEWSLETTER_CHECKBOX)
        self.check(self.SPECIAL_OFFERS_CHECKBOX)

        # Address information
        self.fill(self.FIRST_NAME, data["firstname"])
        self.fill(self.LAST_NAME, data["lastname"])
        self.fill(self.COMPANY, data.get("company", ""))
        self.fill(self.ADDRESS1, data["address1"])
        self.fill(self.ADDRESS2, data.get("address2", ""))
        self.select_option(self.COUNTRY, data["country"])
        self.fill(self.STATE, data["state"])
        self.fill(self.CITY, data["city"])
        self.fill(self.ZIPCODE, data["zipcode"])
        self.fill(self.MOBILE_NUMBER, data["mobile_number"])

    @allure.step("Submit registration form")
    def submit(self):
        """Click the Create Account button."""
        self.click(self.CREATE_ACCOUNT_BUTTON)

    @allure.step("Fill and submit registration form")
    def register(self, data: dict):
        """Fill and submit the registration form in one step."""
        self.fill_registration_form(data)
        self.submit()

    # ──────────────────────────────────────────
    # Verification
    # ──────────────────────────────────────────

    def is_account_created(self) -> bool:
        """Check if the 'Account Created' success page is shown."""
        return self.is_visible(self.ACCOUNT_CREATED_HEADER)

    def get_success_message(self) -> str:
        """Get the account created confirmation text."""
        return self.get_text(self.ACCOUNT_CREATED_HEADER)

    @allure.step("Click Continue after account creation")
    def click_continue(self):
        """Click Continue button on the success page."""
        self.click(self.CONTINUE_BUTTON)
