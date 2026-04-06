"""
test_smoke.py — Smoke test suite for quick CI sanity checks.

These tests verify that the most critical paths are functional.
They should run fast and catch major regressions.
"""

import pytest
import allure
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.contact_page import ContactPage
from utils.api_client import APIClient
from config.settings import settings
from utils.logger import get_logger

logger = get_logger("test_smoke")


@allure.epic("Smoke Tests")
@allure.feature("Critical Path Validation")
@pytest.mark.smoke
class TestSmoke:
    """
    Smoke test suite — quick sanity checks for major features.

    Run with: pytest -m smoke
    """

    @allure.story("Home Page")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_home_page_accessible(self, page):
        """Smoke: Home page loads and displays content."""
        home = HomePage(page)
        home.open()
        assert home.verify_page_loaded(), "Home page must load"

    @allure.story("Login Page")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_page_accessible(self, page):
        """Smoke: Login page loads and shows login form."""
        login = LoginPage(page)
        login.open()
        assert login.verify_login_form_visible(), "Login form must be visible"

    @allure.story("Products Page")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_products_page_has_products(self, page):
        """Smoke: Products page loads and shows products."""
        products = ProductsPage(page)
        products.open()
        assert products.verify_page_loaded(), "Products page must load"
        assert products.get_product_count() > 0, "Products must be displayed"

    @allure.story("Search")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_returns_results(self, page):
        """Smoke: Product search returns results."""
        products = ProductsPage(page)
        products.open()
        products.search_product("top")
        assert products.get_product_count() > 0, "Search should return results"

    @allure.story("Cart")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_cart_accessible(self, page):
        """Smoke: Cart page is accessible."""
        cart = CartPage(page)
        cart.open()
        assert cart.verify_page_loaded(), "Cart page must load"

    @allure.story("Contact")
    @allure.severity(allure.severity_level.NORMAL)
    def test_contact_page_accessible(self, page):
        """Smoke: Contact page loads with form."""
        contact = ContactPage(page)
        contact.open()
        assert contact.verify_page_loaded(), "Contact page must load"

    @allure.story("API Health")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_api_products_endpoint_healthy(self):
        """Smoke: API products endpoint returns 200."""
        client = APIClient()
        response = client.get("/productsList")
        client.assert_status(response, 200)
        client.close()

    @allure.story("API Health")
    @allure.severity(allure.severity_level.NORMAL)
    def test_api_brands_endpoint_healthy(self):
        """Smoke: API brands endpoint returns 200."""
        client = APIClient()
        response = client.get("/brandsList")
        client.assert_status(response, 200)
        client.close()
