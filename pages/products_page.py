"""
products_page.py — Page object for the Products listing page.

URL: https://automationexercise.com/products
"""

import allure
from pages.base_page import BasePage


class ProductsPage(BasePage):
    """Page object for the Products listing and search page."""

    # ──────────────────────────────────────────
    # Selectors
    # ──────────────────────────────────────────

    PAGE_HEADER = "h2.title.text-center:has-text('All Products')"
    SEARCHED_PRODUCTS_HEADER = "h2.title.text-center:has-text('Searched Products')"

    # Search
    SEARCH_INPUT = "#search_product"
    SEARCH_BUTTON = "#submit_search"

    # Product cards
    PRODUCT_CARD = "div.productinfo"
    PRODUCT_NAMES = "div.productinfo p"
    PRODUCT_PRICES = "div.productinfo h2"
    PRODUCT_IMAGE = "div.productinfo img"
    VIEW_PRODUCT_LINKS = "a[href^='/product_details/']"

    # Add to cart overlay
    ADD_TO_CART_BUTTON = "a.add-to-cart"
    CONTINUE_SHOPPING_BUTTON = "button.btn-success:has-text('Continue Shopping')"
    VIEW_CART_LINK = "a[href='/view_cart']:has-text('View Cart')"

    # Category sidebar
    CATEGORY_SIDEBAR = "div.left-sidebar"
    CATEGORY_WOMEN = "a[href='#Women']"
    CATEGORY_MEN = "a[href='#Men']"
    CATEGORY_KIDS = "a[href='#Kids']"

    # Brands sidebar
    BRANDS_SECTION = "div.brands_products"

    # ──────────────────────────────────────────
    # Actions
    # ──────────────────────────────────────────

    @allure.step("Open products page")
    def open(self):
        """Navigate to the products listing page."""
        self.navigate("/products")
        return self

    @allure.step("Verify products page is loaded")
    def verify_page_loaded(self) -> bool:
        """Check that the products page loaded with products visible."""
        return (
            self.is_visible(self.PAGE_HEADER)
            and self.get_element_count(self.PRODUCT_CARD) > 0
        )

    @allure.step("Search for product: {query}")
    def search_product(self, query: str):
        """
        Search for a product by name.

        Args:
            query: Search term (e.g., 'top', 'tshirt', 'dress').
        """
        self.fill(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)

    def get_product_names(self) -> list[str]:
        """Get names of all visible products."""
        return self.get_all_texts(self.PRODUCT_NAMES)

    def get_product_count(self) -> int:
        """Get the number of visible product cards."""
        return self.get_element_count(self.PRODUCT_CARD)

    def is_searched_products_visible(self) -> bool:
        """Check if 'Searched Products' header is visible after a search."""
        return self.is_visible(self.SEARCHED_PRODUCTS_HEADER)

    @allure.step("Click View Product for product at index {index}")
    def view_product(self, index: int = 0):
        """Click 'View Product' link for a product at the given index."""
        links = self.page.locator(self.VIEW_PRODUCT_LINKS)
        if links.count() > index:
            links.nth(index).click()

    @allure.step("Add product at index {index} to cart")
    def add_product_to_cart(self, index: int = 0):
        """Hover over a product and click 'Add to cart'."""
        self._dismiss_consent_overlay()
        products = self.page.locator("div.product-image-wrapper")
        if products.count() > index:
            product = products.nth(index)
            product.hover()
            self._dismiss_consent_overlay()
            overlay_add = product.locator("a.add-to-cart")
            overlay_add.first.click()
            # Wait for the add-to-cart modal to appear
            self.page.wait_for_selector("div.modal-content", state="visible", timeout=5000)

    @allure.step("Click Continue Shopping")
    def continue_shopping(self):
        """Click 'Continue Shopping' in the add-to-cart modal."""
        self.click(self.CONTINUE_SHOPPING_BUTTON)

    @allure.step("Click View Cart from modal")
    def go_to_cart_from_modal(self):
        """Click 'View Cart' link in the add-to-cart modal."""
        self._dismiss_consent_overlay()
        # Wait for the modal to appear and the View Cart link to be visible
        self.page.wait_for_selector(
            "div.modal-content a[href='/view_cart']",
            state="visible",
            timeout=10000,
        )
        self.click("div.modal-content a[href='/view_cart']")

    # ──────────────────────────────────────────
    # Category navigation
    # ──────────────────────────────────────────

    def is_category_sidebar_visible(self) -> bool:
        """Check if the category sidebar is visible."""
        return self.is_visible(self.CATEGORY_SIDEBAR)

    @allure.step("Click category: {category}")
    def click_category(self, category: str):
        """Click a category in the sidebar."""
        self.click(f"a[href='#{category}']")
