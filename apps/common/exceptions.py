"""
Global exception handler.

Wired up in `config/settings/base.py` via
`REST_FRAMEWORK["EXCEPTION_HANDLER"]`. DRF's default handler already
turns exceptions into an HTTP response with the right status code; this
wrapper just reshapes the *body* of that response into the standard
`{ success, message, errors }` envelope described in Part 06, so the
frontend never has to special-case error formats per endpoint.
"""

from rest_framework.views import exception_handler as drf_exception_handler


def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is None:
        # Unhandled exception (e.g. a bug) — let Django's default 500
        # behavior take over rather than masking it.
        return response

    data = response.data

    # DRF's ValidationError / NotAuthenticated / PermissionDenied etc.
    # commonly return {"detail": "..."} for single, non-field errors.
    if isinstance(data, dict) and set(data.keys()) == {"detail"}:
        response.data = {
            "success": False,
            "message": str(data["detail"]),
        }
        return response

    # Field-level validation errors: {"title": ["This field is required."]}
    errors = data if isinstance(data, dict) else {"non_field_errors": data}
    response.data = {
        "success": False,
        "message": "Validation failed." if response.status_code == 400 else "Request failed.",
        "errors": errors,
    }
    return response
