"""
test_navigation.py — Site navigation tests.

Covers page loading, navigation between main pages, logo link,
and page title verification.
"""

import pytest
import allure
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.contact_page import ContactPage
from config.settings import settings
from utils.logger import get_logger

logger = get_logger("test_navigation")


@allure.epic("User Experience")
@allure.feature("Navigation")
class TestNavigation:
    """Test suite for site navigation and page integrity."""

    @allure.story("Home Page")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.navigation
    def test_home_page_loads(self, home_page):
        """Test that the home page loads successfully."""
        assert home_page.verify_page_loaded(), "Home page should load completely"
        assert home_page.is_nav_visible(), "Navigation bar should be visible"

    @allure.story("Page Navigation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.navigation
    def test_navigate_to_products(self, home_page):
        """Test navigation from home to products page."""
        home_page.go_to_products()

        products = ProductsPage(home_page.page)
        assert products.verify_page_loaded(), "Products page should load"
        assert "products" in products.current_url.lower(), (
            "URL should contain 'products'"
        )

    @allure.story("Page Navigation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.navigation
    def test_navigate_to_login(self, home_page):
        """Test navigation from home to login page."""
        home_page.go_to_login()

        login = LoginPage(home_page.page)
        assert login.verify_login_form_visible(), "Login form should be visible"
        assert "login" in login.current_url.lower(), (
            "URL should contain 'login'"
        )

    @allure.story("Page Navigation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.navigation
    def test_navigate_to_cart(self, home_page):
        """Test navigation from home to cart page."""
        home_page.go_to_cart()

        cart = CartPage(home_page.page)
        assert cart.verify_page_loaded(), "Cart page should load"
        assert "cart" in cart.current_url.lower() or "view_cart" in cart.current_url.lower(), (
            "URL should contain 'cart'"
        )

    @allure.story("Page Navigation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.navigation
    def test_navigate_to_contact(self, home_page):
        """Test navigation from home to Contact Us page."""
        home_page.go_to_contact()

        contact = ContactPage(home_page.page)
        assert contact.verify_page_loaded(), "Contact page should load"
        assert "contact" in contact.current_url.lower(), (
            "URL should contain 'contact'"
        )

    @allure.story("Logo")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.navigation
    def test_logo_links_to_home(self, page):
        """Test that clicking the logo navigates to the home page."""
        # Start from a different page
        page.goto(f"{settings.base_url}/products", wait_until="domcontentloaded")

        # Click logo
        page.click("div.logo a")

        # Should be at home
        home = HomePage(page)
        assert home.verify_page_loaded(), "Clicking logo should return to home"
        assert home.current_url.rstrip("/") == settings.base_url.rstrip("/") or \
               home.current_url.rstrip("/").endswith("/"), (
            "URL should be the home page"
        )

    @allure.story("Page Title")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.navigation
    @pytest.mark.xfail(reason="Known site issue: automationexercise.com returns empty <title> on some pages")
    def test_page_titles(self, home_page):
        """Test that each page has a proper title."""
        assert home_page.title, "Home page should have a title"

        # Navigate to products and check title
        home_page.go_to_products()
        assert home_page.title, "Products page should have a title"

        # Navigate to login and check title
        home_page.go_to_login()
        assert home_page.title, "Login page should have a title"
