# Changelog

All notable changes to the AGXCL Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-07

### Added
- Initial release of AGXCL Python SDK
- `AgefixClient` class for blockchain interactions
- `AgefixConfig` dataclass for configuration
- `TokenContract` helper for ERC-20 style tokens
- `NFTContract` helper for NFT management
- Contract deployment functionality
- Contract query methods (read-only operations)
- Transaction execution (state-changing operations)
- Gas estimation capabilities
- Balance checking utilities
- Transaction receipt retrieval
- Full type hints with dataclasses
- Comprehensive docstrings (Google/NumPy style)
- Sphinx documentation
- Example code for common use cases

### Features
- **Contract Deployment**: Deploy AGXCL smart contracts with constructor arguments
- **Contract Queries**: Execute read-only contract method calls
- **Transactions**: Submit signed transactions to blockchain
- **Token Operations**: Create, transfer, and manage ERC-20 tokens
- **NFT Operations**: Mint, transfer, and query NFTs
- **Gas Estimation**: Predict transaction costs before execution
- **Account Management**: Query balances and transaction history
- **Type Safety**: Full type hints and dataclasses
- **Pythonic API**: Clean, idiomatic Python design
- **Documentation**: Sphinx-generated HTML docs with API reference

### Dataclasses
- `AgefixConfig`: Client configuration
- `ContractDeployment`: Deployment result information
- `QueryResult`: Contract query results
- `TransactionResult`: Transaction execution results

### Dependencies
- requests >=2.31.0
- eth-account >=0.10.0
- web3 >=6.11.0

### Development Dependencies
- pytest >=7.4.0
- black >=23.0.0
- mypy >=1.5.0

### Documentation Dependencies
- sphinx >=7.2.6
- sphinx-rtd-theme >=2.0.0

### Python Version Support
- Python 3.8+
- Python 3.9
- Python 3.10
- Python 3.11

### Documentation
- Sphinx documentation in `/docs/`
- Build with: `cd docs && make html`
- API reference with autodoc
- Napoleon-style docstrings
- Intersphinx links to Python docs

### License
MIT License

### Repository
https://github.com/agefix/agxcl-sdk-python

### PyPI Package
https://pypi.org/project/agxcl-sdk/
