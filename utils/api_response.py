"""Utilities for consistent JSON responses from the REST API."""

from datetime import datetime, timezone
from typing import Optional, Tuple

from flask import Response, jsonify


def api_response(
    success: bool,
    data: Optional[object] = None,
    message: str = "",
    status_code: int = 200,
) -> Tuple[Response, int]:
    """Build a timestamped response using the API's standard envelope.

    Args:
        success: Whether the request completed successfully.
        data: Response payload, or ``None`` when there is no payload.
        message: Human-readable result or error message.
        status_code: HTTP status to return.

    Returns:
        A Flask JSON response and its HTTP status code.
    """
    response = jsonify(
        {
            "success": success,
            "data": data,
            "message": message,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )
    return response, status_code
