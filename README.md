# agxcl-sdk

Official Python SDK for interacting with AGXCL smart contracts on the AgeFix blockchain.

## Installation

```bash
pip install agxcl-sdk
```

## Quick Start

```python
from agxcl_sdk import AgefixClient, AgefixConfig, TokenContract

# Initialize client
client = AgefixClient(AgefixConfig(
    rpc_url="https://rpc.agefix.com",
    chain_id="agefix-mainnet-1",
    private_key="YOUR_PRIVATE_KEY"  # Optional, required for transactions
))

# Deploy a token contract
token = TokenContract(client)
deployment = token.deploy("MyToken", "MTK", "1000000")
print(f"Token deployed at: {deployment.contract_address}")

# Transfer tokens
token.transfer("0x...recipientAddress", "100")
```

## Features

- 🚀 Simple API for contract deployment and interaction
- 💰 Built-in helpers for Token and NFT contracts
- 🔒 Secure transaction signing
- 📊 Query contract state
- ⛽ Gas estimation
- 🔍 Transaction receipts and status

## API Reference

### AgefixClient

#### Initialization
```python
from agxcl_sdk import AgefixClient, AgefixConfig

client = AgefixClient(AgefixConfig(
    rpc_url="https://rpc.agefix.com",
    chain_id="agefix-mainnet-1",
    private_key="your_private_key"
))
```

#### Methods

**deploy_contract(contract_code, constructor_args=None)**
Deploy a new AGXCL smart contract.

```python
deployment = client.deploy_contract(contract_code, ["arg1", "arg2"])
```

**query_contract(contract_address, method, args=None)**
Query contract state (read-only operation).

```python
result = client.query_contract(contract_address, "getValue", [])
```

**execute_transaction(contract_address, method, args=None, value="0")**
Execute a state-changing transaction.

```python
tx = client.execute_transaction(contract_address, "setValue", [42])
```

**get_balance(address)**
Get AGX token balance for an address.

```python
balance = client.get_balance("0x...")
```

**estimate_gas(contract_address, method, args=None)**
Estimate gas cost for a transaction.

```python
gas = client.estimate_gas(contract_address, "setValue", [42])
```

### TokenContract

Helper class for ERC-20 style tokens.

```python
from agxcl_sdk import TokenContract

token = TokenContract(client)
deployment = token.deploy("Token Name", "SYMBOL", "1000000")
tx = token.transfer(to_address, "100")
tx = token.approve(spender_address, "100")
balance = token.balance_of(address)
```

### NFTContract

Helper class for NFT (non-fungible token) contracts.

```python
from agxcl_sdk import NFTContract

nft = NFTContract(client)
deployment = nft.deploy("NFT Collection", "NFT")
tx = nft.mint(owner_address, "ipfs://metadata-uri")
owner = nft.owner_of(token_id)
```

## Examples

### Deploy Custom Contract

```python
contract_code = """
contract SimpleStorage {
  state {
    uint256 value;
  }

  function setValue(uint256 newValue) public {
    value = newValue;
  }

  function getValue() public view returns (uint256) {
    return value;
  }
}
"""

deployment = client.deploy_contract(contract_code)
client.execute_transaction(deployment.contract_address, "setValue", [42])
result = client.query_contract(deployment.contract_address, "getValue", [])
print(f"Stored value: {result.data}")
```

### Check Transaction Status

```python
tx = token.transfer(recipient_address, "100")
receipt = client.get_transaction_receipt(tx.tx_hash)
print(f"Transaction status: {receipt['status']}")
print(f"Block number: {receipt['blockNumber']}")
print(f"Gas used: {receipt['gasUsed']}")
```

## Error Handling

```python
try:
    token.transfer(to_address, amount)
except RuntimeError as e:
    print(f"Transaction failed: {e}")
```

## Security

- Never commit private keys to version control
- Use environment variables for sensitive data
- Always estimate gas before transactions
- Validate contract addresses and amounts

## License

MIT

## Support

- Documentation: https://agefix.com/developers
- GitHub: https://github.com/agefix/agxcl-sdk-python
- Discord: https://discord.gg/agefix
