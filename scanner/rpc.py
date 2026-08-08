from web3 import Web3


RPC_URLS = [
    "https://bsc-rpc.publicnode.com",
    "https://bsc-dataseed.binance.org/",
    "https://bsc-dataseed1.binance.org/",
    "https://bsc-dataseed2.binance.org/",
    "https://bsc-dataseed3.binance.org/",
]


w3 = None


def connect() -> bool:
    global w3

    for rpc_url in RPC_URLS:
        print(f"Trying RPC: {rpc_url}")

        try:
            candidate = Web3(
                Web3.HTTPProvider(
                    rpc_url,
                    request_kwargs={"timeout": 10},
                )
            
            )

            if candidate.is_connected():
                print(f"✓ Connected to: {rpc_url}")
                w3 = candidate
                return True

        except Exception as e:
            print(f"✗ Failed: {e}")

    w3 = None
    return False


def is_connected() -> bool:
    return w3 is not None and w3.is_connected()


def get_latest_block():
    if not is_connected():
        if not connect():
            raise ConnectionError("No working BNB Chain RPC available.")

    return w3.eth.block_number