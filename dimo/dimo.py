from requests import Session

from .api.attestation import Attestation
from .api.auth import Auth
from .api.conversations import Conversations
from .api.device_definitions import DeviceDefinitions
from .api.token_exchange import TokenExchange
from .api.trips import Trips
from .api.valuations import Valuations
from .api.vehicle_triggers import VehicleTriggers

from .graphql.identity import Identity
from .graphql.telemetry import Telemetry

from .request import Request
from .environments import dimo_environment
from typing import Optional
from typing_extensions import Dict
from typing import Any
from urllib.parse import urljoin


class DIMO:

    def __init__(
        self, env: str = "Production", session: Optional[Session] = None
    ) -> None:

        self.env = env
        # Assert valid environment specified
        if env not in dimo_environment:
            raise ValueError(f"Unknown environment: {env}")

        self.urls = dimo_environment[env]

        self._client_id: Optional[str] = None
        self._services: Dict[str, Any] = {}
        self.session = (
            session or Session()
        )  # Use the provided session or create a new one

    # Creates a full path for endpoints combining DIMO service, specific endpoint, and optional params
    def _get_full_path(self, service: str, path: str, params=None) -> str:
        base_path = self.urls[service]
        path_formatted = path.format(**(params or {}))
        return urljoin(base_path, path_formatted)

    # Sets headers based on access_token or privileged_token
    def _get_auth_headers(self, token):
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # request method for HTTP requests for the REST API
    def request(self, http_method, service, path, **kwargs):
        full_path = self._get_full_path(service, path)
        return Request(http_method, full_path, self.session)(**kwargs)

    # query method for graphQL queries, identity and telemetry
    def query(self, service, query, variables=None, token=None):
        headers = self._get_auth_headers(token) if token else {}
        headers["Content-Type"] = "application/json"
        headers["User-Agent"] = "dimo-python-sdk"

        data = {"query": query, "variables": variables or {}}

        response = self.request("POST", service, "", headers=headers, data=data)
        return response

    def __getattr__(self, name: str) -> Any:
        """
        Lazy-load and cache service modules as attributes
        """
        # If service is already created, return from cache
        if name in self._services:
            return self._services[name]
        # Otherwise, see if its a known service
        mapping = {
            "attestation": (Attestation, ("request", "_get_auth_headers")),
            "auth": (Auth, ("request", "_get_auth_headers", "env", "self")),
            "conversations": (Conversations, ("request", "_get_auth_headers", "_get_full_path", "session")),
            "device_definitions": (DeviceDefinitions, ("request", "_get_auth_headers")),
            "token_exchange": (
                TokenExchange,
                ("request", "_get_auth_headers", "identity", "self"),
            ),
            "trips": (Trips, ("request", "_get_auth_headers")),
            "valuations": (Valuations, ("request", "_get_auth_headers")),
            "identity": (Identity, ("self",)),
            "telemetry": (Telemetry, ("self",)),
            "vehicle_triggers": (VehicleTriggers, ("request", "_get_auth_headers")),
        }
        if name in mapping:
            cls, deps = mapping[name]
            args = [getattr(self, dep) if dep != "self" else self for dep in deps]
            instance = cls(*args)
            # And cache the service for future use
            self._services[name] = instance
            return instance
        raise AttributeError(
            f"{self.__class__.__name__!r} object has no attribute {name!r}"
        )
