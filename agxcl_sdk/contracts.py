"""
Helper classes for common contract types
"""

from typing import Optional
from .client import AgefixClient


class TokenContract:
    """
    Helper class for ERC-20 style token contracts
    
    Example:
        >>> token = TokenContract(client)
        >>> deployment = token.deploy("MyToken", "MTK", "1000000")
        >>> token.transfer("0x...", "100")
    """
    
    def __init__(self, client: AgefixClient, contract_address: Optional[str] = None):
        """
        Initialize token contract helper
        
        Args:
            client: AgefixClient instance
            contract_address: Address of existing contract (optional)
        """
        self.client = client
        self.contract_address = contract_address
    
    def deploy(self, name: str, symbol: str, total_supply: str):
        """
        Deploy a new token contract
        
        Args:
            name: Token name
            symbol: Token symbol
            total_supply: Initial token supply
            
        Returns:
            ContractDeployment info
        """
        token_code = f'''
contract Token {{
  state {{
    string name = "{name}";
    string symbol = "{symbol}";
    uint256 totalSupply = {total_supply};
    mapping(address => uint256) balances;
    mapping(address => mapping(address => uint256)) allowances;
  }}

  constructor() {{
    balances[msg.sender] = totalSupply;
  }}

  function balanceOf(address account) public view returns (uint256) {{
    return balances[account];
  }}

  function transfer(address to, uint256 amount) public returns (bool) {{
    require(balances[msg.sender] >= amount, "Insufficient balance");
    balances[msg.sender] -= amount;
    balances[to] += amount;
    emit Transfer(msg.sender, to, amount);
    return true;
  }}

  function approve(address spender, uint256 amount) public returns (bool) {{
    allowances[msg.sender][spender] = amount;
    emit Approval(msg.sender, spender, amount);
    return true;
  }}

  function transferFrom(address from, address to, uint256 amount) public returns (bool) {{
    require(balances[from] >= amount, "Insufficient balance");
    require(allowances[from][msg.sender] >= amount, "Insufficient allowance");
    balances[from] -= amount;
    balances[to] += amount;
    allowances[from][msg.sender] -= amount;
    emit Transfer(from, to, amount);
    return true;
  }}

  event Transfer(address indexed from, address indexed to, uint256 value);
  event Approval(address indexed owner, address indexed spender, uint256 value);
}}
        '''
        
        deployment = self.client.deploy_contract(token_code)
        self.contract_address = deployment.contract_address
        return deployment
    
    def balance_of(self, address: str) -> str:
        """Get token balance for an address"""
        if not self.contract_address:
            raise RuntimeError("Contract not deployed")
        result = self.client.query_contract(
            self.contract_address,
            "balanceOf",
            [address]
        )
        return result.data
    
    def transfer(self, to: str, amount: str):
        """Transfer tokens to another address"""
        if not self.contract_address:
            raise RuntimeError("Contract not deployed")
        return self.client.execute_transaction(
            self.contract_address,
            "transfer",
            [to, amount]
        )
    
    def approve(self, spender: str, amount: str):
        """Approve spender to use tokens"""
        if not self.contract_address:
            raise RuntimeError("Contract not deployed")
        return self.client.execute_transaction(
            self.contract_address,
            "approve",
            [spender, amount]
        )


class NFTContract:
    """
    Helper class for NFT (non-fungible token) contracts
    
    Example:
        >>> nft = NFTContract(client)
        >>> deployment = nft.deploy("MyNFT", "MNFT")
        >>> nft.mint("0x...", "ipfs://metadata-uri")
    """
    
    def __init__(self, client: AgefixClient, contract_address: Optional[str] = None):
        """
        Initialize NFT contract helper
        
        Args:
            client: AgefixClient instance
            contract_address: Address of existing contract (optional)
        """
        self.client = client
        self.contract_address = contract_address
    
    def deploy(self, name: str, symbol: str):
        """
        Deploy a new NFT contract
        
        Args:
            name: NFT collection name
            symbol: NFT collection symbol
            
        Returns:
            ContractDeployment info
        """
        nft_code = f'''
contract NFT {{
  state {{
    string name = "{name}";
    string symbol = "{symbol}";
    uint256 nextTokenId = 1;
    mapping(uint256 => address) owners;
    mapping(uint256 => string) tokenURIs;
    mapping(address => uint256) balances;
  }}

  function mint(address to, string memory uri) public returns (uint256) {{
    uint256 tokenId = nextTokenId++;
    owners[tokenId] = to;
    tokenURIs[tokenId] = uri;
    balances[to]++;
    emit Mint(to, tokenId, uri);
    return tokenId;
  }}

  function ownerOf(uint256 tokenId) public view returns (address) {{
    return owners[tokenId];
  }}

  function tokenURI(uint256 tokenId) public view returns (string memory) {{
    return tokenURIs[tokenId];
  }}

  function balanceOf(address owner) public view returns (uint256) {{
    return balances[owner];
  }}

  event Mint(address indexed to, uint256 indexed tokenId, string uri);
}}
        '''
        
        deployment = self.client.deploy_contract(nft_code)
        self.contract_address = deployment.contract_address
        return deployment
    
    def mint(self, to: str, uri: str):
        """Mint a new NFT"""
        if not self.contract_address:
            raise RuntimeError("Contract not deployed")
        return self.client.execute_transaction(
            self.contract_address,
            "mint",
            [to, uri]
        )
    
    def owner_of(self, token_id: int) -> str:
        """Get NFT owner"""
        if not self.contract_address:
            raise RuntimeError("Contract not deployed")
        result = self.client.query_contract(
            self.contract_address,
            "ownerOf",
            [token_id]
        )
        return result.data
