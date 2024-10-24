from typing import Optional
from dimo.errors import check_type, check_optional_type


class VehicleSignalDecoding:

    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers

    def list_config_urls_by_vin(self, vin: str, protocol: Optional[str] = None) -> dict:
        check_type("vin", vin, str)
        check_optional_type("protocol", protocol, str)
        params = {}
        if protocol is not None:
            params["protocol"] = protocol
        url = f"/v1/device-config/vin/{vin}/urls"
        return self._request("GET", "VehicleSignalDecoding", url, params=params)

    def list_config_urls_by_address(
        self, address: str, protocol: Optional[str] = None
    ) -> dict:
        check_type("address", address, str)
        check_optional_type("protocol", protocol, str)
        params = {}
        if protocol is not None:
            params["protocol"] = protocol
        url = f"/v1/device-config/eth-addr/{address}/urls"
        return self._request("GET", "VehicleSignalDecoding", url, params=params)

    def get_pid_configs(self, template_name: str) -> dict:
        check_type("template_name", template_name, str)
        url = f"/v1/device-config/pids/{template_name}"
        return self._request("GET", "VehicleSignalDecoding", url)

    def get_device_settings(self, template_name: str) -> dict:
        check_type("template_name", template_name, str)
        url = f"/v1/device-config/settings/{template_name}"
        return self._request("GET", "VehicleSignalDecoding", url)

    def get_dbc_text(self, template_name: str):
        check_type("template_name", template_name, str)
        url = f"/v1/device-config/dbc/{template_name}"
        return self._request("GET", "VehicleSignalDecoding", url)

    def get_device_status_by_address(self, address: str) -> dict:
        check_type("address", address, str)
        url = f"/v1/device-config/eth-addr/{address}/status"
        return self._request("GET", "VehicleSignalDecoding", url)

    def set_device_status_by_address(
        self, privilege_token: str, address: str, config: dict
    ) -> None:
        check_type("privilege_token", privilege_token, str)
        check_type("address", address, str)
        check_type("config", config, dict)
        body = {"config": config}
        url = f"/v1/device-config/eth-addr/{address}/status"
        return self._request(
            "PATCH",
            "VehicleSignalDecoding",
            url,
            data=body,
            headers=self._get_auth_headers(privilege_token),
        )

    def get_jobs_by_address(self, address: str):
        check_type("address", address, str)
        url = f"/v1/device-config/eth-addr/{address}/jobs"
        return self._request("GET", "VehicleSignalDecoding", url)

    def get_pending_jobs_by_address(self, address: str):
        check_type("address", address, str)
        url = f"/v1/device-config/eth-addr/{address}/jobs/pending"
        return self._request("GET", "VehicleSignalDecoding", url)

    def set_job_status_by_address(
        self, privilege_token: str, address: str, job_id: str, status: str
    ):
        check_type("privilege_token", privilege_token, str)
        check_type("address", address, str)
        check_type("job_id", job_id, str)
        check_type("status", status, str)
        url = f"/v1/device-config/eth-addr/{address}/jobs/{job_id}/{status}"
        return self._request(
            "PATCH",
            "VehicleSignalDecoding",
            url,
            headers=self._get_auth_headers(privilege_token),
        )
