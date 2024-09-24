class Valuations:

    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers

    def get_valuations(self, access_token, user_device_id):
        url = f'/v1/user/devices/{user_device_id}/valuations'
        return self._request(
            'GET',
            'Valuations',
            url,
            headers=self._get_auth_headers(access_token)
        )

    def get_instant_offer(self, access_token, user_device_id):
        url = f'/v1/user/devices/{user_device_id}/instant-offer'
        return self._request(
            'GET',
            'Valuations',
            url,
            headers=self._get_auth_headers(access_token)
        )

    def get_offers(self, access_token, user_device_id):
        url = f'/v1/user/devices/{user_device_id}/offers'
        return self._request(
            'GET',
            'Valuations',
            url,
            headers=self._get_auth_headers(access_token)
        )
