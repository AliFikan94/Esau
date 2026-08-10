from .blocks import get_block_transactions
from .transactions import inspect_transaction, classify_transaction
from .contracts import get_contract_type, get_token_info


def scan_block(block_number):
    transactions = get_block_transactions(block_number)

    results = []

    for tx in transactions:
        inspected = inspect_transaction(tx)

        to_address = tx.get("to")

        if not to_address:
            address_type = "contract_creation"
            token_info = None

        else:
            address_type = get_contract_type(to_address)

            if address_type == "erc20":
                token_info = get_token_info(to_address)
            else:
                token_info = None

        results.append({
            **inspected,
            "classification": classify_transaction(tx),
            "address_type": address_type,
            "token": token_info,
        })

    return results