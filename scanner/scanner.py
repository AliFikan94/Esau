from datetime import datetime, timezone

from .blocks import get_block_transactions
from .transactions import inspect_transaction, classify_transaction
from .contracts import get_contract_type, get_token_info

from storage.database import get_token, save_token
from provenance.fingerprint import check_fingerprint


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

        memory_status = "not_applicable"
        remembered_token = None
        fingerprint = None

        if token_info:
            address = token_info["address"]

            remembered_token = get_token(address)

            if remembered_token:
                memory_status = "known"

            else:
                memory_status = "new"

                seen_at = datetime.now(timezone.utc).isoformat()

                token_to_save = {
                    **token_info,
                    "first_seen_block": block_number,
                    "first_seen_at": seen_at,
                }

                save_token(token_to_save)

                fingerprint = check_fingerprint(
                    address,
                    block_number,
                    seen_at,
                )

        results.append({
            **inspected,
            "classification": classify_transaction(tx),
            "address_type": address_type,
            "token": token_info,
            "memory_status": memory_status,
            "remembered_token": remembered_token,
            "fingerprint": fingerprint,
        })

    return results
