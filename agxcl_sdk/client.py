"""
AgeFix AGXCL SDK Client
Provides methods for deploying and interacting with AGXCL smart contracts
"""

import requests
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class AgefixConfig:
    """Configuration for AgeFix client"""
    rpc_url: str
    chain_id: str
    private_key: Optional[str] = None


@dataclass
class ContractDeployment:
    """Contract deployment result"""
    contract_address: str
    transaction_hash: str
    block_number: int


@dataclass
class QueryResult:
    """Contract query result"""
    success: bool
    data: Any
    error: Optional[str] = None


@dataclass
class TransactionResult:
    """Transaction execution result"""
    tx_hash: str
    block_number: int
    gas_used: int
    success: bool


class AgefixClient:
    """
    AgeFix AGXCL SDK Client
    
    Example:
        >>> client = AgefixClient(AgefixConfig(
        ...     rpc_url="https://rpc.agefix.com",
        ...     chain_id="agefix-mainnet-1",
        ...     private_key="your_private_key"
        ... ))
        >>> deployment = client.deploy_contract(contract_code)
        >>> result = client.query_contract(deployment.contract_address, "getValue", [])
    """
    
    def __init__(self, config: AgefixConfig):
        """Initialize AgeFix client with configuration"""
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
    
    def deploy_contract(
        self,
        contract_code: str,
        constructor_args: Optional[List[Any]] = None
    ) -> ContractDeployment:
        """
        Deploy a new AGXCL smart contract
        
        Args:
            contract_code: AGXCL contract source code
            constructor_args: Constructor arguments (optional)
            
        Returns:
            ContractDeployment with contract address and transaction info
            
        Raises:
            RuntimeError: If deployment fails
        """
        if constructor_args is None:
            constructor_args = []
        
        try:
            response = self.session.post(
                f"{self.config.rpc_url}/deploy",
                json={
                    "code": contract_code,
                    "args": constructor_args,
                    "chainId": self.config.chain_id,
                    "privateKey": self.config.private_key
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            return ContractDeployment(
                contract_address=data["contractAddress"],
                transaction_hash=data["txHash"],
                block_number=data["blockNumber"]
            )
        except Exception as e:
            raise RuntimeError(f"Contract deployment failed: {str(e)}")
    
    def query_contract(
        self,
        contract_address: str,
        method: str,
        args: Optional[List[Any]] = None
    ) -> QueryResult:
        """
        Query contract state (read-only)
        
        Args:
            contract_address: Address of deployed contract
            method: Method name to call
            args: Method arguments (optional)
            
        Returns:
            QueryResult with data or error
        """
        if args is None:
            args = []
        
        try:
            response = self.session.post(
                f"{self.config.rpc_url}/query",
                json={
                    "contractAddress": contract_address,
                    "method": method,
                    "args": args,
                    "chainId": self.config.chain_id
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            return QueryResult(success=True, data=data["result"])
        except Exception as e:
            return QueryResult(success=False, data=None, error=str(e))
    
    def execute_transaction(
        self,
        contract_address: str,
        method: str,
        args: Optional[List[Any]] = None,
        value: str = "0"
    ) -> TransactionResult:
        """
        Execute contract transaction (state-changing)
        
        Args:
            contract_address: Address of deployed contract
            method: Method name to call
            args: Method arguments (optional)
            value: Amount of AGX tokens to send (optional)
            
        Returns:
            TransactionResult with transaction info
            
        Raises:
            RuntimeError: If transaction fails or private key not provided
        """
        if not self.config.private_key:
            raise RuntimeError("Private key required for transactions")
        
        if args is None:
            args = []
        
        try:
            response = self.session.post(
                f"{self.config.rpc_url}/execute",
                json={
                    "contractAddress": contract_address,
                    "method": method,
                    "args": args,
                    "value": value,
                    "chainId": self.config.chain_id,
                    "privateKey": self.config.private_key
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            return TransactionResult(
                tx_hash=data["txHash"],
                block_number=data["blockNumber"],
                gas_used=data["gasUsed"],
                success=True
            )
        except Exception as e:
            raise RuntimeError(f"Transaction execution failed: {str(e)}")
    
    def get_transaction_receipt(self, tx_hash: str) -> Dict[str, Any]:
        """
        Get transaction receipt
        
        Args:
            tx_hash: Transaction hash
            
        Returns:
            Transaction receipt with status and logs
        """
        try:
            response = self.session.get(
                f"{self.config.rpc_url}/tx/{tx_hash}",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise RuntimeError(f"Failed to get transaction receipt: {str(e)}")
    
    def get_balance(self, address: str) -> str:
        """
        Get account balance
        
        Args:
            address: Account address
            
        Returns:
            Balance in AGX tokens
        """
        try:
            response = self.session.get(
                f"{self.config.rpc_url}/balance/{address}",
                timeout=30
            )
            response.raise_for_status()
            return response.json()["balance"]
        except Exception as e:
            raise RuntimeError(f"Failed to get balance: {str(e)}")
    
    def estimate_gas(
        self,
        contract_address: str,
        method: str,
        args: Optional[List[Any]] = None
    ) -> int:
        """
        Estimate gas for transaction
        
        Args:
            contract_address: Contract address
            method: Method name
            args: Method arguments (optional)
            
        Returns:
            Estimated gas cost
        """
        if args is None:
            args = []
        
        try:
            response = self.session.post(
                f"{self.config.rpc_url}/estimateGas",
                json={
                    "contractAddress": contract_address,
                    "method": method,
                    "args": args,
                    "chainId": self.config.chain_id
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json()["gasEstimate"]
        except Exception as e:
            raise RuntimeError(f"Failed to estimate gas: {str(e)}")
