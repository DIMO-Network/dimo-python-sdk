from dimo.constants import dimo_constants
from dimo.errors import check_type, check_optional_type
from dimo.permission_decoder import PermissionDecoder
import json


class TokenExchange:

    def __init__(
        self, request_method, get_auth_headers, identity_instance, dimo_instance
    ):
        self._request = request_method
        self._get_auth_headers = get_auth_headers
        self._identity = identity_instance
        self._dimo = dimo_instance
        self._permission_decoder = PermissionDecoder()

    def _decode_vehicle_permissions(self, token_id: int, client_id: str) -> dict:
        response = self._identity.check_vehicle_privileges(token_id)
        try:
            # If response is bytes
            response = json.loads(response.decode('utf-8'))
            nodes = (
                response.get("data", {})
                .get("vehicle", {})
                .get("sacds", {})
                .get("nodes", [])
            )
            if not nodes or not isinstance(nodes, list):
                raise ValueError("Invalid response from server")
            filtered_sacd = next(
                (
                    node
                    for node in nodes
                    if node.get("grantee").lower() == client_id.lower()
                ),
                None,
            )

            if not filtered_sacd:
                raise ValueError(
                    f"No permissions found for developer license: {client_id}. "
                    "Has this vehicle been shared?"
                )

            return self._permission_decoder.decode_permission_bits(
                filtered_sacd["permissions"]
            )

        except Exception as e:
            raise ValueError(f"Failed to decode permissions: {str(e)}")

    def exchange(
        self,
        developer_jwt: str,
        token_id: int,
        client_id: str = None,
        env: str = "Production",
        privileges: list = None,
    ) -> dict:

        if client_id is None:
            client_id = self._dimo._client_id
            if not client_id:
                raise ValueError(
                    "No client_id found. Please make sure you've obtained a Developer JWT before calling token exchange."
                )
        check_type("developer_jwt", developer_jwt, str)
        check_optional_type("privileges", privileges, list)
        check_type("token_id", token_id, int)
        check_type("client_id", client_id, str)

        if privileges is None:
            privileges = self._decode_vehicle_permissions(token_id, client_id)

        body = {
            "nftContractAddress": dimo_constants[env]["NFT_address"],
            "privileges": privileges,
            "tokenId": token_id,
        }
        response = self._request(
            "POST",
            "TokenExchange",
            "/v1/tokens/exchange",
            headers=self._get_auth_headers(developer_jwt),
            data=body,
        )
        return response
