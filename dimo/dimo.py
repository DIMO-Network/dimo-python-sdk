from .api.attestation import Attestation
from .api.auth import Auth
from .api.device_definitions import DeviceDefinitions
from .api.token_exchange import TokenExchange
from .api.trips import Trips
from .api.valuations import Valuations
from .api.vehicle_events import VehicleEvents

from .graphql.identity import Identity
from .graphql.telemetry import Telemetry

from .request import Request
from .environments import dimo_environment
import re


class DIMO:

    def __init__(self, env="Production"):
        self.env = env
        self.urls = dimo_environment[env]
        self._client_id = None
        self.attestation = Attestation(self.request, self._get_auth_headers)
        self.auth = Auth(self.request, self._get_auth_headers, self.env, self)
        self.device_definitions = DeviceDefinitions(
            self.request, self._get_auth_headers
        )
        self.identity = Identity(self)
        self.token_exchange = TokenExchange(
            self.request, self._get_auth_headers, self.identity, self
        )
        self.trips = Trips(self.request, self._get_auth_headers)
        self.valuations = Valuations(self.request, self._get_auth_headers)
        self.telemetry = Telemetry(self)
        self.vehicle_events = VehicleEvents(self.request, self._get_auth_headers)
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
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # request method for HTTP requests for the REST API
    def request(self, http_method, service, path, **kwargs):
        full_path = self._get_full_path(service, path)
        return Request(http_method, full_path)(**kwargs)

    # query method for graphQL queries, identity and telemetry
    def query(self, service, query, variables=None, token=None):
        headers = self._get_auth_headers(token) if token else {}
        headers["Content-Type"] = "application/json"
        headers["User-Agent"] = "dimo-python-sdk"

        data = {"query": query, "variables": variables or {}}

        response = self.request("POST", service, "", headers=headers, data=data)
        return response
