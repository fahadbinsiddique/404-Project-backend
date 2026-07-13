"""
Standardized response envelope helpers.

Every endpoint in this project returns responses shaped like:

    { "success": true,  "message": "...", "data": ... }
    { "success": false, "message": "...", "errors": {...} }

per Part 06 (API Design & Endpoint Specification). Views should use
these helpers instead of constructing `Response(...)` ad hoc, so the
envelope stays consistent everywhere.
"""

from rest_framework.response import Response


def success_response(data=None, message="Success.", status_code=200):
    return Response(
        {"success": True, "message": message, "data": data},
        status=status_code,
    )


def error_response(message="Something went wrong.", errors=None, status_code=400):
    payload = {"success": False, "message": message}
    if errors is not None:
        payload["errors"] = errors
    return Response(payload, status=status_code)
