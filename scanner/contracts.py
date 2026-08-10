from . import rpc


ERC20_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function",
    },
]


def _ensure_connection():
    if not rpc.is_connected():
        if not rpc.connect():
            raise ConnectionError(
                "No working BNB Chain RPC available."
            )


def is_contract(address):
    if not address:
        return False

    _ensure_connection()

    code = rpc.w3.eth.get_code(address)

    return code not in (b"", b"0x")


def get_contract_type(address):
    """
    Classify an address as:
    - wallet
    - erc20
    - contract
    """

    if not address:
        return "unknown"

    if not is_contract(address):
        return "wallet"

    token = get_token_info(address)

    if token is not None:
        return "erc20"

    return "contract"


def get_token_info(address):
    """
    Try to identify a contract as an ERC-20 style token.

    Returns token metadata when all required ERC-20
    methods are available. Returns None otherwise.
    """

    if not is_contract(address):
        return None

    contract = rpc.w3.eth.contract(
        address=address,
        abi=ERC20_ABI,
    )

    try:
        name = contract.functions.name().call()
        symbol = contract.functions.symbol().call()
        decimals = contract.functions.decimals().call()
        total_supply = contract.functions.totalSupply().call()

        return {
            "address": address,
            "name": name,
            "symbol": symbol,
            "decimals": decimals,
            "total_supply": total_supply,
            "is_token": True,
        }

    except Exception:
        return None