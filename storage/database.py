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

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized: {DB_PATH}")