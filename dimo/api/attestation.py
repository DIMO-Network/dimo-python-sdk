from dimo.errors import check_type, check_optional_type
from typing import Optional


class Attestation:
    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers

    def create_vin_vc(self, vehicle_jwt: str, token_id: int) -> dict:
        """
        Generate cryptographic proof of a vehicle's VIN or retrieve existing unexpired attestation.

        Args:
            vehicle_jwt (str): Authentication JWT token
            token_id (int): Vehicle token identifier

        Returns:
            dict: Response containing vcUrl, vcQuery, and confirmation message
        """
        check_type("vehicle_jwt", vehicle_jwt, str)
        check_type("token_id", token_id, int)
        url = f"/v2/attestation/vin/{token_id}"
        return self._request(
            "POST",
            "Attestation",
            url,
            headers=self._get_auth_headers(vehicle_jwt),
        )

    def create_pom_vc(self, vehicle_jwt: str, token_id: int) -> dict:
        """
        Create proof of movement verifiable credential (v1 API).

        Args:
            vehicle_jwt (str): Authentication JWT token
            token_id (int): Vehicle token identifier

        Returns:
            dict: Response from the API
        """
        check_type("vehicle_jwt", vehicle_jwt, str)
        check_type("token_id", token_id, int)
        url = f"/v1/vc/pom/{token_id}"
        return self._request(
            "POST", "Attestation", url, headers=self._get_auth_headers(vehicle_jwt)
        )

    def create_odometer_statement(
        self, vehicle_jwt: str, token_id: int, timestamp: Optional[str] = None
    ) -> dict:
        """
        Produce verifiable odometer reading attestation.

        Args:
            vehicle_jwt (str): Authentication JWT token
            token_id (int): Vehicle token identifier
            timestamp (str, optional): Specific moment for reading (ISO 8601 format)

        Returns:
            dict: Success message directing to telemetry-api retrieval
        """
        check_type("vehicle_jwt", vehicle_jwt, str)
        check_type("token_id", token_id, int)
        check_optional_type("timestamp", timestamp, str)

        url = f"/v2/attestation/odometer-statement/{token_id}"
        data = {}
        if timestamp:
            data["timestamp"] = timestamp

        return self._request(
            "POST",
            "Attestation",
            url,
            headers=self._get_auth_headers(vehicle_jwt),
            data=data if data else None,
        )

    def create_vehicle_health(
        self, vehicle_jwt: str, token_id: int, start_time: str, end_time: str
    ) -> dict:
        """
        Generate health status verification for specified timeframe.

        Args:
            vehicle_jwt (str): Authentication JWT token
            token_id (int): Vehicle token identifier
            start_time (str): Report beginning (ISO 8601 format)
            end_time (str): Report conclusion (ISO 8601 format)

        Returns:
            dict: Success message with telemetry-api retrieval instructions
        """
        check_type("vehicle_jwt", vehicle_jwt, str)
        check_type("token_id", token_id, int)
        check_type("start_time", start_time, str)
        check_type("end_time", end_time, str)

        url = f"/v2/attestation/vehicle-health/{token_id}"
        data = {"startTime": start_time, "endTime": end_time}

        return self._request(
            "POST",
            "Attestation",
            url,
            headers=self._get_auth_headers(vehicle_jwt),
            data=data,
        )

    def create_vehicle_position(
        self, vehicle_jwt: str, token_id: int, timestamp: str
    ) -> dict:
        """
        Produce location verification at specified moment.

        Args:
            vehicle_jwt (str): Authentication JWT token
            token_id (int): Vehicle token identifier
            timestamp (str): Location snapshot timing (ISO 8601 format)

        Returns:
            dict: Success message with telemetry-api retrieval instructions
        """
        check_type("vehicle_jwt", vehicle_jwt, str)
        check_type("token_id", token_id, int)
        check_type("timestamp", timestamp, str)

        url = f"/v2/attestation/vehicle-position/{token_id}"
        data = {"timestamp": timestamp}

        return self._request(
            "POST",
            "Attestation",
            url,
            headers=self._get_auth_headers(vehicle_jwt),
            data=data,
        )
