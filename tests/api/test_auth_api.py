"""
test_auth_api.py — API tests for the Login Verification endpoint.

Tests POST /verifyLogin with valid/invalid credentials,
missing parameters, and unsupported HTTP methods.
"""

import pytest
import allure
from utils.fake_data import generate_user_data
from utils.logger import get_logger

logger = get_logger("test_auth_api")


@allure.epic("API Testing")
@allure.feature("Authentication API")
class TestAuthAPI:
    """Test suite for the Verify Login API endpoint."""

    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    def test_verify_login_with_valid_credentials(self, api_client, api_test_user):
        """Test that POST /verifyLogin with valid credentials returns 200."""
        response = api_client.post(
            "/verifyLogin",
            data={
                "email": api_test_user["email"],
                "password": api_test_user["password"],
            }
        )

        data = response.json()
        assert data.get("responseCode") == 200, (
            f"Valid login should return responseCode 200, got: {data}"
        )
        assert "user exists" in data.get("message", "").lower(), (
            f"Should confirm user exists, got: {data.get('message')}"
        )

    @allure.story("Missing Email")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.negative
    def test_verify_login_without_email(self, api_client):
        """Test that POST /verifyLogin without email returns 400."""
        response = api_client.post(
            "/verifyLogin",
            data={"password": "somepassword"}
        )

        data = response.json()
        assert data.get("responseCode") == 400, (
            f"Missing email should return responseCode 400, got: {data}"
        )

    @allure.story("Missing Password")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.negative
    def test_verify_login_without_password(self, api_client):
        """Test that POST /verifyLogin without password returns 400."""
        response = api_client.post(
            "/verifyLogin",
            data={"email": "test@test.com"}
        )

        data = response.json()
        assert data.get("responseCode") == 400, (
            f"Missing password should return responseCode 400, got: {data}"
        )

    @allure.story("Invalid Credentials")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.negative
    def test_verify_login_with_invalid_credentials(self, api_client):
        """Test that POST /verifyLogin with invalid details returns 404."""
        response = api_client.post(
            "/verifyLogin",
            data={
                "email": "nonexistent_user_xyz@fake.com",
                "password": "wrongpassword123",
            }
        )

        data = response.json()
        assert data.get("responseCode") == 404, (
            f"Invalid credentials should return responseCode 404, got: {data}"
        )
        assert "not found" in data.get("message", "").lower(), (
            f"Should say 'User not found', got: {data.get('message')}"
        )

    @allure.story("Unsupported Method")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.negative
    def test_delete_to_verify_login_returns_405(self, api_client):
        """Test that DELETE to /verifyLogin returns 405 (method not supported)."""
        response = api_client.delete("/verifyLogin")

        data = response.json()
        assert data.get("responseCode") == 405 or response.status_code == 405, (
            f"DELETE should return 405, got: {data}"
        )

    @allure.story("Empty Credentials")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.api
    @pytest.mark.negative
    def test_verify_login_with_empty_credentials(self, api_client):
        """Test that POST /verifyLogin with empty email and password is handled."""
        response = api_client.post(
            "/verifyLogin",
            data={"email": "", "password": ""}
        )

        data = response.json()
        # Should not return 200 for empty credentials
        assert data.get("responseCode") != 200, (
            f"Empty credentials should not succeed, got: {data}"
        )
