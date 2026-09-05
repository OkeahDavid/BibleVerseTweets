"""Minimal Telegram Bot API client: send messages, and long-poll for commands.

No python-telegram-bot dependency -- the Bot API is a plain HTTPS/JSON API and
this project only needs sendMessage and getUpdates, so a thin wrapper over
`requests` keeps the dependency list small.
"""

import time

import requests

API_ROOT = "https://api.telegram.org/bot{token}/{method}"


def send_message(token, chat_id, text):
    url = API_ROOT.format(token=token, method="sendMessage")
    response = requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=10)
    response.raise_for_status()
    return response.json()


def _get_updates(token, offset=None, timeout=30):
    url = API_ROOT.format(token=token, method="getUpdates")
    params = {"timeout": timeout}
    if offset is not None:
        params["offset"] = offset
    response = requests.get(url, params=params, timeout=timeout + 10)
    response.raise_for_status()
    return response.json()["result"]


def run_bot(token, handle_command):
    """Long-poll for incoming messages and dispatch commands.

    `handle_command` is called as handle_command(command, chat_id) for every
    message that starts with "/", and should return the reply text (or None
    to send nothing).
    """
    print("Bot is running. Press Ctrl+C to stop.")
    offset = None
    while True:
        try:
            updates = _get_updates(token, offset=offset)
        except requests.RequestException as error:
            print(f"Warning: failed to fetch updates: {error}")
            time.sleep(5)
            continue

        for update in updates:
            offset = update["update_id"] + 1
            message = update.get("message", {})
            text = message.get("text", "")
            chat_id = message.get("chat", {}).get("id")

            if not text.startswith("/") or chat_id is None:
                continue

            command = text.split()[0].lstrip("/").split("@")[0]
            reply = handle_command(command, chat_id)
            if reply:
                send_message(token, chat_id, reply)
