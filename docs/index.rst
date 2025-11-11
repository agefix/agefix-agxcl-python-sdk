AGXCL Python SDK Documentation
================================

.. image:: https://img.shields.io/pypi/v/agxcl-sdk.svg
   :target: https://pypi.org/project/agxcl-sdk/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/agxcl-sdk.svg
   :target: https://pypi.org/project/agxcl-sdk/
   :alt: Python versions

Official Python SDK for building applications on the AgeFix blockchain using the AGXCL smart contract language.

Installation
------------

Install using pip:

.. code-block:: bash

   pip install agxcl-sdk

Quick Start
-----------

Here's a simple example to get you started:

.. code-block:: python

   from agxcl_sdk import AgefixClient, AgefixConfig, TokenContract

   # Initialize client
   config = AgefixConfig(
       rpc_url="https://rpc.agefix.com",
       chain_id="agefix-mainnet-1",
       private_key="your-private-key"
   )
   client = AgefixClient(config)

   # Deploy a token contract
   token = TokenContract(client)
   deployment = token.deploy(
       name="MyToken",
       symbol="MTK",
       total_supply="1000000"
   )

   print(f"Contract deployed at: {deployment.contract_address}")

   # Transfer tokens
   tx = token.transfer(
       to="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
       amount="100"
   )
   print(f"Transfer completed: {tx.tx_hash}")

Features
--------

* 🚀 **Easy Contract Deployment**: Deploy AGXCL smart contracts with simple Python functions
* 🔍 **Contract Queries**: Read contract state with intuitive query methods
* ✍️ **Transaction Execution**: Execute state-changing contract methods
* 💰 **Token Support**: Built-in helpers for ERC-20 style tokens
* 🎨 **NFT Support**: Simplified NFT minting and management
* ⛽ **Gas Estimation**: Estimate transaction costs before execution
* 🔐 **Type Safety**: Full type hints for better IDE support
* 📊 **Dataclasses**: Clean, Pythonic data structures

Examples
--------

Token Contract
~~~~~~~~~~~~~~

.. code-block:: python

   from agxcl_sdk import AgefixClient, AgefixConfig, TokenContract

   config = AgefixConfig(
       rpc_url="https://rpc.agefix.com",
       chain_id="agefix-mainnet-1",
       private_key="your-private-key"
   )
   client = AgefixClient(config)

   # Deploy token
   token = TokenContract(client)
   deployment = token.deploy("MyToken", "MTK", "1000000")
   
   # Check balance
   balance = token.balance_of("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb")
   print(f"Balance: {balance}")
   
   # Transfer tokens
   tx = token.transfer("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb", "100")
   print(f"Transfer TX: {tx.tx_hash}")

NFT Contract
~~~~~~~~~~~~

.. code-block:: python

   from agxcl_sdk import AgefixClient, AgefixConfig, NFTContract

   config = AgefixConfig(
       rpc_url="https://rpc.agefix.com",
       chain_id="agefix-mainnet-1",
       private_key="your-private-key"
   )
   client = AgefixClient(config)

   # Deploy NFT collection
   nft = NFTContract(client)
   deployment = nft.deploy("MyNFTs", "MNFT")
   
   # Mint NFT
   tx = nft.mint(
       to="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
       uri="ipfs://QmXxxx..."
   )
   print(f"NFT minted: {tx.tx_hash}")
   
   # Get owner
   owner = nft.owner_of(1)
   print(f"Token #1 owner: {owner}")

Custom Contract Interaction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from agxcl_sdk import AgefixClient, AgefixConfig

   config = AgefixConfig(
       rpc_url="https://rpc.agefix.com",
       chain_id="agefix-mainnet-1",
       private_key="your-private-key"
   )
   client = AgefixClient(config)

   # Deploy custom contract
   contract_code = """
   contract MyContract {
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
   
   # Execute transaction
   client.execute_transaction(
       deployment.contract_address,
       "setValue",
       [42]
   )
   
   # Query state
   result = client.query_contract(
       deployment.contract_address,
       "getValue"
   )
   print(f"Value: {result.data}")

API Reference
-------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

Client
~~~~~~

.. autoclass:: agxcl_sdk.client.AgefixClient
   :members:
   :undoc-members:
   :show-inheritance:

Configuration
~~~~~~~~~~~~~

.. autoclass:: agxcl_sdk.client.AgefixConfig
   :members:
   :undoc-members:
   :show-inheritance:

Result Types
~~~~~~~~~~~~

.. autoclass:: agxcl_sdk.client.ContractDeployment
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: agxcl_sdk.client.QueryResult
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: agxcl_sdk.client.TransactionResult
   :members:
   :undoc-members:
   :show-inheritance:

Contract Helpers
~~~~~~~~~~~~~~~~

.. autoclass:: agxcl_sdk.contracts.TokenContract
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: agxcl_sdk.contracts.NFTContract
   :members:
   :undoc-members:
   :show-inheritance:

Contributing
------------

We welcome contributions! Please see our `GitHub repository <https://github.com/agefix/agxcl-sdk-python>`_ for guidelines.

Support
-------

* Documentation: https://docs.agefix.com/python-sdk/
* GitHub: https://github.com/agefix/agxcl-sdk-python
* Discord: https://discord.gg/agefix
* Website: https://agefix.com

License
-------

MIT License - see LICENSE file for details.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
