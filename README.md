
Python SDK to interact with Sui Blockchain 

Supports creating wallets, fetching data, signing transactions 
# Install
``
pip install sui-python-sdk
``

Todo: 
- Better type checking
- Use objects instead of json or dict models 
- More functions & helpers   
- Add more examples 
- Add support for Secp256k1 Signing (only ed25519 now)
- Add websocket support & event subscription 
- Add support for publishing move packages 

# How to Use 
### Import required objects 
```python
from sui_python_sdk.wallet import SuiWallet
from sui_python_sdk.provider import SuiJsonRpcProvider
from sui_python_sdk.rpc_tx_data_serializer import RpcTxDataSerializer
from sui_python_sdk.signer_with_provider import SignerWithProvider
from sui_python_sdk.models import TransferObjectTransaction,TransferSuiTransaction,MoveCallTransaction
```

### Wallet 
```python
# Create wallet using a mnemonic
mnemonic = "all all all all all all all all all all all all"
my_wallet = SuiWallet(mnemonic=mnemonic)
# Create a new wallet with random address
random_wallet = SuiWallet.create_random_wallet()
```
```python
# Get address of your wallet 
my_wallet.get_address()
> '0xbb98ad0ae2f72677c6526d66ca3d3669c280c25a'
```
```python
random_wallet.get_address()
>'0x97534f7d430793fa4ff4619a5431c3d72fe8397d'
```

### Providers
```python
# Setup Providers
rpc_url = "https://fullnode.devnet.sui.io"
faucet_url ="https://faucet.devnet.sui.io/gas"

provider = SuiJsonRpcProvider(rpc_url=rpc_url, faucet_url=faucet_url)
serializer = RpcTxDataSerializer(rpc_url=rpc_url)
signer = SignerWithProvider(provider=provider, serializer=serializer, signer_wallet=my_wallet)
```

```python
# Request tokens to your wallet 
provider.request_tokens_from_faucet(my_wallet.get_address())
```


```python
# Get objects owned by wallet
provider.get_objects_owned_by_address(my_wallet.get_address())
```
### Execute Transaction
```python
# Transfer an Object 
object_id_to_transfer = next(item for item in provider.get_objects_owned_by_address(my_wallet.get_address())["result"] if item["type"]=='0x2::coin::Coin<0x2::sui::SUI>')["objectId"]
> '0x1794085eed584e9aaafa317c6f0422f814ffb260'
```

```python
# Create a move call transaction
tmp_move_call = MoveCallTransaction(
                   package_object_id="0x2",
                   module="sui",
                   function="transfer", 
                   type_arguments=[], 
                   arguments=[
                       object_id_to_transfer,
                       random_wallet.get_address()
                   ], 
                   gas_budget=1000,
                   gas_payment=None, 
                )

# Sign and execute the transaction
signer.execute_move_call(tx_move_call=tmp_move_call)
```

#### Fetch the Transaction
```python
# Get the transaction 
provider.get_transaction_with_effects('OF1XpY/BYHQhUjtjzN7IlwxD/YTC1yFQ5Dvh8zzC2Uc=')
```