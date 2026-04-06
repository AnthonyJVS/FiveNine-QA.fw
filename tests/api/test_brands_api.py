"""
test_brands_api.py — API tests for the Brands endpoint.

Tests GET /brandsList, PUT method rejection, and response structure.
"""

import pytest
import allure
from utils.logger import get_logger

logger = get_logger("test_brands_api")


@allure.epic("API Testing")
@allure.feature("Brands API")
class TestBrandsAPI:
    """Test suite for the Brands List API endpoint."""

    @allure.story("GET Brands")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    def test_get_all_brands_returns_200(self, api_client):
        """Test that GET /brandsList returns 200 with brand data."""
        response = api_client.get("/brandsList")
        api_client.assert_status(response, 200)

        data = response.json()
        assert "brands" in data, "Response should contain 'brands' key"

    @allure.story("GET Brands")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_brands_list_is_not_empty(self, api_client):
        """Test that the brands list contains at least one brand."""
        response = api_client.get("/brandsList")
        data = response.json()

        brands = data.get("brands", [])
        assert len(brands) > 0, "Brands list should not be empty"
        logger.info(f"Total brands: {len(brands)}")

    @allure.story("GET Brands")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_brand_has_expected_fields(self, api_client):
        """Test that each brand has the expected fields."""
        response = api_client.get("/brandsList")
        data = response.json()
        brands = data.get("brands", [])

        assert len(brands) > 0, "Need at least one brand to validate"

        brand = brands[0]
        assert "id" in brand, "Brand should have 'id' field"
        assert "brand" in brand, "Brand should have 'brand' field"

        logger.info(f"Sample brand: {brand}")

    @allure.story("PUT Brands (Negative)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.negative
    def test_put_to_brands_returns_405(self, api_client):
        """Test that PUT to /brandsList returns 405 (method not supported)."""
        response = api_client.put("/brandsList")

        data = response.json()
        assert data.get("responseCode") == 405 or response.status_code == 405, (
            "PUT to brands list should return 405"
        )
