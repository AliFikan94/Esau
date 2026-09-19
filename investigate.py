import sys
from datetime import datetime, timezone

from scanner.contracts import get_contract_type, get_token_info
from scanner.rpc import connect, is_connected
from storage.database import get_token, save_token
from provenance.fingerprint import check_fingerprint


def investigate(address):
    if not is_connected():
        if not connect():
            print("✗ Could not connect to BNB Chain")
            return

    address_type = get_contract_type(address)

    print(f"\n{'=' * 60}")
    print(f"ESAU CASE FILE: {address}")
    print(f"{'=' * 60}")
    print(f"Address type: {address_type}")

    if address_type != "erc20":
        print("Not an ERC-20 token — nothing further to investigate yet.")
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


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python investigate.py <address>")
        sys.exit(1)

    investigate(sys.argv[1])
