"""PicoRun runtime classes."""

from typing import Any, ClassVar

from requests import Response

import picorun.errors


class ApiRequestArgs:
    """Arguments for making an API call with requests."""

    def __init__(
        self,
        path: dict[str, Any] | None = None,
        query: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> None:
        """Construct an object with the arguments for the API call."""
        self.path = path if isinstance(path, dict) else {}
        self.query = query if isinstance(query, dict) else {}
        self.json = payload if isinstance(payload, dict) else {}
        self.headers = headers if isinstance(headers, dict) else {}

    def to_kwargs(self) -> dict[str, Any]:
        """Convert the object to a dictionary of keyword arguments for requests."""
        output = {}
        for property in ["headers", "json", "query"]:
            output[property] = getattr(self, property)
        return output


class ApiResponse:
    """API response."""

    _error_mapping: ClassVar[dict[int : picorun.errors.ApiError]] = {
        400: picorun.errors.Http400Error,
        401: picorun.errors.Http401Error,
        403: picorun.errors.Http403Error,
        404: picorun.errors.Http404Error,
        405: picorun.errors.Http405Error,
        418: picorun.errors.Http418Error,
        429: picorun.errors.Http429Error,
        500: picorun.errors.Http500Error,
        501: picorun.errors.Http501Error,
        502: picorun.errors.Http502Error,
    }

    def __init__(self, response: Response) -> None:
        """Construct an ApiResponse."""
        self.response = response
        self.status_code = response.status_code
        self.headers = response.headers
        self.body = response.text
        if (
            "Content-Type" in response.headers
            and "application/json" in response.headers["Content-Type"]
        ):
            self.body = response.json()

    def asdict(self) -> dict[str, Any]:
        """Convert the object to a dictionary."""
        return {
            "statusCode": self.status_code,
            "headers": dict(self.headers),
            "body": self.body,
        }

    def raise_for_status(self) -> None:
        """
        Raise an exception if an error response is received.

        This method is inspired by the Requests' method of the same name. The difference
        is PicoRun raises classed errors for many common HTTP error codes. This makes it
        easier to handle the errors in Step Functions.
        """
        if self.status_code in self._error_mapping:
            exp = self._error_mapping[self.status_code]
            raise exp(self.body)

        if self.status_code >= 400:
            raise picorun.errors.ApiError(self.body, self.status_code)
