from dimo.errors import check_type


class DeviceDefinitions:

    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers

    def get_by_mmy(self, make: str, model: str, year: int) -> dict:
        check_type("make", make, str)
        check_type("model", model, str)
        check_type("year", year, int)
        params = {"make": make, "model": model, "year": year}
        return self._request(
            "GET", "DeviceDefinitions", "/device-definitions", params=params
        )

    def get_by_id(self, id: str) -> dict:
        check_type("id", id, str)
        url = f"/device-definitions/{id}"
        return self._request("GET", "DeviceDefinitions", url)

    def list_device_makes(self) -> dict:
        return self._request("GET", "DeviceDefinitions", "/device-makes")

    def get_device_type_by_id(self, id: str):
        check_type("id", id, str)
        url = f"/device-types/{id}"
        return self._request("GET", "DeviceDefinitions", url)
