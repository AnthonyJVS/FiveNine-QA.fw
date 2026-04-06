"""
product_detail_page.py — Page object for the Product Detail page.

URL: https://automationexercise.com/product_details/<id>
"""

import allure
from dataclasses import dataclass
from typing import Optional
from pages.base_page import BasePage


@dataclass
class ProductInfo:
    """Structured product detail data."""
    name: str
    category: str
    price: str
    availability: str
    condition: str
    brand: str


class ProductDetailPage(BasePage):
    """Page object for an individual product detail page."""

    # ──────────────────────────────────────────
    # Selectors
    # ──────────────────────────────────────────

    PRODUCT_NAME = "div.product-information h2"
    PRODUCT_CATEGORY = "div.product-information p:nth-of-type(1)"
    PRODUCT_PRICE = "div.product-information span span"
    PRODUCT_AVAILABILITY = "div.product-information p:has-text('Availability')"
    PRODUCT_CONDITION = "div.product-information p:has-text('Condition')"
    PRODUCT_BRAND = "div.product-information p:has-text('Brand')"
    PRODUCT_IMAGE = "div.view-product img"

    QUANTITY_INPUT = "#quantity"
    ADD_TO_CART_BUTTON = "button.cart"

    CONTINUE_SHOPPING = "button:has-text('Continue Shopping')"
    VIEW_CART = "a:has-text('View Cart')"

    # Review section
    WRITE_REVIEW_HEADER = "a[href='#reviews']:has-text('Write Your Review')"
    REVIEW_NAME = "#name"
    REVIEW_EMAIL = "#email"
    REVIEW_TEXT = "#review"
    REVIEW_SUBMIT = "#button-review"
    REVIEW_SUCCESS = "div.alert-success span"

    # ──────────────────────────────────────────
    # Actions
    # ──────────────────────────────────────────

    @allure.step("Get product information")
    def get_product_info(self) -> ProductInfo:
        """
        Extract all product details from the page.

        Returns:
            ProductInfo dataclass with name, category, price, etc.
        """
        return ProductInfo(
            name=self.get_text(self.PRODUCT_NAME),
            category=self.get_text(self.PRODUCT_CATEGORY),
            price=self.get_text(self.PRODUCT_PRICE),
            availability=self.get_text(self.PRODUCT_AVAILABILITY),
            condition=self.get_text(self.PRODUCT_CONDITION),
            brand=self.get_text(self.PRODUCT_BRAND),
        )

    @allure.step("Set quantity to {quantity}")
    def set_quantity(self, quantity: int):
        """Set the product quantity."""
        self.page.locator(self.QUANTITY_INPUT).fill(str(quantity))

    @allure.step("Add product to cart")
    def add_to_cart(self, quantity: Optional[int] = None):
        """Add the product to cart, optionally setting quantity first."""
        if quantity is not None:
            self.set_quantity(quantity)
        self.click(self.ADD_TO_CART_BUTTON)

    @allure.step("Verify product detail page is loaded")
    def verify_page_loaded(self) -> bool:
        """Check that product details are visible."""
        return all([
            self.is_visible(self.PRODUCT_NAME),
            self.is_visible(self.PRODUCT_PRICE),
            self.is_visible(self.ADD_TO_CART_BUTTON),
        ])

    @allure.step("Write a product review")
    def write_review(self, name: str, email: str, review_text: str):
        """
        Submit a product review.

        Args:
            name: Reviewer name.
            email: Reviewer email.
            review_text: Review content.
        """
        self.scroll_to_element(self.WRITE_REVIEW_HEADER)
        self.fill(self.REVIEW_NAME, name)
        self.fill(self.REVIEW_EMAIL, email)
        self.fill(self.REVIEW_TEXT, review_text)
        self.click(self.REVIEW_SUBMIT)

    def is_review_success(self) -> bool:
        """Check if the review submission success message is visible."""
        return self.is_visible(self.REVIEW_SUCCESS)
