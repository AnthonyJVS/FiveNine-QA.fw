"""
home_page.py — Page object for the Home / Landing page.

URL: https://automationexercise.com/
"""

import allure
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page object for the automationexercise.com home page."""

    # ──────────────────────────────────────────
    # Selectors
    # ──────────────────────────────────────────

    # Navigation bar
    NAV_HOME = "a[href='/']:has-text('Home')"
    NAV_PRODUCTS = "a[href='/products']"
    NAV_CART = "a[href='/view_cart']"
    NAV_LOGIN = "a[href='/login']"
    NAV_CONTACT = "a[href='/contact_us']"
    NAV_TEST_CASES = "a[href='/test_cases']"
    NAV_LOGOUT = "a[href='/logout']"
    NAV_DELETE_ACCOUNT = "a[href='/delete_account']"
    NAV_LOGGED_IN_AS = "li:has-text('Logged in as')"

    # Page elements
    LOGO = "div.logo img"
    SLIDER = "#slider"
    FEATURES_SECTION = "div.features_items"
    SUBSCRIPTION_INPUT = "#susbscribe_email"
    SUBSCRIPTION_BUTTON = "#subscribe"
    SUBSCRIPTION_SUCCESS = "#success-subscribe .alert-success"
    FOOTER = "#footer"
    CATEGORY_SIDEBAR = "div.left-sidebar"

    # ──────────────────────────────────────────
    # Actions
    # ──────────────────────────────────────────

    @allure.step("Open home page")
    def open(self):
        """Navigate to the home page."""
        self.navigate("/")
        return self

    @allure.step("Verify home page is loaded")
    def verify_page_loaded(self) -> bool:
        """Verify the home page loaded successfully."""
        self.wait_for_element(self.FEATURES_SECTION)
        return self.is_visible(self.LOGO) and self.is_visible(self.SLIDER)

    @allure.step("Navigate to Products page")
    def go_to_products(self):
        """Click the Products link in the navigation bar."""
        self.click(self.NAV_PRODUCTS)

    @allure.step("Navigate to Cart page")
    def go_to_cart(self):
        """Click the Cart link in the navigation bar."""
        self.click(self.NAV_CART)

    @allure.step("Navigate to Login page")
    def go_to_login(self):
        """Click the Signup/Login link in the navigation bar."""
        self.click(self.NAV_LOGIN)

    @allure.step("Navigate to Contact Us page")
    def go_to_contact(self):
        """Click the Contact Us link in the navigation bar."""
        self.click(self.NAV_CONTACT)

    @allure.step("Navigate to Test Cases page")
    def go_to_test_cases(self):
        """Click the Test Cases link in the navigation bar."""
        self.click(self.NAV_TEST_CASES)

    @allure.step("Logout")
    def logout(self):
        """Click the Logout link."""
        self.click(self.NAV_LOGOUT)

    @allure.step("Delete account")
    def delete_account(self):
        """Click the Delete Account link."""
        self.click(self.NAV_DELETE_ACCOUNT)

    # ──────────────────────────────────────────
    # Verification methods
    # ──────────────────────────────────────────

    def is_logged_in(self) -> bool:
        """Check if a user is currently logged in."""
        return self.is_visible(self.NAV_LOGGED_IN_AS)

    def get_logged_in_username(self) -> str:
        """Get the username displayed in the 'Logged in as' text."""
        text = self.get_text(self.NAV_LOGGED_IN_AS)
        # Text format: "Logged in as <username>"
        return text.replace("Logged in as", "").strip()

    def is_nav_visible(self) -> bool:
        """Verify main navigation links are visible."""
        return all([
            self.is_visible(self.NAV_HOME),
            self.is_visible(self.NAV_PRODUCTS),
            self.is_visible(self.NAV_CART),
            self.is_visible(self.NAV_LOGIN),
        ])

    @allure.step("Subscribe with email")
    def subscribe(self, email: str):
        """Enter email and subscribe."""
        self.scroll_to_element(self.SUBSCRIPTION_INPUT)
        self.fill(self.SUBSCRIPTION_INPUT, email)
        self.click(self.SUBSCRIPTION_BUTTON)

    def is_subscription_success(self) -> bool:
        """Check if subscription success message appeared."""
        return self.is_visible(self.SUBSCRIPTION_SUCCESS)
