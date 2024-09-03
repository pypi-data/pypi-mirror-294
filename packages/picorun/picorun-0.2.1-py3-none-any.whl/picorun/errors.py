"""PicoRun Errors."""


class ApiError(Exception):
    """Exception raised when an API call fails."""

    def __init__(self, message: str, status_code: int) -> None:
        """Construct an ApiError."""
        super().__init__(f"Error {status_code}: {message}")
        self.status_code = status_code


class Http400Error(ApiError):
    """HTTP 400 Bad Request Error."""

    def __init__(self, message: str) -> None:
        """Construct a HTTP 400 Error."""
        super().__init__(message, 400)


class Http401Error(ApiError):
    """HTTP 401 Unauthorised Error."""

    def __init__(self, message: str) -> None:
        """Construct a HTTP 401 Error."""
        super().__init__(message, 401)


class Http403Error(ApiError):
    """HTTP 403 Forbidden Error."""

    def __init__(self, message: str) -> None:
        """Construct a HTTP 403 Error."""
        super().__init__(message, 403)


class Http404Error(ApiError):
    """HTTP 404 Not Found Error."""

    def __init__(self, message: str) -> None:
        """Construct a HTTP 404 Error."""
        super().__init__(message, 404)


class Http405Error(ApiError):
    """HTTP 405 Method Not Allowed Error."""

    def __init__(self, message: str) -> None:
        """Construct a HTTP 405 Error."""
        super().__init__(message, 405)


class Http418Error(ApiError):
    """HTTP 418 Teapot Error."""

    def __init__(self, message: str) -> None:
        """Construct a HTTP 418 Error."""
        super().__init__(message, 418)


class Http429Error(ApiError):
    """HTTP 429 Too Many Requests Error."""

    def __init__(self, message: str) -> None:
        """Construct a HTTP 429 Error."""
        super().__init__(message, 429)


class Http500Error(ApiError):
    """HTTP 500 Internal Server Error Error."""

    def __init__(self, message: str) -> None:
        """Construct a HTTP 500 Error."""
        super().__init__(message, 500)


class Http501Error(ApiError):
    """HTTP 501 Not Implemented Error."""

    def __init__(self, message: str) -> None:
        """Construct a HTTP 501 Error."""
        super().__init__(message, 501)


class Http502Error(ApiError):
    """HTTP 502 Bad Gateway Error."""

    def __init__(self, message: str) -> None:
        """Construct a HTTP 502 Error."""
        super().__init__(message, 502)
