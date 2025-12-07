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

The `examples/` directory contains comprehensive code examples for all AgeFix protocol interactions:

### 📁 Available Example Files

- **[defi_examples.py](examples/defi_examples.py)** - DeFi Protocol Examples
  - Liquidity pool creation and management
  - Token swaps with slippage protection
  - Lending and borrowing with collateral
  - Yield farming and staking
  - Portfolio analytics and TVL statistics

- **[gaming_examples.py](examples/gaming_examples.py)** - Gaming Protocol Examples
  - Game registration and session management
  - Tournament creation and participation
  - Achievement unlocking and tracking
  - Player statistics and leaderboards

- **[nft_examples.py](examples/nft_examples.py)** - NFT Marketplace Examples
  - NFT minting with metadata and IPFS
  - Listing and buying NFTs
  - Auction creation and bidding
  - NFT discovery and collection management

- **[governance_examples.py](examples/governance_examples.py)** - Governance Protocol Examples
  - Proposal creation and voting
  - Gauge weight voting for reward distribution
  - Validator bribes and incentives
  - Governance statistics and history

### 🚀 Running Examples

Each example file can be run directly or imported into your project:

```bash
# Install dependencies
pip install agxcl-sdk

# Set environment variables
export AGEFIX_API_KEY="your_api_key"
export WALLET_ADDRESS="your_wallet_address"
export PRIVATE_KEY="your_private_key"

# Run a specific example
python examples/defi_examples.py
python examples/gaming_examples.py
python examples/nft_examples.py
python examples/governance_examples.py
```

### 📖 Using Examples in Your Code

Import individual functions from example files:

```python
from examples.defi_examples import (
    create_liquidity_pool,
    swap_tokens,
    complete_defi_workflow
)
import asyncio

async def main():
    # Create a liquidity pool
    pool = await create_liquidity_pool()

    # Execute a token swap
    await swap_tokens(pool['poolId'], 'AGX', 100, 49.5)

    # Run complete DeFi workflow
    await complete_defi_workflow()

asyncio.run(main())
```

### 🎯 Quick Example: DeFi Swap

```python
import os
import asyncio
from agxcl_sdk import AgefixClient, AgefixConfig

client = AgefixClient(AgefixConfig(
    api_url='https://api.agefix.com',
    api_key=os.environ.get('AGEFIX_API_KEY'),
    wallet_address=os.environ.get('WALLET_ADDRESS'),
    private_key=os.environ.get('PRIVATE_KEY')
))

async def swap_example():
    # Get swap quote
    quote = await client.defi.get_swap_quote({
        'poolId': 'pool_123',
        'tokenIn': 'AGX',
        'amountIn': 100
    })

    print(f'You will receive: {quote["amountOut"]} CURE')

    # Execute swap with slippage protection
    result = await client.defi.swap({
        'poolId': 'pool_123',
        'tokenIn': 'AGX',
        'amountIn': 100,
        'minAmountOut': quote['amountOut'] * 0.99  # 1% slippage
    })

    print(f'Swap completed! {result["txHash"]}')

asyncio.run(swap_example())
```

### 🎮 Quick Example: Gaming Session

```python
async def gaming_example():
    # Register a game
    game = await client.gaming.register_game({
        'gameName': 'AgeFix Quest',
        'gameType': 'adventure',
        'entryFeeAgx': 10,
        'rewardPoolAgx': 1000
    })

    # Start game session
    session = await client.gaming.start_session({
        'gameId': game['gameId'],
        'difficulty': 'hard'
    })

    # Submit score with achievements
    result = await client.gaming.submit_score({
        'sessionId': session['sessionId'],
        'score': 9500,
        'achievementIds': ['first_win', 'speed_runner']
    })

    print(f'Earned: {result["rewardsEarned"]} AGX')

asyncio.run(gaming_example())
```

For more detailed examples, see the individual example files in the `examples/` directory.

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
