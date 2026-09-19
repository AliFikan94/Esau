import os
import sys
import time
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

from investigate import investigate
from storage.database import record_query, record_feedback, initialize_database

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_CHAT_ID = os.getenv("OWNER_CHAT_ID")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

MAX_MESSAGE_LENGTH = 4000

WELCOME_TEXT = (
    "Send me a BNB Chain contract address or a token name/symbol "
    "and I'll investigate it.\n\n"
    "Use /feedback <message> anytime to tell me what's working or not."
)


def send_message(chat_id, text):
    for start in range(0, len(text), MAX_MESSAGE_LENGTH):
        chunk = text[start:start + MAX_MESSAGE_LENGTH]

        requests.post(
            f"{API_URL}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": f"```\n{chunk}\n```",
                "parse_mode": "Markdown",
            },
            timeout=10,
        )


def handle_message(chat_id, text):
    query = text.strip()

    if not query:
        return

    if query.startswith("/feedback"):
        parts = query.split(maxsplit=1)
        message = parts[1] if len(parts) > 1 else ""

        if not message:
            send_message(chat_id, "Usage: /feedback <your message>")
            return

        record_feedback(
            chat_id, message, datetime.now(timezone.utc).isoformat()
        )

        if OWNER_CHAT_ID:
            send_message(OWNER_CHAT_ID, f"Feedback from {chat_id}: {message}")

        send_message(chat_id, "Thanks — got it.")
        return

    if query.startswith("/"):
        parts = query.split(maxsplit=1)
        query = parts[1] if len(parts) > 1 else ""

        if not query:
            send_message(chat_id, WELCOME_TEXT)
            return

    record_query(chat_id, query, datetime.now(timezone.utc).isoformat())

    send_message(chat_id, f"Investigating \"{query}\"...")

    try:
        result = investigate(query)
    except Exception as exc:
        result = f"✗ Investigation failed: {exc}"

    send_message(chat_id, result)


def run():
    if not BOT_TOKEN:
        print("✗ TELEGRAM_BOT_TOKEN not set. Add it to your .env file.")
        sys.exit(1)

    initialize_database()

    print("Esau bot is listening...")

    offset = None

    while True:
        try:
            response = requests.get(
                f"{API_URL}/getUpdates",
                params={"timeout": 30, "offset": offset},
                timeout=35,
            )
            response.raise_for_status()

            updates = response.json().get("result", [])

            for update in updates:
                offset = update["update_id"] + 1

                message = update.get("message")

                if not message or "text" not in message:
                    continue

                handle_message(message["chat"]["id"], message["text"])

        except KeyboardInterrupt:
            print("\n\nShutting down Esau bot...")
            break

        except Exception as exc:
            print(f"✗ Bot error: {exc}")
            time.sleep(5)


if __name__ == "__main__":
    run()
