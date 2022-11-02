import base64

from .provider import SuiJsonRpcProvider
from .rpc_tx_data_serializer import RpcTxDataSerializer
from .wallet import SuiWallet
from .models import MoveCallTransaction


class SignerWithProvider:

    def __init__(self,
                 provider: SuiJsonRpcProvider,
                 serializer: RpcTxDataSerializer,
                 signer_wallet: SuiWallet
                 ):
        self.provider = provider
        self.serializer = serializer
        self.signer_wallet = signer_wallet

    def get_address(self):
        return self.signer_wallet.get_address()

    def sign_data(self, data: bytes):
        return self.signer_wallet.sign_data(data)

    def request_sui_from_faucet(self):
        return self.provider.request_tokens_from_faucet(self.get_address())

    def sign_and_execute_transaction(self, tx_bytes: bytes):
        signature_bytes = self.sign_data(tx_bytes)
        return self.provider.execute_transaction(
            tx_bytes_b64_encoded=base64.b64encode(tx_bytes).decode(),
            signature_b64_encoded=base64.b64encode(signature_bytes).decode(),
            pubkey_b64_encoded=self.signer_wallet.get_public_key_as_b64_string(),
        )

    def execute_move_call(self, tx_move_call: MoveCallTransaction):
        tx_bytes_b64 = self.serializer.new_move_call(
            signer_addr=self.signer_wallet.get_address(),
            tx=tx_move_call)["result"]["txBytes"]
        return self.sign_and_execute_transaction(tx_bytes=base64.b64decode(tx_bytes_b64))
