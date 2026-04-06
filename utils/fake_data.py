"""
fake_data.py — Test data generators using Faker.

Provides factory functions for generating realistic test data
for user registration, contact forms, and other test scenarios.

Usage:
    from utils.fake_data import generate_user_data, generate_contact_data
    user = generate_user_data()
"""

from faker import Faker

fake = Faker()


def generate_user_data() -> dict:
    """
    Generate a complete user registration dataset.

    Returns:
        Dictionary with all fields required for automationexercise.com signup.
    """
    first_name = fake.first_name()
    last_name = fake.last_name()

    return {
        "name": f"{first_name} {last_name}",
        "email": fake.unique.email(),
        "password": fake.password(length=12, special_chars=True),
        "title": fake.random_element(["Mr", "Mrs"]),
        "birth_date": str(fake.random_int(min=1, max=28)),
        "birth_month": str(fake.random_int(min=1, max=12)),
        "birth_year": str(fake.random_int(min=1970, max=2005)),
        "firstname": first_name,
        "lastname": last_name,
        "company": fake.company(),
        "address1": fake.street_address(),
        "address2": fake.secondary_address(),
        "country": fake.random_element([
            "India", "United States", "Canada", "Australia",
            "Israel", "New Zealand", "Singapore"
        ]),
        "zipcode": fake.zipcode(),
        "state": fake.state(),
        "city": fake.city(),
        "mobile_number": fake.phone_number(),
    }


def generate_contact_data() -> dict:
    """
    Generate data for the Contact Us form.

    Returns:
        Dictionary with name, email, subject, and message fields.
    """
    return {
        "name": fake.name(),
        "email": fake.email(),
        "subject": fake.sentence(nb_words=5),
        "message": fake.paragraph(nb_sentences=3),
    }


def generate_login_credentials(valid: bool = True) -> dict:
    """
    Generate login credentials.

    Args:
        valid: If False, generates clearly invalid credentials.

    Returns:
        Dictionary with email and password.
    """
    if valid:
        return {
            "email": fake.email(),
            "password": fake.password(length=10),
        }
    return {
        "email": f"invalid_{fake.random_int()}@nonexistent.com",
        "password": "wrong_password_123",
    }


def generate_search_queries() -> list[str]:
    """Return a list of product search terms for testing."""
    return [
        "top",
        "tshirt",
        "dress",
        "jean",
        "saree",
    ]
