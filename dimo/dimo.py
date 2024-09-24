from .api.auth import Auth
from .api.device_data import DeviceData
from .api.device_definitions import DeviceDefinitions
from .api.devices import Devices
from .api.events import Events
from .api.token_exchange import TokenExchange
from .api.trips import Trips
from .api.user import User
from .api.valuations import Valuations
from .api.vehicle_signal_decoding import VehicleSignalDecoding

from .graphql.identity import Identity
from .graphql.telemetry import Telemetry

from .request import Request
from .environments import dimo_environment
import re

class DIMO:

    def __init__(self, env="Production"):
        self.env = env
        self.urls = dimo_environment[env]
        self.auth = Auth(self.request, self._get_auth_headers, self.env)
        self.device_data = DeviceData(self.request, self._get_auth_headers)
        self.device_definitions = DeviceDefinitions(self.request, self._get_auth_headers)
        self.devices = Devices(self.request, self._get_auth_headers)
        self.events = Events(self.request, self._get_auth_headers)
        self.token_exchange = TokenExchange(self.request, self._get_auth_headers)
        self.trips = Trips(self.request, self._get_auth_headers)
        self.user = User(self.request, self._get_auth_headers)
        self.valuations = Valuations(self.request, self._get_auth_headers)
        self.vehicle_signal_decoding = VehicleSignalDecoding(self.request, self._get_auth_headers)
        self.identity = Identity(self)
        self.telemetry = Telemetry(self)
        self._session = Request.session

    # Creates a full path for endpoints combining DIMO service, specific endpoint, and optional params
    def _get_full_path(self, service, path, params=None):
        base_path = self.urls[service] 
        full_path = f"{base_path}{path}"

        if params:
            for key, value in params.items():
                pattern = f":{key}"
                full_path = re.sub(pattern, str(value), full_path)
        return full_path 

    # Sets headers based on access_token or privileged_token
    def _get_auth_headers(self, token):
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    # request method for HTTP requests for the REST API
    def request(self, http_method, service, path, **kwargs):
        full_path = self._get_full_path(service, path)
        return Request(http_method, full_path)(**kwargs)

    # query method for graphQL queries, identity and telemetry
    def query(self, service, query, variables=None, token=None):
        headers = self._get_auth_headers(token) if token else {}
        headers['Content-Type'] = 'application/json'
        headers['User-Agent'] = 'dimo-python-sdk'

        data = {
            'query': query,
            'variables': variables or {}
        }

        response = self.request(
            'POST',
            service,
            '',
            headers=headers,
            data=data
        )
        return response
