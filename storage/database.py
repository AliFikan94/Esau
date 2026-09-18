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

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized: {DB_PATH}")