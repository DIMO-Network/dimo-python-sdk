from dimo.errors import check_type


class VehicleEvents:

    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers

    def list_webhooks(self, developer_jwt: str):
        check_type("developer_jwt", developer_jwt, str)
        url = f"/webhooks"
        return self._request(
            "GET", "VehicleEvents", url, headers=self._get_auth_headers(developer_jwt)
        )

    def register_webhook(self, developer_jwt: str, request: object):
        check_type("developer_jwt", developer_jwt, str)
        check_type("request", request, object)
        url = f"/webhooks"
        return self._request(
            "POST",
            "VehicleEvents",
            url,
            headers=self._get_auth_headers(developer_jwt),
            data=request,
        )

    def webhook_signals(self, developer_jwt: str):
        check_type("developer_jwt", developer_jwt, str)
        url = f"/webhooks/signals"
        return self._request(
            "GET", "VehicleEvents", url, headers=self._get_auth_headers(developer_jwt)
        )

    def update_webhook(self, developer_jwt: str, id: str, request: object):
        check_type("developer_jwt", developer_jwt, str)
        check_type("id", id, str)
        check_type("request", request, object)
        url = f"/webhooks/{id}"
        return self._request(
            "PUT",
            "VehicleEvents",
            url,
            headers=self._get_auth_headers(developer_jwt),
            json=request,
        )

    def delete_webhook(self, developer_jwt: str, id: str):
        check_type("developer_jwt", developer_jwt, str)
        check_type("id", id, str)
        url = f"/webhooks/{id}"
        return self._request(
            "DELETE",
            "VehicleEvents",
            url,
            headers=self._get_auth_headers(developer_jwt),
        )

    def vehicle_subscriptions(self, developer_jwt: str, token_id: str):
        check_type("developer_jwt", developer_jwt, str)
        check_type("token_id", token_id, str)
        url = f"/subscriptions/{token_id}"
        return self._request(
            "GET", "VehicleEvents", url, headers=self._get_auth_headers(developer_jwt)
        )

    def subscribe_vehicle(self, developer_jwt: str, token_id: str, event_id: str, request={}):
        check_type("developer_jwt", developer_jwt, str)
        check_type("token_id", token_id, str)
        check_type("event_id", event_id, str)
        check_type("request", request, object)
        url = f"/subscriptions/{token_id}/event/{event_id}"
        return self._request(
            "POST", "VehicleEvents", url, headers=self._get_auth_headers(developer_jwt), json=request
        )

    def unsubscribe_vehicle(self, developer_jwt: str, token_id: str, event_id: str):
        check_type("developer_jwt", developer_jwt, str)
        check_type("token_id", token_id, str)
        check_type("event_id", event_id, str)
        url = f"/subscriptions/{token_id}/event/{event_id}"
        return self._request(
            "DELETE",
            "VehicleEvents",
            url,
            headers=self._get_auth_headers(developer_jwt),
        )
