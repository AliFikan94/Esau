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


def format_name_search(name):
    matches = search_tokens(name)

    lines = [f"{'=' * 60}", f"ESAU NAME SEARCH: \"{name}\"", f"{'=' * 60}"]

    if not matches:
        lines.append("No matches in Esau's memory yet.")
        lines.append(
            "That is not a safety signal — Esau simply hasn't "
            "investigated anything by that name."
        )
        lines.append(f"{'=' * 60}")
        return "\n".join(lines)

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
        lines.append(f"{len(enriched)} DIFFERENT contracts share this name.")
        lines.append(
            "A shared name is not proof of a relationship. Ranked "
            "below by transfer activity Esau has personally "
            "observed — this is an activity signal, not a safety "
            "verdict."
        )
        lines.append("")
    else:
        lines.append("1 match in memory.")
        lines.append("")

    for token in enriched:
        lines.append(f"  {token['symbol']} — {token['name']}")
        lines.append(f"  {token['address']}")
        lines.append(
            f"  First seen: {token['first_seen_at']} "
            f"(block {token['first_seen_block']})"
        )
        lines.append(f"  Transfers observed by Esau: {token['activity_count']}")

        redeploy = token["redeploy"]

        if redeploy and redeploy["is_redeploy"]:
            lines.append(
                f"  ⚠ Bytecode matches: {redeploy['matching_addresses']}"
            )

        lines.append("")

    lines.append(f"{'=' * 60}")

    return "\n".join(lines)


def format_address_case_file(address):
    if not is_connected():
        if not connect():
            return "✗ Could not connect to BNB Chain"

    address = to_checksum(address)

    address_type = get_contract_type(address)

    lines = [f"{'=' * 60}", f"ESAU CASE FILE: {address}", f"{'=' * 60}"]
    lines.append(f"Address type: {address_type}")

    if address_type == "wallet":
        funding = get_earliest_incoming_transfer(address)

        if funding:
            lines.append("Earliest funding observed by Esau:")
            lines.append(
                f"  {funding['value']} wei from {funding['from_address']}"
            )
            lines.append(f"  at block {funding['block_number']}")
        else:
            lines.append("No funding history observed by Esau yet.")
            lines.append(
                "Esau only knows transfers it has personally watched "
                "live — this is not proof none exist."
            )

        lines.append(f"{'=' * 60}")
        return "\n".join(lines)

    if address_type != "erc20":
        lines.append(
            "Not an ERC-20 contract — nothing further to investigate yet."
        )
        lines.append(f"{'=' * 60}")
        return "\n".join(lines)

    token_info = get_token_info(address)

    lines.append(f"Name: {token_info['name']}")
    lines.append(f"Symbol: {token_info['symbol']}")
    lines.append(f"Decimals: {token_info['decimals']}")
    lines.append(f"Total supply: {token_info['total_supply']}")

    remembered = get_token(address)

    if remembered:
        lines.append(
            f"Memory: KNOWN (first seen block {remembered['first_seen_block']})"
        )
        seen_at = remembered["first_seen_at"]
        block = remembered["first_seen_block"]
    else:
        lines.append("Memory: NEW to Esau")

        seen_at = datetime.now(timezone.utc).isoformat()
        block = None

        save_token({
            **token_info,
            "first_seen_block": block,
            "first_seen_at": seen_at,
        })

    fingerprint = check_fingerprint(address, block, seen_at)

    if fingerprint["is_redeploy"]:
        lines.append(
            f"⚠ REDEPLOY: bytecode matches "
            f"{fingerprint['matching_addresses']}"
        )
    else:
        lines.append("Bytecode: no prior match in memory")

    lines.append(f"{'=' * 60}")

    return "\n".join(lines)


def investigate(query):
    initialize_database()

    if Web3.is_address(query):
        return format_address_case_file(query)

    return format_name_search(query)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python investigate.py <address or name>")
        sys.exit(1)

    print("\n" + investigate(sys.argv[1]) + "\n")
