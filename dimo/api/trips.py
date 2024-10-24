from dimo.errors import check_type


class Trips:

    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers

    def trips(self, privilege_token: str, token_id: str, page=None) -> dict:
        check_type("privilege_token", privilege_token, str)
        check_type("token_id", token_id, str)
        params = {}
        if page is not None:
            params["page"] = [page]
        url = f"/v1/vehicle/{token_id}/trips"
        return self._request(
            "GET",
            "Trips",
            url,
            params=params,
            headers=self._get_auth_headers(privilege_token),
        )
