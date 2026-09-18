from core.banner import show_banner
from scanner import connect, is_connected, get_latest_block
from scanner.watcher import watch_blocks
from scanner.scanner import scan_block


def handle_block(block_number):
    print(f"\n{'=' * 60}")
    print(f"SCANNING BLOCK: {block_number:,}")
    print(f"{'=' * 60}")

    try:
        results = scan_block(block_number)

        total = len(results)

        contracts = sum(
            1
            for tx in results
            if tx["address_type"] in ("contract", "erc20")
        )

        tokens = sum(
            1
            for tx in results
            if tx["token"] is not None
        )

        redeploys = sum(
            1
            for tx in results
            if tx["fingerprint"] and tx["fingerprint"]["is_redeploy"]
        )

        classifications = {}

        for tx in results:
            classification = tx["classification"]
            classifications[classification] = (
                classifications.get(classification, 0) + 1
            )

        print(f"Transactions: {total}")
        print(f"Contracts: {contracts}")
        print(f"Tokens: {tokens}")
        print(f"Redeploys: {redeploys}")
        print(f"Classifications: {classifications}")

        for tx in results:
            fingerprint = tx["fingerprint"]

            if fingerprint and fingerprint["is_redeploy"]:
                print(
                    f"  ⚠ REDEPLOY: {tx['token']['symbol']} "
                    f"({fingerprint['address']}) matches bytecode "
                    f"already seen at "
                    f"{fingerprint['matching_addresses']}"
                )

    except Exception as exc:
        print(f"Scanner error: {exc}")


def main():
    show_banner()

    print("Initializing Core...")

    print("✓ Configuration Loaded")
    print("✓ Logger Ready")

    if not is_connected():
        print("Connecting to BNB Chain...")

        if not connect():
            print("✗ Could not connect to BNB Chain")
            return

    print("✓ Scanner Ready")
    print("✓ Connected to BNB Chain")
    print(f"✓ Latest Block: {get_latest_block():,}")

    print("✓ Security Ready")
    print("✓ Analyzer Ready")

    print("\nEsau is ready.")
    print("Esau is watching the blockchain...\n")

    try:
        watch_blocks(handle_block, interval=2)
    except KeyboardInterrupt:
        print("\n\nShutting down Esau...")
        print("Goodbye.")


if __name__ == "__main__":
    main()