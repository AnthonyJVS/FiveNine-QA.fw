"""
cart_page.py — Page object for the Shopping Cart page.

URL: https://automationexercise.com/view_cart
"""

import allure
from dataclasses import dataclass
from pages.base_page import BasePage


@dataclass
class CartItem:
    """Structured cart item data."""
    name: str
    price: str
    quantity: str
    total: str


class CartPage(BasePage):
    """Page object for the shopping cart page."""

    # ──────────────────────────────────────────
    # Selectors
    # ──────────────────────────────────────────

    CART_TABLE = "#cart_info_table"
    CART_ROWS = "#cart_info_table tbody tr"
    CART_PRODUCT_NAME = "td.cart_description h4 a"
    CART_PRODUCT_PRICE = "td.cart_price p"
    CART_PRODUCT_QUANTITY = "td.cart_quantity button"
    CART_PRODUCT_TOTAL = "td.cart_total p"
    CART_DELETE_BUTTON = "td.cart_delete a"

    EMPTY_CART_TEXT = "#empty_cart"
    PROCEED_TO_CHECKOUT = "a.check_out"

    # ──────────────────────────────────────────
    # Actions
    # ──────────────────────────────────────────

    @allure.step("Open cart page")
    def open(self):
        """Navigate to the cart page."""
        self.navigate("/view_cart")
        return self

    @allure.step("Verify cart page is loaded")
    def verify_page_loaded(self) -> bool:
        """Check that the cart page loaded."""
        return self.is_visible(self.CART_TABLE) or self.is_visible(self.EMPTY_CART_TEXT)

    def get_cart_items(self) -> list[CartItem]:
        """
        Extract all items from the cart table.

        Returns:
            List of CartItem dataclass instances.
        """
        items = []
        rows = self.page.locator(self.CART_ROWS)

        for i in range(rows.count()):
            row = rows.nth(i)
            name_el = row.locator("td.cart_description h4 a")

            # Skip rows without a product name (e.g., header rows)
            if name_el.count() == 0:
                continue

            items.append(CartItem(
                name=name_el.text_content().strip(),
                price=row.locator("td.cart_price p").text_content().strip(),
                quantity=row.locator("td.cart_quantity button").text_content().strip(),
                total=row.locator("td.cart_total p").text_content().strip(),
            ))

        return items

    def get_cart_item_count(self) -> int:
        """Get the number of items in the cart."""
        return len(self.get_cart_items())

    @allure.step("Remove item at index {index} from cart")
    def remove_item(self, index: int = 0):
        """Remove a cart item by its row index."""
        delete_buttons = self.page.locator(self.CART_DELETE_BUTTON)
        if delete_buttons.count() > index:
            delete_buttons.nth(index).click()
            # Wait for the item to be removed
            self.page.wait_for_timeout(1000)

    def is_cart_empty(self) -> bool:
        """Check if the cart is empty."""
        return self.is_visible(self.EMPTY_CART_TEXT)

    def get_empty_cart_text(self) -> str:
        """Get the empty cart message text."""
        return self.get_text(self.EMPTY_CART_TEXT)

    @allure.step("Proceed to checkout")
    def proceed_to_checkout(self):
        """Click the Proceed to Checkout button."""
        self.click(self.PROCEED_TO_CHECKOUT)

    def verify_item_in_cart(self, product_name: str) -> bool:
        """Check if a specific product is in the cart."""
        items = self.get_cart_items()
        return any(product_name.lower() in item.name.lower() for item in items)
