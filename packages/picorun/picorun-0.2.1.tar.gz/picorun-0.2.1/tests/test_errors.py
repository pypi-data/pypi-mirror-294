"""Test picorun classes."""

import picorun.errors


def test_api_error() -> None:
    """Test ApiError."""
    error = picorun.errors.ApiError("message", 404)
    assert str(error) == "Error 404: message"
    assert error.status_code == 404
