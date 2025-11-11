"""
"""
AGXCL SDK for Python
Official SDK for AgeFix blockchain smart contracts
"""

from .client import AgefixClient, AgefixConfig, ContractDeployment, QueryResult, TransactionResult
from .contracts import TokenContract, NFTContract

__version__ = "1.0.0"
__author__ = "AgeFix Team"
__email__ = "dev@agefix.com"
__license__ = "MIT"

__all__ = [
    "AgefixClient",
    "AgefixConfig",
    "ContractDeployment",
    "QueryResult",
    "TransactionResult",
    "TokenContract",
    "NFTContract",
]

Official Python SDK for interacting with AGXCL smart contracts
"""

__version__ = "1.0.0"

from .client import AgefixClient
from .contracts import TokenContract, NFTContract

__all__ = ["AgefixClient", "TokenContract", "NFTContract"]
