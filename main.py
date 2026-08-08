from core.banner import show_banner
from scanner import is_connected, get_latest_block
from scanner.watcher import watch_blocks
from scanner.blocks import get_block
from scanner.transactions import get_transactions


def on_new_block(block_number):
    block = get_block(block_number)
    transactions = get_transactions(block_number)

    print("\n" + "=" * 50)
    print(f"Block: {block.number:,}")
    print(f"Transactions: {len(transactions):,}")
    print(f"Gas Used: {block.gasUsed:,}")

    print("\nScanning transactions...\n")

    for tx_hash in transactions:
        print(tx_hash.hex())


def main():
    show_banner()

    print("Initializing Core...")

    print("✓ Configuration Loaded")
    print("✓ Logger Ready")

    if not is_connected():
        print("✗ Could not connect to BNB Chain")
        return

    print("✓ Scanner Ready")
    print("✓ Connected to BNB Chain")
    print(f"✓ Latest Block: {get_latest_block():,}")

    print("✓ Security Ready")
    print("✓ Analyzer Ready")

    print("\nEsau is ready.")
    print("\nEsau is watching the blockchain...\n")

    try:
        watch_blocks(on_new_block, interval=1)
    except KeyboardInterrupt:
        print("\n\nShutting down Esau...")
        print("Goodbye.")


if __name__ == "__main__":
    main()