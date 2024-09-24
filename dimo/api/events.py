class Events:

    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers

    def get_events(self, access_token):
        return self._request(
            'GET',
            'Events',
            '/v1/events',
            headers=self._get_auth_headers(access_token)
        )
