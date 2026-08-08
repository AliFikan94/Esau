from .blocks import get_block


def get_transactions(block_number):
    """
    Return all transactions in a block.
    """
    block = get_block(block_number)
    return block.transactions


