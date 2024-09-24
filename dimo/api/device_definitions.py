class DeviceDefinitions:

    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers

    def get_by_mmy(self, make, model, year):
        params = {
            'make': make,
            'model': model,
            'year': year
        }
        return self._request(
            'GET',
            'DeviceDefinitions',
            '/device-definitions',
            params=params
        )

    def get_by_id(self, id):
        url = f'/device-definitions/{id}'
        return self._request(
            'GET',
            'DeviceDefinitions',
            url)

    def list_device_makes(self):
        return self._request(
            'GET',
            'DeviceDefinitions',
            '/device-makes'
        )

    def get_device_type_by_id(self, id):
        url = f'/device-types/{id}'
        return self._request(
            'GET',
            'DeviceDefinitions',
            url)
