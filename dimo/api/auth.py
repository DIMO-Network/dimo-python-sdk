from web3 import Web3
from eth_account.messages import encode_defunct
from dimo.constants import dimo_constants
from dimo.errors import check_type, check_optional_type
from urllib.parse import urlencode
from typing import Dict, Optional


class Auth:

    def __init__(self, request_method, get_auth_headers, env):
        self._request = request_method
        self._get_auth_headers = get_auth_headers
        self.env = env

    def generate_challenge(
        self,
        client_id: str,
        domain: str,
        address: str,
        headers: Dict[str, str] = {"Content-Type": "application/x-www-form-urlencoded"},
        scope: str = "openid email",
        response_type: str = "code",
    ) -> Dict:
        check_type("client_id", client_id, str)
        check_type("domain", domain, str)
        check_type("address", address, str)
        if headers != {"Content-Type": "application/x-www-form-urlencoded"}:
            raise ValueError(
                "Headers must be '{'Content-Type': 'application/x-www-form-urlencoded'}'"
            )
        body = {
            "client_id": client_id,
            "domain": domain,
            "scope": scope,
            "response_type": response_type,
            "address": address,
        }

        return self._request(
            "POST",
            "Auth",
            "/auth/web3/generate_challenge",
            data=urlencode(body),
            headers=headers,
        )

    def sign_challenge(self, message: str, private_key: str) -> str:
        check_type("message", message, str)
        check_type("private_key", private_key, str)

        web3 = Web3(Web3.HTTPProvider(dimo_constants[self.env]["RPC_provider"]))
        signed_message = web3.eth.account.sign_message(
            encode_defunct(text=message), private_key=private_key
        )
        return signed_message.signature.hex()

    def submit_challenge(
        self,
        client_id: str,
        domain: str,
        state: str,
        signature: str,
        headers: Dict[str, str] = {"Content-Type": "application/x-www-form-urlencoded"},
    ) -> Dict:
        check_type("client_id", client_id, str)
        check_type("domain", domain, str)
        check_type("state", state, str)
        check_type("signature", signature, str)
        check_type("headers", headers, dict)
        if headers != {"Content-Type": "application/x-www-form-urlencoded"}:
            raise ValueError(
                "Headers must be '{'Content-Type': 'application/x-www-form-urlencoded'}'"
            )

        form_data = {
            "client_id": client_id,
            "domain": domain,
            "state": state,
            "signature": signature,
            "grant_type": "authorization_code",
        }

        return self._request(
            "POST",
            "Auth",
            "/auth/web3/submit_challenge",
            data=form_data,
            headers=headers,
        )

    # Requires client_id, domain, and private_key. Address defaults to client_id.
    def get_token(
        self,
        client_id: str,
        domain: str,
        private_key: str,
        address: Optional[str] = None,
        scope="openid email",
        response_type="code",
    ) -> Dict:
        check_type("client_id", client_id, str)
        check_type("domain", domain, str)
        check_type("private_key", private_key, str)
        check_optional_type("address", address, str)

        if address is None:
            address = client_id

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        challenge = self.generate_challenge(
            headers=headers,
            client_id=client_id,
            domain=domain,
            scope=scope,
            response_type=response_type,
            address=address,
        )

        sign = self.sign_challenge(
            message=challenge["challenge"],
            private_key=private_key,
        )

        state = challenge["state"]
        signature = sign

        submit = self.submit_challenge(client_id, domain, state, signature, headers)
        return submit
