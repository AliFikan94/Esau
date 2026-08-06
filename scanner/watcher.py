import time
from .rpc import w3


def watch_blocks(callback, interval=2):
    last_block = w3.eth.block_number

    print(f"Watching from block {last_block:,}")

    while True:
        current = w3.eth.block_number

        if current > last_block:
            for block in range(last_block + 1, current + 1):
                callback(block)

            last_block = current

        time.sleep(interval)