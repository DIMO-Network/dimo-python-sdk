from dimo.constants import dimo_constants
from dimo.errors import check_type


class TokenExchange:

    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers

    def exchange(
        self, token: str, privileges: list, token_id: int, env: str = "Production"
    ) -> dict:
        check_type("token", token, str)
        check_type("privileges", privileges, list)
        check_type("token_id", token_id, int)
        body = {
            "nftContractAddress": dimo_constants[env]["NFT_address"],
            "privileges": privileges,
            "tokenId": token_id,
        }
        response = self._request(
            "POST",
            "TokenExchange",
            "/v1/tokens/exchange",
            headers=self._get_auth_headers(token),
            data=body,
        )
        return response
