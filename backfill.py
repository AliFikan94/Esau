import sys

from scanner import connect, is_connected, get_latest_block
from scanner.scanner import scan_block
from storage.database import initialize_database


def backfill(block_count):
    initialize_database()

    if not is_connected():
        if not connect():
            print("✗ Could not connect to BNB Chain")
            return

    latest = get_latest_block()
    target = max(latest - block_count, 0)

    print(f"\n{'=' * 60}")
    print(f"ESAU BACKFILL: walking back {block_count} blocks")
    print(f"From block {latest:,} toward block {target:,}")
    print(f"{'=' * 60}\n")

    block_number = latest
    scanned = 0

    try:
        while block_number > target:
            try:
                scan_block(block_number)
                scanned += 1

                if scanned % 100 == 0:
                    print(
                        f"  ...scanned {scanned} blocks, "
                        f"now at block {block_number:,}"
                    )

            except Exception as exc:
                print(f"\n✗ Stopped at block {block_number:,}: {exc}")
                print(
                    "This RPC has likely stopped serving blocks this "
                    "old — that is expected, not a bug."
                )
                break

            block_number -= 1

    except KeyboardInterrupt:
        print("\n\nBackfill interrupted by user.")

    print(f"\n{'=' * 60}")
    print(f"Backfill finished: {scanned} blocks scanned")
    print(
        f"Funding and activity history now reaches back to "
        f"block {block_number + 1:,}"
    )
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Usage: python backfill.py <number of blocks>")
        sys.exit(1)

    backfill(int(sys.argv[1]))
