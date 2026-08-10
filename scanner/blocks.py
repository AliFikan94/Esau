from . import rpc


def get_block(block_number):
    if not rpc.is_connected():
        if not rpc.connect():
            raise ConnectionError("No working BNB Chain RPC available.")

    return rpc.w3.eth.get_block(block_number)


def get_block_transactions(block_number):
    if not rpc.is_connected():
        if not rpc.connect():
            raise ConnectionError("No working BNB Chain RPC available.")

    block = rpc.w3.eth.get_block(
        block_number,
        full_transactions=True,
    )

    return block.transactions