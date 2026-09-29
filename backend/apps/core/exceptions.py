"""Consistent API error shape: {"detail": str, "errors": {field: [messages]}}."""

from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None
    data = response.data
    if isinstance(data, dict) and set(data) == {"detail"}:
        response.data = {"detail": str(data["detail"]), "errors": {}}
    elif isinstance(data, dict):
        detail = data.get("detail") or data.get("non_field_errors", ["Please correct the errors below."])
        if isinstance(detail, list):
            detail = detail[0]
        errors = {k: v for k, v in data.items() if k not in {"detail"}}
        response.data = {"detail": str(detail), "errors": errors}
    else:
        response.data = {"detail": str(data[0]) if data else "Request failed.", "errors": {}}
    return response
