import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "esau.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection
def save_token(token):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO tokens (
            address,
            name,
            symbol,
            decimals,
            total_supply,
            first_seen_block,
            first_seen_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        token["address"],
        token.get("name"),
        token.get("symbol"),
        token.get("decimals"),
        str(token.get("total_supply")),
        token.get("first_seen_block"),
        token.get("first_seen_at"),
    ))

    connection.commit()
    connection.close()


def get_token(address):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM tokens
        WHERE address = ?
    """, (address,))

    token = cursor.fetchone()

    connection.close()

    return dict(token) if token else None


def search_tokens(name):
    connection = get_connection()

    cursor = connection.cursor()

    pattern = f"%{name}%"

    cursor.execute("""
        SELECT *
        FROM tokens
        WHERE name LIKE ? COLLATE NOCASE
        OR symbol LIKE ? COLLATE NOCASE
        ORDER BY first_seen_at
    """, (pattern, pattern))

    matches = cursor.fetchall()

    connection.close()

    return [dict(match) for match in matches]


def token_exists(address):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT 1
        FROM tokens
        WHERE address = ?
    """, (address,))

    exists = cursor.fetchone() is not None

    connection.close()

    return exists


def save_fingerprint(fingerprint):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO contract_fingerprints (
            address,
            bytecode_hash,
            first_seen_block,
            first_seen_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        fingerprint["address"],
        fingerprint["bytecode_hash"],
        fingerprint.get("first_seen_block"),
        fingerprint.get("first_seen_at"),
    ))

    connection.commit()
    connection.close()


def get_fingerprint(address):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM contract_fingerprints
        WHERE address = ?
    """, (address,))

    fingerprint = cursor.fetchone()

    connection.close()

    return dict(fingerprint) if fingerprint else None


def find_fingerprints_by_hash(bytecode_hash, exclude_address=None):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM contract_fingerprints
        WHERE bytecode_hash = ?
        AND address != ?
    """, (bytecode_hash, exclude_address or ""))

    matches = cursor.fetchall()

    connection.close()

    return [dict(match) for match in matches]


def record_transfer(transfer):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO transfers (
            tx_hash,
            from_address,
            to_address,
            value,
            block_number,
            seen_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        transfer["tx_hash"],
        transfer["from_address"],
        transfer["to_address"],
        str(transfer["value"]),
        transfer.get("block_number"),
        transfer.get("seen_at"),
    ))

    connection.commit()
    connection.close()


def get_earliest_incoming_transfer(address):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM transfers
        WHERE to_address = ?
        ORDER BY block_number ASC, id ASC
        LIMIT 1
    """, (address,))

    transfer = cursor.fetchone()

    connection.close()

    return dict(transfer) if transfer else None


def count_transfers_involving(address):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM transfers
        WHERE from_address = ? OR to_address = ?
    """, (address, address))

    row = cursor.fetchone()

    connection.close()

    return row["count"]


def record_query(chat_id, query, asked_at):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO queries (chat_id, query, asked_at)
        VALUES (?, ?, ?)
    """, (str(chat_id), query, asked_at))

    connection.commit()
    connection.close()


def record_feedback(chat_id, message, submitted_at):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO feedback (chat_id, message, submitted_at)
        VALUES (?, ?, ?)
    """, (str(chat_id), message, submitted_at))

    connection.commit()
    connection.close()


def initialize_database():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT UNIQUE NOT NULL,
            name TEXT,
            symbol TEXT,
            decimals INTEGER,
            total_supply TEXT,
            first_seen_block INTEGER,
            first_seen_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contract_fingerprints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT UNIQUE NOT NULL,
            bytecode_hash TEXT NOT NULL,
            first_seen_block INTEGER,
            first_seen_at TEXT
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_fingerprints_hash
        ON contract_fingerprints (bytecode_hash)
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transfers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tx_hash TEXT UNIQUE NOT NULL,
            from_address TEXT NOT NULL,
            to_address TEXT NOT NULL,
            value TEXT NOT NULL,
            block_number INTEGER,
            seen_at TEXT
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_transfers_to
        ON transfers (to_address)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_transfers_from
        ON transfers (from_address)
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT,
            query TEXT NOT NULL,
            asked_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT,
            message TEXT NOT NULL,
            submitted_at TEXT
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized: {DB_PATH}")