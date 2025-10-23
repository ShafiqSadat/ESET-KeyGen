#!/usr/bin/env python3
"""
Educational License Key Generator

This script demonstrates how to generate a random alphanumeric code and send it to a Telegram chat
via the Telegram Bot API. It is intended for educational purposes only and does not interface
with or activate any commercial software. You should replace the environment variables with
your own Telegram bot token and chat ID to test sending messages.

Usage:
    Set the TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables and run this script.
"""

import os
import random
import string
import requests


def generate_key(length: int = 20) -> str:
    """Generate a random uppercase alphanumeric key of a given length."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def send_key_via_telegram(token: str, chat_id: str, key: str) -> bool:
    """Send the generated key to a Telegram chat.

    Args:
        token: The API token for your Telegram bot.
        chat_id: The chat ID where the message should be sent.
        key: The license key string to send.

    Returns:
        True if the message was sent successfully, False otherwise.
    """
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    # Escape backticks for MarkdownV2 formatting
    message = f"🔐 Your sample license key: `{key}`"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "MarkdownV2",
    }
    response = requests.post(url, data=data, timeout=10)
    return response.status_code == 200


def main() -> None:
    """Main function to generate and send a key."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.")
        return

    key = generate_key()
    if send_key_via_telegram(token, chat_id, key):
        print("Key sent successfully!")
    else:
        print("Failed to send key.")


if __name__ == "__main__":
    main()
