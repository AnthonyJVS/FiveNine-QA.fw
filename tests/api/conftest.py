"""
tests/api/conftest.py — API-specific fixtures.

Provides a configured APIClient instance and test user management.
"""

import pytest
from utils.api_client import APIClient
from utils.fake_data import generate_user_data
from utils.logger import get_logger

logger = get_logger("api_conftest")


@pytest.fixture(scope="session")
def api_client():
    """
    Session-scoped API client.

    Shared across all API tests for efficiency.
    Closed at session end.
    """
    client = APIClient()
    yield client
    client.close()


@pytest.fixture
def api_test_user(api_client):
    """
    Create a test user via API and clean up after test.

    Yields:
        dict with the user's registration data (including email/password).
    """
    user_data = generate_user_data()

    # Create the user
    response = api_client.post("/createAccount", data=user_data)
    logger.info(f"Created API test user: {user_data['email']}")

    yield user_data

    # Teardown — delete the user
    try:
        api_client.delete("/deleteAccount", data={
            "email": user_data["email"],
            "password": user_data["password"],
        })
        logger.info(f"Deleted API test user: {user_data['email']}")
    except Exception as e:
        logger.warning(f"Failed to clean up API test user: {e}")
