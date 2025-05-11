from unittest.mock import MagicMock

from dimo.dimo import DIMO


def test_get_full_path_no_params():
    client = DIMO(env="Dev")
    result = client._get_full_path("Valuations", "/v2/vehicles/1234/valuations")
    assert result == "https://valuations-api.dev.dimo.zone/v2/vehicles/1234/valuations"


def test_get_full_path_with_params():
    client = DIMO(env="Dev")
    result = client._get_full_path(
        "Telemetry",
        "/items/{item_id}",
        {"item_id": 123},
    )
    assert result == "https://telemetry-api.dev.dimo.zone/items/123"


def test_get_auth_headers():
    client = DIMO(env="Dev")
    headers = client._get_auth_headers("token123")
    assert headers == {
        "Authorization": "Bearer token123",
        "Content-Type": "application/json",
    }


def test_query_calls_request_with_correct_payload(monkeypatch):
    client = DIMO(env="Dev")
    # Create a fake request method on the client
    fake_request = MagicMock(return_value={"data": {"result": True}})
    monkeypatch.setattr(client, "request", fake_request)

    query_str = "query { test }"
    variables = {"key": "value"}
    result = client.query("Trips", query_str, variables=variables, token="mocked_token")

    # Verify the fake request was invoked once
    fake_request.assert_called_once()
    # Inspect call arguments
    args, kwargs = fake_request.call_args
    assert args[0] == "POST"
    assert args[1] == "Trips"
    assert args[2] == ""

    # Assert correct headers
    headers = kwargs["headers"]
    assert headers["Authorization"] == "Bearer mocked_token"
    assert headers["Content-Type"] == "application/json"
    assert headers["User-Agent"] == "dimo-python-sdk"

    # Check payload data
    data = kwargs["data"]
    assert data["query"] == query_str
    assert data["variables"] == variables

    assert result == {"data": {"result": True}}
