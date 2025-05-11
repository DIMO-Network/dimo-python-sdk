import json
import pytest
from requests import RequestException
from unittest.mock import Mock

from dimo.request import Request, HTTPError


class DummyResponse:
    def __init__(
        self, status_code=200, headers=None, json_data=None, content=b"", txt=""
    ):
        self.status_code = status_code
        self.headers = headers or {}
        self._json_data = json_data
        self.content = content
        self.txt = txt
        # .raise_for_status will be set per-test via side_effect

    def json(self):
        if isinstance(self._json_data, Exception):
            raise self._json_data
        return self._json_data


@pytest.fixture
def session():
    return Mock()


def make_request(session, **kwargs):
    req = Request("POST", "https://api.example.com/endpoint", session)
    return req(**kwargs)


def test_json_request_body_is_serialized_and_passed_through(session):
    data = {"foo": "bar"}
    headers = {"Content-Type": "application/json"}
    resp = DummyResponse(
        status_code=200,
        headers={"Content-Type": "application/json"},
        json_data={"ok": True},
    )
    resp.raise_for_status = Mock()
    session.request.return_value = resp

    result = make_request(session, headers=headers, data=data)

    # ensure data was JSON-dumped
    _, call_kwargs = session.request.call_args
    assert call_kwargs["data"] == json.dumps(data)

    # ensure we got the parsed JSON back
    assert result == {"ok": True}


def test_non_json_response_returns_raw_content(session):
    resp = DummyResponse(
        status_code=200,
        headers={"Content-Type": "text/plain"},
        content=b"hello world",
    )
    resp.raise_for_status = Mock()
    session.request.return_value = resp

    result = make_request(session)
    assert result == b"hello world"


def test_http_error_wraps_json_body(session):
    # prepare a RequestException with a response whose .json() returns a dict
    err_resp = DummyResponse(
        status_code=400,
        json_data={"error": "Bad things"},
        txt="Bad things text",
    )
    exc = RequestException("Bad Request")
    exc.response = err_resp

    # have raise_for_status raise that exception
    good_resp = DummyResponse()
    good_resp.raise_for_status = Mock(side_effect=exc)
    session.request.return_value = good_resp

    with pytest.raises(HTTPError) as ei:
        make_request(session)
    err = ei.value
    assert err.status == 400
    assert err.body == {"error": "Bad things"}
    assert "Bad Request" in str(err)
