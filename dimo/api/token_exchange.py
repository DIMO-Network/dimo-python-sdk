from dimo.constants import dimo_constants

class TokenExchange:

    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers

    def exchange(self, token, privileges, token_id, env="Production"):
        body = {
                'nftContractAddress':  dimo_constants[env]['NFT_address'],
                'privileges': privileges,
                'tokenId': token_id
            }
        response = self._request(
            'POST',
            'TokenExchange',
            '/v1/tokens/exchange',
            headers=self._get_auth_headers(token),
            data=body
        )
        return response
