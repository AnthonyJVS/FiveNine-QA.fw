"""
api_client.py — Reusable HTTP client wrapper for API testing.

Wraps requests.Session with logging, base URL management,
and response assertion helpers.

Usage:
    from utils.api_client import APIClient

    client = APIClient()
    response = client.get("/productsList")
    client.assert_status(response, 200)
"""

import json
import requests
import allure
from typing import Any, Optional

from config.settings import settings
from utils.logger import get_logger

logger = get_logger("api_client")

_SENSITIVE_KEYS = {"password", "token", "authorization"}


def _redact(value: Any) -> Any:
    """Return a copy of dict/list values with sensitive keys masked, for safe logging."""
    if isinstance(value, dict):
        return {
            k: ("***REDACTED***" if k.lower() in _SENSITIVE_KEYS else _redact(v))
            for k, v in value.items()
        }
    if isinstance(value, list):
        return [_redact(item) for item in value]
    return value


class APIClient:
    """HTTP client with logging, session management, and assertion helpers."""

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or settings.api_base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
        })
        self.timeout = settings.api_timeout
        logger.info(f"APIClient initialized — base_url={self.base_url}")

    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint path."""
        if endpoint.startswith("http"):
            return endpoint
        return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    def _log_request(self, method: str, url: str, **kwargs):
        """Log outgoing request details (sensitive fields redacted)."""
        logger.debug(
            f"REQUEST: {method.upper()} {url} | "
            f"params={_redact(kwargs.get('params'))} | "
            f"data={_redact(kwargs.get('data'))} | "
            f"json={_redact(kwargs.get('json'))}"
        )

    def _log_response(self, response: requests.Response):
        """Log incoming response details (sensitive fields redacted)."""
        try:
            body = _redact(response.json())
            body_str = json.dumps(body, indent=2)[:500]
        except (json.JSONDecodeError, ValueError):
            body_str = response.text[:500]

        logger.debug(
            f"RESPONSE: {response.status_code} | "
            f"elapsed={response.elapsed.total_seconds():.3f}s | "
            f"body={body_str}"
        )

    @allure.step("GET {endpoint}")
    def get(self, endpoint: str, params: Optional[dict] = None, **kwargs) -> requests.Response:
        """Send GET request."""
        url = self._build_url(endpoint)
        self._log_request("GET", url, params=params)

        response = self.session.get(url, params=params, timeout=self.timeout, **kwargs)
        self._log_response(response)
        return response

    @allure.step("POST {endpoint}")
    def post(
        self,
        endpoint: str,
        data: Optional[dict] = None,
        json_data: Optional[dict] = None,
        **kwargs,
    ) -> requests.Response:
        """Send POST request."""
        url = self._build_url(endpoint)
        self._log_request("POST", url, data=data, json=json_data)

        response = self.session.post(
            url, data=data, json=json_data, timeout=self.timeout, **kwargs
        )
        self._log_response(response)
        return response

    @allure.step("PUT {endpoint}")
    def put(
        self,
        endpoint: str,
        data: Optional[dict] = None,
        json_data: Optional[dict] = None,
        **kwargs,
    ) -> requests.Response:
        """Send PUT request."""
        url = self._build_url(endpoint)
        self._log_request("PUT", url, data=data, json=json_data)

        response = self.session.put(
            url, data=data, json=json_data, timeout=self.timeout, **kwargs
        )
        self._log_response(response)
        return response

    @allure.step("DELETE {endpoint}")
    def delete(self, endpoint: str, data: Optional[dict] = None, **kwargs) -> requests.Response:
        """Send DELETE request."""
        url = self._build_url(endpoint)
        self._log_request("DELETE", url, data=data)

        response = self.session.delete(url, data=data, timeout=self.timeout, **kwargs)
        self._log_response(response)
        return response

    # ──────────────────────────────────────────
    # Assertion helpers
    # ──────────────────────────────────────────

    @staticmethod
    def assert_status(response: requests.Response, expected: int):
        """Assert HTTP status code matches expected."""
        assert response.status_code == expected, (
            f"Expected status {expected}, got {response.status_code}. "
            f"Response: {response.text[:300]}"
        )

    @staticmethod
    def assert_json_key(response: requests.Response, key: str) -> Any:
        """Assert JSON response contains a key and return its value."""
        data = response.json()
        assert key in data, f"Key '{key}' not found in response: {list(data.keys())}"
        return data[key]

    @staticmethod
    def assert_response_time(response: requests.Response, max_seconds: float = 5.0):
        """Assert response time is within acceptable threshold."""
        elapsed = response.elapsed.total_seconds()
        assert elapsed < max_seconds, (
            f"Response took {elapsed:.3f}s, exceeding threshold of {max_seconds}s"
        )

    def close(self):
        """Close the HTTP session."""
        self.session.close()
        logger.info("APIClient session closed")
