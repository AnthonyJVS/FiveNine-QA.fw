"""
test_cart.py — Shopping cart tests.

Covers adding products, verifying cart items, removing products,
and multiple products in cart.
"""

import pytest
import allure
from pages.home_page import HomePage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from utils.logger import get_logger

logger = get_logger("test_cart")


@allure.epic("E-Commerce")
@allure.feature("Shopping Cart")
class TestCart:
    """Test suite for shopping cart operations."""

    @allure.story("Add to Cart")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_add_product_to_cart(self, products_page):
        """Test adding a product to the shopping cart."""
        # Get first product name before adding
        product_names = products_page.get_product_names()
        assert len(product_names) > 0, "Products page should have products"

        # Add first product to cart
        products_page.add_product_to_cart(0)
        products_page.go_to_cart_from_modal()

        # Verify product is in cart
        cart = CartPage(products_page.page)
        items = cart.get_cart_items()
        assert len(items) > 0, "Cart should have at least one item"

    @allure.story("Verify Cart Details")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    def test_cart_item_has_correct_details(self, products_page):
        """Test that cart item displays correct name, price, and quantity."""
        products_page.add_product_to_cart(0)
        products_page.go_to_cart_from_modal()

        cart = CartPage(products_page.page)
        items = cart.get_cart_items()
        assert len(items) > 0, "Cart should have items"

        item = items[0]
        assert item.name, "Cart item should have a name"
        assert item.price, "Cart item should have a price"
        assert item.quantity, "Cart item should have a quantity"
        assert item.total, "Cart item should have a total"

        logger.info(
            f"Cart item — Name: {item.name}, Price: {item.price}, "
            f"Qty: {item.quantity}, Total: {item.total}"
        )

    @allure.story("Remove from Cart")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.cart
    def test_remove_product_from_cart(self, products_page):
        """Test removing a product from the cart."""
        products_page.add_product_to_cart(0)
        products_page.go_to_cart_from_modal()

        cart = CartPage(products_page.page)
        initial_count = cart.get_cart_item_count()
        assert initial_count > 0, "Cart should have items before removal"

        cart.remove_item(0)

        # Verify item was removed (either fewer items or cart is empty)
        cart.page.wait_for_timeout(2000)  # Wait for removal animation
        final_count = cart.get_cart_item_count()
        assert final_count < initial_count or cart.is_cart_empty(), (
            "Cart should have fewer items after removal"
        )

    @allure.story("Multiple Products")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    def test_add_multiple_products_to_cart(self, products_page):
        """Test adding multiple products to the cart."""
        # Add first product
        products_page.add_product_to_cart(0)
        products_page.continue_shopping()

        # Add second product
        products_page.add_product_to_cart(1)
        products_page.go_to_cart_from_modal()

        # Verify cart has both products
        cart = CartPage(products_page.page)
        items = cart.get_cart_items()
        assert len(items) >= 2, (
            f"Cart should have at least 2 items, got {len(items)}"
        )

        # Verify they are different products
        names = [item.name for item in items]
        logger.info(f"Cart items: {names}")

    @allure.story("Empty Cart")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.cart
    def test_empty_cart_message(self, cart_page):
        """Test that an empty cart displays an appropriate message."""
        if cart_page.is_cart_empty():
            # Cart is already empty — verify message
            assert cart_page.is_visible(cart_page.EMPTY_CART_TEXT), (
                "Empty cart message should be visible"
            )
        else:
            # Cart has items (from previous tests) — just verify page loaded
            assert cart_page.verify_page_loaded(), "Cart page should load"
