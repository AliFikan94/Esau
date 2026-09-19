import sys
from datetime import datetime, timezone

from web3 import Web3

from scanner.contracts import get_contract_type, get_token_info
from scanner.rpc import connect, is_connected, to_checksum
from storage.database import (
    get_token,
    save_token,
    search_tokens,
    get_earliest_incoming_transfer,
    count_transfers_involving,
    initialize_database,
)
from provenance.fingerprint import check_fingerprint, get_stored_redeploy_status


def search_by_name(name):
    matches = search_tokens(name)

    print(f"\n{'=' * 60}")
    print(f"ESAU NAME SEARCH: \"{name}\"")
    print(f"{'=' * 60}")

    if not matches:
        print("No matches in Esau's memory yet.")
        print(
            "That is not a safety signal — Esau simply hasn't "
            "investigated anything by that name."
        )
        print(f"{'=' * 60}\n")
        return

    enriched = [
        {
            **token,
            "activity_count": count_transfers_involving(token["address"]),
            "redeploy": get_stored_redeploy_status(token["address"]),
        }
        for token in matches
    ]

    enriched.sort(key=lambda token: token["activity_count"], reverse=True)

    if len(enriched) > 1:
        print(f"{len(enriched)} DIFFERENT contracts share this name.")
        print(
            "A shared name is not proof of a relationship. Ranked "
            "below by transfer activity Esau has personally "
            "observed — this is an activity signal, not a safety "
            "verdict.\n"
        )
    else:
        print("1 match in memory.\n")

    for token in enriched:
        print(f"  {token['symbol']} — {token['name']}")
        print(f"  {token['address']}")
        print(
            f"  First seen: {token['first_seen_at']} "
            f"(block {token['first_seen_block']})"
        )
        print(f"  Transfers observed by Esau: {token['activity_count']}")

        redeploy = token["redeploy"]

        if redeploy and redeploy["is_redeploy"]:
            print(
                f"  ⚠ Bytecode matches: {redeploy['matching_addresses']}"
            )

        print()

    print(f"{'=' * 60}\n")


def investigate_address(address):
    if not is_connected():
        if not connect():
            print("✗ Could not connect to BNB Chain")
            return

    address = to_checksum(address)

    address_type = get_contract_type(address)

    print(f"\n{'=' * 60}")
    print(f"ESAU CASE FILE: {address}")
    print(f"{'=' * 60}")
    print(f"Address type: {address_type}")

    if address_type == "wallet":
        funding = get_earliest_incoming_transfer(address)

        if funding:
            print(f"Earliest funding observed by Esau:")
            print(f"  {funding['value']} wei from {funding['from_address']}")
            print(f"  at block {funding['block_number']}")
        else:
            print("No funding history observed by Esau yet.")
            print(
                "Esau only knows transfers it has personally watched "
                "live — this is not proof none exist."
            )

        print(f"{'=' * 60}\n")
        return

    if address_type != "erc20":
        print("Not an ERC-20 contract — nothing further to investigate yet.")
        print(f"{'=' * 60}\n")
        return

    token_info = get_token_info(address)

    print(f"Name: {token_info['name']}")
    print(f"Symbol: {token_info['symbol']}")
    print(f"Decimals: {token_info['decimals']}")
    print(f"Total supply: {token_info['total_supply']}")

    remembered = get_token(address)

    if remembered:
        print(f"Memory: KNOWN (first seen block {remembered['first_seen_block']})")
        seen_at = remembered["first_seen_at"]
        block = remembered["first_seen_block"]
    else:
        print("Memory: NEW to Esau")

        seen_at = datetime.now(timezone.utc).isoformat()
        block = None

        save_token({
            **token_info,
            "first_seen_block": block,
            "first_seen_at": seen_at,
        })

    fingerprint = check_fingerprint(address, block, seen_at)

    if fingerprint["is_redeploy"]:
        print(
            f"⚠ REDEPLOY: bytecode matches "
            f"{fingerprint['matching_addresses']}"
        )
    else:
        print("Bytecode: no prior match in memory")

    print(f"{'=' * 60}\n")


def investigate(query):
    initialize_database()

    if Web3.is_address(query):
        investigate_address(query)
    else:
        search_by_name(query)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python investigate.py <address or name>")
        sys.exit(1)

    investigate(sys.argv[1])
