"""Test picorun classes."""

import pytest

import picorun
import picorun.errors


def mock_response(
    status_code: int = 200,
    headers: dict[str, str] | None = None,
    text: str | None = None,
    json: dict[str, str] | None = None,
) -> "MockResponse":  # noqa: F821 class defined in this function
    """Mock requests.Response."""

    class MockResponse:
        def __init__(self) -> None:
            self.status_code = status_code
            self.headers = headers or {}
            self.text = text
            self.json = lambda: json

    return MockResponse()


def test_api_request_args() -> None:
    """Test ApiRequestArgs."""
    args = picorun.picorun.ApiRequestArgs(
        path={"path": "value"},
        query={"query": "value"},
        payload={"payload": "value"},
        headers={"headers": "value"},
    )
    assert args.path == {"path": "value"}
    assert args.query == {"query": "value"}
    assert args.json == {"payload": "value"}
    assert args.headers == {"headers": "value"}
    assert args.to_kwargs() == {
        "headers": {"headers": "value"},
        "json": {"payload": "value"},
        "query": {"query": "value"},
    }


def test_api_request_empty_args() -> None:
    """Test ApiRequestArgs with empty arguments."""
    args = picorun.picorun.ApiRequestArgs()
    assert args.path == {}
    assert args.query == {}
    assert args.json == {}
    assert args.headers == {}
    assert args.to_kwargs() == {
        "headers": {},
        "json": {},
        "query": {},
    }


def test_api_response() -> None:
    """Test ApiResponse."""
    response = mock_response(
        status_code=200,
        headers={"Content-Type": "text/plain"},
        text="body",
    )
    api_response = picorun.picorun.ApiResponse(response)
    assert api_response.response == response
    assert api_response.status_code == 200
    assert api_response.headers == {"Content-Type": "text/plain"}
    assert api_response.body == "body"
    assert api_response.asdict() == {
        "statusCode": 200,
        "headers": {"Content-Type": "text/plain"},
        "body": "body",
    }


def test_api_response_no_content_type() -> None:
    """Test ApiResponse with no content type header."""
    response = mock_response(status_code=200, text="")
    api_response = picorun.picorun.ApiResponse(response)
    assert api_response.body == ""


def test_api_response_json() -> None:
    """Test ApiResponse with JSON body."""
    response = mock_response(
        status_code=200,
        headers={"Content-Type": "application/json"},
        json={"key": "value"},
    )
    api_response = picorun.picorun.ApiResponse(response)
    assert api_response.body == {"key": "value"}
    assert api_response.asdict() == {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": {"key": "value"},
    }


@pytest.mark.parametrize(
    ("code", "exp"),
    [
        (400, picorun.errors.Http400Error),
        (401, picorun.errors.Http401Error),
        (403, picorun.errors.Http403Error),
        (404, picorun.errors.Http404Error),
        (405, picorun.errors.Http405Error),
        (418, picorun.errors.Http418Error),
        (429, picorun.errors.Http429Error),
        (500, picorun.errors.Http500Error),
        (501, picorun.errors.Http501Error),
        (502, picorun.errors.Http502Error),
        (451, picorun.errors.ApiError),
    ],
)
def test_api_response_error_errors(code: int, exp: picorun.errors.ApiError) -> None:
    """Test ApiResponse with 400 Bad Request Error."""
    response = mock_response(
        status_code=code,
        text="",
    )
    api_response = picorun.picorun.ApiResponse(response)
    with pytest.raises(exp):
        api_response.raise_for_status()
