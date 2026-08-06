from .rpc import w3


def get_block(block_number):
    return w3.eth.get_block(block_number)


def get_block_transactions(block_number):
    block = w3.eth.get_block(block_number, full_transactions=True)
    return block.transactions