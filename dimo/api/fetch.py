from dimo.errors import check_type, check_optional_type


class Fetch:

    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers

    def _build_params(self, **kwargs):
        params = {}
        for key, value in kwargs.items():
            if value is not None:
                params[key] = value
        return params

    def get_index_keys(
        self,
        vehicle_jwt: str,
        token_id: int,
        after=None,
        before=None,
        id=None,
        limit=None,
        producer=None,
        source=None,
        type=None,
    ) -> dict:
        check_type("vehicle_jwt", vehicle_jwt, str)
        check_type("token_id", token_id, int)
        params = self._build_params(
            after=after, before=before, id=id, limit=limit,
            producer=producer, source=source, type=type,
        )
        url = f"/v1/vehicle/index-keys/{token_id}"
        return self._request(
            "GET",
            "Fetch",
            url,
            params=params,
            headers=self._get_auth_headers(vehicle_jwt),
        )

    def get_latest_index_key(
        self,
        vehicle_jwt: str,
        token_id: int,
        after=None,
        before=None,
        id=None,
        limit=None,
        producer=None,
        source=None,
        type=None,
    ) -> dict:
        check_type("vehicle_jwt", vehicle_jwt, str)
        check_type("token_id", token_id, int)
        params = self._build_params(
            after=after, before=before, id=id, limit=limit,
            producer=producer, source=source, type=type,
        )
        url = f"/v1/vehicle/latest-index-key/{token_id}"
        return self._request(
            "GET",
            "Fetch",
            url,
            params=params,
            headers=self._get_auth_headers(vehicle_jwt),
        )

    def get_latest_object(
        self,
        vehicle_jwt: str,
        token_id: int,
        after=None,
        before=None,
        id=None,
        limit=None,
        producer=None,
        source=None,
        type=None,
    ) -> dict:
        check_type("vehicle_jwt", vehicle_jwt, str)
        check_type("token_id", token_id, int)
        params = self._build_params(
            after=after, before=before, id=id, limit=limit,
            producer=producer, source=source, type=type,
        )
        url = f"/v1/vehicle/latest-object/{token_id}"
        return self._request(
            "GET",
            "Fetch",
            url,
            params=params,
            headers=self._get_auth_headers(vehicle_jwt),
        )

    def get_objects(
        self,
        vehicle_jwt: str,
        token_id: int,
        after=None,
        before=None,
        id=None,
        limit=None,
        producer=None,
        source=None,
        type=None,
    ) -> dict:
        check_type("vehicle_jwt", vehicle_jwt, str)
        check_type("token_id", token_id, int)
        params = self._build_params(
            after=after, before=before, id=id, limit=limit,
            producer=producer, source=source, type=type,
        )
        url = f"/v1/vehicle/objects/{token_id}"
        return self._request(
            "GET",
            "Fetch",
            url,
            params=params,
            headers=self._get_auth_headers(vehicle_jwt),
        )
