from .blocks import get_block_transactions


def get_transactions(block_number):
    """
    Return all full transactions in a block.
    """
    return get_block_transactions(block_number)


def inspect_transaction(tx):
    """
    Convert a Web3 transaction into a clean dictionary.
    """

    return {
        "hash": tx["hash"].hex(),
        "from": tx["from"],
        "to": tx["to"],
        "value": tx["value"],
        "gas": tx["gas"],
        "gas_price": tx["gasPrice"],
        "input": tx["input"].hex(),
        "block_number": tx["blockNumber"],
        "transaction_index": tx["transactionIndex"],
    }

def classify_transaction(tx):
    """
    Basic transaction classification.
    """

    input_data = tx["input"]

    if isinstance(input_data, bytes):
        input_data = input_data.decode(
            "utf-8",
            errors="ignore",
        )

    if "Block built by Puissant" in input_data:
        return "infrastructure"

    if tx["to"] is None:
        return "contract_creation"

    return "contract_interaction"