from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware


RPC_URLS = [
    "https://bsc-rpc.publicnode.com",
    "https://bsc-dataseed.binance.org/",
    "https://bsc-dataseed1.binance.org/",
    "https://bsc-dataseed2.binance.org/",
    "https://bsc-dataseed3.binance.org/",
]

w3 = None
current_rpc = None


def connect() -> bool:
    global w3, current_rpc

    for url in RPC_URLS:
        try:
            print(f"Trying RPC: {url}")

            candidate = Web3(
                Web3.HTTPProvider(
                    url,
                    request_kwargs={"timeout": 10},
                )
            )

            candidate.middleware_onion.inject(
                ExtraDataToPOAMiddleware,
                layer=0,
            )

            if candidate.is_connected():
                w3 = candidate
                current_rpc = url

                print(f"✓ Connected to: {url}")
                return True

        except Exception as exc:
            print(f"✗ RPC failed: {exc}")

    w3 = None
    current_rpc = None
    return False


def is_connected() -> bool:
    return w3 is not None and w3.is_connected()


def to_checksum(address):
    return Web3.to_checksum_address(address)


def get_latest_block() -> int:
    if not is_connected():
        if not connect():
            raise ConnectionError("No working BNB Chain RPC available.")

    return w3.eth.block_number