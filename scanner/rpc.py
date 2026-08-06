import os
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

RPC_URL = os.getenv(
    "RPC_URL",
    "https://bsc-dataseed.binance.org/"
)

w3 = Web3(Web3.HTTPProvider(RPC_URL))

w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)


def is_connected() -> bool:
    return w3.is_connected()


def get_latest_block():
    return w3.eth.block_number