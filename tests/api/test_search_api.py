"""
test_search_api.py — API tests for the Search Product endpoint.

Tests POST /searchProduct with valid queries, missing parameters,
result matching, and non-existent products.
"""

import pytest
import allure
from utils.logger import get_logger

logger = get_logger("test_search_api")


@allure.epic("API Testing")
@allure.feature("Search API")
class TestSearchAPI:
    """Test suite for the Search Product API endpoint."""

    @allure.story("Valid Search")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    def test_search_product_returns_results(self, api_client):
        """Test that POST /searchProduct with a valid query returns 200."""
        response = api_client.post(
            "/searchProduct",
            data={"search_product": "top"}
        )
        api_client.assert_status(response, 200)

        data = response.json()
        assert "products" in data, "Response should contain 'products' key"
        assert len(data["products"]) > 0, "Search for 'top' should return results"

    @allure.story("Missing Parameter")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.negative
    def test_search_without_parameter_returns_400(self, api_client):
        """Test that POST /searchProduct without search_product returns 400."""
        response = api_client.post("/searchProduct")

        data = response.json()
        assert data.get("responseCode") == 400 or response.status_code == 400, (
            "Missing search_product parameter should return 400"
        )
        logger.info(f"Missing param response: {data}")

    @allure.story("Result Matching")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_search_results_match_query(self, api_client):
        """Test that search results are relevant to the search query."""
        query = "tshirt"
        response = api_client.post(
            "/searchProduct",
            data={"search_product": query}
        )
        data = response.json()
        products = data.get("products", [])

        assert len(products) > 0, f"Search for '{query}' should return results"

        # Log product names for inspection
        names = [p.get("name", "unnamed") for p in products]
        logger.info(f"Search '{query}' returned: {names}")

    @allure.story("Non-Existent Product")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.negative
    def test_search_nonexistent_product(self, api_client):
        """Test searching for a product that doesn't exist."""
        response = api_client.post(
            "/searchProduct",
            data={"search_product": "xyznonexistent123456"}
        )
        api_client.assert_status(response, 200)

        data = response.json()
        products = data.get("products", [])
        assert len(products) == 0, (
            f"Search for non-existent product should return empty list, "
            f"got {len(products)} results"
        )

    @allure.story("Search Variations")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.api
    @pytest.mark.parametrize("query", ["top", "dress", "jean", "saree"])
    def test_search_various_categories(self, api_client, query):
        """Test searching for different product categories via API."""
        response = api_client.post(
            "/searchProduct",
            data={"search_product": query}
        )
        api_client.assert_status(response, 200)

        data = response.json()
        count = len(data.get("products", []))
        logger.info(f"API search '{query}': {count} results")
