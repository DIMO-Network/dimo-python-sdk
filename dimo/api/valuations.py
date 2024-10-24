from dimo.errors import check_type


class Valuations:

    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers

    def get_valuations(self, access_token: str, user_device_id: int) -> dict:
        check_type("access_token", access_token, str)
        check_type("token_id", user_device_id, int)
        url = f"/v1/user/devices/{user_device_id}/valuations"
        return self._request(
            "GET", "Valuations", url, headers=self._get_auth_headers(access_token)
        )

    def get_instant_offer(self, access_token: str, user_device_id: str) -> None:
        check_type("access_token", access_token, str)
        check_type("user_device_id", user_device_id, str)
        url = f"/v1/user/devices/{user_device_id}/instant-offer"
        return self._request(
            "GET", "Valuations", url, headers=self._get_auth_headers(access_token)
        )

    def get_offers(self, access_token: str, user_device_id: str) -> dict:
        check_type("access_token", access_token, str)
        check_type("user_device_id", user_device_id, str)
        url = f"/v1/user/devices/{user_device_id}/offers"
        return self._request(
            "GET", "Valuations", url, headers=self._get_auth_headers(access_token)
        )
