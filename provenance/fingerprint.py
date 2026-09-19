import hashlib

from scanner import rpc
from storage.database import (
    save_fingerprint,
    get_fingerprint,
    find_fingerprints_by_hash,
)


def _ensure_connection():
    if not rpc.is_connected():
        if not rpc.connect():
            raise ConnectionError("No working BNB Chain RPC available.")


def hash_bytecode(bytecode: bytes) -> str:
    return hashlib.sha256(bytecode).hexdigest()


def get_bytecode_hash(address):
    _ensure_connection()

    address = rpc.to_checksum(address)

    code = rpc.w3.eth.get_code(address)

    return hash_bytecode(code)


def check_fingerprint(address, block_number, seen_at):
    """
    Fingerprint a contract's bytecode and check it against every
    fingerprint Esau has already stored.

    A shared bytecode hash across two different addresses means the
    same contract was redeployed under a new address. It is not a
    verdict on intent, only evidence that the addresses are related.
    """

    address = rpc.to_checksum(address)

    bytecode_hash = get_bytecode_hash(address)

    matches = find_fingerprints_by_hash(
        bytecode_hash,
        exclude_address=address,
    )

    if not get_fingerprint(address):
        save_fingerprint({
            "address": address,
            "bytecode_hash": bytecode_hash,
            "first_seen_block": block_number,
            "first_seen_at": seen_at,
        })

    return {
        "address": address,
        "bytecode_hash": bytecode_hash,
        "is_redeploy": len(matches) > 0,
        "matching_addresses": [match["address"] for match in matches],
    }
