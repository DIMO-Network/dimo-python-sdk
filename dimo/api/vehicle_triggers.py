from dimo.errors import check_type


class VehicleTriggers:

    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers

    def list_all_webhooks(self, developer_jwt: str):
        """
        Lists all webhooks for a given developer license
        """
        check_type("developer_jwt", developer_jwt, str)
        url = f"/v1/webhooks"
        return self._request(
            "GET", "VehicleTriggers", url, headers=self._get_auth_headers(developer_jwt)
        )

    def register_webhook(self, developer_jwt: str, request: object):
        """
        Creates a new webhook under the developer license
        """
        check_type("developer_jwt", developer_jwt, str)
        check_type("request", request, object)
        url = f"/v1/webhooks"
        return self._request(
            "POST",
            "VehicleTriggers",
            url,
            headers=self._get_auth_headers(developer_jwt),
            data=request,
        )

    def webhook_signals(self, developer_jwt: str):
        """
        Fetches the list of signal names available for the data field
        """
        check_type("developer_jwt", developer_jwt, str)
        url = f"/v1/webhooks/signals"
        return self._request(
            "GET", "VehicleTriggers", url, headers=self._get_auth_headers(developer_jwt)
        )

    def list_vehicle_subscriptions(self, developer_jwt: str, token_did: str):
        """
        Lists all webhooks that a specified vehicle token id is subscribed to
        """
        check_type("developer_jwt", developer_jwt, str)
        check_type("token_id", token_did, str)
        url = f"/v1/webhooks/vehicles/{token_did}"
        return self._request(
            "GET", "VehicleTriggers", url, headers=self._get_auth_headers(developer_jwt)
        )

    def list_vehicle_subscriptions_by_trigger(self, developer_jwt: str, webhook_id: str):
        """
        Lists all vehicle subscriptions for a given webhook id
        """
        check_type("developer_jwt", developer_jwt, str)
        check_type("webhook_id", webhook_id, str)
        url = f"/v1/webhooks/{webhook_id}"
        return self._request(
            "GET", "VehicleTriggers", url, headers=self._get_auth_headers(developer_jwt)
        )

    def update_webhook(self, developer_jwt: str, webhook_id: str, request: object):
        """
        Updates a webhook by a provided webhook id
        """
        check_type("developer_jwt", developer_jwt, str)
        check_type("webhook_id", webhook_id, str)
        check_type("request", request, object)
        url = f"/v1/webhooks/{webhook_id}"
        return self._request(
            "PUT",
            "VehicleTriggers",
            url,
            headers=self._get_auth_headers(developer_jwt),
            data=request,
        )

    def delete_webhook(self, developer_jwt: str, webhook_id: str):
        """
        Deletes a webhook by a provided webhook id
        """
        check_type("developer_jwt", developer_jwt, str)
        check_type("webhook_id", webhook_id, str)
        url = f"/v1/webhooks/{webhook_id}"
        return self._request(
            "DELETE",
            "VehicleTriggers",
            url,
            headers=self._get_auth_headers(developer_jwt),
        )

    def subscribe_all_vehicles(self, developer_jwt: str, webhook_id: str):
        """
        Subscribes all vehicles to a specified webhook
        """
        check_type("developer_jwt", developer_jwt, str)
        check_type("webhook_id", webhook_id, str)
        url = f"/v1/webhooks/{webhook_id}/subscribe/all"
        return self._request(
            "POST", "VehicleTriggers", url, headers=self._get_auth_headers(developer_jwt)
        )

    def subscribe_vehicle(self, developer_jwt: str, token_did: str, webhook_id: str):
        """
        Subscribes a single vehicle to a specified webhook
        """
        check_type("developer_jwt", developer_jwt, str)
        check_type("token_id", token_did, str)
        check_type("webhook_id", webhook_id, str)
        url = f"/v1/webhooks/{webhook_id}/subscribe/{token_did}"
        return self._request(
            "POST", "VehicleTriggers", url, headers=self._get_auth_headers(developer_jwt)
        )

    def unsubscribe_all_vehicles(self, developer_jwt: str, webhook_id: str):
        """
        Unsubscribes all vehicles from a specified webhook
        """
        check_type("developer_jwt", developer_jwt, str)
        check_type("webhook_id", webhook_id, str)
        url = f"/v1/webhooks/{webhook_id}/unsubscribe/all"
        return self._request(
            "DELETE",
            "VehicleTriggers",
            url,
            headers=self._get_auth_headers(developer_jwt),
        )

    def unsubscribe_vehicle(self, developer_jwt: str, token_did: str, webhook_id: str):
        """
        Unsubscribes a single vehicle from a specified webhook
        """
        check_type("developer_jwt", developer_jwt, str)
        check_type("token_id", token_did, str)
        check_type("webhook_id", webhook_id, str)
        url = f"/v1/webhooks/{webhook_id}/unsubscribe/{token_did}"
        return self._request(
            "DELETE",
            "VehicleTriggers",
            url,
            headers=self._get_auth_headers(developer_jwt),
        )
