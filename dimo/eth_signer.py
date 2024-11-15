from eth_account import Account
from eth_account.messages import encode_defunct
from eth_utils import to_bytes


class EthSigner:
    @staticmethod
    def sign_message(message: str, private_key: str) -> str:
        message_bytes = to_bytes(text=message)
        signable_message = encode_defunct(message_bytes)
        account = Account.from_key(private_key)
        signed_message = account.sign_message(signable_message)

        return signed_message.signature.hex()
