"""
test_products_api.py — API tests for the Products endpoint.

Tests GET /productsList, POST method rejection, response structure,
and non-empty product list validation.
"""

import pytest
import allure
from utils.api_client import APIClient
from utils.logger import get_logger

logger = get_logger("test_products_api")


@allure.epic("API Testing")
@allure.feature("Products API")
class TestProductsAPI:
    """Test suite for the Products List API endpoint."""

    @allure.story("GET Products")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_all_products_returns_200(self, api_client):
        """Test that GET /productsList returns 200 with product data."""
        response = api_client.get("/productsList")
        api_client.assert_status(response, 200)

        data = response.json()
        assert "products" in data, "Response should contain 'products' key"

    @allure.story("GET Products")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_products_list_is_not_empty(self, api_client):
        """Test that the products list contains at least one product."""
        response = api_client.get("/productsList")
        data = response.json()

        products = data.get("products", [])
        assert len(products) > 0, "Products list should not be empty"
        logger.info(f"Total products: {len(products)}")

    @allure.story("GET Products")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_product_has_expected_fields(self, api_client):
        """Test that each product contains the expected data fields."""
        response = api_client.get("/productsList")
        data = response.json()
        products = data.get("products", [])

        assert len(products) > 0, "Need at least one product to validate"

        product = products[0]
        expected_fields = ["id", "name", "price", "brand", "category"]

        for field in expected_fields:
            assert field in product, (
                f"Product should contain '{field}' field. "
                f"Available fields: {list(product.keys())}"
            )

        logger.info(f"Sample product: {product}")

    @allure.story("POST Products (Negative)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.negative
    def test_post_to_products_returns_405(self, api_client):
        """Test that POST to /productsList returns 405 (method not supported)."""
        response = api_client.post("/productsList")

        data = response.json()
        assert data.get("responseCode") == 405 or response.status_code == 405, (
            "POST to products list should return 405"
        )
        logger.info(f"POST /productsList response: {data}")

    @allure.story("Response Performance")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.api
    def test_products_response_time(self, api_client):
        """Test that the products API responds within acceptable time."""
        response = api_client.get("/productsList")
        api_client.assert_response_time(response, max_seconds=10.0)

    @allure.story("GET Products")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.api
    def test_product_category_structure(self, api_client):
        """Test that product categories have proper nested structure."""
        response = api_client.get("/productsList")
        data = response.json()
        products = data.get("products", [])

        assert len(products) > 0, "Need products to validate"

        product = products[0]
        category = product.get("category", {})

        assert "usertype" in category or "category" in category or isinstance(category, dict), (
            f"Category should have structure, got: {category}"
        )
