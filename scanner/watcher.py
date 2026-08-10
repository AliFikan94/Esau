import time

from . import rpc


def watch_blocks(callback, interval=2):
    """
    Watch BNB Chain for new blocks.

    When a new block appears, pass its block number
    to the supplied callback.
    """

    if not rpc.is_connected():
        if not rpc.connect():
            raise ConnectionError(
                "No working BNB Chain RPC available."
            )

    last_block = rpc.w3.eth.block_number

    print(f"Watching from block {last_block:,}")

    while True:
        try:
            current = rpc.w3.eth.block_number

            if current > last_block:
                for block_number in range(
                    last_block + 1,
                    current + 1,
                ):
                    print(f"New block: {block_number:,}")
                    callback(block_number)

                last_block = current

        except Exception as exc:
            print(f"Watcher error: {exc}")

            # Try to reconnect if the current RPC dies.
            if not rpc.connect():
                print("Waiting for RPC connection...")

        time.sleep(interval)
