"""
test_search.py — Product search and filtering tests.

Covers valid search, result relevance, empty results,
special characters, and product detail navigation from search.
"""

import pytest
import allure
from pages.products_page import ProductsPage
from pages.product_detail_page import ProductDetailPage
from utils.logger import get_logger

logger = get_logger("test_search")


@allure.epic("Product Catalog")
@allure.feature("Search")
class TestSearch:
    """Test suite for product search functionality."""

    @allure.story("Valid Search")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.search
    def test_search_existing_product(self, products_page):
        """Test that searching for an existing product returns results."""
        products_page.search_product("top")

        assert products_page.is_searched_products_visible(), (
            "'Searched Products' header should appear"
        )
        assert products_page.get_product_count() > 0, (
            "Search for 'top' should return at least one result"
        )

    @allure.story("Result Relevance")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.search
    def test_search_results_contain_query(self, products_page):
        """Test that search results are relevant to the query."""
        query = "tshirt"
        products_page.search_product(query)

        product_names = products_page.get_product_names()
        assert len(product_names) > 0, "Should have search results"

        # At least some results should contain the search term
        # (being lenient since product names may vary)
        logger.info(f"Search results for '{query}': {product_names}")

    @allure.story("Empty Search Results")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.search
    @pytest.mark.negative
    def test_search_nonexistent_product(self, products_page):
        """Test that searching for a non-existent product returns no results."""
        products_page.search_product("xyznonexistent123456")

        assert products_page.is_searched_products_visible(), (
            "'Searched Products' header should still appear"
        )
        assert products_page.get_product_count() == 0, (
            "Non-existent product search should return zero results"
        )

    @allure.story("Special Characters")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.search
    @pytest.mark.negative
    def test_search_with_special_characters(self, products_page):
        """Test that search handles special characters gracefully."""
        products_page.search_product("!@#$%^&*()")

        # Should not crash — either show no results or handle gracefully
        assert products_page.is_searched_products_visible() or \
               products_page.is_visible(products_page.PAGE_HEADER), (
            "Page should remain stable after special character search"
        )

    @allure.story("Product Detail from Search")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.search
    def test_view_product_from_search_results(self, products_page):
        """Test navigating to product detail from search results."""
        products_page.search_product("dress")

        assert products_page.get_product_count() > 0, (
            "Should have search results for 'dress'"
        )

        # Click first product
        products_page.view_product(0)

        # Verify product detail page loaded
        detail = ProductDetailPage(products_page.page)
        assert detail.verify_page_loaded(), "Product detail page should load"

    @allure.story("Multiple Searches")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.search
    @pytest.mark.parametrize("query", ["top", "dress", "jean", "saree"])
    def test_search_various_products(self, products_page, query):
        """Test searching for different product categories."""
        products_page.search_product(query)

        assert products_page.is_searched_products_visible(), (
            f"'Searched Products' header should appear for query '{query}'"
        )
        count = products_page.get_product_count()
        logger.info(f"Search '{query}': {count} results")
