from dimo.constants import dimo_constants

class TokenExchange:

    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers

    async def exchange(self, access_token, privileges, token_id, env="Production"):
        body = {
                'nftContractAddress':  dimo_constants[env]['NFT_address'],
                'privileges': privileges,
                'tokenId': token_id
            }
        response = self._request(
            'POST',
            'TokenExchange',
            '/v1/tokens/exchange',
            headers=self._get_auth_headers(access_token),
            data=body
        )
        return response
