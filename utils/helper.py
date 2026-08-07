"""
utils/helper.py
Small, shared helper functions used across the backend -- request
validation and consistent error-response formatting.
"""

from flask import jsonify


def validate_payload(data, required_fields):
    """
    Ensure the request JSON body exists and contains every required field.
    Returns (True, None) on success, or (False, error_message) on failure.
    """
    if data is None:
        return False, "Request body must be valid JSON."

    missing = [field for field in required_fields if field not in data]
    if missing:
        return False, f"Missing required field(s): {', '.join(missing)}"

    return True, None


def error_response(message: str, status_code: int = 400):
    """Build a consistent JSON error response."""
    return jsonify({"status": "error", "message": message}), status_code
