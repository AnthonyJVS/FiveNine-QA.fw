"""
tests/ui/conftest.py — UI-specific fixtures.

Provides page object instances and common UI setup.
"""

import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from pages.products_page import ProductsPage
from pages.product_detail_page import ProductDetailPage
from pages.cart_page import CartPage
from pages.contact_page import ContactPage
from utils.fake_data import generate_user_data
from utils.logger import get_logger

logger = get_logger("ui_conftest")


# ──────────────────────────────────────────────
# Page object fixtures
# ──────────────────────────────────────────────

@pytest.fixture
def home_page(page):
    """Home page object, navigated to the home page."""
    hp = HomePage(page)
    hp.open()
    return hp


@pytest.fixture
def login_page(page):
    """Login page object, navigated to the login page."""
    lp = LoginPage(page)
    lp.open()
    return lp


@pytest.fixture
def products_page(page):
    """Products page object, navigated to the products page."""
    pp = ProductsPage(page)
    pp.open()
    return pp


@pytest.fixture
def cart_page(page):
    """Cart page object, navigated to the cart page."""
    cp = CartPage(page)
    cp.open()
    return cp


@pytest.fixture
def contact_page(page):
    """Contact page object, navigated to the contact page."""
    cp = ContactPage(page)
    cp.open()
    return cp


# ──────────────────────────────────────────────
# User data fixtures
# ──────────────────────────────────────────────

@pytest.fixture
def new_user_data():
    """Generate fresh user registration data for a test."""
    return generate_user_data()


@pytest.fixture
def registered_user(page, new_user_data):
    """
    Register a new user and return their credentials.

    Yields:
        dict with keys: name, email, password (and all registration data).

    Teardown:
        Deletes the account after the test completes.
    """
    login_pg = LoginPage(page)
    login_pg.open()
    login_pg.start_signup(new_user_data["name"], new_user_data["email"])

    reg_pg = RegistrationPage(page)
    reg_pg.fill_registration_form(new_user_data)
    reg_pg.submit()
    reg_pg.click_continue()

    logger.info(f"Registered test user: {new_user_data['email']}")

    # Ensure the user is logged out before yielding so the login test runs correctly
    home = HomePage(page)
    if home.is_logged_in():
        home.logout()

    yield new_user_data

    # Teardown — delete the test account
    try:
        home = HomePage(page)
        if home.is_logged_in():
            home.delete_account()
            logger.info(f"Deleted test user: {new_user_data['email']}")
    except Exception as e:
        logger.warning(f"Failed to clean up test user: {e}")
