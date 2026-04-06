"""
test_user_api.py — API tests for User Account CRUD operations.

Tests create, read, update, and delete user account endpoints.
"""

import pytest
import allure
from utils.fake_data import generate_user_data
from utils.logger import get_logger

logger = get_logger("test_user_api")


@allure.epic("API Testing")
@allure.feature("User CRUD API")
class TestUserAPI:
    """Test suite for User Account CRUD API endpoints."""

    @allure.story("Create User")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    def test_create_user_account(self, api_client):
        """Test that POST /createAccount creates a new user (201)."""
        user_data = generate_user_data()

        response = api_client.post("/createAccount", data=user_data)

        data = response.json()
        assert data.get("responseCode") == 201, (
            f"Create user should return 201, got: {data}"
        )
        assert "created" in data.get("message", "").lower(), (
            f"Should confirm user created, got: {data.get('message')}"
        )

        # Cleanup
        api_client.delete("/deleteAccount", data={
            "email": user_data["email"],
            "password": user_data["password"],
        })
        logger.info(f"Created and cleaned up user: {user_data['email']}")

    @allure.story("Get User Details")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    def test_get_user_detail_by_email(self, api_client, api_test_user):
        """Test that GET /getUserDetailByEmail returns user details."""
        response = api_client.get(
            "/getUserDetailByEmail",
            params={"email": api_test_user["email"]}
        )

        data = response.json()
        assert data.get("responseCode") == 200, (
            f"Get user detail should return 200, got: {data}"
        )

        user = data.get("user", {})
        assert user.get("email") == api_test_user["email"], (
            f"Returned email should match. Expected: {api_test_user['email']}, "
            f"Got: {user.get('email')}"
        )
        logger.info(f"Retrieved user details: {user.get('name')}")

    @allure.story("Update User")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    def test_update_user_account(self, api_client, api_test_user):
        """Test that PUT /updateAccount updates user details."""
        updated_data = api_test_user.copy()
        updated_data["firstname"] = "UpdatedFirstName"
        updated_data["lastname"] = "UpdatedLastName"
        updated_data["company"] = "Updated QA Corp"

        response = api_client.put("/updateAccount", data=updated_data)

        data = response.json()
        assert data.get("responseCode") == 200, (
            f"Update user should return 200, got: {data}"
        )
        assert "updated" in data.get("message", "").lower(), (
            f"Should confirm user updated, got: {data.get('message')}"
        )

    @allure.story("Delete User")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    def test_delete_user_account(self, api_client):
        """Test that DELETE /deleteAccount deletes a user (200)."""
        from utils.helpers import unique_email

        # Create a user with guaranteed unique email
        user_data = generate_user_data()
        user_data["email"] = unique_email("delete_test")
        create_response = api_client.post("/createAccount", data=user_data)
        create_data = create_response.json()
        assert create_data.get("responseCode") == 201, (
            f"User must be created first, got: {create_data}"
        )

        # Delete the user
        response = api_client.delete(
            "/deleteAccount",
            data={
                "email": user_data["email"],
                "password": user_data["password"],
            }
        )

        data = response.json()
        assert data.get("responseCode") == 200, (
            f"Delete account should return 200, got: {data}"
        )
        assert "deleted" in data.get("message", "").lower(), (
            f"Should confirm account deleted, got: {data.get('message')}"
        )

    @allure.story("Get Non-Existent User")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.negative
    def test_get_user_detail_nonexistent_email(self, api_client):
        """Test fetching details for a non-existent user."""
        response = api_client.get(
            "/getUserDetailByEmail",
            params={"email": "nonexistent_xyz_999@fake.com"}
        )

        data = response.json()
        assert data.get("responseCode") == 404 or data.get("responseCode") == 400, (
            f"Non-existent user should return 404 or 400, got: {data}"
        )

    @allure.story("Create Duplicate User")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.negative
    def test_create_duplicate_user(self, api_client, api_test_user):
        """Test that creating a user with an existing email fails."""
        response = api_client.post("/createAccount", data=api_test_user)

        data = response.json()
        # Should return an error since user already exists
        assert data.get("responseCode") != 201, (
            f"Duplicate user creation should not return 201, got: {data}"
        )
